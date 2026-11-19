# Capitulo 4: cartoes de capitulo, mapa de Mauara, cartas de taro, historia de Divilandia,
# lembranca da traicao, peruca pela metade, imagem final e cut-ins da corrida.
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, PROJ
import gen_ch1_assets as G1

_Draw = ImageDraw.Draw
_FORMAS = ('ellipse', 'polygon', 'line', 'rectangle', 'rounded_rectangle', 'arc', 'chord', 'pieslice', 'point', 'text')


class _DesenhoMisturado:
    """ImageDraw que mistura cores semitransparentes (o ImageDraw comum substitui o pixel em imagens RGBA)."""

    def __init__(self, im):
        self.im = im
        self._d = _Draw(im)

    def __getattr__(self, nome):
        attr = getattr(self._d, nome)
        if nome not in _FORMAS:
            return attr

        def desenhar(*a, **k):
            cores = [k.get('fill'), k.get('outline'), k.get('stroke_fill')]
            semi = any(isinstance(c, tuple) and len(c) == 4 and c[3] < 255 for c in cores)
            if not semi:
                return attr(*a, **k)
            camada = Image.new('RGBA', self.im.size, (0, 0, 0, 0))
            getattr(_Draw(camada), nome)(*a, **k)
            self.im.alpha_composite(camada)
        return desenhar


def _draw_rgba(im, mode=None):
    if mode is None and im.mode == 'RGBA':
        return _DesenhoMisturado(im)
    return _Draw(im, mode)


ImageDraw.Draw = _draw_rgba

PREV4 = HERE + '/prev4/'
os.makedirs(PREV4, exist_ok=True)
G.PREV = PREV4
PIC = PROJ + '/img/pictures/'
font = G1.font
RB = [(232, 52, 60), (250, 140, 40), (250, 214, 50), (84, 190, 92), (62, 132, 222), (150, 92, 206)]


