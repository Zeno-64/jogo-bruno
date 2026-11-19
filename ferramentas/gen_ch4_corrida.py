# Capitulo 4: cenarios (fundo + chao, emendaveis na horizontal) e obstaculos da corrida Umamusume.
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_assets import C, outline, PROJ

PREV4 = HERE + '/prev4/'
PIC = PROJ + '/img/pictures/'
FW, FH = 408, 210      # fundo (meia resolucao)
CW, CH = 408, 130      # chao


def grad(w, h, top, bottom):
    t = np.linspace(0, 1, h)[:, None]
    arr = np.zeros((h, w, 4), np.uint8)
    for i in range(3):
        arr[..., i] = np.repeat(top[i] * (1 - t) + bottom[i] * t, w, axis=1).astype(np.uint8)
    arr[..., 3] = 255
    return Image.fromarray(arr, 'RGBA')


def salvar(im, nome):
    im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    im.save(PIC + nome + '.png')
    return im


def tocha(d, x, y):
    d.rectangle((x - 2, y, x + 2, y + 26), fill=C(90, 60, 40))
    d.polygon([(x - 6, y), (x, y - 16), (x + 6, y)], fill=C(255, 150, 40))
    d.polygon([(x - 3, y), (x, y - 9), (x + 3, y)], fill=C(255, 230, 120))


def sol(d, cx, cy, r):
    for k in range(12):
        a = math.radians(k * 30)
        d.polygon([(cx + r * 0.7 * math.cos(a - 0.2), cy + r * 0.7 * math.sin(a - 0.2)), (cx + r * 1.3 * math.cos(a), cy + r * 1.3 * math.sin(a)),
                   (cx + r * 0.7 * math.cos(a + 0.2), cy + r * 0.7 * math.sin(a + 0.2))], fill=C(200, 150, 40))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=C(240, 196, 70))
    d.ellipse((cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6), fill=C(255, 230, 140))


def busto_peq(d, x, y, cor):
    d.rectangle((x - 5, y + 8, x + 5, y + 22), fill=C(200, 192, 176))
    d.ellipse((x - 6, y - 4, x + 6, y + 10), fill=C(214, 206, 190))
    d.ellipse((x - 8, y - 7, x + 8, y + 5), fill=cor)


def uma_silhueta(d, x, y, cor, s=1.0):
    d.ellipse((x - 4 * s, y - 20 * s, x + 4 * s, y - 12 * s), fill=cor)
    d.polygon([(x - 4 * s, y - 20 * s), (x - 3 * s, y - 25 * s), (x - 1 * s, y - 20 * s)], fill=cor)
    d.polygon([(x + 1 * s, y - 20 * s), (x + 3 * s, y - 25 * s), (x + 4 * s, y - 20 * s)], fill=cor)
    d.line((x, y - 12 * s, x + 3 * s, y - 2 * s), fill=cor, width=max(1, int(3 * s)))
    d.line((x + 3 * s, y - 2 * s, x - 5 * s, y + 6 * s), fill=cor, width=max(1, int(2 * s)))
    d.line((x + 3 * s, y - 2 * s, x + 10 * s, y + 4 * s), fill=cor, width=max(1, int(2 * s)))
    d.line((x + 1 * s, y - 9 * s, x + 9 * s, y - 13 * s), fill=cor, width=max(1, int(2 * s)))
    d.line((x + 1 * s, y - 9 * s, x - 7 * s, y - 6 * s), fill=cor, width=max(1, int(2 * s)))
    d.polygon([(x + 2 * s, y - 4 * s), (x + 12 * s, y - 8 * s), (x + 9 * s, y - 2 * s)], fill=cor)


# ---------------------------------------------------------------- fundos
def fundo_templo3():
    im = grad(FW, FH, (110, 60, 20), (200, 140, 60)); d = ImageDraw.Draw(im)
    for x in range(0, FW, 34):
        d.rectangle((x, 0, x + 30, FH), fill=C(214, 170, 80))
        d.line((x, 0, x, FH), fill=C(150, 104, 40))
        for y in range(10, FH, 26):
            d.rectangle((x + 6, y, x + 24, y + 14), outline=C(170, 120, 50))
    for x in range(0, FW, 136):
        d.rectangle((x + 40, 0, x + 64, 150), fill=C(190, 40, 110))
        d.polygon([(x + 40, 150), (x + 52, 162), (x + 64, 150)], fill=C(190, 40, 110))
        sol(d, x + 100, 60, 22)
        tocha(d, x + 20, 100)
    d.rectangle((0, 170, FW, FH), fill=C(120, 80, 30))
    return im


