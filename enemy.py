import pygame as pg
from setting import *

class Enemy:
    def __init__(self) -> None:
        self.enemy_img = pg.image.load("./images/mother_angry.png")
        self.enemy_img = pg.transform.scale(self.enemy_img, (60, 60))
        self.enemy_rect = pg.Rect(WIDTH - 100, HEIGHT / 2 - 60, 60, 60)
        self.screen = pg.display.get_surface()
    
    def disp(self):
        self.screen.blit(self.enemy_img, self.enemy_rect)
