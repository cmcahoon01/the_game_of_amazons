import random
from math import sqrt
from time import perf_counter
from copy import deepcopy as copy

class MonteCarloNode:
    def __init__(self, prior, board, previous_move=None):
        self.prior = prior  # prior is the probability of choosing this node

        self.children = []  # legal next moves
        self.visit_count = 0  # number of times this node has been visited
        self.value_sum = 0  # sum of the values of all the visits
        self.board = board  # the board state at this node
        self.previous_move = previous_move  # the move that led to this node

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def expand(self):
        moves = self.board.get_move_list()
        for move in moves:
            self.board.submit_move(move)
            self.children.append(MonteCarloNode(1 / len(moves), copy(self.board), move))
            self.board.undo_move()

    def evaluate_position(self, heuristic_function):
        h = heuristic_function(self.board)
        if h == 1 and h == -1:  # if the game is over
            return h, False
        return h, True

    def ucb_score(self, parent_visit_count, parent_turn):
        prior_score = self.prior * sqrt(parent_visit_count) / (1 + self.visit_count)
        if self.visit_count == 0:
            value_score = 0
        else:
            value_score = self.value() if parent_turn == self.board.black_turn else -self.value()
        return prior_score + value_score

    def get_highest_ucb_child(self):
        best = None, float("-inf")
        for child_node in self.children:
            score = child_node.ucb_score(self.visit_count, self.board.black_turn)
            if score > best[1]:
                best = child_node, score
        assert best[0] is not None
        return best[0]


def run_monte_carlo_tree_search(board, heuristic_function, time_limit, iterations=1000):
    root = MonteCarloNode(0, board)
    root.expand()

    while perf_counter() < time_limit:
    # for _ in range(iterations):
        node = root
        search_path = [node]
        while node.children:
            node = node.get_highest_ucb_child()
            search_path.append(node)
        value, ended = node.evaluate_position(heuristic_function)
        if not ended:
            node.expand()

        back_propagate(value, search_path, node.board.black_turn)
    return root.get_highest_ucb_child().previous_move, root.visit_count


def back_propagate(value, search_path, turn):
    for node in reversed(search_path):
        node.visit_count += 1
        node.value_sum += value if node.board.black_turn == turn else -value
