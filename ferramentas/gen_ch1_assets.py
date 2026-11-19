# Graficos novos do Capitulo 1: Monark, rato, capivara, sino, Baratelli com flor e imagens de cena.
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, sheet, PROJ

G.PREV = HERE + '/prev/'
os.makedirs(G.PREV, exist_ok=True)
preview = G.preview
FONTS = 'C:/Windows/Fonts/'


def blank():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


# ---------------------------------------------------------------- Monark (cigano vidente)
SK = C(116, 74, 50); SK_D = C(88, 54, 36); SK_L = C(140, 94, 64)
HR = C(26, 20, 20); HR_L = C(52, 40, 38)
BND = C(196, 34, 44); BND_D = C(140, 20, 32); BND_DOT = C(250, 214, 90)
GOLD = C(244, 198, 64); GOLD_D = C(190, 140, 30)
SHIRT = C(244, 240, 228); SHIRT_D = C(206, 198, 184)
VEST = C(150, 28, 40); VEST_D = C(104, 18, 30)
SASH = C(120, 60, 170); SASH_D = C(84, 40, 124)
PANT = C(40, 36, 46); PANT_D = C(26, 24, 32)
BOOT = C(98, 60, 34); BOOT_D = C(66, 40, 24)
MO = C(30, 18, 16)


def monark_down(p):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    # pernas e botas
    d.rectangle((17, 34, 22, ly), fill=PANT); d.rectangle((26, 34, 31, ry), fill=PANT)
    d.line((22, 34, 22, ly), fill=PANT_D); d.line((26, 34, 26, ry), fill=PANT_D)
    d.rectangle((16, ly - 2, 22, ly + 3), fill=BOOT); d.line((16, ly + 3, 22, ly + 3), fill=BOOT_D)
    d.rectangle((26, ry - 2, 32, ry + 3), fill=BOOT); d.line((26, ry + 3, 32, ry + 3), fill=BOOT_D)
    # tronco largo
    d.polygon([(12, 20), (36, 20), (33, 35), (15, 35)], fill=SHIRT)
    d.polygon([(13, 20), (19, 20), (20, 34), (15, 34)], fill=VEST)
    d.polygon([(35, 20), (29, 20), (28, 34), (33, 34)], fill=VEST)
    d.line((19, 20, 20, 34), fill=GOLD); d.line((29, 20, 28, 34), fill=GOLD)
    d.polygon([(20, 20), (28, 20), (24, 27)], fill=SK)  # peito aberto
    d.line((21, 21, 24, 26), fill=GOLD); d.line((27, 21, 24, 26), fill=GOLD)
    d.ellipse((23, 25, 25, 27), fill=GOLD)
    d.rectangle((15, 31, 33, 34), fill=SASH); d.line((15, 34, 33, 34), fill=SASH_D)
    d.rectangle((30, 33, 32, 38), fill=SASH)
    # bracos fortes
    d.ellipse((7, 19, 15, 27), fill=SHIRT); d.ellipse((33, 19, 41, 27), fill=SHIRT)
    d.rectangle((8, 25, 13, 33), fill=SK); d.rectangle((35, 25, 40, 33), fill=SK)
    d.line((8, 25, 8, 33), fill=SK_D); d.line((40, 25, 40, 33), fill=SK_D)
    d.rectangle((8, 26, 13, 27), fill=GOLD_D); d.rectangle((35, 26, 40, 27), fill=GOLD_D)
    # cabeca
    d.ellipse((17, 5, 31, 21), fill=SK)
    d.ellipse((15, 2, 33, 11), fill=HR)
    d.rectangle((16, 7, 32, 10), fill=BND); d.line((16, 10, 32, 10), fill=BND_D)
    for x in range(18, 32, 4):
        d.point((x, 8), fill=BND_DOT)
    d.polygon([(32, 8), (36, 12), (35, 16), (33, 11)], fill=BND)  # ponta do lenco
    d.rectangle((20, 13, 21, 14), fill=MO); d.rectangle((27, 13, 28, 14), fill=MO)
    d.line((19, 12, 22, 12), fill=HR); d.line((26, 12, 29, 12), fill=HR)
    d.line((21, 17, 27, 17), fill=HR)  # bigode
    d.polygon([(19, 17), (29, 17), (27, 21), (21, 21)], fill=HR)
    d.line((22, 18, 26, 18), fill=C(150, 60, 60))
    d.ellipse((15, 14, 18, 18), outline=GOLD)  # argola
    return outline(im, MO)


