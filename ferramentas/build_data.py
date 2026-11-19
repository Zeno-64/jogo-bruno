# Monta o mapa, os eventos e o banco de dados do jogo (RPG Maker MZ).
import json, re, random

PROJ = 'K:/Kevin/workspace/jogo-bruno'
random.seed(42)


def load(name):
    with open(f'{PROJ}/data/{name}', encoding='utf-8') as f:
        return json.load(f)


def save(name, obj):
    with open(f'{PROJ}/data/{name}', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))


# ------------------------------------------------------------ autotiles
core = open(f'{PROJ}/js/rmmz_core.js', encoding='utf-8').read()
FLOOR = json.loads(re.search(r'Tilemap\.FLOOR_AUTOTILE_TABLE\s*=\s*(\[.*?\]);', core, re.S).group(1))
assert len(FLOOR) == 48


def classify(q, sx, sy):
    if sy < 2:
        return (False, False, True)
    h_open = (sx == 0) if q in (0, 2) else (sx == 3)
    v_open = (sy == 2) if q in (0, 1) else (sy == 5)
    return (h_open, v_open, False)


SHAPE_OF = {}
for shape, quarters in enumerate(FLOOR):
    key = tuple(classify(q, sx, sy) for q, (sx, sy) in enumerate(quarters))
    SHAPE_OF.setdefault(key, shape)


def floor_shape(same):
    """same(dx, dy) -> True se o vizinho e do mesmo tipo."""
    key = []
    for q, (hx, vy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
        h_open = not same(hx, 0)
        v_open = not same(0, vy)
        diag_open = (not h_open) and (not v_open) and (not same(hx, vy))
        key.append((h_open, v_open, diag_open))
    return SHAPE_OF[tuple(key)]


# sanity: todas as 256 combinacoes de vizinhos tem um formato
for m in range(256):
    nb = {(dx, dy): bool(m >> i & 1) for i, (dx, dy) in enumerate(
        [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)])}
    floor_shape(lambda dx, dy: nb[(dx, dy)])

W, H = 25, 19
A1, A2 = 2048, 2816
MEADOW = A2 + 0 * 48
DIRT_K = 1        # Dirt (Meadow)
MOSS_K = 23       # Moss (decoracao)
WATER_K = 8       # Water C (Dirt), A1


def auto_layer(cells, base_id, also_same=frozenset()):
    out = {}
    group = set(cells) | set(also_same)
    for (x, y) in cells:
        def same(dx, dy, x=x, y=y):
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or nx >= W or ny >= H:
                return True
            return (nx, ny) in group
        out[(x, y)] = base_id + floor_shape(same)
    return out


data = [0] * (W * H * 6)


def put(x, y, z, tid):
    data[(z * H + y) * W + x] = tid


# chao: grama
for y in range(H):
    for x in range(W):
        put(x, y, 0, MEADOW)

# estrada de terra
road = set()
for y in range(0, H):
    road |= {(2, y), (3, y)}
for y in range(15, H):
    road |= {(x, y) for x in range(1, 6)}
road |= {(4, 13), (5, 13), (6, 13), (7, 13), (4, 14), (5, 14)}
puddles = {(3, 6), (4, 16), (5, 16)}
for (x, y), t in auto_layer(road - puddles, A2 + DIRT_K * 48, also_same=puddles).items():
    put(x, y, 0, t)
for (x, y), t in auto_layer(puddles, A1 + WATER_K * 48).items():
    put(x, y, 0, t)

# trilhos (folha D, ids 512/513) na linha 11
for x in range(W):
    put(x, 11, 2, 513 if random.random() < 0.3 else 512)

# floresta no topo
used = set()


def b(x, y, tid, z=2):
    assert (x, y, z) not in used, (x, y, z)
    used.add((x, y, z))
    put(x, y, z, tid)


for x in range(0, 24, 2):
    if x in (2,):
        continue
    b(x, 0, 176); b(x + 1, 0, 177); b(x, 1, 184); b(x + 1, 1, 185)
