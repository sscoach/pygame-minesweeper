import sys
import random

import pygame

from board import Board
from constants import *

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Minesweeper pygame")

fps = pygame.time.Clock()

number_font = pygame.font.Font(None, 15)


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

        surface.fill(COLOR_BLACK)

        for y in range(int(height)):
            for x in range(int(width)):
                rect = (x * LINE_SIZE, y * LINE_SIZE, LINE_SIZE, LINE_SIZE)
                pygame.draw.rect(surface, COLOR_LINE, rect, 1)
                item = board.get_cell(x, y)
                if item == BOARD_MINE:
                    rect = (x * LINE_SIZE + 1, y * LINE_SIZE + 1, LINE_SIZE - 2, LINE_SIZE - 2)
                    pygame.draw.rect(surface, COLOR_MINE, rect, 0)
                else:
                    text = number_font.render(f"{item}", True, (255, 255, 0), (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(x * LINE_SIZE + LINE_SIZE / 2, y * LINE_SIZE + LINE_SIZE / 2))
                    surface.blit(text, text_rect)

        pygame.display.flip()

        fps.tick(FPS)


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
