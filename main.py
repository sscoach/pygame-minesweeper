import sys
import random

import pygame

from constants import *

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Minesweeper pygame")

fps = pygame.time.Clock()


def place_mines(cells, width, height, count):
    placed = 0

    while placed < count:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        if cells[y][x] == 0:
            cells[y][x] = 1
            placed += 1


def main():
    width = int(SCREEN_WIDTH / LINE_SIZE)
    height = int(SCREEN_HEIGHT / LINE_SIZE)
    cells = [[0 for x in range(int(width))] for y in range(int(height))]
    place_mines(cells, width, height, count=30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        surface.fill(COLOR_BLACK)

        for y in range(int(height)):
            for x in range(int(width)):
                rect = (x * LINE_SIZE, y * LINE_SIZE, LINE_SIZE, LINE_SIZE)
                pygame.draw.rect(surface, COLOR_LINE, rect, 1)
                if cells[y][x] == 1:
                    rect = (x * LINE_SIZE + 1, y * LINE_SIZE + 1, LINE_SIZE - 2, LINE_SIZE - 2)
                    pygame.draw.rect(surface, COLOR_MINE, rect, 0)

        pygame.display.flip()

        fps.tick(FPS)


def quit():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
