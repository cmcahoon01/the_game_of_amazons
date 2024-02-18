from bot.botBoard import BotBoard
from time import perf_counter


class Bot:
    move_time_limit = 0.5
    aim_time_limit = 0.5

    end_thinking_time = 0

    def __init__(self, board):
        self.true_board = None
        self.bit_board = None
        self.setup_board(board)

    def setup_board(self, board):
        self.true_board = board
        self.bit_board = BotBoard(board)

    def make_move(self, updated_board=None):
        if updated_board:
            self.setup_board(updated_board)
        self.move_queen()
        self.shoot_arrow()

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
        print("shooting took:", perf_counter() - start, "\n")

    def make_half_move(self):
        best = self.iterative_deepening()
        translated_move = self.bit_board.translate_move(best)
        self.true_board.submit_move(translated_move)
        self.bit_board.submit_move(best, translated_move)

    def iterative_deepening(self):
        depth = 1
        best = float('-inf'), None
        while perf_counter() < self.end_thinking_time:
            searched = self.tree_search(self.bit_board, depth if depth else -1)
            if searched[0] > best[0]:
                best = searched
            depth += 1
        print("Depth reached:", depth - 1, end=" ")
        return best[1]

    def tree_search(self, board, depth):
        if depth == 0 or perf_counter() > self.end_thinking_time:  # negative depth means limit is time
            return self.heuristic(board), None
        moves = board.get_move_list()
        best = float('-inf'), None
        for move in moves:
            swapped_player = board.submit_move(move)
            score = self.tree_search(board, depth - 1)[0] * (-1 if swapped_player else 1)
            if score > best[0]:
                best = score, move
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
