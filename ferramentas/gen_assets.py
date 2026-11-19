# Gera os graficos do jogo a partir da foto e de desenho em pixel art.
import os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

PROJ = 'K:/Kevin/workspace/jogo-bruno'
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referencias', '1.webp')
PREV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prev') + os.sep
os.makedirs(PREV, exist_ok=True)
random.seed(7)
np.random.seed(7)


def C(*v):
    return tuple(v) + (255,) if len(v) == 3 else tuple(v)


def outline(img, color):
    a = img.split()[3].point(lambda v: 255 if v > 0 else 0)
    dil = a.filter(ImageFilter.MaxFilter(3))
    edge = ImageChops.subtract(dil, a)
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste(Image.new('RGBA', img.size, color), (0, 0), edge)
    out.alpha_composite(img)
    return out


def preview(img, name, scale=4, bg=(120, 170, 110, 255)):
    b = Image.new('RGBA', img.size, bg)
    b.alpha_composite(img)
    b.resize((img.width * scale, img.height * scale), Image.NEAREST).save(PREV + name)


# ---------------------------------------------------------------- Baratelli
HAT = C(232, 150, 176); HAT_L = C(248, 192, 208); HAT_D = C(192, 106, 138); BAND = C(204, 88, 126)
HAIR = C(108, 68, 38); HAIR_L = C(146, 96, 58); HAIR_D = C(72, 44, 24)
SKIN = C(242, 204, 174); SKIN_D = C(214, 166, 136)
BEARD = C(80, 52, 32); BEARD_L = C(108, 72, 46)
GLASS = C(52, 52, 64); LENS = C(226, 236, 242)
EYE = C(36, 26, 26); MOUTH = C(190, 104, 104)
DRESS = C(184, 150, 222); DRESS_L = C(216, 196, 244); DRESS_D = C(148, 114, 196); DRESS_DD = C(118, 88, 168)
SHOE = C(250, 210, 24); SHOE_D = C(204, 160, 10)
BAG = C(252, 240, 206); BAG_D = C(222, 198, 146); COMB = C(228, 58, 72); BEAK = C(246, 184, 38)
STRAP = C(150, 96, 54)
OUT = C(46, 28, 44)


