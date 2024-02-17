import pygame
from pieces import Piece, Queen, Arrow
from board import Board
from constants import BOARD_SIZE, SCALE, SHOOT_COLOR
import numpy as np
import pickle

piece_bit = -1
blocker_bit = -1
num_straight_moves = 0
num_diagonal_moves = 0
# moves = np.zeros((BOARD_SIZE * BOARD_SIZE))
straight_masks = [-1] * (BOARD_SIZE * BOARD_SIZE)
diagonal_masks = [-1] * (BOARD_SIZE * BOARD_SIZE)
straight_moves = [{}] * (BOARD_SIZE * BOARD_SIZE)
diagonal_moves = [{}] * (BOARD_SIZE * BOARD_SIZE)


def initialize_board(board):
    board.bitboard = 0
    board.grid = [[Piece(SCALE) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]


def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the display
    screen = pygame.display.set_mode((BOARD_SIZE * SCALE, BOARD_SIZE * SCALE))
    pygame.display.set_caption("Generator")

    initial_board = Board()
    initialize_board(initial_board)

    generate_tables(screen, clock, initial_board)
    # test_tables(screen, clock, initial_board)

    # Quit Pygame
    pygame.quit()


def can_reach(piece_bit, pos, straight):
    x1 = piece_bit % BOARD_SIZE
    y1 = piece_bit // BOARD_SIZE
    x2 = pos % BOARD_SIZE
    y2 = pos // BOARD_SIZE
    if straight and (x1 == x2 or y1 == y2):
        return piece_bit != pos
    if not straight and abs(x1 - x2) == abs(y1 - y2):
        return piece_bit != pos
    return False


def get_moves(piece_bit, straight):
    move_bits = 0
    num_moves = 0
    for i in range(BOARD_SIZE * BOARD_SIZE):
        if can_reach(piece_bit, i, straight):
            move_bits |= 1 << i
            num_moves += 1
    return move_bits, num_moves


def next_root_pos(board):
    global piece_bit, straight_masks, diagonal_masks, blocker_bit, num_straight_moves, num_diagonal_moves
    piece_bit += 1
    if piece_bit >= BOARD_SIZE * BOARD_SIZE:
        piece_bit = 0
        return False
    num_straight_moves, num_diagonal_moves = 0, 0
    if straight_masks[piece_bit] == -1:
        straight_masks[piece_bit], num_straight_moves = get_moves(piece_bit, straight=True)
        diagonal_masks[piece_bit], num_diagonal_moves = get_moves(piece_bit, straight=False)
    return True


def next_blocker(board, straight):
    global piece_bit, blocker_bit, straight_masks, diagonal_masks
    global straight_moves, diagonal_moves, num_straight_moves, num_diagonal_moves
    blocker_bit += 1
    if (straight and blocker_bit >= 2 ** num_straight_moves) or (not straight and blocker_bit >= 2 ** num_diagonal_moves):
        blocker_bit = -1
        return False
    masks = straight_masks if straight else diagonal_masks
    full = convert_to_full(masks[piece_bit], blocker_bit)
    if piece_bit == 2 and full == 4096:
        print("full:", full, "straight:", straight)
    if straight:
        straight_moves[piece_bit][full] = get_valid_moves(full, straight, board)
    else:
        diagonal_moves[piece_bit][full] = get_valid_moves(full, straight, board)
    return True


def get_valid_moves(full, straight, board=None):
    global piece_bit, blocker_bit, straight_masks, diagonal_masks
    if straight:
        queen_directions = [(0, 1), (-1, 0), (1, 0), (0, -1)]
    else:
        queen_directions = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

    start_x, start_y = piece_bit % BOARD_SIZE, piece_bit // BOARD_SIZE
    valid = 0
    for direction in queen_directions:
        x, y = start_x + direction[0], start_y + direction[1]
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and not (full & (1 << (x + y * BOARD_SIZE))):
            valid |= 1 << (x + y * BOARD_SIZE)
            if board:
                board.grid[x][y] = Arrow(SCALE)
            x, y = x + direction[0], y + direction[1]
    return valid


def convert_to_full(mask, value):
    hare = 1
    tortoise = 1
    out = 0
    while hare < mask:
        if mask & hare:
            if tortoise & value:
                out |= hare
            tortoise <<= 1
        hare <<= 1
    if tortoise <= value:
        return False
    return out


def convert_to_reduced(mask, value):
    hare = 1
    tortoise = 1
    out = 0
    while hare < mask:
        if mask & hare:
            if hare & value:
                out |= tortoise
            tortoise <<= 1
        hare <<= 1
    return out


def save_moves():
    global straight_moves, diagonal_moves, diagonal_masks, straight_masks
    print("Saving moves")
    with open("../straight_masks.pkl", "wb") as f:
        print(straight_masks[2])
        pickle.dump(straight_masks, f)
    with open("../diagonal_masks.pkl", "wb") as f:
        print(diagonal_masks[2])
        pickle.dump(diagonal_masks, f)
    with open("../straight_moves.pkl", "wb") as f:
        print(straight_moves[2][4104])
        pickle.dump(straight_moves, f)
    with open("../diagonal_moves.pkl", "wb") as f:
        print(diagonal_moves[2][0])
        pickle.dump(diagonal_moves, f)

def generate_tables(screen, clock, board):
    global piece_bit, blocker_bit, straight_masks, diagonal_masks, straight_moves, diagonal_moves
    running = True
    next_root_pos(board)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        while True:
            if not next_blocker(board, True):
                break
        while True:
            if not next_blocker(board, False):
                break
        draw_from_bits(board, straight_masks, diagonal_masks, straight_moves, diagonal_moves, piece_bit, 4104)
        if piece_bit == 2:
            print(bin(piece_bit), bin(straight_masks[piece_bit]), bin(straight_moves[piece_bit][4104]))
        board.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        if not next_root_pos(board) or piece_bit == 4:
            save_moves()
            return


def draw_from_bits(board, straight_bits, diagonal_bits, straight_moves, diagonal_moves, queen_bit, blockers):
    straight_bits = straight_bits[queen_bit]
    diagonal_bits = diagonal_bits[queen_bit]
    straight_masked = straight_bits & blockers
    diagonal_masked = diagonal_bits & blockers
    straight_moves = straight_moves[queen_bit][straight_masked]
    diagonal_moves = diagonal_moves[queen_bit][diagonal_masked]
    initialize_board(board)
    x, y = queen_bit % BOARD_SIZE, queen_bit // BOARD_SIZE
    board.grid[x][y] = Queen(SCALE, "white")
    for i in range(BOARD_SIZE * BOARD_SIZE):
        if straight_moves & (1 << i) or diagonal_moves & (1 << i):
            x, y = i % BOARD_SIZE, i // BOARD_SIZE
            board.grid[x][y] = Piece(SCALE, SHOOT_COLOR)
        if blockers & (1 << i):
            x, y = i % BOARD_SIZE, i // BOARD_SIZE
            board.grid[x][y] = Arrow(SCALE)


def test_tables(screen, clock, board):
    print("loading")
    with open("../straight_moves.pkl", "rb") as f:
        straight_moves = pickle.load(f)
    with open("../diagonal_moves.pkl", "rb") as f:
        diagonal_moves = pickle.load(f)
    with open("../straight_masks.pkl", "rb") as f:
        straight_masks = pickle.load(f)
    with open("../diagonal_masks.pkl", "rb") as f:
        diagonal_masks = pickle.load(f)
    print("loaded")

    print(straight_moves[2][4104])
    print(straight_masks[2])
    print(diagonal_moves[2][4104])
    print(diagonal_masks[2])
    source_bit = 2
    blockers = 4104
    running = True
    print(bin(piece_bit), bin(straight_masks[piece_bit]), bin(straight_moves[piece_bit][blockers]))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        draw_from_bits(board, straight_masks, diagonal_masks, straight_moves, diagonal_moves, source_bit, blockers)
        board.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
