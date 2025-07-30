import random
import pygame
from const import *


class Board:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

        self.size = min(int(SCREEN_WIDTH / self.columns), int(SCREEN_HEIGHT / self.rows))
        self.start_x = SCREEN_WIDTH / 2 - (self.size * self.columns) / 2
        self.start_y = SCREEN_HEIGHT / 2 - (self.size * self.rows) / 2

        self.mine_field = [
            [None for _ in range(self.columns)] for _ in range(self.rows)
        ]

        self.state_field = [
            [STATE_HIDDEN for _ in range(self.columns)] for _ in range(self.rows)
        ]

        self.font = pygame.font.Font(None, 17)

        max_mine_count = 10
        mine_count = 0
        while mine_count < max_mine_count:
            x = random.randrange(0, self.columns)
            y = random.randrange(0, self.rows)
            if self.mine_field[y][x] is None:
                self.mine_field[y][x] = FIELD_MINE
                mine_count += 1

        for y in range(self.rows):
            for x in range(self.columns):
                if self.mine_field[y][x] is None:
                    mine_count = self.calculate_mine_count(x, y)
                    self.mine_field[y][x] = mine_count

        print(self.mine_field)

    def calculate_mine_count(self, x, y):
        result = 0

        for y_delta in [-1, 0, 1]:
            for x_delta in [-1, 0, 1]:
                new_pos = (x + x_delta, y + y_delta)
                if not self.is_valid_position(new_pos): continue

                value = self.mine_field[new_pos[1]][new_pos[0]]
                if value == FIELD_MINE:
                    result += 1

        return result

    def draw(self, surface):

        for y in range(self.rows):
            for x in range(self.columns):
                rect = (self.start_x + x * self.size, self.start_y + y * self.size, self.size + 1,
                        self.size + 1)
                pygame.draw.rect(surface, WHITE, rect, 1)

                fill_rect = (self.start_x + x * self.size + 2, self.start_y + y * self.size + 2,
                             self.size + 1 - 3,
                             self.size + 1 - 3)
                state = self.state_field[y][x]
                pygame.draw.rect(surface, GREY, fill_rect, 0)

                if state == STATE_HIDDEN:
                    pass
                elif state == STATE_OPEN:
                    pygame.draw.rect(surface, BLACK, fill_rect, 0)
                    mine = self.mine_field[y][x]
                    self.draw_text(surface, (x, y), mine, WHITE)
                else:
                    self.draw_text(surface, (x, y), state, BLACK)

    def draw_text(self, surface, pos, title, color):
        x, y = pos

        text = self.font.render(f"{title}", True, color, None)
        text_rect = text.get_rect(
            center=(self.start_x + x * self.size + self.size / 2,
                    self.start_y + y * self.size + self.size / 2))
        surface.blit(text, text_rect)

    def on_click(self, pos, button):
        relative_pos = (pos[0] - self.start_x, pos[1] - self.start_y)

        if relative_pos[0] < 0: return False
        if relative_pos[1] < 0: return False

        if self.size * self.columns < relative_pos[0]: return False
        if self.size * self.rows < relative_pos[1]: return False

        index_pos = (int(relative_pos[0] / self.size), int(relative_pos[1] / self.size))

        if button == pygame.BUTTON_LEFT:
            return self.open(index_pos)
        elif button == pygame.BUTTON_RIGHT:
            self.mark(index_pos)
            return False

        return False

    def open(self, index_pos):
        x, y = index_pos
        state = self.state_field[y][x]
        if state != STATE_HIDDEN: return False

        self.state_field[y][x] = STATE_OPEN

        mine = self.mine_field[y][x]
        if mine == 0:
            for y_delta in [-1, 0, 1]:
                for x_delta in [-1, 0, 1]:
                    new_pos = (x + x_delta, y + y_delta)
                    if not self.is_valid_position(new_pos): continue

                    self.open(new_pos)
            return False

        return mine == FIELD_MINE

    def mark(self, index_pos):
        x, y = index_pos
        state = self.state_field[y][x]
        if state == STATE_HIDDEN:
            self.state_field[y][x] = STATE_FLAGGED
        elif state == STATE_FLAGGED:
            self.state_field[y][x] = STATE_QUESTION
        elif state == STATE_QUESTION:
            self.state_field[y][x] = STATE_HIDDEN

    def is_valid_position(self, position):
        x, y = position
        if x < 0 or self.columns <= x: return False
        if y < 0 or self.rows <= y: return False
        return True
