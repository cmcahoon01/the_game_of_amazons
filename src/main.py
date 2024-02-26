import pygame

from bot.bot import Bot
from bot.evilBot import EvilBot
from pieces import Piece, Queen, Arrow
from board import Board
from constants import BOARD_SIZE, SCALE
import pickle


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
    bot1 = Bot(board, c=1)
    bot2 = EvilBot(board)
    bots = [bot1, bot2]
    current_bot = 0
    # board = pickle.load(open("board.p", "rb"))
    # bots = pickle.load(open("bots.p", "rb"))
    # current_bot = pickle.load(open("current_bot.p", "rb"))
    board.draw(screen)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_event(event, board)

        # bots[current_bot].make_move(updated_board=board)
        # current_bot = (current_bot + 1) % 2
        try:
            bots[current_bot].make_move(updated_board=board)
            current_bot = (current_bot + 1) % 2
        except Exception as e:
            print(e)
            pickle.dump(board, open("board.p", "wb"))
            pickle.dump(bots, open("bots.p", "wb"))
            pickle.dump(current_bot, open("current_bot.p", "wb"))
        #     running = False

        board.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def handle_event(event, board):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # left click
            x, y = get_tile(event.pos)
            board.click(x, y)
        elif event.button == 3:  # right click
            board.right_click()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            bot = Bot(board)
            bot.make_move()
            # try:
            #     bot.make_move()
            # except Exception as e:
            #     print(e)


def get_tile(pos):
    x, y = pos
    return x // SCALE, y // SCALE


if __name__ == '__main__':
    main()
