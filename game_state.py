#!/usr/bin/env python3

"""
The classes in this file control the game state itself, rather than the display.
You can also run this with the included main driver in this file.
"""
import sys
from enum import Enum, StrEnum, auto

class Space(StrEnum):
    EMPTY = " "
    SEED = "."
    FLOWER = "*"

class Turn(StrEnum):
    DANDELION = "Dandelion"
    WIND = "Wind"

class WindDirection(StrEnum):
    SW = "SW"
    S = "S"
    SE = "SE"
    W = "W"
    E = "E"
    NW = "NW"
    N = "N"
    NE = "NE"

class DandelionGame:

    def __init__(self):
        self.grid = []
        for c in range(0, 5):
            row = []
            for r in range(0, 5):
                row.append(Space.EMPTY)
            self.grid.append(row)

        self.valid_wind_dirs = set(WindDirection.__members__)

    def print(self, outf=sys.stdout):
        TOP = "  ╔" + "═" * 39 + "╗"
        BOTTOM = "  ╚" + "═" * 39 + "╝"
        outf.write("  ")
        for i in range(1, 6): 
            outf.write("    {}   ".format(i))
        outf.write("\n")
        outf.write(TOP + "\n")
        for y in range(0, 5):
            outf.write("  " + "║       " * 5 + "║\n")
            outf.write("{} ".format(y+1))
            for x in range(0, 5):
                outf.write("║   {}   ".format(self.grid[x][y]))
            outf.write("║\n  ")
            outf.write("║       " * 5 + "║\n")
            if y < 4:
                outf.write("  ║" + "═" * 39 + "║\n")
        outf.write(BOTTOM + "\n")

    def add_flower(self, row, col):
        '''You can put a flower on any spot that is empty or a seed'''
        if self.grid[col][row] is Space.FLOWER:
            return False
        self.grid[col][row] = Space.FLOWER
        return True

    def propagate(self, row, col, wind_dir):
        row_delta = 0
        col_delta = 0

        match wind_dir:
            case WindDirection.S:
                row_delta = 1
            case WindDirection.N:
                row_delta = -1
            case WindDirection.E:
                col_delta = 1
            case WindDirection.W:
                col_delta = -1
            case WindDirection.NE:
                row_delta = -1
                col_delta = 1
            case WindDirection.SE:
                row_delta = 1
                col_delta = 1
            case WindDirection.NW:
                row_delta = -1
                col_delta = -1
            case WindDirection.SW:
                row_delta = 1
                col_delta = -1
        
        r = row
        c = col
        while r in range(0, 5) and c in range(0, 5):
            if self.grid[c][r] is Space.EMPTY:
                self.grid[c][r] = Space.SEED
            r += row_delta
            c += col_delta

    def blow_wind(self, wind_dir):
        # For each grid space, see if you find a flower, and then propagate
        # the seeds out in the correct direction
        for row in range(0, 5):
            for col in range(0, 5):
                if self.grid[col][row] is Space.FLOWER:
                    self.propagate(row, col, wind_dir)
        self.valid_wind_dirs.remove(wind_dir)

    def check_winner(self):
        for c in range(0, 5):
            for r in range(0, 5):
                if self.grid[c][r] is Space.EMPTY:
                    return Turn.WIND
        return Turn.DANDELION
        
if __name__ == "__main__":
    import sys
    dg = DandelionGame()
    for i in range(1, 8):
        print("   ------------- Turn {} -------------   ".format(i))
        dg.print()
        
        # Dandelion moves first: pick a square in which to place a flower
        print("Dandelion's Turn!")

        valid_spot = False
        while not valid_spot:
            row_s = input("Pick a row (1-5)   : ")
            col_s = input("Pick a column (1-5): ")

            try:
                row = int(row_s) - 1
                col = int(col_s) - 1
            except TypeError as err:
                print("That's not a valid entry.")
                continue
            if not ((row >= 0) and (row < 5)):
                print("That's not a valid row!")
                continue
            if not ((col >= 0) and (col < 5)):
                print("That's not a valid column!")
                continue

            if not dg.add_flower(row, col):
                print("Spot must be empty! Try again.")
            else:
                valid_spot = True

        # Wind moves second: pick a wind direction from the remaining choices
        print("\n\n")
        dg.print()
        valid_wind = False
        direction = None
        while not valid_wind:
            direction = input("\nWind's Turn. Pick a direction from " \
                + ", ".join(sorted(list(dg.valid_wind_dirs))) \
                + ": ").upper()
            if direction in dg.valid_wind_dirs:
                valid_wind = True
        dg.blow_wind(WindDirection(direction))
        print("\n\n")

    # After 7 turns, game is over
    print("   ------------- Final -------------   ")
    dg.print()
    print("The winner was: {}".format(dg.check_winner()))

