# Monta o Capitulo 1: mapa-mundi, Recife, Sao Matheos, casa do Gusrola, Luz da Se (patio e estacao).
import json, re, random, copy
from collections import deque
import numpy as np
from fx import destaque, capitulo, pose

PROJ = 'K:/Kevin/workspace/jogo-bruno'
random.seed(1)


def load(name):
    with open(f'{PROJ}/data/{name}', encoding='utf-8-sig') as f:
        return json.load(f)


def save(name, obj):
    with open(f'{PROJ}/data/{name}', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))


TILESETS = load('Tilesets.json')

# ------------------------------------------------------------ autotiles
core = open(f'{PROJ}/js/rmmz_core.js', encoding='utf-8').read()
FLOOR = json.loads(re.search(r'Tilemap\.FLOOR_AUTOTILE_TABLE\s*=\s*(\[.*?\]);', core, re.S).group(1))
WALLT = json.loads(re.search(r'Tilemap\.WALL_AUTOTILE_TABLE\s*=\s*(\[.*?\]);', core, re.S).group(1))


def classify(q, sx, sy):
    if sy < 2:
        return (False, False, True)
    h_open = (sx == 0) if q in (0, 2) else (sx == 3)
    v_open = (sy == 2) if q in (0, 1) else (sy == 5)
    return (h_open, v_open, False)


FLOOR_OF = {}
for shape, quarters in enumerate(FLOOR):
    FLOOR_OF.setdefault(tuple(classify(q, sx, sy) for q, (sx, sy) in enumerate(quarters)), shape)

WALL_OF = {}
for shape, quarters in enumerate(WALLT):
    (tlx, tly), (trx, try_), (blx, bly), (brx, bry) = quarters
    WALL_OF[(tlx == 0, tly == 0, trx == 3, bry == 3)] = shape
assert len(WALL_OF) == 16


def floor_shape(same):
    key = []
    for (hx, vy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        h_open = not same(hx, 0)
        v_open = not same(0, vy)
        diag_open = (not h_open) and (not v_open) and (not same(hx, vy))
        key.append((h_open, v_open, diag_open))
    return FLOOR_OF[tuple(key)]


def wall_shape(same):
    return WALL_OF[(not same(-1, 0), not same(0, -1), not same(1, 0), not same(0, 1))]


A1, A2, A3, A4 = 2048, 2816, 4352, 5888
C0, D0, E0 = 256, 512, 768
E_TOCA = E0 + 5
IT_CHAVE, IT_BANANA_DOURADA = 41, 40


def registrar_tileset_e():
    """Folha E do Exterior (Morro_E): cascas de banana, rachadura, tabua de ponte, toca de rato e cocos."""
    ts = load('Tilesets.json')
    t = ts[2]
    t['tilesetNames'][8] = 'Morro_E'
    for n in (0, 1, 2, 3, 4):
        t['flags'][E0 + n] = 0x600       # passaveis, por baixo dos personagens
    t['flags'][E0 + 5] = 0x610           # toca: estrela (desenhada por cima)
    t['flags'][E0 + 6] = 0x60f           # monte de cocos: bloqueia
    save('Tilesets.json', ts)
    TILESETS[:] = ts


class Map:
    def __init__(self, w, h, tileset):
        self.w, self.h, self.ts = w, h, tileset
        self.data = [0] * (w * h * 6)
        self.events = [None]

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def put(self, x, y, z, tid):
        if self.inside(x, y):
            self.data[(z * self.h + y) * self.w + x] = tid

    def get(self, x, y, z):
        return self.data[(z * self.h + y) * self.w + x]

    def auto(self, cells, base, z, same_extra=(), wall=False):
        cells = set(c for c in cells if self.inside(*c))
        group = cells | set(same_extra)
        for (x, y) in cells:
            def same(dx, dy, x=x, y=y):
                nx, ny = x + dx, y + dy
                if not self.inside(nx, ny):
                    return True
                return (nx, ny) in group
            self.put(x, y, z, base + (wall_shape(same) if wall else floor_shape(same)))

    def region(self, cells, rid=1):
        for (x, y) in cells:
            self.put(x, y, 5, rid)

    def passable(self, x, y):
        if not self.inside(x, y) or self.get(x, y, 5) == 1:
            return False
        flags = TILESETS[self.ts]['flags']
        for z in (3, 2, 1, 0):
            tid = self.get(x, y, z)
            f = flags[tid]
            if f & 0x10:
                continue
            return (f & 0x0F) != 0x0F
        return False

    def reach(self, start, blocked=()):
        seen = {start}; q = deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in seen and n not in blocked and self.passable(*n):
                    seen.add(n); q.append(n)
        return seen

    def add_event(self, name, x, y, pages):
        eid = len(self.events)
        self.events.append({'id': eid, 'name': name, 'note': '', 'pages': pages, 'x': x, 'y': y})
        return eid


def rect(x0, y0, x1, y1):
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


def building(m, x0, x1, roof_y0, roof_y1, wall_y0, wall_y1, roof_kind, wall_kind):
    m.auto(rect(x0, roof_y0, x1, roof_y1), A3 + roof_kind * 48, 0, wall=True)
    m.auto(rect(x0, wall_y0, x1, wall_y1), A3 + wall_kind * 48, 0, wall=True)


def room(m, x0, y0, x1, y1, top_kind, side_kind, floor_kind, door=None):
    """Interior: teto (A4 topo) na borda, parede (A4 lado) com 2 linhas no alto e chao."""
    ceiling = set()
    for x in range(x0, x1 + 1):
        ceiling |= {(x, y0), (x, y1)}
    for y in range(y0, y1 + 1):
        ceiling |= {(x0, y), (x1, y)}
    if door:
        ceiling.discard(door)
    walls = rect(x0 + 1, y0 + 1, x1 - 1, y0 + 2)
    floor = rect(x0 + 1, y0 + 3, x1 - 1, y1 - 1) | ({door} if door else set())
    m.auto(ceiling, A4 + top_kind * 48, 0)
    m.auto(walls, A4 + side_kind * 48, 0, wall=True)
    m.auto(floor, A2 + floor_kind * 48, 0)
    m.region(ceiling)
    return floor


def value_noise(w, h, cells, octaves, seed):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        n = cells * (2 ** o)
        g = rng.random((n + 1, n + 1))
        ys = np.linspace(0, n, h, endpoint=False); xs = np.linspace(0, n, w, endpoint=False)
        y0 = ys.astype(int); x0 = xs.astype(int)
        fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
        fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)
        a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
        acc += (a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy) * amp
        tot += amp; amp *= 0.5
    return acc / tot


# ------------------------------------------------------------ comandos de evento
def cmd(code, params, ind=0):
    return {'code': code, 'indent': ind, 'parameters': params}


def text(lines, face='', idx=0, name='', bg=0, pos=2, ind=0):
    return [cmd(101, [face, idx, bg, pos, name], ind)] + [cmd(401, [l], ind) for l in lines]


BF = dict(face='Baratelli', idx=0, name='Baratelli')


def bar(*lines, ind=0):
    return text(list(lines), ind=ind, **BF)


def npc(name, *lines, face='', idx=0, ind=0):
    return text(list(lines), face=face, idx=idx, name=name, ind=ind)


def narr(*lines, ind=0, bg=0):
    return text(list(lines), ind=ind, bg=bg)


def audio(name, vol=90, pitch=100):
    return {'name': name, 'volume': vol, 'pitch': pitch, 'pan': 0}


def se(name, ind=0, vol=90, pitch=100):
    return [cmd(250, [audio(name, vol, pitch)], ind)]


def bgm(name, ind=0, vol=80):
    return [cmd(241, [audio(name, vol)], ind)]


