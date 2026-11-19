# Arte da segunda leva: batalha lateral (SV), Rei Macaco, coco, banana dourada, chave e o tileset E do morro.
import math, os, random, shutil, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_assets import C, outline, PROJ
from gen_ch2_scenes import tile_pos

POSES = ['corrida', 'chute', 'soco', 'dor', 'queda', 'magia', 'cansado', 'choro', 'riso', 'pulo', 'facada', 'rastejar']
PREV = HERE + '/prev_v2/'
os.makedirs(PREV, exist_ok=True)


# ================================================================ batalha lateral: atores
# Folha SV do MZ: 9 colunas x 6 linhas; cada movimento ocupa 3 quadros (18 movimentos).
# Os quadros aqui tem 96x96 (sprite de 48 px ampliado 2x, sem suavizar).
SV_LOOKS = {
    'Baratelli': ('soco', 'chute'), 'Baratelli_Flor': ('soco', 'chute'), 'Baratelli_Cigana': ('soco', 'chute'),
    'Leandra': ('soco', 'chute'), 'Leandra_Careca': ('soco', 'chute'),
    'Leona': ('soco', 'chute'), 'Leona_Cavalo': ('chute', 'chute'),
    'Kevinho': ('chute', 'chute'),
    'Baratelli_Diva': ('soco', 'chute'), 'Kevinho_Uma': ('chute', 'chute'),
}


def sv_sheet(nome, ataque, especial):
    ch = Image.open(f'{PROJ}/img/characters/${nome}.png').convert('RGBA')
    po = Image.open(f'{PROJ}/img/characters/Pose_{nome}.png').convert('RGBA')

    def cf(col, row):
        return ch.crop((col * 48, row * 48, col * 48 + 48, row * 48 + 48))

    def pf(pose, k, bloco=1):  # bloco: 0 baixo, 1 esquerda, 2 direita, 3 cima
        r = POSES.index(pose)
        c = bloco * 3 + k
        return po.crop((c * 48, r * 48, c * 48 + 48, r * 48 + 48))

    def respira(im, px):
        out = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
        out.alpha_composite(im.resize((48, 48 - px), Image.NEAREST), (0, px))
        return out

    L = lambda k: cf(k, 1)
    trio = lambda pose, bloco=1: [pf(pose, k, bloco) for k in range(3)]
    outro = 'chute' if ataque == 'soco' else 'soco'
    mov = [
        [L(0), L(1), L(2)],                         # 0 walk
        [L(1), respira(L(1), 1), respira(L(1), 2)],  # 1 wait (respirando)
        trio('magia'),                              # 2 chant
        [pf('soco', 0)] * 3,                        # 3 guard
        trio('dor'),                                # 4 damage
        trio('pulo'),                               # 5 evade
        trio(ataque),                               # 6 thrust (ataque sem arma)
        trio(outro),                                # 7 swing
        trio('soco'),                               # 8 missile
        trio(especial),                             # 9 skill
        trio('magia'),                              # 10 spell
        trio('magia'),                              # 11 item
        trio('corrida', bloco=2),                   # 12 escape (corre para a direita)
        trio('riso'),                               # 13 victory
        trio('cansado'),                            # 14 dying (pouca vida)
        trio('choro'),                              # 15 abnormal
        [pf('queda', 1)] * 3,                       # 16 sleep
        [pf('queda', 1), pf('queda', 1), pf('queda', 2)],  # 17 dead (estrelinhas piscando)
    ]
    F = 96
    sheet = Image.new('RGBA', (9 * F, 6 * F), (0, 0, 0, 0))
    for idx, frames in enumerate(mov):
        bx, row = idx // 6, idx % 6
        for k, fr in enumerate(frames):
            sheet.alpha_composite(fr.resize((F, F), Image.NEAREST), ((bx * 3 + k) * F, row * F))
    sheet.save(f'{PROJ}/img/sv_actors/SV_{nome}.png')
    return sheet


def make_sv_actors():
    for nome, (ataque, especial) in SV_LOOKS.items():
        sh = sv_sheet(nome, ataque, especial)
    pv = Image.new('RGBA', sh.size, (60, 70, 90, 255)); pv.alpha_composite(sh); pv.save(PREV + 'sv_kevinho.png')


