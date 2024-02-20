from bot.botBoard import BotBoard
from time import perf_counter
import random

from constants import BOARD_SIZE


class EvilBot:
    move_time_limit = 7
    aim_time_limit = 3

    end_thinking_time = 0

    def __init__(self, board):
        self.true_board = None
        self.bit_board = None
        self.setup_board(board)
        self.evaluated_leafs = 0

    def setup_board(self, board):
        self.true_board = board
        self.bit_board = BotBoard(board)

    def make_move(self, updated_board=None):
        self.evaluated_leafs = 0
        if updated_board:
            self.setup_board(updated_board)
        self.move_queen()
        self.shoot_arrow()
        print("-Evaluated leafs:", self.evaluated_leafs, "\n")

    def move_queen(self):
        print("-Thinking where to move")
        start = perf_counter()
        self.end_thinking_time = start + self.move_time_limit
        self.make_half_move()
        print("moving took:", perf_counter() - start)

    def shoot_arrow(self):
        print("-Thinking where to shoot")
        start = perf_counter()
        self.end_thinking_time = start + self.aim_time_limit
        self.make_half_move()
        print("shooting took:", perf_counter() - start)

    def make_half_move(self):
        best = self.iterative_deepening()
        translated_move = self.bit_board.translate_move(best)
        self.true_board.submit_move(translated_move)
        self.bit_board.submit_move(best, translated_move)

    def iterative_deepening(self):
        depth = 1
        best = float('-inf'), None
        while perf_counter() < self.end_thinking_time:
            searched = self.search_with_pruning(self.bit_board, depth if depth else -1, float('-inf'), float('inf'))
            if searched[0] > best[0]:
                best = searched
            depth += 1
        print("-Depth reached:", depth - 1, "best found:", best[0], end=" ")
        return best[1]

    def search_with_pruning(self, board, depth, alpha, beta):
        if depth == 0 or perf_counter() > self.end_thinking_time:
            self.evaluated_leafs += 1
            return self.heuristic(board), None
        moves = board.get_move_list()
        best = float('-inf'), None
        for move in random.sample(moves, len(moves)):  # randomize move order for better pruning
            swapped_player = board.submit_move(move)
            a, b = (-beta, -alpha) if swapped_player else (alpha, beta)
            score = self.search_with_pruning(board, depth - 1, a, b)[0] * (-1 if swapped_player else 1)
            board.undo_move()
            if score > best[0]:
                best = score, move
            if best[0] > alpha:
                alpha = best[0]
            if alpha >= beta:
                break
        return best

    def heuristic(self, board):
        move_diff = self.get_num_moves(board)
        control_diff = self.get_controlled_squares(board)
        return move_diff + control_diff * 10

    @staticmethod
    def get_controlled_squares(board):  # areas with opposing queens are not controlled
        white_area = 0
        seen_queens = set()
        for i in range(2):
            for queen in board.queens[i]:
                if queen in seen_queens:
                    continue
                seen_queens.add(queen)
                visited = set()
                stack = [queen]
                this_queens_control = 1  # to account for the queen's tile not being counted
                white_queens_in_area = 1 - i
                black_queens_in_area = i
                while stack:
                    x, y = stack.pop()
                    if (x, y) in visited:
                        continue
                    visited.add((x, y))
                    this_queens_control += 1
                    for direction in board.directions:
                        new_x, new_y = x + direction[0], y + direction[1]
                        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                            if (new_x, new_y) in board.queens[0]:
                                if (new_x, new_y) not in seen_queens:
                                    seen_queens.add((new_x, new_y))
                                    white_queens_in_area += 1
                            elif (new_x, new_y) in board.queens[not i]:
                                if (new_x, new_y) not in seen_queens:
                                    seen_queens.add((new_x, new_y))
                                    black_queens_in_area += 1
                            if board.bit_board & (1 << (new_x + new_y * BOARD_SIZE)):
                                continue
                            stack.append((new_x, new_y))
                total_queens_in_area = white_queens_in_area + black_queens_in_area
                white_area += this_queens_control * (white_queens_in_area - black_queens_in_area) / total_queens_in_area
        if board.black_turn:
            return -white_area
        return white_area

    @staticmethod
    def get_num_moves(board):
        temp, board.currently_aiming = board.currently_aiming, None  # temporarily remove aiming queen
        my_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn
        their_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn  # undo the change
        board.currently_aiming = temp
        return (my_moves - their_moves) / (my_moves + their_moves)
