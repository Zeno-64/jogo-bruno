# Capitulo 4: imagens de batalha da Arara Barraqueira e da Capivara Marombeira (frente e visao lateral).
import math, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_assets import C, outline, PROJ

PREV4 = HERE + '/prev4/'
WHITE = C(255, 255, 255); EYE_D = C(34, 28, 40)


def arara():
    W = 120
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    red, red_l, red_d = C(222, 40, 46), C(250, 96, 90), C(160, 22, 30)
    blue, yel = C(40, 96, 210), C(250, 210, 50)
    d.polygon([(70, 74), (82, 74), (104, 116), (92, 118)], fill=red_d)
    d.polygon([(76, 78), (82, 78), (98, 112), (94, 113)], fill=blue)
    d.polygon([(52, 46), (110, 22), (116, 40), (80, 70)], fill=blue)
    d.polygon([(54, 48), (96, 34), (90, 50), (70, 62)], fill=yel)
    d.ellipse((40, 40, 86, 96), fill=red)
    d.ellipse((50, 60, 80, 94), fill=red_l)
    d.polygon([(46, 50), (6, 30), (2, 44), (36, 70)], fill=blue)
    d.polygon([(44, 52), (18, 40), (20, 52), (38, 64)], fill=yel)
    d.ellipse((30, 10, 70, 50), fill=red)
    d.ellipse((34, 18, 52, 38), fill=WHITE)
    for k in range(4):
        d.line((36, 22 + k * 4, 50, 22 + k * 4), fill=C(240, 230, 230))
    d.ellipse((40, 22, 48, 32), fill=EYE_D); d.point((42, 24), fill=WHITE)
    d.line((36, 18, 50, 22), fill=EYE_D, width=2)
    d.polygon([(32, 28), (14, 30), (10, 42), (18, 50), (30, 42)], fill=C(232, 226, 214))
    d.polygon([(14, 40), (26, 40), (20, 50)], fill=C(60, 56, 60))
    d.chord((14, 34, 30, 48), 200, 340, fill=C(200, 60, 80))
    for (x, y) in ((64, 96), (72, 96)):
        d.line((x, y, x - 2, y + 10), fill=C(80, 70, 70), width=3)
    return outline(im, C(60, 16, 20))


def capivara():
    W = 130
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cap, cap_l, cap_d = C(150, 104, 62), C(184, 138, 90), C(110, 74, 42)
    iron, iron_l = C(70, 74, 86), C(150, 156, 170)
    for x in (34, 54, 86, 104):
        d.rectangle((x, 96, x + 12, 122), fill=cap_d)
    d.ellipse((24, 50, 122, 112), fill=cap)
    d.ellipse((40, 74, 112, 112), fill=cap_l)
    # braco com haltere (flexionando)
    d.line((44, 70, 22, 70), fill=cap, width=16)
    d.ellipse((24, 56, 44, 76), fill=cap_l)
    d.line((22, 74, 22, 44), fill=cap, width=14)
    d.line((10, 40, 34, 40), fill=iron_l, width=4)
    d.rectangle((4, 30, 12, 50), fill=iron); d.rectangle((32, 30, 40, 50), fill=iron)
    # cabeca
    d.ellipse((60, 20, 116, 72), fill=cap)
    d.ellipse((92, 34, 128, 70), fill=cap_l)
    d.ellipse((66, 16, 78, 28), fill=cap_d)
    d.rectangle((64, 30, 110, 36), fill=C(226, 40, 60))
    d.polygon([(64, 30), (54, 26), (56, 40), (64, 36)], fill=C(226, 40, 60))
    d.ellipse((96, 40, 104, 48), fill=EYE_D); d.point((98, 42), fill=WHITE)
    d.line((92, 38, 106, 41), fill=EYE_D, width=2)
    d.ellipse((118, 48, 124, 54), fill=EYE_D)
    d.arc((104, 52, 124, 66), 20, 160, fill=cap_d, width=2)
    for (x, y) in ((80, 60), (86, 64)):
        d.ellipse((x - 2, y - 3, x + 2, y + 3), fill=C(150, 200, 255))
    return outline(im, C(50, 30, 18))


def salvar(im, nome, k=2):
    big = im.resize((im.width * k, im.height * k), Image.NEAREST)
    for pasta in ('sv_enemies', 'enemies'):
        big.save(f'{PROJ}/img/{pasta}/{nome}.png')
    pv = Image.new('RGBA', big.size, (60, 90, 70, 255)); pv.alpha_composite(big); pv.save(PREV4 + nome + '.png')


if __name__ == '__main__':
    salvar(arara().transpose(Image.FLIP_LEFT_RIGHT), 'Arara_Barraqueira')
    salvar(capivara(), 'Capivara_Marombeira')
    print('ok')
