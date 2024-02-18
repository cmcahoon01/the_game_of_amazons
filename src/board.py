import pygame
from pieces import Piece, Queen, Arrow, Selection
from constants import SCALE, BOARD_SIZE, BORDER_COLOR, TILE_COLOR


class Board:
    queen_directions = [(-1, 1), (0, 1), (1, 1),
                        (-1, 0), (0, 0), (1, 0),
                        (-1, -1), (0, -1), (1, -1)]

    def __init__(self):
        self.bitboard = 89131683419996112206878998600
        self.grid = [[Piece(SCALE) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.white_queens = [(0, 6), (3, 9), (6, 9), (9, 6)]
        self.black_queens = [(0, 3), (3, 0), (6, 0), (9, 3)]
        for x, y in self.white_queens:
            self.grid[x][y] = Queen(SCALE, "white")
        for x, y in self.black_queens:
            self.grid[x][y] = Queen(SCALE, "black")

        self.clicked_queen = None
        self.selections = []
        self.aiming_queen = None
        self.black_turn = True

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
        if self.grid[x][y].type == "queen" and self.black_turn == (self.grid[x][y].color == "black"):
            self.clear_selections()
            if self.aiming_queen is not None:
                self.return_queen()
            self.clicked_queen = x, y
            self.add_selections()
        elif self.clicked_queen is not None and self.grid[x][y].type != "selection":
            if self.aiming_queen is not None:
                self.return_queen()
            self.clicked_queen = None
            self.clear_selections()
        elif self.clicked_queen is not None and self.grid[x][y].type == "selection":
            self.clear_selections()
            if self.aiming_queen is None:
                self.move_queen(x, y)
            else:
                self.shoot_arrow(x, y)

    def right_click(self):
        if self.aiming_queen is not None:
            self.return_queen()
        self.clicked_queen = None
        self.clear_selections()

    def add_selections(self):
        for direction in self.queen_directions:
            x, y = self.clicked_queen[0] + direction[0], self.clicked_queen[1] + direction[1]
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.grid[x][y].type is None:
                self.grid[x][y] = Selection(SCALE, color=self.aiming_queen)
                self.selections.append((x, y))
                x, y = x + direction[0], y + direction[1]

    def clear_selections(self):
        for x, y in self.selections:
            if self.grid[x][y].type == "selection":
                self.grid[x][y] = Piece(SCALE)
        self.selections = []

    def move_queen(self, x, y):
        self.grid[x][y] = self.grid[self.clicked_queen[0]][self.clicked_queen[1]]
        self.aiming_queen = self.clicked_queen
        self.clicked_queen = x, y
        self.grid[self.aiming_queen[0]][self.aiming_queen[1]] = Piece(SCALE)

        self.add_selections()

    def shoot_arrow(self, x, y):
        self.grid[x][y] = Arrow(SCALE)

        # remove queen from old position, add queen to new position and add arrow
        self.bitboard ^= 2 ** (self.aiming_queen[0] + self.aiming_queen[1] * 10)
        self.bitboard ^= 2 ** (self.clicked_queen[0] + self.clicked_queen[1] * 10)
        self.bitboard ^= 2 ** (x + y * 10)

        queens = self.black_queens if self.black_turn else self.white_queens
        queens.remove(self.aiming_queen)
        queens.append(self.clicked_queen)

        self.aiming_queen = None
        self.clicked_queen = None
        self.black_turn = not self.black_turn

    def return_queen(self):
        self.grid[self.aiming_queen[0]][self.aiming_queen[1]] = self.grid[self.clicked_queen[0]][self.clicked_queen[1]]
        self.grid[self.clicked_queen[0]][self.clicked_queen[1]] = Piece(SCALE)
        self.aiming_queen = None
        self.clicked_queen = None

    def get_move_list(self):
        move_list = []
        if self.aiming_queen is None:
            queens = self.black_queens if self.black_turn else self.white_queens
        else:
            queens = [self.clicked_queen]
        for queen in queens:
            for direction in self.queen_directions:
                x, y = queen[0] + direction[0], queen[1] + direction[1]
                while (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and
                       (self.grid[x][y].type is None or self.grid[x][y].type == "selection")):
                    move_list.append((queen[0], queen[1], x, y))
                    x, y = x + direction[0], y + direction[1]
        return move_list

    def submit_move(self, move):
        if self.aiming_queen is None:
            self.clicked_queen = move[0], move[1]
            self.move_queen(move[2], move[3])
        else:
            self.clear_selections()
            self.shoot_arrow(move[2], move[3])

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
