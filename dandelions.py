#!/usr/bin/env python3

from enum import Enum
import itertools
import math
import sys

import pygame
import numpy as np

from pygame import gfxdraw

# Constants
BOARD_BORDER = 75
BOARD_HEIGHT = 800
BOARD_WIDTH = 800
BOARD_RIGHT_MARGIN = 375
BOARD_BACKGROUND = (128, 186, 221)
BLACK = (0, 0, 0)

class Turn(Enum):
    DANDELION = 0
    WIND = 1

# Grid manipulation functions are adapted from 
# https://towardsdatascience.com/python-miniproject-making-the-game-of-go-from-scratch-in-pygame-d94f406d4944

def make_grid(size):
    """Return list of (start_point, end_point pairs) defining gridlines
    Args:
        size (int): size of grid
    Returns:
        Tuple[List[Tuple[float, float]]]: start and end points for gridlines
    """
    start_points, end_points = [], []

    # vertical start points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_HEIGHT - BOARD_BORDER, size)
    ys = np.full((size), BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x)
    xs = np.full((size), BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_HEIGHT - BOARD_BORDER, size)
    ys = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x)
    xs = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    end_points += list(zip(xs, ys))

    return (start_points, end_points)

def xy_to_colrow(x, y, size):
    """Convert x,y coordinates to column and row number
    Args:
        x (float): x position
        y (float): y position
        size (int): size of grid
    Returns:
        Tuple[int, int]: column and row numbers of intersection
    """
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x_dist = x - BOARD_BORDER
    y_dist = y - BOARD_BORDER
    col = int(math.floor(x_dist / inc))
    row = int(math.floor(y_dist / inc))
    return col, row

def colrow_to_xy(col, row, size):
    """Convert column and row numbers to x,y coordinates
    Args:
        col (int): column number (horizontal position)
        row (int): row number (vertical position)
        size (int): size of grid
    Returns:
        Tuple[float, float]: x,y coordinates of intersection
    """
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x = int(BOARD_BORDER + col * inc)
    y = int(BOARD_BORDER + row * inc)
    return x, y

class Game:
    def __init__(self, grid_size=6):
        self.board = np.zeros((grid_size, grid_size))
        self.size = grid_size
        self.turn = Turn.DANDELION
        self.start_points, self.end_points = make_grid(self.size)

    def init_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((BOARD_WIDTH + BOARD_RIGHT_MARGIN, BOARD_HEIGHT))
        self.screen = screen

    def clear_screen(self):
        # fill board and add gridlines
        self.screen.fill(BOARD_BACKGROUND)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # Draw the compass rose
        center = ( BOARD_WIDTH + BOARD_BORDER + BOARD_BORDER, 275 )
        segment_len = 43
        pygame.draw.circle(self.screen, (0, 255, 0), center, 150, 0)
        #for i in range(0, 8):
        #    pygame.draw.polygon(self.screen, (255,0,0),
        #        [ center, [ center[0] + ]]
        #                            )

        pygame.display.flip()

    def handle_click(self):
        # get board position
        x, y = pygame.mouse.get_pos()
        
        # Check to see whose turn it is. If it's the Dandelion turn, then we
        # should have a click on the grid. If it's the Wind turn, then we 
        # should have a click on the compass rose
        col, row = xy_to_colrow(x, y, self.size)
        print(col, row)

    def update(self):
        # TODO: undo button
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_click()
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    g = Game()
    g.init_pygame()
    g.clear_screen()
    #g.draw()

    while True:
        g.update()
        pygame.time.wait(100)