# ================================================================ batalha lateral: inimigos
def make_sv_enemies():
    os.makedirs(f'{PROJ}/img/sv_enemies', exist_ok=True)
    shutil.copy2(f'{PROJ}/img/enemies/Kura.png', f'{PROJ}/img/sv_enemies/Kura.png')
    import gen_ch3_assets as G3
    G3.make_frog_battler(sombra=False, destino=f'{PROJ}/img/sv_enemies/Gusrola_Sapo.png')


# ================================================================ Rei Macaco
def crown(d, cx, top):
    gold, dark, gem = (246, 204, 70, 255), (120, 80, 20, 255), (220, 40, 60, 255)
    pts = [(cx - 8, top + 9), (cx - 8, top + 2), (cx - 4, top + 5), (cx, top), (cx + 4, top + 5), (cx + 8, top + 2), (cx + 8, top + 9)]
    d.polygon(pts, fill=gold, outline=dark)
    d.line((cx - 7, top + 8, cx + 7, top + 8), fill=(200, 150, 40, 255))
    d.point((cx, top + 6), fill=gem); d.point((cx - 1, top + 6), fill=gem)
    for x in (cx - 8, cx, cx + 8):
        d.point((x, top - 1 if x == cx else top + 1), fill=(255, 250, 200, 255))


def make_rei_macaco():
    src = Image.open(f'{PROJ}/img/characters/$Macaco.png').convert('RGBA')
    out = src.copy()
    d = ImageDraw.Draw(out)
    for r in range(4):
        for c in range(3):
            fr = src.crop((c * 48, r * 48, c * 48 + 48, r * 48 + 48))
            px = fr.load()
            xs = [x for y in range(12, 18) for x in range(48) if px[x, y][3] > 0]
            cx = (min(xs) + max(xs)) // 2 if xs else 24
            if r == 1:
                cx -= 1
            elif r == 2:
                cx += 1
            crown(d, c * 48 + cx, r * 48 + 4)
    out.save(f'{PROJ}/img/characters/$Rei_Macaco.png')
    out.resize((out.width * 3, out.height * 3), Image.NEAREST).save(PREV + 'rei_macaco.png')


# ================================================================ coco que rola e banana dourada (eventos)
def make_coco():
    S = 4
    sheet = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for c in range(3):
        im = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        cx, cy, r = 24 * S, 35 * S, 10 * S
        d.ellipse((cx - r + 2 * S, cy + r - 3 * S, cx + r - 2 * S, cy + r + 1 * S), fill=(0, 0, 0, 70))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(122, 78, 42, 255))
        d.ellipse((cx - r + 3 * S, cy - r + 2 * S, cx + r - 6 * S, cy + r - 8 * S), fill=(150, 100, 58, 255))
        a0 = c * 2 * math.pi / 3
        for k in range(7):
            a = a0 + k * 0.9
            x1, y1 = cx + math.cos(a) * r * 0.25, cy + math.sin(a) * r * 0.25
            x2, y2 = cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9
            d.line((x1, y1, x2, y2), fill=(96, 58, 30, 255), width=S)
        for k in range(3):
            a = a0 + k * 2 * math.pi / 3 + 0.4
            x, y = cx + math.cos(a) * r * 0.42, cy + math.sin(a) * r * 0.42
            d.ellipse((x - 1.6 * S, y - 1.6 * S, x + 1.6 * S, y + 1.6 * S), fill=(52, 30, 16, 255))
        im = outline(im.resize((48, 48), Image.LANCZOS), C(40, 24, 12))
        for r_ in range(4):
            sheet.alpha_composite(im, (c * 48, r_ * 48))
    sheet.save(f'{PROJ}/img/characters/!$Coco.png')


