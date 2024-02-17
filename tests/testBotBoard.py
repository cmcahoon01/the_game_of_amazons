import pygame
from src.pieces import Piece, Queen, Arrow
from src.board import Board
from src.constants import BOARD_SIZE, SCALE
from src.bot import Bot


def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the display
    screen = pygame.display.set_mode((BOARD_SIZE * SCALE, BOARD_SIZE * SCALE))
    pygame.display.set_caption("The Game of Amazons")

    initial_board = Board()
    wipe_board(initial_board)
    bot = Bot(initial_board)

    main_loop(screen, clock, initial_board, bot.bit_board)

    # Quit Pygame
    pygame.quit()


def main_loop(screen, clock, board, bot_board):
    running = True
    moves = bot_board.get_move_list()
    i = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_event(event, board)
        bot_board.submit_move(moves[i])
        draw_bitboard(board, bot_board)
        board.draw(screen)
        bot_board.undo_move()
        i = (i + 1) % len(moves)

        pygame.display.flip()
        clock.tick(2)


def draw_bitboard(board, bot_board):
    wipe_board(board)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            bit = x + y * BOARD_SIZE
            if bot_board.bit_board & (1 << bit):
                if (x, y) in bot_board.queens[0]:
                    board.grid[x][y] = Queen(SCALE, "white")
                elif (x, y) in bot_board.queens[1]:
                    board.grid[x][y] = Queen(SCALE, "black")
                else:
                    board.grid[x][y] = Arrow(SCALE)


def wipe_board(board):
    board.bitboard = 2
    board.grid = [[Piece(SCALE) for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
    board.grid[1][0] = Queen(SCALE, "white")
    board.black_queens = [(1, 0)]
    board.white_queens = []
    board.black_turn = True


def handle_event(event, board):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # left click
            x, y = get_tile(event.pos)
            board.click(x, y)
        elif event.button == 3:  # right click
            board.right_click()


def get_tile(pos):
    x, y = pos
    return x // SCALE, y // SCALE


if __name__ == '__main__':
    main()
