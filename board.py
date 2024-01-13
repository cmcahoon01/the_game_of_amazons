import pygame
from pieces import Piece, Queen, Arrow, Selection
from constants import SCALE, BOARD_SIZE, BORDER_COLOR, TILE_COLOR


class Board:
    def __init__(self):
        self.grid = [[Piece(SCALE) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        white_queens = [(0, 6), (3, 9), (6, 9), (9, 6)]
        black_queens = [(0, 3), (3, 0), (6, 0), (9, 3)]
        for x, y in white_queens:
            self.grid[x][y] = Queen(SCALE, "white")
        for x, y in black_queens:
            self.grid[x][y] = Queen(SCALE, "black")

        self.clicked = None
        self.selections = []
        self.shooting = None

    def draw(self, screen):
        screen.fill(TILE_COLOR)
        for i in range(1, BOARD_SIZE):
            pygame.draw.line(screen, BORDER_COLOR, (0, i * SCALE), (BOARD_SIZE * SCALE, i * SCALE))
            pygame.draw.line(screen, BORDER_COLOR, (i * SCALE, 0), (i * SCALE, BOARD_SIZE * SCALE))
        self.draw_pieces(screen)

    def draw_pieces(self, screen):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].draw(screen, x, y)

    def click(self, x, y):
        if self.grid[x][y].type == "queen":
            self.clear_selections()
            if self.shooting is not None:
                self.return_queen()
            self.clicked = x, y
            self.add_selections()
        elif self.clicked is not None and self.grid[x][y].type != "selection":
            if self.shooting is not None:
                self.return_queen()
            self.clicked = None
            self.clear_selections()
        elif self.clicked is not None and self.grid[x][y].type == "selection":
            self.clear_selections()
            if self.shooting is None:
                self.move_queen(x, y)
            else:
                self.shoot_arrow(x, y)

    def right_click(self):
        if self.shooting is not None:
            self.return_queen()
        self.clicked = None
        self.clear_selections()

    def add_selections(self):
        queen_directions = [(-1, 1), (0, 1), (1, 1),
                            (-1, 0), (0, 0), (1, 0),
                            (-1, -1), (0, -1), (1, -1)]
        for direction in queen_directions:
            x, y = self.clicked[0] + direction[0], self.clicked[1] + direction[1]
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.grid[x][y].type is None:
                self.grid[x][y] = Selection(SCALE, color=self.shooting)
                self.selections.append((x, y))
                x, y = x + direction[0], y + direction[1]

    def clear_selections(self):
        for x, y in self.selections:
            if self.grid[x][y].type == "selection":
                self.grid[x][y] = Piece(SCALE)
        self.selections = []

    def move_queen(self, x, y):
        self.grid[x][y] = self.grid[self.clicked[0]][self.clicked[1]]
        self.shooting = self.clicked
        self.clicked = x, y
        self.grid[self.shooting[0]][self.shooting[1]] = Piece(SCALE)

        self.add_selections()

    def shoot_arrow(self, x, y):
        self.grid[x][y] = Arrow(SCALE)
        self.shooting = None
        self.clicked = None

    def return_queen(self):
        self.grid[self.shooting[0]][self.shooting[1]] = self.grid[self.clicked[0]][self.clicked[1]]
        self.grid[self.clicked[0]][self.clicked[1]] = Piece(SCALE)
        self.shooting = None
        self.clicked = None

    def __getitem__(self, tup):
        return self.grid[tup[0]][tup[1]]

    def __setitem__(self, tup, value):
        self.grid[tup[0]][tup[1]] = value

    def __iter__(self):  # iterate over flattened grid
        for col in self.grid:
            for piece in col:
                yield piece

    def __str__(self):
        return str(self.grid)
