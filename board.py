import random
import pygame
from const import *


class Board:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

        self.size = min(int(SCREEN_HEIGHT / self.rows), int(SCREEN_WIDTH / self.columns))
        self.start_x = SCREEN_WIDTH / 2 - (self.size * self.columns) / 2
        self.start_y = SCREEN_HEIGHT / 2 - (self.size * self.rows) / 2
        self.width = self.size * self.columns
        self.height = self.size * self.rows

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
                pos = (x + x_delta, y + y_delta)
                if not self.is_valid_position(pos): continue

                value = self.mine_field[pos[1]][pos[0]]
                if value == FIELD_MINE:
                    result += 1

        return result

    def draw(self, surface):
        for y in range(self.rows):
            for x in range(self.columns):
                rect = self.get_cell_bound(x, y)
                pygame.draw.rect(surface, WHITE, rect, 1)

                fill_rect = rect.inflate(-3, -3).move(1, 1)
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

    def get_cell_bound(self, x, y):
        return pygame.Rect(self.start_x + x * self.size, self.start_y + y * self.size,
                           self.size + 1, self.size + 1)

    def draw_text(self, surface, pos, title, color):
        x, y = pos

        text = self.font.render(f"{title}", True, color, None)
        text_rect = text.get_rect(center=self.get_cell_bound(x, y).center)
        surface.blit(text, text_rect)

    def on_click(self, pos, button):
        relative_pos = (pos[0] - self.start_x, pos[1] - self.start_y)

        if relative_pos[0] < 0: return
        if relative_pos[1] < 0: return

        if self.width < relative_pos[0]: return
        if self.height < relative_pos[1]: return

        index_pos = (int(relative_pos[0] / self.size), int(relative_pos[1] / self.size))

        if button == pygame.BUTTON_LEFT:
            self.open(index_pos)
        elif button == pygame.BUTTON_RIGHT:
            self.mark(index_pos)

    def open(self, index_pos):
        if not self.is_valid_position(index_pos): return

        x, y = index_pos
        state = self.state_field[y][x]
        if state != STATE_HIDDEN: return

        self.state_field[y][x] = STATE_OPEN

        mine = self.mine_field[y][x]
        if mine == 0:
            for y_delta in [-1, 0, 1]:
                for x_delta in [-1, 0, 1]:
                    new_pos = (x + x_delta, y + y_delta)
                    self.open(new_pos)

    def mark(self, index_pos):
        x, y = index_pos
        state = self.state_field[y][x]
        if state == STATE_HIDDEN:
            self.state_field[y][x] = STATE_FLAGGED
        elif state == STATE_FLAGGED:
            self.state_field[y][x] = STATE_QUESTION
        elif state == STATE_QUESTION:
            self.state_field[y][x] = STATE_HIDDEN

    def is_valid_position(self, pos):
        x, y = pos
        if x < 0 or self.columns <= x: return False
        if y < 0 or self.rows <= y: return False
        return True