def banana_img(w, cor=(255, 200, 40, 255), luz=(255, 246, 180, 255), borda=(120, 74, 10), angulo=-12):
    """Banana em forma de lua crescente (w = largura final em px)."""
    from PIL import ImageChops
    S = 4
    W, H = w * S, int(w * 0.72) * S
    outer = Image.new('L', (W, H), 0); ImageDraw.Draw(outer).ellipse((0.04 * W, -0.62 * H, 0.96 * W, 0.92 * H), fill=255)
    inner = Image.new('L', (W, H), 0); ImageDraw.Draw(inner).ellipse((0.10 * W, -0.95 * H, 0.90 * W, 0.58 * H), fill=255)
    mask = ImageChops.subtract(outer, inner)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    im.paste(Image.new('RGBA', (W, H), cor), (0, 0), mask)
    hi = Image.new('L', (W, H), 0); ImageDraw.Draw(hi).arc((0.16 * W, -0.70 * H, 0.84 * W, 0.80 * H), 35, 145, fill=255, width=max(1, int(0.045 * H)))
    im.paste(Image.new('RGBA', (W, H), luz), (0, 0), ImageChops.multiply(hi, mask))
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).arc((0.05 * W, -0.60 * H, 0.95 * W, 0.90 * H), 30, 150, fill=255, width=max(1, int(0.05 * H)))
    im.paste(Image.new('RGBA', (W, H), tuple(max(0, v - 40) for v in cor[:3]) + (255,)), (0, 0), ImageChops.multiply(sh, mask))
    cols = [x for x in range(W) if any(mask.getpixel((x, y)) for y in range(0, H, 2))]
    d = ImageDraw.Draw(im)
    for x in (cols[0] + 2 * S, cols[-1] - 2 * S):
        ys = [y for y in range(H) if mask.getpixel((x, y))]
        y = (ys[0] + ys[-1]) // 2 if ys else H // 4
        r = 0.05 * H
        d.ellipse((x - r, y - r, x + r, y + r), fill=(96, 60, 16, 255))
    x = cols[-1] - 2 * S
    d.line((x, 0.22 * H, x + 0.06 * W, 0.08 * H), fill=(110, 76, 24, 255), width=max(1, int(0.05 * H)))
    im = im.rotate(angulo, resample=Image.BICUBIC, expand=True)
    im = im.resize((im.width // S, im.height // S), Image.LANCZOS)
    return outline(im, C(*borda))


def star(d, x, y, r, cor):
    d.polygon([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28),
               (x, y + r), (x - r * 0.28, y + r * 0.28), (x - r, y), (x - r * 0.28, y - r * 0.28)], fill=cor)


def make_banana_dourada_evento():
    S = 4
    sheet = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for c in range(3):
        im = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0))
        glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((8 * S, 14 * S, 40 * S, 40 * S), fill=(255, 220, 90, 120))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(5 * S)))
        d = ImageDraw.Draw(im)
        d.ellipse((14 * S, 38 * S, 34 * S, 42 * S), fill=(0, 0, 0, 60))
        b = banana_img(30 * S)
        im.alpha_composite(b, (24 * S - b.width // 2, (29 - [0, 1, 0][c]) * S - b.height // 2))
        d = ImageDraw.Draw(im)
        for (x, y, r) in [((12, 14, 3.5), (36, 18, 2.5)), ((35, 12, 3.5), (13, 22, 2.5)), ((24, 10, 3.5), (38, 26, 2.5))][c]:
            star(d, x * S, y * S, r * S, (255, 255, 230, 255))
        im = im.resize((48, 48), Image.LANCZOS)
        for r_ in range(4):
            sheet.alpha_composite(im, (c * 48, r_ * 48))
    sheet.save(f'{PROJ}/img/characters/!$Banana_Dourada.png')


# ================================================================ figuras de item (256x256, no estilo das outras)
def item_canvas():
    S = 2
    return Image.new('RGBA', (256 * S, 256 * S), (0, 0, 0, 0)), S


def finish_item(im, S, glow_color, nome):
    im = im.resize((256, 256), Image.LANCZOS)
    a = im.split()[3]
    glow = Image.new('RGBA', im.size, glow_color)
    glow.putalpha(a.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.7)))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.alpha_composite(glow); out.alpha_composite(im)
    out.save(f'{PROJ}/img/pictures/{nome}.png')
    pv = Image.new('RGBA', out.size, (50, 60, 80, 255)); pv.alpha_composite(out); pv.save(PREV + nome + '.png')