def curls(d, box, color, step=3):
    x0, y0, x1, y1 = box
    for y in range(y0, y1, step):
        for x in range(x0 + (y // step) % 2, x1, step):
            d.point((x, y), fill=color)


def skirt(d, cx, top, bottom, wtop, wbot, sway=0):
    d.polygon([(cx - wtop, top), (cx + wtop, top), (cx + wbot + sway, bottom), (cx - wbot + sway, bottom)], fill=DRESS)
    for i, yy in enumerate(range(top + 4, bottom + 1, 4)):
        t = (yy - top) / (bottom - top)
        w = int(wtop + (wbot - wtop) * t)
        s = int(sway * t)
        d.line((cx - w + s, yy - 1, cx + w + s, yy - 1), fill=DRESS_L)
        d.line((cx - w + s, yy, cx + w + s, yy), fill=DRESS_D)
    w = wbot
    d.line((cx - w + sway, bottom, cx + w + sway, bottom), fill=DRESS_DD)
    for x in range(cx - w + 1 + sway, cx + w + sway, 3):
        d.point((x, bottom - 1), fill=DRESS_L)



def hat(d, side=False):
    if side:
        d.ellipse((5, 5, 39, 11), fill=HAT); d.arc((5, 5, 39, 11), 10, 170, fill=HAT_D); d.ellipse((8, 5, 36, 8), fill=HAT_L)
        d.ellipse((15, 0, 29, 8), fill=HAT); d.ellipse((17, 1, 25, 4), fill=HAT_L); d.rectangle((15, 6, 29, 7), fill=BAND)
    else:
        d.ellipse((8, 5, 40, 12), fill=HAT); d.arc((8, 5, 40, 12), 10, 170, fill=HAT_D); d.ellipse((11, 5, 37, 9), fill=HAT_L)
        d.ellipse((17, 0, 31, 8), fill=HAT); d.ellipse((19, 1, 27, 4), fill=HAT_L); d.rectangle((17, 6, 31, 7), fill=BAND)
        for x in range(11, 38, 4):
            d.point((x, 10), fill=HAT_D)


def head_front(d):
    d.ellipse((17, 10, 31, 25), fill=SKIN)
    d.rectangle((17, 16, 18, 21), fill=BEARD); d.rectangle((30, 16, 31, 21), fill=BEARD)
    d.polygon([(18, 20), (30, 20), (30, 23), (27, 27), (21, 27), (18, 23)], fill=BEARD)
    d.line((20, 19, 28, 19), fill=BEARD)
    d.line((21, 24, 27, 24), fill=BEARD_L)
    d.line((22, 22, 26, 22), fill=MOUTH)
    d.rectangle((18, 13, 22, 16), outline=GLASS, fill=LENS)
    d.rectangle((26, 13, 30, 16), outline=GLASS, fill=LENS)
    d.line((23, 14, 25, 14), fill=GLASS)
    d.rectangle((20, 14, 20, 15), fill=EYE); d.rectangle((28, 14, 28, 15), fill=EYE)
    d.polygon([(13, 9), (18, 9), (18, 19), (17, 29), (15, 33), (12, 27)], fill=HAIR)
    d.polygon([(30, 9), (35, 9), (36, 27), (33, 33), (31, 29), (30, 19)], fill=HAIR)
    curls(d, (13, 11, 18, 32), HAIR_L); curls(d, (31, 11, 36, 32), HAIR_L)
    hat(d)


def head_side(d):
    d.ellipse((14, 10, 26, 25), fill=SKIN)
    d.point((13, 16), fill=SKIN); d.point((13, 17), fill=SKIN_D)
    d.polygon([(14, 19), (23, 19), (25, 23), (21, 27), (16, 26), (14, 23)], fill=BEARD)
    d.line((15, 19, 19, 19), fill=BEARD)
    d.line((14, 21, 16, 21), fill=MOUTH)
    d.rectangle((15, 13, 18, 16), outline=GLASS, fill=LENS)
    d.line((19, 14, 23, 14), fill=GLASS)
    d.rectangle((15, 14, 15, 15), fill=EYE)
    d.polygon([(21, 9), (31, 9), (34, 20), (34, 31), (30, 35), (26, 32), (24, 24), (22, 17)], fill=HAIR)
    curls(d, (24, 11, 34, 33), HAIR_L)
    hat(d, side=True)


def bar_down(p):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # cabelo atras
    d.ellipse((13, 7, 35, 30), fill=HAIR_D)
    d.rectangle((13, 18, 35, 34), fill=HAIR_D)
    d.ellipse((13, 28, 35, 37), fill=HAIR_D)
    # sapatos
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.rectangle((18, ly, 21, ly + 2), fill=SHOE); d.line((18, ly + 2, 21, ly + 2), fill=SHOE_D)
    d.rectangle((27, ry, 30, ry + 2), fill=SHOE); d.line((27, ry + 2, 30, ry + 2), fill=SHOE_D)
    # saia e corpete
    skirt(d, 24, 30, 43, 7, 11, sway=p)
    d.rectangle((18, 24, 30, 31), fill=DRESS)
    d.line((18, 31, 30, 31), fill=DRESS_D)
    # gola de babados em V
    d.line((19, 24, 24, 29), fill=DRESS_L); d.line((29, 24, 24, 29), fill=DRESS_L)
    d.line((20, 24, 24, 28), fill=DRESS_D); d.line((28, 24, 24, 28), fill=DRESS_D)
    # bracos
    d.rectangle((15, 27, 17, 32), fill=SKIN); d.point((15, 32), fill=SKIN_D)
    d.rectangle((31, 27, 33, 32), fill=SKIN); d.point((33, 32), fill=SKIN_D)
    # mangas bufantes
    d.ellipse((13, 22, 19, 28), fill=DRESS_L); d.arc((13, 22, 19, 28), 20, 160, fill=DRESS_D)
    d.ellipse((29, 22, 35, 28), fill=DRESS_L); d.arc((29, 22, 35, 28), 20, 160, fill=DRESS_D)
    # alca da bolsa
    d.line((19, 23, 31, 30), fill=STRAP)
    # bolsa de galinha
    d.ellipse((29, 29, 38, 37), fill=BAG); d.arc((29, 29, 38, 37), 30, 150, fill=BAG_D)
    d.rectangle((32, 27, 34, 29), fill=COMB); d.point((35, 28), fill=COMB)
    d.point((31, 32), fill=EYE); d.point((36, 32), fill=EYE)
    d.rectangle((33, 33, 34, 34), fill=BEAK)
    head_front(d)
    return outline(im, OUT)


def bar_up(p):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.rectangle((18, ly, 21, ly + 2), fill=SHOE); d.line((18, ly + 2, 21, ly + 2), fill=SHOE_D)
    d.rectangle((27, ry, 30, ry + 2), fill=SHOE); d.line((27, ry + 2, 30, ry + 2), fill=SHOE_D)
    skirt(d, 24, 30, 43, 7, 11, sway=-p)
    d.rectangle((18, 24, 30, 31), fill=DRESS)
    d.rectangle((15, 27, 17, 32), fill=SKIN); d.rectangle((31, 27, 33, 32), fill=SKIN)
    d.ellipse((13, 22, 19, 28), fill=DRESS_L); d.ellipse((29, 22, 35, 28), fill=DRESS_L)
    # pedaco da bolsa aparecendo do lado esquerdo
    d.ellipse((10, 29, 16, 36), fill=BAG); d.rectangle((11, 27, 13, 29), fill=COMB)
    # cabelo longo cobrindo as costas
    d.ellipse((13, 6, 35, 30), fill=HAIR)
    d.rectangle((13, 18, 35, 33), fill=HAIR)
    d.ellipse((12, 27, 36, 38), fill=HAIR)
    curls(d, (14, 14, 35, 37), HAIR_L)
    curls(d, (15, 16, 34, 36), HAIR_D, step=4)
    hat(d)
    return outline(im, OUT)


def bar_left(p, bag=True):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # cabelo atras (nuca, lado direito)
    d.polygon([(21, 9), (33, 10), (35, 22), (35, 33), (30, 37), (24, 34), (22, 24)], fill=HAIR_D)
    # sapatos alternando
    fx = {-1: 15, 0: 19, 1: 22}[p]; bx = {-1: 26, 0: 24, 1: 19}[p]
    d.rectangle((bx, 43, bx + 4, 45), fill=SHOE_D)
    d.rectangle((fx, 43, fx + 4, 45), fill=SHOE); d.point((fx, 44), fill=SHOE_D)
    # saia
    skirt(d, 24, 30, 43, 5, 10, sway=-p)
    d.rectangle((20, 24, 28, 31), fill=DRESS)
    d.line((20, 31, 28, 31), fill=DRESS_D)
    d.line((20, 24, 20, 28), fill=DRESS_L)
    # braco e manga
    d.rectangle((22, 27, 24, 33), fill=SKIN); d.point((22, 33), fill=SKIN_D)
    d.ellipse((20, 22, 27, 28), fill=DRESS_L); d.arc((20, 22, 27, 28), 20, 160, fill=DRESS_D)
    if bag:
        d.line((26, 23, 25, 29), fill=STRAP)
        d.ellipse((21, 29, 30, 37), fill=BAG); d.arc((21, 29, 30, 37), 30, 150, fill=BAG_D)
        d.rectangle((24, 27, 26, 29), fill=COMB)
        d.point((23, 31), fill=EYE)
        d.rectangle((19, 32, 20, 33), fill=BEAK)
    head_side(d)
    return outline(im, OUT)


def sheet(frames_by_dir):
    sh = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for r, frames in enumerate(frames_by_dir):
        for c, f in enumerate(frames):
            sh.alpha_composite(f, (c * 48, r * 48))
    return sh


def make_baratelli():
    down = [bar_down(p) for p in (-1, 0, 1)]
    left = [bar_left(p) for p in (-1, 0, 1)]
    right = [bar_left(p, bag=False).transpose(Image.FLIP_LEFT_RIGHT) for p in (-1, 0, 1)]
    up = [bar_up(p) for p in (-1, 0, 1)]
    sh = sheet([down, left, right, up])
    sh.save(PROJ + '/img/characters/$Baratelli.png')
    preview(sh, 'baratelli.png', 4)


# ---------------------------------------------------------------- Ovelha
WOOL = C(242, 238, 228); WOOL_L = C(255, 255, 252); WOOL_D = C(214, 206, 192)
FACE = C(236, 226, 210); EAR = C(232, 168, 166); LEG = C(108, 98, 90); SH_OUT = C(84, 74, 66)


def fluffy(d, box, base=WOOL):
    x0, y0, x1, y1 = box
    d.ellipse(box, fill=WOOL_D)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    for i in range(14):
        a = i / 14 * 2 * np.pi
        px, py = cx + np.cos(a) * rx * 0.72, cy + np.sin(a) * ry * 0.72
        d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=base)
    d.ellipse((x0 + 3, y0 + 3, x1 - 3, y1 - 3), fill=base)
    for i in range(8):
        a = i / 8 * 2 * np.pi
        px, py = cx + np.cos(a) * rx * 0.45, cy + np.sin(a) * ry * 0.45 - 2
        d.point((px, py), fill=WOOL_L); d.point((px + 1, py), fill=WOOL_L)


def sheep_down(p):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    l1 = 43 + (1 if p == -1 else 0); l2 = 43 + (1 if p == 1 else 0)
    for x, yb in ((16, l2), (29, l1)):
        d.rectangle((x, 34, x + 2, yb), fill=LEG)
    fluffy(d, (10, 14, 38, 38))
    for x, yb in ((19, l1), (26, l2)):
        d.rectangle((x, 36, x + 2, yb + 1), fill=LEG)
    d.ellipse((11, 24, 18, 29), fill=FACE); d.ellipse((13, 25, 16, 28), fill=EAR)
    d.ellipse((30, 24, 37, 29), fill=FACE); d.ellipse((32, 25, 35, 28), fill=EAR)
    d.ellipse((17, 22, 31, 38), fill=FACE)
    d.ellipse((18, 18, 30, 26), fill=WOOL)
    d.rectangle((20, 28, 21, 29), fill=EYE); d.rectangle((27, 28, 28, 29), fill=EYE)
    d.rectangle((23, 34, 25, 35), fill=EAR)
    return outline(im, SH_OUT)


def sheep_up(p):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    l1 = 43 + (1 if p == -1 else 0); l2 = 43 + (1 if p == 1 else 0)
    for x, yb in ((16, l1), (29, l2), (19, l2), (26, l1)):
        d.rectangle((x, 34, x + 2, yb), fill=LEG)
    d.ellipse((13, 12, 19, 17), fill=FACE); d.ellipse((29, 12, 35, 17), fill=FACE)
    fluffy(d, (10, 13, 38, 39))
    d.ellipse((21, 33, 27, 39), fill=WOOL_L)
    return outline(im, SH_OUT)


def sheep_left(p):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    off = {-1: (-2, 2), 0: (0, 0), 1: (2, -2)}[p]
    for x, o in ((19, off[1]), (33, off[0])):
        d.rectangle((x + o, 34, x + o + 2, 43), fill=LEG)
    fluffy(d, (14, 17, 42, 38))
    for x, o in ((16, off[0]), (30, off[1])):
        d.rectangle((x + o, 35, x + o + 2, 44), fill=LEG)
    d.ellipse((4, 18, 17, 31), fill=FACE)
    d.ellipse((12, 16, 19, 21), fill=FACE); d.ellipse((14, 17, 17, 20), fill=EAR)
    d.ellipse((7, 14, 17, 21), fill=WOOL)
    d.rectangle((8, 22, 9, 23), fill=EYE)
    d.rectangle((4, 26, 5, 27), fill=EAR)
    return outline(im, SH_OUT)


def make_sheep():
    down = [sheep_down(p) for p in (-1, 0, 1)]
    left = [sheep_left(p) for p in (-1, 0, 1)]
    right = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in left]
    up = [sheep_up(p) for p in (-1, 0, 1)]
    sh = sheet([down, left, right, up])
    sh.save(PROJ + '/img/characters/$Ovelha.png')
    preview(sh, 'ovelha.png', 4)


