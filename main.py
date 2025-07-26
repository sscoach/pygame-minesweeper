import pygame
import sys
from const import *
from board import Board


def main():
    pygame.init()

    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    fps = pygame.time.Clock()

    board = Board(9, 9)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                board.on_click(event.pos, event.button)



        surface.fill(BLACK)

        board.draw(surface)

        pygame.display.flip()

        fps.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
