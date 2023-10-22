import pygame as pg
from setting import *
import random

class GameCassette:
    def __init__(self) -> None:   
        self.game_cassette_img = pg.image.load("./images/game_software_cassette.png")
        self.game_cassette_img = pg.transform.scale(self.game_cassette_img, (50, 50))
        self.gameCassettes = []
        self.appendGameCassettes()
        self.screen = pg.display.get_surface()

    def appendGameCassettes(self):
        self.gameCassettes.clear()
        for i in range(10):
            gx = 100 + i * 70
            gy = random.randint(20, HEIGHT - 60)
            self.gameCassettes.append(pg.Rect(gx, gy, 50, 50))

    def disp(self):
        for gameCassette in self.gameCassettes:
            self.screen.blit(self.game_cassette_img, gameCassette)
