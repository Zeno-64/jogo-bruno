# Morro do Macaco (Capitulo 3), versao nova e maior.
# O Rei Macaco cobra pedagio: tres bananas douradas, cada uma atras de um desafio:
#   - Ilha das Cascas: chao escorregadio (regiao 3), puzzle de deslizar;
#   - Trilha das Pedras: pedras frageis (regiao 4) que desmoronam se a Baratelli parar;
#   - Corredor dos Cocos: um macaco joga cocos que rolam pelo corredor.
# Com as tres, os macacos montam uma ponte ate o labirinto e a casa da vidente.
import os, random, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ch1 as B
from build_ch1 import (Map, rect, building, cmd, text, narr, se, wait, balloon, flash, shake, transfer,
                       switch, self_sw, rc, move, page, A4, END, E0, IT_BANANA_DOURADA)
from build_ch2 import if_, choices, script, item, fadeout, fadein, img
from fx import destaque, pose

M_MORRO, M_VIDENTE = 13, 14
S_C3_KEV, S_C3_TOPO = 16, 17
S_PONTE = 21
V_BANANAS, V_RAND = 6, 5
CE_COCO, CE_QUEDA = 4, 5
E_CRACK, E_PONTE, E_COCOS = E0 + 3, E0 + 4, E0 + 6
E_CASCAS = (E0, E0 + 1, E0 + 2)

W, H = 40, 42
INICIO = (19, 38)            # chegada, vindo da casa da Baratelli

# ---------------------------------------------------------------- desenho
ILHAS = [
    (14, 1, 24, 7),      # topo: casa da vidente
    (12, 9, 26, 15),     # labirinto
    (14, 20, 24, 25),    # praca do Rei Macaco
    (17, 27, 21, 32),    # patamar do bau
    (15, 34, 23, 39),    # inicio
    (13, 35, 14, 35),    # pier ate a Ilha das Cascas
    (3, 32, 11, 38),     # Ilha das Cascas
    (1, 23, 12, 23),     # Corredor dos Cocos
    (37, 28, 39, 32),    # ninho
]
NICHOS = [(1, 22), (4, 22), (7, 22), (10, 22)]      # (1,22) e o monte de cocos
PEDRAS_FRAGEIS = [(25, 37), (27, 37), (27, 35), (29, 35), (31, 35), (31, 33), (31, 31), (33, 31), (35, 31)]
# de baixo para cima; inclui as duas beiradas (a borda da ilha bloqueia a saida sem a tabua)
PONTE = [(19, 20), (19, 19), (19, 18), (19, 17), (19, 16), (19, 15)]
LABIRINTO_X0, LABIRINTO_Y0 = 12, 9
LABIRINTO = [
    'RRRRRRRRR.RRRRR',
    '....R...R...R..',
    '.RR.R.R.RRR.R.R',
    '.R....R.....R..',
    '.R.RRRR.RR.RR.R',
    '...R.....R.....',
    'RR.R.RR.R...RRR',
]
CASCAS_X0, CASCAS_Y0, CASCAS_W, CASCAS_H = 3, 32, 9, 7
CASCAS_ENTRADA = (11, 35)
CASCAS_PEDRAS = [(0, 5), (0, 6), (1, 1), (3, 6), (6, 5), (7, 4), (8, 2)]   # (coluna, linha) na ilha
CASCAS_BANANA = (1, 2)
ARVORES = [(15, 39), (23, 39), (14, 25), (24, 21), (17, 32), (39, 29)]
MIRANTE = (24, 25)
BANANAS = {'cascas': (CASCAS_X0 + CASCAS_BANANA[0], CASCAS_Y0 + CASCAS_BANANA[1]),
           'ninho': (38, 30), 'cocos': (4, 22)}
PORTA = (19, 4)
CORREDOR_Y, COCO_XA, COCO_XB = 23, 2, 13
VOLTA_COCO = (15, 23)
CIPO, FIM_CIPO = (38, 32), (22, 38)