def fundo_templo2():
    im = grad(FW, FH, (20, 70, 70), (40, 130, 120)); d = ImageDraw.Draw(im)
    for x in range(0, FW, 51):
        d.rectangle((x, 0, x + 48, FH), fill=C(40, 140, 130))
        d.rectangle((x + 4, 30, x + 44, 90), fill=C(30, 110, 104))
        uma_silhueta(d, x + 22, 74, C(240, 200, 80), 1.3)
        d.rectangle((x + 4, 30, x + 44, 90), outline=C(240, 200, 80))
    for x in range(20, FW, 102):
        d.rectangle((x - 10, 110, x + 10, 170), fill=C(196, 190, 176))
        uma_silhueta(d, x, 106, C(214, 208, 194), 1.6)
    d.rectangle((0, 170, FW, FH), fill=C(60, 90, 80))
    for x in range(0, FW, 8):
        d.line((x, 172, x + 4, 172), fill=C(250, 250, 240))
    return im


def fundo_templo1():
    im = grad(FW, FH, (60, 50, 44), (110, 96, 80)); d = ImageDraw.Draw(im)
    for y in range(0, FH, 16):
        off = 0 if (y // 16) % 2 else 12
        for x in range(-off, FW, 24):
            d.rectangle((x, y, x + 22, y + 14), fill=C(150, 138, 120), outline=C(110, 100, 86))
    cores = [C(250, 214, 96), C(214, 84, 40), C(70, 124, 232), C(46, 38, 56)]
    for k, x in enumerate(range(16, FW, 50)):
        d.rectangle((x - 16, 96, x + 16, 102), fill=C(120, 84, 50))
        busto_peq(d, x, 70, cores[k % 4])
        d.rectangle((x - 12, 40, x + 12, 48), fill=C(236, 196, 70))
    for x in range(0, FW, 102):
        tocha(d, x + 40, 120)
    d.rectangle((0, 170, FW, FH), fill=C(90, 80, 70))
    return im


def fundo_escadaria():
    im = grad(FW, FH, (250, 150, 110), (250, 210, 160)); d = ImageDraw.Draw(im)
    d.ellipse((300, 20, 340, 60), fill=C(255, 240, 200))
    for k in range(5):
        x0 = 120 + k * 14; x1 = 300 - k * 14; y1 = 170 - k * 22; y0 = y1 - 22
        d.rectangle((x0, y0, x1, y1), fill=C(214, 176, 100)); d.line((x0, y0, x1, y0), fill=C(240, 210, 140))
    d.rectangle((186, 40, 234, 60), fill=C(214, 176, 100)); d.rectangle((200, 44, 220, 60), fill=C(30, 20, 18))
    rng = random.Random(5)
    for k in range(14):
        x = k * 32 + rng.randint(-6, 6)
        if 110 < x < 310:
            continue
        d.ellipse((x - 26, 90 + rng.randint(-10, 10), x + 26, 190), fill=C(40, 100, 60))
        d.rectangle((x - 3, 150, x + 3, 190), fill=C(90, 60, 40))
    d.rectangle((0, 170, FW, FH), fill=C(176, 150, 110))
    return im


def fundo_floresta(claro=False):
    topo, base = ((150, 220, 255), (220, 250, 220)) if claro else ((20, 60, 40), (50, 110, 70))
    im = grad(FW, FH, topo, base); d = ImageDraw.Draw(im)
    rng = random.Random(9 if claro else 8)
    camadas = [(C(70, 130, 90) if not claro else C(150, 200, 150), 0.7), (C(40, 100, 60) if not claro else C(100, 170, 110), 1.0)]
    for cor, esc in camadas:
        for k in range(16):
            x = k * 28 + rng.randint(-8, 8)
            if claro and 160 < x < 260:
                continue
            h = rng.randint(60, 140) * esc
            d.rectangle((x - 3, FH - h * 0.3 - 30, x + 3, FH), fill=C(70, 50, 34))
            d.ellipse((x - 22 * esc, FH - h - 30, x + 22 * esc, FH - h * 0.3 - 20), fill=cor)
    if claro:
        luz = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(luz)
        ld.ellipse((140, 40, 280, 200), fill=(255, 255, 230, 140))
        im.alpha_composite(luz)
        d = ImageDraw.Draw(im)
    else:
        for k in range(10):
            x = rng.randint(0, FW)
            d.line([(x, 0), (x + rng.randint(-6, 6), 40), (x + rng.randint(-4, 4), 70)], fill=C(80, 160, 80), width=2)
    d.rectangle((0, 170, FW, FH), fill=C(60, 110, 50) if not claro else C(110, 170, 90))
    return im


# ---------------------------------------------------------------- chaos (3 raias)
def chao(base, linha, detalhe=None, seed=0):
    im = Image.new('RGBA', (CW, CH), base + (255,)); d = ImageDraw.Draw(im)
    rng = random.Random(seed)
    for _ in range(140):
        x, y = rng.randint(0, CW - 1), rng.randint(0, CH - 1)
        k = rng.choice([-14, -8, 8, 12])
        d.point((x, y), fill=tuple(max(0, min(255, c + k)) for c in base) + (255,))
    for y in (40, 68, 96):
        for x in range(0, CW, 12):
            d.line((x, y, x + 6, y), fill=linha + (255,))
    if detalhe:
        detalhe(d, rng)
    return im


def det_tapete(d, rng):
    cores = [(232, 52, 60), (250, 140, 40), (250, 214, 50), (84, 190, 92), (62, 132, 222), (150, 92, 206)]
    for k, c in enumerate(cores):
        d.line((0, 6 + k * 2, CW, 6 + k * 2), fill=c + (255,))


def det_pista(d, rng):
    d.rectangle((0, 0, CW, 6), fill=(250, 250, 240, 255))
    for x in range(0, CW, 40):
        d.rectangle((x, 0, x + 3, 6), fill=(60, 60, 60, 255))


def det_pedras(d, rng):
    for _ in range(18):
        x, y = rng.randint(0, CW), rng.randint(0, CH)
        d.rectangle((x, y, x + rng.randint(10, 26), y + rng.randint(6, 12)), outline=(110, 98, 84, 255))


def det_grama(d, rng):
    for _ in range(90):
        x, y = rng.randint(0, CW), rng.randint(0, CH)
        d.line((x, y, x + rng.randint(-2, 2), y - 4), fill=(70, 140, 60, 255))
    for _ in range(12):
        x, y = rng.randint(0, CW), rng.randint(0, CH)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=rng.choice([(255, 120, 160, 255), (255, 230, 90, 255)]))


