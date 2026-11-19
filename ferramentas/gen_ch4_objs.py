# Capitulo 4: objetos de evento (templo e floresta) e tiles novos (Morro_E e Templo_E).
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, PROJ
from gen_ch2_chars import blank, darker, lighter, WHITE, EYE_D
from gen_ch2_scenes import tile_pos

PREV4 = HERE + '/prev4/'
os.makedirs(PREV4, exist_ok=True)

STONE = C(206, 198, 180); STONE_L = C(232, 226, 210); STONE_D = C(150, 140, 122); STONE_DD = C(104, 96, 84)
GOLD = C(236, 196, 70); GOLD_L = C(255, 236, 150); GOLD_D = C(180, 136, 34)
TEAL = C(40, 150, 140); TEAL_L = C(100, 200, 186); TEAL_D = C(20, 96, 92)
OUTS = C(60, 52, 44)
WIGS = {
    'loira': (C(250, 214, 96), C(255, 240, 170), C(206, 160, 50)),
    'ruiva': (C(214, 84, 40), C(250, 140, 80), C(160, 50, 24)),
    'azul': (C(70, 124, 232), C(140, 180, 255), C(40, 80, 170)),
    'preta': (C(46, 38, 56), C(96, 84, 116), C(24, 20, 30)),
}


def wig(d, cx, top, cor, larg=8, alt=14):
    base, luz, esc = cor
    d.ellipse((cx - larg - 1, top, cx + larg + 1, top + 12), fill=base)
    d.polygon([(cx - larg - 1, top + 6), (cx - larg - 3, top + alt), (cx - larg + 3, top + alt + 2), (cx - larg + 3, top + 8)], fill=base)
    d.polygon([(cx + larg + 1, top + 6), (cx + larg + 3, top + alt), (cx + larg - 3, top + alt + 2), (cx + larg - 3, top + 8)], fill=base)
    for (x, y) in [(cx - 5, top + 3), (cx, top + 2), (cx + 5, top + 3), (cx - larg, top + 9), (cx + larg, top + 9),
                   (cx - larg - 1, top + 13), (cx + larg + 1, top + 13)]:
        d.arc((x - 2, y - 2, x + 2, y + 2), 180, 360, fill=luz)
    d.arc((cx - larg, top + 1, cx + larg, top + 11), 200, 340, fill=esc)


# ---------------------------------------------------------------- busto e suporte
def busto(cor=None):
    im, d = blank()
    d.rectangle((17, 32, 31, 45), fill=STONE)
    d.rectangle((15, 44, 33, 46), fill=STONE_D); d.rectangle((15, 31, 33, 33), fill=STONE_L)
    d.line((18, 34, 18, 43), fill=STONE_L); d.line((30, 34, 30, 43), fill=STONE_D)
    d.rectangle((20, 37, 28, 40), fill=GOLD); d.line((21, 38, 27, 38), fill=GOLD_D)
    d.polygon([(14, 31), (34, 31), (31, 22), (17, 22)], fill=STONE)
    d.line((17, 23, 31, 23), fill=STONE_L)
    d.rectangle((21, 18, 27, 23), fill=STONE_D)
    d.ellipse((16, 3, 32, 21), fill=STONE)
    d.arc((16, 3, 32, 21), 120, 240, fill=STONE_L)
    d.line((20, 12, 22, 12), fill=STONE_DD); d.line((26, 12, 28, 12), fill=STONE_DD)
    d.point((24, 15), fill=STONE_D); d.line((22, 18, 26, 18), fill=STONE_D)
    if cor:
        wig(d, 24, 1, WIGS[cor], larg=8, alt=15)
    return outline(im, OUTS)


WOOD = C(140, 96, 56); WOOD_L = C(180, 130, 80); WOOD_D = C(96, 62, 34)
FOAM = C(236, 214, 190); FOAM_D = C(200, 176, 150)


def suporte(cor=None):
    im, d = blank()
    d.ellipse((15, 41, 33, 46), fill=WOOD_D); d.ellipse((16, 40, 32, 44), fill=WOOD)
    d.rectangle((23, 22, 25, 42), fill=WOOD); d.line((23, 22, 23, 42), fill=WOOD_L)
    d.ellipse((17, 7, 31, 24), fill=FOAM)
    d.arc((17, 7, 31, 24), 100, 260, fill=FOAM_D)
    if cor:
        wig(d, 24, 5, WIGS[cor], larg=7, alt=14)
    return outline(im, OUTS)


