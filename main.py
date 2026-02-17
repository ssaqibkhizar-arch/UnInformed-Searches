import pygame
import random

from dfs import dfsVisualizer
from bfs import bfsVisualizer
from ucs import ucsVisualizer
from dls import dlsVisualizer
from iddfs import iddfsVisualizer
from bds import bidirectionalVisualizer as bidirectionalVisualizer

WIDTH = 600
HEIGHT = 700 
ROWS = 20 

pygame.font.init()
STAT_FONT = pygame.font.SysFont('arial', 24, bold=True)
LEGEND_FONT = pygame.font.SysFont('arial', 14)
TITLE_FONT = pygame.font.SysFont('arial', 18, bold=True)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNINFORMED SEARCHES")

RED = (255, 65, 54)
GREEN = (46, 204, 64)
BLUE = (0, 116, 217)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)
PURPLE = (177, 13, 201)

class Node:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.parent = None 
        self.weight = 1
        self.neighbors = []
        self.totalRows = totalRows

    def getPos(self): return self.row, self.col
    def isWall(self): return self.color == BLACK
    
    def reset(self): 
        self.color = WHITE
        self.parent = None
        self.weight = 1
        
    def makeStart(self): self.color = TURQUOISE
    def makeWall(self): self.color = BLACK
    def makeEnd(self): self.color = YELLOW
    def makeClosed(self): self.color = RED
    def makeOpen(self): self.color = GREEN
    def makePath(self): self.color = BLUE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
        if self.weight > 1 and not self.isWall():
            weightFont = pygame.font.SysFont('arial', 12) 
            text = weightFont.render(str(self.weight), True, BLACK)
            win.blit(text, (self.x + self.width/2 - text.get_width()/2, 
                            self.y + self.width/2 - text.get_height()/2))

    def updateNeighbors(self, grid):
        self.neighbors = []
        
        # 1. UP
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():
            self.neighbors.append(grid[self.row - 1][self.col])

        # 2. RIGHT
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall():
            self.neighbors.append(grid[self.row][self.col + 1])

        # 3. BOTTOM
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall():
            self.neighbors.append(grid[self.row + 1][self.col])

        # 4. BOTTOM-RIGHT (Diagonal)
        if self.row < self.totalRows - 1 and self.col < self.totalRows - 1 and not grid[self.row + 1][self.col + 1].isWall():
            self.neighbors.append(grid[self.row + 1][self.col + 1])

        # 5. LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].isWall():
            self.neighbors.append(grid[self.row][self.col - 1])

        # 6. TOP-LEFT (Diagonal)
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].isWall():
            self.neighbors.append(grid[self.row - 1][self.col - 1])

def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def drawUI(win, width, statusText, algoName="None"):
    uiBgColor = (235, 235, 235) 
    pygame.draw.rect(win, uiBgColor, (0, width, width, 100))
    pygame.draw.line(win, (50, 50, 50), (0, width), (width, width), 2) 

    algoSurface = STAT_FONT.render(f"Algo: {algoName}", True, (0, 50, 150)) 
    win.blit(algoSurface, (15, width + 15))

    if len(statusText) > 30: 
        smallStatFont = pygame.font.SysFont('arial', 12)
        statusSurface = smallStatFont.render(f"Status: {statusText}", True, BLACK)
    else:
        statusSurface = LEGEND_FONT.render(f"Status: {statusText}", True, BLACK)
        
    win.blit(statusSurface, (15, width + 50))

    pygame.draw.line(win, (180, 180, 180), (280, width + 10), (280, width + 90), 2) 
    
    ctrlTitle = TITLE_FONT.render("Controls", True, (50, 50, 50))
    win.blit(ctrlTitle, (295, width + 15))
    
    c1 = LEGEND_FONT.render("1-6: Choose Algo", True, BLACK)
    c2 = LEGEND_FONT.render("Space: Start", True, BLACK)
    c3 = LEGEND_FONT.render("C: Clear Board", True, BLACK)
    
    win.blit(c1, (295, width + 40))
    win.blit(c2, (295, width + 58))
    win.blit(c3, (295, width + 76))

    pygame.draw.line(win, (180, 180, 180), (450, width + 10), (450, width + 90), 2) 

    def drawLegendItem(color, text, x, y):
        pygame.draw.rect(win, color, (x, y, 12, 12)) 
        pygame.draw.rect(win, BLACK, (x, y, 12, 12), 1)
        label = pygame.font.SysFont('arial', 11).render(text, True, (30,30,30))
        win.blit(label, (x + 18, y - 2))

    baseX = 460
    drawLegendItem(TURQUOISE, "Start", baseX, width + 20)
    drawLegendItem(GREEN, "Frontier", baseX, width + 45)
    drawLegendItem(BLUE, "Path", baseX, width + 70)

    baseX2 = 530
    drawLegendItem(YELLOW, "Target", baseX2, width + 20)
    drawLegendItem(RED, "Visited", baseX2, width + 45)

def draw(win, grid, rows, width, status, algoName):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    drawGrid(win, rows, width)
    drawUI(win, width, status, algoName)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def reconstructPath(endNode, drawFunc):
    curr = endNode
    while curr.parent:
        curr.makePath()
        curr = curr.parent
        drawFunc()
    curr.makeStart()
    curr.makePath()

def clearSearch(grid):
    for row in grid:
        for node in row:
            if node.color in {RED, GREEN, BLUE, PURPLE}:
                node.reset()
            node.parent = None

def generateRandomWeights(grid):
    for row in grid:
        for node in row:
            if node.color == WHITE:
                node.weight = random.randint(1, 9)

def resetWeights(grid):
    for row in grid:
        for node in row:
            node.weight = 1

def main(win, width):
    grid = makeGrid(ROWS, width)
    start = None
    end = None
    run = True
    
    currentAlgo = None
    algoName = "Select (1-6)"
    statusText = "Setup: Click Start & End -> Select Algo -> Space"

    while run:
        draw(win, grid, ROWS, width, statusText, algoName)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = getClickedPos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.makeStart()
                    elif not end and node != start:
                        end = node
                        end.makeEnd()

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = getClickedPos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start: start = None
                    elif node == end: end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    resetWeights(grid)
                    currentAlgo = bfsVisualizer
                    algoName = "BFS"
                
                elif event.key == pygame.K_2:
                    resetWeights(grid)
                    currentAlgo = dfsVisualizer
                    algoName = "DFS"

                elif event.key == pygame.K_3:
                    generateRandomWeights(grid)
                    currentAlgo = ucsVisualizer
                    algoName = "UCS (Weighted)"

                elif event.key == pygame.K_4:
                    resetWeights(grid)
                    currentAlgo = dlsVisualizer
                    algoName = "DLS"

                elif event.key == pygame.K_5:
                    resetWeights(grid)
                    currentAlgo = iddfsVisualizer
                    algoName = "IDDFS"

                elif event.key == pygame.K_6:
                    resetWeights(grid)
                    currentAlgo = bidirectionalVisualizer
                    algoName = "Bidirectional Search"
                
                if event.key == pygame.K_SPACE and start and end and currentAlgo:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    clearSearch(grid)
                    updateDisplay = lambda: draw(win, grid, ROWS, width, "Searching...", algoName)
                    
                    found = currentAlgo(updateDisplay, grid, start, end)
                    
                    if found:
                        if currentAlgo != bidirectionalVisualizer:
                            reconstructPath(end, updateDisplay)
                        statusText = "Success! Path Found."
                    else:
                        statusText = "Failed. No Path."

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)
                    statusText = "Setup: Cleared"
                    algoName = "Select (1-6)"
                    currentAlgo = None

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)