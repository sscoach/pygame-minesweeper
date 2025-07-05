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
    board.init(count=MINE_COUNT)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    pos = (event.pos[0] // LINE_SIZE, event.pos[1] // LINE_SIZE)
                    game_over = board.handle_click(event, pos)
                    if board.is_clear():
                        game_over = True
                else:
                    game_over = False
                    board.init(count=MINE_COUNT)

        surface.fill(COLOR_BLACK)

        board.draw(surface, game_over)
        if game_over:
            render_game_over(surface, font, board)

        pygame.display.flip()

        fps.tick(FPS)


def render_game_over(surface, font, board):
    lines = ["You Win" if board.is_clear() else "Game Over", "Click to retry"]

    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2 - 25
    for line in lines:
        text_surface = font.render(line, False, COLOR_GAME_OVER_TEXT,
                                   COLOR_GAME_OVER_BACKGROUND)
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.center = (x, y)
        surface.blit(text_surface, text_surface_rect)
        y += 50


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
