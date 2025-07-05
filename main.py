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
    board.place_mines(count=45)
    board.calculate_numbers()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_game()
                return
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = (event.pos[0] // LINE_SIZE, event.pos[1] // LINE_SIZE)
                    if event.button == pygame.BUTTON_LEFT:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_SHIFT:
                            game_over = board.chording(pos)
                        else:
                            game_over = board.open(pos)
                    elif event.button == pygame.BUTTON_RIGHT:
                        game_over = board.mark(pos)
                    else:
                        buttons = pygame.mouse.get_pressed()
                        if buttons[0] and buttons[2]:
                            game_over = board.chording(pos)
            else:
                pass


        surface.fill(COLOR_BLACK)

        board.draw(surface, game_over)

        pygame.display.flip()

        fps.tick(FPS)


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