def monark_up(p):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((17, 34, 22, ly), fill=PANT); d.rectangle((26, 34, 31, ry), fill=PANT)
    d.rectangle((16, ly - 2, 22, ly + 3), fill=BOOT); d.rectangle((26, ry - 2, 32, ry + 3), fill=BOOT)
    d.polygon([(12, 20), (36, 20), (33, 35), (15, 35)], fill=VEST)
    d.line((24, 21, 24, 31), fill=VEST_D)
    d.rectangle((15, 31, 33, 34), fill=SASH)
    d.ellipse((7, 19, 15, 27), fill=SHIRT); d.ellipse((33, 19, 41, 27), fill=SHIRT)
    d.rectangle((8, 25, 13, 33), fill=SK); d.rectangle((35, 25, 40, 33), fill=SK)
    d.ellipse((17, 4, 31, 20), fill=HR)
    d.ellipse((16, 2, 32, 12), fill=HR_L)
    d.rectangle((16, 7, 32, 10), fill=BND)
    d.polygon([(22, 9), (26, 9), (28, 17), (24, 15), (20, 17)], fill=BND)  # no do lenco
    return outline(im, MO)


def monark_left(p):
    im, d = blank()
    fx = {-1: 14, 0: 19, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 18}[p]
    d.rectangle((bx, 34, bx + 5, 42), fill=PANT_D); d.rectangle((bx - 1, 41, bx + 5, 45), fill=BOOT_D)
    d.rectangle((fx, 34, fx + 5, 42), fill=PANT); d.rectangle((fx - 2, 41, fx + 5, 45), fill=BOOT)
    d.polygon([(16, 20), (32, 20), (31, 35), (17, 35)], fill=SHIRT)
    d.polygon([(22, 20), (32, 20), (31, 34), (22, 34)], fill=VEST)
    d.line((22, 20, 22, 34), fill=GOLD)
    d.rectangle((17, 31, 31, 34), fill=SASH)
    d.ellipse((20, 19, 29, 28), fill=SHIRT)
    d.rectangle((21, 25, 26, 34), fill=SK); d.line((21, 25, 21, 34), fill=SK_D)
    d.rectangle((21, 27, 26, 28), fill=GOLD_D)
    d.ellipse((15, 5, 29, 21), fill=SK)
    d.point((14, 13), fill=SK); d.point((14, 14), fill=SK_D)
    d.ellipse((19, 2, 33, 14), fill=HR)
    d.rectangle((15, 7, 31, 10), fill=BND)
    d.polygon([(30, 8), (35, 12), (34, 17), (31, 12)], fill=BND)
    d.rectangle((17, 13, 18, 14), fill=MO)
    d.polygon([(14, 17), (22, 17), (22, 21), (16, 21)], fill=HR)
    d.ellipse((22, 14, 25, 18), outline=GOLD)
    return outline(im, MO)


def make_monark():
    down = [monark_down(p) for p in (-1, 0, 1)]
    left = [monark_left(p) for p in (-1, 0, 1)]
    right = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in left]
    up = [monark_up(p) for p in (-1, 0, 1)]
    sh = sheet([down, left, right, up])
    sh.save(PROJ + '/img/characters/$Monark.png')
    preview(sh, 'monark.png', 4)


# ---------------------------------------------------------------- Rato
RAT = C(124, 120, 128); RAT_L = C(164, 160, 168); RAT_D = C(88, 84, 94)
PINK = C(232, 150, 160); RED_EYE = C(220, 40, 50); R_OUT = C(40, 34, 40)


def rat_down(p):
    im, d = blank()
    d.line((24, 26, 24 + p * 3, 18), fill=PINK, width=2)  # rabo atras
    d.ellipse((15, 24, 33, 42), fill=RAT)
    d.ellipse((18, 26, 30, 34), fill=RAT_L)
    d.ellipse((15, 30, 20, 35), fill=RAT_D); d.ellipse((28, 30, 33, 35), fill=RAT_D)
    d.ellipse((17, 32, 31, 45), fill=RAT)
    d.ellipse((15, 29, 21, 35), fill=RAT); d.ellipse((16, 30, 20, 34), fill=PINK)
    d.ellipse((27, 29, 33, 35), fill=RAT); d.ellipse((28, 30, 32, 34), fill=PINK)
    d.point((21, 38), fill=RED_EYE); d.point((27, 38), fill=RED_EYE)
    d.ellipse((23, 43, 25, 45), fill=PINK)
    d.line((18, 42, 21, 43), fill=RAT_D); d.line((30, 42, 27, 43), fill=RAT_D)
    fy = 44 + (1 if p else 0)
    d.point((19 - p, fy), fill=PINK); d.point((29 + p, fy), fill=PINK)
    return outline(im, R_OUT)