def me(name, ind=0, vol=90):
    return [cmd(249, [audio(name, vol)], ind)]


def wait(f, ind=0):
    return [cmd(230, [f], ind)]


def balloon(char, bid, ind=0, w=True):
    return [cmd(213, [char, bid, w], ind)]


def tint(tone, dur=0, ind=0, w=False):
    return [cmd(223, [tone, dur, w], ind)]


def flash(color, dur, ind=0, w=True):
    return [cmd(224, [color, dur, w], ind)]


def shake(power, speed, dur, ind=0, w=True):
    return [cmd(225, [power, speed, dur, w], ind)]


def transfer(map_id, x, y, d=0, fade=0, ind=0):
    return [cmd(201, [0, map_id, x, y, d, fade], ind)]


def switch(sid, on=True, ind=0):
    return [cmd(121, [sid, sid, 0 if on else 1], ind)]


def var_set(vid, value, ind=0):
    return [cmd(122, [vid, vid, 0, 0, value], ind)]


def self_sw(ch='A', on=True, ind=0):
    return [cmd(123, [ch, 0 if on else 1], ind)]


def pic(pid, name, x, y, opacity=255, origin=1, scale=100, ind=0):
    return [cmd(231, [pid, name, origin, 0, x, y, scale, scale, opacity, 0], ind)]


def move_pic(pid, x, y, opacity, dur, scale=100, origin=1, w=False, ind=0):
    return [cmd(232, [pid, None, origin, 0, x, y, scale, scale, opacity, 0, dur, w, 0], ind)]


def erase_pic(pid, ind=0):
    return [cmd(235, [pid], ind)]


def anim(char, aid, ind=0, w=True):
    return [cmd(212, [char, aid, w], ind)]


NIGHT = [-68, -68, 0, 68]
DARK = [-90, -85, -20, 80]
NORMAL = [0, 0, 0, 0]
PINK = [40, -10, 40, 0]

# rotas de movimento
DOWN, LEFT, RIGHT, UP = 1, 2, 3, 4
TOWARD, AWAY = 10, 11


def rc(code, *params):
    return {'code': code, 'parameters': list(params)}


def route(steps, repeat=False, skippable=False, wait=True):
    lst = [s if isinstance(s, dict) else rc(s) for s in steps]
    return {'list': lst + [rc(0)], 'repeat': repeat, 'skippable': skippable, 'wait': wait}


def move(char, steps, w=True, skippable=True, ind=0, repeat=False):
    r = route(steps, repeat=repeat, skippable=skippable, wait=w)
    return [cmd(205, [char, r], ind)] + [cmd(505, [s], ind) for s in r['list'][:-1]]


def face_event(eid):
    return rc(45, f'this.turnTowardCharacter($gameMap.event({eid}))')


END = cmd(0, [])


def if_(params, then, els=None):
    sub = lambda lst: [dict(c, indent=c['indent'] + 1) for c in lst]
    out = [cmd(111, params)] + sub(then) + [cmd(0, [], 1)]
    if els is not None:
        out += [cmd(411, [])] + sub(els) + [cmd(0, [], 1)]
    return out + [cmd(412, [])]


def item(iid, n):
    return [cmd(126, [iid, 0 if n >= 0 else 1, 0, abs(n)])]


def page(lst, image=None, trigger=0, priority=1, move_type=0, speed=3, freq=3,
         sw1=None, sw2=None, var=None, self_switch=None, dir_fix=False, step=False,
         through=False, walk=True, mroute=None):
    img = {'characterIndex': 0, 'characterName': '', 'direction': 2, 'pattern': 1, 'tileId': 0}
    if image:
        img.update(image)
    return {
        'conditions': {'actorId': 1, 'actorValid': False, 'itemId': 1, 'itemValid': False,
                       'selfSwitchCh': self_switch or 'A', 'selfSwitchValid': bool(self_switch),
                       'switch1Id': sw1 or 1, 'switch1Valid': bool(sw1),
                       'switch2Id': sw2 or 1, 'switch2Valid': bool(sw2),
                       'variableId': var[0] if var else 1, 'variableValid': bool(var),
                       'variableValue': var[1] if var else 0},
        'directionFix': dir_fix, 'image': img, 'list': lst + [END],
        'moveFrequency': freq,
        'moveRoute': mroute or {'list': [rc(0)], 'repeat': True, 'skippable': False, 'wait': False},
        'moveSpeed': speed, 'moveType': move_type, 'priorityType': priority,
        'stepAnime': step, 'through': through, 'trigger': trigger, 'walkAnime': walk,
    }


def ambient(m, tone):
    """Evento paralelo que acerta a cor da tela ao entrar no mapa."""
    m.add_event('Ambiente', 0, 0, [page(tint(tone, 0) + [cmd(214, [])], trigger=4, priority=0)])


# switches e variaveis
S_MONARK, S_NOITE, S_SINO, S_FIM = 1, 2, 3, 4
V_CHECK = 3
M_RECIFE, M_MUNDO, M_MATHEOS, M_GUSROLA, M_PATIO, M_ESTACAO = 1, 2, 3, 4, 5, 6

# ============================================================ 1. RECIFE
def build_recife():
    m = Map(27, 19, 2)
    W, H = m.w, m.h
    MEADOW, COBBLE, SAND = 0, 3, 16
    m.auto(rect(0, 0, W - 1, H - 1), A2 + MEADOW * 48, 0)
    road = rect(0, 6, W - 1, 8)
    m.auto(road, A2 + COBBLE * 48, 0)
    sand = rect(0, 14, W - 1, 15)
    sea = rect(0, 16, W - 1, H - 1)
    m.auto(sand, A2 + SAND * 48, 0)
    m.auto(sea, A1 + 10 * 48, 0)
    # casas e escola
    building(m, 1, 5, 2, 3, 4, 5, 1, 11)       # casa rosa
    building(m, 7, 11, 2, 3, 4, 5, 2, 9)       # casa laranja
    building(m, 14, 24, 1, 3, 4, 5, 7, 10)     # escola
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y) in [(3, 5), (9, 5), (19, 5)]:
        b(x, y, 131)
    for (x, y) in [(2, 4), (4, 4), (8, 4), (10, 4), (15, 4), (16, 4), (22, 4), (23, 4)]:
        b(x, y, 96)
    b(18, 4, 73); b(20, 4, 73)            # placas misticas
    b(1, 2, 128, 3); b(10, 2, 136, 3)    # chamines
    # arvores atras das casas
    for x in list(range(0, 14)) + [25, 26]:
        b(x, 0, 157); b(x, 1, 165)
    b(12, 3, 157); b(12, 4, 165); b(13, 3, 157); b(13, 4, 165)
    b(25, 2, 157); b(25, 3, 165); b(26, 3, 157); b(26, 4, 165)
    b(6, 3, 166); b(6, 4, 245); b(0, 4, 245); b(25, 5, 245); b(26, 5, 166)
    # praca: palmeiras, flores, pedras
    palms = [(2, 10), (8, 12), (16, 10), (22, 12), (25, 9), (5, 14), (19, 14)]
    for (x, y) in palms:
        b(x, y - 1, 236); b(x, y, 244)
    for i, (x, y) in enumerate([(4, 10), (6, 11), (9, 10), (14, 12), (17, 12), (20, 10), (23, 10), (1, 12),
                                (10, 13), (24, 13), (3, 13), (15, 9)]):
        b(x, y, 160 + i % 4)
    for (x, y) in [(7, 9), (18, 9), (21, 13), (13, 13)]:
        b(x, y, 250)
    b(17, 6, 137)  # placa da escola
    return m