def make_item_banana_dourada():
    im, S = item_canvas(); d = ImageDraw.Draw(im)
    b = banana_img(200 * S, cor=(255, 196, 36, 255))
    im.alpha_composite(b, (128 * S - b.width // 2, 132 * S - b.height // 2))
    d = ImageDraw.Draw(im)
    for (x, y, r) in [(60, 70, 16), (196, 84, 11), (176, 186, 13), (90, 190, 8)]:
        star(d, x * S, y * S, r * S, (255, 255, 235, 255))
    finish_item(im, S, (255, 214, 80, 255), 'Item_Banana_Dourada')


def make_item_chave():
    im, S = item_canvas(); d = ImageDraw.Draw(im)
    ferro, escuro, ferrugem = (150, 120, 96, 255), (90, 66, 50, 255), (176, 96, 46, 255)
    cx, cy = 88 * S, 98 * S
    d.ellipse((cx - 50 * S, cy - 50 * S, cx + 50 * S, cy + 50 * S), fill=ferro, outline=escuro, width=6 * S)
    d.ellipse((cx - 24 * S, cy - 24 * S, cx + 24 * S, cy + 24 * S), fill=(0, 0, 0, 0), outline=escuro, width=6 * S)
    d.polygon([(cx + 30 * S, cy + 30 * S), (cx + 42 * S, cy + 18 * S), (212 * S, 200 * S), (200 * S, 212 * S)], fill=ferro, outline=escuro)
    for (x, y) in [(176, 164), (196, 184)]:
        d.polygon([(x * S, y * S), ((x + 14) * S, (y - 14) * S), ((x + 26) * S, (y - 2) * S), ((x + 12) * S, (y + 12) * S)],
                  fill=ferro, outline=escuro)
    rng = random.Random(7)
    for _ in range(40):
        a = rng.uniform(0, 2 * math.pi); rr = rng.uniform(26, 46)
        x, y = cx + math.cos(a) * rr * S, cy + math.sin(a) * rr * S
        s = rng.uniform(2, 5) * S
        d.ellipse((x - s, y - s, x + s, y + s), fill=ferrugem)
    for _ in range(14):
        t = rng.uniform(0.15, 0.9)
        x = cx + 36 * S + (212 * S - cx - 36 * S) * t; y = cy + 24 * S + (206 * S - cy - 24 * S) * t
        s = rng.uniform(2, 4) * S
        d.ellipse((x - s, y - s, x + s, y + s), fill=ferrugem)
    finish_item(outline(im, C(50, 34, 24)), S, (255, 220, 160, 255), 'Item_Chave')


# ================================================================ tileset E do Exterior (morro e patio)
E_PEELS = (0, 1, 2)
E_CRACK, E_BRIDGE, E_TOCA, E_COCOS = 3, 4, 5, 6


def peel_tile(seed):
    rng = random.Random(seed)
    S = 4
    t = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    for _ in range(rng.randint(1, 2)):
        x, y = rng.randint(12, 34) * S, rng.randint(14, 34) * S
        a0 = rng.uniform(0, 2 * math.pi)
        d.ellipse((x - 3 * S, y - 2 * S, x + 3 * S, y + 2 * S), fill=(120, 84, 30, 255))
        for k in range(3):
            a = a0 + k * 2.1 + rng.uniform(-0.3, 0.3)
            ex, ey = x + math.cos(a) * 13 * S, y + math.sin(a) * 9 * S
            mx, my = x + math.cos(a + 0.3) * 6 * S, y + math.sin(a + 0.3) * 4 * S
            d.polygon([(x, y), (mx, my), (ex, ey), (x + math.cos(a - 0.4) * 5 * S, y + math.sin(a - 0.4) * 3 * S)],
                      fill=(246, 214, 70, 255))
            d.line((mx, my, ex, ey), fill=(150, 110, 30, 255), width=S)
            d.ellipse((ex - 1.5 * S, ey - 1.5 * S, ex + 1.5 * S, ey + 1.5 * S), fill=(70, 50, 20, 255))
    t = t.resize((48, 48), Image.LANCZOS)
    return outline(t, C(90, 64, 20))


def crack_tile():
    S = 4
    t = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    dark = (40, 34, 30, 230)
    for pts in [[(8, 10), (16, 18), (14, 26), (22, 32), (20, 40)], [(16, 18), (26, 16), (34, 22), (42, 20)],
                [(22, 32), (30, 34), (36, 42)], [(34, 22), (32, 30)]]:
        d.line([(x * S, y * S) for x, y in pts], fill=dark, width=int(1.8 * S), joint='curve')
    for (x, y) in [(10, 36), (38, 12), (28, 8)]:
        d.ellipse(((x - 1.5) * S, (y - 1.5) * S, (x + 1.5) * S, (y + 1.5) * S), fill=(80, 70, 60, 200))
    return t.resize((48, 48), Image.LANCZOS)


def bridge_tile():
    t = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    rng = random.Random(5)
    for k in range(4):
        y0 = k * 12
        c = (150 + rng.randint(-12, 10), 102 + rng.randint(-8, 8), 56 + rng.randint(-6, 6), 255)
        d.rectangle((6, y0 + 1, 41, y0 + 10), fill=c)
        d.line((6, y0 + 10, 41, y0 + 10), fill=(86, 56, 28, 255))
        d.line((6, y0 + 1, 41, y0 + 1), fill=(186, 138, 84, 255))
        d.point((9, y0 + 5), fill=(70, 46, 22, 255)); d.point((38, y0 + 5), fill=(70, 46, 22, 255))
    for x in (3, 44):
        d.line((x, 0, x, 47), fill=(196, 170, 110, 255), width=3)
        d.line((x - 1, 0, x - 1, 47), fill=(120, 96, 56, 255))
        for y in range(2, 48, 12):
            d.line((x - 3, y, x + 2, y + 3), fill=(120, 96, 56, 255), width=2)
    return t


def toca_tile():
    S = 4
    t = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.ellipse((8 * S, 18 * S, 40 * S, 46 * S), fill=(110, 92, 70, 255))
    d.ellipse((12 * S, 22 * S, 36 * S, 46 * S), fill=(24, 18, 14, 255))
    d.ellipse((15 * S, 28 * S, 21 * S, 32 * S), fill=(255, 210, 90, 255))
    d.ellipse((26 * S, 28 * S, 32 * S, 32 * S), fill=(255, 210, 90, 255))
    t = t.resize((48, 48), Image.LANCZOS)
    t2 = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); t2.alpha_composite(t)
    px = t2.load()
    for y in range(44, 48):
        for x in range(48):
            if px[x, y][3]:
                px[x, y] = (px[x, y][0], px[x, y][1], px[x, y][2], 0)
    return t2


def cocos_tile():
    S = 4
    t = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    for (x, y) in [(15, 34), (31, 34), (23, 24), (24, 38)]:
        r = 8
        d.ellipse(((x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S), fill=(122, 78, 42, 255))
        d.ellipse(((x - r + 2) * S, (y - r + 2) * S, (x + 2) * S, (y + 1) * S), fill=(150, 100, 58, 255))
    return outline(t.resize((48, 48), Image.LANCZOS), C(40, 24, 12))


def make_morro_e():
    sheet = Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    for n in E_PEELS:
        sheet.alpha_composite(peel_tile(20 + n), tile_pos(n))
    sheet.alpha_composite(crack_tile(), tile_pos(E_CRACK))
    sheet.alpha_composite(bridge_tile(), tile_pos(E_BRIDGE))
    sheet.alpha_composite(toca_tile(), tile_pos(E_TOCA))
    sheet.alpha_composite(cocos_tile(), tile_pos(E_COCOS))
    sheet.save(f'{PROJ}/img/tilesets/Morro_E.png')
    pv = Image.new('RGBA', (48 * 7, 48), (110, 110, 100, 255))
    for i in range(7):
        x, y = tile_pos(i)
        pv.alpha_composite(sheet.crop((x, y, x + 48, y + 48)), (i * 48, 0))
    pv.resize((pv.width * 3, pv.height * 3), Image.NEAREST).save(PREV + 'morro_e.png')


def make_cipo():
    """Cipó pendurado na beira do ninho (3 quadros balançando)."""
    S = 4
    sheet = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for c in range(3):
        im = Image.new('RGBA', (48 * S, 48 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        bal = [-2, 0, 2][c]
        pts = [(24 * S + (math.sin(t / 6.0) * 3 + bal * t / 47) * S, t * S) for t in range(0, 48)]
        d.line(pts, fill=(70, 120, 40, 255), width=4 * S, joint='curve')
        d.line([(x - S, y) for x, y in pts], fill=(120, 170, 70, 255), width=S)
        for k, t in enumerate(range(6, 46, 9)):
            x, y = pts[t]
            lado = 1 if k % 2 else -1
            d.ellipse((x + lado * 2 * S - 4 * S, y - 3 * S, x + lado * 2 * S + 4 * S, y + 3 * S), fill=(90, 160, 60, 255))
        im = outline(im.resize((48, 48), Image.LANCZOS), C(30, 60, 20))
        for r_ in range(4):
            sheet.alpha_composite(im, (c * 48, r_ * 48))
    sheet.save(f'{PROJ}/img/characters/!$Cipo.png')


def main():
    make_cipo()
    make_sv_actors()
    make_sv_enemies()
    make_rei_macaco()
    make_coco()
    make_banana_dourada_evento()
    make_item_banana_dourada()
    make_item_chave()
    make_morro_e()
    print('arte nova pronta')


if __name__ == '__main__':
    main()