def prev(im, nome, k=2):
    bg = Image.new('RGBA', im.size, (40, 44, 56, 255)); bg.alpha_composite(im)
    bg.resize((im.width // k, im.height // k), Image.LANCZOS).save(PREV4 + nome + '.png')


def grad(w, h, top, bottom, mid=None):
    t = np.linspace(0, 1, h)[:, None]
    arr = np.zeros((h, w, 4), np.uint8)
    for i in range(3):
        if mid is None:
            v = top[i] * (1 - t) + bottom[i] * t
        else:
            v = np.where(t < 0.5, top[i] * (1 - t * 2) + mid[i] * t * 2, mid[i] * (2 - t * 2) + bottom[i] * (t * 2 - 1))
        arr[..., i] = np.repeat(v, w, axis=1).astype(np.uint8)
    arr[..., 3] = 255
    return Image.fromarray(arr, 'RGBA')


def glow(im, box, color, blur, shape='ellipse'):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (d.ellipse if shape == 'ellipse' else d.rectangle)(box, fill=color)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def star4(d, x, y, r, col):
    d.polygon([(x, y - r), (x + r * 0.25, y - r * 0.25), (x + r, y), (x + r * 0.25, y + r * 0.25), (x, y + r),
               (x - r * 0.25, y + r * 0.25), (x - r, y), (x - r * 0.25, y - r * 0.25)], fill=col)


def ceu_estrelado(d, rng, box, n, cor=(255, 250, 230)):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rng.randint(x0, x1), rng.randint(y0, y1)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse((x - r, y - r, x + r, y + r), fill=cor + (rng.randint(120, 255),))


def legenda(im, txt, y=None, cor=(255, 236, 170), size=30):
    d = ImageDraw.Draw(im)
    f = font('georgiab.ttf', size)
    w = d.textlength(txt, font=f)
    y = im.height - 52 if y is None else y
    x0 = (im.width - w) / 2
    fita = Image.new('RGBA', im.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(fita)
    fd.rounded_rectangle((x0 - 26, y - 8, x0 + w + 26, y + size + 10), 14, fill=(30, 18, 34, 200))
    im.alpha_composite(fita)
    d = ImageDraw.Draw(im)
    d.text((x0 + 2, y + 2), txt, font=f, fill=(0, 0, 0, 200))
    d.text((x0, y), txt, font=f, fill=cor + (255,))


def moldura(arte, nome, sepia=False):
    W, H = arte.width + 40, arte.height + 40
    im = Image.new('RGBA', (W + 30, H + 30), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((18, 22, W + 12, H + 16), 22, fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    ouro, ouro_l, ouro_d = ((200, 170, 120), (236, 214, 170), (130, 100, 60)) if sepia else ((236, 196, 70), (255, 236, 150), (170, 124, 30))
    d.rounded_rectangle((15, 15, W + 14, H + 14), 20, fill=ouro_d + (255,))
    d.rounded_rectangle((18, 18, W + 11, H + 11), 18, fill=ouro + (255,))
    d.rounded_rectangle((24, 24, W + 5, H + 5), 14, fill=ouro_d + (255,))
    mask = Image.new('L', arte.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, arte.width - 1, arte.height - 1), 12, fill=255)
    im.paste(arte, (35, 35), mask)
    d = ImageDraw.Draw(im)
    for (x, y) in ((24, 24), (W + 5, 24), (24, H + 5), (W + 5, H + 5)):
        d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=ouro_l + (255,), outline=ouro_d + (255,), width=3)
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(200, 40, 90, 255) if not sepia else (150, 110, 70, 255))
    for x in range(70, W - 30, 60):
        d.ellipse((x - 3, 18, x + 3, 24), fill=ouro_l + (255,)); d.ellipse((x - 3, H + 11, x + 3, H + 17), fill=ouro_l + (255,))
    im.save(PIC + nome + '.png')
    prev(im, nome)
    return im


# ================================================================ figuras estilizadas para a historia
def diva(d, x, base, s, cabelo, vestido, pele, coroa=False, boa=None, bracos='baixo', olhos=None):
    h = 150 * s
    d.polygon([(x - 34 * s, base), (x + 34 * s, base), (x + 14 * s, base - h * 0.55), (x - 14 * s, base - h * 0.55)], fill=vestido)
    d.polygon([(x - 12 * s, base - h * 0.55), (x + 12 * s, base - h * 0.55), (x + 10 * s, base - h * 0.74), (x - 10 * s, base - h * 0.74)], fill=vestido)
    if bracos == 'cima':
        for sgn in (-1, 1):
            d.line((x + sgn * 10 * s, base - h * 0.72, x + sgn * 30 * s, base - h * 0.95), fill=pele, width=int(7 * s))
    else:
        for sgn in (-1, 1):
            d.line((x + sgn * 10 * s, base - h * 0.72, x + sgn * 20 * s, base - h * 0.45), fill=pele, width=int(7 * s))
    hy = base - h * 0.84
    d.ellipse((x - 30 * s, hy - 38 * s, x + 30 * s, hy + 18 * s), fill=cabelo)
    d.ellipse((x - 12 * s, hy - 12 * s, x + 12 * s, hy + 14 * s), fill=pele)
    if olhos:
        d.ellipse((x - 7 * s, hy - 2 * s, x - 3 * s, hy + 2 * s), fill=olhos); d.ellipse((x + 3 * s, hy - 2 * s, x + 7 * s, hy + 2 * s), fill=olhos)
    if boa:
        for k in range(9):
            t = k / 8
            bx = x - 22 * s + 44 * s * t
            by = base - h * 0.72 + math.sin(t * math.pi) * 10 * s
            d.ellipse((bx - 6 * s, by - 6 * s, bx + 6 * s, by + 6 * s), fill=boa)
    if coroa:
        cy = hy - 38 * s
        d.polygon([(x - 14 * s, cy + 6 * s), (x - 14 * s, cy - 8 * s), (x - 7 * s, cy), (x, cy - 12 * s), (x + 7 * s, cy),
                   (x + 14 * s, cy - 8 * s), (x + 14 * s, cy + 6 * s)], fill=(255, 220, 80, 255))
    return hy


def heroi(d, x, base, s, cor, arma='espada', flip=1):
    d.polygon([(x - 10 * s, base), (x + 10 * s, base), (x + 8 * s, base - 40 * s), (x - 8 * s, base - 40 * s)], fill=cor)
    d.ellipse((x - 8 * s, base - 58 * s, x + 8 * s, base - 40 * s), fill=cor)
    if arma == 'espada':
        d.line((x + 6 * s * flip, base - 34 * s, x + 22 * s * flip, base - 70 * s), fill=(230, 230, 240, 255), width=max(2, int(3 * s)))
    else:
        d.line((x + 6 * s * flip, base - 30 * s, x + 8 * s * flip, base - 80 * s), fill=(120, 80, 40, 255), width=max(2, int(3 * s)))
        d.polygon([(x + 8 * s * flip, base - 80 * s), (x + 30 * s * flip, base - 74 * s), (x + 8 * s * flip, base - 66 * s)], fill=arma)


def soldado(d, x, base, s, tocha=True):
    cor = (40, 30, 34, 255)
    d.polygon([(x - 11 * s, base), (x + 11 * s, base), (x + 9 * s, base - 44 * s), (x - 9 * s, base - 44 * s)], fill=cor)
    d.ellipse((x - 9 * s, base - 62 * s, x + 9 * s, base - 44 * s), fill=(214, 190, 170, 255))
    d.chord((x - 11 * s, base - 66 * s, x + 11 * s, base - 46 * s), 180, 360, fill=(170, 176, 190, 255))
    d.arc((x - 8 * s, base - 64 * s, x + 4 * s, base - 54 * s), 200, 280, fill=(255, 255, 255, 255), width=2)
    if tocha:
        d.line((x + 8 * s, base - 30 * s, x + 14 * s, base - 70 * s), fill=(110, 70, 40, 255), width=max(2, int(3 * s)))
        d.ellipse((x + 8 * s, base - 84 * s, x + 20 * s, base - 66 * s), fill=(255, 160, 40, 255))
        d.ellipse((x + 11 * s, base - 80 * s, x + 17 * s, base - 70 * s), fill=(255, 236, 120, 255))


def careca_monoculo(d, x, y, s, cor_pele=(236, 200, 170, 255)):
    d.ellipse((x - 24 * s, y - 28 * s, x + 24 * s, y + 26 * s), fill=cor_pele)
    d.arc((x - 18 * s, y - 24 * s, x + 6 * s, y - 6 * s), 200, 290, fill=(255, 255, 255, 255), width=max(1, int(3 * s)))
    d.ellipse((x + 2 * s, y - 6 * s, x + 14 * s, y + 6 * s), outline=(236, 196, 70, 255), width=max(1, int(2 * s)))
    d.ellipse((x - 12 * s, y - 3 * s, x - 6 * s, y + 3 * s), fill=(30, 20, 20, 255))
    d.ellipse((x + 6 * s, y - 3 * s, x + 10 * s, y + 3 * s), fill=(30, 20, 20, 255))
    d.line((x + 14 * s, y, x + 18 * s, y + 20 * s), fill=(236, 196, 70, 255), width=1)
    d.polygon([(x - 14 * s, y + 10 * s), (x, y + 6 * s), (x + 14 * s, y + 10 * s), (x, y + 13 * s)], fill=(70, 46, 30, 255))
    d.arc((x - 8 * s, y + 12 * s, x + 8 * s, y + 20 * s), 200, 340, fill=(120, 40, 40, 255), width=2)


def cobra(d, pts, larg, cor, cor_l):
    d.line(pts, fill=cor, width=larg, joint='curve')
    d.line(pts, fill=cor_l, width=max(2, larg // 4), joint='curve')


def saco_dinheiro(d, x, y, s):
    d.ellipse((x - 22 * s, y - 16 * s, x + 22 * s, y + 26 * s), fill=(200, 170, 110, 255))
    d.polygon([(x - 8 * s, y - 14 * s), (x + 8 * s, y - 14 * s), (x + 12 * s, y - 26 * s), (x - 12 * s, y - 26 * s)], fill=(200, 170, 110, 255))
    d.line((x - 10 * s, y - 15 * s, x + 10 * s, y - 15 * s), fill=(120, 80, 40, 255), width=3)
    f = font('georgiab.ttf', int(24 * s))
    d.text((x - 7 * s, y - 6 * s), '$', font=f, fill=(90, 120, 50, 255))


def casinha(d, x, base, s, cor_parede, cor_teto):
    d.rectangle((x - 22 * s, base - 30 * s, x + 22 * s, base), fill=cor_parede)
    d.polygon([(x - 28 * s, base - 30 * s), (x, base - 54 * s), (x + 28 * s, base - 30 * s)], fill=cor_teto)
    d.rectangle((x - 6 * s, base - 16 * s, x + 6 * s, base), fill=(110, 70, 40, 255))


def bicho(d, x, y, s, tipo):
    if tipo == 'ovelha':
        for (dx, dy) in ((-8, 0), (0, -5), (8, 0), (0, 4), (-4, -3), (5, -3)):
            d.ellipse((x + (dx - 9) * s, y + (dy - 7) * s, x + (dx + 9) * s, y + (dy + 7) * s), fill=(250, 250, 250, 255))
        d.ellipse((x + 12 * s, y - 8 * s, x + 22 * s, y + 4 * s), fill=(60, 60, 60, 255))
        d.line((x - 6 * s, y + 8 * s, x - 6 * s, y + 16 * s), fill=(60, 60, 60, 255), width=3)
        d.line((x + 6 * s, y + 8 * s, x + 6 * s, y + 16 * s), fill=(60, 60, 60, 255), width=3)
    else:
        d.ellipse((x - 18 * s, y - 10 * s, x + 16 * s, y + 12 * s), fill=(150, 104, 62, 255))
        d.ellipse((x + 8 * s, y - 14 * s, x + 26 * s, y + 4 * s), fill=(150, 104, 62, 255))
        d.ellipse((x + 18 * s, y - 8 * s, x + 21 * s, y - 5 * s), fill=(30, 20, 20, 255))
        d.line((x - 10 * s, y + 10 * s, x - 10 * s, y + 16 * s), fill=(110, 74, 42, 255), width=3)
        d.line((x + 8 * s, y + 10 * s, x + 8 * s, y + 16 * s), fill=(110, 74, 42, 255), width=3)


# ================================================================ painéis da historia (680x380 + moldura)
AW, AH = 680, 380


def h1_divilandia():
    im = grad(AW, AH, (255, 186, 214), (255, 236, 170))
    d = ImageDraw.Draw(im)
    for k in range(14):
        a = math.radians(-180 + k * 13)
        d.polygon([(340, 120), (340 + 700 * math.cos(a - 0.03), 120 + 700 * math.sin(a - 0.03)),
                   (340 + 700 * math.cos(a + 0.03), 120 + 700 * math.sin(a + 0.03))], fill=(255, 250, 220, 90))
    for (x, y, r) in ((90, 70, 30), (130, 64, 24), (560, 90, 34), (604, 84, 26)):
        d.ellipse((x - r, y - r * 0.6, x + r, y + r * 0.6), fill=(255, 255, 255, 230))
    d.polygon([(0, 330), (170, 290), (340, 300), (520, 282), (680, 310), (680, 380), (0, 380)], fill=(130, 200, 120, 255))
    pal = (250, 214, 232, 255); pal_d = (220, 160, 196, 255)
    d.rectangle((170, 170, 510, 320), fill=pal)
    for x in (160, 270, 410, 520):
        d.rectangle((x - 22, 120, x + 22, 320), fill=pal_d)
        d.ellipse((x - 26, 92, x + 26, 140), fill=(255, 214, 90, 255))
        d.line((x, 92, x, 64), fill=(140, 90, 50, 255), width=3)
        d.polygon([(x, 64), (x + 26, 72), (x, 82)], fill=(255, 80, 150, 255))
    d.ellipse((290, 90, 390, 190), fill=(255, 214, 90, 255))
    for x in range(190, 500, 40):
        d.rounded_rectangle((x, 230, x + 20, 270), 10, fill=(170, 110, 160, 255))
    d.rectangle((310, 250, 370, 320), fill=(150, 80, 120, 255))
    d.rectangle((270, 186, 410, 200), fill=(236, 196, 70, 255))
    glow(im, (270, 60, 410, 210), (255, 250, 200, 140), 24)
    d = ImageDraw.Draw(im)
    diva(d, 340, 190, 0.62, (255, 222, 100, 255), (255, 92, 160, 255), (246, 210, 180, 255), coroa=True, bracos='cima')
    rng = random.Random(1)
    for _ in range(26):
        star4(d, rng.randint(10, 670), rng.randint(10, 300), rng.randint(3, 8), (255, 255, 240, 230))
    legenda(im, 'Reino de Divilândia')
    return im


def h2_vera_prime():
    im = grad(AW, AH, (40, 14, 60), (110, 40, 90))
    d = ImageDraw.Draw(im)
    rng = random.Random(2)
    ceu_estrelado(d, rng, (0, 0, 680, 200), 60)
    d.polygon([(400, 330), (430, 150), (460, 330)], fill=(30, 14, 40, 255))
    for (x, top) in ((470, 100), (540, 60), (610, 120)):
        d.rectangle((x - 26, top + 30, x + 26, 330), fill=(36, 18, 50, 255))
        d.polygon([(x - 32, top + 34), (x, top - 30), (x + 32, top + 34)], fill=(60, 24, 80, 255))
        d.rectangle((x - 6, top + 70, x + 6, top + 90), fill=(255, 60, 90, 255))
    d.polygon([(0, 330), (680, 320), (680, 380), (0, 380)], fill=(30, 12, 36, 255))
    # brilho sendo sugado
    for k in range(40):
        t = k / 40
        x = 30 + t * 240 + rng.uniform(-10, 10)
        y = 120 + math.sin(t * 7) * 40 + rng.uniform(-10, 10)
        star4(d, x, y, 3 + t * 5, (255, 230, 120, 255))
    glow(im, (200, 70, 360, 330), (190, 40, 120, 150), 30)
    d = ImageDraw.Draw(im)
    hy = diva(d, 290, 330, 1.2, (250, 214, 112, 255), (110, 20, 60, 255), (112, 70, 52, 255), bracos='cima',
              boa=(255, 196, 228, 255), olhos=(255, 40, 60, 255))
    legenda(im, 'Vera Verão Prime')
    return im


def h3_batalha():
    im = grad(AW, AH, (60, 40, 90), (240, 150, 120))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 140), (150, 90), (240, 160), (0, 200)], fill=(80, 60, 100, 255))
    d.polygon([(680, 150), (540, 90), (440, 160), (680, 210)], fill=(80, 60, 100, 255))
    diva(d, 120, 120, 0.42, (255, 222, 100, 255), (255, 92, 160, 255), (246, 210, 180, 255), coroa=True)
    diva(d, 560, 120, 0.42, (250, 214, 112, 255), (110, 20, 60, 255), (112, 70, 52, 255), boa=(255, 196, 228, 255))
    for (x0, x1) in ((90, 150), (530, 590)):
        d.line([(x0 + 20, 0), (x0 + 5, 40), (x0 + 30, 60), (x0 + 10, 100)], fill=(255, 255, 200, 255), width=5)
    d.polygon([(0, 300), (680, 290), (680, 380), (0, 380)], fill=(90, 70, 60, 255))
    rng = random.Random(3)
    cores = [(60, 90, 160, 255), (160, 50, 60, 255), (60, 120, 70, 255), (120, 80, 150, 255), (200, 140, 40, 255)]
    for k in range(26):
        x = 40 + k * 23 + rng.uniform(-8, 8)
        s = 0.7 + rng.random() * 0.4
        heroi(d, x, 330 + rng.uniform(-6, 10), s, cores[k % 5], 'espada' if k % 3 else cores[(k + 2) % 5], flip=1 if x < 340 else -1)
    legenda(im, 'Heróis de todos os lados se uniram')
    return im


def h4_paz():
    im = grad(AW, AH, (140, 200, 255), (210, 240, 255))
    d = ImageDraw.Draw(im)
    d.ellipse((560, 30, 640, 110), fill=(255, 236, 120, 255))
    glow(im, (530, 0, 670, 140), (255, 240, 160, 120), 20)
    d = ImageDraw.Draw(im)
    for k, c in enumerate(RB):
        r = 330 - k * 14
        d.arc((340 - r, 300 - r, 340 + r, 300 + r), 180, 360, fill=c + (230,), width=14)
    d.polygon([(0, 270), (200, 240), (420, 260), (680, 236), (680, 380), (0, 380)], fill=(120, 196, 100, 255))
    d.polygon([(0, 320), (680, 300), (680, 380), (0, 380)], fill=(100, 176, 86, 255))
    for (x, c, t) in ((90, (250, 240, 220, 255), (200, 80, 70, 255)), (180, (240, 220, 200, 255), (90, 120, 200, 255)),
                      (520, (250, 236, 210, 255), (200, 120, 60, 255))):
        casinha(d, x, 290, 1.0, c, t)
    for (x, y, tp) in ((260, 320, 'ovelha'), (330, 336, 'capivara'), (420, 322, 'ovelha'), (600, 334, 'capivara')):
        bicho(d, x, y, 1.0, tp)
    rng = random.Random(4)
    for _ in range(30):
        x, y = rng.randint(0, 680), rng.randint(300, 370)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=rng.choice([(255, 120, 160, 255), (255, 230, 90, 255), (255, 255, 255, 255)]))
    legenda(im, 'E o mundo viveu em paz...')
    return im