# ---------------------------------------------------------------- Trem enferrujado
def value_noise(w, h, cells, octaves=4, seed=0):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        n = cells * (2 ** o)
        g = rng.random((n + 1, n + 1))
        g[-1, :] = g[0, :]; g[:, -1] = g[:, 0]
        ys = np.linspace(0, n, h, endpoint=False); xs = np.linspace(0, n, w, endpoint=False)
        y0 = ys.astype(int); x0 = xs.astype(int)
        fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
        fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)
        a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; dd = g[y0 + 1][:, x0 + 1]
        v = a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + dd * fx * fy
        acc += v * amp; tot += amp; amp *= 0.5
    return acc / tot


def rust_fill(img, box, seed, dark=False):
    x0, y0, x1, y1 = box
    w, h = x1 - x0 + 1, y1 - y0 + 1
    n = value_noise(w, h, 3, 4, seed)
    pal = [(70, 40, 24), (104, 56, 30), (140, 76, 38), (170, 96, 48), (196, 122, 64)]
    if dark:
        pal = [(48, 30, 20), (70, 42, 26), (96, 56, 32), (120, 70, 38), (140, 84, 46)]
    q = np.clip((n - 0.25) / 0.5 * len(pal), 0, len(pal) - 1).astype(int)
    arr = np.array(pal, dtype=np.uint8)[q]
    jitter = np.random.default_rng(seed + 1).integers(-10, 11, (h, w, 1))
    arr = np.clip(arr.astype(int) + jitter, 0, 255).astype(np.uint8)
    patch = Image.fromarray(arr, 'RGB').convert('RGBA')
    img.paste(patch, (x0, y0))


