# Capitulo 4: figuras dos itens novos (chaves do templo, cenoura dourada, guarana e pena de pavao).
import math, os, random, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_assets import C, outline
from gen_v2 import item_canvas, finish_item, star


def chave(nome, cor, cor_d, enfeite):
    im, S = item_canvas(); d = ImageDraw.Draw(im)
    cx, cy = 92 * S, 96 * S
    d.ellipse((cx - 50 * S, cy - 50 * S, cx + 50 * S, cy + 50 * S), fill=cor, outline=cor_d, width=6 * S)
    d.ellipse((cx - 22 * S, cy - 22 * S, cx + 22 * S, cy + 22 * S), fill=(0, 0, 0, 0), outline=cor_d, width=6 * S)
    d.polygon([(cx + 30 * S, cy + 30 * S), (cx + 42 * S, cy + 18 * S), (212 * S, 200 * S), (200 * S, 212 * S)], fill=cor, outline=cor_d)
    for (x, y) in [(176, 164), (196, 184)]:
        d.polygon([(x * S, y * S), ((x + 14) * S, (y - 14) * S), ((x + 26) * S, (y - 2) * S), ((x + 12) * S, (y + 12) * S)], fill=cor, outline=cor_d)
    enfeite(d, cx, cy, S)
    finish_item(outline(im, C(40, 30, 30)), S, (255, 240, 200, 255), nome)


def enf_jade(d, cx, cy, S):
    for k in range(6):
        a = k / 6 * 2 * math.pi
        x, y = cx + math.cos(a) * 36 * S, cy + math.sin(a) * 36 * S
        d.ellipse((x - 5 * S, y - 5 * S, x + 5 * S, y + 5 * S), fill=(200, 255, 220, 255))


def enf_ferradura(d, cx, cy, S):
    d.arc((cx - 40 * S, cy - 44 * S, cx + 40 * S, cy + 40 * S), 200, 340, fill=(255, 230, 120, 255), width=7 * S)


def enf_arcoiris(d, cx, cy, S):
    cores = [(232, 52, 60), (250, 140, 40), (250, 214, 50), (84, 190, 92), (62, 132, 222), (150, 92, 206)]
    for k, c in enumerate(cores):
        r = 46 - k * 4
        d.arc((cx - r * S, cy - r * S, cx + r * S, cy + r * S), 180, 360, fill=c + (255,), width=4 * S)


def cenoura():
    im, S = item_canvas(); d = ImageDraw.Draw(im)
    d.polygon([(70 * S, 70 * S), (110 * S, 50 * S), (200 * S, 210 * S), (190 * S, 214 * S)], fill=(255, 196, 40, 255))
    d.polygon([(70 * S, 70 * S), (110 * S, 50 * S), (150 * S, 120 * S), (120 * S, 134 * S)], fill=(255, 214, 80, 255))
    for k in range(5):
        y = 90 + k * 22
        d.line((80 * S + k * 18 * S, y * S, 100 * S + k * 18 * S, (y - 8) * S), fill=(200, 140, 20, 255), width=3 * S)
    for (dx, dy) in [(-30, -40), (-10, -50), (10, -44)]:
        d.ellipse(((88 + dx) * S, (56 + dy) * S, (108 + dx) * S, (100 + dy) * S), fill=(90, 190, 80, 255))
    for (x, y, r) in [(60, 150, 12), (200, 80, 10), (150, 200, 8)]:
        star(d, x * S, y * S, r * S, (255, 255, 230, 255))
    finish_item(outline(im, C(110, 70, 10)), S, (255, 214, 80, 255), 'Item_Cenoura')


def guarana():
    im, S = item_canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((90 * S, 70 * S, 166 * S, 220 * S), 20 * S, fill=(60, 140, 70, 255))
    d.rectangle((110 * S, 40 * S, 146 * S, 74 * S), fill=(60, 140, 70, 255))
    d.rectangle((106 * S, 30 * S, 150 * S, 44 * S), fill=(220, 40, 40, 255))
    d.rounded_rectangle((98 * S, 110 * S, 158 * S, 176 * S), 10 * S, fill=(250, 240, 220, 255))
    for (x, y) in [(116, 140), (140, 140), (128, 156)]:
        d.ellipse(((x - 10) * S, (y - 10) * S, (x + 10) * S, (y + 10) * S), fill=(200, 30, 40, 255))
        d.ellipse(((x - 5) * S, (y - 5) * S, (x + 5) * S, (y + 5) * S), fill=(255, 255, 255, 255))
        d.ellipse(((x - 2) * S, (y - 2) * S, (x + 2) * S, (y + 2) * S), fill=(20, 20, 20, 255))
    finish_item(outline(im, C(20, 50, 20)), S, (180, 255, 180, 255), 'Item_Guarana')


def pena():
    im, S = item_canvas(); d = ImageDraw.Draw(im)
    d.line((60 * S, 220 * S, 170 * S, 50 * S), fill=(230, 220, 190, 255), width=5 * S)
    for k in range(14):
        t = k / 14
        x, y = 60 + 110 * t, 220 - 170 * t
        d.line((x * S, y * S, (x - 34 + t * 10) * S, (y - 6) * S), fill=(70, 170, 140, 255), width=3 * S)
        d.line((x * S, y * S, (x + 20) * S, (y + 16 - t * 10) * S), fill=(70, 170, 140, 255), width=3 * S)
    cx, cy = 172 * S, 56 * S
    d.ellipse((cx - 40 * S, cy - 50 * S, cx + 40 * S, cy + 50 * S), fill=(36, 122, 112, 255))
    d.ellipse((cx - 28 * S, cy - 36 * S, cx + 28 * S, cy + 36 * S), fill=(236, 196, 70, 255))
    d.ellipse((cx - 18 * S, cy - 24 * S, cx + 18 * S, cy + 24 * S), fill=(40, 90, 200, 255))
    d.ellipse((cx - 8 * S, cy - 11 * S, cx + 8 * S, cy + 11 * S), fill=(16, 26, 70, 255))
    finish_item(outline(im, C(20, 50, 50)), S, (160, 255, 230, 255), 'Item_Pena')


if __name__ == '__main__':
    chave('Item_Chave_Jade', (90, 200, 140, 255), (30, 110, 70, 255), enf_jade)
    chave('Item_Chave_Ferradura', (220, 170, 90, 255), (130, 90, 40, 255), enf_ferradura)
    chave('Item_Chave_ArcoIris', (240, 236, 250, 255), (130, 110, 170, 255), enf_arcoiris)
    cenoura()
    guarana()
    pena()
    print('ok')
