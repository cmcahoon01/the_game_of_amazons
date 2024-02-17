import copy
from math import log2
from random import choice
from time import perf_counter
from constants import BOARD_SIZE
from copy import deepcopy as copy


class Bot:
    class BotBoard:

        def __init__(self, board):
            self.bit_board = board.bitboard
            self.queens = [copy(board.white_queens),
                           copy(board.black_queens)]  # in this order so that we can use the black_turn bool to index
            self.history = []

            self.black_turn = board.black_turn
            self.ready_to_shoot = board.shooting is not None

            self.directions = [(-1, -1), (0, -1), (1, -1),
                               (-1, 0), (1, 0),
                               (-1, 1), (0, 1), (1, 1)]

            self.masks = [[[0] * 8] * BOARD_SIZE] * BOARD_SIZE  # assume we loaded this in this shape
            self.possible_moves = [[[{}] * 8] * BOARD_SIZE] * BOARD_SIZE  # assume we loaded this in this shape

        def submit_move(self, new_bitboard, translated=None):
            self.history.append((self.bit_board, copy(self.queens)))
            if not self.ready_to_shoot:  # if we just moved a queen, update the queen list
                old_x, old_y, new_x, new_y = translated if translated else self.translate_move(new_bitboard)
                self.queens[self.black_turn].remove((old_x, old_y))
                self.queens[self.black_turn].append((new_x, new_y))
            self.bit_board = new_bitboard
            if self.ready_to_shoot:  # if we just shot an arrow
                self.black_turn = not self.black_turn  # switch turns
            self.ready_to_shoot = not self.ready_to_shoot

        def undo_move(self):
            previous = self.history.pop()
            self.bit_board = previous[0]
            self.queens = previous[1]
            if not self.ready_to_shoot:
                self.black_turn = not self.black_turn
            self.ready_to_shoot = not self.ready_to_shoot

        def get_move_list(self, queen=None):
            moves = []
            if queen:
                queens_to_check = [queen]
            else:
                queens_to_check = self.queens[self.black_turn]
            for x, y in queens_to_check:
                if self.ready_to_shoot:
                    board_template = self.bit_board
                else:
                    board_template = self.bit_board ^ (1 << (x + y * BOARD_SIZE))
                for direction in self.directions:
                    current_x, current_y = x + direction[0], y + direction[1]
                    while 0 <= current_x < BOARD_SIZE and 0 <= current_y < BOARD_SIZE:
                        pos_bit = 1 << (current_x + current_y * BOARD_SIZE)
                        if board_template & pos_bit:
                            break
                        move = board_template | pos_bit
                        moves.append(move)
                        current_x, current_y = current_x + direction[0], current_y + direction[1]
            return moves

        def lookup_move_list(self):
            moves = []
            for x, y in self.queens[self.black_turn]:
                if self.ready_to_shoot:
                    board_template = self.bit_board
                else:
                    board_template = self.bit_board ^ (2 ** (x + y * BOARD_SIZE))
                for directional_mask in self.masks[x][y]:
                    masked = self.bit_board & directional_mask
                    if masked:
                        move_bits = self.possible_moves[x][y][directional_mask]
                        for bit in move_bits:
                            applied = board_template | bit
                            moves.append(applied)
            return moves

        # compares the current bitboard to the new one and returns old and new position of the queen
        #   or just the new position if the queen shot an arrow
        def translate_move(self, new_bitboard):
            difference = self.bit_board ^ new_bitboard
            old_queen_bit = difference & self.bit_board
            new_piece_bit = difference & new_bitboard
            assert bool(old_queen_bit) != self.ready_to_shoot  # there should be a missing queen if we didn't shoot
            assert new_piece_bit  # there should be a new piece somewhere
            if old_queen_bit:
                old_queen_index = int(log2(old_queen_bit))
                old_x, old_y = old_queen_index % BOARD_SIZE, old_queen_index // BOARD_SIZE
            else:
                old_x, old_y = -1, -1
            new_piece_index = int(log2(new_piece_bit))
            new_x, new_y = new_piece_index % BOARD_SIZE, new_piece_index // BOARD_SIZE
            return old_x, old_y, new_x, new_y

    def __init__(self, board):
        self.true_board = board
        self.bit_board = self.BotBoard(board)

    def make_move(self):
        # assert self.true_board.bitboard == self.bit_board.bit_board
        # assert self.true_board.black_turn == self.bit_board.black_turn
        # assert (self.true_board.shooting is not None) == self.bit_board.ready_to_shoot
        queen = self.move_queen()
        self.shoot_arrow(queen)

    def move_queen(self):
        print("Thinking where to move")
        moves = self.bit_board.get_move_list()
        best = float('-inf'), None
        for move in moves:
            self.bit_board.submit_move(move)
            score = self.heuristic(self.bit_board)
            if score > best[0]:
                best = score, move
            self.bit_board.undo_move()
        translated_move = self.bit_board.translate_move(best[1])
        self.true_board.submit_move(translated_move)
        self.bit_board.submit_move(best[1], translated_move)
        return translated_move[2], translated_move[3]

    def shoot_arrow(self, from_queen):
        print("Thinking where to shoot")
        moves = self.bit_board.get_move_list(from_queen)
        best = float('-inf'), None
        for move in moves:
            self.bit_board.submit_move(move)
            score = -self.heuristic(self.bit_board)
            if score > best[0]:
                best = score, move
            self.bit_board.undo_move()
        translated_move = self.bit_board.translate_move(best[1])
        self.true_board.submit_move(translated_move)
        self.bit_board.submit_move(best[1], translated_move)

    @staticmethod
    def heuristic(board):
        my_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn
        their_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn
        return my_moves - their_moves
