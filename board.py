import random

import pygame

from constants import *


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for x in range(width)] for y in range(height)]
        self.number_font = pygame.font.Font(None, 15)

    def is_mine(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.cells[y][x] == BOARD_MINE

    def place_mines(self, count):
        placed = 0

        while placed < count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if not self.is_mine(x, y):
                self.set_cell(x, y, BOARD_MINE)
                placed += 1

    def set_cell(self, x, y, value):
        self.cells[y][x] = value

    def get_cell(self, x, y):
        return self.cells[y][x]

    def get_mine_number_around(self, x, y):
        if self.get_cell(x, y) == BOARD_MINE:
            return None

        result = 0
        for y_index in [-1, 0, 1]:
            for x_index in [-1, 0, 1]:
                if self.is_mine(x + x_index, y + y_index):
                    result += 1

        return result

    def calculate_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                number = self.get_mine_number_around(x, y)
                if number is not None:
                    self.set_cell(x, y, number)

    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                rect = (x * LINE_SIZE, y * LINE_SIZE, LINE_SIZE, LINE_SIZE)
                pygame.draw.rect(surface, COLOR_LINE, rect, 1)
                item = self.get_cell(x, y)
                if item == BOARD_MINE:
                    rect = (x * LINE_SIZE + 1, y * LINE_SIZE + 1, LINE_SIZE - 2, LINE_SIZE - 2)
                    pygame.draw.rect(surface, COLOR_MINE, rect, 0)
                else:
                    text = self.number_font.render(f"{item}", True, (255, 255, 0), (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(x * LINE_SIZE + LINE_SIZE / 2, y * LINE_SIZE + LINE_SIZE / 2))
                    surface.blit(text, text_rect)

    def open(self, pos):
        print(f"open: {pos[0]} {pos[1]}")

    def open_around(self, pos):
        print(f"open_around: {pos[0]} {pos[1]}")