b(24, 0, 157); b(24, 1, 165)
for x in (0, 5, 9, 14, 19, 23):
    b(x, 2, 157); b(x, 3, 165)
b(11, 2, 232); b(11, 3, 240)
# arvores secas perto do trem
b(12, 8, 232); b(12, 9, 240)
b(5, 7, 232); b(5, 8, 240)
# placa
b(1, 9, 137)
# tocos, pedras, tronco, arbustos
for (x, y, t) in [(15, 14, 156), (21, 15, 243), (22, 13, 167), (17, 16, 171), (7, 16, 171),
                  (20, 17, 164), (0, 13, 166), (24, 13, 166), (0, 17, 166)]:
    b(x, y, t)
flowers = [(14, 6), (19, 5), (21, 8), (16, 9), (9, 16), (18, 13), (23, 16), (7, 17), (12, 5), (24, 4)]
for i, (x, y) in enumerate(flowers):
    b(x, y, 160 + i % 4)
tufts = [(13, 4), (18, 7), (22, 5), (11, 14), (14, 17), (20, 12), (6, 17), (24, 9), (1, 13),
         (16, 4), (10, 17), (0, 6), (1, 4), (13, 9), (23, 10), (17, 10),
         (5, 12), (11, 12), (5, 10), (11, 10), (12, 12), (4, 10)]
for i, (x, y) in enumerate(tufts):
    b(x, y, [152, 154, 155, 153][i % 4])

# ------------------------------------------------------------ eventos
def cmd(code, params, ind=0):
    return {'code': code, 'indent': ind, 'parameters': params}


def text(lines, face='', idx=0, name='', bg=0, pos=2, ind=0):
    return [cmd(101, [face, idx, bg, pos, name], ind)] + [cmd(401, [l], ind) for l in lines]


def se(name, ind=0, vol=90):
    return [cmd(250, [{'name': name, 'volume': vol, 'pitch': 100, 'pan': 0}], ind)]


END = cmd(0, [])


def page(lst, image=None, trigger=0, priority=1, move_type=0, speed=3, freq=3,
         self_switch=None, dir_fix=False, step=False, through=False):
    img = {'characterIndex': 0, 'characterName': '', 'direction': 2, 'pattern': 1, 'tileId': 0}
    if image:
        img.update(image)
    return {
        'conditions': {'actorId': 1, 'actorValid': False, 'itemId': 1, 'itemValid': False,
                       'selfSwitchCh': self_switch or 'A', 'selfSwitchValid': bool(self_switch),
                       'switch1Id': 1, 'switch1Valid': False, 'switch2Id': 1, 'switch2Valid': False,
                       'variableId': 1, 'variableValid': False, 'variableValue': 0},
        'directionFix': dir_fix, 'image': img, 'list': lst + [END],
        'moveFrequency': freq,
        'moveRoute': {'list': [{'code': 0, 'parameters': []}], 'repeat': True, 'skippable': False, 'wait': False},
        'moveSpeed': speed, 'moveType': move_type, 'priorityType': priority,
        'stepAnime': step, 'through': through, 'trigger': trigger, 'walkAnime': True,
    }


events = [None]


def add_event(name, x, y, pages):
    eid = len(events)
    events.append({'id': eid, 'name': name, 'note': '', 'pages': pages, 'x': x, 'y': y})
    return eid


BF = dict(face='Baratelli', idx=0, name='Baratelli')

# 1 introducao
add_event('Introducao', 0, 18, [
    page([cmd(223, [[5, 10, 20, 70], 1, False]), cmd(230, [30])]
         + text(['Uma manhã de neblina perto da antiga linha de trem...'])
         + text(['Dizem que por aqui vive alguém que ama trens, tarô...',
                 'e ler a mão das pessoas.'])
         + [cmd(123, ['A', 0])], trigger=3, priority=0),
    page([], trigger=0, priority=0, self_switch='A'),
])

