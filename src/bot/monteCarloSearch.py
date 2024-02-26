import random
from math import sqrt, log
from time import perf_counter
from copy import deepcopy as copy
import numpy as np

# time_dict = {"appending": 0, "expand": 0, "evaluate": 0, "ucb": 0, "get_highest": 0,
#              "back_propagate": 0}
max_depth = 0


class MonteCarloNode:
    def __init__(self, prior, previous_move=None):
        self.prior = prior  # prior is the probability of choosing this node

        self.children = []  # legal next moves
        self.visit_count = 0  # number of times this node has been visited
        self.value_sum = 0  # sum of the values of all the visits
        self.previous_move = previous_move  # the move that led to this node
        if previous_move is None:
            self.visit_count = 1  # if it's the root node, we want to give it a visit count of 1

    def value(self):
        return self.value_sum / self.visit_count

    def expand(self, board):
        moves = board.get_move_list()
        for move in moves:
            self.children.append(MonteCarloNode(1 / len(moves), previous_move=move))

    def ucb_score(self, parent_visit_count, changed_turn, c):
        if self.visit_count == 0:
            return float("inf")
        prior_score = c * (1 + parent_visit_count) / (1 + self.visit_count)
        # prior_score = c * sqrt((parent_visit_count + 1) / (self.visit_count + 1))
        # prior_score = self.prior * sqrt(parent_visit_count) / (1 + self.visit_count)
        value_score = self.value_sum if changed_turn else -self.value_sum
        return prior_score + value_score

    def get_highest_ucb_child(self, board, c):
        best = None, float("-inf")
        for child_node in self.children:
            score = child_node.ucb_score(self.visit_count, changed_turn=board.currently_aiming is None, c=c)
            # score = child_node.ucb_score(self.visit_count, changed_turn=board.empty_turn, c=c)
            # score = child_node.ucb_score(self.visit_count, changed_turn=False, c=c)
            if score > best[1]:
                best = child_node, score
        return best[0]

    def u(self):
        return 2.0 * log(1.0 + self.N) * sqrt(max(1, self.N - 1)) * self.child_prior / (1 + self.child_N)


def run_monte_carlo_tree_search(board, heuristic_function, time_limit, c=10, iterations=1000):
    global max_depth
    max_depth = 0
    root = MonteCarloNode(1)
    root.expand(board)

    # for _ in range(iterations):
    while perf_counter() < time_limit:
        node = root
        search_path = [node]
        while node.children:
            node = node.get_highest_ucb_child(board, c)
            board.submit_move(node.previous_move)
            search_path.append(node)
        value, ended = evaluate_position(heuristic_function, board)
        if not ended:
            node.expand(board)

        back_propagate(value, search_path, board)

    # print(sorted([(child.visit_count, round(child.value(), 2),) for child in root.children], reverse=True))
    print(sorted([child.visit_count for child in root.children], reverse=True))
    print("max depth:", max_depth)
    best_child = np.argmax([child.value() for child in root.children])
    best_child = root.children[best_child]
    if best_child is None:
        return None, root.visit_count
    return best_child.previous_move, root.visit_count


def evaluate_position(heuristic_function, board):
    h = heuristic_function(board)
    if h == -1 or h == 1:
        return h, True
    # if board.is_game_over():
    #     return h, True
    return h, False


def back_propagate(value, search_path, board):
    global max_depth
    max_depth = max(max_depth, len(search_path) - 1)
    for i, node in enumerate(reversed(search_path)):
        node.visit_count += 1
        if board.currently_aiming is None:
            value *= -1
        # if board.empty_turn:
        #     value *= -1
        # value *= -1
        node.value_sum += value
        if i != len(search_path) - 1:
            board.undo_move()
