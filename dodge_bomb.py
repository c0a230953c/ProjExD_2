import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん または 爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def create_bomb_images_and_accs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の拡大サーフェスと加速度のリストを返す
    """
    bd_imgs = []
    bd_accs = [a for a in range(1, 11)]
    
    for r in range(1, 11):
        bd_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bd_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bd_imgs.append(bd_img)
    
    return bd_imgs, bd_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bd_imgs, bd_accs = create_bomb_images_and_accs()
    bd_rct = bd_imgs[0].get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, -5
    gob_img = pg.Surface((1100, 650))
    gob_img.set_alpha(128)
    pg.draw.rect(gob_img, (0, 0, 0), pg.Rect(0, 0, 800, 1600))
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver", True, (255, 255, 255))
    cry_kk_img = pg.image.load("fig/8.png")

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bd_rct):  #   工科トンと爆弾が重なっていたら
            screen.blit(gob_img, (0, 0))
            screen.blit(txt, [420, 280])
            screen.blit(cry_kk_img, (360, 280))
            screen.blit(cry_kk_img, (730, 280))
            pg.display.flip()
            time.sleep(5)
            return
        idx = min(tmr // 500, 9) 
        bd_img = bd_imgs[idx]
        avx = vx * bd_accs[idx]
        avy = vy * bd_accs[idx]
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bd_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
