# Capitulo 2: imagens de cena, inimigo de batalha, rio (parallax) e tiles extras.
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, PROJ
import gen_ch1_assets as G1

G.PREV = HERE + '/prev/'
FONTS = 'C:/Windows/Fonts/'


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def save_prev(im, name, scale=1, bg=(60, 60, 70, 255)):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im)
    if scale != 1:
        b = b.resize((int(im.width * scale), int(im.height * scale)), Image.NEAREST if scale > 1 else Image.LANCZOS)
    b.save(G.PREV + name)


def tile_pos(n):
    return (((n // 128) % 2) * 8 + n % 8) * 48, ((n % 128) // 8) * 48


# ================================================================ cartoes de capitulo
def make_cards():
    gold = (246, 208, 110, 255); pink = (250, 214, 230, 255)
    G1.card(PROJ + '/img/pictures/Capitulo2.png', [
        (220, 'Capítulo 2', G1.font('georgiab.ttf', 64), gold),
        (350, 'Calvícies e Esfolamentos', G1.font('georgiai.ttf', 36), pink),
    ])
    G1.card(PROJ + '/img/pictures/FimCapitulo2.png', [
        (220, 'Fim do Capítulo 2', G1.font('georgiab.ttf', 58), gold),
        (350, 'O faro da Peruca de Ouro foi despertado...', G1.font('georgiai.ttf', 28), pink),
    ])


# ================================================================ Kura (inimigo, visao frontal)
def make_kura_battler():
    S = 2
    W, H = 340, 440
    im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    aura = Image.new('RGBA', im.size, (0, 0, 0, 0)); ad = ImageDraw.Draw(aura)
    ad.ellipse((40 * S, 40 * S, 300 * S, 430 * S), fill=(110, 40, 160, 120))
    aura = aura.filter(ImageFilter.GaussianBlur(28 * S))
    im.alpha_composite(aura)
    d = ImageDraw.Draw(im)
    cl, cl_l, cl_d = (30, 22, 42, 255), (66, 46, 92, 255), (14, 10, 22, 255)
    rng = random.Random(5)
    # corpo do manto com barra rasgada
    body = [(118, 120), (222, 120), (270, 300), (300, 410)]
    pts = [(118 * S, 120 * S), (222 * S, 120 * S), (262 * S, 260 * S), (300 * S, 405 * S)]
    x = 300
    while x > 40:
        nx = x - rng.randint(14, 26)
        pts.append(((x + nx) // 2 * S, (405 + rng.randint(12, 34)) * S))
        pts.append((nx * S, (400 - rng.randint(0, 8)) * S))
        x = nx
    pts += [(40 * S, 405 * S), (78 * S, 260 * S)]
    d.polygon(pts, fill=cl)
    for fx, top in ((130, 150), (170, 140), (210, 150), (245, 230), (100, 230)):
        d.line((fx * S, top * S, (fx + (fx - 170) // 3) * S, 400 * S), fill=cl_d, width=4 * S)
    d.line((122 * S, 130 * S, 70 * S, 380 * S), fill=cl_l, width=3 * S)
    # mangas abertas com garras
    for side in (-1, 1):
        cx = 170 + side * 70
        sl = [(170 + side * 40, 140), (170 + side * 120, 200), (170 + side * 140, 270), (170 + side * 100, 280), (170 + side * 60, 200)]
        d.polygon([(a * S, b * S) for a, b in sl], fill=cl_l)
        hx, hy = 170 + side * 128, 278
        for k in range(4):
            ang = math.radians(90 + side * (-30 + k * 18))
            d.line((hx * S, hy * S, (hx + math.cos(ang) * 34) * S, (hy + math.sin(ang) * 40) * S),
                   fill=(150, 130, 170, 255), width=5 * S)
            d.line(((hx + math.cos(ang) * 34) * S, (hy + math.sin(ang) * 40) * S,
                    (hx + math.cos(ang) * 40) * S, (hy + math.sin(ang) * 50) * S), fill=(220, 210, 230, 255), width=3 * S)
    # capuz
    d.ellipse((100 * S, 20 * S, 240 * S, 170 * S), fill=cl)
    d.polygon([(170 * S, 6 * S), (196 * S, 34 * S), (144 * S, 34 * S)], fill=cl)
    d.arc((100 * S, 20 * S, 240 * S, 170 * S), 200, 340, fill=cl_l, width=4 * S)
    d.ellipse((122 * S, 56 * S, 218 * S, 158 * S), fill=(4, 2, 8, 255))
    glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for ex in (148, 192):
        gd.ellipse(((ex - 22) * S, 90 * S, (ex + 22) * S, 124 * S), fill=(255, 30, 60, 200))
    glow = glow.filter(ImageFilter.GaussianBlur(9 * S))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    for ex, sgn in ((148, 1), (192, -1)):
        d.polygon([((ex - 14) * S, (104 - 4 * sgn) * S), ((ex + 14) * S, (104 + 4 * sgn) * S),
                   ((ex + 10) * S, 114 * S), ((ex - 10) * S, 114 * S)], fill=(255, 50, 70, 255))
        d.line(((ex - 8) * S, 106 * S, (ex + 6) * S, 106 * S), fill=(255, 210, 210, 255), width=2 * S)
    # fumaca na base
    smoke = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(smoke)
    for _ in range(26):
        cx = rng.randint(50, 290); cy = rng.randint(380, 430); r = rng.randint(14, 34)
        sd.ellipse(((cx - r) * S, (cy - r // 2) * S, (cx + r) * S, (cy + r // 2) * S), fill=(40, 20, 60, 150))
    smoke = smoke.filter(ImageFilter.GaussianBlur(8 * S))
    im.alpha_composite(smoke)
    im = im.resize((W, H), Image.LANCZOS)
    im.save(PROJ + '/img/enemies/Kura.png')
    save_prev(im, 'kura_battler.png', 0.6, bg=(80, 70, 90, 255))


# ================================================================ mural da maldicao
def relief(stone, fig, shadow=(70, 50, 34), light=(232, 214, 176)):
    a = fig.split()[3]
    sh = Image.new('RGBA', stone.size, shadow + (0,)); sh.putalpha(a.point(lambda v: int(v * 0.75)))
    hl = Image.new('RGBA', stone.size, light + (0,)); hl.putalpha(a.point(lambda v: int(v * 0.6)))
    out = stone.copy()
    out.alpha_composite(hl, (-1, -1))
    out.alpha_composite(sh, (2, 2))
    out.alpha_composite(fig)
    return out


def make_mural():
    W, H = 760, 430
    n = G.value_noise(W, H, 6, 5, 77)
    base = np.array([190, 164, 122], dtype=float)
    arr = np.clip(base[None, None, :] + (n[..., None] - 0.5) * 80, 0, 255)
    grain = np.random.default_rng(3).integers(-12, 13, (H, W, 1))
    arr = np.clip(arr + grain, 0, 255).astype(np.uint8)
    stone = Image.fromarray(arr, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(stone)
    rng = random.Random(9)
    for _ in range(14):
        x, y = rng.randint(0, W), rng.randint(0, H)
        pts = [(x, y)]
        for k in range(rng.randint(4, 9)):
            x += rng.randint(-18, 18); y += rng.randint(-14, 14); pts.append((x, y))
        d.line(pts, fill=(118, 96, 70, 255), width=1)
    fig = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f = ImageDraw.Draw(fig)
    ink = (84, 58, 38, 255)
    # moldura e divisorias
    f.rectangle((10, 10, W - 11, H - 11), outline=ink, width=4)
    f.rectangle((20, 20, W - 21, H - 21), outline=ink, width=2)
    for x in (258, 502):
        f.line((x, 20, x, H - 21), fill=ink, width=3); f.line((x + 6, 20, x + 6, H - 21), fill=ink, width=1)
    numf = font('georgiab.ttf', 30)
    for cx, txt in ((139, 'I'), (383, 'II'), (626, 'III')):
        w = f.textlength(txt, font=numf)
        f.text((cx - w / 2, 30), txt, font=numf, fill=ink)
    PURP = (120, 70, 140, 235); SK = (226, 186, 150, 235); GOLDC = (226, 178, 60, 240); BLUE = (90, 120, 170, 230)
    BROWN = (130, 86, 52, 235); DARK = (46, 32, 54, 240); RED = (176, 40, 40, 240)
    # ---- painel I: o eclipse da maldicao e o bebe careca
    f.ellipse((97, 72, 181, 156), fill=RED)
    f.ellipse((105, 80, 173, 148), fill=DARK)
    for (cx, cy, r) in ((60, 110, 16), (214, 104, 14), (196, 168, 10)):
        for k in range(3):
            f.arc((cx - r + k * 4, cy - r + k * 4, cx + r - k * 4, cy + r - k * 4), 30 + k * 60, 300 + k * 20, fill=PURP, width=3)
    f.polygon([(58, 330), (112, 330), (104, 226), (66, 226)], fill=PURP)
    f.ellipse((64, 186, 106, 228), fill=SK)
    f.arc((70, 190, 96, 210), 200, 300, fill=(255, 245, 230, 255), width=3)
    f.line((68, 238, 44, 196), fill=SK, width=7); f.line((102, 238, 124, 196), fill=SK, width=7)
    f.line((78, 206, 84, 206), fill=ink, width=2); f.line((90, 206, 96, 206), fill=ink, width=2)
    f.arc((78, 214, 94, 226), 200, 340, fill=ink, width=2)
    f.polygon([(98, 210), (101, 218), (95, 218)], fill=(140, 190, 230, 240))
    f.rectangle((126, 292, 226, 324), fill=BROWN)
    for x in (132, 220):
        f.rectangle((x - 3, 324, x + 3, 350), fill=BROWN)
    for x in range(132, 222, 12):
        f.line((x, 270, x, 292), fill=BROWN, width=3)
    f.line((126, 270, 226, 270), fill=BROWN, width=4)
    f.ellipse((152, 262, 186, 296), fill=SK)
    f.arc((158, 266, 176, 280), 200, 300, fill=(255, 245, 230, 255), width=2)
    f.rectangle((150, 290, 200, 306), fill=BLUE)
    f.line((162, 278, 166, 278), fill=ink, width=2); f.line((172, 278, 176, 278), fill=ink, width=2)
    f.ellipse((166, 284, 172, 290), fill=ink)
    # ---- painel II: a peruca que apodrece
    f.polygon([(330, 360), (436, 360), (416, 216), (350, 216)], fill=PURP)
    f.line((352, 230, 318, 300), fill=PURP, width=12); f.line((414, 230, 448, 300), fill=PURP, width=12)
    f.ellipse((346, 140, 420, 214), fill=SK)
    f.ellipse((338, 116, 428, 168), fill=GOLDC)
    for (x0, y0) in ((340, 150), (414, 152), (356, 160), (402, 164)):
        f.polygon([(x0, y0), (x0 + 8, y0 + 4), (x0 + 3, y0 + 14)], fill=(150, 120, 70, 240))
    rng2 = random.Random(2)
    for _ in range(26):
        x = rng2.randint(330, 440); y = rng2.randint(172, 340)
        f.polygon([(x, y), (x + 6, y + 2), (x + 2, y + 8)], fill=GOLDC)
    f.ellipse((392, 168, 412, 188), outline=GOLDC, width=3)
    f.line((364, 176, 372, 176), fill=ink, width=2); f.line((396, 178, 404, 178), fill=ink, width=2)
    f.arc((370, 186, 398, 204), 200, 340, fill=ink, width=3)
    hx, hy = 462, 110
    f.polygon([(hx - 18, hy - 30), (hx + 18, hy - 30), (hx, hy)], fill=BROWN)
    f.polygon([(hx - 18, hy + 30), (hx + 18, hy + 30), (hx, hy)], fill=BROWN)
    f.polygon([(hx - 8, hy + 30), (hx + 8, hy + 30), (hx, hy + 14)], fill=GOLDC)
    f.line((hx - 22, hy - 32, hx + 22, hy - 32), fill=ink, width=3); f.line((hx - 22, hy + 32, hx + 22, hy + 32), fill=ink, width=3)
    for k in range(5):
        f.ellipse((290 + k * 30, 372 + (k % 2) * 6, 312 + k * 30, 386 + (k % 2) * 6), fill=(160, 140, 100, 200))
    # ---- painel III: o roubo dos cabelos
    f.ellipse((660, 70, 720, 130), fill=(236, 226, 190, 230))
    f.ellipse((672, 64, 732, 124), fill=(0, 0, 0, 0))
    f.polygon([(540, 360), (620, 360), (606, 200), (556, 200)], fill=DARK)
    f.ellipse((550, 140, 612, 210), fill=DARK)
    f.ellipse((562, 158, 600, 200), fill=(10, 6, 14, 250))
    f.ellipse((568, 174, 576, 180), fill=RED); f.ellipse((586, 174, 594, 180), fill=RED)
    f.line((604, 236, 640, 250), fill=DARK, width=10)
    f.polygon([(690, 360), (722, 360), (716, 280), (696, 280)], fill=(196, 186, 160, 235))
    f.ellipse((688, 244, 724, 282), fill=SK)
    ribbon = []
    for k in range(40):
        t = k / 39
        x = 690 - t * 46
        y = 262 - math.sin(t * math.pi) * 34 + t * 2
        ribbon.append((x, y))
    for w, col in ((12, GOLDC), (5, (250, 222, 120, 240))):
        f.line(ribbon, fill=col, width=w, joint='curve')
    for k in range(4):
        x = 652 - k * 4; f.line((x, 250 + k * 3, 640, 252), fill=GOLDC, width=3)
    for (cx, cy) in ((540, 120), (612, 112)):
        f.arc((cx - 12, cy - 12, cx + 12, cy + 12), 0, 270, fill=PURP, width=3)
    # desgaste
    a = np.array(fig.split()[3]).astype(float)
    er = G.value_noise(W, H, 12, 3, 41)
    a *= np.clip((er - 0.18) / 0.35, 0.35, 1.0)
    fig.putalpha(Image.fromarray(a.astype(np.uint8)))
    out = relief(stone, fig)
    vign = Image.new('L', (W, H), 0); vd = ImageDraw.Draw(vign)
    vd.rectangle((0, 0, W, H), fill=90); vd.rectangle((30, 30, W - 30, H - 30), fill=0)
    vign = vign.filter(ImageFilter.GaussianBlur(24))
    dark = Image.new('RGBA', (W, H), (30, 20, 12, 255)); dark.putalpha(vign)
    out.alpha_composite(dark)
    out.save(PROJ + '/img/pictures/Mural_Raulete.png')
    save_prev(out, 'mural.png', 1)


# ================================================================ papeis com as letras da senha
def make_papers():
    for letter, pos in (('H', 1), ('A', 2), ('I', 3), ('R', 4)):
        W, H = 340, 420
        n = G.value_noise(W, H, 5, 4, 10 + pos)
        base = np.array([246, 238, 214], dtype=float)
        arr = np.clip(base[None, None, :] + (n[..., None] - 0.5) * 30, 0, 255).astype(np.uint8)
        im = Image.fromarray(arr, 'RGB').convert('RGBA')
        d = ImageDraw.Draw(im)
        d.polygon([(W - 46, 0), (W, 0), (W, 46)], fill=(0, 0, 0, 0))
        d.polygon([(W - 46, 0), (W - 46, 46), (W, 46)], fill=(214, 204, 178, 255))
        d.rectangle((0, 0, W - 1, H - 1), outline=(190, 178, 150, 255), width=2)
        hf = font('georgiab.ttf', 22); sf = font('georgiai.ttf', 16)
        t = 'LABORATÓRIO RAULETE'; w = d.textlength(t, font=hf)
        d.text(((W - w) / 2, 22), t, font=hf, fill=(70, 50, 90, 255))
        t = f'Memorando interno  •  nº 0{pos}'; w = d.textlength(t, font=sf)
        d.text(((W - w) / 2, 54), t, font=sf, fill=(90, 80, 70, 255))
        d.line((30, 82, W - 30, 82), fill=(150, 130, 110, 255), width=2)
        bf = font('georgiab.ttf', 190)
        bb = d.textbbox((0, 0), letter, font=bf)
        lw, lh = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((W - lw) / 2 - bb[0] + 3, 108 - bb[1] + 3), letter, font=bf, fill=(120, 30, 30, 90))
        d.text(((W - lw) / 2 - bb[0], 108 - bb[1]), letter, font=bf, fill=(186, 28, 40, 255))
        pf = font('georgia.ttf', 28)
        t = f'Letra {pos} de 4'; w = d.textlength(t, font=pf)
        d.text(((W - w) / 2, 290), t, font=pf, fill=(60, 50, 50, 255))
        stamp = Image.new('RGBA', (196, 50), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
        sd.rectangle((2, 2, 193, 47), outline=(196, 40, 50, 200), width=4)
        stf = font('georgiab.ttf', 22); t = 'CONFIDENCIAL'; w = sd.textlength(t, font=stf)
        sd.text(((196 - w) / 2, 11), t, font=stf, fill=(196, 40, 50, 200))
        stamp = stamp.rotate(8, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(stamp, (W - stamp.width - 12, H - stamp.height - 6))
        ring = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
        cx, cy = (60, 370) if pos % 2 else (270, 140)
        rd.arc((cx - 34, cy - 34, cx + 34, cy + 34), 20, 320, fill=(150, 100, 50, 70), width=5)
        im.alpha_composite(ring.filter(ImageFilter.GaussianBlur(1)))
        sh = Image.new('RGBA', (W + 16, H + 16), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((8, 10, W + 8, H + 10), fill=(0, 0, 0, 110))
        sh = sh.filter(ImageFilter.GaussianBlur(5))
        sh.alpha_composite(im, (4, 2))
        sh.save(PROJ + f'/img/pictures/Papel_{letter}.png')
        if pos == 1:
            save_prev(sh, 'papel.png', 0.7)


# ================================================================ rio rapido (parallax ancorado ao mapa)
def aniso_noise(W, H, gx, gy, seed):
    """Ruido de valor periodico (emenda perfeita nas bordas), com celulas de W/gx por H/gy."""
    rng = np.random.default_rng(seed)
    g = rng.random((gy, gx))
    xs = np.arange(W) / (W / gx); ys = np.arange(H) / (H / gy)
    x0 = np.floor(xs).astype(int); y0 = np.floor(ys).astype(int)
    fx = xs - x0; fy = ys - y0
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    x1 = (x0 + 1) % gx; x0 = x0 % gx; y1 = (y0 + 1) % gy; y0 = y0 % gy
    a = g[np.ix_(y0, x0)]; b = g[np.ix_(y0, x1)]; c = g[np.ix_(y1, x0)]; d = g[np.ix_(y1, x1)]
    fx = fx[None, :]; fy = fy[:, None]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


def make_river():
    W, H = 384, 192
    base = 0.6 * aniso_noise(W, H, 4, 8, 51) + 0.4 * aniso_noise(W, H, 8, 16, 61)
    streak = 0.65 * aniso_noise(W, H, 3, 48, 52) + 0.35 * aniso_noise(W, H, 6, 64, 62)
    dark = aniso_noise(W, H, 4, 32, 63)
    deep = np.array([14, 46, 76]); mid = np.array([30, 96, 134]); hi = np.array([168, 222, 236])
    t = base[..., None]
    col = deep * (1 - t) + mid * t
    s = np.clip((streak - 0.60) / 0.10, 0, 1)[..., None]
    col = col * (1 - s * 0.7) + hi * s * 0.7
    dk = np.clip((dark - 0.62) / 0.12, 0, 1)[..., None]
    col = col * (1 - dk * 0.35)
    y = np.arange(H)[:, None, None]
    col = col * (1 - np.clip(1 - y / 22.0, 0, 1) * 0.6)
    foam_n = aniso_noise(W, 24, 12, 6, 53)
    foam = np.zeros((H, W))
    foam[H - 24:, :] = np.clip((foam_n - 0.42) / 0.18, 0, 1) * np.linspace(0.15, 1, 24)[:, None]
    foam = foam[..., None]
    col = col * (1 - foam * 0.85) + np.array([226, 240, 244]) * foam * 0.85
    img = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), 'RGB')
    img.save(PROJ + '/img/parallaxes/!Correnteza.png')
    big = Image.new('RGB', (W * 2, H), (0, 0, 0)); big.paste(img, (0, 0)); big.paste(img, (W, 0))
    big.save(G.PREV + 'rio.png')


# ================================================================ folha D do calabouco (ponte larga, pedras no rio)
WOOD = [(150, 104, 62), (164, 116, 70), (140, 96, 56), (158, 110, 66), (146, 100, 60), (166, 120, 74)]


def plank_tile(kind, rng):
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    for b in range(6):
        y0 = b * 8
        c = WOOD[b]
        d.rectangle((0, y0, 47, y0 + 7), fill=c + (255,))
        d.line((0, y0, 47, y0), fill=tuple(min(255, v + 26) for v in c) + (255,))
        d.line((0, y0 + 7, 47, y0 + 7), fill=(64, 42, 24, 255))
        for _ in range(5):
            gx = rng.randint(0, 40); gy = y0 + rng.randint(2, 5)
            d.line((gx, gy, gx + rng.randint(4, 9), gy), fill=tuple(v - 22 for v in c) + (255,))
    if kind in ('L', 'R'):
        bx = 0 if kind == 'L' else 40
        d.rectangle((bx, 0, bx + 7, 47), fill=(96, 62, 34, 255))
        d.line((bx + (7 if kind == 'L' else 0), 0, bx + (7 if kind == 'L' else 0), 47), fill=(56, 36, 20, 255))
        d.line((bx + (1 if kind == 'L' else 6), 0, bx + (1 if kind == 'L' else 6), 47), fill=(128, 88, 52, 255))
        for b in range(6):
            cx = bx + 3 if kind == 'L' else bx + 4
            d.rectangle((cx - 1, b * 8 + 3, cx + 1, b * 8 + 5), fill=(170, 170, 176, 255))
            d.point((cx - 1, b * 8 + 3), fill=(230, 230, 236, 255))
        px = bx + (8 if kind == 'L' else -2)
        for b in range(6):
            d.point((px if kind == 'L' else bx - 1, b * 8 + 4), fill=(60, 60, 64, 255))
    return t


def rock_tile(seed, big=True):
    rng = random.Random(seed)
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    foam = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); fd = ImageDraw.Draw(foam)
    fd.ellipse((4, 12, 34, 40), fill=(236, 246, 250, 170))
    for k in range(6):
        fd.line((30 + k * 2, 20 + k * 2, 47, 22 + k * 2), fill=(236, 246, 250, 120), width=2)
    foam = foam.filter(ImageFilter.GaussianBlur(1.2))
    t.alpha_composite(foam)
    d = ImageDraw.Draw(t)
    r = 13 if big else 9
    cx, cy = 20, 26
    d.ellipse((cx - r, cy - r + 2, cx + r, cy + r - 1), fill=(96, 96, 104, 255))
    d.ellipse((cx - r + 3, cy - r + 3, cx + r - 5, cy + r - 6), fill=(128, 128, 136, 255))
    d.ellipse((cx - r + 6, cy - r + 5, cx - 1, cy - 2), fill=(160, 160, 170, 255))
    d.arc((cx - r, cy - r + 2, cx + r, cy + r - 1), 10, 170, fill=(60, 60, 68, 255), width=2)
    return outline(t, C(40, 40, 48)) if False else t


def make_dungeon_d():
    sheet = Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    rng = random.Random(4)
    for n, kind in ((0, 'L'), (1, 'M'), (2, 'R')):
        sheet.alpha_composite(plank_tile(kind, random.Random(10 + n)), tile_pos(n))
    sheet.alpha_composite(rock_tile(1, True), tile_pos(3))
    sheet.alpha_composite(rock_tile(2, False), tile_pos(4))
    sheet.save(PROJ + '/img/tilesets/Calabouco_D.png')
    pv = Image.new('RGBA', (48 * 5, 48 * 2), (30, 80, 120, 255))
    for i in range(5):
        x, y = tile_pos(i)
        pv.alpha_composite(sheet.crop((x, y, x + 48, y + 48)), (i * 48, 0))
    for i, n in enumerate((0, 1, 1, 2)):
        x, y = tile_pos(n)
        pv.alpha_composite(sheet.crop((x, y, x + 48, y + 48)), (i * 48, 48))
    pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(G.PREV + 'calabouco_d.png')


# ================================================================ folha D do laboratorio (perucas, tubos, cartaz)
def wig_head(hair, hair_l, hair_d, style):
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((22, 30, 25, 43), fill=(150, 150, 160, 255))
    d.ellipse((14, 41, 34, 47), fill=(110, 110, 120, 255))
    if style == 'long':
        d.polygon([(12, 12), (36, 12), (38, 36), (34, 39), (14, 39), (10, 36)], fill=hair_d)
    d.ellipse((15, 8, 33, 30), fill=(228, 224, 216, 255))
    d.ellipse((13, 4, 35, 22), fill=hair)
    if style == 'curly':
        for (x, y) in ((12, 14), (34, 14), (12, 22), (35, 22), (16, 6), (30, 6), (23, 3)):
            d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=hair)
            d.arc((x - 3, y - 3, x + 3, y + 3), 200, 340, fill=hair_l)
    else:
        d.polygon([(12, 10), (16, 10), (16, 32), (13, 34), (11, 28)], fill=hair)
        d.polygon([(36, 10), (32, 10), (32, 32), (35, 34), (37, 28)], fill=hair)
        d.line((14, 12, 14, 30), fill=hair_l); d.line((34, 12, 34, 30), fill=hair_l)
    d.arc((17, 5, 31, 14), 200, 330, fill=hair_l)
    return outline(t, C(40, 34, 40))


def hair_tube(hair, liquid):
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((13, 40, 35, 46), fill=(90, 96, 110, 255)); d.rectangle((13, 2, 35, 7), fill=(90, 96, 110, 255))
    d.rectangle((15, 7, 33, 40), fill=liquid)
    for k in range(5):
        x = 18 + k * 3
        d.line([(x, 34), (x + 2, 26), (x - 1, 18), (x + 2, 11)], fill=hair, width=2)
    d.line((16, 8, 16, 39), fill=(255, 255, 255, 160))
    d.rectangle((15, 7, 33, 40), outline=(200, 230, 240, 200))
    for (x, y) in ((28, 30), (24, 20), (30, 14)):
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(240, 255, 255, 200))
    return outline(t, C(30, 30, 40))


def poster_tile():
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((8, 4, 40, 44), fill=(60, 30, 80, 255)); d.rectangle((8, 4, 40, 44), outline=(236, 196, 86, 255), width=2)
    d.ellipse((16, 10, 32, 28), fill=(240, 202, 170, 255))
    d.arc((18, 11, 26, 18), 190, 290, fill=(255, 245, 230, 255), width=2)
    d.ellipse((25, 17, 30, 22), outline=(236, 196, 86, 255))
    d.line((20, 24, 28, 24), fill=(70, 46, 30, 255))
    d.polygon([(14, 30), (34, 30), (36, 40), (12, 40)], fill=(92, 42, 124, 255))
    d.text((19, 30), 'R', fill=(236, 196, 86, 255))
    return outline(t, C(30, 20, 30))


def floor_hair():
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    rng = random.Random(8)
    cols = [(250, 214, 96, 220), (40, 34, 50, 220), (160, 90, 50, 220)]
    for _ in range(9):
        x = rng.randint(6, 40); y = rng.randint(8, 42)
        pts = [(x, y)]
        for k in range(4):
            x += rng.randint(-4, 6); y += rng.randint(-3, 3); pts.append((x, y))
        d.line(pts, fill=rng.choice(cols), width=1)
    return t


def make_lab_d():
    sheet = Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    heads = [
        ((250, 214, 96, 255), (255, 240, 168, 255), (212, 164, 52, 255), 'long'),
        ((40, 34, 50, 255), (92, 82, 116, 255), (22, 18, 28, 255), 'long'),
        ((196, 70, 52, 255), (236, 120, 90, 255), (140, 44, 34, 255), 'curly'),
        ((120, 76, 44, 255), (164, 112, 70, 255), (84, 52, 30, 255), 'curly'),
    ]
    for n, (h, hl, hd, st) in enumerate(heads):
        sheet.alpha_composite(wig_head(h, hl, hd, st), tile_pos(n))
    sheet.alpha_composite(hair_tube((250, 214, 96, 255), (120, 220, 170, 170)), tile_pos(4))
    sheet.alpha_composite(hair_tube((40, 34, 50, 255), (160, 140, 230, 170)), tile_pos(5))
    sheet.alpha_composite(poster_tile(), tile_pos(6))
    sheet.alpha_composite(floor_hair(), tile_pos(7))
    sheet.save(PROJ + '/img/tilesets/Laboratorio_D.png')
    pv = Image.new('RGBA', (48 * 8, 48), (200, 205, 210, 255))
    for i in range(8):
        x, y = tile_pos(i)
        pv.alpha_composite(sheet.crop((x, y, x + 48, y + 48)), (i * 48, 0))
    pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(G.PREV + 'lab_d.png')


# ================================================================ tronco boiando no rio (objeto)
def make_log():
    frames = []
    for bob in (0, 1, 0):
        t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
        foam = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); fd = ImageDraw.Draw(foam)
        fd.ellipse((2, 24 + bob, 46, 40 + bob), fill=(230, 244, 250, 120))
        t.alpha_composite(foam.filter(ImageFilter.GaussianBlur(1.5)))
        d = ImageDraw.Draw(t)
        d.rounded_rectangle((6, 25 + bob, 42, 35 + bob), 5, fill=(110, 74, 44, 255))
        d.line((8, 27 + bob, 40, 27 + bob), fill=(146, 100, 62, 255))
        d.ellipse((38, 25 + bob, 45, 35 + bob), fill=(176, 132, 84, 255))
        d.ellipse((40, 28 + bob, 43, 32 + bob), fill=(130, 90, 54, 255))
        d.line((16, 25 + bob, 12, 20 + bob), fill=(96, 64, 38, 255), width=2)
        frames.append(outline(t, C(50, 32, 20)))
    sh = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for r in range(4):
        for c, f in enumerate(frames):
            sh.alpha_composite(f, (c * 48, r * 48))
    sh.save(PROJ + '/img/characters/!$Tronco.png')


if __name__ == '__main__':
    make_cards()
    make_kura_battler()
    make_mural()
    make_papers()
    make_river()
    make_dungeon_d()
    make_lab_d()
    make_log()
    print('ok')