# ---------------------------------------------------------------- estatua de Umamusume (empurravel)
UMA_COR = {'dourada': (C(240, 200, 80), C(190, 146, 40)), 'prata': (C(222, 226, 236), C(160, 166, 180)),
           'bronze': (C(206, 132, 72), C(150, 88, 44))}


def estatua_uma(nome, brilho=False):
    im, d = blank()
    cor, cor_d = UMA_COR[nome]
    d.rectangle((13, 38, 35, 46), fill=STONE_D); d.rectangle((13, 38, 35, 39), fill=STONE)
    d.rectangle((19, 40, 29, 44), fill=cor); d.line((20, 42, 28, 42), fill=cor_d)
    # corpo em pose de corrida (pedra) com crina e cauda na cor do metal
    d.polygon([(30, 22), (37, 26), (38, 32), (33, 30)], fill=cor)          # cauda
    d.rectangle((19, 20, 29, 30), fill=STONE)
    d.line((21, 30, 17, 37), fill=STONE, width=3); d.line((27, 30, 31, 37), fill=STONE, width=3)
    d.line((19, 22, 13, 27), fill=STONE, width=2); d.line((29, 22, 34, 18), fill=STONE, width=2)
    d.ellipse((18, 6, 30, 20), fill=STONE)
    d.polygon([(18, 9), (19, 1), (23, 7)], fill=STONE_D); d.polygon([(30, 9), (29, 1), (25, 7)], fill=STONE_D)
    d.polygon([(17, 8), (31, 8), (32, 18), (29, 12), (19, 12), (16, 18)], fill=cor)  # crina
    d.line((21, 14, 22, 14), fill=STONE_DD); d.line((26, 14, 27, 14), fill=STONE_DD)
    d.line((22, 24, 26, 24), fill=cor)
    if brilho:
        for (x, y) in [(10, 10), (38, 8), (8, 30), (40, 34)]:
            d.line((x - 2, y, x + 2, y), fill=GOLD_L); d.line((x, y - 2, x, y + 2), fill=GOLD_L)
    return outline(im, OUTS)


def alavanca(ligada):
    im, d = blank()
    d.rectangle((14, 36, 34, 45), fill=STONE_D); d.rectangle((14, 36, 34, 38), fill=STONE)
    d.rectangle((21, 33, 27, 37), fill=STONE_DD)
    ang = 35 if ligada else -35
    x2 = 24 + 16 * math.sin(math.radians(ang)); y2 = 35 - 16 * math.cos(math.radians(ang))
    d.line((24, 35, x2, y2), fill=C(110, 110, 120), width=3)
    knob = C(80, 200, 90) if ligada else C(220, 60, 60)
    d.ellipse((x2 - 4, y2 - 4, x2 + 4, y2 + 4), fill=knob)
    d.point((x2 - 1, y2 - 2), fill=WHITE)
    return outline(im, OUTS)


def chama(d, cx, base, f, s=1.0):
    hs = [14, 17, 15][f]
    d.polygon([(cx - 7 * s, base), (cx - 4 * s, base - hs * 0.6 * s), (cx - 1 * s, base - hs * s),
               (cx + 3 * s, base - hs * 0.7 * s), (cx + 7 * s, base)], fill=C(250, 120, 30))
    d.polygon([(cx - 4 * s, base), (cx - 1 * s, base - hs * 0.55 * s), (cx + 2 * s, base - hs * 0.75 * s),
               (cx + 4 * s, base)], fill=C(255, 210, 70))
    d.ellipse((cx - 2 * s, base - 5 * s, cx + 2 * s, base - 1), fill=C(255, 250, 200))


def braseiro(aceso, f=0):
    im, d = blank()
    d.rectangle((20, 34, 28, 45), fill=STONE_D); d.rectangle((16, 44, 32, 46), fill=STONE_DD)
    d.chord((12, 22, 36, 38), 0, 180, fill=STONE)
    d.rectangle((12, 28, 36, 30), fill=GOLD)
    d.ellipse((14, 26, 34, 32), fill=C(50, 34, 30))
    if aceso:
        chama(d, 24, 30, f)
    else:
        for (x, y) in [(18, 28), (23, 29), (28, 28)]:
            d.ellipse((x - 2, y - 1, x + 2, y + 1), fill=C(90, 70, 60))
    return outline(im, OUTS)