def events_recife(m):
    ambient(m, NORMAL)
    # 2 intro
    intro = (capitulo('Capitulo1')
             + narr('Continente da Gordura do Amor.', 'Recife, a capital: praias, capivaras e ovelhas.')
             + narr('Mais um dia começa, e Baratelli está',
                    'atrasada para a aula de leitura de mãos...')
             + balloon(-1, 1)
             + bar('Ai, ai, ai! Tô atrasada de novo!', 'A escola fica logo ali na frente!')
             + self_sw())
    m.add_event('Introdução', 0, 18, [page(intro, trigger=3, priority=0),
                                         page([], priority=0, self_switch='A')])
    # 3 Monark
    monark = m.add_event('Monark', 16, 7, [
        page([], image={'characterName': '$Monark', 'direction': 4}),
        page([], sw1=S_MONARK, priority=0),
    ])
    # 4.. gatilhos do esbarrao na coluna x=12
    cena = (se('Run')
            + move(-1, [rc(29, 5), RIGHT], w=True)
            + move(monark, [TOWARD] * 12, w=True)
            + move(-1, [face_event(monark)], w=True)
            + se('Blow1') + shake(5, 8, 12) + pose(-1, 'dor')
            + move(-1, [rc(35), rc(14, -1, 0), rc(36), rc(29, 4)], w=True)
            + balloon(-1, 6)
            + narr('PÁ! Baratelli esbarrou em alguém!')
            + bar('Ai! Me perdoa, sou muito', 'descuidada, hihi!')
            + bar('Estou atrasada pra minha aula de', 'leitura de mãos...')
            + balloon(-1, 4)
            + bar('...mas sinto que meu coração', 'palpita na sua presença, hihihi!')
            + narr('Era um cigano grande e forte, de olhar',
                   'misterioso, que dizia ver o futuro das pessoas.')
            + npc('Cigano', 'Meu nome é Monark.')
            + balloon(monark, 5)
            + npc('Monark', 'Agora cala a boca! Você nunca vai',
                  'conseguir ler o futuro sendo tão', 'submissa assim!')
            + pose(monark, 'soco', olhar=-1, espera=8)
            + se('Blow3') + shake(7, 9, 15) + pose(-1, 'dor')
            + move(-1, [rc(35), rc(14, -1, 0), rc(36)], w=True)
            + pose(-1, 'queda', segurar=True)
            + balloon(-1, 6)
            + bar('M-me desculpa... por favor...')
            + se('Cry1', vol=70) + pose(-1, 'choro', repetir=True, segurar=True)
            + narr('Baratelli chora aos prantos.')
            + npc('Monark', 'Escute bem. Venha à estação de trem',
                  'abandonada, a Luz da Sé, à meia-noite.')
            + pose(monark, 'riso', repetir=True, segurar=True)
            + npc('Monark', 'Lá eu te ensino as artes de ler o', 'futuro. Hahaha!')
            + pose(monark, '')
            + move(monark, [rc(37), RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, rc(39)], w=True)
            + switch(S_MONARK) + pose(-1, '')
            + wait(30)
            + bar('(Snif... Tenho que ser forte!', 'Pelo futuro dos moradores de rua', 'e das minorias!)')
            + bar('(Preciso contar isso pro Gusrola!', 'Ele mora em São Matheos, a oeste.)')
            + narr('Saia de Recife pelo lado esquerdo', 'para chegar ao mapa do mundo.'))
    for y in range(6, 16):
        m.add_event('Esbarrão', 12, y, [page(cena, trigger=1, priority=0),
                                        page([], sw1=S_MONARK, priority=0)])
    # escola
    m.add_event('Porta da escola', 19, 5, [
        page(bar('A sala de leitura de mãos fica', 'aqui dentro... corre, Baratelli!')),
        page(bar('A aula já começou faz tempo...', 'Melhor ir falar com o Gusrola.'), sw1=S_MONARK),
    ])
    for (x, y) in [(3, 5), (9, 5)]:
        m.add_event('Porta', x, y, [page(narr('A porta está trancada.'))])
    m.add_event('Placa da escola', 17, 6, [page(narr('ESCOLA DE ARTES MÍSTICAS DE RECIFE',
                                                    'Hoje: aula de leitura de mãos!'))])
    # saida para o mapa do mundo
    for y in (6, 7, 8):
        m.add_event('Saída', 0, y, [
            page(bar('Não dá pra voltar agora!', 'Tô atrasada pra aula!')
                 + move(-1, [RIGHT], w=True), trigger=1, priority=0),
            page(transfer(M_MUNDO, 29, 38, 2), trigger=1, priority=0, sw1=S_MONARK),
        ])
    # capivaras e ovelhas
    for (x, y) in [(5, 11), (11, 10), (21, 11)]:
        m.add_event('Capivara', x, y, [page(narr('A capivara te olha com toda a calma', 'do mundo.'),
                                            image={'characterName': '$Capivara', 'direction': 2},
                                            move_type=1, speed=2, freq=2)])
    for (x, y) in [(14, 11), (24, 11), (7, 13)]:
        m.add_event('Ovelha', x, y, [page(se('Sheep') + npc('Ovelha', 'Béééé!'),
                                          image={'characterName': '$Ovelha', 'direction': 4},
                                          move_type=1, speed=2, freq=3)])
    return monark


