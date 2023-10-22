import pygame as pg
from setting import *

class Player:
    def __init__(self) -> None:
        self.player_img = pg.image.load("./images/pose_hashiru_guruguru_man.png")
        self.player_img = pg.transform.scale(self.player_img, (60, 70))
        self.player_img_flip = pg.transform.flip(self.player_img, True, False)
        self.player_rect = pg.Rect(100, HEIGHT / 2 - 60, 60, 70)
        self.isLeft = False
        self.screen = pg.display.get_surface()

    def disp(self):
        if self.isLeft:
            self.screen.blit(self.player_img, self.player_rect)
        else:
            self.screen.blit(self.player_img_flip, self.player_rect)