def h5_araujo():
    im = grad(AW, AH, (24, 50, 34), (60, 90, 50))
    d = ImageDraw.Draw(im)
    for k, x in enumerate((150, 340, 530)):
        d.rectangle((x - 70, 30, x + 70, 200), fill=(150, 110, 50, 255))
        d.rectangle((x - 60, 40, x + 60, 190), fill=(70, 50, 60, 255))
        careca_monoculo(d, x, 112, 1.6 - k * 0.1)
        d.rectangle((x - 40, 170, x + 40, 190), fill=(110, 70, 140, 255))
    pts = [(-20, 300), (80, 250), (160, 320), (260, 260), (340, 330), (430, 260), (520, 320), (610, 260), (700, 300)]
    cobra(d, pts, 34, (60, 140, 60, 255), (140, 210, 110, 255))
    d.ellipse((600, 236, 650, 280), fill=(60, 140, 60, 255))
    d.ellipse((622, 246, 632, 256), fill=(255, 220, 40, 255))
    d.line((646, 262, 668, 270), fill=(200, 40, 60, 255), width=3)
    for x in (110, 300, 480):
        saco_dinheiro(d, x, 330, 1.0)
    legenda(im, 'A família Araújo, a linhagem do Raulete', size=26)
    return im


def h6_golpe():
    im = grad(AW, AH, (60, 10, 20), (200, 80, 40))
    d = ImageDraw.Draw(im)
    rng = random.Random(6)
    for _ in range(40):
        x, y = rng.randint(0, 680), rng.randint(0, 260)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 180, 80, 160))
    d.polygon([(0, 300), (680, 300), (680, 380), (0, 380)], fill=(40, 20, 20, 255))
    for k in range(7):
        soldado(d, 400 + k * 42, 330 - (k % 2) * 6, 1.0)
    for k, x in enumerate((70, 160, 250)):
        diva(d, x, 340, 0.5 + (k % 2) * 0.08, [(255, 222, 100, 255), (230, 90, 40, 255), (40, 34, 50, 255)][k],
             [(255, 92, 160, 255), (120, 200, 255, 255), (180, 120, 255, 255)][k], (240, 200, 170, 255),
             boa=(255, 220, 240, 255), bracos='cima')
    for _ in range(26):
        x, y = rng.randint(20, 330), rng.randint(260, 370)
        star4(d, x, y, rng.randint(2, 5), rng.choice([(255, 214, 90, 255), (255, 150, 200, 255), (200, 220, 255, 255)]))
    legenda(im, 'O golpe: caçaram todas as bichas e divas', size=26)
    return im


