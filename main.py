import sys

import pygame

from constants import *

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Minesweeper pygame")

fps = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        surface.fill(COLOR_BLACK)

        for y in range(int(SCREEN_HEIGHT / LINE_SIZE)):
            for x in range(int(SCREEN_WIDTH / LINE_SIZE)):
                pygame.draw.rect(surface, COLOR_LINE, (x * LINE_SIZE, y * LINE_SIZE, LINE_SIZE, LINE_SIZE), 1)

        pygame.display.flip()

        fps.tick(FPS)


def quit():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
