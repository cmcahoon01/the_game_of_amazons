import pygame
from pieces import Piece, Queen, Arrow
from board import Board
from constants import BOARD_SIZE, SCALE
from bot import Bot


def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the display
    screen = pygame.display.set_mode((BOARD_SIZE * SCALE, BOARD_SIZE * SCALE))
    pygame.display.set_caption("The Game of Amazons")

    initial_board = Board()

    main_loop(screen, clock, initial_board)

    # Quit Pygame
    pygame.quit()


def main_loop(screen, clock, board):
    running = True
    bot = Bot(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_event(event, board, bot)

        # bot.make_move()
        board.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def handle_event(event, board, bot):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # left click
            x, y = get_tile(event.pos)
            board.click(x, y)
        elif event.button == 3:  # right click
            board.right_click()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            bot = Bot(board)
            try:
                bot.make_move()
            except Exception as e:
                print(e)


def get_tile(pos):
    x, y = pos
    return x // SCALE, y // SCALE


if __name__ == '__main__':
    main()
