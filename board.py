import random
import pygame
from const import *


class Board:
    def __init__(self):

        self.mine_field = [
            [None for _ in range(9)] for _ in range(9)
        ]

        self.state_field = [
            [STATE_HIDDEN for _ in range(9)] for _ in range(9)
        ]

        self.font = pygame.font.Font(None, 17)

        max_mine_count = 10
        mine_count = 0
        while mine_count < max_mine_count:
            x = random.randrange(0, 9)
            y = random.randrange(0, 9)
            if self.mine_field[y][x] is None:
                self.mine_field[y][x] = FIELD_MINE
                mine_count += 1

        for y in range(9):
            for x in range(9):
                if self.mine_field[y][x] is None:
                    mine_count = self.calculate_mine_count(x, y)
                    self.mine_field[y][x] = mine_count

        print(self.mine_field)

    def calculate_mine_count(self, x, y):
        result = 0

        for y_delta in [-1, 0, 1]:
            for x_delta in [-1, 0, 1]:
                try:
                    value = self.mine_field[y_delta + y][x_delta + x]
                    if value == FIELD_MINE:
                        result += 1
                except IndexError:
                    pass

        return result

    def draw(self, surface):
        size = int(SCREEN_HEIGHT / 9)
        start_x = SCREEN_WIDTH / 2 - (size * 9) / 2
        start_y = SCREEN_HEIGHT / 2 - (size * 9) / 2

        for y in range(9):
            for x in range(9):
                rect = (start_x + x * size, start_y + y * size, size + 1, size + 1)
                pygame.draw.rect(surface, WHITE, rect, 1)

                fill_rect = (start_x + x * size + 2, start_y + y * size + 2, size + 1 - 3, size + 1 - 3)
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
        size = int(SCREEN_HEIGHT / 9)
        start_x = SCREEN_WIDTH / 2 - (size * 9) / 2
        start_y = SCREEN_HEIGHT / 2 - (size * 9) / 2

        text = self.font.render(f"{title}", True, color, None)
        text_rect = text.get_rect(
            center=(start_x + x * size + size / 2, start_y + y * size + size / 2))
        surface.blit(text, text_rect)

    def on_click(self, pos, button):
        size = int(SCREEN_HEIGHT / 9)
        start_x = SCREEN_WIDTH / 2 - (size * 9) / 2
        start_y = SCREEN_HEIGHT / 2 - (size * 9) / 2
        relative_pos = (pos[0] - start_x, pos[1] - start_y)

        if relative_pos[0] < 0: return
        if relative_pos[1] < 0: return

        if size * 9 < relative_pos[0]: return
        if size * 9 < relative_pos[1]: return

        index_pos = (int(relative_pos[0] / size), int(relative_pos[1] / size))

        if button == pygame.BUTTON_LEFT:
            self.open(index_pos)
        elif button == pygame.BUTTON_RIGHT:
            self.mark(index_pos)


    def open(self, index_pos):
        x, y = index_pos
        state = self.state_field[y][x]
        if state != STATE_HIDDEN: return

        self.state_field[y][x] = STATE_OPEN

        mine = self.mine_field[y][x]
        if mine == 0:
            for y_delta in [-1, 0, 1]:
                for x_delta in [-1, 0, 1]:
                    try:
                        new_pos = (x + x_delta, y + y_delta)
                        self.open(new_pos)
                    except IndexError:
                        pass


    def mark(self, index_pos):
        x, y = index_pos
        state = self.state_field[y][x]
        if state == STATE_HIDDEN:
            self.state_field[y][x] = STATE_FLAGGED
        elif state == STATE_FLAGGED:
            self.state_field[y][x] = STATE_QUESTION
        elif state == STATE_QUESTION:
            self.state_field[y][x] = STATE_HIDDEN


