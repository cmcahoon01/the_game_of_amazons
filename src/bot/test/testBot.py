from connect_2_board import Connect2Board
import random
from bot.monteCarloSearch import run_monte_carlo_tree_search


class Bot:
    def __init__(self, c=10):
        self.board = Connect2Board()
        self.evaluated_leafs = 0
        self.c = c

    def make_move(self):
        self.evaluated_leafs = 0
        best, leafs = run_monte_carlo_tree_search(self.board, self.heuristic, 0, c=self.c)
        self.evaluated_leafs += leafs
        self.board.submit_move(best)
        print("Evaluated leafs:", self.evaluated_leafs, "\n")

    @staticmethod
    def heuristic(board):
        if board.is_game_over():
            return board.get_winner()
        return 0


if __name__ == '__main__':
    bot = Bot()
    while not bot.board.is_game_over():
        bot.make_move()
        print(bot.board)
    print(bot.board.get_winner())