def esfinge(olhos=False, boca=0):
    im, d = blank()
    d.rectangle((8, 34, 40, 46), fill=STONE_D); d.rectangle((8, 34, 40, 36), fill=STONE)
    for x in (12, 20, 28, 36):
        d.rectangle((x - 2, 39, x + 2, 43), fill=TEAL)
    d.polygon([(6, 34), (42, 34), (38, 16), (10, 16)], fill=STONE)
    d.ellipse((11, 2, 37, 34), fill=STONE)
    d.arc((11, 2, 37, 34), 110, 250, fill=STONE_L, width=2)
    d.ellipse((7, 14, 13, 24), fill=STONE_D); d.ellipse((35, 14, 41, 24), fill=STONE_D)
    for ex in (18, 30):
        if olhos:
            d.ellipse((ex - 3, 13, ex + 3, 18), fill=GOLD_L); d.ellipse((ex - 1, 14, ex + 1, 17), fill=GOLD)
        else:
            d.line((ex - 3, 16, ex + 3, 16), fill=STONE_DD)
    d.line((24, 18, 23, 23), fill=STONE_D); d.line((23, 23, 25, 23), fill=STONE_D)
    if boca:
        d.ellipse((19, 25, 29, 25 + 3 + boca * 2), fill=C(60, 40, 40))
    else:
        d.line((20, 27, 28, 27), fill=STONE_DD)
    d.arc((15, 4, 33, 14), 200, 340, fill=WHITE)   # careca brilhando
    return outline(im, OUTS)


# ---------------------------------------------------------------- portas, armadilhas e efeitos
def porta_pedra(abertura):
    im, d = blank()
    d.rectangle((2, 0, 45, 47), fill=C(24, 18, 16))
    off = int(abertura * 44)
    if abertura < 1:
        d.rectangle((4, 2 - off, 43, 47 - off), fill=STONE)
        d.rectangle((4, 2 - off, 43, 47 - off), outline=STONE_D)
        for k in range(3):
            y = 8 + k * 13 - off
            d.rectangle((9, y, 38, y + 9), outline=TEAL_D)
            d.line((13, y + 4, 34, y + 4), fill=TEAL)
            d.point((24, y + 2), fill=GOLD); d.point((24, y + 7), fill=GOLD)
        d.ellipse((21, 21 - off, 27, 27 - off), fill=GOLD_D)
        d.rectangle((23, 25 - off, 25, 30 - off), fill=GOLD_D)
    d.rectangle((0, 0, 47, 3), fill=GOLD); d.rectangle((0, 0, 2, 47), fill=GOLD_D); d.rectangle((45, 0, 47, 47), fill=GOLD_D)
    return im


def porta_selada(f=0, brilha=False):
    im, d = blank()
    d.rectangle((0, 0, 47, 47), fill=C(40, 30, 54))
    d.rectangle((3, 3, 44, 47), fill=C(64, 50, 86))
    glow = [C(150, 110, 230), C(190, 150, 255), C(230, 200, 255)][f] if brilha else C(110, 86, 150)
    d.pieslice((14, 10, 34, 30), 90, 270, fill=glow)
    d.pieslice((19, 10, 39, 30), 90, 270, fill=C(64, 50, 86))
    for k in range(7):
        a = math.radians(-90 + k * 30 - 90)
        x, y = 24 + 17 * math.cos(a), 22 + 17 * math.sin(a)
        d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=glow)
    d.rectangle((20, 34, 28, 40), fill=C(30, 22, 40)); d.rectangle((20, 34, 28, 40), outline=glow)
    d.rectangle((0, 0, 47, 2), fill=C(110, 90, 140))
    return im


THORN = C(70, 110, 50); THORN_D = C(40, 70, 30); SPIKE = C(220, 210, 180); BERRY = C(170, 30, 60)


def espinhos(n, f=0):
    im, d = blank()
    rng = random.Random(5 + f)
    alturas = {0: 10, 1: 22, 2: 38}[n]
    for k in range(9 + n * 4):
        x = 4 + rng.random() * 40
        h = alturas * (0.6 + rng.random() * 0.4)
        sw = (f - 1) * 1.5
        d.line((x, 46, x + sw + rng.uniform(-5, 5), 46 - h), fill=THORN if k % 2 else THORN_D, width=3)
    for k in range(10 + n * 8):
        x = 4 + rng.random() * 40; y = 46 - rng.random() * alturas
        d.polygon([(x, y), (x + 3, y - 1), (x + 1, y + 2)], fill=SPIKE)
    if n == 2:
        for k in range(4):
            x = 8 + rng.random() * 32; y = 46 - rng.random() * 30
            d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=BERRY)
    return outline(im, C(24, 36, 18))


