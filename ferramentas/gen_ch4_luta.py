# Capitulo 4: arte do minigame de luta (arena do templo, Pavao-Hipopotamo, penas, onda, sapo e vidente).
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, PROJ

PREV4 = HERE + '/prev4/'
PIC = PROJ + '/img/pictures/'

HIP = C(140, 118, 164); HIP_L = C(176, 156, 198); HIP_D = C(104, 84, 128)
SNOUT = C(198, 168, 196); SNOUT_D = C(160, 128, 162)
FAN = C(36, 122, 112); FAN_L = C(70, 170, 140); FAN_D = C(20, 80, 80)
EYE_GOLD = C(236, 196, 70); EYE_BLUE = C(40, 90, 200); EYE_NAVY = C(16, 26, 70)
CREST = C(40, 140, 200); OUTP = C(40, 26, 50)
WHITE = C(255, 255, 255); EYE_D = C(34, 28, 40)


def eyespot(d, x, y, s):
    d.ellipse((x - s, y - s * 1.3, x + s, y + s * 1.3), fill=EYE_GOLD)
    d.ellipse((x - s * 0.7, y - s * 0.9, x + s * 0.7, y + s * 0.9), fill=EYE_BLUE)
    d.ellipse((x - s * 0.35, y - s * 0.45, x + s * 0.35, y + s * 0.45), fill=EYE_NAVY)


def fan_aberto(d, cx, cy, r, a0, a1, brilho=False):
    d.pieslice((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=FAN)
    d.pieslice((cx - r * 0.72, cy - r * 0.72, cx + r * 0.72, cy + r * 0.72), a0, a1, fill=FAN_L)
    n = 15
    for k in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * k / n)
        d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)), fill=FAN_D)
    for (rr, cnt, s) in ((0.86, 9, 5), (0.62, 7, 4), (0.4, 5, 3)):
        for k in range(cnt):
            a = math.radians(a0 + (a1 - a0) * (k + 0.5) / cnt)
            x, y = cx + r * rr * math.cos(a), cy + r * rr * math.sin(a)
            if brilho:
                d.ellipse((x - s - 2, y - s * 1.3 - 2, x + s + 2, y + s * 1.3 + 2), fill=C(255, 250, 200))
            eyespot(d, x, y, s)


def cauda_fechada(d, x0, y0):
    d.polygon([(x0, y0 - 6), (x0 + 30, y0 - 14), (x0 + 38, y0 - 4), (x0 + 33, y0 + 14), (x0, y0 + 10)], fill=FAN)
    d.line((x0, y0 + 2, x0 + 36, y0), fill=FAN_D)
    for k in range(3):
        eyespot(d, x0 + 12 + k * 9, y0 - 2 + (k % 2) * 4, 3)


def crista(d, x, y):
    for (dx, dy) in ((-8, -20), (0, -24), (8, -20)):
        d.line((x, y, x + dx, y + dy), fill=C(60, 70, 110))
        d.ellipse((x + dx - 3, y + dy - 4, x + dx + 3, y + dy + 2), fill=CREST)


