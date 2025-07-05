import sys

import pygame

from board import Board
from constants import *


def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Minesweeper pygame")
    fps = pygame.time.Clock()
    width = int(SCREEN_WIDTH / LINE_SIZE)
    height = int(SCREEN_HEIGHT / LINE_SIZE)
    board = Board(width, height)
    board.place_mines(count=45)
    board.calculate_numbers()
    font = pygame.font.Font(None, 40)
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
                    game_over = board.handle_click(event, pos)
            else:
                pass

        surface.fill(COLOR_BLACK)

        board.draw(surface, game_over)
        if game_over:
            render_game_over(surface, font)

        pygame.display.flip()

        fps.tick(FPS)


def render_game_over(surface, font):
    text_surface = font.render(
        "Game Over",
        False,
        COLOR_GAME_OVER_TEXT,
        COLOR_GAME_OVER_BACKGROUND,
    )
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = (
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2,
    )
    surface.blit(text_surface, text_surface_rect)


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