def pedra_tile(x, y):
    return 159 if (x + y) % 4 == 0 else 166


def construir():
    m = Map(W, H, 2)
    chao = set(NICHOS) | set(PEDRAS_FRAGEIS)
    for (x0, y0, x1, y1) in ILHAS:
        chao |= rect(x0, y0, x1, y1)
    faces = {(x, y + 1) for (x, y) in chao if (x, y + 1) not in chao and y + 1 < H}
    m.auto(chao, A4 + 36 * 48, 0)
    m.auto(faces, A4 + 44 * 48, 0, wall=True)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    obst = set()

    # casa da vidente
    building(m, 17, 21, 1, 2, 3, 4, 19, 12)
    b(*PORTA, 131); b(18, 3, 73); b(20, 3, 97)
    # labirinto de pedras
    for dy, linha in enumerate(LABIRINTO):
        for dx, ch in enumerate(linha):
            if ch == 'R':
                c = (LABIRINTO_X0 + dx, LABIRINTO_Y0 + dy)
                obst.add(c); b(*c, pedra_tile(*c))
    # Ilha das Cascas: pedras, cascas de banana e chao escorregadio
    rng = random.Random(7)
    escorrega = []
    for cy in range(CASCAS_H):
        for cx in range(CASCAS_W):
            c = (CASCAS_X0 + cx, CASCAS_Y0 + cy)
            if c == CASCAS_ENTRADA:
                continue
            if (cx, cy) in CASCAS_PEDRAS:
                obst.add(c); b(*c, pedra_tile(*c))
            else:
                escorrega.append(c)
                if rng.random() < 0.55:
                    b(*c, rng.choice(E_CASCAS))
    m.region(escorrega, 3)
    # pedras frageis com rachaduras
    m.region(PEDRAS_FRAGEIS, 4)
    for c in PEDRAS_FRAGEIS:
        b(*c, E_CRACK)
    # monte de cocos do Macaco dos Cocos
    b(1, 22, E_COCOS); obst.add((1, 22))
    # arvores de banana (o tronco bloqueia; a copa fica por cima)
    for (x, y) in ARVORES:
        b(x, y - 1, 157, 3); b(x, y, 165); obst.add((x, y))
    # mirante: uma pedra na beira da praca
    b(*MIRANTE, 166); obst.add(MIRANTE)
    # enfeites (passaveis)
    for (x, y, t) in [(15, 6, 161), (23, 5, 160), (14, 2, 162), (24, 3, 163), (16, 36, 160), (22, 34, 161),
                      (19, 29, 250), (15, 24, 162), (23, 23, 160), (38, 28, 161), (12, 23, 250)]:
        b(x, y, t)
    m.obstacles = obst
    m.floor = chao
    return m


def pulos(m):
    """Pulo de uma plataforma para outra (1 tile de vazio). Só pula se o pouso estiver firme."""
    andavel = lambda c: c in m.floor and c not in m.obstacles and m.passable(*c)
    dirs = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}
    n = 0
    for y in range(m.h):
        for x in range(m.w):
            if (x, y) in m.floor:
                continue
            lst = []
            for d, (dx, dy) in dirs.items():
                if andavel((x - dx, y - dy)) and andavel((x + dx, y + dy)):
                    lx, ly = x + dx, y + dy
                    lst += if_([6, -1, d],
                               if_([12, f'MapaVivo.livre({lx}, {ly})'],
                                   se('Jump1') + move(-1, [rc(14, 2 * dx, 2 * dy)], w=True),
                                   balloon(-1, 2)))
            if lst:
                m.add_event('Pulo', x, y, [page(lst, trigger=1, priority=1)])
                n += 1
    return n


# ---------------------------------------------------------------- falas e eventos
def bar(*lines, ind=0):
    return text(list(lines), face='Baratelli', idx=0, name='Baratelli', ind=ind)


