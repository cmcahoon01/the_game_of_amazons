import pygame
from Pieces import Piece, Queen, Arrow

BOARD_SIZE = 10
SCALE = 100
TILE_COLOR = (161, 176, 194)
BORDER_COLOR = (0, 0, 0)


def initialize_board():
    board = [[Piece(x, y, SCALE) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
    white_queens = [(0, 6), (3, 9), (6, 9), (9, 6)]
    black_queens = [(0, 3), (3, 0), (6, 0), (9, 3)]
    for x, y in white_queens:
        board[x][y] = Queen(x, y, SCALE, "white")
    for x, y in black_queens:
        board[x][y] = Queen(x, y, SCALE, "black")
    return board


def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the display
    screen = pygame.display.set_mode((BOARD_SIZE * SCALE, BOARD_SIZE * SCALE))
    pygame.display.set_caption("The Game of Amazons")

    initial_board = initialize_board()

    main_loop(screen, clock, initial_board)

    # Quit Pygame
    pygame.quit()


def draw_board(screen):
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BORDER_COLOR, (0, i * SCALE), (BOARD_SIZE * SCALE, i * SCALE))
        pygame.draw.line(screen, BORDER_COLOR, (i * SCALE, 0), (i * SCALE, BOARD_SIZE * SCALE))


def main_loop(screen, clock, board):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(TILE_COLOR)

        draw_board(screen)
        for col in board:
            for piece in col:
                piece.draw(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
