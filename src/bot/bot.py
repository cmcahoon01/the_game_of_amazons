from bot.botBoard import BotBoard
from time import perf_counter
import random
from bot.monteCarloSearch import run_monte_carlo_tree_search


class Bot:
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
        print("Evaluated leafs:", self.evaluated_leafs, "\n")

    def move_queen(self):
        print("Thinking where to move")
        start = perf_counter()
        self.end_thinking_time = start + self.move_time_limit
        self.make_half_move()
        print("moving took:", perf_counter() - start)

    def shoot_arrow(self):
        print("Thinking where to shoot")
        start = perf_counter()
        self.end_thinking_time = start + self.aim_time_limit
        self.make_half_move()
        print("shooting took:", perf_counter() - start)

    def make_half_move(self):
        best, leafs = run_monte_carlo_tree_search(self.bit_board, self.heuristic, self.end_thinking_time, 10000)
        self.evaluated_leafs += leafs
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
        print("Depth reached:", depth - 1)
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

    @staticmethod
    def heuristic(board):
        temp, board.currently_aiming = board.currently_aiming, None  # temporarily remove aiming queen
        my_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn
        their_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn  # undo the change
        board.currently_aiming = temp
        if my_moves == 0:
            return float('-inf')
        if their_moves == 0:
            return float('inf')
        return (my_moves - their_moves) / (my_moves + their_moves)