def rat_up(p):
    im, d = blank()
    d.ellipse((15, 22, 33, 38), fill=RAT)
    d.ellipse((18, 24, 30, 32), fill=RAT_L)
    d.ellipse((15, 20, 21, 26), fill=RAT); d.ellipse((16, 21, 20, 25), fill=PINK)
    d.ellipse((27, 20, 33, 26), fill=RAT); d.ellipse((28, 21, 32, 25), fill=PINK)
    pts = [(24, 37), (24 + p * 2, 41), (24 - p * 3, 45), (24 + p * 2, 47)]
    d.line(pts, fill=PINK, width=2)
    fy = 38 + (1 if p else 0)
    d.point((18 - p, fy), fill=PINK); d.point((30 + p, fy), fill=PINK)
    return outline(im, R_OUT)


def rat_left(p):
    im, d = blank()
    pts = [(34, 36), (39, 33 + p), (43, 36 - p), (46, 32)]
    d.line(pts, fill=PINK, width=2)
    d.ellipse((16, 28, 37, 43), fill=RAT)
    d.ellipse((20, 29, 34, 35), fill=RAT_L)
    d.polygon([(17, 31), (8, 38), (17, 42)], fill=RAT)
    d.ellipse((15, 27, 22, 33), fill=RAT); d.ellipse((16, 28, 20, 32), fill=PINK)
    d.point((13, 35), fill=RED_EYE)
    d.ellipse((6, 37, 9, 40), fill=PINK)
    for x, o in ((18, p), (31, -p)):
        d.rectangle((x + o, 43, x + o + 2, 44), fill=PINK)
    return outline(im, R_OUT)


def make_rat():
    down = [rat_down(p) for p in (-1, 0, 1)]
    left = [rat_left(p) for p in (-1, 0, 1)]
    right = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in left]
    up = [rat_up(p) for p in (-1, 0, 1)]
    sh = sheet([down, left, right, up])
    sh.save(PROJ + '/img/characters/$Rato.png')
    preview(sh, 'rato.png', 4, bg=(70, 64, 60, 255))
    return sh


# ---------------------------------------------------------------- Capivara
CAP = C(150, 102, 62); CAP_L = C(184, 136, 90); CAP_D = C(112, 74, 44); NOSE = C(70, 46, 32)
C_OUT = C(56, 36, 24)


def capy_down(p):
    im, d = blank()
    l1 = 43 + (1 if p == -1 else 0); l2 = 43 + (1 if p == 1 else 0)
    d.ellipse((11, 16, 37, 40), fill=CAP)
    d.ellipse((14, 18, 34, 30), fill=CAP_L)
    for x, yb in ((15, l1), (30, l2)):
        d.rectangle((x, 36, x + 3, yb), fill=CAP_D)
    d.rectangle((16, 22, 32, 42), fill=CAP)
    d.rounded_rectangle((16, 26, 32, 44), 5, fill=CAP)
    d.ellipse((15, 20, 20, 25), fill=CAP_D); d.ellipse((28, 20, 33, 25), fill=CAP_D)
    d.rectangle((19, 30, 20, 31), fill=EYE_C); d.rectangle((28, 30, 29, 31), fill=EYE_C)
    d.rounded_rectangle((19, 37, 29, 44), 3, fill=CAP_D)
    d.rectangle((21, 39, 22, 40), fill=NOSE); d.rectangle((26, 39, 27, 40), fill=NOSE)
    return outline(im, C_OUT)


EYE_C = C(30, 20, 16)


def capy_up(p):
    im, d = blank()
    l1 = 43 + (1 if p == -1 else 0); l2 = 43 + (1 if p == 1 else 0)
    for x, yb in ((15, l1), (30, l2)):
        d.rectangle((x, 34, x + 3, yb), fill=CAP_D)
    d.ellipse((11, 14, 37, 42), fill=CAP)
    d.ellipse((14, 16, 34, 30), fill=CAP_L)
    d.ellipse((15, 12, 20, 17), fill=CAP_D); d.ellipse((28, 12, 33, 17), fill=CAP_D)
    return outline(im, C_OUT)