SECOES = {
    'templo3': (fundo_templo3, lambda: chao((200, 160, 70), (255, 236, 160), det_tapete, 1)),
    'templo2': (fundo_templo2, lambda: chao((150, 104, 64), (250, 250, 240), det_pista, 2)),
    'templo1': (fundo_templo1, lambda: chao((140, 130, 116), (220, 214, 200), det_pedras, 3)),
    'escadaria': (fundo_escadaria, lambda: chao((176, 150, 110), (230, 214, 180), det_pedras, 4)),
    'floresta': (lambda: fundo_floresta(False), lambda: chao((110, 84, 54), (170, 140, 100), det_grama, 5)),
    'saida': (lambda: fundo_floresta(True), lambda: chao((130, 104, 66), (200, 176, 130), det_grama, 6)),
}


# ---------------------------------------------------------------- obstaculos (48x48 -> 96x96)
STONE = C(206, 198, 180); STONE_D = C(150, 140, 122)


def ob_coluna():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 28, 44, 44), 6, fill=STONE)
    for x in range(10, 44, 8):
        d.line((x, 29, x, 43), fill=STONE_D)
    d.ellipse((36, 28, 46, 44), fill=C(226, 220, 204)); d.ellipse((39, 32, 43, 40), fill=STONE_D)
    return outline(im, C(60, 52, 44))


def ob_peruca():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((6, 40, 34, 38), fill=C(140, 96, 56), width=3)
    d.ellipse((30, 28, 44, 42), fill=C(236, 214, 190))
    d.ellipse((28, 24, 46, 38), fill=C(214, 84, 40))
    d.ellipse((2, 36, 14, 44), fill=C(96, 62, 34))
    return outline(im, C(60, 40, 30))


def ob_busto():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 26, 34, 44), fill=STONE)
    d.ellipse((16, 8, 32, 28), fill=STONE)
    d.ellipse((13, 4, 35, 20), fill=C(70, 124, 232))
    d.line((20, 18, 22, 18), fill=STONE_D); d.line((26, 18, 28, 18), fill=STONE_D)
    return outline(im, C(60, 52, 44))


def ob_estatua():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((12, 38, 36, 46), fill=STONE_D)
    uma_silhueta(d, 24, 30, STONE, 1.4)
    return outline(im, C(60, 52, 44))


def ob_raiz():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line([(2, 44), (12, 34), (24, 40), (34, 30), (46, 42)], fill=C(110, 76, 44), width=6)
    d.line([(12, 34), (16, 24)], fill=C(110, 76, 44), width=4)
    return outline(im, C(50, 30, 18))


