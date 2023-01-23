import pygame as pg

class Score:
    def __init__(self, game, score):
        self.game = game
        self.score = score



    def draw(self):
        font = pg.font.Font('freesansbold.tff', 30)
        self.game.screen.blit(font.render(f'score: {self.score}', True, "white",), (5, 5))