def capy_left(p):
    im, d = blank()
    off = {-1: (-2, 2), 0: (0, 0), 1: (2, -2)}[p]
    for x, o in ((32, off[0]), (16, off[1])):
        d.rectangle((x + o, 36, x + o + 3, 44), fill=CAP_D)
    d.ellipse((12, 20, 42, 40), fill=CAP)
    d.ellipse((16, 21, 38, 30), fill=CAP_L)
    d.rounded_rectangle((3, 20, 20, 33), 5, fill=CAP)
    d.ellipse((14, 18, 19, 23), fill=CAP_D)
    d.rectangle((9, 23, 10, 24), fill=EYE_C)
    d.rectangle((3, 26, 5, 28), fill=NOSE)
    for x, o in ((35, off[1]), (19, off[0])):
        d.rectangle((x + o, 37, x + o + 3, 45), fill=CAP)
    return outline(im, C_OUT)


def make_capybara():
    down = [capy_down(p) for p in (-1, 0, 1)]
    left = [capy_left(p) for p in (-1, 0, 1)]
    right = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in left]
    up = [capy_up(p) for p in (-1, 0, 1)]
    sh = sheet([down, left, right, up])
    sh.save(PROJ + '/img/characters/$Capivara.png')
    preview(sh, 'capivara.png', 4)
    return sh


# ---------------------------------------------------------------- Sino do trem (objeto 48x96)
BRONZE = C(196, 146, 54); BRONZE_L = C(238, 196, 98); BRONZE_D = C(136, 94, 30)
WOOD = C(112, 74, 44); WOOD_D = C(78, 50, 30); WOOD_L = C(144, 100, 62)