def make_train():
    W, H = 240, 168
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rng = random.Random(3)
    # cabine traseira (mais alta) - corpo
    rust_fill(im, (150, 24, 214, 60), 11)
    d = ImageDraw.Draw(im)
    # telhado pontudo quebrado da cabine
    d.polygon([(144, 26), (182, 6), (220, 26), (214, 30), (182, 13), (150, 30)], fill=(92, 54, 32))
    d.polygon([(150, 24), (182, 8), (190, 12), (160, 28)], fill=(132, 74, 40))
    for x in range(156, 214, 9):
        d.line((x, 26 - (x - 150) // 4 if x < 182 else 26 - (214 - x) // 4, x + 4, 33), fill=(64, 40, 26), width=2)
    d.polygon([(186, 10), (204, 18), (196, 22)], fill=(40, 28, 22))  # buraco no telhado
    # maquinario em cima
    d.rectangle((172, 0, 184, 12), fill=(84, 52, 34)); d.rectangle((174, 0, 182, 3), fill=(120, 72, 40))
    d.line((184, 4, 200, 1), fill=(84, 52, 34), width=2)
    # corpo principal
    rust_fill(im, (14, 50, 226, 128), 21)
    d = ImageDraw.Draw(im)
    # topo (teto) visto de cima, com vigas expostas
    d.polygon([(14, 50), (226, 50), (222, 38), (18, 38)], fill=(42, 30, 24))
    for x in range(22, 222, 12):
        d.line((x, 38, x - 3, 50), fill=(118, 72, 40), width=2)
    for x0, x1 in ((30, 70), (96, 118), (200, 222)):
        d.polygon([(x0, 50), (x1, 50), (x1 + 2, 39), (x0 + 3, 39)], fill=(138, 78, 40))
    d.line((14, 50, 226, 50), fill=(70, 42, 26), width=2)
    # costuras verticais e rebites
    for x in range(14, 226, 26):
        d.line((x, 52, x, 126), fill=(84, 46, 26))
        for y in range(56, 126, 9):
            d.point((x + 2, y), fill=(206, 136, 80))
    d.rectangle((14, 52, 226, 57), fill=(96, 54, 30))
    d.rectangle((14, 118, 226, 128), fill=(84, 48, 28))
    # janelas quebradas
    for (x0, y0, x1, y1) in ((30, 64, 56, 92), (66, 64, 92, 92), (166, 64, 192, 92)):
        d.rectangle((x0, y0, x1, y1), fill=(34, 26, 22))
        d.rectangle((x0, y0, x1, y0 + 2), fill=(60, 40, 28))
        d.polygon([(x0, y1), (x0 + 6, y1 - 7), (x0 + 11, y1)], fill=(120, 68, 36))
        d.line((x0 + 3, y0 + 4, x1 - 5, y1 - 6), fill=(70, 48, 34))
    # porta
    d.rectangle((116, 60, 146, 124), fill=(110, 60, 32)); d.rectangle((116, 60, 146, 124), outline=(70, 40, 24))
    d.rectangle((122, 66, 140, 86), fill=(34, 26, 22))
    d.rectangle((123, 92, 139, 118), outline=(84, 46, 28))
    # buracos de ferrugem
    for _ in range(9):
        x = rng.randint(20, 220); y = rng.randint(96, 116)
        d.ellipse((x, y, x + rng.randint(3, 7), y + rng.randint(2, 5)), fill=(40, 28, 22))
    # musgo e trepadeiras
    MOSS = [(78, 112, 46), (98, 136, 58), (62, 92, 40)]
    for _ in range(70):
        x = rng.randint(14, 224); y = rng.choice([rng.randint(36, 46), rng.randint(110, 128)])
        d.ellipse((x, y, x + rng.randint(2, 5), y + rng.randint(2, 4)), fill=rng.choice(MOSS))
    for _ in range(8):
        x = rng.randint(20, 220); y = 48; L = rng.randint(10, 30)
        for k in range(L):
            d.point((x + (k // 5) % 2, y + k), fill=rng.choice(MOSS))
    # chassi e rodas
    d.rectangle((10, 126, 230, 134), fill=(58, 38, 26)); d.line((10, 126, 230, 126), fill=(110, 68, 40))
    d.rectangle((24, 134, 216, 144), fill=(40, 28, 20))
    for cx in (42, 74, 166, 198):
        d.ellipse((cx - 13, 128, cx + 13, 154), fill=(46, 32, 24))
        d.ellipse((cx - 10, 131, cx + 10, 151), fill=(96, 56, 32))
        d.ellipse((cx - 4, 137, cx + 4, 145), fill=(56, 36, 24))
        for k in range(6):
            a = k / 6 * np.pi * 2
            d.line((cx, 141, cx + np.cos(a) * 9, 141 + np.sin(a) * 9), fill=(70, 44, 28))
        d.arc((cx - 13, 128, cx + 13, 154), 200, 320, fill=(150, 90, 50))
    d.rectangle((52, 136, 64, 140), fill=(80, 50, 30)); d.rectangle((176, 136, 188, 140), fill=(80, 50, 30))
    im = outline(im, C(30, 20, 16))
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((6, 144, 234, 162), fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    shadow.alpha_composite(im)
    im = shadow
    sh = Image.new('RGBA', (W * 3, H * 4), (0, 0, 0, 0))
    for r in range(4):
        for c in range(3):
            sh.alpha_composite(im, (c * W, r * H))
    sh.save(PROJ + '/img/characters/!$TremVelho.png')
    preview(im, 'trem.png', 3)


# ---------------------------------------------------------------- Trilhos (folha D)
def make_rails():
    sheetD = Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    for t in range(2):
        tile = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(tile)
        rng = random.Random(10 + t)
        for sx in (3, 19, 35):
            d.rectangle((sx, 9, sx + 9, 40), fill=(98, 68, 44))
            d.line((sx, 9, sx + 9, 9), fill=(126, 92, 62))
            d.line((sx, 40, sx + 9, 40), fill=(64, 42, 28))
            d.line((sx + 9, 10, sx + 9, 40), fill=(72, 48, 32))
            for _ in range(6):
                d.point((sx + rng.randint(1, 8), rng.randint(11, 38)), fill=(80, 56, 36))
        for ry in (13, 31):
            d.rectangle((0, ry, 47, ry + 3), fill=(110, 94, 84))
            d.line((0, ry, 47, ry), fill=(156, 142, 130))
            d.line((0, ry + 4, 47, ry + 4), fill=(52, 42, 36))
            for _ in range(10):
                d.point((rng.randint(0, 47), ry + rng.randint(1, 3)), fill=(150, 84, 48))
        if t == 1:
            for _ in range(10):
                x = rng.randint(0, 46); y = rng.randint(6, 44)
                for k in range(rng.randint(3, 6)):
                    d.point((x + rng.randint(-1, 1), y - k), fill=rng.choice([(86, 140, 52), (110, 160, 66), (70, 118, 44)]))
        sheetD.alpha_composite(tile, (t * 48, 0))
    sheetD.save(PROJ + '/img/tilesets/Trilhos.png')
    preview(sheetD.crop((0, 0, 96, 48)), 'trilhos.png', 4, bg=(122, 170, 70, 255))


# ---------------------------------------------------------------- Neblina
def make_fog():
    n = value_noise(512, 512, 4, 5, 99)
    a = np.clip((n - 0.35) / 0.4, 0, 1) ** 1.3 * 200
    img = np.zeros((512, 512, 4), dtype=np.uint8)
    img[..., 0] = 236; img[..., 1] = 240; img[..., 2] = 246; img[..., 3] = a.astype(np.uint8)
    Image.fromarray(img, 'RGBA').filter(ImageFilter.GaussianBlur(2)).save(PROJ + '/img/pictures/Neblina.png')


# ---------------------------------------------------------------- Foto: rosto, foto e titulo
def make_photo_assets():
    ph = Image.open(SRC).convert('RGB')
    W, H = ph.size
    # rosto (face) 144x144 na posicao 0 de uma folha 576x288
    face = ph.crop((640, 728, 868, 956)).resize((144, 144), Image.LANCZOS)
    fs = Image.new('RGBA', (576, 288), (0, 0, 0, 0))
    fs.paste(face, (0, 0))
    fs.save(PROJ + '/img/faces/Baratelli.png')
    face.resize((288, 288), Image.LANCZOS).save(PREV + 'face.png')
    # foto em moldura (para mostrar no jogo)
    h = 600; w = round(W * h / H)
    small = ph.resize((w, h), Image.LANCZOS)
    pol = Image.new('RGBA', (w + 24, h + 24), (250, 248, 242, 255))
    pol.paste(small, (12, 12))
    pol.save(PROJ + '/img/pictures/Foto_Baratelli.png')
    # tela de titulo 816x624
    bgw = 816; bgh = round(H * bgw / W)
    bg = ph.resize((bgw, bgh), Image.LANCZOS)
    top = int(bgh * 0.30)
    bg = bg.crop((0, top, 816, top + 624)).filter(ImageFilter.GaussianBlur(9))
    bg = Image.blend(bg, Image.new('RGB', bg.size, (232, 236, 240)), 0.35).convert('RGBA')
    fh = 560; fw = round(W * fh / H)
    fg = ph.resize((fw, fh), Image.LANCZOS)
    frame = Image.new('RGBA', (fw + 20, fh + 20), (250, 248, 242, 255))
    frame.paste(fg, (10, 10))
    shadow = Image.new('RGBA', bg.size, (0, 0, 0, 0))
    fx = (816 - frame.width) // 2; fy = 24
    ImageDraw.Draw(shadow).rectangle((fx + 6, fy + 8, fx + frame.width + 6, fy + frame.height + 8), fill=(0, 0, 0, 110))
    bg.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
    bg.alpha_composite(frame, (fx, fy))
    bg.convert('RGB').save(PROJ + '/img/titles1/Baratelli.png')
    bg.resize((408, 312)).save(PREV + 'title.png')


if __name__ == '__main__':
    make_baratelli()
    make_sheep()
    make_train()
    make_rails()
    make_fog()
    make_photo_assets()
    print('ok')
