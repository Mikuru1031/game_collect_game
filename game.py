import pygame as pg
from setting import *
from player import Player
from enemy import Enemy
from gameCassete import GameCassette

#ゲームクラス
class Game:
    def __init__(self) -> None:
        #スクリーンを取得
        self.screen = pg.display.get_surface()
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
        self.screen.fill("white")
        font = pg.font.Font(None, 100)
        text = font.render("PRESS SPACE KEY", True, "black")
        self.screen.blit(text, (80 , HEIGHT / 2 - 50))

        ##入力
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.page = 1

    def gameStage(self):
        ##画面を初期化
        self.screen.fill("white")
        #当たり判定の表示
        # pg.draw.rect(self.screen, "green", self.player.player_rect, 1)
        # pg.draw.rect(self.screen, "green", self.enemy.enemy_rect, 1)

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
            #####強制シャットダウン#####
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
        self.screen.fill("white")
        font = pg.font.Font(None, 100)
        text = font.render("GAME CLEAR", True, "RED")
        self.screen.blit(text, (170 , HEIGHT / 2 - 50))

        ##入力
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.gameReset()
            self.page = 1

    def gameOver(self):
        ##画面を初期化
        self.screen.fill("black")
        font = pg.font.Font(None, 100)
        text = font.render("GAME OVER", True, "RED")
        self.screen.blit(text, (170 , HEIGHT / 2 - 50))

        ##入力
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.gameReset()
            self.page = 1