# ============================================================ 2. MAPA DO MUNDO
def build_world():
    m = Map(60, 48, 1)
    W, H = m.w, m.h
    n1 = value_noise(W, H, 4, 4, 11)
    n2 = value_noise(W, H, 5, 3, 22)
    n3 = value_noise(W, H, 6, 3, 33)
    land = np.zeros((H, W), bool)
    north = np.zeros((H, W), bool); south = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            dn = ((x - 30) / 24) ** 2 + ((y - 11) / 8.2) ** 2 - 0.55 * (n1[y, x] - 0.5)
            ds = ((x - 30) / 23) ** 2 + ((y - 35.5) / 9.8) ** 2 - 0.55 * (n1[y, x] - 0.5)
            if dn < 1 and 2 <= y <= 19:
                north[y, x] = True
            if ds < 1 and 26 <= y <= 46:
                south[y, x] = True
    # baia de Recife
    for y in range(40, H):
        for x in range(W):
            if abs(x - 30) <= (y - 39) * 1.0:
                south[y, x] = False
    # lugares e estradas
    RECIFE = [(29, 36), (30, 36), (29, 37), (30, 37)]
    MATHEOS = [(17, 30), (18, 30), (17, 31), (18, 31)]
    LUZ = [(44, 29), (44, 30)]
    road = set()
    road |= {(x, 38) for x in range(17, 45)}
    road |= {(17, y) for y in range(32, 39)}
    road |= {(44, y) for y in range(31, 39)}
    keep = set(road) | set(RECIFE) | set(MATHEOS) | set(LUZ)
    near = set()
    for (x, y) in keep:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                near.add((x + dx, y + dy))
    for (x, y) in near:
        if 0 <= x < W and 0 <= y < H and y <= 39:
            south[y, x] = True
    land = north | south
    # rios
    river_s = {(21, y) for y in range(41, H)} | rect(20, 40, 22, 41) | {(38, y) for y in range(22, 31)} | {(37, 30), (37, 31)}
    poison = {(24, y) for y in range(1, 11)} | {(25, 10), (26, 10), (27, 10), (27, 11), (28, 11)}
    poison |= {(36, y) for y in range(1, 11)} | {(35, 10), (34, 10), (33, 10), (33, 11), (32, 11)}
    for (x, y) in river_s:
        if m.inside(x, y):
            land[y, x] = False
    sea = {(x, y) for y in range(H) for x in range(W) if not land[y, x]}
    # distancia ate a terra para o mar profundo e a areia
    dist = np.full((H, W), 99)
    q = deque()
    for y in range(H):
        for x in range(W):
            if land[y, x]:
                dist[y, x] = 0; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if m.inside(nx, ny) and dist[ny, nx] > dist[y, x] + 1:
                dist[ny, nx] = dist[y, x] + 1; q.append((nx, ny))
    deep = {(x, y) for (x, y) in sea if dist[y, x] >= 3 and (x, y) not in river_s}
    m.auto(sea, A1 + 0 * 48, 0)
    m.auto(deep, A1 + 1 * 48, 1)   # mar profundo tem bordas transparentes: vai por cima do mar
    # distancia ate o mar (para praias)
    sdist = np.full((H, W), 99)
    q = deque()
    for (x, y) in sea:
        if (x, y) not in river_s:
            sdist[y, x] = 0; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if m.inside(nx, ny) and sdist[ny, nx] > sdist[y, x] + 1:
                sdist[ny, nx] = sdist[y, x] + 1; q.append((nx, ny))
    # chao
    kinds = {}
    for y in range(H):
        for x in range(W):
            if not land[y, x]:
                continue
            if north[y, x] and y <= 20:
                k = 8
                if n2[y, x] > 0.6:
                    k = 18
                elif n2[y, x] < 0.36:
                    k = 10
            else:
                k = 0 if n2[y, x] < 0.62 else 2
                if sdist[y, x] <= 1 and (y >= 39 or 24 <= x <= 37 and y >= 37):
                    k = 16
                if abs(x - 44) <= 3 and abs(y - 30) <= 2:
                    k = 10
            kinds[(x, y)] = k
    # jardins da mansao
    for (x, y) in rect(26, 9, 34, 15):
        if (x, y) in kinds:
            kinds[(x, y)] = 0
    for k in set(kinds.values()):
        cells = {c for c, v in kinds.items() if v == k}
        m.auto(cells, A2 + k * 48, 0)
    m.auto(poison, A1 + 4 * 48, 0)
    # sobreposicoes: florestas, montanhas, estradas
    over = {}
    for (x, y), k in kinds.items():
        if (x, y) in near or (x, y) in poison:
            continue
        if north[y, x] and y <= 20:
            if (y <= 5 or n3[y, x] > 0.68) and not ((26 <= x <= 34 and 8 <= y <= 16)):
                over[(x, y)] = 22 if n1[y, x] > 0.45 else 7
            elif n3[y, x] < 0.38:
                over[(x, y)] = 12
        else:
            if (x >= 47 and 32 <= y <= 41 or x <= 11 and 33 <= y <= 41) and n3[y, x] > 0.42:
                over[(x, y)] = 6
            elif sdist[y, x] <= 2 and n2[y, x] > 0.45 and k != 16:
                over[(x, y)] = 20
            elif n3[y, x] > 0.6:
                over[(x, y)] = 4
            elif abs(x - 44) <= 4 and abs(y - 30) <= 3 and n3[y, x] < 0.45:
                over[(x, y)] = 12
    for (x, y) in rect(26, 9, 34, 15):
        over.pop((x, y), None)
    for c in [(26, 9), (34, 9), (26, 15), (34, 15), (27, 15), (33, 9)]:
        if c in kinds and c not in poison:
            over[c] = 4
    over = {c: k for c, k in over.items() if c not in river_s}
    for k in set(over.values()):
        m.auto({c for c, v in over.items() if v == k}, A2 + k * 48, 1)
    m.auto(road, A2 + 13 * 48, 1)
    # icones
    for (x, y), t in zip(RECIFE, [C0 + 128, C0 + 129, C0 + 136, C0 + 137]):
        m.put(x, y, 2, t)
    for (x, y), t in zip(MATHEOS, [C0 + 74, C0 + 75, C0 + 82, C0 + 83]):
        m.put(x, y, 2, t)
    m.put(44, 29, 2, C0 + 118); m.put(44, 30, 2, C0 + 126)
    mansion = [[144, 145, 146], [152, 153, 154], [160, 161, 162]]
    for dy, row in enumerate(mansion):
        for dx, t in enumerate(row):
            m.put(29 + dx, 11 + dy, 2, t)
    m.put(23, 15, 2, 163); m.put(24, 15, 2, 164)
    m.put(36, 15, 2, 165); m.put(37, 15, 2, 166)
    m.put(30, 27, 2, C0 + 1)   # placa na costa norte
    return m, RECIFE, MATHEOS, LUZ


def events_world(m, RECIFE, MATHEOS, LUZ):
    m.add_event('Ambiente', 0, 0, [
        page(tint(NORMAL, 0) + [cmd(214, [])], trigger=4, priority=0),
        page(tint(NIGHT, 0) + [cmd(214, [])], trigger=4, priority=0, sw1=S_NOITE),
    ])
    intro = (wait(20)
             + narr('Este é o nosso mundo, dividido em', 'dois continentes.')
             + [cmd(204, [8, 24, 4, True])]
             + narr('Ao norte fica o Continente Sodoma de Calvice:',
                    'seca, morte e trevas, com rios químicos que',
                    'descem do extremo norte.')
             + narr('Os rios terminam na Mansão do Fuhrer Raulete,',
                    'em São Berunado: muros, jardins e flores...',
                    'e duas cidades com tudo sugado por ela.')
             + narr('Dizem que o careca Raulete tenta criar uma',
                    'fórmula de cabelos loiros para curar a sua',
                    'careca.')
             + [cmd(204, [2, 24, 4, True])]
             + narr('Ao sul fica o Continente da Gordura do Amor:',
                    'colorido, cheio de árvores, flores e rios',
                    'limpinhos. No centro, a capital Recife.')
             + narr('Siga a estrada para o oeste até São Matheos,',
                    'onde mora o Gusrola.')
             + self_sw())
    m.add_event('Introdução', 0, 1, [page(intro, trigger=3, priority=0),
                                       page([], priority=0, self_switch='A')])
    # Recife (linha de baixo do icone)
    for (x, y) in RECIFE[2:]:
        m.add_event('Recife', x, y, [
            page(transfer(M_RECIFE, 1, 7, 6), trigger=1, priority=0),
            page(bar('Não dá tempo de voltar pra casa!', 'O Monark me espera à meia-noite!')
                 + move(-1, [DOWN], w=True), trigger=1, priority=0, sw1=S_NOITE),
        ])
    for (x, y) in MATHEOS[2:]:
        m.add_event('São Matheos', x, y, [
            page(transfer(M_MATHEOS, 10, 13, 8), trigger=1, priority=0),
            page(bar('Já falei com o Gusrola.', 'Agora, para a Luz da Sé!')
                 + move(-1, [DOWN], w=True), trigger=1, priority=0, sw1=S_NOITE),
        ])
    m.add_event('Luz da Sé', 44, 30, [
        page(narr('A estação de trem abandonada Luz da Sé.')
             + bar('O Monark disse meia-noite...', 'Ainda é cedo.')
             + move(-1, [DOWN], w=True), trigger=1, priority=0),
        page(var_set(V_CHECK, 1) + transfer(M_PATIO, 12, 16, 8), trigger=1, priority=0, sw1=S_NOITE),
    ])
    m.add_event('Placa da costa', 30, 27, [page(
        narr('"Do outro lado do mar: Sodoma de Calvice.',
             'Cuidado com a mansão de São Berunado!"'))])


