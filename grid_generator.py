__author__ = "Tyler McDonnell"

import random
import os
 
EMPTY   = '0'
BLOCKED = '1'
START   = '2'
GOAL    = '3'
PIT     = '4'

def _l(t):
    '''
    Returns the length index of a tuple coordinate.
    '''
    return t[0]

def _w(t):
    '''
    Returns the width index of a tuple coordinate.
    '''
    return t[1]

def _choose(length, width):
    '''
    Generates a random grid space given the dimensions of grid.
    '''
    return (random.randint(0, length-1), random.randint(0,width-1))


def _check(grid, square):
    '''
    Checks a random grid square to ensure that:

    * It is not already a start, goal, blocked, or pit spot.
    
    :param grid:     2D list representing grid.
    :param square:   Tuple (L,W) of the square to be checked.

    :return: True if it passes check; False otherwise.
    '''
    return (grid[_l(square)][_w(square)] == EMPTY)

def _select(grid, l, w):
    '''
    Selects a random square for an obstacle.

    :param grid:     2D list representing grid.
    :param l:        Length of grid.
    :param w:        Width of grid.
    '''
    while True:
        s = _choose(l,w)
        if _check(grid, s):
            return s
    

def grid(f, length, width, start=None, goal=None, blocked=0, pit=0):
    '''
    Generates a grid for the GridWorld domain as defined
    by the RLPY Python package for reinforcement learning.

    The GridWorld consists of a grid where each spot may 
    take on one of the following values:

    * 0: empty
    * 1: blocked
    * 2: start
    * 3: goal
    * 4: pit

    This generator generates random grids of pre-defined
    dimensions with specified numbers of pits and blocked
    spaces. The goal of an agent in the GridWorld domain
    is to move from start to goal.

    Note: This generator does NOT guarantee that there is
    a path from start to goal. The map is randomly generated.
    To ensure that there is a high probability of being such
    a path, the number of pits and blocked blocks should
    be small with respect to the size of the total grid.

    :param f:        Name for output grid world file.
    :param length:   Length of grid world.
    :param width:    Width of grid world.
    :param start:    Tuple (L,W) specifying location of start spot.
    :param goal:     Tuple (L,W) specifying location of goal spot.
    :param blocked:  Number of blocked grid spots.
    :param pit:      Number of pit grid spots.
    '''
    grid = [[EMPTY for i in range(width)] for i in range(length)]

    # Fill in start and goal spots.
    if start == None:
        # Randomly generate start spot.
        start = _select(grid, length, width)
    if goal == None:
        # Randomly generate goal spot.
        goal = _select(grid, length, width)
    grid[_l(start)][_w(start)] = START
    grid[_l(goal)][_w(goal)] = GOAL

    # Generate blocked spots.
    b = None
    for i in range(blocked):
        b = _select(grid, length, width)
        grid[_l(b)][_w(b)] = BLOCKED 

    # Generate pits.
    p = None
    for i in range(pit):
        p = _select(grid, length, width)
        grid[_l(p)][_w(p)] = PIT

    print ("(%d,%d) & (%d,%d) & (%d,%d) & (%d,%d)" %
           (_l(start),
           _w(start),
           _l(goal),
           _w(goal),
           _l(b),
           _w(b),
           _l(p),
           _w(p)))
    print ("\hline")
        
    # Write to file.
    f = open(f, 'wb')
    for y in range(length):
        row = " ".join(grid[y])
        f.write('%s\n' % row)
    f.close()


def generate_many(directory, num, length, width, start=None, goal=None, blocked=0, pit=0):
    '''
    Generates many grid worlds and saves them to a directory.
    
    See grid() function.

    Grids will be named "grid%d" where d is the i-th generated grid.
    
    :param directory:   Directory to save grids too. 
    :param num:         Number of grids to generate.
    '''
    for i in range(num):
        f = os.path.join(directory, 'grid%d.txt' % i)
        grid(f, length, width, start, goal, blocked, pit)
            

if __name__ == '__main__':
    #grid('4x5.txt', 4, 5, (3, 0), (3,2), 1, 4)
    #generate_many('worlds/4x4/', 2, 4, 4, (0,0), (3,3), 1, 2)
    #generate_many('worlds/5x5/', 2, 5, 5, (0,0), (4,4), 1, 3)
    #generate_many('worlds/6x6/', 2, 6, 6, (0,0), (5,5), 2, 4)
    #generate_many('worlds/7x7/', 2, 7, 7, (0,0), (6,6), 3, 6)
    #generate_many('worlds/8x8/', 2, 8, 8, (0,0), (7,7), 4, 8)
    #generate_many('worlds/9x9/', 2, 9, 9, (0,0), (8,8), 5, 10)
    #generate_many('worlds/10x10/', 2, 10, 10, (0,0), (9,9), 6, 12)

    generate_many('worlds/4x4vary/', 50, 4, 4, start=(0,0), goal=(2,2), blocked=1, pit=1)
