import sys

import pygame

from board import Board
from constants import *

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Minesweeper pygame")

fps = pygame.time.Clock()


def main():
    width = int(SCREEN_WIDTH / LINE_SIZE)
    height = int(SCREEN_HEIGHT / LINE_SIZE)
    board = Board(width, height)
    board.place_mines(count=30)
    board.calculate_numbers()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_game()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"MOUSEBUTTONDOWN: {event.pos} {event.button} {event.touch} {event.window}")
                pos = (event.pos[0] // LINE_SIZE, event.pos[1] // LINE_SIZE)
                game_over = False
                if event.button == pygame.BUTTON_LEFT:
                    game_over = board.open(pos)
                elif event.button == pygame.BUTTON_RIGHT:
                    game_over = board.mark(pos)


        surface.fill(COLOR_BLACK)

        board.draw(surface)

        pygame.display.flip()

        fps.tick(FPS)


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