# ============================================================ 3. SAO MATHEOS
def build_matheos():
    m = Map(21, 15, 2)
    W, H = m.w, m.h
    m.auto(rect(0, 0, W - 1, H - 1), A2 + 8 * 48, 0)
    n = value_noise(W, H, 3, 3, 5)
    soil = {(x, y) for x in range(W) for y in range(5, H) if n[y, x] > 0.55}
    m.auto(soil, A2 + 15 * 48, 1)
    houses = [(1, 4, 1, 2, 3, 4, 2), (7, 11, 1, 2, 3, 4, 9), (14, 18, 1, 2, 3, 4, 16), (13, 17, 8, 9, 10, 11, 15)]
    for (x0, x1, r0, r1, w0, w1, door) in houses:
        building(m, x0, x1, r0, r1, w0, w1, 5, 12)
        m.put(door, w1, 2, 131)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y, t) in [(1, 3, 52), (4, 4, 53), (8, 3, 54), (11, 4, 55), (14, 4, 49), (18, 3, 50),
                      (13, 10, 51), (17, 11, 52), (10, 3, 56), (3, 4, 57)]:
        b(x, y, t)
    for (x, y) in [(1, 1), (4, 2), (8, 1), (11, 2), (15, 1), (18, 2), (14, 9)]:
        b(x, y, 169)  # buracos no telhado
    # lixo
    trash = [(5, 5, 141), (6, 5, 181), (0, 6, 182), (12, 5, 144), (13, 5, 183), (19, 6, 141),
             (3, 8, C0 + 26), (6, 9, C0 + 29), (2, 11, 164), (8, 11, C0 + 30), (19, 9, 189),
             (11, 8, 190), (5, 13, 191), (16, 13, C0 + 24), (19, 12, C0 + 25), (0, 13, 144),
             (12, 12, 149), (4, 7, 171), (9, 9, 171), (18, 7, 171), (1, 9, 239), (7, 7, 239),
             (15, 6, 239), (12, 10, 239), (19, 3, 156), (6, 2, 232), (6, 3, 240), (12, 1, 232), (12, 2, 240)]
    for (x, y, t) in trash:
        b(x, y, t)
    b(7, 6, 137)  # placa
    return m