def cabeca(d, hx, hy, olhos='normal', boca='fechada'):
    d.ellipse((hx - 26, hy - 22, hx + 24, hy + 22), fill=HIP)
    d.ellipse((hx - 38, hy - 8, hx + 4, hy + 26), fill=SNOUT)
    d.ellipse((hx - 34, hy - 2, hx - 28, hy + 4), fill=SNOUT_D)
    if boca == 'aberta':
        d.chord((hx - 36, hy + 6, hx - 2, hy + 26), 0, 180, fill=C(120, 40, 60))
        d.rectangle((hx - 30, hy + 15, hx - 8, hy + 17), fill=WHITE)
    elif boca == 'lingua':
        d.arc((hx - 34, hy + 8, hx - 6, hy + 22), 20, 160, fill=SNOUT_D, width=2)
        d.ellipse((hx - 26, hy + 16, hx - 16, hy + 28), fill=C(240, 110, 140))
    else:
        d.arc((hx - 34, hy + 6, hx - 6, hy + 22), 30, 150, fill=SNOUT_D, width=2)
    ex, ey = hx - 4, hy - 8
    if olhos == 'x':
        d.line((ex - 4, ey - 4, ex + 4, ey + 4), fill=EYE_D, width=2); d.line((ex - 4, ey + 4, ex + 4, ey - 4), fill=EYE_D, width=2)
    elif olhos == 'espiral':
        d.ellipse((ex - 5, ey - 5, ex + 5, ey + 5), fill=WHITE)
        d.arc((ex - 4, ey - 4, ex + 4, ey + 4), 0, 270, fill=EYE_D); d.arc((ex - 2, ey - 2, ex + 2, ey + 2), 90, 360, fill=EYE_D)
    elif olhos == 'bravo':
        d.ellipse((ex - 5, ey - 4, ex + 5, ey + 5), fill=WHITE); d.ellipse((ex - 3, ey - 2, ex + 2, ey + 4), fill=C(200, 30, 50))
        d.line((ex - 8, ey - 8, ex + 6, ey - 3), fill=EYE_D, width=2)
    else:
        d.ellipse((ex - 5, ey - 5, ex + 5, ey + 5), fill=WHITE); d.ellipse((ex - 3, ey - 3, ex + 2, ey + 4), fill=EYE_D)
        for k in (-3, 0, 3):
            d.line((ex + k, ey - 5, ex + k * 1.5, ey - 10), fill=EYE_D)
    d.ellipse((hx + 6, hy - 22, hx + 16, hy - 12), fill=HIP_D)
    d.ellipse((hx - 30, hy + 6, hx - 22, hy + 12), fill=C(240, 150, 190))
    crista(d, hx + 2, hy - 20)


def pernas(d, fases):
    for (x, dx, cor) in fases:
        d.rectangle((x + dx, 98, x + dx + 12, 124), fill=cor)
        for t in range(3):
            d.point((x + dx + 2 + t * 4, 124), fill=C(240, 230, 240))


def pavao_frame(pose):
    W, H = 160, 130
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    olhos, boca = 'normal', 'fechada'
    hx, hy = 40, 64
    if pose in ('leque',):
        fan_aberto(d, 100, 74, 59, 195, 345, brilho=True)
        olhos, boca = 'bravo', 'aberta'
    elif pose == 'ko':
        pass
    else:
        cauda_fechada(d, 118, 72)
    if pose == 'ko':
        d.ellipse((30, 76, 140, 124), fill=HIP)
        d.ellipse((50, 92, 130, 124), fill=HIP_L)
        for x in (52, 72, 100, 120):
            d.rectangle((x, 56, x + 10, 82), fill=HIP_D)
        cabeca(d, 34, 96, 'x', 'lingua')
        for (x, y) in ((140, 116), (150, 108), (10, 120)):
            d.line((x, y, x + 10, y - 6), fill=FAN_D, width=2); eyespot(d, x + 10, y - 6, 3)
        return im
    walk = {'andar1': 4, 'andar2': -4}.get(pose, 0)
    if pose == 'investida':
        pernas(d, [(50, -8, HIP_D), (70, 8, HIP_D), (102, -10, HIP_D), (120, 10, HIP_D)])
    elif pose == 'preparo':
        pernas(d, [(50, 0, HIP_D), (74, 10, HIP_D), (104, 0, HIP_D), (120, 0, HIP_D)])
    else:
        pernas(d, [(50, walk, HIP_D), (70, -walk, HIP_D), (104, -walk, HIP_D), (120, walk, HIP_D)])
    d.ellipse((40, 50, 140, 112), fill=HIP)
    d.ellipse((56, 76, 132, 112), fill=HIP_L)
    if pose == 'investida':
        pernas(d, [(56, -10, HIP), (110, 8, HIP)])
    else:
        pernas(d, [(56, -walk, HIP), (110, walk, HIP)])
    if pose == 'preparo':
        hx, hy = 34, 74; olhos = 'bravo'
        for (x, y, r) in ((6, 74, 4), (0, 66, 3)):
            d.ellipse((x - r, y - r, x + r, y + r), fill=C(240, 240, 250))
    elif pose == 'investida':
        hx, hy = 32, 76; olhos = 'bravo'; boca = 'aberta'
    elif pose == 'dor':
        olhos = 'x'; boca = 'aberta'
    elif pose == 'tonto':
        olhos = 'espiral'; boca = 'lingua'
    elif pose == 'grito':
        boca = 'aberta'; olhos = 'bravo'
    cabeca(d, hx, hy, olhos, boca)
    if pose == 'tonto':
        for k in range(3):
            a = math.radians(k * 120)
            x, y = hx + 2 + 16 * math.cos(a), hy - 40 + 6 * math.sin(a)
            d.polygon([(x, y - 5), (x + 1.5, y - 1.5), (x + 5, y), (x + 1.5, y + 1.5), (x, y + 5), (x - 1.5, y + 1.5), (x - 5, y), (x - 1.5, y - 1.5)], fill=C(255, 230, 80))
    if pose == 'dor':
        for (x, y) in ((70, 40), (60, 46)):
            d.ellipse((x - 2, y - 3, x + 2, y + 3), fill=C(150, 200, 255))
    if pose == 'grito':
        for k in range(3):
            d.arc((hx - 70 - k * 12, hy - 20 - k * 10, hx - 30 + k * 4, hy + 30 + k * 10), 120, 240, fill=WHITE, width=2)
    return im


