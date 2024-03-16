import random

import numpy as np
import tensorflow as tf
from tensorflow import keras

from board import Board
from evilBot import EvilBot
from test.neutralBot import NeutralBot


def model_board(board):
    board_3d = np.zeros((4, 10, 10))
    # 10 by 10 board
    # one layer for arrows/queens
    # one layer for black queens
    # one layer for white queens
    # one layer for last move

    for i in range(10):
        for j in range(10):
            if board.bit_board & (1 << (i + j * 10)):
                board_3d[0][i][j] = 1
            if (i, j) in board.queens[0]:
                board_3d[1][i][j] = 1
            if (i, j) in board.queens[1]:
                board_3d[2][i][j] = 1
    x, y = board.last_move()
    board_3d[3][x][y] = 1
    return board_3d


def board_model(conv_size, conv_depth):
    model = keras.Input(shape=(4, 10, 10))
    x = model
    for i in range(conv_depth):
        x = keras.layers.Conv2D(conv_size, 3, activation='relu')(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(64, activation='relu')(x)
    x = keras.layers.Dense(1, activation='sigmoid')(x)
    return keras.Model(model, x)


def generate_data(num_games):
    data = []
    for _ in range(num_games):
        board = Board()
        bots = [EvilBot(board), NeutralBot(board)]
        current_bot = random.randint(0, 1)
        turn = 1
        while not board.is_game_over():
            bots[current_bot].make_move(updated_board=board)
            current_bot = (current_bot + 1) % 2
            turn += 1
            data.append((turn, model_board(bots[0].bit_board)))
            print(turn, model_board(bots[0].bit_board))
        print("game over")
    return data


def main():
    data = generate_data(2)
    np_data = np.array(data)
    np.save("data.npy", np_data)


if __name__ == '__main__':
    main()
