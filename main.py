import os
import sys
import pygame as pg
from setting import *
from game import Game

#####強制シャットダウンのための前置き#####
# os.system("sudo echo 悪魔のゲーム開始...。")

##ゲームを初期化
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

#ゲームを生成
game = Game()

##ループ
while True:
    #ゲームを開始
    if game.page == 0:
        game.gameInit()
    elif game.page == 1:
        game.gameStage()
    elif game.page == 2:
        game.gameClear()
    elif game.page == 3:
        game.gameOver()

    ##画面を更新
    pg.display.update()
    pg.time.Clock().tick(60)

    ##イベント処理
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()