def h7_fuga():
    im = grad(AW, AH, (14, 18, 50), (40, 60, 90))
    d = ImageDraw.Draw(im)
    rng = random.Random(7)
    ceu_estrelado(d, rng, (0, 0, 680, 220), 70)
    d.ellipse((520, 40, 600, 120), fill=(255, 248, 214, 255))
    glow(im, (480, 0, 640, 160), (255, 248, 214, 90), 20)
    d = ImageDraw.Draw(im)
    for k in range(9):
        x = 20 + k * 80 + rng.uniform(-10, 10)
        d.polygon([(x - 40, 330), (x, 150 + rng.uniform(-30, 30)), (x + 40, 330)], fill=(16, 40, 30, 255))
    d.polygon([(0, 320), (680, 310), (680, 380), (0, 380)], fill=(20, 30, 26, 255))
    x, base = 330, 330
    d.polygon([(x - 30, base), (x + 40, base), (x + 20, base - 70), (x - 14, base - 70)], fill=(230, 90, 150, 255))
    d.polygon([(x - 14, base - 70), (x + 20, base - 70), (x + 70, base - 40), (x + 56, base - 30)], fill=(200, 60, 120, 255))
    d.ellipse((x - 14, base - 106, x + 18, base - 70), fill=(250, 214, 96, 255))
    d.ellipse((x - 8, base - 98, x + 12, base - 74), fill=(246, 210, 180, 255))
    d.polygon([(x + 10, base - 100), (x + 52, base - 92), (x + 16, base - 80)], fill=(250, 214, 96, 255))
    d.line((x - 10, base - 60, x - 40, base - 46), fill=(246, 210, 180, 255), width=6)
    d.line((x - 40, base - 46, x - 42, base - 30), fill=(120, 90, 50, 255), width=2)
    d.rectangle((x - 50, base - 30, x - 34, base - 12), fill=(255, 210, 90, 255))
    glow(im, (x - 90, base - 70, x + 6, base + 20), (255, 210, 90, 160), 14)
    d = ImageDraw.Draw(im)
    # o ratinho no ombro
    mx, my = x + 10, base - 74
    d.ellipse((mx - 6, my - 6, mx + 8, my + 4), fill=(170, 170, 180, 255))
    d.ellipse((mx - 9, my - 10, mx - 3, my - 4), fill=(200, 160, 170, 255))
    d.point((mx - 4, my - 2), fill=(20, 20, 20, 255))
    d.line((mx + 8, my, mx + 18, my + 6), fill=(200, 160, 170, 255), width=1)
    for k in range(4):
        d.line((x + 40 + k * 22, base - 40 + k * 4, x + 70 + k * 22, base - 40 + k * 4), fill=(255, 255, 255, 120), width=2)
    legenda(im, 'A filha da Hebe com o Ratinho fugiu', size=26)
    return im


def h8_linhagem():
    im = grad(AW, AH, (50, 20, 80), (150, 70, 140))
    d = ImageDraw.Draw(im)
    rng = random.Random(8)
    ceu_estrelado(d, rng, (0, 0, 680, 380), 50)
    for k in range(5):
        a = -30 + k * 15
        cx, cy = 140 + k * 26, 120
        card = Image.new('RGBA', (60, 96), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, 59, 95), 6, fill=(244, 232, 200, 255))
        cd.rounded_rectangle((4, 4, 55, 91), 4, fill=(60, 30, 90, 255))
        star4(cd, 30, 48, 12, (240, 204, 110, 255))
        card = card.rotate(-a, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(card, (int(cx - card.width / 2), int(cy - card.height / 2)))
    d = ImageDraw.Draw(im)
    gens = [(130, 300, 0.42, (255, 222, 100, 255), (230, 90, 150, 255)),
            (250, 300, 0.40, (120, 80, 40, 255), (90, 120, 200, 255)),
            (360, 300, 0.40, (200, 150, 60, 255), (120, 180, 100, 255)),
            (470, 300, 0.40, (80, 50, 30, 255), (200, 120, 60, 255))]
    pts = []
    for (x, base, s, hair, dress) in gens:
        hy = diva(d, x, base, s, hair, dress, (240, 204, 174, 255))
        pts.append((x, hy - 20))
    bx, base = 590, 310
    pts.append((bx, 150))
    d.line(pts, fill=(255, 220, 120, 255), width=4, joint='curve')
    for (x, y) in pts:
        d.polygon([(x, y + 10), (x - 10, y), (x - 6, y - 7), (x, y - 3), (x + 6, y - 7), (x + 10, y)], fill=(255, 90, 150, 255))
    glow(im, (bx - 70, 120, bx + 70, 340), (255, 230, 150, 150), 20)
    d = ImageDraw.Draw(im)
    sil = (30, 14, 40, 255)
    d.polygon([(bx - 40, base), (bx + 40, base), (bx + 22, base - 80), (bx - 22, base - 80)], fill=sil)
    d.rectangle((bx - 18, base - 112, bx + 18, base - 78), fill=sil)
    d.ellipse((bx - 18, base - 150, bx + 20, base - 108), fill=sil)
    for sgn in (-1, 1):
        px = bx + sgn * 24
        d.polygon([(px, base - 136), (px + sgn * 14, base - 126), (px + sgn * 16, base - 96), (px + sgn * 8, base - 80), (px - sgn * 2, base - 104)], fill=sil)
    d.polygon([(bx - 4, base - 142), (bx - 22, base - 146), (bx - 32, base - 124), (bx - 28, base - 96), (bx - 18, base - 120)], fill=sil)
    d.ellipse((bx - 16, base - 152, bx - 6, base - 142), fill=(230, 30, 70, 255))
    legenda(im, 'O sangue divino, de geração em geração', size=26)
    return im


def flashback():
    im = grad(AW, AH, (80, 64, 50), (150, 124, 90))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 250, 680, 380), fill=(90, 80, 70, 255))
    for k in range(10):
        y = 270 + k * 11
        d.line((0, y, 680, y + 4), fill=(120, 106, 90, 255), width=2)
    d.rectangle((0, 210, 680, 250), fill=(130, 96, 60, 255))
    for x in range(0, 680, 34):
        d.line((x, 210, x, 250), fill=(100, 74, 46, 255), width=2)
    d.line((0, 180, 680, 180), fill=(100, 74, 46, 255), width=5)
    for x in range(20, 680, 80):
        d.line((x, 180, x, 210), fill=(100, 74, 46, 255), width=5)
    # Leandra (loira) e Leona avancando; Raulete atras puxando os cabelos dourados
    lx, base = 300, 210
    d.polygon([(lx - 22, base), (lx + 22, base), (lx + 12, base - 50), (lx - 12, base - 50)], fill=(170, 150, 120, 255))
    d.ellipse((lx - 16, base - 82, lx + 16, base - 50), fill=(232, 210, 180, 255))
    for k in range(9):
        t = k / 8
        d.line((lx + 10, base - 74 + k * 3, lx + 100 + t * 120, base - 120 + math.sin(t * 6) * 30 + k * 2), fill=(250, 214, 96, 255), width=3)
    rx = 540
    d.polygon([(rx - 40, base), (rx + 40, base), (rx + 26, base - 90), (rx - 26, base - 90)], fill=(60, 30, 70, 255))
    careca_monoculo(d, rx, base - 116, 1.0)
    d.line((rx - 26, base - 80, rx - 70, base - 110), fill=(236, 220, 210, 255), width=8)
    ox = 200
    d.polygon([(ox - 20, base), (ox + 20, base), (ox + 14, base - 56), (ox - 10, base - 56)], fill=(110, 30, 50, 255))
    d.ellipse((ox - 14, base - 86, ox + 16, base - 56), fill=(240, 226, 214, 255))
    d.polygon([(ox - 16, base - 82), (ox + 14, base - 88), (ox - 30, base - 40), (ox - 26, base - 70)], fill=(30, 26, 36, 255))
    d.line((ox + 10, base - 46, ox + 60, base - 54), fill=(240, 226, 214, 255), width=6)
    d.polygon([(ox + 58, base - 58), (ox + 92, base - 56), (ox + 58, base - 50)], fill=(230, 230, 240, 255))
    star4(d, ox + 92, base - 56, 8, (255, 255, 255, 255))
    arr = np.array(im).astype(float)
    g = arr[..., :3].mean(axis=2)
    arr[..., 0] = np.clip(g * 1.08 + 18, 0, 255); arr[..., 1] = np.clip(g * 0.92 + 8, 0, 255); arr[..., 2] = np.clip(g * 0.7, 0, 255)
    im = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    vin = Image.new('L', im.size, 0); ImageDraw.Draw(vin).ellipse((-80, -60, AW + 80, AH + 60), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(40))
    dark = Image.new('RGBA', im.size, (40, 26, 16, 255))
    im = Image.composite(im, dark, vin)
    legenda(im, 'A traição na ponte', cor=(255, 230, 200))
    return im


