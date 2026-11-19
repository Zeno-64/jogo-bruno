# Gera as folhas de poses (corrida, chute, soco, dor, queda...) e o data/Poses.json.
import json, math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = 'K:/Kevin/workspace/jogo-bruno'
CHARS = PROJ + '/img/characters/'
PREV = HERE + '/prev/'

ROWS = ['corrida', 'chute', 'soco', 'dor', 'queda', 'magia', 'cansado', 'choro', 'riso', 'pulo', 'facada', 'rastejar']
F = 48
PIV = (24, 45)

# ---------------------------------------------------------------- personagens
BASE = dict(skin=(242, 204, 174), leg=(242, 204, 174), shoe=(250, 210, 24), sleeve=(184, 150, 222),
            aura=(255, 170, 225), eyes=[(20, 14), (28, 14)], eye_side=(15, 14), hip=40, shoulder=26,
            out=(46, 28, 44))
ALVOS = {
    '$Baratelli': dict(BASE),
    '$Baratelli_Flor': dict(BASE),
    '$Baratelli_Cigana': dict(BASE, sleeve=(204, 42, 60), aura=(255, 120, 150)),
    '$Monark': dict(BASE, skin=(116, 74, 50), leg=(40, 36, 46), shoe=(98, 60, 34), sleeve=(244, 240, 228),
                    aura=(255, 90, 90), eyes=[(20, 13), (27, 13)], eye_side=(17, 13), hip=36, out=(30, 18, 16)),
    '$Leandra': dict(BASE, skin=(248, 216, 188), leg=(248, 216, 188), shoe=(224, 182, 150), sleeve=(200, 176, 134),
                     aura=(255, 222, 120), eyes=[(20, 21), (28, 21)], eye_side=(17, 21), hip=38, shoulder=28,
                     out=(64, 42, 34)),
    '$Leona': dict(BASE, skin=(252, 230, 216), leg=(252, 230, 216), shoe=(44, 34, 44), sleeve=(146, 34, 64),
                   aura=(190, 120, 255), eyes=[(20, 21), (28, 21)], eye_side=(17, 21), hip=38, shoulder=28,
                   out=(40, 22, 36)),
    '$Kura': dict(BASE, skin=(150, 130, 170), leg=(30, 22, 42), shoe=(16, 12, 24), sleeve=(62, 44, 86),
                  aura=(170, 60, 255), eyes=[(20, 13), (27, 13)], eye_side=(16, 13), hip=34, shoulder=24,
                  out=(10, 6, 14)),
    '$Raulete': dict(BASE, skin=(240, 202, 170), leg=(36, 30, 44), shoe=(24, 20, 26), sleeve=(128, 70, 164),
                     aura=(255, 210, 90), eyes=[(20, 13), (27, 13)], eye_side=(17, 13), hip=36, out=(30, 18, 30)),
    '$Kevinho': dict(BASE, skin=(232, 192, 160), leg=(58, 82, 132), shoe=(244, 244, 244), sleeve=(92, 180, 124),
                     aura=(120, 255, 160), eyes=[(20, 14), (27, 14)], eye_side=(17, 14), hip=36, out=(30, 26, 30)),
    '$Gusrola_Sapo': dict(BASE, skin=(94, 168, 76), leg=(60, 118, 48), shoe=(60, 118, 48), sleeve=(94, 168, 76),
                          aura=(140, 255, 120), eyes=[(16, 8), (31, 8)], eye_side=(17, 8), hip=38, shoulder=28,
                          out=(24, 50, 20)),
    '$Vidente': dict(BASE, skin=(236, 206, 182), leg=(108, 58, 140), shoe=(74, 36, 100), sleeve=(146, 96, 180),
                     aura=(150, 200, 255), eyes=[(20, 14), (27, 14)], eye_side=(18, 14), out=(40, 24, 40)),
    'People1#2': dict(BASE, skin=(250, 214, 182), sleeve=None, leg=None, shoe=None, aura=(140, 255, 120),
                      eyes=[(20, 18), (27, 18)], eye_side=(17, 18), out=(40, 30, 30)),
    'People1#5': dict(BASE, skin=(250, 214, 182), sleeve=None, leg=None, shoe=None, aura=(255, 200, 140),
                      eyes=[(20, 18), (27, 18)], eye_side=(17, 18), out=(40, 30, 30)),
    'Evil#7': dict(BASE, skin=(220, 190, 170), sleeve=None, leg=None, shoe=None, aura=(170, 80, 220),
                   eyes=[(20, 18), (27, 18)], eye_side=(17, 18), out=(20, 14, 24)),
}
ALVOS['$Leandra_Careca'] = dict(ALVOS['$Leandra'])
ALVOS['$Leona_Cavalo'] = dict(ALVOS['$Leona'])
ALVOS['$Raulete_Peruca'] = dict(ALVOS['$Raulete'])
# Capitulo 4
ALVOS['$Baratelli_Diva'] = dict(BASE, sleeve=(255, 170, 214), shoe=(198, 162, 236), aura=(255, 210, 120))
ALVOS['$Kevinho_Uma'] = dict(BASE, skin=(124, 80, 54), leg=(124, 80, 54), shoe=(244, 244, 244), sleeve=(248, 248, 248),
                             aura=(120, 255, 160), eyes=[(20, 15), (27, 15)], eye_side=(16, 15), hip=34, out=(30, 22, 24))
