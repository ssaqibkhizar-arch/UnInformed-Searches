import pygame
import random
# Import algorithms
from dfs import dfs_visualizer 
# from bfs import bfs_visualizer
# You can add imports for ucs, dls, iddfs, bidirectional later

# --- CONFIGURATION ---
WIDTH = 600
HEIGHT = 700 
ROWS = 20 

# --- FONTS (Professional Look) ---
pygame.font.init()
# Arial is standard and clean. 'bold=True' makes headers pop.
STAT_FONT = pygame.font.SysFont('arial', 24, bold=True)       # For "Algo: BFS"
LEGEND_FONT = pygame.font.SysFont('arial', 14)                # For small text
TITLE_FONT = pygame.font.SysFont('arial', 18, bold=True)      # For section headers

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GOOD PERFORMANCE TIME APP")

# --- COLORS ---
RED = (255, 65, 54)      # Visited
GREEN = (46, 204, 64)    # Frontier
BLUE = (0, 116, 217)     # Path
YELLOW = (255, 220, 0)   # Target
WHITE = (255, 255, 255)  # Empty
BLACK = (20, 20, 20)     # Wall
TURQUOISE = (64, 224, 208) # Start
GREY = (128, 128, 128)   # Lines
PURPLE = (177, 13, 201)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.parent = None 

    def get_pos(self): return self.row, self.col
    def is_wall(self): return self.color == BLACK
    def reset(self): 
        self.color = WHITE
        self.parent = None
    def make_start(self): self.color = TURQUOISE
    def make_wall(self): self.color = BLACK
    def make_end(self): self.color = YELLOW
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_path(self): self.color = BLUE
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_ui(win, width, status_text, algo_name="None"):
    # 1. Background & Border (Clean Light Grey)
    ui_bg_color = (235, 235, 235) 
    pygame.draw.rect(win, ui_bg_color, (0, width, width, 100))
    pygame.draw.line(win, (50, 50, 50), (0, width), (width, width), 2) # Darker border

    # --- COLUMN 1: STATUS (Left, wider space) ---
    # Moved divider from x=240 to x=280 to prevent overlap
    
    # Algorithm Name
    algo_surface = STAT_FONT.render(f"Algo: {algo_name}", True, (0, 50, 150)) # Dark Blue
    win.blit(algo_surface, (15, width + 15))

    # Status Text (Text wrapping safety)
    if len(status_text) > 30: # If text is too long, shrink it slightly
        small_stat_font = pygame.font.SysFont('arial', 12)
        status_surface = small_stat_font.render(f"Status: {status_text}", True, BLACK)
    else:
        status_surface = LEGEND_FONT.render(f"Status: {status_text}", True, BLACK)
        
    win.blit(status_surface, (15, width + 50))

    # --- COLUMN 2: CONTROLS (Middle) ---
    pygame.draw.line(win, (180, 180, 180), (280, width + 10), (280, width + 90), 2) # Divider
    
    # Headers
    ctrl_title = TITLE_FONT.render("Controls", True, (50, 50, 50))
    win.blit(ctrl_title, (295, width + 15))
    
    # Instructions
    c1 = LEGEND_FONT.render("1-6: Choose Algo", True, BLACK)
    c2 = LEGEND_FONT.render("Space: Start", True, BLACK)
    c3 = LEGEND_FONT.render("C: Clear Board", True, BLACK)
    
    win.blit(c1, (295, width + 40))
    win.blit(c2, (295, width + 58))
    win.blit(c3, (295, width + 76))

    # --- COLUMN 3: LEGEND (Right) ---
    pygame.draw.line(win, (180, 180, 180), (450, width + 10), (450, width + 90), 2) # Divider

    def draw_legend_item(color, text, x, y):
        # Draw box with thin black outline
        pygame.draw.rect(win, color, (x, y, 12, 12)) 
        pygame.draw.rect(win, BLACK, (x, y, 12, 12), 1)
        # Text
        label = pygame.font.SysFont('arial', 11).render(text, True, (30,30,30))
        win.blit(label, (x + 18, y - 2))

    # Column A (Start, Open, Path)
    base_x = 460
    draw_legend_item(TURQUOISE, "Start", base_x, width + 20)
    draw_legend_item(GREEN, "Frontier", base_x, width + 45)
    draw_legend_item(BLUE, "Path", base_x, width + 70)

    # Column B (Target, Closed, Wall)
    base_x2 = 530
    draw_legend_item(YELLOW, "Target", base_x2, width + 20)
    draw_legend_item(RED, "Visited", base_x2, width + 45)
    draw_legend_item(BLACK, "Wall", base_x2, width + 70)

def draw(win, grid, rows, width, status, algo_name):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    draw_ui(win, width, status, algo_name)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def reconstruct_path(end_node, draw_func):
    curr = end_node
    while curr.parent:
        curr.make_path()
        curr = curr.parent
        draw_func()
    curr.make_start()
    curr.make_path()

def clear_search(grid):
    for row in grid:
        for node in row:
            if node.color in {RED, GREEN, BLUE, PURPLE}:
                node.reset()
            node.parent = None

# --- MAIN LOOP ---
def main(win, width):
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    
    # Algorithm Selection State
    current_algo = None
    algo_name = "Select (1-6)"
    status_text = "Setup: Click nodes -> Select Algo -> Space"

    while run:
        draw(win, grid, ROWS, width, status_text, algo_name)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # --- MOUSE HANDLING ---
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_wall()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start: start = None
                    elif node == end: end = None

            # --- KEYBOARD HANDLING ---
            if event.type == pygame.KEYDOWN:
                # Algorithm Selection
                if event.key == pygame.K_1:
                    current_algo = bfs_visualizer
                    algo_name = "BFS"
                elif event.key == pygame.K_2:
                    current_algo = dfs_visualizer
                    algo_name = "DFS"
                # Add others here later:
                # elif event.key == pygame.K_3: current_algo = ucs_visualizer; algo_name = "UCS"
                
                # Start Search
                if event.key == pygame.K_SPACE and start and end and current_algo:
                    clear_search(grid)
                    update_display = lambda: draw(win, grid, ROWS, width, "Searching...", algo_name)
                    
                    found = current_algo(update_display, grid, start, end)
                    
                    if found:
                        reconstruct_path(end, update_display)
                        status_text = "Success! Path Found."
                    else:
                        status_text = "Failed. No Path."

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    status_text = "Setup: Cleared"
                    algo_name = "Select (1-6)"
                    current_algo = None

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