# 2 Baratelli
add_event('Baratelli', 8, 13, [
    page(text(['Oii! Meu nome é Baratelli,', 'tenho 19 aninhos! Hihi :3'], **BF)
         + text(['Eu amo tarô e amo trens...', 'Olha esse aqui atrás de mim!', 'Não é lindo? *-*'], **BF)
         + text(['Meu sonho é ler a mão de todas', 'as pessoas do mundo!'], **BF)
         + text(['Eu tenho 17 sobrinhos, mas dois', 'são especiais: o Kevino Oh Kevino',
                 'e o Gusrola. Eles são meus', 'amores queridos! S2'], **BF)
         + text(['Todo dia, antes de vir pro trabalho,', 'eu ajudo vários moradores de rua.',
                 'Isso me dá forças pra continuar', 'firme no meu querido trabalho!'], **BF)
         + [cmd(123, ['A', 0]), cmd(117, [1])],
         image={'characterName': '$Baratelli', 'direction': 2}),
    page(text(['Voltou! Hihi :3'], **BF) + [cmd(117, [1])],
         image={'characterName': '$Baratelli', 'direction': 2}, self_switch='A'),
])

# 3 e 4 sobrinhos
add_event('Kevino', 6, 14, [page(
    text(['Eu sou o Kevino Oh Kevino!', 'A tia Baratelli é a melhor tia', 'do mundo! S2'],
         face='People1', idx=0, name='Kevino'),
    image={'characterName': 'People1', 'characterIndex': 0, 'direction': 6})])
add_event('Gusrola', 10, 14, [page(
    text(['Eu sou o Gusrola!', 'A tia já leu minha mão umas 300', 'vezes. Sempre dá trem, hihi.'],
         face='People1', idx=2, name='Gusrola'),
    image={'characterName': 'People1', 'characterIndex': 2, 'direction': 4})])

# 5 trem + bloqueios ao redor
add_event('Trem', 8, 11, [page([cmd(117, [2])],
                               image={'characterName': '!$TremVelho', 'direction': 2, 'pattern': 1},
                               dir_fix=True)])
for (x, y) in [(6, 11), (7, 11), (9, 11), (10, 11), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10)]:
    add_event('Trem (bloqueio)', x, y, [page([cmd(117, [2])])])

# placa
add_event('Placa', 1, 9, [page(text(['ESTAÇÃO NEBLINA — DESATIVADA', '',
                                     '(Alguém escreveu embaixo: "trens são vida S2")']))])

# ovelhas
for (x, y) in [(14, 5), (17, 6), (20, 4), (15, 8), (19, 9), (22, 7)]:
    add_event('Ovelha', x, y, [page(se('Sheep') + text(['Béééé!'], name='Ovelha'),
                                    image={'characterName': '$Ovelha', 'direction': random.choice([2, 4, 6])},
                                    move_type=1, speed=2, freq=3)])

# ------------------------------------------------------------ mapa
m = load('Map001.json')
m.update({
    'width': W, 'height': H, 'tilesetId': 2, 'data': data, 'events': events,
    'displayName': 'Velha Estação na Neblina', 'note': '<neblina:150>',
    'autoplayBgm': True, 'bgm': {'name': 'Town1', 'pan': 0, 'pitch': 100, 'volume': 70},
    'autoplayBgs': True, 'bgs': {'name': 'Wind1', 'pan': 0, 'pitch': 100, 'volume': 30},
    'scrollType': 0, 'disableDashing': False,
})
save('Map001.json', m)

mi = load('MapInfos.json')
mi[1]['name'] = 'Velha Estação'
save('MapInfos.json', mi)

