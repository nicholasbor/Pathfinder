import pygame
from queue import PriorityQueue
import math

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinder")

BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
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
        self.neighbours = []

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
        self.colour = PURPLE

    def clear(self):
        self.colour = WHITE

    def open(self):
        self.colour = GREEN

    def close(self):
        self.colour = RED

    def make_path(self):
        self.colour = YELLOW

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        # Cell below is a neighbour
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): 
            self.neighbours.append(grid[self.row + 1][self.col])

        # Cell to the right is a neighbour
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])

        # Cell above is a neighbour
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])

        # Cell to the left is a neighbour
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])
        

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

def h(x, y):
    x1, y1 = x
    x2, y2 = y
    return abs(x1 - x2) + abs (y1 - y2)

def draw_path(came_from, curr, draw):
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        draw()

def astar(draw, grid, start, end):
    index = 0
    pq = PriorityQueue()
    pq.put((0, index, start))
    last = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    queue_hash = { start }    

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = pq.get()[2]
        queue_hash.remove(curr)

        if curr == end:
            draw_path(last, end, draw)
            end.set_end()
            start.set_start()
            return True

        for neighbour in curr.neighbours:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbour]:
                last[neighbour] = curr
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in queue_hash:
                    index += 1
                    pq.put((f_score[neighbour], index, neighbour))
                    queue_hash.add(neighbour)
                    neighbour.open()
        
        draw()

        if curr != start:
            curr.close()

    return False


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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and start and end:
                for row in grid:
                    for cell in row:
                        cell.update_neighbours(grid)

                # Run algorithm
                astar(lambda: draw(WINDOW, grid, rows, WIDTH), grid, start, end)