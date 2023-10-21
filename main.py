import os
import random
import sys
import pygame as pg

#シャットダウンのための前置き
# os.system("sudo echo 悪魔のゲーム開始...。")

#---定義
WIDTH = 800
HEIGHT = 600
page = 0

player_img = pg.image.load("./images/pose_hashiru_guruguru_man.png")
player_img = pg.transform.scale(player_img, (60, 70))
player_img_flip = pg.transform.flip(player_img, True, False)
player_rect = pg.Rect(100, HEIGHT / 2 - 60, 60, 70)
isLeft = False

enemy_img = pg.image.load("./images/mother_angry.png")
enemy_img = pg.transform.scale(enemy_img, (60, 60))
enemy_rect = pg.Rect(WIDTH - 100, HEIGHT / 2 - 60, 60, 60)

walls = [
    pg.Rect(0, 0, WIDTH, 10),
    pg.Rect(0, HEIGHT-10, WIDTH, 10),
    pg.Rect(0, 0, 10, HEIGHT),
    pg.Rect(WIDTH-10, 0, 10, HEIGHT)
]

game_img = pg.image.load("./images/game_software_cassette.png")
game_img = pg.transform.scale(game_img, (50, 50))
games = []
for i in range(10):
    gx = 50 + i * 70
    gy = random.randint(20, HEIGHT - 60)
    games.append(pg.Rect(gx, gy, 50, 50)) 

#---ゲームを初期化
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

#ゲームの初期設定関数
def gameInit():
    global page
    #---画面を初期化
    screen.fill("white")
    font = pg.font.Font(None, 100)
    text = font.render("PRESS SPACE KEY", True, "black")
    screen.blit(text, (80 , HEIGHT / 2 - 50))

    #入力
    key = pg.key.get_pressed()
    if key[pg.K_SPACE]:
        page = 1

#ゲームステージ関数
def game():
    global isLeft, page
    #---画面を初期化
    screen.fill("white")
    #当たり判定を表示
    pg.draw.rect(screen, "green", player_rect, 1)
    pg.draw.rect(screen, "green", enemy_rect, 1)

    #---入力
    vx = 0
    vy = 0
    key = pg.key.get_pressed()
    if key[pg.K_RIGHT]:
        vx = 3
        isLeft = False
    if key[pg.K_LEFT]:
        vx = -3
        isLeft = True
    if key[pg.K_UP]:
        vy = -3
    if key[pg.K_DOWN]:
        vy = 3

    #---描画、処理、判定
    #壁の処理
    #描画
    for wall in walls:
        pg.draw.rect(screen, "black", wall)

    #プレイヤーの処理
    #描画
    if isLeft:
        screen.blit(player_img, player_rect)
    else:
        screen.blit(player_img_flip, player_rect)

    #移動
    player_rect.x += vx
    player_rect.y += vy

    #壁と衝突した時の処理
    if player_rect.collidelist(walls) != -1:
        player_rect.x -= vx
        player_rect.y -= vy

    #敵と衝突した時の処理
    if player_rect.colliderect(enemy_rect):
        #強制シャットダウン
        # os.system("sudo shutdown now")
        pg.mixer.Sound("./audio/gameOver.mp3").play()
        page = 3

    #ゲームと衝突した時の処理
    if player_rect.collidelist(games) != -1:
        pg.mixer.Sound("./audio/get.mp3").play()
        games.pop(player_rect.collidelist(games))

    #敵の処理
    #描画
    screen.blit(enemy_img, enemy_rect)

    #追跡
    if enemy_rect.x >= player_rect.x:
        enemy_rect.x -= 2
    if enemy_rect.x <= player_rect.x:
        enemy_rect.x += 2
    if enemy_rect.y >= player_rect.y:
        enemy_rect.y -= 2
    if enemy_rect.y <= player_rect.y:
        enemy_rect.y += 2

    #ゲームカセットの処理
    for game in games:
        screen.blit(game_img, game)

    #ゲームカセットの数が0になったら
    if len(games) <= 0:
        pg.mixer.Sound("./audio/clear.mp3").play()
        page = 2

#ゲームリセット関数
def gameReset():
    global player_rect, enemy_rect, isLeft, games

    player_rect = pg.Rect(100, HEIGHT / 2 - 60, 60, 70)
    enemy_rect = pg.Rect(WIDTH - 100, HEIGHT / 2 - 60, 60, 60)

    isLeft = False
    games = []
    for i in range(10):
        gx = 50 + i * 70
        gy = random.randint(20, HEIGHT - 60)
        games.append(pg.Rect(gx, gy, 50, 50)) 

def gameClear():
    global page
    #---画面を初期化
    screen.fill("white")
    font = pg.font.Font(None, 100)
    text = font.render("GAME CLEAR", True, "RED")
    screen.blit(text, (170 , HEIGHT / 2 - 50))

    #入力
    key = pg.key.get_pressed()
    if key[pg.K_SPACE]:
        gameReset()
        page = 1

def gameOver():
    global page
    #---画面を初期化
    screen.fill("black")
    font = pg.font.Font(None, 100)
    text = font.render("GAME OVER", True, "RED")
    screen.blit(text, (170 , HEIGHT / 2 - 50))

    #入力
    key = pg.key.get_pressed()
    if key[pg.K_SPACE]:
        gameReset()
        page = 1

#---ループ
while True:
    if page == 0:
        gameInit()
    elif page == 1:
        game()
    elif page == 2:
        gameClear()
    elif page == 3:
        gameOver()

    #---画面を更新
    pg.display.update()
    pg.time.Clock().tick(60)

    #---イベント処理
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()