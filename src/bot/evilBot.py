from bot.botBoard import BotBoard
from time import perf_counter


class EvilBot:
    time_limit = 1

    end_thinking_time = 0

    def __init__(self, board):
        self.true_board = board
        self.bit_board = BotBoard(board)
        self.setup_board(board)

    def setup_board(self, board):
        self.true_board = board
        self.bit_board = BotBoard(board)

    def make_move(self, updated_board=None):
        if updated_board:
            self.setup_board(updated_board)
        print("Thinking what to do")
        start = perf_counter()
        self.end_thinking_time = start + self.time_limit
        self.make_full_move()
        print("turn took:", perf_counter() - start, "\n")

    def make_full_move(self):
        best = self.iterative_deepening()
        # assert None not in best
        if None in best:
            raise Exception("None in best")
        for move in best:
            translated_move = self.bit_board.translate_move(move)
            self.true_board.submit_move(translated_move)
            self.bit_board.submit_move(move, translated_move)

    def iterative_deepening(self):
        depth = 2
        best = float('-inf'), None, None
        while perf_counter() < self.end_thinking_time:
        # while depth < 3:
            searched = self.tree_search(self.bit_board, depth)
            if searched[0] > best[0] and None not in searched:
                best = searched
            depth += 1
        print("Depth reached:", depth - 1, end=" ")
        return best[1], best[2]

    def tree_search(self, board, depth):
        if depth == 0 or perf_counter() > self.end_thinking_time:
        # if depth == 0:
            return self.heuristic(board), None, None
        moves = board.get_move_list()
        best = float('-inf'), None, None
        for move in moves:
            swapped_player = board.submit_move(move)
            score, next_move, next_next_move = self.tree_search(board, depth - 1)
            score *= -1 if swapped_player else 1
            if score > best[0]:
                best = score, move, next_move
            board.undo_move()
        return best

    @staticmethod
    def heuristic(board):
        temp, board.currently_aiming = board.currently_aiming, None  # temporarily remove aiming queen
        my_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn
        their_moves = len(board.get_move_list())
        board.black_turn = not board.black_turn  # undo the change
        board.currently_aiming = temp
        return my_moves - their_moves