# ================================================================ bustos em pixel art (96x96 ampliado)
SK = G.SKIN; SK_D = G.SKIN_D
HR, HR_L, HR_D = G.HAIR, G.HAIR_L, G.HAIR_D
BEARD, BEARD_L = G.BEARD, G.BEARD_L


def meia_peruca_px(d, x, y, s=1.0):
    base, luz, esc = (255, 206, 64, 255), (255, 240, 160, 255), (200, 150, 30, 255)
    d.pieslice((x - 18 * s, y - 16 * s, x + 18 * s, y + 16 * s), 90, 270, fill=base)
    for k in range(5):
        cy = y + 6 * s + k * 5 * s
        d.ellipse((x - 18 * s, cy - 3 * s, x - 10 * s, cy + 3 * s), fill=base)
        d.arc((x - 17 * s, cy - 2 * s, x - 11 * s, cy + 2 * s), 180, 360, fill=luz)
    for (cx, cy) in ((x - 10 * s, y - 8 * s), (x - 4 * s, y - 12 * s), (x - 12 * s, y), (x - 4 * s, y - 2 * s)):
        d.arc((cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s), 180, 360, fill=luz)
    pts = [(x, y - 16 * s)]
    for k in range(1, 9):
        pts.append((x + (2 if k % 2 else -1) * s, y - 16 * s + k * 4 * s))
    d.line(pts, fill=esc, width=2)


def busto_baratelli(expr='raiva', peruca=True):
    im = Image.new('RGBA', (96, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # guarda-chuva amarelo atras
    d.line((76, 22, 66, 70), fill=(140, 96, 52, 255), width=2)
    d.pieslice((52, 4, 96, 44), 180, 360, fill=(255, 214, 40, 255))
    for a in (210, 240, 270, 300, 330):
        d.line((74, 24, 74 + 22 * math.cos(math.radians(a)), 24 + 20 * math.sin(math.radians(a))), fill=(206, 152, 18, 255))
    # cabelo, chiquinhas e rabo
    d.ellipse((18, 6, 78, 58), fill=HR)
    for (x0, flip) in ((20, -1), (76, 1)):
        d.polygon([(x0, 30), (x0 + 12 * flip, 34), (x0 + 14 * flip, 60), (x0 + 8 * flip, 82), (x0 - 2 * flip, 64)], fill=HR)
        G.curls(d, (min(x0, x0 + 14 * flip), 34, max(x0, x0 + 14 * flip), 78), HR_L, step=4)
        d.rectangle((x0 - 2, 28, x0 + 3, 33), fill=(250, 210, 60, 255))
    G.curls(d, (24, 8, 72, 30), HR_L, step=4)
    # vestido arco-iris
    for k, c in enumerate(RB):
        d.rectangle((14, 74 + k * 4, 82, 77 + k * 4), fill=c + (255,))
    d.ellipse((8, 66, 30, 86), fill=(255, 170, 214, 255)); d.ellipse((66, 66, 88, 86), fill=(255, 170, 214, 255))
    d.rectangle((40, 60, 56, 74), fill=SK_D)
    # rosto
    d.ellipse((30, 20, 66, 66), fill=SK)
    d.polygon([(30, 44), (66, 44), (64, 58), (56, 68), (40, 68), (32, 58)], fill=BEARD)
    d.polygon([(36, 46), (60, 46), (58, 50), (38, 50)], fill=BEARD_L)
    if expr == 'raiva':
        d.rectangle((40, 54, 56, 59), fill=(250, 250, 250, 255))
        for x in range(42, 56, 3):
            d.line((x, 54, x, 59), fill=(170, 150, 150, 255))
        d.rectangle((40, 54, 56, 59), outline=(120, 40, 40, 255))
    else:
        d.chord((40, 52, 56, 62), 0, 180, fill=(150, 50, 60, 255))
    for ex in (38, 58):
        d.rectangle((ex - 7, 33, ex + 7, 43), outline=(52, 52, 64, 255), fill=(226, 236, 242, 255), width=2)
        d.ellipse((ex - 2, 36, ex + 2, 41), fill=(36, 26, 26, 255))
    d.line((45, 37, 51, 37), fill=(52, 52, 64, 255), width=2)
    if expr == 'raiva':
        d.line((31, 27, 44, 32), fill=HR_D, width=3); d.line((65, 27, 52, 32), fill=HR_D, width=3)
        d.line((46, 24, 50, 24), fill=(200, 60, 60, 255)); d.line((47, 22, 49, 26), fill=(200, 60, 60, 255))
    else:
        d.line((31, 28, 44, 29), fill=HR_D, width=3); d.line((65, 28, 52, 29), fill=HR_D, width=3)
    d.polygon([(30, 26), (66, 26), (64, 20), (48, 16), (32, 20)], fill=HR)
    G3flower(d, 30, 14)
    if peruca:
        d.ellipse((60, 70, 76, 86), fill=SK)
        meia_peruca_px(d, 74, 70, 1.0)
    return outline(im, (46, 24, 30, 255))


def G3flower(d, x, y):
    for k in range(5):
        a = k / 5 * 2 * math.pi
        px, py = x + math.cos(a) * 4, y + math.sin(a) * 4
        d.ellipse((px - 3, py - 3, px + 3, py + 3), fill=(230, 30, 70, 255))
    d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 220, 60, 255))


