import sys
import random

import pygame

from constants import *

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Minesweeper pygame")

fps = pygame.time.Clock()

number_font = pygame.font.Font(None, 15)


def place_mines(board, width, height, count):
    placed = 0

    while placed < count:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        if board[y][x] != BOARD_MINE:
            board[y][x] = BOARD_MINE
            placed += 1


def is_mine(board, width, height, x, y):
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    return board[y][x] == BOARD_MINE


def get_mine_number_around(board, width, height, x, y):
    if board[y][x] == BOARD_MINE:
        return None

    result = 0
    for y_index in [-1, 0, 1]:
        for x_index in [-1, 0, 1]:
            if is_mine(board, width, height, x + x_index, y + y_index):
                result += 1

    return result


def calculate_numbers(board, width, height):
    for y in range(height):
        for x in range(width):
            number = get_mine_number_around(board, width, height, x, y)
            if number is not None:
                board[y][x] = number


def main():
    width = int(SCREEN_WIDTH / LINE_SIZE)
    height = int(SCREEN_HEIGHT / LINE_SIZE)
    board = [[None for x in range(int(width))] for y in range(int(height))]

    place_mines(board, width, height, count=30)

    calculate_numbers(board, width, height)

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
                item = board[y][x]
                if item == BOARD_MINE:
                    rect = (x * LINE_SIZE + 1, y * LINE_SIZE + 1, LINE_SIZE - 2, LINE_SIZE - 2)
                    pygame.draw.rect(surface, COLOR_MINE, rect, 0)
                else:
                    text = number_font.render(f"{item}", True, (255, 255, 0), (0, 0, 0))
                    text_rect = text.get_rect(center = (x * LINE_SIZE + LINE_SIZE / 2, y * LINE_SIZE + LINE_SIZE / 2))
                    surface.blit(text, text_rect)


        pygame.display.flip()

        fps.tick(FPS)


def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