# ------------------------------------------------------------ eventos comuns
ce1 = (text(['Posso ler a sua mão?'], **BF)
       + [cmd(102, [['Pode ler!', 'Agora não'], 1, 0, 2, 0]),
          cmd(402, [0, 'Pode ler!'])]
       + text(['Deixa eu ver essa mãozinha...', 'Hmmmm...'], ind=1, **BF)
       + se('Magic3', ind=1)
       + [cmd(122, [1, 1, 0, 2, 1, 5], 1)])
palm = [
    ['Vejo uma viagem de trem no seu', 'futuro! Piuí! *-*'],
    ['Sua linha da vida é looonga!', 'Vai durar mais que esse trem velho,', 'hihi.'],
    ['Hmm... vejo uma ovelha muito', 'importante no seu caminho.', 'Fique de olho!'],
    ['Vejo muito amor! Igual o que eu', 'sinto pelos meus 17 sobrinhos S2'],
    ['Sua mão diz que hoje é um ótimo', 'dia pra ajudar alguém!'],
]
for k, lines in enumerate(palm, 1):
    ce1 += [cmd(111, [1, 1, 0, k, 0], 1)] + text(lines, ind=2, **BF) + [cmd(0, [], 2), cmd(412, [], 1)]
ce1 += text(['Agora, uma carta de tarô pra você!'], ind=1, **BF) + se('Book1', ind=1) + [cmd(122, [2, 2, 0, 2, 1, 6], 1)]
tarot = [
    ['O Sol! Dias de alegria e calor...', 'mesmo com essa neblina, hihi.'],
    ['A Estrela! Esperança! Seus sonhos', 'estão no caminho certo.'],
    ['O Carro! Movimento e conquista...', 'é praticamente um trem! *-*'],
    ['A Roda da Fortuna! A vida gira', 'igual roda de trem!'],
    ['O Louco! Uma aventura nova vai', 'começar!'],
    ['O Mundo! Um ciclo se completa.', 'Que lindo!'],
]
for k, lines in enumerate(tarot, 1):
    ce1 += [cmd(111, [1, 2, 0, k, 0], 1)] + text(lines, ind=2, **BF) + [cmd(0, [], 2), cmd(412, [], 1)]
ce1 += text(['Volte sempre! Ainda faltam muitas', 'mãos no mundo pra eu ler! :3'], ind=1, **BF)
ce1 += [cmd(0, [], 1), cmd(402, [1, 'Agora não'])]
ce1 += text(['Tudo bem! Mas um dia eu vou ler', 'a mão de todo mundo, hihi :3'], ind=1, **BF)
ce1 += [cmd(0, [], 1), cmd(404, []), END]

ce2 = (text(['Um trem antigo, todo enferrujado e coberto de musgo.',
             'Parece que está parado aqui há muitos anos...'])
       + text(['Tem uma foto presa na porta do trem...'])
       + se('Book2')
       + [cmd(231, [1, 'Foto_Baratelli', 1, 0, 408, 312, 100, 100, 255, 0])]
       + text(['É a Baratelli, toda feliz, posando na frente',
               'desse mesmo trem!'], bg=1)
       + [cmd(235, [1]), END])

ce = load('CommonEvents.json')
ce[1] = {'id': 1, 'list': ce1, 'name': 'Leitura de Mão', 'switchId': 1, 'trigger': 0}
ce[2] = {'id': 2, 'list': ce2, 'name': 'Trem Antigo', 'switchId': 1, 'trigger': 0}
save('CommonEvents.json', ce)

# ------------------------------------------------------------ sistema e tileset
s = load('System.json')
s.update({'startMapId': 1, 'startX': 3, 'startY': 17, 'partyMembers': [1],
          'title1Name': 'Baratelli', 'title2Name': ''})
s['variables'][1] = 'Leitura de mão'
s['variables'][2] = 'Carta de tarô'
save('System.json', s)

ts = load('Tilesets.json')
ts[2]['tilesetNames'][7] = 'Trilhos'
save('Tilesets.json', ts)

print('eventos', len(events) - 1, 'shapes ok', len(SHAPE_OF))
