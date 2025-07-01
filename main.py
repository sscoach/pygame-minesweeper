import sys

import pygame

from constants import *

pygame.init()

surface = pygame.display.set_mode((320, 240))

pygame.display.set_caption("Minesweeper pygame")

fps = pygame.time.Clock()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        surface.fill(COLOR_BLACK)

        pygame.display.flip()
        
        fps.tick(FPS)


if __name__ == "__main__":
    main()