ALVOS['$Leona_Adulta'] = dict(BASE, skin=(252, 230, 216), leg=(30, 24, 38), shoe=(18, 14, 22), sleeve=(72, 34, 100),
                              aura=(190, 80, 255), eyes=[(20, 13), (26, 13)], eye_side=(17, 13), hip=31, shoulder=19,
                              out=(22, 12, 26))
ALVOS['$Vera_Verao'] = dict(BASE, skin=(112, 70, 52), leg=(204, 28, 74), shoe=(204, 28, 74), sleeve=(112, 70, 52),
                            aura=(255, 220, 120), eyes=[(20, 14), (27, 14)], eye_side=(15, 14), hip=36, out=(70, 36, 30))
ALVOS['$Curupira'] = dict(BASE, skin=(196, 140, 96), leg=(196, 140, 96), shoe=(160, 106, 70), sleeve=(196, 140, 96),
                          aura=(255, 120, 40), eyes=[(20, 15), (27, 15)], eye_side=(17, 15), hip=34, out=(56, 26, 16))


def base_frames(key):
    if '#' in key:
        name, idx = key.split('#'); idx = int(idx)
        im = Image.open(CHARS + name + '.png').convert('RGBA')
        bx, by = (idx % 4) * 144, (idx // 4) * 192
    else:
        im = Image.open(CHARS + key + '.png').convert('RGBA')
        bx, by = 0, 0
    fr = {}
    for r, d in enumerate((2, 4, 6, 8)):
        fr[d] = [im.crop((bx + p * F, by + r * F, bx + p * F + F, by + r * F + F)) for p in range(3)]
    return fr


def sample(img, x, y, fallback):
    for r in range(0, 4):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                xx, yy = x + dx, y + dy
                if 0 <= xx < F and 0 <= yy < F:
                    px = img.getpixel((xx, yy))
                    if px[3] > 200 and sum(px[:3]) > 60:
                        return px[:3]
    return fallback


# ---------------------------------------------------------------- operacoes
def blank():
    return Image.new('RGBA', (F, F), (0, 0, 0, 0))


def rot(img, ang, piv=PIV):
    if not ang:
        return img.copy()
    big = Image.new('RGBA', (F * 2, F * 2), (0, 0, 0, 0))
    big.alpha_composite(img, (F // 2, F // 2))
    big = big.rotate(ang, resample=Image.NEAREST, center=(piv[0] + F // 2, piv[1] + F // 2))
    return big.crop((F // 2, F // 2, F // 2 + F, F // 2 + F))


def shift(img, dx, dy):
    out = blank()
    out.alpha_composite(img, (0, 0)) if (dx, dy) == (0, 0) else out.paste(img, (dx, dy), img)
    return out


def scale_b(img, sx, sy):
    w, h = max(1, round(F * sx)), max(1, round(F * sy))
    s = img.resize((w, h), Image.NEAREST)
    out = blank()
    out.alpha_composite(s, (round(24 - 24 * sx), round(47 - 47 * sy))) if w <= F and h <= F else None
    if w > F or h > F:
        big = Image.new('RGBA', (F * 2, F * 2), (0, 0, 0, 0))
        big.alpha_composite(s, (round(F - 24 * sx), round(F + 47 - 47 * sy) - F // 2 * 0))
        out = big.crop((F // 2, F - 1 + 0, F // 2 + F, F - 1 + F))
        out = blank()
        ox, oy = round(24 - 24 * sx), round(47 - 47 * sy)
        tmp = Image.new('RGBA', (F * 3, F * 3), (0, 0, 0, 0))
        tmp.alpha_composite(s, (F + ox, F + oy))
        out = tmp.crop((F, F, 2 * F, 2 * F))
    return out


def tint(img, color, amount):
    r, g, b, a = img.split()
    solid = Image.new('RGB', img.size, color)
    mixed = Image.blend(Image.merge('RGB', (r, g, b)), solid, amount)
    out = Image.merge('RGBA', (*mixed.split(), a))
    return out


def mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def over(*layers):
    out = blank()
    for l in layers:
        out.alpha_composite(l)
    return out


def contorno(layer, color):
    a = layer.split()[3].point(lambda v: 255 if v > 0 else 0)
    edge = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(3)), a)
    out = blank()
    out.paste(Image.new('RGBA', (F, F), color + (255,)), (0, 0), edge)
    out.alpha_composite(layer)
    return out


def membro(p, a, b, cor, ponta, raio=3, largura=4, extra=None):
    l = blank(); d = ImageDraw.Draw(l)
    d.line([a, b], fill=cor + (255,), width=largura)
    d.ellipse((b[0] - raio, b[1] - raio, b[0] + raio, b[1] + raio), fill=ponta + (255,))
    if extra:
        extra(d)
    return contorno(l, p['out'])


def estrelas(n, cx, cy, r, fase, cor=(255, 236, 90)):
    l = blank(); d = ImageDraw.Draw(l)
    for k in range(n):
        a = fase + k * 2 * math.pi / n
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * 0.45
        d.line((x - 2, y, x + 2, y), fill=cor + (255,)); d.line((x, y - 2, x, y + 2), fill=cor + (255,))
        d.point((x, y), fill=(255, 255, 255, 255))
    return l


def gotas_suor(pontos):
    l = blank(); d = ImageDraw.Draw(l)
    for (x, y) in pontos:
        d.polygon([(x, y - 2), (x + 2, y + 1), (x, y + 3), (x - 2, y + 1)], fill=(170, 220, 255, 255))
        d.point((x - 1, y), fill=(255, 255, 255, 255))
    return l


def linhas_velocidade(lado, fase):
    l = blank(); d = ImageDraw.Draw(l)
    for k, y in enumerate((18, 27, 36)):
        x0 = 34 + ((k + fase) % 3) * 2
        if lado < 0:
            d.line((x0, y, x0 + 9, y), fill=(255, 255, 255, 170))
        else:
            d.line((48 - x0 - 9, y, 48 - x0, y), fill=(255, 255, 255, 170))
    return l


def poeira(cx, cy, k):
    l = blank(); d = ImageDraw.Draw(l)
    for i, (dx, dy, r) in enumerate(((0, 0, 3), (4, -2, 2), (-3, -1, 2))):
        rr = r + k
        d.ellipse((cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr), fill=(226, 214, 190, 150))
    return l


def aura(cor, tam, fase):
    l = blank()
    g = Image.new('RGBA', (F, F), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((24 - tam, 26 - tam * 1.15, 24 + tam, 26 + tam * 1.15), fill=cor + (150,))
    l.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(l)
    rng = random.Random(fase)
    for _ in range(4):
        x, y = rng.randint(8, 40), rng.randint(4, 40)
        d.line((x - 1, y, x + 1, y), fill=(255, 255, 255, 230)); d.line((x, y - 1, x, y + 1), fill=(255, 255, 255, 230))
    return l


def lagrimas(olhos, comp, fase):
    l = blank(); d = ImageDraw.Draw(l)
    for i, (x, y) in enumerate(olhos):
        c = comp + ((i + fase) % 2)
        d.line((x, y + 1, x, y + 1 + c), fill=(120, 190, 255, 255))
        d.point((x, y + 2 + c), fill=(200, 235, 255, 255))
        if fase:
            d.point((x + (1 if i else -1), y + 4 + c + fase), fill=(160, 210, 255, 220))
    return l


def deitado(img, sinal=-1):
    """Personagem deitado (cabeca para a direita quando sinal=-1)."""
    bb = img.getbbox()
    if not bb:
        return img.copy()
    fig = img.crop(bb)
    fig = fig.rotate(90 * sinal, expand=True, resample=Image.NEAREST)
    out = blank()
    x = (F - fig.width) // 2
    y = 46 - fig.height
    out.alpha_composite(fig, (max(0, x), max(0, y)))
    return out


# ---------------------------------------------------------------- poses
def make_sheet(key, p):
    fr = base_frames(key)
    L, D, U = fr[4][1], fr[2][1], fr[8][1]
    if p['sleeve'] is None:
        p = dict(p)
        p['sleeve'] = sample(D, 14, 28, (120, 100, 140))
        p['leg'] = sample(D, 21, 40, (60, 50, 70))
        p['shoe'] = sample(D, 21, 45, (50, 40, 30))
    hip, sh = p['hip'], p['shoulder']
    rows = {}

    # corrida
    def corrida_l(f):
        b = shift(rot(fr[4][f], 10), 0, [-2, 0, -2][f])
        extra = [linhas_velocidade(-1, f)]
        if f == 1:
            extra.append(poeira(34, 44, 0))
        return over(*extra, b)
    side = [corrida_l(f) for f in range(3)]
    rows['corrida'] = {4: side, 6: [mirror(x) for x in side],
                       2: [over(poeira(18 if f != 1 else 30, 45, 0) if f == 1 else blank(), shift(fr[2][f], 0, [-2, 0, -2][f])) for f in range(3)],
                       8: [shift(fr[8][f], 0, [-2, 0, -2][f]) for f in range(3)]}

    # chute
    def chute_l(f):
        corpo = L
        if f == 0:
            return rot(scale_b(corpo, 1.0, 0.95), -6)
        if f == 1:
            perna = membro(p, (24, hip), (5, hip - 4), p['leg'], p['shoe'], raio=3, largura=5)
            sopro = blank(); sd = ImageDraw.Draw(sopro)
            sd.arc((-2, hip - 14, 14, hip + 6), 110, 250, fill=(255, 255, 255, 200), width=2)
            return over(sopro, rot(over(corpo, perna), -14))
        perna = membro(p, (24, hip), (14, hip), p['leg'], p['shoe'], raio=3, largura=5)
        return rot(over(corpo, perna), -6)
    side = [chute_l(f) for f in range(3)]
    rows['chute'] = {4: side, 6: [mirror(x) for x in side], 2: [mirror(x) for x in side], 8: side}

    # soco e facada
    def soco_l(f, faca=False):
        if f == 0:
            return rot(L, -5)
        alcance = 4 if f == 1 else 12
        def lamina(d, ax=alcance):
            if faca:
                d.polygon([(ax - 1, sh - 2), (ax - 9, sh - 1), (ax - 1, sh + 1)], fill=(220, 226, 236, 255))
                d.line((ax - 1, sh - 2, ax - 8, sh - 1), fill=(255, 255, 255, 255))
        braco = membro(p, (24, sh), (alcance, sh - 1), p['sleeve'], p['skin'], raio=3, largura=4, extra=lamina)
        corpo = rot(over(L, braco), 6 if f == 1 else 3)
        if f == 1:
            imp = blank(); idr = ImageDraw.Draw(imp)
            for a in range(0, 360, 60):
                x, y = 2 + math.cos(math.radians(a)) * 4, sh - 1 + math.sin(math.radians(a)) * 4
                idr.line((2, sh - 1, x, y), fill=(255, 250, 200, 230))
            corpo = over(corpo, imp)
        return corpo
    for nome, faca in (('soco', False), ('facada', True)):
        side = [soco_l(f, faca) for f in range(3)]
        rows[nome] = {4: side, 6: [mirror(x) for x in side], 2: [mirror(x) for x in side], 8: side}

    # dor
    def dor(img, f, lean=True):
        if f == 0:
            b = rot(img, -12) if lean else img
            b = shift(tint(b, (255, 255, 255), 0.55), 2, 0)
            return over(b, estrelas(3, 26, 6, 9, 0.3))
        if f == 1:
            b = rot(img, -18) if lean else shift(img, -2, 0)
            b = shift(tint(b, (255, 60, 60), 0.3), 3 if lean else 0, 0)
            return over(b, estrelas(3, 26, 6, 9, 1.4))
        return shift(rot(img, -8) if lean else img, 1, 0)
    side = [dor(L, f) for f in range(3)]
    rows['dor'] = {4: side, 6: [mirror(x) for x in side], 2: [dor(D, f, False) for f in range(3)],
                   8: [dor(U, f, False) for f in range(3)]}

    # queda (cai para tras e fica deitado)
    lying = deitado(L, -1)
    head_x = 40
    side = [rot(L, -45), lying, over(lying, estrelas(4, head_x - 4, 26, 8, 0.0))]
    rows['queda'] = {4: side, 6: [mirror(x) for x in side], 2: side, 8: [mirror(x) for x in side]}

    # rastejar (deitado, braco esticado para frente)
    def rast(f):
        b = shift(lying, -1 if f == 1 else 0, 0)
        if f == 1:
            braco = membro(p, (16, 40), (4, 39), p['sleeve'], p['skin'], raio=2, largura=3)
            b = over(b, braco)
        return b
    side = [rast(f) for f in range(3)]
    rows['rastejar'] = {4: [mirror(x) for x in side], 6: side, 2: side, 8: [mirror(x) for x in side]}

    # magia
    def magia(img, f):
        tam = [12, 18, 15][f]
        return over(aura(p['aura'], tam, f), shift(img, 0, [-1, -3, -2][f]))
    rows['magia'] = {d: [magia(fr[d][1], f) for f in range(3)] for d in (2, 4, 6, 8)}

    # cansado
    def cansado(img, f, side_sign=0):
        b = scale_b(img, 1.0, [0.9, 0.94, 0.9][f])
        if side_sign:
            b = rot(b, 12 * side_sign)
        gotas = gotas_suor([(34, 8 + f * 2), (13, 12 + (2 - f))]) if f != 1 else gotas_suor([(35, 12)])
        return over(b, gotas)
    rows['cansado'] = {2: [cansado(D, f) for f in range(3)], 8: [cansado(U, f) for f in range(3)],
                       4: [cansado(L, f, 1) for f in range(3)]}
    rows['cansado'][6] = [mirror(x) for x in rows['cansado'][4]]

    # choro
    def choro(img, olhos, f):
        b = shift(img, [0, 1, -1][f], 0)
        if olhos:
            olhos2 = [(x + [0, 1, -1][f], y) for (x, y) in olhos]
            b = over(b, lagrimas(olhos2, [3, 6, 4][f], f))
        return b
    rows['choro'] = {2: [choro(D, p['eyes'], f) for f in range(3)], 8: [choro(U, None, f) for f in range(3)],
                     4: [choro(L, [p['eye_side']], f) for f in range(3)]}
    rows['choro'][6] = [mirror(x) for x in rows['choro'][4]]

    # riso
    def riso(img, f):
        b = shift(scale_b(img, 1.0, 0.95 if f == 1 else 1.0), 0, [-3, 0, -2][f])
        if f != 1:
            l = blank(); d = ImageDraw.Draw(l)
            d.line((37, 8, 41, 5), fill=(255, 255, 255, 230)); d.line((38, 12, 43, 11), fill=(255, 255, 255, 230))
            d.line((10, 8, 6, 5), fill=(255, 255, 255, 230)); d.line((9, 12, 4, 11), fill=(255, 255, 255, 230))
            b = over(b, l)
        return b
    rows['riso'] = {d: [riso(fr[d][1], f) for f in range(3)] for d in (2, 4, 6, 8)}

    # pulo
    rows['pulo'] = {d: [scale_b(fr[d][1], 1.12, 0.86), scale_b(fr[d][1], 0.9, 1.08), fr[d][1].copy()] for d in (2, 4, 6, 8)}

    sheet = Image.new('RGBA', (F * 12, F * len(ROWS)), (0, 0, 0, 0))
    for r, nome in enumerate(ROWS):
        for di, d in enumerate((2, 4, 6, 8)):
            for f in range(3):
                sheet.alpha_composite(rows[nome][d][f], ((di * 3 + f) * F, r * F))
    return sheet


def nome_folha(key):
    return 'Pose_' + key.replace('$', '').replace('#', '_')


def main():
    sheets = {}
    for key, p in ALVOS.items():
        sh = make_sheet(key, p)
        nome = nome_folha(key)
        sh.save(CHARS + nome + '.png')
        sheets[key] = nome
    with open(PROJ + '/data/Poses.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'rows': ROWS, 'sheets': sheets}, f, ensure_ascii=False, separators=(',', ':'))
    pl = open(PROJ + '/js/plugins.js', encoding='utf-8').read()
    if '"Poses"' not in pl:
        entry = '{"name":"Poses","status":true,"description":"Poses de ação para os personagens.","parameters":{}}'
        pl = pl.replace('\n];', ',\n' + entry + '\n];')
        open(PROJ + '/js/plugins.js', 'w', encoding='utf-8', newline='\n').write(pl)
    # previa: Baratelli, Leona, Kevinho e Gusrola humano, olhando para a esquerda
    pv = Image.new('RGBA', (F * 3 * 4 + 30, F * len(ROWS)), (110, 140, 100, 255))
    for i, key in enumerate(['$Baratelli_Cigana', '$Leona', '$Kevinho', 'People1#2']):
        sh = Image.open(CHARS + nome_folha(key) + '.png')
        pv.alpha_composite(sh.crop((F * 3, 0, F * 6, F * len(ROWS))), (i * (F * 3 + 10), 0))
    pv.resize((pv.width * 2, pv.height * 2), Image.NEAREST).save(PREV + 'poses.png')
    print('poses:', len(sheets), 'folhas')


if __name__ == '__main__':
    main()
