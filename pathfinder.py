import pygame

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinder")

BLACK = (0, 0, 0)
GREY = (127, 127, 127)
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
            grid[row].append(cell)

    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, GREY, (i * gap, 0), (i * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for i in row:
            i.draw(window)
    
    draw_grid(window, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col



rows = 80
grid = make_grid(rows, WIDTH)

start = None
end = None

started = False
running = True
  
while running:
    draw(WINDOW, grid, rows, WIDTH)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if started:
            continue

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, rows, WIDTH)
            cell = grid[row][col]
            if not start and cell != end:
                start = cell
                start.set_start()
            
            elif not end and cell != start:
                end = cell
                end.set_end()

            elif cell != start and cell != end:
                cell.set_barrier()

        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, rows, WIDTH)
            cell = grid[row][col]
            cell.clear()
            if cell == start:
                start = None
            elif cell == end:
                end = None