def kev(*lines, i=0, ind=0):
    return text(list(lines), face='Kevinho', idx=i, name='Kevinho', ind=ind)


def rei(*lines):
    return text(list(lines), name='Rei Macaco')


def sorteio(falas, quem):
    """Uma fala sorteada (variavel 5) por vez."""
    out = [cmd(122, [V_RAND, V_RAND, 0, 2, 0, len(falas) - 1])]
    for i, f in enumerate(falas):
        out += [cmd(111, [1, V_RAND, 0, i, 0])] + quem(*f, ind=1) + [cmd(0, [], 1), cmd(412, [])]
    return out


MACACO = lambda d=2: img('$Macaco', 0, d)


def eventos_base(m):
    m.add_event('Ambiente', 0, 0, [page(B.tint([0, 0, 10, 0], 0) + [cmd(214, [])], trigger=4, priority=0)])
    m.add_event('Chegada', 0, H - 1, [
        page([], priority=0),
        page(wait(10) + fadein()
             + narr('O Morro do Macaco: plataformas de pedra', 'flutuando acima das nuvens...')
             + kev('Uau... a casa da vidente fica lá no', 'topo!')
             + bar('E como a gente chega lá em cima?!')
             + narr('Para pular de uma plataforma para outra,', 'ande em direção à beira.')
             + narr('Dizem que um tal de Rei Macaco cobra', 'pedágio de quem quer subir...')
             + self_sw(), trigger=3, priority=0, sw1=S_C3_KEV),
        page([], priority=0, self_switch='A'),
    ])
    m.put(16, 36, 2, 137)
    m.add_event('Placa', 16, 36, [page(narr('MORRO DO MACACO', 'A vidente mora no topo.',
                                            'Pedágio: três bananas douradas.'))])
    m.add_event('Macaco', 21, 35, [page(se('Macaco', pitch=115)
                                        + narr('U-u-a-a! O macaco aponta lá para cima, onde',
                                               'um macaco de coroa cruza os braços.')
                                        + kev('Aquele ali deve ser o chefe...'), image=MACACO())])
    m.add_event('Macaco', 15, 34, [page(se('Macaco', pitch=120)
                                        + narr('O macaco aponta para a ilha cheia de cascas', 'e escorrega de propósito. Ele adora.')
                                        + kev('Chão escorregadio... anotado.'), image=MACACO(4))])
    m.add_event('Macaco', 22, 36, [page(se('Macaco', pitch=110)
                                        + narr('O macaco aponta para as pedras rachadas e', 'faz "CABUM!" com as mãos.')
                                        + bar('Entendi: não dá pra ficar parada em cima', 'delas!'), image=MACACO(6))])
    m.add_event('Macaco', 19, 29, [page(se('Macaco', pitch=115)
                                        + narr('O macaco te oferece uma banana...', 'e come na sua frente.')
                                        + bar('Que falta de educação!'), image=MACACO(), move_type=1, speed=3, freq=3)])
    m.add_event('Baú', 21, 28, [
        page(se('Chest1') + self_sw()
             + item(7, 3) + destaque('item', imagem='Item_Pocao', nome='Poção x3',
                                     texto='Cada uma recupera 500 de vida.'), image=img('!Chest', 0, 2, 0)),
        page([], image=img('!Chest', 0, 8, 0), self_switch='A'),
    ])
    m.add_event('Macaco', 16, 6, [page(se('Macaco', pitch=115)
                                       + narr('U-u! O macaco abre caminho.', 'A casa da vidente é logo ali!'), image=MACACO())])
    m.add_event('Macaco perdido', 13, 10, [page(se('Macaco', pitch=100)
                                                + narr('Um macaco sentado num canto do labirinto,', 'com cara de cansado.')
                                                + narr('"Tô procurando a saída desde o carnaval."')
                                                + kev('...Qual carnaval?') + narr('"Não lembro mais."'),
                                                image=MACACO(6))])
    m.add_event('Porta da vidente', PORTA[0], PORTA[1], [
        page(se('Door1') + switch(S_C3_TOPO) + transfer(M_VIDENTE, 8, 11, 8), trigger=1, priority=0)])