VINE = C(60, 140, 60); VINE_L = C(110, 190, 90); VINE_D = C(34, 90, 40)


def cipo(fase, f=0):
    im, d = blank()
    if fase == 0:  # escondido: um tufo de capim com um laco discreto
        for k, x in enumerate((16, 20, 24, 28, 32)):
            d.line((x, 44, x + (k - 2) * 2, 36 - (k % 2) * 3), fill=C(90, 160, 70), width=2)
        d.arc((18, 38, 30, 46), 180, 360, fill=VINE_D)
        return im
    alt = {1: [10, 18, 26], 2: [34, 38, 34], 3: [20, 10, 4]}[fase][f]
    pts = []
    for k in range(12):
        t = k / 11
        pts.append((24 + math.sin(t * 5 + f) * 6 * (1 - t * 0.3), 46 - t * alt))
    d.line(pts, fill=VINE, width=4)
    d.line(pts, fill=VINE_L, width=1)
    if fase == 2:
        x, y = pts[-1]
        d.ellipse((x - 7, y - 4, x + 7, y + 6), outline=VINE_D, width=2)
    for k in range(2, 11, 3):
        x, y = pts[k]
        d.ellipse((x - 3, y - 2, x + 2, y + 2), fill=VINE_L)
    return outline(im, C(20, 50, 20))


MUD = C(120, 92, 60); MUD_L = C(156, 124, 84); MUD_D = C(86, 62, 38)


def areia(bolha, f=0):
    im, d = blank()
    d.ellipse((2, 18, 46, 46), fill=MUD_D)
    d.ellipse((5, 20, 43, 44), fill=MUD)
    for k in range(3):
        r = 6 + k * 6
        a0 = (f * 40 + k * 70) % 360
        d.arc((24 - r, 32 - r * 0.55, 24 + r, 32 + r * 0.55), a0, a0 + 120, fill=MUD_L)
    if bolha:
        for (x, y, r) in [(16, 30, 2 + f), (30, 35, 3 - f % 2), (24, 26, 1 + f % 2)]:
            d.ellipse((x - r, y - r, x + r, y + r), outline=MUD_L)
    return im


def plataforma_portal(ativa, f=0):
    im, d = blank()
    d.ellipse((4, 24, 44, 46), fill=STONE_D); d.ellipse((6, 24, 42, 43), fill=STONE)
    d.ellipse((12, 28, 36, 40), outline=TEAL_D, width=2)
    for k in range(6):
        a = math.radians(k * 60 + f * 20)
        x, y = 24 + 15 * math.cos(a), 34 + 7 * math.sin(a)
        d.point((x, y), fill=GOLD)
    if ativa:
        glow = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        h = [26, 30, 28][f]
        gd.polygon([(12, 34), (36, 34), (32, 34 - h), (16, 34 - h)], fill=(150, 230, 255, 110))
        gd.ellipse((12, 28, 36, 40), fill=(170, 240, 255, 170))
        glow = glow.filter(ImageFilter.GaussianBlur(2))
        im.alpha_composite(glow)
        d = ImageDraw.Draw(im)
        for (x, y) in [(18, 22 - f * 3), (30, 16 + f * 2), (24, 10 + f * 4)]:
            d.point((x, y), fill=WHITE)
    return im


def brilho_dourado(f, grande=False):
    im, d = blank()
    rng = random.Random(30 + f)
    for k in range(5 if grande else 3):
        x = 10 + rng.random() * 28; y = 14 + rng.random() * 26
        r = (3 if grande else 2) + (k + f) % 2
        a = (k + f) % 3
        col = [C(255, 240, 150), C(255, 214, 80), C(255, 255, 230)][a]
        d.line((x - r, y, x + r, y), fill=col); d.line((x, y - r, x, y + r), fill=col)
        d.point((x, y), fill=WHITE)
    return im


BONE = C(236, 230, 214); BONE_D = C(190, 180, 160)


