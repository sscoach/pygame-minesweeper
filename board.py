import random
import pygame

from constants import *

# 💣💥☀✴🧨☠︎︎👊🎯👾🚀🎮👽💯🛢
# https://emojidb.org/
BOARD_MINE = "💣"
MINE_EXPLOSION = "💥"

STATE_NONE = None
STATE_MARK = "X"
STATE_UNKNOWN = "?"
STATE_OPEN = "O"


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None for x in range(width)] for y in range(height)]
        self.state = [[STATE_NONE for x in range(width)] for y in range(height)]
        self.number_font = pygame.font.Font(None, 17)
        self.emoji_font = pygame.font.Font("assets/fonts/NotoEmoji-VariableFont_wght.ttf", 10)
        # https://fonts.google.com/

    def is_mine(self, pos):
        (x, y) = pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.cells[y][x] == BOARD_MINE

    def place_mines(self, count):
        placed = 0

        while placed < count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if not self.is_mine((x, y)):
                self.set_cell((x, y), BOARD_MINE)
                placed += 1

    def set_state(self, pos, value):
        (x, y) = pos
        print(f"set_state {pos} {self.get_state(pos)} -> {value}")
        self.state[y][x] = value

    def get_state(self, pos):
        return self.state[pos[1]][pos[0]]

    def set_cell(self, pos, value):
        (x, y) = pos
        self.cells[y][x] = value

    def get_cell(self, pos):
        (x, y) = pos
        return self.cells[y][x]

    def get_mine_number_around(self, pos):
        (x, y) = pos
        if self.get_cell(pos) == BOARD_MINE:
            return None

        result = 0
        for y_index in [-1, 0, 1]:
            for x_index in [-1, 0, 1]:
                if self.is_mine((x + x_index, y + y_index)):
                    result += 1

        return result

    def calculate_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                number = self.get_mine_number_around((x, y))
                if number is not None:
                    self.set_cell((x, y), number)

    def draw(self, surface, game_over):
        for y in range(self.height):
            for x in range(self.width):
                self.draw_cell(surface, (x, y), game_over)

    def draw_cell(self, surface, pos, game_over):
        (x, y) = pos
        rect = (x * LINE_SIZE, y * LINE_SIZE, LINE_SIZE, LINE_SIZE)
        inner_rect = (x * LINE_SIZE + 1, y * LINE_SIZE + 1, LINE_SIZE - 2, LINE_SIZE - 2)

        pygame.draw.rect(surface, COLOR_LINE, rect, 0)
        number = self.get_cell((x, y))
        state = self.get_state((x, y))

        pygame.draw.rect(surface, COLOR_INITIAL, inner_rect, 0)

        if state == STATE_OPEN:
            pygame.draw.rect(surface, COLOR_OPEN, inner_rect, 0)
            if number == BOARD_MINE:
                self.draw_emoji(surface, (x, y), MINE_EXPLOSION, COLOR_MINE, None)
            else:
                self.draw_text(surface, (x, y), number, COLOR_TEXT, None)

        elif state == STATE_MARK:
            self.draw_text(surface, (x, y), state, COLOR_MARK, COLOR_INITIAL)
        elif state == STATE_UNKNOWN:
            self.draw_text(surface, (x, y), state, COLOR_MARK, COLOR_INITIAL)

        if game_over:
            if state == STATE_NONE and number == BOARD_MINE:
                self.draw_emoji(surface, (x, y), number, COLOR_TEXT, None)

        # if item != BOARD_MINE:
        #     self.draw_item_text(surface, (x, y), item, COLOR_DEBUG_TEXT)

    def draw_text(self, surface, pos, text, color, background):
        (x, y) = pos
        text = self.number_font.render(f"{text}", True, color, background)
        text_rect = text.get_rect(
            center=(x * LINE_SIZE + LINE_SIZE / 2, y * LINE_SIZE + LINE_SIZE / 2))
        surface.blit(text, text_rect)

    def draw_emoji(self, surface, pos, text, color, background):
        (x, y) = pos
        text = self.emoji_font.render(f"{text}", True, color, background)
        text_rect = text.get_rect(
            center=(x * LINE_SIZE + LINE_SIZE / 2, y * LINE_SIZE + LINE_SIZE / 2))
        surface.blit(text, text_rect)

    def open(self, pos):
        (x, y) = pos
        if x < 0 or self.width <= x: return False
        if y < 0 or self.height <= y: return False
        if self.get_state(pos) != STATE_NONE: return False

        print(f"open: {pos[0]} {pos[1]}")
        self.set_state(pos, STATE_OPEN)
        if self.is_mine(pos): return True

        if self.get_cell(pos) == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    self.open((x + dx, y + dy))

        return False

    def mark(self, pos):
        (x, y) = pos
        print(f"mark: {x} {y}")
        state = self.get_state(pos)
        if state == STATE_NONE:
            self.set_state(pos, STATE_MARK)
        elif state == STATE_MARK:
            self.set_state(pos, STATE_UNKNOWN)
        elif state == STATE_UNKNOWN:
            self.set_state(pos, STATE_NONE)

    def chording(self, pos):
        if self.get_state(pos) != STATE_OPEN: return False

        number = self.get_cell(pos)
        if self.count_flagged_neighbors(pos) == number:
            return self.open_not_flagged_neighbors(pos)
        return False

    def count_flagged_neighbors(self, pos):
        (x, y) = pos

        result = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                try:
                    new_pos = (x + dx, y + dy)
                    if self.get_state(new_pos) == STATE_MARK:
                        result += 1
                    elif self.get_state(new_pos) == STATE_UNKNOWN:
                        return 0
                except IndexError:
                    print(f"index error {x + dx}, {y + dy}")
                    pass
        return result

    def open_not_flagged_neighbors(self, pos):
        (x, y) = pos

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                try:
                    new_pos = (x + dx, y + dy)
                    if self.get_state(new_pos) == STATE_NONE:
                        if self.open(new_pos):
                            return True
                except IndexError:
                    print(f"index error {x + dx}, {y + dy}")
                    pass
        return False
