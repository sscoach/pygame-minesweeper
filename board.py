import random

from constants import *


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for x in range(width)] for y in range(height)]

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