def banana_dourada(m, x, y):
    lst = (se('Item1') + item(IT_BANANA_DOURADA, 1) + [cmd(122, [V_BANANAS, V_BANANAS, 1, 0, 1])]
           + destaque('item', imagem='Item_Banana_Dourada', nome='Banana Dourada', texto='O pedágio do Rei Macaco.')
           + bar('Uma banana dourada! Já tenho \\V[6] de 3.')
           + self_sw())
    m.add_event('Banana dourada', x, y, [
        page(lst, image=img('!$Banana_Dourada', 0, 2), trigger=1, priority=0, step=True),
        page([], priority=0, self_switch='A'),
    ])


def eventos_rei(m):
    for (x, y) in BANANAS.values():
        banana_dourada(m, x, y)
    guarda = m.add_event('Macaco guarda', 18, 20, [
        page(se('Macaco', pitch=105) + narr('O macaco guarda cruza os braços:', '"Assunto de pedágio é com o rei."'),
             image=MACACO()),
        page(se('Macaco', pitch=120) + narr('O macaco guarda faz joinha para a ponte.'), image=MACACO(), sw1=S_PONTE),
    ])
    primeira = (se('Macaco', pitch=100) + balloon(0, 1)
                + rei('U-u-a-a! ALTO LÁ!', 'Eu sou o REI MACACO, dono deste morro!')
                + bar('Rei... macaco?')
                + rei('Ninguém sobe sem pagar o pedágio:', 'TRÊS BANANAS DOURADAS!')
                + kev('Bananas... douradas?!')
                + rei('Uma está na Ilha das Cascas, a oeste.', 'Outra no ninho, depois das pedras que caem.')
                + rei('E a última está com o Macaco dos Cocos.', 'Boa sorte. Vai precisar. U-u-a-a!')
                + bar('Por que tudo neste morro envolve banana?!')
                + self_sw('A'))
    ponte = []
    for (x, y) in PONTE:
        ponte += se('Hammer') + shake(2, 9, 6, w=False) + script(f'MapaVivo.mudarTile({x}, {y}, 2, {E_PONTE});') + wait(16)
    pagar = (rei('TRÊS BANANAS DOURADAS!', 'Que brilho... que perfume...')
             + item(IT_BANANA_DOURADA, -3) + se('Item3')
             + rei('MACACADA! PONTE!')
             + se('Macaco', pitch=120) + move(guarda, [rc(14, 0, 0)], w=False) + move(0, [rc(14, 0, 0)], w=True)
             + ponte + switch(S_PONTE) + se('Applause1')
             + rei('Pronto: uma legítima ponte de macaco.', 'Pode subir, moça.')
             + kev('Valeu, majestade!')
             + rei('E cuidado no labirinto lá em cima:', 'tem macaco perdido lá desde o carnaval.'))
    cobrar = rei('Cadê minhas bananas douradas?', 'Você só tem \\V[6] de 3!')
    m.add_event('Rei Macaco', 20, 20, [
        page(if_([2, 'A', 1], primeira, if_([1, V_BANANAS, 0, 3, 1], pagar, cobrar)), image=img('$Rei_Macaco', 0, 2)),
        page(se('Macaco', pitch=100) + sorteio([('Gostou da ponte? Patente minha.',),
                                            ('Volte sempre! Traga bananas.',),
                                            ('U-u-a-a! Um rei nunca esquece um', 'pedágio pago.')],
                                           lambda *l, ind=0: text(list(l), name='Rei Macaco', ind=ind)),
             image=img('$Rei_Macaco', 0, 2), sw1=S_PONTE),
    ])