def cranio(fase, f=0):
    im, d = blank()
    if fase <= 1:
        d.ellipse((14, 18, 34, 38), fill=BONE)
        d.rectangle((18, 34, 30, 42), fill=BONE)
        d.ellipse((17, 25, 23, 31), fill=EYE_D); d.ellipse((25, 25, 31, 31), fill=EYE_D)
        d.polygon([(24, 32), (22, 36), (26, 36)], fill=EYE_D)
        for x in range(19, 30, 3):
            d.line((x, 38, x, 41), fill=BONE_D)
        d.polygon([(28, 17), (36, 13), (34, 21)], fill=C(240, 120, 170)); d.ellipse((26, 15, 31, 20), fill=C(250, 160, 190))
        if fase == 1:
            d.line((22, 18, 25, 24), fill=EYE_D); d.line((25, 24, 23, 28), fill=EYE_D)
            d.line((30, 30, 33, 36), fill=EYE_D)
        im = outline(im, C(70, 60, 50))
        return im
    rng = random.Random(9 + f)
    cor = [C(220, 210, 190), C(255, 214, 90), C(255, 240, 160)]
    for k in range(60):
        x = 24 + rng.gauss(0, 7); y = 40 + rng.gauss(0, 2.5)
        c = cor[0] if fase == 2 else cor[1 + (k + f) % 2]
        d.point((x, y), fill=c)
    if fase == 3:
        for (x, y) in [(14 + f * 4, 30), (30 - f * 3, 26), (24, 20 + f * 2)]:
            d.line((x - 2, y, x + 2, y), fill=C(255, 250, 200)); d.line((x, y - 2, x, y + 2), fill=C(255, 250, 200))
    return im