def events_matheos(m):
    ambient(m, NORMAL)
    m.add_event('Chegada', 0, 14, [
        page(narr('São Matheos: uma cidadezinha pobre e imunda,',
                  'com 4 casas meio destruídas e muito lixo.')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    m.add_event('Porta do Gusrola', 9, 4, [page(
        se('Door1') + transfer(M_GUSROLA, 6, 8, 8), trigger=1, priority=0)])
    for (x, y) in [(2, 4), (16, 4), (15, 11)]:
        m.add_event('Porta', x, y, [page(narr('Não tem ninguém em casa... e a porta', 'está caindo aos pedaços.'))])
    m.add_event('Placa', 7, 6, [page(narr('SÃO MATHEOS', 'População: pouca. Lixo: muito.'))])
    for y in (13, 14):
        pass
    for x in range(8, 13):
        m.add_event('Saída', x, 14, [page(transfer(M_MUNDO, 17, 32, 2), trigger=1, priority=0)])
    for (x, y) in [(4, 9), (16, 7)]:
        m.add_event('Rato', x, y, [page(se('Cancel2') + bar('Eca, um rato!'),
                                        image={'characterName': '$Rato', 'direction': 2},
                                        move_type=1, speed=4, freq=4)])


# ============================================================ 4. CASA DO GUSROLA
def build_gusrola():
    m = Map(13, 10, 3)
    room(m, 0, 0, 12, 9, 19, 27, 2, door=(6, 9))
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y, t) in [(2, 3, 171), (2, 4, 179), (10, 2, 175), (10, 3, 183), (6, 1, 86), (3, 1, 216),
                      (8, 5, 238), (9, 5, 239), (7, 5, 120), (10, 7, 220), (11, 8, 237), (1, 8, 228),
                      (11, 4, 236), (1, 6, 248), (4, 8, 27), (9, 1, 36), (4, 2, 37)]:
        b(x, y, t)
    return m


def events_gusrola(m):
    ambient(m, NORMAL)
    G = dict(face='People1', idx=2)
    gus = m.add_event('Gusrola', 6, 5, [
        page(npc('Gusrola', 'Hehehe... o que foi, titia?', **G),
             image={'characterName': 'People1', 'characterIndex': 2, 'direction': 2}),
        page(npc('Gusrola', 'Vai logo, titia! Não deixa o cigano', 'esperando! Hehehe...', **G),
             image={'characterName': 'People1', 'characterIndex': 2, 'direction': 2}, sw1=S_NOITE),
    ])
    dance_pics = [
        (2, 'Feliz_Coracao', 150, 170), (3, 'Feliz_Flor', 670, 160), (4, 'Feliz_ArcoIris', 408, 150),
        (5, 'Feliz_Ovelha', 170, 420), (6, 'Feliz_Capivara', 650, 420),
    ]
    danca = (bgm('Town3', vol=85) + tint(PINK, 40)
             + move(-1, [rc(29, 4)] + [rc(18), rc(15, 6), rc(19), rc(15, 6), rc(17), rc(15, 6), rc(16), rc(15, 6),
                                        rc(14, 0, 0), rc(15, 4)] * 4, w=False))
    for (pid, name, x, y) in dance_pics:
        danca += pic(pid, name, x, y + 20, opacity=0, scale=80)
        danca += move_pic(pid, x, y, 255, 40, scale=100)
        danca += balloon(-1, 4 if pid % 2 else 3, w=False) + wait(45)
    danca += wait(60)
    for (pid, name, x, y) in dance_pics:
        danca += move_pic(pid, x, y - 30, 0, 50, scale=120)
    danca += wait(60) + [cmd(242, [3])] + [cmd(221, [])]
    for (pid, _, _, _) in dance_pics:
        danca += erase_pic(pid)
    cena = (wait(15)
            + move(gus, [rc(25)], w=True)
            + balloon(-1, 4)
            + bar('Gusrola! Acho que encontrei o', 'amor da minha vida!')
            + bar('Um cigano grande e forte,', 'igualzinho aos meus sonhos!')
            + balloon(gus, 8)
            + npc('Gusrola', 'Hahaha! Sua boba... acha mesmo que', 'alguém pode te amar, além daquela',
                  'que te deu à luz? Hahaha!', **G)
            + balloon(-1, 3)
            + bar('Hihihi! Gusrola, você é muito', 'engraçado!')
            + narr('Baratelli riu inocentemente, achando', 'que era tudo uma piada.')
            + bar('Ele me chamou pra encontrar com ele', 'à meia-noite, na Luz da Sé!')
            + balloon(gus, 1)
            + tint([-40, -40, -20, 60], 20, w=True)
            + npc('Gusrola', '(Heh... então o cigano que o Raulete', 'mandou já começou o serviço...)', **G)
            + tint(NORMAL, 20, w=True)
            + npc('Gusrola', 'Vá, minha titia querida! Encontre', 'esse cigano e desperte o seu',
                  'verdadeiro potencial!', **G)
            + balloon(-1, 4)
            + pose(-1, 'riso', espera=10)
            + bar('Aaaah, que felicidade! Hihihi!')
            + narr('Baratelli fica tão feliz que começa a dançar',
                   'O Lago dos Cisnes no meio da sala!')
            + danca
            + narr('Passam-se as horas...')
            + narr('...e já é quase meia-noite.')
            + switch(S_NOITE) + tint(NIGHT, 0)
            + transfer(M_MUNDO, 17, 32, 2, fade=2)
            + [cmd(222, [])]
            + bar('Hora de ir pra estação Luz da Sé!', 'Fica a leste, depois de Recife.'))
    # a cena comeca quando a Baratelli fala com o Gusrola (antes disso, a casa pode ser explorada)
    m.events[gus]['pages'].insert(1, page(cena, image={'characterName': 'People1', 'characterIndex': 2, 'direction': 2},
                                          sw1=S_MONARK))
    chegada = (bar('Gusrola! Cheguei!')
               + npc('Gusrola', 'Hehehe... entra, titia. Fica à vontade.', **G)
               + narr('Explore a casa e fale com o Gusrola quando', 'quiser contar a novidade.')
               + self_sw())
    m.add_event('Conversa', 0, 9, [page(chegada, trigger=3, priority=0, sw1=S_MONARK),
                                   page([], priority=0, self_switch='A')])
    m.add_event('Saída', 6, 9, [page(se('Door1') + transfer(M_MATHEOS, 9, 5, 2), trigger=1, priority=0)])
    return gus


# ============================================================ 5. LUZ DA SE - PATIO (labirinto dos ratos)
LANE_WALLS = {5: [12], 8: [2, 22], 11: [12], 14: [3, 21]}
W_PATIO = 25


def build_patio():
    m = Map(25, 19, 2)
    W, H = m.w, m.h
    SAND, FENCE = 16, 14
    m.auto(rect(0, 0, W - 1, H - 1), A2 + SAND * 48, 0)
    n = value_noise(W, H, 3, 3, 9)
    m.auto({(x, y) for x in range(W) for y in range(4, H) if n[y, x] > 0.58}, A2 + 15 * 48, 1)
    building(m, 7, 17, 0, 1, 2, 3, 5, 10)
    m.put(12, 3, 2, 131)
    m.put(11, 2, 2, 79); m.put(13, 2, 2, 79)
    m.put(9, 2, 2, 104); m.put(15, 2, 2, 104); m.put(8, 3, 2, 52); m.put(16, 2, 2, 53)
    walls = set()
    for x in list(range(0, 7)) + list(range(18, 25)):
        walls.add((x, 3))
    for y in range(4, H):
        walls |= {(0, y), (W - 1, y)}
    walls |= {(x, H - 1) for x in range(W) if x != 12}
    for y, gaps in LANE_WALLS.items():
        walls |= {(x, y) for x in range(W) if x not in gaps}
    islands = {(5, 9), (9, 9), (16, 9), (19, 9), (7, 13), (17, 13)}
    debris_ids = [181, 182, 183, 189, 190, 191, 141, 159, 167, C0 + 26, C0 + 29, C0 + 30, C0 + 17, C0 + 18, 180, 188]
    rng = random.Random(3)
    debris = set(islands)
    for c in sorted(walls):
        x, y = c
        if y in LANE_WALLS and 1 <= x <= 23 and rng.random() < 0.35:
            debris.add(c)
    lamps = {(3, 8), (21, 8)}
    debris -= lamps
    fence = walls - debris - lamps
    m.auto(fence, A2 + FENCE * 48, 1)
    for c in sorted(debris):
        m.put(c[0], c[1], 2, rng.choice(debris_ids))
    # postes de luz nos checkpoints
    for x in (3, 21):
        m.put(x, 6, 3, 8); m.put(x, 7, 3, 16); m.put(x, 8, 2, 24)
    # arvores secas no fundo
    for x in (1, 4, 19, 22):
        m.put(x, 1, 2, 232); m.put(x, 2, 2, 240)
    for (x, y) in [(2, 0), (5, 1), (20, 0), (23, 1), (0, 1), (24, 2)]:
        m.put(x, y, 2, 159 if (x + y) % 2 else 167)
    for (x, y) in [(2, 16), (22, 16), (4, 17), (20, 17), (1, 15), (23, 15)]:
        m.put(x, y, 2, rng.choice([181, 141, C0 + 26]))
    # tocas de onde sai a manada de ratos (y=10)
    m.put(0, 10, 3, E_TOCA); m.put(W - 1, 10, 3, E_TOCA)
    return m


def rato(m, x, y, chamada, speed=4, d=4):
    """Rato com movimento esperto (plugin Patrulhas): morde ao encostar."""
    m.add_event('Rato', x, y, [page(
        [cmd(117, [1])], image={'characterName': '$Rato', 'direction': d},
        trigger=2, move_type=3, speed=speed, freq=5,
        mroute=route([rc(45, chamada)], repeat=True, skippable=True, wait=False))])


def events_patio(m):
    ambient(m, DARK)
    m.add_event('Chegada', 0, 18, [
        page(bgm('Dungeon3', vol=70)
             + narr('Luz da Sé... uma estação de trem abandonada,', 'cercada de destroços.')
             + se('Cat', pitch=150, vol=60)
             + balloon(-1, 1)
             + bar('Ratos! Muitos ratos!', 'Se eles me pegarem...')
             + narr('Chegue até a porta da estação sem ser pega',
                    'pelos ratos. Segure Shift para correr.')
             + narr('Cuidado: alguns ratos farejam quem chega', 'perto, e os da toca correm em bando!')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    # porta trancada: a chave fica no fim do corredor de cima, a esquerda
    abrir = (se('Key') + narr('Clec! O cadeado enferrujado abre.') + item(IT_CHAVE, -1) + self_sw('A')
             + se('Door2') + transfer(M_ESTACAO, 10, 11, 8))
    primeira = (se('Buzzer1') + bar('Trancada?! Tem um cadeado enferrujado', 'aqui!')
                + narr('Lá no fim do corredor, à esquerda, alguma', 'coisa brilha...')
                + self_sw('B'))
    m.add_event('Porta da estação', 12, 3, [
        page(if_([8, IT_CHAVE], abrir,
                 if_([2, 'B', 0], se('Buzzer1') + bar('Trancada! Cadê aquela chave...'), primeira)),
             trigger=1, priority=1),
        page(se('Door2') + transfer(M_ESTACAO, 10, 11, 8), trigger=1, priority=0, self_switch='A'),
    ])
    m.add_event('Chave', 1, 4, [
        page(se('Item1') + item(IT_CHAVE, 1)
             + destaque('item', imagem='Item_Chave', nome='Chave Enferrujada', texto='Abre o cadeado da estação.')
             + bar('A chave! Agora é voltar até a porta...', 'sem virar petisco de rato.') + self_sw(),
             image={'characterName': '!$Brilho', 'direction': 2}, trigger=1, priority=0, step=True),
        page([], priority=0, self_switch='A'),
    ])
    m.add_event('Placa', 11, 3, [page(narr('ESTAÇÃO LUZ DA SÉ', '(desativada)'))])
    for x in (2, 22):
        m.add_event('Checkpoint', x, 8, [
            page([cmd(111, [1, V_CHECK, 0, 2, 0])] + [cmd(0, [], 1), cmd(411, [])]
                 + var_set(V_CHECK, 2, ind=1) + se('Save2', ind=1)
                 + destaque('aviso', icone=212, nome='Checkpoint!', texto='Se um rato te pegar, você volta pra cá.', ind=1)
                 + [cmd(0, [], 1), cmd(412, [])], trigger=1, priority=0),
        ])
    m.add_event('Voltar', 12, 18, [page(transfer(M_MUNDO, 44, 31, 2), trigger=1, priority=0)])
    # corredor 1 (y 12-13): um rato de ponta a ponta, dois vigiando as entradas
    # e um farejador perto da saida do meio
    rato(m, 8, 12, 'this.patrulhar(1, 23, 0)', speed=4, d=6)
    rato(m, 5, 13, 'this.patrulhar(1, 6, 0)', speed=3, d=4)
    rato(m, 19, 13, 'this.patrulhar(18, 23, 0)', speed=3, d=6)
    rato(m, 12, 13, 'this.patrulhar(9, 15, 3, 5, 12, 13)', speed=3, d=4)
    # corredor 2 (y 9-10): manada saindo da toca da direita, patrulheiro e farejador na saida esquerda
    for k in range(3):
        rato(m, W_PATIO - 1, 10, f'this.correrLinha({W_PATIO - 1}, 0, 34, 0, false, {k * 16})', speed=5, d=4)
    rato(m, 12, 9, 'this.patrulhar(10, 15, 0)', speed=4, d=6)
    rato(m, 3, 9, 'this.patrulhar(1, 4, 2, 5, 9, 10)', speed=3, d=4)
    # corredor 3 (y 6-7): dois ratos se cruzando, um bem rapido
    rato(m, 20, 6, 'this.patrulhar(1, 23, 0)', speed=5, d=4)
    rato(m, 6, 7, 'this.patrulhar(1, 23, 0)', speed=4, d=6)
    # corredor da porta (y 4): um rato rapido entre a chave e a porta
    rato(m, 16, 4, 'this.patrulhar(4, 20, 0)', speed=5, d=4)


def ce_pego():
    falas = [('Aaai! Um rato me mordeu!',), ('Socorro! Ele mordeu meu dedão!',),
             ('Ai! Esse rato tem dente de tubarão!',), ('Eca! Ele me lambeu E me mordeu!',)]
    sorteio = [cmd(122, [5, 5, 0, 2, 0, len(falas) - 1])]
    for i, f in enumerate(falas):
        sorteio += [cmd(111, [1, 5, 0, i, 0])] + bar(*f, ind=1) + [cmd(0, [], 1), cmd(412, [])]
    lst = (se('Bite') + flash([255, 40, 40, 170], 20) + shake(4, 9, 10, w=False)
           + pose(-1, 'dor')
           + sorteio
           + [cmd(111, [1, V_CHECK, 0, 2, 0])] + transfer(M_PATIO, 2, 8, 8, ind=1)
           + [cmd(0, [], 1), cmd(411, [])] + transfer(M_PATIO, 12, 16, 8, ind=1)
           + [cmd(0, [], 1), cmd(412, []), END])
    return {'id': 1, 'list': lst, 'name': 'Pega pelos ratos', 'switchId': 1, 'trigger': 0}


# ============================================================ 6. ESTACAO LUZ DA SE (interior)
def build_estacao():
    m = Map(21, 13, 2)
    floor = room(m, 0, 0, 20, 12, 16, 24, 19, door=(10, 12))
    for x in range(1, 20):
        m.put(x, 7, 2, 513 if random.random() < 0.35 else 512)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y, t) in [(3, 1, 104), (16, 1, 104), (2, 2, 49), (7, 1, 50), (12, 2, 51), (14, 1, 54), (5, 2, 53),
                      (18, 1, 57), (1, 3, C0 + 17), (13, 4, C0 + 18), (2, 10, C0 + 26), (17, 10, 181),
                      (18, 10, 141), (19, 9, 182), (1, 9, C0 + 29), (15, 9, 239), (4, 11, 171),
                      (12, 9, 171), (8, 10, C0 + 24), (19, 11, 190)]:
        b(x, y, t)
    return m


def events_estacao(m):
    ambient(m, NIGHT)
    m.add_event('Chegada', 0, 12, [
        page(bgm('Dungeon6', vol=55) + [cmd(245, [audio('Wind1', 40)])]
             + narr('Dentro da Luz da Sé, tudo está em silêncio.')
             + bar('Monark? Cadê você?')
             + balloon(-1, 8)
             + bar('(Hmm... ali no canto tem o sino do', 'trem. Será que eu toco?)')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    trem = m.add_event('Trem', 7, 7, [page(
        narr('O velho trem da Luz da Sé, todo enferrujado.', 'Parado aqui há muitos e muitos anos...'),
        image={'characterName': '!$TremVelho', 'direction': 2, 'pattern': 1}, dir_fix=True)])
    for (x, y) in [(5, 7), (6, 7), (8, 7), (9, 7), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)]:
        m.add_event('Trem (bloqueio)', x, y, [page(narr('O velho trem da Luz da Sé, todo enferrujado.'))])
    sino = m.add_event('Sino', 18, 3, [
        page(move(0, [rc(33)], w=False)
             + se('Bell3') + wait(30) + se('Bell3') + wait(30) + se('Bell3')
             + narr('DLÉM! DLÉM! DLÉM!')
             + move(0, [rc(34)], w=False)
             + switch(S_SINO),
             image={'characterName': '!$Sino', 'direction': 2, 'pattern': 1}, dir_fix=True),
        page(narr('O sino ainda está vibrando...'),
             image={'characterName': '!$Sino', 'direction': 2, 'pattern': 1}, dir_fix=True, sw1=S_SINO),
    ])
    MK = 'Monark'
    final = (wait(30) + [cmd(242, [2])]
             + se('Door2')
             + balloon(-1, 1)
             + move(-1, [rc(29, 4)], w=True)
             + bar('Monark!')
             + bgm('Scene4', vol=65))
    monark_eid = len(m.events)
    final += (move(monark_eid, [rc(29, 3)] + [TOWARD] * 12, w=True)
              + move(-1, [face_event(monark_eid)], w=True)
              + npc(MK, 'Vejo que você veio, pequena.')
              + balloon(-1, 4)
              + bar('Eu tenho que despertar todas as', 'minhas habilidades... pra ajudar', 'a ler o futuro!')
              + npc(MK, 'Hmpf. Antes de tudo, precisamos', 'fazer um ritual.')
              + npc(MK, 'Me dê a sua mão.')
              + balloon(-1, 6)
              + bar('(Que vergonha... mas é pelo', 'bem maior!)')
              + bar('T-tudo bem!')
              + [cmd(242, [1])]
              + se('Darkness3') + anim(-1, 101)
              + flash([170, 60, 255, 200], 30, w=False) + shake(6, 8, 30)
              + pose(-1, 'dor', segurar=True)
              + bar('AAAAAI! Que dor!!')
              + se('Pollen') + anim(-1, 33)
              + [cmd(322, [1, '$Baratelli_Flor', 0, 'Baratelli', 0, ''])]
              + pose(-1, '')
              + narr('Uma flor começou a brotar da cabeça', 'de Baratelli!')
              + me('Curse1')
              + destaque('maldicao', imagem='Evento_Flor', nome='Flor da Calvície',
                         texto='Quando a última pétala cair, Baratelli ficará calva.')
              + balloon(monark_eid, 1)
              + pose(monark_eid, 'riso', repetir=True, segurar=True)
              + npc(MK, 'Hahahaha! Caiu direitinho!')
              + pose(monark_eid, '')
              + npc(MK, 'Quando a última pétala dessa flor cair,', 'você vai ficar calva e infeliz...', 'para sempre!')
              + npc(MK, '...a não ser que encontre a lendária')
              + destaque('evento', imagem='Peruca_Ouro', titulo='A LENDA', nome='Peruca de Ouro',
                         texto='Dizem que ela cura qualquer calvície.')
              + npc(MK, 'PERUCA DE OURO!')
              + pose(monark_eid, 'riso', repetir=True, segurar=True)
              + npc(MK, 'Mande lembranças ao Fuhrer Raulete!', 'Hahahaha!')
              + pose(monark_eid, '')
              + move(monark_eid, [rc(37), rc(29, 4)] + [DOWN] * 10 + [rc(39)], w=True)
              + switch(S_FIM)
              + bgm('Scene2', vol=60)
              + balloon(-1, 6)
              + pose(-1, 'choro', repetir=True, segurar=True)
              + bar('Snif... snif...', 'Ele me enganou...')
              + narr('Baratelli olha com raiva enquanto Monark',
                     'desaparece na escuridão.')
              + pose(-1, '')
              + bar('Nunca mais vou cair na conversa', 'de ninguém!')
              + se('Fall', vol=70)
              + narr('Uma mecha do seu cabelo cai no chão...')
              + balloon(-1, 1)
              + narr('Baratelli pega a mecha num gesto de ódio', 'e determinação.')
              + me('Fanfare3')
              + pose(-1, 'magia', repetir=True, segurar=True)
              + bar('Eu vou encontrar a grande', 'PERUCA DOURADA!')
              + pose(-1, '')
              + wait(30) + [cmd(242, [3])] + [cmd(246, [3])] + [cmd(221, [])] + wait(40)
              + narr('Enquanto isso, na Mansão de São Berunado...')
              + se('Darkness1', vol=70)
              + npc('Raulete', 'Hehehe... então a flor foi plantada.')
              + npc('???', '......')
              + narr('Uma sombra sem rosto se curva diante dele.')
              + npc('Raulete', 'Continue de olho na Baratelli, Kura.')
              + npc('Raulete', 'Quando ela encontrar a Peruca de Ouro...',
                    'a peruca será MINHA, e a minha careca',
                    'finalmente terá cura! Hahahaha!')
              + me('Mystery')
              + capitulo('FimCapitulo1')
              + transfer(8, 4, 5, 6, fade=2))   # segue para o Capitulo 2 (Casa da Leandra)
    m.add_event('Monark', 10, 12, [
        page([], priority=0),
        page(final, image={'characterName': '$Monark', 'direction': 8}, trigger=3, sw1=S_SINO),
        page([], priority=0, sw1=S_FIM),
    ])
    m.add_event('Saída', 10, 12, [
        page(bar('Não vou embora sem encontrar', 'o Monark!') + move(-1, [UP], w=True), trigger=1, priority=0),
    ])
    return sino


# ============================================================ montagem
def map_json(template, m, display, bgm_name='', bgs_name='', note='', bgm_vol=70, bgs_vol=40):
    j = copy.deepcopy(template)
    j.update({
        'width': m.w, 'height': m.h, 'tilesetId': m.ts, 'data': m.data, 'events': m.events,
        'displayName': display, 'note': note,
        'autoplayBgm': bool(bgm_name), 'bgm': audio(bgm_name, bgm_vol) if bgm_name else audio('', 90),
        'autoplayBgs': bool(bgs_name), 'bgs': audio(bgs_name, bgs_vol) if bgs_name else audio('', 90),
        'scrollType': 0, 'disableDashing': False, 'encounterList': [], 'encounterStep': 30,
        'parallaxName': '', 'parallaxShow': True, 'specifyBattleback': False,
    })
    return j


def main():
    template = load('Map001.json')
    registrar_tileset_e()

    rec = build_recife(); events_recife(rec)
    world, RECIFE, MATHEOS, LUZ = build_world(); events_world(world, RECIFE, MATHEOS, LUZ)
    mat = build_matheos(); events_matheos(mat)
    gus = build_gusrola(); events_gusrola(gus)
    pat = build_patio(); events_patio(pat)
    est = build_estacao(); events_estacao(est)

    # ---- verificacoes de caminho
    r = rec.reach((1, 7))
    assert (19, 6) in r and (0, 7) in r, 'recife'
    assert all((11, y) in r and (12, y) in r for y in range(6, 16)), 'coluna do esbarrao'
    w = world.reach((29, 38))
    for c in [(17, 31), (17, 32), (44, 30), (44, 31), (29, 37), (30, 27 + 1)]:
        assert c in w, ('mundo', c)
    assert (30, 12) not in w, 'mansao alcancavel'
    mt = mat.reach((10, 13))
    assert (9, 5) in mt and (9, 4) in mt and (10, 14) in mt, 'matheos'
    gr = gus.reach((6, 8)) if hasattr(gus, 'reach') else None
    p = pat.reach((12, 16))
    assert (12, 4) in p and (12, 3) in p and (2, 8) in p and (22, 8) in p and (12, 18) in p, 'patio'
    e = est.reach((10, 11))
    assert (18, 4) in e and (17, 3) in e, 'estacao'

    maps = [
        (M_RECIFE, rec, 'Recife', 'Town2', 'Wave1', ''),
        (M_MUNDO, world, 'Mundo', 'Field1', '', ''),
        (M_MATHEOS, mat, 'São Matheos', 'Town6', 'Wind2', ''),
        (M_GUSROLA, gus, 'Casa do Gusrola', 'Scene3', '', ''),
        (M_PATIO, pat, 'Luz da Sé', '', 'Night', '<neblina:90>'),
        (M_ESTACAO, est, 'Estação Luz da Sé', '', '', ''),
    ]
    for mid, m, disp, bgmn, bgsn, note in maps:
        save(f'Map{mid:03d}.json', map_json(template, m, disp, bgmn, bgsn, note))

    names = {M_RECIFE: 'Recife', M_MUNDO: 'Mapa do Mundo', M_MATHEOS: 'São Matheos',
             M_GUSROLA: 'Casa do Gusrola', M_PATIO: 'Luz da Sé - Pátio', M_ESTACAO: 'Luz da Sé - Estação'}
    parents = {M_RECIFE: M_MUNDO, M_MATHEOS: M_MUNDO, M_GUSROLA: M_MATHEOS, M_PATIO: M_MUNDO, M_ESTACAO: M_PATIO}
    order = [M_MUNDO, M_RECIFE, M_MATHEOS, M_GUSROLA, M_PATIO, M_ESTACAO]
    mi = [None] * 7
    for o, mid in enumerate(order, 1):
        mi[mid] = {'id': mid, 'expanded': True, 'name': names[mid], 'order': o,
                   'parentId': parents.get(mid, 0), 'scrollX': 0, 'scrollY': 0}
    save('MapInfos.json', mi)

    ce = load('CommonEvents.json')
    ce[1] = ce_pego()
    for i in range(2, len(ce)):
        if ce[i]:
            ce[i] = {'id': i, 'list': [END], 'name': '', 'switchId': 1, 'trigger': 0}
    save('CommonEvents.json', ce)

    s = load('System.json')
    s.update({'startMapId': M_RECIFE, 'startX': 1, 'startY': 7, 'partyMembers': [1]})
    for i, n in {1: 'Conheceu o Monark', 2: 'Noite (falou com Gusrola)', 3: 'Tocou o sino',
                 4: 'Fim do Capítulo 1'}.items():
        s['switches'][i] = n
    s['variables'][1] = ''; s['variables'][2] = ''
    s['variables'][3] = 'Checkpoint dos ratos'
    save('System.json', s)

    a = load('Actors.json')
    a[1].update({'name': 'Baratelli', 'nickname': '', 'characterName': '$Baratelli', 'characterIndex': 0,
                 'faceName': 'Baratelli', 'faceIndex': 0, 'profile': 'Sonha em ser a maior taróloga do mundo.'})
    save('Actors.json', a)

    pl = open(f'{PROJ}/js/plugins.js', encoding='utf-8').read()
    if '"Regioes"' not in pl:
        pl = pl.replace('\n];', ',\n{"name":"Regioes","status":true,"description":"Bloqueia a passagem nos tiles marcados com a região 1.","parameters":{}}\n];')
        open(f'{PROJ}/js/plugins.js', 'w', encoding='utf-8', newline='\n').write(pl)
    print('ok: eventos', {disp: len(m.events) - 1 for _, m, disp, *_ in maps})


if __name__ == '__main__':
    main()