def bell_frame(angle):
    im = Image.new('RGBA', (48, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # poste e braco
    d.rectangle((6, 18, 11, 92), fill=WOOD); d.line((11, 18, 11, 92), fill=WOOD_D); d.line((6, 18, 6, 92), fill=WOOD_L)
    d.rectangle((4, 88, 13, 93), fill=WOOD_D)
    d.rectangle((6, 18, 42, 22), fill=WOOD); d.line((6, 22, 42, 22), fill=WOOD_D)
    d.line((11, 30, 22, 22), fill=WOOD, width=3)
    # sino (desenhado separado para girar)
    b = Image.new('RGBA', (40, 44), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
    bd.rectangle((18, 0, 21, 5), fill=C(80, 80, 86))
    bd.polygon([(12, 6), (27, 6), (31, 28), (36, 34), (3, 34), (8, 28)], fill=BRONZE)
    bd.polygon([(13, 7), (17, 7), (14, 30), (9, 31)], fill=BRONZE_L)
    bd.polygon([(24, 7), (27, 7), (31, 28), (29, 31)], fill=BRONZE_D)
    bd.rectangle((3, 32, 36, 35), fill=BRONZE_D); bd.line((4, 32, 35, 32), fill=BRONZE_L)
    bd.ellipse((16, 34, 23, 41), fill=C(90, 64, 26))
    b = b.rotate(angle, resample=Image.NEAREST, center=(20, 2))
    im.alpha_composite(b, (5, 22))
    return outline(im, C(40, 26, 18))


def make_bell():
    frames = [bell_frame(a) for a in (16, 0, -16)]
    sh = Image.new('RGBA', (144, 384), (0, 0, 0, 0))
    for r in range(4):
        for c, f in enumerate(frames):
            sh.alpha_composite(f, (c * 48, r * 96))
    sh.save(PROJ + '/img/characters/!$Sino.png')
    preview(sh.crop((0, 0, 144, 96)), 'sino.png', 4, bg=(60, 60, 80, 255))


# ---------------------------------------------------------------- Baratelli com a flor amaldicoada
def flower_icon(size=11):
    im = Image.new('RGBA', (size, size + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = size // 2
    d.line((c, c + 2, c, size + 5), fill=C(60, 140, 60), width=1)
    d.line((c, size + 2, c + 3, size), fill=C(60, 140, 60))
    for k in range(5):
        a = k / 5 * 2 * math.pi - math.pi / 2
        px, py = c + math.cos(a) * 3, c + math.sin(a) * 3
        d.ellipse((px - 2.5, py - 2.5, px + 2.5, py + 2.5), fill=C(220, 30, 70))
    d.ellipse((c - 1.5, c - 1.5, c + 1.5, c + 1.5), fill=C(255, 214, 60))
    return outline(im, C(70, 10, 30))


def make_baratelli_flower():
    base = Image.open(PROJ + '/img/characters/$Baratelli.png').convert('RGBA')
    fl = flower_icon(9).crop((0, 0, 11, 12))
    out = base.copy()
    # flor brotando no topo do chapeu (baixo, esquerda, direita, cima)
    pos = {0: 19, 1: 17, 2: 20, 3: 19}
    for r in range(4):
        for c in range(3):
            out.alpha_composite(fl, (c * 48 + pos[r], r * 48))
    out.save(PROJ + '/img/characters/$Baratelli_Flor.png')
    preview(out, 'baratelli_flor.png', 4)


# ---------------------------------------------------------------- Imagens de cena
def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def centered(d, y, txt, f, fill, shadow=None, W=816):
    w = d.textlength(txt, font=f)
    if shadow:
        d.text(((W - w) / 2 + 3, y + 3), txt, font=f, fill=shadow)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill)


def card(path, lines):
    im = Image.new('RGBA', (816, 624), (14, 10, 22, 255))
    n = G.value_noise(816, 624, 3, 4, 5)
    glow = np.clip(1 - np.hypot(*np.meshgrid(np.linspace(-1, 1, 816), np.linspace(-1, 1, 624))) * 0.9, 0, 1)
    arr = np.zeros((624, 816, 4), dtype=np.uint8)
    arr[..., 0] = (40 + 50 * glow * n).astype(np.uint8)
    arr[..., 1] = (20 + 24 * glow * n).astype(np.uint8)
    arr[..., 2] = (52 + 60 * glow * n).astype(np.uint8)
    arr[..., 3] = 255
    im = Image.fromarray(arr, 'RGBA')
    d = ImageDraw.Draw(im)
    for (y, txt, f, col) in lines:
        centered(d, y, txt, f, col, shadow=(0, 0, 0, 200))
    d.line((208, 330, 608, 330), fill=(220, 180, 90, 255), width=2)
    im.save(path)
    im.resize((408, 312)).save(G.PREV + os.path.basename(path))


def make_cards():
    gold = (246, 208, 110, 255); pink = (250, 214, 230, 255)
    card(PROJ + '/img/pictures/Capitulo1.png', [
        (220, 'Capítulo 1', font('georgiab.ttf', 64), gold),
        (350, 'A Baratelli, a Criança e a Flor', font('georgiai.ttf', 34), pink),
    ])
    card(PROJ + '/img/pictures/FimCapitulo1.png', [
        (220, 'Fim do Capítulo 1', font('georgiab.ttf', 58), gold),
        (350, 'A busca pela Peruca de Ouro continua...', font('georgiai.ttf', 30), pink),
    ])


def heart(size, col):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    r = size // 4
    d.ellipse((0, 0, 2 * r + 2, 2 * r + 2), fill=col)
    d.ellipse((size - 2 * r - 2, 0, size - 1, 2 * r + 2), fill=col)
    d.polygon([(1, r + 4), (size - 2, r + 4), (size // 2, size - 2)], fill=col)
    d.ellipse((r // 2, r // 2, r + 2, r + 2), fill=(255, 255, 255, 170))
    return im


def soft(im, glow_col, rad=10):
    a = im.split()[3].filter(ImageFilter.GaussianBlur(rad))
    g = Image.new('RGBA', im.size, glow_col); g.putalpha(a.point(lambda v: int(v * 0.8)))
    g.alpha_composite(im)
    return g


def make_happy():
    pad = 24
    h = heart(110, (240, 70, 120, 255))
    canvas = Image.new('RGBA', (110 + pad * 2, 110 + pad * 2), (0, 0, 0, 0)); canvas.alpha_composite(h, (pad, pad))
    soft(canvas, (255, 160, 200, 255)).save(PROJ + '/img/pictures/Feliz_Coracao.png')
    # flor grande
    f = Image.new('RGBA', (170, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(f)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        px, py = 85 + math.cos(a) * 38, 85 + math.sin(a) * 38
        d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=(255, 150, 190, 255))
        d.ellipse((px - 16, py - 16, px + 10, py + 10), fill=(255, 196, 220, 255))
    d.ellipse((60, 60, 110, 110), fill=(255, 210, 70, 255)); d.ellipse((70, 66, 92, 86), fill=(255, 240, 160, 255))
    soft(f, (255, 230, 240, 255), 8).save(PROJ + '/img/pictures/Feliz_Flor.png')
    # arco-iris
    w, hh = 520, 280
    rb = Image.new('RGBA', (w, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(rb)
    cols = [(240, 70, 70), (250, 150, 60), (250, 220, 80), (110, 200, 100), (90, 150, 240), (150, 100, 220)]
    for i, c in enumerate(cols):
        r = 250 - i * 18
        d.ellipse((260 - r, 270 - r, 260 + r, 270 + r), outline=c + (230,), width=18)
    rb = rb.crop((0, 0, w, 272))
    for cx in (60, 460):
        for k in range(6):
            dx = (k - 2.5) * 22
            ImageDraw.Draw(rb).ellipse((cx + dx - 30, 228 - (k % 2) * 10, cx + dx + 30, 272), fill=(255, 255, 255, 245))
    soft(rb, (255, 255, 255, 255), 6).save(PROJ + '/img/pictures/Feliz_ArcoIris.png')
    # ovelha e capivara grandes (a partir dos sprites)
    for name, src in (('Feliz_Ovelha', '$Ovelha'), ('Feliz_Capivara', '$Capivara')):
        sp = Image.open(PROJ + f'/img/characters/{src}.png').convert('RGBA').crop((48, 0, 96, 48))
        big = sp.resize((192, 192), Image.NEAREST)
        cv = Image.new('RGBA', (232, 232), (0, 0, 0, 0)); cv.alpha_composite(big, (20, 20))
        soft(cv, (255, 255, 255, 255), 6).save(PROJ + f'/img/pictures/{name}.png')


def make_wig():
    W, H = 360, 320
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rng = random.Random(4)
    gold = [(255, 214, 80), (246, 190, 50), (255, 236, 140), (214, 156, 30)]
    # forma da peruca: cachos em volta de uma cupula
    d.ellipse((90, 40, 270, 210), fill=gold[1] + (255,))
    pts = []
    for k in range(26):
        a = math.pi + k / 25 * math.pi
        pts.append((180 + math.cos(a) * 92, 130 + math.sin(a) * 92))
    for (x, y) in [(90 + i * 9, 130 + abs(math.sin(i)) * 0) for i in range(0)]:
        pass
    for side in (-1, 1):
        for k in range(7):
            cx = 180 + side * (78 + (k % 2) * 10)
            cy = 120 + k * 22
            for j in range(3):
                r = 20 - j * 5
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=gold[j % 4] + (255,))
    for k in range(14):
        a = math.pi + k / 13 * math.pi
        cx, cy = 180 + math.cos(a) * 82, 128 + math.sin(a) * 82
        d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=gold[k % 2] + (255,))
        d.arc((cx - 12, cy - 12, cx + 12, cy + 12), 200, 340, fill=gold[2] + (255,), width=3)
    d.ellipse((120, 70, 240, 170), fill=gold[1] + (255,))
    for _ in range(40):
        x = rng.randint(118, 240); y = rng.randint(60, 168)
        d.arc((x - 9, y - 9, x + 9, y + 9), rng.randint(0, 180), rng.randint(200, 360), fill=rng.choice(gold) + (255,), width=3)
    # brilhos
    for (x, y, s) in [(110, 60, 14), (262, 92, 10), (200, 40, 8), (150, 220, 9), (300, 200, 12), (60, 170, 9)]:
        d.polygon([(x, y - s), (x + s / 4, y - s / 4), (x + s, y), (x + s / 4, y + s / 4), (x, y + s),
                   (x - s / 4, y + s / 4), (x - s, y), (x - s / 4, y - s / 4)], fill=(255, 255, 240, 255))
    im = outline(im, C(120, 76, 10))
    soft(im, (255, 230, 120, 255), 16).save(PROJ + '/img/pictures/Peruca_Ouro.png')
    im.save(G.PREV + 'peruca.png')


if __name__ == '__main__':
    make_monark()
    make_rat()
    make_capybara()
    make_bell()
    make_baratelli_flower()
    make_cards()
    make_happy()
    make_wig()
    print('ok')