# ---------------------------------------------------------------- montagem das folhas de 8 personagens
def folha8(entradas, nome):
    """entradas: lista de 8 itens; cada um e uma lista de 4 linhas (direcoes 2,4,6,8) com 3 quadros."""
    sh = Image.new('RGBA', (576, 384), (0, 0, 0, 0))
    for i, linhas in enumerate(entradas):
        bx, by = (i % 4) * 144, (i // 4) * 192
        for r, quadros in enumerate(linhas):
            for c, q in enumerate(quadros):
                sh.alpha_composite(q, (bx + c * 48, by + r * 48))
    sh.save(f'{PROJ}/img/characters/{nome}.png')
    pv = Image.new('RGBA', sh.size, (90, 100, 90, 255)); pv.alpha_composite(sh)
    pv.resize((sh.width * 2, sh.height * 2), Image.NEAREST).save(PREV4 + nome.strip('!$') + '.png')


def tres(q):
    return [q, q, q]


def make_folhas():
    b = {k: busto(k) for k in WIGS}
    s = {k: suporte(k) for k in WIGS}
    folha8([
        [tres(busto()), tres(b['loira']), tres(b['ruiva']), tres(b['azul'])],
        [tres(b['preta'])] * 4,
        [tres(s['loira']), tres(s['ruiva']), tres(s['azul']), tres(s['preta'])],
        [tres(suporte())] * 4,
        [tres(estatua_uma('dourada')), tres(estatua_uma('prata')), tres(estatua_uma('bronze')), tres(estatua_uma('dourada', True))],
        [tres(alavanca(False)), tres(alavanca(True)), tres(alavanca(False)), tres(alavanca(True))],
        [tres(braseiro(False)), [braseiro(True, f) for f in range(3)], [braseiro(True, f) for f in range(3)], tres(braseiro(False))],
        [tres(esfinge()), tres(esfinge(True)), [esfinge(True, 1), esfinge(True, 2), esfinge(True, 1)], tres(esfinge())],
    ], '!Templo1')
    folha8([
        [tres(porta_pedra(0)), tres(porta_pedra(1 / 3)), tres(porta_pedra(2 / 3)), tres(porta_pedra(1))],
        [tres(porta_selada()), [porta_selada(f, True) for f in range(3)], [porta_selada(f, True) for f in range(3)], tres(porta_selada())],
        [[espinhos(0, f) for f in range(3)], [espinhos(1, f) for f in range(3)], [espinhos(2, f) for f in range(3)], tres(espinhos(2, 1))],
        [tres(cipo(0)), [cipo(1, f) for f in range(3)], [cipo(2, f) for f in range(3)], [cipo(3, f) for f in range(3)]],
        [[areia(False, f) for f in range(3)], [areia(True, f) for f in range(3)], [areia(True, f) for f in range(3)], [areia(False, f) for f in range(3)]],
        [tres(plataforma_portal(False)), [plataforma_portal(True, f) for f in range(3)], [plataforma_portal(True, f) for f in range(3)], tres(plataforma_portal(False))],
        [[brilho_dourado(f) for f in range(3)], [brilho_dourado(f, True) for f in range(3)], [brilho_dourado(f) for f in range(3)], [brilho_dourado(f, True) for f in range(3)]],
        [tres(cranio(0)), tres(cranio(1)), [cranio(2, f) for f in range(3)], [cranio(3, f) for f in range(3)]],
    ], '!Templo2')


# ---------------------------------------------------------------- tiles: Morro_E (Exterior) ganha a floresta e a piramide
def pegada(d, ang):
    """Pegada de pe descalco; os dedos apontam para 'ang' (graus, 0 = direita, 90 = baixo)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    cor = C(92, 70, 44, 170)
    for (s, off) in ((1, -6), (-1, 6)):
        cx, cy = 24 + px * off, 24 + py * off
        pts = []
        for k in range(16):
            t = k / 16 * 2 * math.pi
            r1, r2 = 5.5, 3.2
            x = cx + ux * math.cos(t) * r1 + px * math.sin(t) * r2
            y = cy + uy * math.cos(t) * r1 + py * math.sin(t) * r2
            pts.append((x, y))
        d.polygon(pts, fill=cor)
        for k in range(-2, 3):
            tx = cx + ux * 8 + px * k * 1.8
            ty = cy + uy * 8 + py * k * 1.8
            d.ellipse((tx - 1, ty - 1, tx + 1, ty + 1), fill=cor)


def tile_canvas():
    return Image.new('RGBA', (48, 48), (0, 0, 0, 0))


def t_espinheiro():
    im = espinhos(2, 1)
    return im


def t_lama():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.ellipse((4, 10, 44, 40), fill=C(110, 86, 56, 210))
    d.ellipse((10, 14, 36, 34), fill=C(130, 104, 70, 200))
    d.arc((14, 18, 30, 28), 200, 340, fill=C(160, 130, 90, 220))
    return im


def t_cogumelos():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    for k in range(7):
        a = k / 7 * 2 * math.pi
        x, y = 24 + 15 * math.cos(a), 26 + 10 * math.sin(a)
        d.rectangle((x - 1, y, x + 1, y + 4), fill=C(240, 230, 210))
        d.chord((x - 4, y - 4, x + 4, y + 3), 180, 360, fill=C(210, 50, 50))
        d.point((x - 1, y - 2), fill=WHITE)
    return outline(im, C(70, 40, 30))


def t_marco():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.rectangle((14, 10, 34, 46), fill=STONE)
    d.rectangle((14, 10, 34, 46), outline=STONE_D)
    d.rectangle((17, 14, 31, 22), outline=TEAL_D); d.line((19, 18, 29, 18), fill=TEAL)
    d.ellipse((19, 26, 29, 36), outline=TEAL_D); d.point((24, 31), fill=GOLD)
    d.rectangle((12, 42, 36, 46), fill=STONE_D)
    for (x, y) in [(16, 12), (32, 40)]:
        d.ellipse((x - 3, y - 2, x + 3, y + 2), fill=C(80, 150, 70))
    return outline(im, OUTS)


def glifo_parede(cor_fundo=C(196, 160, 90), cor_linha=C(120, 80, 36)):
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.rectangle((4, 6, 43, 41), fill=cor_fundo)
    d.rectangle((4, 6, 43, 41), outline=cor_linha)
    d.rectangle((8, 10, 39, 37), outline=cor_linha)
    d.ellipse((14, 14, 26, 26), outline=cor_linha); d.point((20, 20), fill=cor_linha)
    d.line((28, 14, 36, 14), fill=cor_linha); d.line((28, 18, 34, 18), fill=cor_linha)
    d.line((14, 30, 34, 30), fill=cor_linha); d.line((14, 33, 30, 33), fill=cor_linha)
    d.polygon([(30, 22), (36, 26), (30, 30)], outline=cor_linha)
    return im


def disco_sol():
    im = Image.new('RGBA', (96, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(16):
        a = math.radians(k * 22.5)
        d.polygon([(48 + 30 * math.cos(a - 0.12), 48 + 30 * math.sin(a - 0.12)), (48 + 46 * math.cos(a), 48 + 46 * math.sin(a)),
                   (48 + 30 * math.cos(a + 0.12), 48 + 30 * math.sin(a + 0.12))], fill=GOLD_D)
    d.ellipse((14, 14, 82, 82), fill=GOLD)
    d.ellipse((20, 20, 76, 76), outline=GOLD_D, width=2)
    d.ellipse((30, 30, 66, 66), fill=GOLD_L)
    d.ellipse((36, 38, 44, 46), fill=C(120, 80, 30)); d.ellipse((52, 38, 60, 46), fill=C(120, 80, 30))
    d.arc((36, 46, 60, 60), 20, 160, fill=C(120, 80, 30), width=3)
    for k in range(8):
        a = math.radians(k * 45 + 22)
        x, y = 48 + 25 * math.cos(a), 48 + 25 * math.sin(a)
        d.rectangle((x - 2, y - 2, x + 2, y + 2), fill=C(40, 150, 140))
    return outline(im, C(100, 64, 20))


def serpente(dir_dir=True):
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.rectangle((4, 30, 44, 46), fill=STONE_D)
    d.ellipse((6, 10, 40, 42), fill=C(60, 150, 110))
    d.polygon([(30, 18), (46, 24), (46, 34), (30, 38)], fill=C(60, 150, 110))
    d.polygon([(32, 30), (46, 32), (46, 36), (32, 37)], fill=C(170, 40, 50))
    for k in range(6):
        d.polygon([(8 + k * 4, 12 + (k % 2) * 2), (10 + k * 4, 2), (14 + k * 4, 12)], fill=[C(230, 60, 60), GOLD, C(60, 120, 220)][k % 3])
    d.ellipse((22, 18, 30, 26), fill=GOLD_L); d.ellipse((25, 20, 28, 25), fill=EYE_D)
    for (x, y) in [(36, 30), (40, 30)]:
        d.polygon([(x, y), (x + 1, y + 4), (x + 2, y)], fill=WHITE)
    im = outline(im, C(30, 50, 40))
    return im if dir_dir else im.transpose(Image.FLIP_LEFT_RIGHT)


def t_porta_escura():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 47, 47), fill=C(20, 14, 12))
    d.rectangle((0, 0, 47, 4), fill=GOLD_D)
    return im


def salvar_tiles(nome_folha, tiles):
    path = f'{PROJ}/img/tilesets/{nome_folha}.png'
    sheet = Image.open(path).convert('RGBA') if os.path.exists(path) else Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    for n, im in tiles.items():
        x, y = tile_pos(n)
        sheet.paste(Image.new('RGBA', (48, 48), (0, 0, 0, 0)), (x, y))
        sheet.alpha_composite(im, (x, y))
    sheet.save(path)
    pv = Image.new('RGBA', (768, 384), (80, 110, 80, 255)); pv.alpha_composite(sheet.crop((0, 0, 768, 384)))
    pv.save(PREV4 + f'{nome_folha}.png')


def morro_e():
    sol = disco_sol()
    tiles = {
        7: t_espinheiro(),
        8: Image.new('RGBA', (48, 48)), 9: Image.new('RGBA', (48, 48)), 10: Image.new('RGBA', (48, 48)), 11: Image.new('RGBA', (48, 48)),
        12: t_lama(), 13: t_cogumelos(), 14: t_marco(), 15: glifo_parede(),
        16: sol.crop((0, 0, 48, 48)), 17: sol.crop((48, 0, 96, 48)), 24: sol.crop((0, 48, 48, 96)), 25: sol.crop((48, 48, 96, 96)),
        18: serpente(True), 19: serpente(False), 20: t_porta_escura(),
    }
    for n, ang in ((8, 90), (9, 180), (10, 0), (11, 270)):
        im = tile_canvas(); pegada(ImageDraw.Draw(im), ang); tiles[n] = im
    salvar_tiles('Morro_E', tiles)


# ---------------------------------------------------------------- tiles: Templo_E (Calabouco/templo)
def t_faixa(horizontal=True):
    im = tile_canvas(); d = ImageDraw.Draw(im)
    for k in range(0, 48, 12):
        if horizontal:
            d.rectangle((k + 1, 22, k + 7, 25), fill=(250, 250, 240, 220))
        else:
            d.rectangle((22, k + 1, 25, k + 7), fill=(250, 250, 240, 220))
    return im


def t_chegada():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    for yy in range(0, 48, 8):
        for xx in range(16, 32, 8):
            if ((yy // 8) + (xx // 8)) % 2 == 0:
                d.rectangle((xx, yy, xx + 7, yy + 7), fill=(250, 250, 250, 230))
            else:
                d.rectangle((xx, yy, xx + 7, yy + 7), fill=(30, 30, 30, 230))
    return im


def t_placa_podio(n):
    im = tile_canvas(); d = ImageDraw.Draw(im)
    cor = {1: (GOLD, GOLD_D), 2: (C(220, 224, 234), C(150, 156, 170)), 3: (C(206, 132, 72), C(140, 80, 40))}[n]
    d.rectangle((4, 4, 43, 43), fill=cor[1]); d.rectangle((7, 7, 40, 40), fill=cor[0])
    d.rectangle((7, 7, 40, 40), outline=lighter(cor[0], 0.5))
    # numeral romano
    xs = {1: [24], 2: [20, 28], 3: [16, 24, 32]}[n]
    for x in xs:
        d.rectangle((x - 2, 14, x + 2, 33), fill=cor[1])
    d.line((12, 14, 36, 14), fill=cor[1], width=2); d.line((12, 33, 36, 33), fill=cor[1], width=2)
    return im


def t_ferradura():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.arc((12, 10, 36, 38), 200, 520, fill=(236, 196, 70, 200), width=5)
    for (x, y) in [(15, 30), (33, 30), (14, 20), (34, 20)]:
        d.point((x, y), fill=(120, 80, 30, 220))
    return im


def t_placa_peruca():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.ellipse((8, 8, 40, 40), fill=(236, 196, 70, 120))
    wig(d, 24, 12, WIGS['loira'], larg=9, alt=16)
    return im


def t_mural_uma():
    im = glifo_parede(C(40, 140, 130), C(16, 80, 76)); d = ImageDraw.Draw(im)
    d.rectangle((8, 10, 39, 37), fill=C(40, 140, 130))
    d.ellipse((18, 12, 24, 18), fill=GOLD)
    d.polygon([(17, 12), (18, 8), (20, 12)], fill=GOLD); d.polygon([(22, 12), (23, 8), (25, 12)], fill=GOLD)
    d.line((21, 18, 24, 26), fill=GOLD, width=2)
    d.line((24, 26, 18, 34), fill=GOLD, width=2); d.line((24, 26, 32, 32), fill=GOLD, width=2)
    d.line((22, 21, 30, 18), fill=GOLD, width=2); d.line((22, 21, 15, 24), fill=GOLD, width=2)
    d.polygon([(24, 25), (32, 22), (30, 26)], fill=GOLD)
    for x in (10, 13, 35, 38):
        d.line((x, 30, x - 3, 30), fill=GOLD_L)
    return im


def t_mural_peruca():
    im = glifo_parede(C(40, 140, 130), C(16, 80, 76)); d = ImageDraw.Draw(im)
    d.rectangle((8, 10, 39, 37), fill=C(40, 140, 130))
    wig(d, 24, 12, WIGS['loira'], larg=9, alt=15)
    for (x, y) in [(12, 14), (36, 16), (13, 34), (35, 33)]:
        d.line((x - 2, y, x + 2, y), fill=GOLD_L); d.line((x, y - 2, x, y + 2), fill=GOLD_L)
    return im


def t_faixa_ouro():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    d.rectangle((0, 18, 47, 29), fill=GOLD)
    d.line((0, 18, 47, 18), fill=GOLD_L); d.line((0, 29, 47, 29), fill=GOLD_D)
    for x in range(2, 48, 8):
        d.polygon([(x, 27), (x + 3, 20), (x + 6, 27)], outline=GOLD_D)
    return im


def t_arco_iris():
    im = tile_canvas(); d = ImageDraw.Draw(im)
    cores = [(232, 52, 60), (250, 140, 40), (250, 214, 50), (84, 190, 92), (62, 132, 222), (150, 92, 206)]
    for k, c in enumerate(cores):
        d.rectangle((0, k * 8, 47, k * 8 + 7), fill=c + (150,))
    return im


def templo_e():
    sol = disco_sol()
    tiles = {
        0: t_faixa(True), 1: t_faixa(False), 2: t_chegada(),
        3: t_placa_podio(1), 4: t_placa_podio(2), 5: t_placa_podio(3),
        6: t_ferradura(), 7: t_placa_peruca(),
        8: glifo_parede(), 9: t_faixa_ouro(),
        10: sol.crop((0, 0, 48, 48)), 11: sol.crop((48, 0, 96, 48)), 18: sol.crop((0, 48, 48, 96)), 19: sol.crop((48, 48, 96, 96)),
        12: serpente(True), 13: t_mural_uma(), 14: t_mural_peruca(), 15: t_arco_iris(), 16: t_porta_escura(),
        17: serpente(False),
    }
    salvar_tiles('Templo_E', tiles)


def main():
    make_folhas()
    morro_e()
    templo_e()
    print('ok')


if __name__ == '__main__':
    main()