def pisada(levantado):
    base = pavao_frame('parado')
    if levantado:
        return base.rotate(-22, resample=Image.NEAREST, center=(124, 120), translate=(0, -6))
    im = base.copy(); d = ImageDraw.Draw(im)
    for (x0, x1) in ((20, 50), (110, 150)):
        for k in range(3):
            d.line((x0 + k * 10, 126, x0 + k * 10 - 8, 112), fill=C(250, 240, 210), width=2)
    return im


def investida_poeira(im):
    d = ImageDraw.Draw(im)
    for (x, y, r) in ((150, 112, 9), (140, 100, 6), (156, 98, 5)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=C(230, 210, 170))
    for k in range(4):
        y = 60 + k * 12
        d.line((150, y, 160, y), fill=WHITE)
    return im


def make_pavao_sheet():
    poses = ['parado', 'parado2', 'andar1', 'andar2', 'preparo', 'investida', 'leque', 'pisar_cima', 'pisar_baixo',
             'dor', 'tonto', 'ko']
    frames = []
    for p in poses:
        if p == 'parado2':
            f = pavao_frame('parado').resize((160, 128), Image.NEAREST)
            g = Image.new('RGBA', (160, 130), (0, 0, 0, 0)); g.alpha_composite(f, (0, 2)); f = g
        elif p == 'pisar_cima':
            f = pisada(True)
        elif p == 'pisar_baixo':
            f = pisada(False)
        else:
            f = pavao_frame(p)
            if p == 'investida':
                f = investida_poeira(f)
        frames.append(outline(f, OUTP).resize((320, 260), Image.NEAREST))
    sheet = Image.new('RGBA', (320 * 4, 260 * 3), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.alpha_composite(f, ((i % 4) * 320, (i // 4) * 260))
    sheet.save(PIC + 'Luta_Pavao.png')
    pv = Image.new('RGBA', sheet.size, (70, 90, 70, 255)); pv.alpha_composite(sheet)
    pv.resize((sheet.width // 2, sheet.height // 2)).save(PREV4 + 'luta_pavao.png')


# ---------------------------------------------------------------- arena
def make_arena():
    W, H = 408, 312
    arr = np.zeros((H, W, 4), np.uint8)
    for y in range(H):
        t = y / 200
        if y < 200:
            c = np.array([60, 30, 90]) * (1 - t) + np.array([250, 150, 110]) * t
        else:
            c = np.array([0, 0, 0])
        arr[y, :, :3] = c; arr[y, :, 3] = 255
    im = Image.fromarray(arr, 'RGBA'); d = ImageDraw.Draw(im)
    rng = random.Random(4)
    for _ in range(40):
        x, y = rng.randint(0, W), rng.randint(0, 80)
        d.point((x, y), fill=C(255, 250, 220))
    d.ellipse((300, 30, 330, 60), fill=C(255, 246, 214))
    for k in range(20):
        x = k * 22 + rng.randint(-6, 6)
        d.ellipse((x - 18, 120 + rng.randint(-10, 10), x + 18, 190), fill=C(30, 70, 50))
    d.rectangle((0, 160, W, 200), fill=C(30, 70, 50))
    pedra, pedra_l, pedra_d = C(214, 176, 100), C(240, 210, 140), C(160, 124, 64)
    for k in range(5):
        x0 = 110 + k * 12; x1 = 298 - k * 12; y1 = 200 - k * 24; y0 = y1 - 24
        d.rectangle((x0, y0, x1, y1), fill=pedra)
        d.line((x0, y0, x1, y0), fill=pedra_l); d.line((x0, y1, x1, y1), fill=pedra_d)
        for x in range(x0 + 6, x1, 12):
            d.line((x, y0 + 4, x, y1 - 4), fill=pedra_d)
    d.rectangle((174, 50, 234, 80), fill=pedra); d.rectangle((174, 50, 234, 52), fill=pedra_l)
    d.rectangle((194, 58, 214, 80), fill=C(30, 20, 18))
    d.polygon([(186, 200), (222, 200), (214, 80), (194, 80)], fill=C(196, 160, 90))
    for y in range(84, 200, 6):
        w = 4 + (y - 80) * 0.12
        d.line((204 - w * 2, y, 204 + w * 2, y), fill=pedra_d)
    for (x, flip) in ((176, 1), (232, -1)):
        d.ellipse((x - 10, 184, x + 10, 202), fill=C(60, 150, 110))
        d.polygon([(x, 186), (x - 14 * flip, 192), (x, 198)], fill=C(170, 40, 50))
        d.ellipse((x - 4, 188, x + 2, 194), fill=C(255, 220, 90))
    for x in (90, 318):
        d.rectangle((x - 3, 150, x + 3, 200), fill=C(90, 60, 40))
        d.polygon([(x - 8, 150), (x, 128), (x + 8, 150)], fill=C(255, 150, 40))
        d.polygon([(x - 4, 150), (x, 136), (x + 4, 150)], fill=C(255, 230, 120))
    chao, chao_l, chao_d = C(176, 150, 110), C(200, 176, 134), C(130, 104, 70)
    d.rectangle((0, 200, W, H), fill=chao)
    for k in range(9):
        y = 200 + int((k / 8) ** 1.6 * 112)
        d.line((0, y, W, y), fill=chao_d)
    for k in range(-12, 13):
        d.line((204 + k * 10, 200, 204 + k * 46, H), fill=chao_d)
    d.ellipse((134, 240, 274, 300), outline=C(150, 110, 60), width=3)
    d.ellipse((164, 252, 244, 288), outline=C(40, 150, 140), width=2)
    for k in range(12):
        a = math.radians(k * 30)
        d.line((204 + 40 * math.cos(a), 270 + 18 * math.sin(a), 204 + 68 * math.cos(a), 270 + 30 * math.sin(a)), fill=C(150, 110, 60))
    for (x0, flip) in ((0, 1), (W, -1)):
        d.polygon([(x0, 0), (x0 + 50 * flip, 0), (x0 + 40 * flip, 180), (x0 + 30 * flip, 312), (x0, 312)], fill=C(24, 54, 34))
        for k in range(8):
            y = k * 34
            d.ellipse((x0 + (10 if flip > 0 else -60), y, x0 + (60 if flip > 0 else -10), y + 40), fill=C(40, 96, 56))
        for k in range(4):
            yy = 10 + k * 70
            d.line([(x0 + 40 * flip, yy), (x0 + 60 * flip, yy + 30), (x0 + 50 * flip, yy + 60)], fill=C(70, 150, 70), width=2)
    im = im.resize((816, 624), Image.NEAREST)
    im.save(PIC + 'Luta_Arena.png')
    im.resize((408, 312)).save(PREV4 + 'luta_arena.png')


# ---------------------------------------------------------------- projeteis e especiais
def make_pena():
    im = Image.new('RGBA', (32, 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((2, 6, 26, 6), fill=C(230, 220, 190))
    for x in range(6, 24, 3):
        d.line((x, 6, x - 3, 2), fill=FAN_L); d.line((x, 6, x - 3, 10), fill=FAN_L)
    d.ellipse((20, 1, 31, 11), fill=FAN); eyespot(d, 26, 6, 3)
    im = outline(im, OUTP).resize((64, 24), Image.NEAREST)
    im.save(PIC + 'Luta_Pena.png')


def make_onda():
    frames = []
    for f in range(3):
        im = Image.new('RGBA', (44, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        h = [18, 24, 20][f]
        d.polygon([(2, 31), (14, 31 - h), (24, 31 - h * 0.6), (34, 31 - h * 0.9), (42, 31)], fill=C(220, 196, 150))
        d.polygon([(8, 31), (16, 31 - h * 0.6), (30, 31 - h * 0.5), (36, 31)], fill=C(250, 236, 200))
        for k in range(4):
            x = 6 + k * 10 + f * 2
            d.ellipse((x - 2, 31 - h - 4 - k % 2 * 3, x + 2, 31 - h - k % 2 * 3), fill=C(200, 170, 120))
        frames.append(outline(im, C(110, 80, 40)).resize((88, 64), Image.NEAREST))
    sh = Image.new('RGBA', (88 * 3, 64), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sh.alpha_composite(f, (i * 88, 0))
    sh.save(PIC + 'Luta_Onda.png')


def make_sapo():
    W = 110
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    frg, frg_l, frg_d, belly = C(94, 168, 76), C(140, 204, 108), C(60, 118, 48), C(214, 228, 150)
    cx = 55
    for sgn in (-1, 1):
        sx, ex = cx + sgn * 26, cx + sgn * 44
        d.line((sx, 56, ex, 56), fill=frg, width=12)
        d.ellipse(((sx + ex) / 2 - 9, 44, (sx + ex) / 2 + 9, 58), fill=frg_l)
        d.line((ex, 58, ex, 30), fill=frg, width=10)
        d.ellipse((ex - 8, 18, ex + 8, 34), fill=frg)
    d.ellipse((cx - 30, 44, cx + 30, 104), fill=frg)
    d.ellipse((cx - 20, 56, cx + 20, 100), fill=belly)
    for k in range(3):
        d.line((cx - 12, 66 + k * 10, cx + 12, 66 + k * 10), fill=C(190, 200, 120))
    d.ellipse((cx - 24, 22, cx + 24, 60), fill=frg)
    for ex in (cx - 14, cx + 14):
        d.ellipse((ex - 10, 12, ex + 10, 32), fill=frg)
        d.ellipse((ex - 7, 15, ex + 7, 29), fill=WHITE)
        d.ellipse((ex - 3, 18, ex + 3, 27), fill=EYE_D)
        d.line((ex - 8, 13, ex + 6, 17 if ex < cx else 11), fill=C(30, 40, 20), width=2)
    d.arc((cx - 16, 36, cx + 16, 52), 20, 160, fill=frg_d, width=2)
    d.polygon([(cx - 26, 46), (cx - 16, 46), (cx - 18, 80), (cx - 28, 80)], fill=C(120, 70, 40))
    d.polygon([(cx + 26, 46), (cx + 16, 46), (cx + 18, 80), (cx + 28, 80)], fill=C(120, 70, 40))
    im = outline(im, C(24, 50, 20)).resize((W * 2, W * 2), Image.NEAREST)
    im.save(PIC + 'Luta_Sapo.png')


def make_vidente():
    W = 80
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    old, old_d, shawl = C(236, 206, 182), C(206, 170, 146), C(108, 58, 140)
    d.polygon([(6, 80), (14, 62), (40, 56), (66, 62), (74, 80)], fill=shawl)
    d.ellipse((18, 10, 62, 62), fill=old)
    d.ellipse((24, 14, 40, 30), fill=WHITE)
    for ex in (32, 48):
        d.ellipse((ex - 5, 34, ex + 5, 42), fill=WHITE); d.ellipse((ex - 3, 34, ex + 3, 42), fill=C(58, 116, 210))
    d.arc((32, 46, 48, 54), 20, 160, fill=C(150, 70, 70), width=2)
    for y in (24, 28):
        d.arc((28, y - 3, 52, y + 3), 200, 340, fill=old_d)
    im = outline(im, C(40, 24, 40))
    g = Image.new('RGBA', (W, W), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((4, 0, 76, 70), fill=(255, 255, 220, 140))
    g = g.filter(ImageFilter.GaussianBlur(8)); g.alpha_composite(im)
    g.resize((W * 2, W * 2), Image.NEAREST).save(PIC + 'Luta_Vidente.png')


def main():
    make_pavao_sheet()
    make_arena()
    make_pena()
    make_onda()
    make_sapo()
    make_vidente()
    print('ok')


if __name__ == '__main__':
    main()
