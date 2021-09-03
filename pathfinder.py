import pygame

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinder")

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.colour = WHITE

    def get_pos(self):
        return (self.row, self.col)
    
    def is_barrier(self):
        return self.colour == BLACK
    
    def is_start(self):
        return self.colour == BLUE

    def is_end(self):
        return self.colour == GREEN

    def set_barrier(self):
        self.colour = BLACK 

    def set_start(self):
        self.colour = BLUE

    def set_end(self):
        self.colour = GREEN

    def clear(self):
        self.colour = WHITE

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

def make_grid(rows, width):
    gap = width // rows
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(rows):
            cell = Cell(row, col, gap, rows)
            grid[col].append(cell)

    return grid

running = True
  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

