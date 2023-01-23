import pygame as pg
from random import randrange


class Hadik2:
    def __init__(self, game):
        self.vec2 = pg.math.Vector2

        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.range = self.size // 2, self.game.WINDOW_SIZE - self.size // 6, self.size
        self.rect.center = self.get_random_position()
        self.direction = self.vec2(0, 0)
        self.step_delay = 100
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.directions[pg.K_UP]:
                self.direction = self.vec2(0, -self.size)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1,pg.K_RIGHT: 1}

            if event.key == pg.K_DOWN and self.directions[pg.K_DOWN]:
                self.direction = self.vec2(0, self.size)
                self.directions = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1,pg.K_RIGHT: 1}

            if event.key == pg.K_LEFT and self.directions[pg.K_LEFT]:
                self.direction = self.vec2(-self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}

            if event.key == pg.K_RIGHT and self.directions[pg.K_RIGHT]:
                self.direction = self.vec2(self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0,pg.K_RIGHT: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(*self.range), randrange(*self.range)]

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.new_game()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'purple', segment) for segment in self.segments]