def eventos_desafios(m):
    # Corredor dos Cocos: o macaco joga um coco que rola ate cair no vao do fim do corredor
    lancador = m.add_event('Macaco dos Cocos', 1, CORREDOR_Y, [
        page(se('Macaco', pitch=125) + narr('O Macaco dos Cocos mostra a língua e', 'pega outro coco.'), image=MACACO(6))])
    m.add_event('Coco', COCO_XA, CORREDOR_Y, [page(
        [cmd(117, [CE_COCO])], image=img('!$Coco', 0, 6), trigger=2, priority=1, move_type=3, speed=5, freq=5,
        mroute=B.route([rc(45, f'this.correrLinha({COCO_XA}, {COCO_XB}, 20, {lancador}, true, 30)')],
                       repeat=True, skippable=True, wait=False))])
    m.add_event('Macaco de capacete', 15, 21, [page(
        se('Macaco', pitch=110) + narr('Um macaco de capacete aponta para o corredor:')
        + narr('"O Macaco dos Cocos não erra um! Esconda-se', 'nos cantinhos e corra quando ele recarregar."')
        + kev('Ele tá de capacete por algum motivo...'), image=MACACO(4))])
    # Ninho: macaco dormindo e o cipo que desce direto para o inicio (so ida)
    m.add_event('Macaco dormindo', 37, 29, [page(
        se('Sleep', vol=60) + balloon(0, 10) + narr('O macaco do ninho ronca. Zzz...'), image=MACACO())])
    descer = (bar('Lá vou eu... UIIIIIIII!') + se('Wind4') + fadeout()
              + script(f'$gamePlayer.locate({FIM_CIPO[0]}, {FIM_CIPO[1]}); $gamePlayer.setDirection(2);')
              + wait(10) + fadein() + kev('Atalho de macaco!'))
    m.add_event('Cipó', CIPO[0], CIPO[1], [page(
        narr('Um cipó comprido desce até lá embaixo,', 'perto de onde vocês chegaram.')
        + choices([('Descer pelo cipó', descer), ('Ficar aqui', [])], cancel=1),
        image=img('!$Cipo', 0, 2), step=True)])


def eventos(m):
    eventos_base(m)
    eventos_rei(m)
    eventos_desafios(m)
    return pulos(m)


def ce_coco():
    falas = [('Ai! Um coco bem na testa!',), ('Esse macaco tem braço de goleiro!',),
             ('Bonk! Tô vendo estrelinhas...',)]
    lst = (se('Blow2') + flash([255, 255, 200, 160], 12) + shake(5, 9, 10, w=False) + pose(-1, 'dor')
           + sorteio(falas, bar) + fadeout()
           + script(f'$gamePlayer.locate({VOLTA_COCO[0]}, {VOLTA_COCO[1]}); $gamePlayer.setDirection(4); '
                    '$gamePlayer.pose("");')
           + wait(6) + fadein())
    return {'id': CE_COCO, 'list': lst + [END], 'name': 'Coco na cabeça', 'switchId': 1, 'trigger': 0}


def ce_queda():
    falas = [('Baratelli! Você tá bem?!',), ('Essas pedras não aguentam nem um', 'pastel de vento!'),
             ('Não dá pra ficar parada em cima delas!',)]
    lst = (se('Fall') + pose(-1, 'queda', segurar=True) + script('MapaVivo.cairDaPedra();') + wait(20) + fadeout()
           + script('MapaVivo.voltarAoChaoFirme(); $gamePlayer.pose("");') + wait(8) + fadein()
           + sorteio(falas, kev))
    return {'id': CE_QUEDA, 'list': lst + [END], 'name': 'Queda das pedras', 'switchId': 1, 'trigger': 0}


def eventos_comuns(ce):
    while len(ce) <= CE_QUEDA:
        ce.append(None)
    ce[CE_COCO] = ce_coco()
    ce[CE_QUEDA] = ce_queda()
    return ce


