import random
import json
from enum import Enum
grid_height = 4
grid_width = 4
grid_max_count = 2
grid_not_probibility = 0.2
four_probibility = 0.3

class vec2(object):
    def __init__(self, x : int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, mutliplier: int):
        return vec2(self.x * mutliplier, self.y * mutliplier)
    
    def in_grid(self):
        return 0 <= self.x < grid_width and 0 <= self.y < grid_height

class state(Enum):
    playing = 0
    lose = 1
    win = 2


class game_state(object):
    def __init__(self, starting_grid: list, starting_score: int = 0):
        self.grid = starting_grid
        self.state = state.playing
        if (starting_score == None):
            self.score = 0
        else:
            self.score = int(starting_score)

    def __str__(self):
        return (f"score:{self.score}, state:{self.state}, grid:{self.grid}")
    

def create_grid() -> list:
    grid =  []
    #create empty grid
    for x in range(grid_width):
        row = []
        for y in range(grid_height):
            row.append(0)
        grid.append(row)
    temp_state = game_state(grid)
    #fill up grid
    for i in range(grid_max_count):      
        temp_state = add_new(temp_state)
        if random.random() < grid_not_probibility:
            break
    return temp_state.grid

def get_empty(grid: list) -> list[vec2]:
    output = []
    for x in range(grid_width):
        for y in range(grid_height):
            if grid[x][y] == 0:
                output.append(vec2(x, y))
    return output

def add_new(current_state: game_state) -> game_state:
    avalible = get_empty(current_state.grid)
    if len(avalible) == 0:
        return current_state # no space to add 
    selected = random.choice(avalible)
    if random.random() < four_probibility:
        value = 4
    else:
        value = 2
    current_state.grid[selected.x][selected.y] = value
    return current_state

def try_move(pos1: vec2, pos2: vec2, current_state : game_state):
    """trys to move pos1 to pos 2 and murge it and returns true if move to empty"""
    #move it
    empty = False
    if current_state.grid[pos2.x][pos2.y] == 0 :
        current_state.grid[pos2.x][pos2.y] = current_state.grid[pos1.x][pos1.y]
        current_state.grid[pos1.x][pos1.y] = 0
        empty = True
    #combine
    elif current_state.grid[pos1.x][pos1.y] == current_state.grid[pos2.x][pos2.y]:
         new_value = current_state.grid[pos2.x][pos2.y] * 2
         current_state.grid[pos2.x][pos2.y] = new_value
         current_state.grid[pos1.x][pos1.y] = 0
         current_state.score += new_value
    
    return current_state, empty

def move_vector(pos: vec2, vector: vec2, current_state : game_state) -> game_state:
    for i in range(1,grid_width):
        pos1 = pos + vector * (i-1)
        pos2 = pos + vector * i
        if not pos2.in_grid(): #if got to end stop repeating
            break
        current_state, empty = try_move(pos1, pos2, current_state)
        if not empty: #if collision stop repeating
            break
        #else keep on going until something happens

    return current_state


def left(current_state: game_state) -> game_state:
    #move left
    for x in range(1, grid_width):
        for y in range(grid_height):
            current_state = move_vector(vec2(y,x), vec2(0,-1), current_state)

    if check_loss(current_state.grid):
        current_state.state = state.lose
        return current_state
    if check_win(current_state.grid):
        current_state.state = state.win

    current_state = add_new(current_state)
    return current_state

def right(current_state: game_state) -> game_state:
    #move left
    for x in range(grid_width-2,-1,-1):
        for y in range(grid_height):
            current_state = move_vector(vec2(y,x), vec2(0,+1), current_state)

    if check_loss(current_state.grid):
        current_state.state = state.lose
        return current_state
    if check_win(current_state.grid):
        current_state.state = state.win

    current_state = add_new(current_state)
    return current_state

def up(current_state: game_state) -> game_state:
    #move left
    for x in range(grid_width):
        for y in range(1, grid_height):
            current_state = move_vector(vec2(y,x), vec2(-1,0), current_state)

    if check_loss(current_state.grid):
        current_state.state = state.lose
        return current_state
    if check_win(current_state.grid):
        current_state.state = state.win

    current_state = add_new(current_state)
    return current_state

def down(current_state: game_state) -> game_state:
    #move left
    for x in range(grid_width):
        for y in range(grid_height-2,-1,-1):
            current_state = move_vector(vec2(y,x), vec2(1,0), current_state)
    
    if check_loss(current_state.grid):
        current_state.state = state.lose
        return current_state
    if check_win(current_state.grid):
        current_state.state = state.win

    current_state = add_new(current_state)
    return current_state

def check_win(grid: list)-> bool:
    for x in range(grid_width):
        for y in range(grid_height-2,-1,-1):
           if grid[x][y] == 2048:
               return True
    return False

def check_loss(grid: list)-> bool:
    print(f"teststring:{get_empty(grid)}, :{len(get_empty(grid)) == 0}" )
    return len(get_empty(grid)) == 0 


def jsonToGrid(string: str) -> list:
    """
    converts json string to grid
    """
    return json.loads(string)

def gridToJson(grid: list) -> str:
    """
    converts grid tp json string
    """
    return json.dumps(grid)