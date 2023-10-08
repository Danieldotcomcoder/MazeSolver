import pygame
import random
from collections import deque
import heapq
import time

# Maze dimensions (number of cells)
width = 30
height = 20
# Dimensions of each cell (pixels)
tile_size = 25

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((width*tile_size + 300, height*tile_size))  # Add 200px for the menu

# Colors
grey = (128,128,128)
white = (255,255,255)
black = (0, 0, 0)
blue = (0,48,143)
green = (132,222,2)
red = (227,38,54)
pink = ( 228, 0, 124 )


# Stack for the recursive backtracker algorithm
stack = []

# Cell class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self):
        x_pos = self.x * tile_size
        y_pos = self.y * tile_size
        wall_thickness = 2

        if self.walls["top"]:
            pygame.draw.rect(window, black, (x_pos, y_pos, tile_size, wall_thickness))
        if self.walls["right"]:
            pygame.draw.rect(window, black, (x_pos + tile_size - wall_thickness, y_pos, wall_thickness, tile_size))
        if self.walls["bottom"]:
            pygame.draw.rect(window, black, (x_pos, y_pos + tile_size - wall_thickness, tile_size, wall_thickness))
        if self.walls["left"]:
            pygame.draw.rect(window, black, (x_pos, y_pos, wall_thickness, tile_size))

    def check_neighbors(self):
        neighbors = []

        if self.x > 0:
            left = grid[self.x - 1][self.y]
            if not left.visited:
                neighbors.append(left)
        if self.x < width - 1:
            right = grid[self.x + 1][self.y]
            if not right.visited:
                neighbors.append(right)
        if self.y > 0:
            top = grid[self.x][self.y - 1]
            if not top.visited:
                neighbors.append(top)
        if self.y < height - 1:
            bottom = grid[self.x][self.y + 1]
            if not bottom.visited:
                neighbors.append(bottom)

        if len(neighbors) > 0:
            return random.choice(neighbors)
        else:
            return None

# Create grid of cells
grid = [[Cell(x,y) for y in range(height)] for x in range(width)]

# Recursive backtracker algorithm
def generate_maze(x,y):
    cell = grid[x][y]
    cell.visited = True

    while len(stack) > 0 or not all(cell.visited for row in grid for cell in row):
        neighbors = cell.check_neighbors()

        if neighbors:
            stack.append(cell)
            next_cell = neighbors

            dx = next_cell.x - cell.x
            dy = next_cell.y - cell.y

            if dx == 1: # right neighbor
                cell.walls["right"] = False
                next_cell.walls["left"] = False
            elif dx == -1: # left neighbor
                cell.walls["left"] = False
                next_cell.walls["right"] = False
            elif dy == 1: # bottom neighbor
                cell.walls["bottom"] = False
                next_cell.walls["top"] = False
            elif dy == -1: # top neighbor
                cell.walls["top"] = False
                next_cell.walls["bottom"] = False

            cell = next_cell
            cell.visited = True

        elif len(stack) > 0:
            cell = stack.pop()

generate_maze(0,0)