def sistema(s):
    for chave, i in (('switches', S_PONTE), ('variables', V_BANANAS)):
        while len(s[chave]) <= i:
            s[chave].append('')
    s['switches'][S_PONTE] = 'Cap.3: ponte dos macacos'
    s['variables'][V_BANANAS] = 'Bananas douradas'


# ---------------------------------------------------------------- verificacoes
def _vizinhos_com_pulo(m, pulos_xy, extra=()):
    ok = lambda c: m.passable(*c) or c in extra
    def viz(c):
        x, y = c
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if ok(n):
                yield n
            elif n in pulos_xy:
                l = (x + 2 * dx, y + 2 * dy)
                if ok(l):
                    yield l
    return viz


def alcance(m, inicio, extra=()):
    pulos_xy = {(e['x'], e['y']) for e in m.events[1:] if e and e['name'] == 'Pulo'}
    # personagens parados (macacos, rei, placa, bau...) tambem bloqueiam o caminho
    parados = {(e['x'], e['y']) for e in m.events[1:]
               if e and e['name'] != 'Pulo' and e['pages'][0]['priorityType'] == 1 and e['pages'][0]['moveType'] == 0}
    viz = _vizinhos_com_pulo(m, pulos_xy, extra)
    seen = {inicio}; q = deque([inicio])
    while q:
        for n in viz(q.popleft()):
            if n not in seen and n not in parados:
                seen.add(n); q.append(n)
    return seen


def deslizar_no_mapa(m, pos, d):
    x, y = pos
    passou = []
    while True:
        nx, ny = x + d[0], y + d[1]
        if not m.passable(nx, ny):
            break
        x, y = nx, ny
        passou.append((x, y))
        if m.get(x, y, 5) != 3:
            break
    return (x, y), passou


def resolver_cascas(m):
    """Resolve a Ilha das Cascas com o mapa pronto: menor numero de deslizes ate a banana e de volta."""
    banana = BANANAS['cascas']
    ini = (CASCAS_ENTRADA, False)
    dist = {ini: 0}; q = deque([ini])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        st = q.popleft()
        pos, tem = st
        for d in dirs:
            if pos == CASCAS_ENTRADA and d == (1, 0):
                continue
            n, passou = deslizar_no_mapa(m, pos, d)
            if n == pos:
                continue
            st2 = (n, tem or banana in passou)
            if st2 not in dist:
                dist[st2] = dist[st] + 1; q.append(st2)
    alvo = (CASCAS_ENTRADA, True)
    assert alvo in dist, 'Ilha das Cascas sem solucao'
    for st in dist:   # nenhum beco sem saida
        seen = {st}; q = deque([st]); volta = False
        while q:
            s = q.popleft()
            if s[0] == CASCAS_ENTRADA:
                volta = True; break
            for d in dirs:
                n, passou = deslizar_no_mapa(m, s[0], d)
                s2 = (n, s[1] or banana in passou)
                if n != s[0] and s2 not in seen:
                    seen.add(s2); q.append(s2)
        assert volta, ('beco sem saida na Ilha das Cascas', st)
    return min(v for (p, t), v in dist.items() if t), dist[alvo]


def verificar(m):
    sem_ponte = alcance(m, INICIO)
    for nome, c in BANANAS.items():
        assert c in sem_ponte, ('banana inalcancavel', nome)
    assert (20, 28) in sem_ponte or (21, 29) in sem_ponte, 'bau'
    assert (19, 20) in sem_ponte, 'pe da ponte'
    assert (19, 15) not in sem_ponte, 'labirinto alcancavel sem a ponte!'
    com_ponte = alcance(m, INICIO, extra=set(PONTE))
    assert (PORTA[0], PORTA[1] + 1) in com_ponte, 'porta da vidente inalcancavel com a ponte'
    ate, total = resolver_cascas(m)
    return {'deslizes ate a banana': ate, 'ida e volta': total, 'tiles alcancados': len(com_ponte)}


if __name__ == '__main__':
    mm = construir()
    print('pulos:', pulos(mm))
    print(verificar(mm))
