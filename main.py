import os
import random
import sys
import pygame as pg
from setting import *

#強制シャットダウンのための前置き
# os.system("sudo echo 悪魔のゲーム開始...。")

#プレイヤークラス
class Player:
    def __init__(self) -> None:
        self.player_img = pg.image.load("./images/pose_hashiru_guruguru_man.png")
        self.player_img = pg.transform.scale(self.player_img, (60, 70))
        self.player_img_flip = pg.transform.flip(self.player_img, True, False)
        self.player_rect = pg.Rect(100, HEIGHT / 2 - 60, 60, 70)
        self.isLeft = False

    def disp(self):
        if self.isLeft:
            screen.blit(self.player_img, self.player_rect)
        else:
            screen.blit(self.player_img_flip, self.player_rect)

#敵クラス
class Enemy:
    def __init__(self) -> None:
        self.enemy_img = pg.image.load("./images/mother_angry.png")
        self.enemy_img = pg.transform.scale(self.enemy_img, (60, 60))
        self.enemy_rect = pg.Rect(WIDTH - 100, HEIGHT / 2 - 60, 60, 60)
    
    def disp(self):
        screen.blit(self.enemy_img, self.enemy_rect)

#ゲームカセットクラス
class GameCassette:
    def __init__(self) -> None:   
        self.game_cassette_img = pg.image.load("./images/game_software_cassette.png")
        self.game_cassette_img = pg.transform.scale(self.game_cassette_img, (50, 50))
        self.gameCassettes = []
        self.appendGameCassettes()

    def appendGameCassettes(self):
        self.gameCassettes.clear()
        for i in range(10):
            gx = 50 + i * 70
            gy = random.randint(20, HEIGHT - 60)
            self.gameCassettes.append(pg.Rect(gx, gy, 50, 50))

    def disp(self):
        for gameCassette in self.gameCassettes:
            screen.blit(self.game_cassette_img, gameCassette)

#ゲームクラス
class Game:
    def __init__(self) -> None:
        #ページの設定用変数
        self.page = 0
        #プレイヤーを生成
        self.player = Player()
        #敵を生成
        self.enemy = Enemy()
        #ゲームカセットを生成
        self.gameCassette = GameCassette()

    def gameInit(self):
        ##画面を初期化
        screen.fill("white")
        font = pg.font.Font(None, 100)
        text = font.render("PRESS SPACE KEY", True, "black")
        screen.blit(text, (80 , HEIGHT / 2 - 50))

        ##入力
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.page = 1

    def gameStage(self):
        ##画面を初期化
        screen.fill("white")
        #当たり判定の表示
        # pg.draw.rect(screen, "green", self.player.player_rect, 1)
        # pg.draw.rect(screen, "green", self.enemy.enemy_rect, 1)

        ##入力
        vx = 0
        vy = 0
        key = pg.key.get_pressed()
        if key[pg.K_RIGHT]:
            vx = 3
            self.player.isLeft = False
        if key[pg.K_LEFT]:
            vx = -3
            self.player.isLeft = True
        if key[pg.K_UP]:
            vy = -3
        if key[pg.K_DOWN]:
            vy = 3

        ##描画、処理
        #プレイヤーを描画
        self.player.disp()

        #プレイヤーの移動
        self.player.player_rect.x += vx
        self.player.player_rect.y += vy

        #プレイヤーが画面外に行かないようにする処理
        if self.player.player_rect.x < 0:
            self.player.player_rect.x -= vx
        elif self.player.player_rect.x > WIDTH-60:
            self.player.player_rect.x -= vx
        if self.player.player_rect.y < 0:
            self.player.player_rect.y -= vy
        elif self.player.player_rect.y > HEIGHT-70:
            self.player.player_rect.y -= vy

        #プレイヤーが敵と衝突した時の処理
        if self.player.player_rect.colliderect(self.enemy.enemy_rect):
            #強制シャットダウン
            # os.system("sudo shutdown -r now")
            pg.mixer.Sound("./audio/gameOver.mp3").play()
            self.page = 3

        #プレイヤーがゲームカセットと衝突した時の処理
        if self.player.player_rect.collidelist(self.gameCassette.gameCassettes) != -1:
            pg.mixer.Sound("./audio/get.mp3").play()
            self.gameCassette.gameCassettes.pop(self.player.player_rect.collidelist(self.gameCassette.gameCassettes))

        #敵を描画
        self.enemy.disp()

        #敵がプレイヤーを追跡する処理
        if self.enemy.enemy_rect.x >= self.player.player_rect.x:
            self.enemy.enemy_rect.x -= 2
        if self.enemy.enemy_rect.x <= self.player.player_rect.x:
            self.enemy.enemy_rect.x += 2
        if self.enemy.enemy_rect.y >= self.player.player_rect.y:
            self.enemy.enemy_rect.y -= 2
        if self.enemy.enemy_rect.y <= self.player.player_rect.y:
            self.enemy.enemy_rect.y += 2

        #ゲームカセットを描画
        self.gameCassette.disp()

        #ゲームカセットの数が0になった時の処理
        if len(self.gameCassette.gameCassettes) <= 0:
            pg.mixer.Sound("./audio/clear.mp3").play()
            self.page = 2

    def gameReset(self):
        #プレイヤーと敵を初期位置へ
        self.player.player_rect = pg.Rect(100, HEIGHT / 2 - 60, 60, 70)
        self.enemy.enemy_rect = pg.Rect(WIDTH - 100, HEIGHT / 2 - 60, 60, 60)
        #変数を初期値にする
        self.player.isLeft = False
        #ゲームカセットを追加
        self.gameCassette.appendGameCassettes()

    def gameClear(self):
        ##画面を初期化
        screen.fill("white")
        font = pg.font.Font(None, 100)
        text = font.render("GAME CLEAR", True, "RED")
        screen.blit(text, (170 , HEIGHT / 2 - 50))

        ##入力
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.gameReset()
            self.page = 1

    def gameOver(self):
        ##画面を初期化
        screen.fill("black")
        font = pg.font.Font(None, 100)
        text = font.render("GAME OVER", True, "RED")
        screen.blit(text, (170 , HEIGHT / 2 - 50))

        ##入力
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.gameReset()
            self.page = 1

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