def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)
def solve_maze_DFS():
    start_time = time.time()
    start_cell = grid[0][0]
    end_cell = grid[width-1][height-1]

    stack = []
    stack.append(start_cell)

    came_from = {}
    came_from[start_cell] = None

    while len(stack) > 0:
        current_cell = stack.pop()

        if current_cell == end_cell:
            break

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            next_x,next_y=current_cell.x+direction[0],current_cell.y+direction[1]

            if next_x>=0 and next_y>=0 and next_x<width and next_y<height:
                next_cell=grid[next_x][next_y]

                dx=next_x-current_cell.x
                dy=next_y-current_cell.y

                if dx==1 and not current_cell.walls["right"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dx==-1 and not current_cell.walls["left"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==1 and not current_cell.walls["bottom"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==-1 and not current_cell.walls["top"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The DFS Algorithm funtion took {execution_time} seconds to complete.")

    # Draw the solution path
    current_cell = end_cell
    while current_cell != start_cell:
        pygame.draw.rect(window, red, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(50)
        current_cell = came_from[current_cell]


    return True  # Return True when the maze is solved
def solve_maze_DFS_RealTime():

    start_time = time.time()
    start_cell = grid[0][0]
    end_cell = grid[width-1][height-1]

    stack = []
    stack.append(start_cell)

    came_from = {}
    came_from[start_cell] = None

    while len(stack) > 0:
        current_cell = stack.pop()

        # Draw the current cell
        pygame.draw.rect(window, red, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(10)

        if current_cell == end_cell:
            break

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            next_x,next_y=current_cell.x+direction[0],current_cell.y+direction[1]

            if next_x>=0 and next_y>=0 and next_x<width and next_y<height:
                next_cell=grid[next_x][next_y]

                dx=next_x-current_cell.x
                dy=next_y-current_cell.y

                if dx==1 and not current_cell.walls["right"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dx==-1 and not current_cell.walls["left"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==1 and not current_cell.walls["bottom"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==-1 and not current_cell.walls["top"] and next_cell not in came_from:
                    stack.append(next_cell)
                    came_from[next_cell]=current_cell

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The DFS Algorithm function took {execution_time} seconds to complete.")

    # Draw the solution path
    current_cell = end_cell
    while current_cell != start_cell:
        pygame.draw.rect(window, green, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(50)
        current_cell = came_from[current_cell]

    return True  # Return True when the maze is solved
def solve_maze_BFS():
    start_time = time.time()
    start_cell = grid[0][0]
    end_cell = grid[width-1][height-1]

    queue = deque()
    queue.append(start_cell)

    came_from = {}
    came_from[start_cell] = None

    while len(queue) > 0:
        current_cell = queue.popleft()

        if current_cell == end_cell:
            break

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            next_x,next_y=current_cell.x+direction[0],current_cell.y+direction[1]

            if next_x>=0 and next_y>=0 and next_x<width and next_y<height:
                next_cell=grid[next_x][next_y]

                dx=next_x-current_cell.x
                dy=next_y-current_cell.y

                if dx==1 and not current_cell.walls["right"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dx==-1 and not current_cell.walls["left"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==1 and not current_cell.walls["bottom"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==-1 and not current_cell.walls["top"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The BFS Algorithm funtion took {execution_time} seconds to complete.")
    # Draw the solution path
    current_cell = end_cell
    while current_cell != start_cell:
        pygame.draw.rect(window, green, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(50)
        current_cell = came_from[current_cell]


    return True  # Return True when the maze is solved
def solve_maze_BFS_RealTime():
    start_time = time.time()
    start_cell = grid[0][0]
    end_cell = grid[width-1][height-1]

    queue = deque()
    queue.append(start_cell)

    came_from = {}
    came_from[start_cell] = None

    while len(queue) > 0:
        current_cell = queue.popleft()

        # Visualize the current cell
        pygame.draw.rect(window, green, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(10)

        if current_cell == end_cell:
            break

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            next_x,next_y=current_cell.x+direction[0],current_cell.y+direction[1]

            if next_x>=0 and next_y>=0 and next_x<width and next_y<height:
                next_cell=grid[next_x][next_y]

                dx=next_x-current_cell.x
                dy=next_y-current_cell.y

                if dx==1 and not current_cell.walls["right"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dx==-1 and not current_cell.walls["left"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==1 and not current_cell.walls["bottom"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell
                elif dy==-1 and not current_cell.walls["top"] and next_cell not in came_from:
                    queue.append(next_cell)
                    came_from[next_cell]=current_cell

    current_cell = end_cell
    while current_cell != start_cell:
        pygame.draw.rect(window, red,
                         pygame.Rect(current_cell.x * tile_size, current_cell.y * tile_size, tile_size - 0.1,
                                     tile_size - 0.1))
        pygame.display.update()
        pygame.time.delay(50)
        current_cell = came_from[current_cell]

    return True  # Return True when the maze is solved
def solve_maze_AAlgorithm():
    start_time = time.time()
    start_cell = grid[0][0]
    end_cell = grid[width-1][height-1]

    open_set = []
    count = 0
    heapq.heappush(open_set, (0, count, start_cell))

    came_from = {}
    came_from[start_cell] = None

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start_cell] = 0

    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start_cell] = heuristic(start_cell, end_cell)

    open_set_dict = {start_cell}

    while len(open_set) > 0:
        current_cell = heapq.heappop(open_set)[2]
        open_set_dict.remove(current_cell)

        if current_cell == end_cell:
            break

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            next_x,next_y=current_cell.x+direction[0],current_cell.y+direction[1]

            if next_x>=0 and next_y>=0 and next_x<width and next_y<height:
                next_cell=grid[next_x][next_y]

                dx=next_x-current_cell.x
                dy=next_y-current_cell.y

                if dx==1 and not current_cell.walls["right"]:
                    tentative_g_score = g_score[current_cell] + 1
                elif dx==-1 and not current_cell.walls["left"]:
                    tentative_g_score = g_score[current_cell] + 1
                elif dy==1 and not current_cell.walls["bottom"]:
                    tentative_g_score = g_score[current_cell] + 1
                elif dy==-1 and not current_cell.walls["top"]:
                    tentative_g_score = g_score[current_cell] + 1
                else:
                    continue

                if tentative_g_score < g_score[next_cell]:
                    came_from[next_cell] = current_cell
                    g_score[next_cell] = tentative_g_score
                    f_score[next_cell] = tentative_g_score + heuristic(next_cell, end_cell)
                    if next_cell not in open_set_dict:
                        count += 1
                        heapq.heappush(open_set, (f_score[next_cell], count, next_cell))
                        open_set_dict.add(next_cell)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The A Algorithm funtion took {execution_time} seconds to complete.")
    # Draw the solution path
    current_cell = end_cell
    while current_cell != start_cell:
        pygame.draw.rect(window, pink, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(50)
        current_cell = came_from[current_cell]



    return True  # Return True when the maze is solved
def solve_maze_AAlgorithm_RealTime():
    start_time = time.time()
    start_cell = grid[0][0]
    end_cell = grid[width-1][height-1]

    open_set = []
    count = 0
    heapq.heappush(open_set, (0, count, start_cell))

    came_from = {}
    came_from[start_cell] = None

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start_cell] = 0

    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start_cell] = heuristic(start_cell, end_cell)

    open_set_dict = {start_cell}

    while len(open_set) > 0:
        current_cell = heapq.heappop(open_set)[2]
        open_set_dict.remove(current_cell)

        # Visualize the current cell
        pygame.draw.rect(window, pink, pygame.Rect(current_cell.x*tile_size, current_cell.y*tile_size, tile_size-0.1, tile_size-0.1))
        pygame.display.update()
        pygame.time.delay(10)

        if current_cell == end_cell:
            break

        for direction in [(0,-1), (1,0), (0,1), (-1,0)]:
            next_x,next_y=current_cell.x+direction[0],current_cell.y+direction[1]

            if next_x>=0 and next_y>=0 and next_x<width and next_y<height:
                next_cell=grid[next_x][next_y]

                dx=next_x-current_cell.x
                dy=next_y-current_cell.y

                if dx==1 and not current_cell.walls["right"]:
                    tentative_g_score = g_score[current_cell] + 1
                elif dx==-1 and not current_cell.walls["left"]:
                    tentative_g_score = g_score[current_cell] + 1
                elif dy==1 and not current_cell.walls["bottom"]:
                    tentative_g_score = g_score[current_cell] + 1
                elif dy==-1 and not current_cell.walls["top"]:
                    tentative_g_score = g_score[current_cell] + 1
                else:
                    continue

                if tentative_g_score < g_score[next_cell]:
                    came_from[next_cell] = current_cell
                    g_score[next_cell] = tentative_g_score
                    f_score[next_cell] = tentative_g_score + heuristic(next_cell, end_cell)
                    if next_cell not in open_set_dict:
                        count += 1
                        heapq.heappush(open_set, (f_score[next_cell], count, next_cell))
                        open_set_dict.add(next_cell)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The A Algorithm function took {execution_time} seconds to complete.")
    current_cell = end_cell
    while current_cell != start_cell:
        pygame.draw.rect(window, red,
                         pygame.Rect(current_cell.x * tile_size, current_cell.y * tile_size, tile_size - 0.1,
                                     tile_size - 0.1))
        pygame.display.update()
        pygame.time.delay(50)
        current_cell = came_from[current_cell]


    return True  # Return True when the maze is solved

maze_solved = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
            x, y = pygame.mouse.get_pos()
            if width*tile_size < x < width*tile_size + 300:  # Clicked within menu
                if 90 < y < 125:  # Clicked "Restart"

                    generate_maze(0,0)
                    maze_solved = False

                elif 145 < y < 170:  # Clicked "Randomize"
                    grid = [[Cell(x,y) for y in range(height)] for x in range(width)]
                    generate_maze(random.randint(0,width-1),random.randint(0,height-1))
                    maze_solved = False

                elif 190 < y < 215:
                    generate_maze(0, 0)
                    maze_solved = solve_maze_BFS()
                    pygame.event.wait()


                elif 240 < y < 265:
                    generate_maze(0, 0)
                    maze_solved = solve_maze_BFS_RealTime()

                elif 290 < y < 315:
                    generate_maze(0, 0)

                    maze_solved = solve_maze_DFS()

                elif 345 < y < 365:
                    generate_maze(0, 0)

                    maze_solved = solve_maze_DFS_RealTime()

                elif 390 < y < 415:
                    generate_maze(0, 0)

                    maze_solved = solve_maze_AAlgorithm()

                elif 445 < y < 470:
                    generate_maze(0, 0)

                    maze_solved = solve_maze_AAlgorithm_RealTime()
                print(y)

    window.fill(blue)

    for row in grid:
        for cell in row:
            cell.draw()

    # Solve the maze (only once)
    if not maze_solved:
        maze_solved = solve_maze_BFS()

    # Draw menu
    pygame.draw.rect(window, black, pygame.Rect(width*tile_size , 0, 300, height*tile_size))
    font = pygame.font.Font(None, 24)
    text = font.render('Menu', True, grey)
    window.blit(text, (width*tile_size + 50, 50))

    # Draw menu options
    options = ['Restart', 'Randomize', 'Breadth First Search', 'BFS in Real Time', 'Depth First Search', 'DFS in Real Time', 'A Algorithm', 'A Algorithm in Real Time']
    for i, option in enumerate(options):
        text = font.render(option, True, white)
        window.blit(text, (width*tile_size + 50, 100 + i*50))

    # Draw start and end squares
    pygame.draw.rect(window, green, pygame.Rect(0, 0, tile_size, tile_size))
    pygame.draw.rect(window, red, pygame.Rect((width-1)*tile_size, (height-1)*tile_size, tile_size, tile_size))
    pygame.display.update()

pygame.quit()