def ob_tronco():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 28, 44, 44), 7, fill=C(140, 96, 56))
    for x in range(8, 40, 7):
        d.line((x, 30, x + 2, 42), fill=C(110, 74, 40))
    d.ellipse((36, 28, 46, 44), fill=C(196, 156, 100)); d.ellipse((39, 32, 43, 40), fill=C(150, 110, 70))
    return outline(im, C(50, 30, 18))


def ob_espinhos():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rng = random.Random(3)
    for k in range(10):
        x = 4 + k * 4
        d.line((x, 46, x + rng.randint(-4, 4), 26 + rng.randint(0, 10)), fill=C(70, 110, 50), width=2)
    for _ in range(14):
        x, y = rng.randint(4, 44), rng.randint(28, 44)
        d.polygon([(x, y), (x + 3, y - 1), (x + 1, y + 2)], fill=C(220, 210, 180))
    return outline(im, C(24, 36, 18))


def ob_lama():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 32, 46, 46), fill=C(96, 70, 44)); d.ellipse((8, 34, 40, 44), fill=C(120, 92, 60))
    d.arc((14, 36, 30, 42), 200, 340, fill=C(156, 124, 84))
    return im


def ob_ferradura():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.arc((12, 12, 36, 40), 200, 520, fill=C(255, 214, 70), width=5)
    for (x, y) in [(15, 30), (33, 30), (14, 21), (34, 21)]:
        d.point((x, y), fill=C(150, 100, 20))
    for (x, y) in [(8, 10), (40, 12), (24, 4)]:
        d.line((x - 2, y, x + 2, y), fill=C(255, 255, 230)); d.line((x, y - 2, x, y + 2), fill=C(255, 255, 230))
    return outline(im, C(120, 80, 20))


def ob_grampo():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(3):
        x = 8 + k * 12
        d.line((x, 44, x + 8, 30), fill=C(60, 50, 70), width=2)
        d.line((x + 3, 44, x + 11, 30), fill=C(60, 50, 70), width=2)
        d.ellipse((x + 6, 27, x + 12, 32), fill=C(190, 60, 120))
    return outline(im, C(30, 20, 30))


def ob_chegada():
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y in range(0, 48, 6):
        for x in range(18, 30, 6):
            d.rectangle((x, y, x + 5, y + 5), fill=C(250, 250, 250) if ((x // 6) + (y // 6)) % 2 else C(30, 30, 30))
    return im


def make_obstaculos():
    fs = [ob_coluna, ob_peruca, ob_busto, ob_estatua, ob_raiz, ob_tronco, ob_espinhos, ob_lama, ob_ferradura, ob_grampo, ob_chegada]
    sh = Image.new('RGBA', (96 * len(fs), 96), (0, 0, 0, 0))
    for i, f in enumerate(fs):
        sh.alpha_composite(f().resize((96, 96), Image.NEAREST), (i * 96, 0))
    sh.save(PIC + 'Corrida_Obj.png')
    pv = Image.new('RGBA', sh.size, (60, 90, 60, 255)); pv.alpha_composite(sh); pv.save(PREV4 + 'corrida_obj.png')


def make_portao():
    im = Image.new('RGBA', (120, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 119, 14), fill=C(60, 140, 90))
    d.rectangle((0, 0, 10, 159), fill=C(200, 200, 210)); d.rectangle((109, 0, 119, 159), fill=C(200, 200, 210))
    for k, y in enumerate((30, 80, 130)):
        d.rectangle((12, y - 18, 107, y + 18), fill=C(240, 240, 248), outline=C(120, 120, 140))
        d.text((54, y - 6), str(k + 1), fill=C(40, 40, 60))
    outline(im, C(40, 40, 50)).save(PIC + 'Corrida_Portao.png')


def main():
    pv = Image.new('RGBA', (816, 6 * 300), (0, 0, 0, 255))
    for i, (nome, (ff, fc)) in enumerate(SECOES.items()):
        f = salvar(ff(), f'Corrida_{nome}_fundo')
        c = salvar(fc(), f'Corrida_{nome}_chao')
        pv.alpha_composite(f.resize((408, 210)), (0, i * 300)); pv.alpha_composite(c.resize((408, 130)), (408, i * 300))
    pv.resize((816 // 1, 1800 // 1)).save(PREV4 + 'corrida_fundos.png')
    make_obstaculos()
    make_portao()
    print('ok')


if __name__ == '__main__':
    main()