def busto_leona():
    im = Image.new('RGBA', (96, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pale, hair, hair_l, suit = (252, 230, 216, 255), (40, 34, 50, 255), (92, 82, 116, 255), (72, 34, 100, 255)
    d.polygon([(60, 10), (84, 16), (92, 50), (86, 90), (74, 60), (66, 26)], fill=(24, 20, 30, 255))
    d.polygon([(10, 96), (16, 74), (34, 66), (62, 66), (80, 74), (86, 96)], fill=suit)
    d.line((48, 70, 48, 96), fill=(236, 196, 86, 255), width=2)
    d.ellipse((24, 10, 72, 58), fill=hair)
    d.ellipse((30, 22, 66, 66), fill=pale)
    d.polygon([(26, 24), (70, 24), (70, 34), (58, 30), (46, 40), (34, 32), (26, 38)], fill=hair)
    for ex, sgn in ((39, 1), (57, -1)):
        d.polygon([(ex - 6, 44 - sgn), (ex + 6, 44 + sgn), (ex + 5, 47), (ex - 5, 47)], fill=(255, 255, 255, 255))
        d.ellipse((ex - 3, 43, ex + 3, 48), fill=(200, 30, 60, 255))
        d.line((ex - 7, 41 + sgn * 2, ex + 7, 41 - sgn * 2), fill=(30, 20, 30, 255), width=2)
    d.line((42, 58, 52, 56), fill=(150, 50, 70, 255), width=2); d.point((53, 55), fill=(150, 50, 70, 255))
    for ex, flip in ((26, 1), (70, -1)):
        d.polygon([(ex, 20), (ex + 5 * flip, -2), (ex + 16 * flip, 14)], fill=(64, 46, 50, 255))
        d.polygon([(ex + 4 * flip, 16), (ex + 6 * flip, 4), (ex + 12 * flip, 14)], fill=(200, 140, 150, 255))
    d.rectangle((42, 8, 54, 12), fill=(236, 196, 86, 255))
    return outline(im, (22, 12, 26, 255))


def px_up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def make_final():
    W, H = 816, 624
    im = grad(W, H, (70, 16, 40), (250, 120, 60), mid=(180, 40, 60))
    d = ImageDraw.Draw(im)
    rng = random.Random(14)
    ceu_estrelado(d, rng, (0, 0, 816, 200), 50)
    d.ellipse((560, 60, 700, 200), fill=(255, 244, 214, 255))
    d.ellipse((546, 54, 686, 194), fill=None)
    d.ellipse((586, 52, 716, 196), fill=(150, 40, 60, 140))
    glow(im, (520, 20, 740, 240), (255, 230, 200, 70), 30)
    d = ImageDraw.Draw(im)
    for k in range(18):
        x = k * 50 + rng.uniform(-10, 10)
        d.polygon([(x - 40, 624), (x, 380 + rng.uniform(-50, 30)), (x + 40, 624)], fill=(30, 10, 24, 255))
    for k in range(26):
        a = math.radians(rng.uniform(0, 360))
        r = rng.uniform(300, 600)
        d.line((408, 330, 408 + r * math.cos(a), 330 + r * math.sin(a)), fill=(255, 200, 150, 40), width=rng.randint(2, 6))
    b = px_up(busto_baratelli('raiva', True), 5)
    glow(im, (160, 120, 660, 620), (255, 140, 80, 120), 40)
    im.alpha_composite(b, (408 - b.width // 2, 624 - b.height + 6))
    d = ImageDraw.Draw(im)
    for _ in range(18):
        star4(d, rng.randint(480, 700), rng.randint(330, 560), rng.randint(3, 8), (255, 236, 150, 255))
    im.save(PIC + 'Final_Cap4.png')
    prev(im, 'Final_Cap4')


def cut_in(nome, busto, texto, sub, cor1, cor2, lado='esq'):
    W, H = 816, 230
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    faixa = grad(W, H, cor1, cor2)
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).polygon([(0, 26), (W, 0), (W, H - 26), (0, H)], fill=255)
    im.paste(faixa, (0, 0), mask)
    d = ImageDraw.Draw(im)
    rng = random.Random(len(nome))
    for _ in range(40):
        y = rng.randint(20, H - 20); x = rng.randint(-100, W)
        d.line((x, y, x + rng.randint(80, 260), y), fill=(255, 255, 255, rng.randint(40, 120)), width=rng.randint(1, 3))
    d.line((0, 26, W, 0), fill=(255, 255, 255, 255), width=4); d.line((0, H, W, H - 26), fill=(255, 255, 255, 255), width=4)
    b = px_up(busto, 3)
    bx = 30 if lado == 'esq' else W - b.width - 30
    im.alpha_composite(b, (bx, H - b.height + 20 if b.height > H else 0))
    f = font('impact.ttf', 58); fs = font('georgiab.ttf', 26)
    tx = 330 if lado == 'esq' else 40
    d = ImageDraw.Draw(im)
    for (dx, dy) in ((4, 4),):
        d.text((tx + dx, 58 + dy), texto, font=f, fill=(0, 0, 0, 160))
    d.text((tx, 58), texto, font=f, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(60, 20, 60, 255))
    fs = font('georgiab.ttf', 21)
    d.text((tx + 4, 136), sub, font=fs, fill=(255, 240, 180, 255), stroke_width=2, stroke_fill=(40, 10, 40, 255))
    im = im.crop((0, 0, W, H))
    im.save(PIC + nome + '.png')
    prev(im, nome)


# ================================================================ cartas de taro
def carta(nome_arq, titulo, numeral, desenho, fundo=((48, 26, 72), (90, 50, 120))):
    S = 2
    W, H = 380, 620
    im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sc = lambda *v: tuple(int(x * S) for x in v)
    d.rounded_rectangle(sc(0, 0, W - 1, H - 1), 18 * S, fill=(244, 232, 200, 255))
    d.rounded_rectangle(sc(10, 10, W - 11, H - 11), 12 * S, fill=fundo[0] + (255,))
    inner = grad((W - 60) * S, (H - 150) * S, fundo[0], fundo[1])
    im.alpha_composite(inner, sc(30, 70))
    d = ImageDraw.Draw(im)
    desenho(im, d, sc, S)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(sc(18, 18, W - 19, H - 19), 10 * S, outline=(232, 190, 90, 255), width=3 * S)
    tf = font('georgiab.ttf', 28 * S); nf = font('georgiab.ttf', 24 * S)
    d.rectangle(sc(30, 548, W - 30, 594), fill=fundo[0] + (255,))
    w = d.textlength(titulo, font=tf)
    d.text(((W * S - w) / 2, 556 * S), titulo, font=tf, fill=(240, 204, 110, 255))
    w = d.textlength(numeral, font=nf)
    d.text(((W * S - w) / 2, 32 * S), numeral, font=nf, fill=(240, 204, 110, 255))
    im = im.resize((W, H), Image.LANCZOS)
    g = Image.new('RGBA', (W + 60, H + 60), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((20, 20, W + 40, H + 40), 24, fill=(255, 220, 140, 160))
    g = g.filter(ImageFilter.GaussianBlur(14))
    g.alpha_composite(im, (30, 30))
    g.save(PIC + nome_arq + '.png')
    prev(g, nome_arq)


def des_vidente(im, d, sc, S):
    rng = random.Random(21)
    for _ in range(40):
        x, y = rng.randint(36, 344), rng.randint(76, 300)
        d.ellipse(sc(x - 1, y - 1, x + 1, y + 1), fill=(255, 250, 220, 255))
    d.ellipse(sc(250, 90, 320, 160), fill=(250, 240, 200, 255)); d.ellipse(sc(268, 84, 338, 154), fill=(78, 42, 108, 255))
    cx = 190
    old, old_d, shawl, shawl_l = (236, 206, 182, 255), (206, 170, 146, 255), (108, 58, 140, 255), (146, 96, 180, 255)
    d.polygon(sc(cx - 120, 540, cx + 120, 540, cx + 80, 360, cx - 80, 360), fill=shawl)
    d.polygon(sc(cx - 90, 360, cx + 90, 360, cx + 50, 430, cx, 450, cx - 50, 430), fill=shawl_l)
    d.ellipse(sc(cx - 70, 190, cx + 70, 360), fill=old)
    d.ellipse(sc(cx - 50, 200, cx - 10, 240), fill=(255, 255, 255, 230))
    glow_l = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(glow_l).ellipse(sc(cx - 90, 170, cx + 90, 300), fill=(255, 255, 230, 110))
    im.alpha_composite(glow_l.filter(ImageFilter.GaussianBlur(20 * S)))
    d = ImageDraw.Draw(im)
    for ex in (cx - 28, cx + 28):
        d.ellipse(sc(ex - 14, 268, ex + 14, 290), fill=(255, 255, 255, 255))
        d.ellipse(sc(ex - 8, 268, ex + 8, 290), fill=(58, 116, 210, 255))
        d.ellipse(sc(ex - 3, 274, ex + 3, 284), fill=(20, 30, 60, 255))
    for (y,) in ((250,), (240,)):
        d.arc(sc(cx - 40, y - 10, cx + 40, y + 10), 200, 340, fill=old_d, width=3 * S)
    d.arc(sc(cx - 20, 310, cx + 20, 330), 20, 160, fill=(150, 70, 70, 255), width=3 * S)
    bola = Image.new('RGBA', im.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(bola)
    bd.ellipse(sc(cx - 70, 400, cx + 70, 540), fill=(150, 220, 255, 230))
    bd.ellipse(sc(cx - 50, 416, cx - 10, 456), fill=(255, 255, 255, 200))
    im.alpha_composite(bola.filter(ImageFilter.GaussianBlur(2 * S)))
    glow_b = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(glow_b).ellipse(sc(cx - 100, 380, cx + 100, 560), fill=(150, 220, 255, 90))
    im.alpha_composite(glow_b.filter(ImageFilter.GaussianBlur(16 * S)))
    d = ImageDraw.Draw(im)
    for (x, y) in ((cx - 30, 440), (cx + 20, 470), (cx - 4, 500)):
        star4(d, x * S, y * S, 8 * S, (255, 255, 255, 255))
    d.rectangle(sc(cx - 50, 530, cx + 50, 546), fill=(120, 80, 48, 255))


def des_sapo(im, d, sc, S):
    rng = random.Random(22)
    d.ellipse(sc(40, 430, 340, 540), fill=(40, 110, 90, 255))
    d.ellipse(sc(60, 440, 320, 530), fill=(60, 140, 110, 255))
    for k in range(6):
        x = 70 + k * 46
        d.line(sc(x, 400, x + rng.randint(-10, 10), 300), fill=(90, 160, 80, 255), width=4 * S)
    cx = 190
    frg, frg_l, frg_d, belly = (94, 168, 76, 255), (140, 204, 108, 255), (60, 118, 48, 255), (214, 228, 150, 255)
    d.ellipse(sc(cx - 110, 300, cx + 110, 500), fill=frg)
    d.ellipse(sc(cx - 70, 340, cx + 70, 490), fill=belly)
    for k in range(3):
        d.line(sc(cx - 40, 380 + k * 30, cx + 40, 380 + k * 30), fill=(190, 200, 120, 255), width=2 * S)
    for sgn in (-1, 1):
        sx = cx + sgn * 88
        ex = cx + sgn * 146
        d.line(sc(sx, 330, ex, 330), fill=frg, width=46 * S)
        d.ellipse(sc((sx + ex) / 2 - 34, 282, (sx + ex) / 2 + 34, 336), fill=frg_l)
        d.arc(sc((sx + ex) / 2 - 34, 282, (sx + ex) / 2 + 34, 336), 200, 340, fill=(255, 255, 255, 160), width=3 * S)
        d.line(sc(ex, 340, ex, 214), fill=frg, width=38 * S)
        d.ellipse(sc(ex - 28, 172, ex + 28, 230), fill=frg)
        for k in range(3):
            d.ellipse(sc(ex - 24 + k * 16, 164, ex - 10 + k * 16, 182), fill=frg_l)
        for k in range(3):
            d.line(sc(ex + sgn * 34, 190 + k * 16, ex + sgn * 52, 184 + k * 16), fill=(255, 255, 255, 220), width=3 * S)
    d.ellipse(sc(cx - 80, 200, cx + 80, 330), fill=frg)
    for ex in (cx - 50, cx + 50):
        d.ellipse(sc(ex - 34, 160, ex + 34, 230), fill=frg)
        d.ellipse(sc(ex - 24, 170, ex + 24, 220), fill=(255, 255, 255, 255))
        d.ellipse(sc(ex - 10, 180, ex + 10, 212), fill=(30, 20, 30, 255))
        d.line(sc(ex - 26, 172, ex + 20, 184 if ex < cx else 160), fill=(30, 40, 20, 255), width=4 * S)
    d.arc(sc(cx - 60, 250, cx + 60, 310), 20, 160, fill=frg_d, width=5 * S)
    d.polygon(sc(cx - 14, 296, cx + 14, 296, cx, 310), fill=(255, 255, 255, 255))
    d.polygon(sc(cx - 100, 300, cx - 60, 300, cx - 70, 420, cx - 110, 420), fill=(120, 70, 40, 255))
    d.polygon(sc(cx + 100, 300, cx + 60, 300, cx + 70, 420, cx + 110, 420), fill=(120, 70, 40, 255))
    for (x, y) in ((70, 120), (310, 140), (60, 260), (320, 280)):
        star4(d, x * S, y * S, 10 * S, (255, 250, 200, 255))


def des_traveco(im, d, sc, S):
    rng = random.Random(23)
    for k, c in enumerate(RB):
        r = 200 - k * 16
        d.arc(sc(190 - r, 330 - r, 190 + r, 330 + r), 180, 360, fill=c + (255,), width=16 * S)
    glow_l = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(glow_l).ellipse(sc(80, 120, 300, 520), fill=(255, 220, 255, 120))
    im.alpha_composite(glow_l.filter(ImageFilter.GaussianBlur(20 * S)))
    d = ImageDraw.Draw(im)
    cx = 190
    pele, cabelo, cabelo_l = (196, 140, 110, 255), (250, 240, 214, 255), (255, 255, 255, 255)
    vest, vest_l = (230, 40, 140, 255), (255, 140, 200, 255)
    d.ellipse(sc(cx - 90, 120, cx + 90, 300), fill=cabelo)
    for k in range(12):
        a = math.radians(-180 + k * 16)
        x, y = cx + 80 * math.cos(a), 220 + 80 * math.sin(a)
        d.arc(sc(x - 14, y - 14, x + 14, y + 14), 160, 380, fill=cabelo_l, width=3 * S)
    d.polygon(sc(cx - 40, 300, cx + 40, 300, cx + 70, 520, cx + 30, 540, cx - 30, 540, cx - 70, 520), fill=vest)
    for _ in range(70):
        x = cx + rng.uniform(-60, 60); y = rng.uniform(310, 530)
        d.ellipse(sc(x - 2, y - 2, x + 2, y + 2), fill=vest_l if rng.random() < 0.6 else (255, 255, 255, 255))
    d.rectangle(sc(cx - 14, 270, cx + 14, 300), fill=pele)
    d.ellipse(sc(cx - 40, 190, cx + 40, 290), fill=pele)
    for ex in (cx - 16, cx + 16):
        d.ellipse(sc(ex - 10, 226, ex + 10, 240), fill=(176, 104, 220, 255))
        d.ellipse(sc(ex - 6, 232, ex + 6, 244), fill=(40, 20, 20, 255))
        for k in (-8, -3, 2, 7):
            d.line(sc(ex + k, 232, ex + k * 1.5, 222), fill=(20, 10, 10, 255), width=2 * S)
    d.ellipse(sc(cx - 12, 262, cx + 12, 274), fill=(220, 30, 80, 255))
    d.polygon(sc(cx - 30, 190, cx - 20, 170, cx - 8, 186, cx, 160, cx + 8, 186, cx + 20, 170, cx + 30, 190), fill=(255, 220, 80, 255))
    d.line(sc(cx + 40, 330, cx + 110, 210), fill=(240, 220, 120, 255), width=5 * S)
    star4(d, (cx + 112) * S, 204 * S, 30 * S, (255, 236, 120, 255))
    star4(d, (cx + 112) * S, 204 * S, 14 * S, (255, 255, 255, 255))
    for sgn in (-1, 1):
        d.polygon(sc(cx + sgn * 30, 540, cx + sgn * 40, 540, cx + sgn * 46, 560, cx + sgn * 26, 560), fill=(200, 160, 236, 255))
    for (x, y) in ((60, 110), (320, 130), (50, 420), (330, 450), (80, 260)):
        star4(d, x * S, y * S, 9 * S, (255, 255, 255, 255))
    for k in range(3):
        d.line(sc(cx - 120, 400 + k * 30, cx - 70, 380 + k * 30), fill=(255, 240, 120, 255), width=4 * S)


# ================================================================ outros
def make_cards():
    gold = (246, 208, 110, 255); pink = (250, 214, 230, 255)
    G1.card(PIC + 'Capitulo4.png', [
        (220, 'Capítulo 4', font('georgiab.ttf', 64), gold),
        (350, 'Gloriosa Saborosa', font('georgiai.ttf', 40), pink),
    ])
    G1.card(PIC + 'FimCapitulo4.png', [
        (220, 'Fim do Capítulo 4', font('georgiab.ttf', 58), gold),
        (350, 'A lua cheia chega em dois dias...', font('georgiai.ttf', 30), pink),
    ])


def make_mapa():
    W, H = 760, 520
    rng = random.Random(40)
    base = grad(W, H, (236, 214, 170), (214, 186, 136))
    n = G.value_noise(W, H, 4, 4, 41)
    arr = np.array(base).astype(float)
    for i in range(3):
        arr[..., i] *= 0.88 + 0.16 * n
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA')
    d = ImageDraw.Draw(im)
    mar = (150, 190, 200, 255)
    d.rectangle((20, 20, W - 20, H - 20), fill=(180, 206, 206, 255))
    for k in range(60):
        x, y = rng.randint(30, W - 30), rng.randint(30, H - 30)
        d.arc((x - 10, y - 4, x + 10, y + 4), 200, 340, fill=(150, 180, 186, 255))
    norte = [(60, 70), (200, 40), (380, 60), (520, 50), (600, 90), (620, 160), (560, 210), (400, 200), (240, 220), (90, 190)]
    sul = [(70, 330), (220, 300), (380, 320), (540, 300), (600, 340), (600, 440), (450, 480), (260, 470), (100, 450)]
    for poly, cor in ((norte, (196, 176, 120, 255)), (sul, (170, 196, 120, 255))):
        d.polygon(poly, fill=cor)
        d.line(poly + [poly[0]], fill=(110, 90, 60, 255), width=3)
    ponte = [(560, 200), (640, 180), (700, 230), (700, 300), (640, 340), (590, 320), (630, 270)]
    d.polygon(ponte, fill=(70, 130, 70, 255))
    d.line(ponte + [ponte[0]], fill=(40, 80, 40, 255), width=3)
    for _ in range(46):
        x = rng.randint(600, 690); y = rng.randint(200, 320)
        if d.im.getpixel((x, y))[:3] == (70, 130, 70):
            d.polygon([(x - 6, y + 6), (x, y - 8), (x + 6, y + 6)], fill=(30, 80, 40, 255))
    f = font('georgiab.ttf', 20); fi = font('georgiai.ttf', 18); ft = font('georgiab.ttf', 30)
    d.text((150, 110), 'Sodoma de Calvice', font=fi, fill=(90, 60, 30, 255))
    d.text((170, 380), 'Gordura do Amor', font=fi, fill=(70, 80, 30, 255))
    for (x, y, nome) in ((140, 420, 'Recife'), (330, 360, 'São Matheos'), (470, 370, 'Morro do Macaco')):
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(160, 40, 40, 255))
        d.text((x + 8, y - 10), nome, font=f, fill=(60, 40, 30, 255))
    d.rectangle((300, 120, 330, 150), fill=(90, 50, 110, 255)); d.polygon([(296, 120), (315, 100), (334, 120)], fill=(60, 30, 80, 255))
    d.text((340, 120), 'Mansão do Raulete', font=f, fill=(70, 30, 80, 255))
    caminho = [(470, 370), (520, 340), (580, 330), (630, 300), (650, 260)]
    for k in range(len(caminho) - 1):
        (x0, y0), (x1, y1) = caminho[k], caminho[k + 1]
        for t in np.linspace(0, 1, 6, endpoint=False):
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(190, 40, 40, 255))
    glow(im, (610, 220, 700, 300), (255, 220, 90, 200), 12)
    d = ImageDraw.Draw(im)
    star4(d, 650, 260, 14, (255, 236, 120, 255)); star4(d, 650, 260, 6, (255, 255, 255, 255))
    d.text((560, 140), 'Floresta', font=f, fill=(30, 70, 30, 255)); d.text((560, 160), 'de Mauara', font=f, fill=(30, 70, 30, 255))
    cx, cy = 90, 270
    for a, comp in ((0, 30), (90, 30), (180, 30), (270, 30)):
        r = math.radians(a)
        d.polygon([(cx + comp * math.cos(r), cy + comp * math.sin(r)), (cx + 6 * math.cos(r + 1.57), cy + 6 * math.sin(r + 1.57)),
                   (cx + 6 * math.cos(r - 1.57), cy + 6 * math.sin(r - 1.57))], fill=(120, 60, 40, 255))
    d.text((cx - 6, cy - 54), 'N', font=f, fill=(120, 60, 40, 255))
    w = d.textlength('O caminho para o leste', font=ft)
    d.text(((W - w) / 2, H - 70), 'O caminho para o leste', font=ft, fill=(90, 50, 30, 255))
    vin = Image.new('L', im.size, 0); ImageDraw.Draw(vin).rounded_rectangle((10, 10, W - 10, H - 10), 30, fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(18))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), vin)
    sh = Image.new('RGBA', (W + 40, H + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((16, 20, W + 24, H + 24), 30, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); sh.alpha_composite(out, (20, 20))
    sh.save(PIC + 'Mapa_Mauara.png')
    prev(sh, 'Mapa_Mauara')


def make_meia_peruca():
    src = Image.open(PIC + 'Peruca_Ouro.png').convert('RGBA')
    W, H = src.size
    mask = Image.new('L', src.size, 0); md = ImageDraw.Draw(mask)
    pts = [(0, 0), (W // 2 + 6, 0)]
    rng = random.Random(3)
    for y in range(10, H, 14):
        pts.append((W // 2 + rng.randint(-10, 10), y))
    pts += [(W // 2, H), (0, H)]
    md.polygon(pts, fill=255)
    out = Image.new('RGBA', src.size, (0, 0, 0, 0)); out.paste(src, (0, 0), mask)
    out = out.crop(out.getbbox())
    pad = Image.new('RGBA', (out.width + 60, out.height + 40), (0, 0, 0, 0)); pad.alpha_composite(out, (30, 20))
    pad.save(PIC + 'Item_Peruca_Metade.png')
    prev(pad, 'Item_Peruca_Metade', 1)


def main():
    make_cards()
    make_mapa()
    carta('Carta_Vidente_Calva', 'A VIDENTE CALVA', 'XXIV', des_vidente)
    carta('Carta_Sapo_Sacudo', 'O SAPO SACUDO', 'XXV', des_sapo, fundo=((20, 60, 50), (40, 110, 90)))
    carta('Carta_Traveco', 'O TRAVECO', 'XXVI', des_traveco, fundo=((70, 20, 70), (130, 50, 120)))
    for k, f in enumerate([h1_divilandia, h2_vera_prime, h3_batalha, h4_paz, h5_araujo, h6_golpe, h7_fuga, h8_linhagem], 1):
        moldura(f(), f'Historia_{k}')
    moldura(flashback(), 'Lembranca_Ponte', sepia=True)
    make_meia_peruca()
    make_final()
    cut_in('CutIn_Baratelli', busto_baratelli('det', False), 'POTENCIAL LATENTE!', 'Carta do Traveco: velocidade de Umamusume!',
           (255, 110, 170), (120, 60, 220), 'esq')
    cut_in('CutIn_Leona', busto_leona(), 'RELÂMPAGO SOMBRIO!', 'Leona: "Ninguém me alcança!"',
           (60, 20, 80), (20, 10, 30), 'dir')
    print('ok')


if __name__ == '__main__':
    main()
