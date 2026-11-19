# Capitulo 4: acampamento (abertura), Floresta de Mauara (labirinto com armadilhas) e o Coracao da Floresta
# (resto da floresta, praca do templo asteca e a luta contra o Pavao-Hipopotamo).
import os, random, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ch4_comum import *

P = 4                       # cada celula do labirinto ocupa 4x4 tiles (corredor 2x2 + parede de 2)
FLORESTA_TOPO, FLORESTA_LADO = A4 + 33 * 48, A4 + 42 * 48   # copa: topo de cerca-viva (folhas cheias); tronco: Floresta A
PRADO, TERRA, CALCADA = A2 + 0 * 48, A2 + 1 * 48, A2 + 3 * 48
E_PEGADA = {2: E0 + 8, 4: E0 + 9, 6: E0 + 10, 8: E0 + 11}   # dedos para baixo, esquerda, direita, cima
E_ESPINHEIRO, E_LAMA, E_COGUMELOS, E_MARCO = E0 + 7, E0 + 12, E0 + 13, E0 + 14
E_GLIFO, E_SOL, E_SERPENTE_D, E_SERPENTE_E, E_PORTA_ESCURA = E0 + 15, (E0 + 16, E0 + 17, E0 + 24, E0 + 25), E0 + 18, E0 + 19, E0 + 20
DECOR_CHAO = [152, 153, 155, 160, 161, 162, 163, 250, 252, 171]
DIR_DE = {(1, 0): 6, (-1, 0): 4, (0, 1): 2, (0, -1): 8}


def registrar_tiles_floresta():
    ts = load('Tilesets.json')
    t = ts[2]
    for n in range(8, 16):
        t['flags'][E0 + n] = 0x600
    t['flags'][E_ESPINHEIRO] = 0x60f
    t['flags'][E_MARCO] = 0x60f
    t['flags'][E_GLIFO] = 0x60f
    for n in E_SOL + (E_SERPENTE_D, E_SERPENTE_E):
        t['flags'][n] = 0x60f
    t['flags'][E_PORTA_ESCURA] = 0x60f
    save('Tilesets.json', ts)
    B.TILESETS[:] = ts


# ================================================================ labirinto
def labirinto(C, R, seed, extra=0.16, inicio=(0, 0)):
    rng = random.Random(seed)
    links = set()
    vis = {inicio}; pilha = [inicio]
    while pilha:
        c = pilha[-1]
        viz = [(c[0] + dx, c[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= c[0] + dx < C and 0 <= c[1] + dy < R and (c[0] + dx, c[1] + dy) not in vis]
        if viz:
            n = rng.choice(viz); links.add(frozenset((c, n))); vis.add(n); pilha.append(n)
        else:
            pilha.pop()
    todas = ([frozenset(((i, j), (i + 1, j))) for i in range(C - 1) for j in range(R)]
             + [frozenset(((i, j), (i, j + 1))) for i in range(C) for j in range(R - 1)])
    for l in todas:
        if l not in links and rng.random() < extra:
            links.add(l)
    return links


def vizinhos(links, c):
    out = []
    for l in links:
        if c in l:
            out.append(next(iter(l - {c})))
    return out


def caminho(links, a, b, sem=()):
    ant = {a: None}; q = deque([a])
    while q:
        c = q.popleft()
        if c == b:
            break
        for n in vizinhos(links, c):
            if frozenset((c, n)) in sem:
                continue
            if n not in ant:
                ant[n] = c; q.append(n)
    if b not in ant:
        return None
    out = [b]
    while ant[out[-1]] is not None:
        out.append(ant[out[-1]])
    return out[::-1]


class Grade:
    """Converte celulas do labirinto em tiles."""

    def __init__(self, ox, oy):
        self.ox, self.oy = ox, oy

    def tiles(self, c):
        x0, y0 = self.ox + c[0] * P + 1, self.oy + c[1] * P + 1
        return [(x0, y0), (x0 + 1, y0), (x0, y0 + 1), (x0 + 1, y0 + 1)]

    def centro(self, c):
        return (self.ox + c[0] * P + 1, self.oy + c[1] * P + 1)

    def ligacao(self, a, b):
        """Os 2x2 tiles do corredor entre as celulas a e b."""
        (a, b) = sorted((a, b))
        if a[1] == b[1]:
            x = self.ox + a[0] * P + 3; y0 = self.oy + a[1] * P + 1
            return [(x, y0), (x + 1, y0), (x, y0 + 1), (x + 1, y0 + 1)]
        y = self.oy + a[1] * P + 3; x0 = self.ox + a[0] * P + 1
        return [(x0, y), (x0 + 1, y), (x0, y + 1), (x0 + 1, y + 1)]

    def borda(self, a, b):
        """Os 2 tiles da celula a que encostam no corredor para b."""
        x0, y0 = self.centro(a)
        dx, dy = b[0] - a[0], b[1] - a[1]
        if dx == 1:
            return [(x0 + 1, y0), (x0 + 1, y0 + 1)]
        if dx == -1:
            return [(x0, y0), (x0, y0 + 1)]
        if dy == 1:
            return [(x0, y0 + 1), (x0 + 1, y0 + 1)]
        return [(x0, y0), (x0 + 1, y0)]


def pintar_floresta(m, chao, rng, decor=0.12, cogumelos=()):
    paredes = {(x, y) for x in range(m.w) for y in range(m.h)} - chao
    tronco = {(x, y) for (x, y) in paredes if (x, y + 1) in chao}
    copa = paredes - tronco
    m.auto(copa, FLORESTA_TOPO, 0)
    m.auto(tronco, FLORESTA_LADO, 0, wall=True)
    m.auto(chao, PRADO, 0)
    m.region(paredes)
    for (x, y) in sorted(chao):
        if rng.random() < decor:
            m.put(x, y, 2, rng.choice(DECOR_CHAO))
    return paredes


# ================================================================ 15. ACAMPAMENTO
def construir_campo():
    m = Map(20, 15, 2)
    chao = rect(2, 2, 18, 12) | rect(18, 6, 19, 8)
    rng = random.Random(41)
    pintar_floresta(m, chao, rng, decor=0.1)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for dx, (t0, t1, t2) in enumerate(((5, 13, 21), (6, 14, 22), (7, 15, 23))):
        b(3 + dx, 3, t0, 3); b(3 + dx, 4, t1); b(3 + dx, 5, t2)
    b(9, 7, 147)
    b(7, 10, 164); b(12, 6, 164)
    for (x, y) in [(15, 3), (16, 3)]:
        b(x, y, 176 + (x - 15), 3); b(x, y + 1, 184 + (x - 15))
    for (x, y, t) in [(11, 11, 160), (13, 10, 161), (6, 7, 162), (16, 9, 250), (4, 9, 163), (14, 4, 152)]:
        b(x, y, t)
    m.auto(rect(17, 6, 19, 8) | rect(14, 7, 16, 7), TERRA, 0)
    return m


def eventos_campo(m):
    m.add_event('Ambiente', 0, 0, [page(tint([-30, -20, 20, 30], 0) + [cmd(214, [])], trigger=4, priority=0)])
    flame(m, 9, 7, 0, 2)
    KE = m.add_event('Kevinho', 11, 8, [
        page([], image=img('$Kevinho', 0, 4)),
        page([], image=img('$Kevinho_Uma', 0, 4), self_switch='A'),
        page([], priority=0, through=True, sw1=S_C4_INICIO),
    ])
    abertura = (
        fadeout() + stop_bgm(1) + stop_bgs(1)
        + script("$gamePlayer.setTransparent(false); $gamePlayer.setThrough(false); $gamePlayer.setOpacity(255);\n"
                 "$gamePlayer.setMoveSpeed(4); $gamePlayer.pose('');")
        + party_remove(2) + party_remove(3) + party_add(BARATELLI) + party_add(KEVINHO)
        + visual(BARATELLI, '$Baratelli_Cigana', 'Baratelli')
        + visual(KEVINHO, '$Kevinho', 'Kevinho')
        + tem_item(IT_CRANIO, [], item(IT_CRANIO, 1))
        + followers(False)
        + script('$gamePlayer.locate(8, 8); $gamePlayer.setDirection(6);')
        + capitulo('Capitulo4')
        + narr('Depois da batalha na casa da vidente, Baratelli', 'e Kevinho descem o Morro do Macaco.')
        + narr('Eles acampam na encosta, debaixo das', 'últimas estrelas da noite.')
        + bgs('Night', 35) + bgs('Fire1', 25)
        + fadein()
        + wait(30)
        + bar('Leandra... eu prometi que ia te vingar.', 'E eu vou.')
        + kev('Você não pregou o olho a noite toda,', 'Baratelli.')
        + bar('Como eu vou dormir, Kevinho? A Peruca', 'Dourada está em algum lugar por aí...')
        # o rastro
        + se('Saint3') + anim(-1, 120, w=False) + flash([255, 230, 140, 160], 30)
        + balloon(-1, 1)
        + narr('De repente, um cheiro doce e dourado passa', 'pelo nariz de Baratelli...')
        + bar('Esse cheiro... é ela! A Peruca Dourada!', 'Eu consigo sentir o RASTRO dela!')
        + kev('Você está... farejando uma peruca?')
        + bar('Não é uma peruca qualquer, Kevinho!', 'É a lendária Peruca Dourada!')
        # carta da vidente
        + se('Magic3') + anim(-1, 117, w=True)
        + narr('O crânio de Leandra brilha nas mãos', 'de Baratelli...')
        + destaque('item', imagem='Carta_Vidente_Calva', titulo='CARTA DE TARÔ', nome='A Vidente Calva',
                   texto='A clarividência da Leandra agora é sua.', tamanho=330)
        + aprender(BARATELLI, SK_VIDENTE)
        + bar('Leandra... você continua comigo.')
        # carta do sapo
        + se('Frog', pitch=80) + wait(20) + se('Frog', pitch=60)
        + narr('Ao longe, um coaxar grave ecoa pela mata...')
        + se('Magic3') + anim(-1, 51, w=True)
        + destaque('item', imagem='Carta_Sapo_Sacudo', titulo='CARTA DE TARÔ', nome='O Sapo Sacudo',
                   texto='A força bruta do Gusrola, finalmente do lado certo.', tamanho=330)
        + aprender(BARATELLI, SK_SAPO)
        + kev('Esse sapo tá mais forte morto do que', 'vivo...')
        + bar('Agora eu tenho duas cartas novas pra usar', 'nas lutas!')
        # bencao do Kevinho
        + bar('Kevinho, chegue mais perto.', 'Você também merece ficar mais forte.')
        + kev('Hã? O que você vai fazer?', i=1)
        + pose(-1, 'magia', olhar=KE, repetir=True, segurar=True)
        + se('Saint5') + anim(KE, 117, w=False) + wait(30)
        + flash([255, 255, 255, 255], 40) + shake(5, 8, 20)
        + narr('Baratelli abençoa Kevinho com seus poderes', 'de cigana!')
        + script(set_self_js(M_CAMPO, [KE], True))
        + visual(KEVINHO, '$Kevinho_Uma', 'Kevinho_Uma')
        + classe(KEVINHO, CLS_UMA)
        + switch(S_C4_UMA)
        + se('Horse') + pose(-1, '')
        + destaque('evento', personagem='$Kevinho_Uma', titulo='NOVO VISUAL', nome='Kevinho, a Umamusume',
                   texto='Orelhas de cavalo, cauda e uma velocidade absurda!')
        + kuma('Orelhas?! Uma cauda?! E esse cabelão?!', i=3)
        + kuma('Eu virei... uma Umamusume?!', i=3)
        + bar('E das mais lindas, hein!')
        + kuma('Eu me sinto capaz de correr até o outro', 'continente!', i=2)
        + narr('Kevinho aprendeu: Coice de Cavala, Galope', 'Relâmpago e Relincho Motivador!')
        # para onde ir
        + bar('O rastro vai para o leste... muito, muito', 'para o leste.')
        + pic(5, 'Mapa_Mauara', 408, 290, opacity=0, scale=90) + move_pic_e(5, 408, 280, 255, 30, scale=100, w=True)
        + narr('Tudo indica que o caminho certo é a grande', 'Floresta de Mauara, no extremo leste...', bg=1)
        + narr('...a única região que liga os dois', 'continentes.', bg=1)
        + move_pic(5, 408, 280, 0, 30, w=True) + erase_pic(5)
        + kuma('A Floresta de Mauara? Dizem que quem', 'entra lá se perde...', i=1)
        + kuma('...e quem se perde nunca mais acha o', 'caminho!', i=1)
        + bar('Então a gente não se perde. Vamos!')
        + script(f"const f = $gamePlayer.followers().follower(0); const k = $gameMap.event({KE});\n"
                 f"f.locate(k.x, k.y); f.setDirection(4);")
        + followers(True)
        + switch(S_C4_INICIO)
        + bgm('Field2', vol=60)
        + narr('Siga para o leste, até a Floresta de Mauara.'))
    m.add_event('Abertura', 0, 14, [page(abertura, trigger=3, priority=0), page([], priority=0, sw1=S_C4_INICIO)])
    m.add_event('Fogueira', 9, 6, [page(narr('A fogueira estala baixinho.')
                                         + kuma('Eu assei uma cenoura. Quer?') + bar('...Cenoura assada? Às cinco da manhã?')
                                         + kuma('É café da manhã de campeã!', i=2))])
    m.add_event('Barraca', 4, 5, [page(narr('A barraca está toda torta.')
                                        + bar('Montada pelo Kevinho. Dá pra perceber.'))])
    for y in (6, 7, 8):
        m.add_event('Saída', 19, y, [page([], priority=0),
                                    page(transfer(M_MAUARA, MAUARA_INICIO[0], MAUARA_INICIO[1], 6, fade=0),
                                         trigger=1, priority=0, sw1=S_C4_INICIO)])


# ================================================================ armadilhas e enfeites comuns aos dois mapas
FALAS_ARMADILHA = [
    bar('Foi o cipó! O cipó me jogou de volta!'),
    bar('Essa floresta tá de brincadeira comigo!'),
    narr('Uma risadinha ecoa entre as árvores:', '"Hihihi! Pé virado, caminho errado!"'),
    kuma('Hihi... quer dizer, que absurdo, Baratelli.', i=2),
    bar('Eu sou cigana, não sou bola de pingue-pongue!'),
]


def armadilha_cipo(m, tiles, destino, mapa):
    """Cipo-laco: pega a Baratelli e joga de volta para 'destino'."""
    for (x, y) in tiles:
        lst = (script(f'$gameVariables.setValue({V_DX}, {destino[0]}); $gameVariables.setValue({V_DY}, {destino[1]});')
               + self_sw('A')
               + se('Twine') + se('Wind4', pitch=130)
               + balloon(-1, 1)
               + pose(-1, 'queda', segurar=True)
               + shake(4, 8, 10)
               + call(CE_CIPO)
               + self_sw('A', False))
        m.add_event('Cipó-laço', x, y, [
            page(lst, image=img('!Templo2', 3, 2), trigger=1, priority=0),
            page([], image=img('!Templo2', 3, 6), priority=0, step=True, dir_fix=True, walk=False, self_switch='A'),
        ])


def areia_movedica(m, x, y, destino):
    lst = (script(f'$gameVariables.setValue({V_DX}, {destino[0]}); $gameVariables.setValue({V_DY}, {destino[1]});')
           + call(CE_AREIA))
    m.add_event('Areia movediça', x, y, [page(lst, image=img('!Templo2', 4, 2), trigger=1, priority=0, step=True,
                                              dir_fix=True, walk=False)])


def espinhos(m, grade, a, b, sw):
    """Espinhos que crescem e fecham o corredor entre as celulas a e b (para sempre)."""
    lig = grade.ligacao(a, b)
    alvo = [t for t in lig if t in m._chao]
    for (x, y) in alvo:
        m.add_event('Espinhos', x, y, [
            page([], priority=0, through=True),
            page([], image=img('!Templo2', 2, 6), priority=1, step=True, dir_fix=True, walk=False, sw1=sw),
        ])
    fechar = (se('Earth2') + se('Wind7', pitch=70) + switch(sw) + shake(5, 8, 16)
              + balloon(-1, 1)
              + sorteio([bar('Espinhos?! Os espinhos fecharam o caminho!'),
                         kuma('O mato fechou o caminho bem na nossa', 'cara! Vamos ter que dar a volta.', i=3),
                         bar('Ah, não! Essa floresta muda sozinha!')]))
    for lado in ((a, b), (b, a)):
        for (x, y) in grade.borda(*lado):
            if (x, y) in m._chao and not any(e and e['x'] == x and e['y'] == y for e in m.events):
                m.add_event('Gatilho espinhos', x, y, [page(if_([0, sw, 1], fechar), trigger=1, priority=0)])
    return alvo


def rastro(m, x, y):
    falas = sorteio([bar('O rastro... a peruca passou por aqui!'),
                     bar('Sinto o cheiro dourado! É por aqui!'),
                     bar('Meus poderes de cigana dizem: por aqui!')])
    m.add_event('Rastro dourado', x, y, [
        page(se('Saint3', vol=70) + falas + self_sw(), image=img('!Templo2', 6, 2), trigger=1, priority=0, step=True,
             dir_fix=True, walk=False),
        page([], image=img('!Templo2', 6, 4), priority=0, step=True, dir_fix=True, walk=False, self_switch='A'),
    ])


def fala_gatilho(m, x, y):
    m.add_event('Conversa', x, y, [page(call(CE_FALAS) + self_sw(), trigger=1, priority=0),
                                   page([], priority=0, self_switch='A')])


def inimigo(m, x, y, tipo, troop, falas_vitoria):
    imagem = img('$Arara', 0, 2) if tipo == 'arara' else img('$Capivara_Maromba', 0, 2)
    venceu = se('Item1', vol=60) + falas_vitoria + self_sw()
    fugiu = narr('Vocês fogem... e o bicho some no mato.') + self_sw()
    perdeu = ([cmd(314, [0, 0])] + narr('Baratelli acorda com uma folha grudada', 'na testa...')
              + kuma('Levanta! Esse bicho é mais fraco que', 'parece!', i=1))
    som = se('Crow', pitch=150) if tipo == 'arara' else se('Cow', pitch=140)
    m.add_event('Arara Barraqueira' if tipo == 'arara' else 'Capivara Marombeira', x, y, [
        page(som + balloon(0, 1) + batalha(troop, venceu, fugiu, perdeu), image=imagem, trigger=2, move_type=1,
             speed=3 if tipo == 'capivara' else 4, freq=3, step=tipo == 'arara'),
        page([], priority=0, self_switch='A'),
    ])


# ================================================================ 16. FLORESTA DE MAUARA (labirinto)
C1, R1 = 12, 9
CL1 = [(0, 6), (4, 4), (8, 2)]       # clareiras 2x2 (celula de cima a esquerda)
INI1, FIM1 = (0, 7), (10, 0)


def clareira_links(cl):
    i, j = cl
    cel = [(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)]
    return cel, {frozenset(((i, j), (i + 1, j))), frozenset(((i, j + 1), (i + 1, j + 1))),
                 frozenset(((i, j), (i, j + 1))), frozenset(((i + 1, j), (i + 1, j + 1)))}


def montar_labirinto(C, R, ox, oy, seed, clareiras, ini, fim):
    links = labirinto(C, R, seed, inicio=ini)
    for cl in clareiras:
        links |= clareira_links(cl)[1]
    grade = Grade(ox, oy)
    chao = set()
    for i in range(C):
        for j in range(R):
            chao |= set(grade.tiles((i, j)))
    for l in links:
        a, b = tuple(l)
        chao |= set(grade.ligacao(a, b))
    for (i, j) in clareiras:
        chao |= rect(ox + i * P + 1, oy + j * P + 1, ox + (i + 1) * P + 2, oy + (j + 1) * P + 2)
    trilha = caminho(links, ini, fim)
    return links, grade, chao, trilha


def galhos_mortos(links, trilha):
    """Galhos que saem da trilha e terminam sem saida: (celula da trilha, primeira celula, celulas do galho)."""
    na_trilha = set(trilha)
    out = []
    for p in trilha:
        for n in vizinhos(links, p):
            if n in na_trilha:
                continue
            vis = {n}; q = deque([n]); volta = False
            while q:
                c = q.popleft()
                for v in vizinhos(links, c):
                    if v == p:
                        continue
                    if v in na_trilha:
                        volta = True
                    elif v not in vis:
                        vis.add(v); q.append(v)
            if not volta:
                out.append((p, n, vis))
    return out


def escolher_espinhos(links, trilha, ini, fim, n, rng, proibidos=()):
    """Corredores que podem fechar sem ilhar ninguem (todas as celulas continuam chegando ao fim)."""
    todas_cel = {c for l in links for c in l}
    cand = [l for l in links if not (set(l) & set(proibidos))]
    rng.shuffle(cand)
    escolhidos = []
    for l in cand:
        teste = set(escolhidos) | {l}
        ok = all(caminho(links, c, fim, sem=teste) for c in todas_cel)
        a, b = tuple(l)
        perto = a in trilha or b in trilha
        if ok and perto and not (a in trilha and b in trilha):
            escolhidos.append(l)
            if len(escolhidos) == n:
                break
    return escolhidos


def construir_mauara():
    W, H = 1 + C1 * P + 1, 1 + R1 * P + 1
    m = Map(W, H, 2)
    links, grade, chao, trilha = montar_labirinto(C1, R1, 0, 0, 2024, CL1, INI1, FIM1)
    x0, y0 = grade.centro(INI1)
    chao |= {(0, y0), (1, y0), (0, y0 + 1), (1, y0 + 1)}             # entrada a oeste
    xf, yf = grade.centro(FIM1)
    chao |= {(xf, 0), (xf + 1, 0), (xf, 1), (xf + 1, 1)}             # saida ao norte
    rng = random.Random(16)
    m._chao = chao
    pintar_floresta(m, chao, rng)
    info = dict(links=links, grade=grade, trilha=trilha, chao=chao, entrada=(1, y0), saida=(xf, 0))
    # pegadas do Curupira na trilha certa (apontando para tras!)
    for k in range(1, len(trilha) - 1, 2):
        c, ant = trilha[k], trilha[k - 1]
        d = DIR_DE[(ant[0] - c[0], ant[1] - c[1])]
        x, y = grade.centro(c)
        m.put(x + rng.randint(0, 1), y + rng.randint(0, 1), 2, E_PEGADA[d])
    return m, info


def eventos_mauara(m, info):
    links, grade, trilha, chao = info['links'], info['grade'], info['trilha'], info['chao']
    rng = random.Random(161)
    m.add_event('Ambiente', 0, 0, [page(tint([-34, -10, -30, 30], 0) + [cmd(214, [])], trigger=4, priority=0)])
    ocupado = set()
    # placa e chegada
    sx, sy = grade.centro(INI1)
    placa_tile(m, sx + 1, sy - 2, 137, 'FLORESTA DE MAUARA', 'Cuidado: aqui mora o Curupira.',
               'As pegadas dele apontam para trás!')
    ocupado.add((sx + 1, sy - 2))
    m.add_event('Chegada', 0, m.h - 1, [
        page([], priority=0),
        page(wait(10)
             + narr('A Floresta de Mauara: árvores tão altas que', 'escondem o céu.')
             + kuma('Credo, que escuro. E esse barulho de', 'tambor?', i=3)
             + bar('Concentra, Kevinho! O rastro da peruca', 'segue floresta adentro.')
             + bar('E olha: pegadas no chão!')
             + kuma('Pegadas com o pé virado pra trás...', 'Será que é o Curupira?', i=1)
             + switch(S_C4_FLORESTA) + self_sw(), trigger=3, priority=0, sw1=S_C4_INICIO),
        page([], priority=0, self_switch='A'),
    ])
    # galhos sem saida: cipos (quem entra volta 3 celulas na trilha) e baus
    galhos = galhos_mortos(links, trilha)
    rng.shuffle(galhos)
    baus = [(IT_CENOURA, 2, 'Item_Cenoura', 'Cenoura Dourada x2', 'Cada uma recupera 300 de vida.'),
            (IT_GUARANA, 2, 'Item_Guarana', 'Guaraná da Floresta x2', 'Cada um recupera 50 de PM.'),
            (7, 2, 'Item_Pocao', 'Poção x2', 'Cada uma recupera 500 de vida.')]
    n_cipo = 0
    cipos = []
    for (p, n, celulas) in galhos:
        ponta = max(celulas, key=lambda c: len(caminho(links, p, c) or []))
        if baus and len(celulas) >= 2:
            iid, qt, imagem, nome, texto = baus.pop()
            x, y = grade.centro(ponta)
            bau(m, x, y, iid, qt, imagem, nome, texto)
            ocupado.add((x, y))
        elif n_cipo < 5:
            i = trilha.index(p)
            volta = trilha[max(0, i - 3)]
            dx, dy = grade.centro(volta)
            tiles = [t for t in grade.ligacao(p, n) if t in chao]
            armadilha_cipo(m, tiles, (dx, dy), M_MAUARA)
            ocupado |= set(tiles)
            cipos.append((p, n))
            n_cipo += 1
    # espinhos que fecham caminhos alternativos
    proib = [INI1, FIM1] + [c for cl in CL1 for c in clareira_links(cl)[0]]
    esp = escolher_espinhos(links, trilha, INI1, FIM1, 3, rng, proibidos=proib)
    for k, l in enumerate(esp):
        a, b = tuple(l)
        ocupado |= set(espinhos(m, grade, a, b, S_ESPINHOS[k]))
    info['espinhos'] = esp
    # rastro dourado em tres bifurcacoes da trilha
    bif = [k for k in range(1, len(trilha) - 1) if len(vizinhos(links, trilha[k])) >= 3]
    for k in bif[::max(1, len(bif) // 3)][:3]:
        lig = [t for t in grade.ligacao(trilha[k], trilha[k + 1]) if t in chao and t not in ocupado]
        if lig:
            rastro(m, *lig[0]); ocupado.add(lig[0])
    # conversas aleatorias ao longo da trilha
    for k in range(3, len(trilha) - 1, 5):
        x, y = grade.centro(trilha[k])
        if (x + 1, y + 1) not in ocupado:
            fala_gatilho(m, x + 1, y + 1); ocupado.add((x + 1, y + 1))
    # clareira do meio: areia movedica, Curupira e cogumelos
    i, j = CL1[1]
    cx, cy = grade.ox + i * P + 1, grade.oy + j * P + 1
    k_meio = min(range(len(trilha)), key=lambda k: abs(trilha[k][0] - i) + abs(trilha[k][1] - j))
    volta = grade.centro(trilha[max(0, k_meio - 2)])
    for (x, y) in [(cx + 2, cy + 1), (cx + 3, cy + 4), (cx + 1, cy + 4)]:
        if (x, y) in chao and (x, y) not in ocupado:
            areia_movedica(m, x, y, volta); ocupado.add((x, y))
    m.put(cx + 4, cy + 2, 2, E_COGUMELOS)
    cur = m.add_event('Curupira', cx + 4, cy + 1, [page(
        se('Laugh', pitch=150) + balloon(0, 4)
        + curupira('Hihihi! Visitas na minha floresta!')
        + sorteio([curupira('Quem segue meus pés anda pra trás!', 'Hihihi!'),
                   curupira('O caminho certo é sempre o que as', 'pegadas NÃO mostram!'),
                   curupira('Cipó no chão, volta pro portão!', 'Hihihi!')])
        + kuma('Ele fala por enigmas...', i=1) + bar('E ri por enigmas também.'),
        image=img('$Curupira', 0, 2), move_type=1, speed=4, freq=4, step=True)])
    ocupado.add((cx + 4, cy + 1))
    # clareira perto da saida: um marco de pedra com dica
    i, j = CL1[2]
    mx, my = grade.ox + i * P + 2, grade.oy + j * P + 2
    m.put(mx, my, 2, E_MARCO)
    m.add_event('Marco de pedra', mx, my, [page(narr('Um marco de pedra coberto de musgo, com', 'desenhos de serpentes emplumadas.')
                                                + narr('"Ao norte, o Coração de Mauara.', 'Lá dorme o templo... e o seu guardião."'))])
    ocupado.add((mx, my))
    # inimigos
    vagas = [c for c in [(3, 3), (6, 6), (9, 5), (5, 1), (2, 1), (10, 7)] if c not in trilha[:2]]
    tipos = [('arara', TR_ARARAS, bar('Vencemos a fofoqueira! Xô, xô!')),
             ('capivara', TR_CAPIVARA, kuma('Capivara marombeira derrotada! O supino', 'dela era fake!', i=2)),
             ('arara', TR_MISTO, bar('Arara e capivara... que dupla!')),
             ('capivara', TR_CAPIVARA, bar('Volta pra academia, capivara!'))]
    for (c, (tipo, tr, fala)) in zip(vagas, tipos):
        x, y = grade.centro(c)
        if (x, y) not in ocupado:
            inimigo(m, x, y, tipo, tr, fala); ocupado.add((x, y))
    # portal (aparece depois de ativar o portal do 3o andar)
    px, py = PORTAIS[0][1], PORTAIS[0][2]
    m.add_event('Portal da floresta', px, py, [
        page([], priority=0),
        page(var_set(V_PORTAL_AQUI, 0) + call(CE_PORTAL), image=img('!Templo2', 5, 4), priority=0, step=True,
             dir_fix=True, walk=False, sw1=S_PORTAL[2]),
    ])
    ocupado.add((px, py))
    # saidas
    ex, ey = info['entrada']
    for y in (ey, ey + 1):
        m.add_event('Para o acampamento', 0, y, [page(transfer(M_CAMPO, CAMPO_SAIDA[0], CAMPO_SAIDA[1], 4, fade=0),
                                                       trigger=1, priority=0)])
    sx2, sy2 = info['saida']
    for x in (sx2, sx2 + 1):
        m.add_event('Para o coração da floresta', x, 0, [page(transfer(M_CORACAO, CORACAO_INICIO[0], CORACAO_INICIO[1], 8, fade=0),
                                                               trigger=1, priority=0)])
    info['ocupado'] = ocupado
    return info


# ================================================================ 17. CORACAO DE MAUARA + TEMPLO
C2, R2 = 9, 4
OY2 = 20
INI2, FIM2 = (4, 3), (4, 0)
CL2 = [(1, 1)]


def construir_coracao():
    W, H = 40, OY2 + R2 * P + 2
    m = Map(W, H, 2)
    links, grade, chao, trilha = montar_labirinto(C2, R2, 1, OY2, 77, CL2, INI2, FIM2)
    x0, y0 = grade.centro(INI2)
    chao |= rect(x0, y0 + 2, x0 + 1, H - 1)                 # entrada ao sul
    xf, yf = grade.centro(FIM2)
    chao |= rect(xf, OY2, xf + 1, yf)                       # saida para a praca
    praca = rect(3, 1, 36, OY2 - 1)
    chao |= praca
    m._chao = chao
    rng = random.Random(170)
    pintar_floresta(m, chao, rng, decor=0.0)
    for (x, y) in sorted(chao):
        if y >= OY2 and rng.random() < 0.12:
            m.put(x, y, 2, rng.choice(DECOR_CHAO))
    # praca de pedra e piramide
    m.auto((rect(5, 13, 34, OY2 - 1) | rect(17, OY2, 20, OY2)) & chao, CALCADA, 0)
    pedra_topo, pedra_lado = A4 + 2 * 48, A4 + 10 * 48
    degraus = [(7, 31, 13, 14, 15, 16), (10, 28, 9, 10, 11, 12), (13, 25, 5, 6, 7, 8), (15, 23, 1, 2, 3, 4)]
    topo_cel, lado_cel = set(), set()
    for (xa, xb, t0, t1, f0, f1) in degraus:
        topo_cel |= rect(xa, t0, xb, t1)
        lado_cel |= rect(xa, f0, xb, f1)
    escada = rect(18, 5, 20, 16)
    topo_cel -= escada; lado_cel -= escada
    topo_cel -= lado_cel
    m.auto(topo_cel, pedra_topo, 0)
    m.auto(lado_cel, pedra_lado, 0, wall=True)
    m.region(topo_cel | lado_cel)
    for y in range(5, 17):
        m.put(18, y, 0, A5 + 68); m.put(19, y, 0, A5 + 69); m.put(20, y, 0, A5 + 70)
    m.put(*CORACAO_PORTA, 0, A5 + 69)
    m.put(19, 4, 2, E_PORTA_ESCURA)
    for k, (x, y) in enumerate([(19, 1), (20, 1), (19, 2), (20, 2)]):
        m.put(x, y, 2, E_SOL[k])
    m.put(17, 16, 2, E_SERPENTE_D); m.put(21, 16, 2, E_SERPENTE_E)
    for x in (9, 13, 25, 29):
        m.put(x, 15, 2, E_GLIFO)
    for (x, y) in [(4, 2), (35, 2), (4, 10), (35, 10)]:
        m.put(x, y - 1, 3, 176); m.put(x + 1, y - 1, 3, 177); m.put(x, y, 2, 184); m.put(x + 1, y, 2, 185)
    for (x, y, t) in [(6, 5, 160), (32, 6, 161), (8, 3, 250), (30, 3, 163), (5, 12, 152), (33, 12, 153), (11, 18, 252), (27, 18, 252)]:
        m.put(x, y, 2, t)
    info = dict(links=links, grade=grade, trilha=trilha, chao=chao)
    return m, info


def luta_pavao(PV, PORTA, BARR):
    tutorial = (narr('MINIGAME DE LUTA!', '← → andar   ↑ pular   ↓ defender/abaixar')
                + narr('Z soco   X chute', 'Q e W usam as cartas quando o Glamour enche.'))
    vitoria = (fadein()
               + pose(PV, 'dor')
               + pavao('Tá bom, tá bom... pode passar, rainha.', 'Só não pisa no meu leque.')
               + kuma('VOCÊ CONSEGUIU, BARATELLI!', i=2)
               + bar('Ninguém segura uma cigana com glamour!')
               + se('Item3') + item(IT_PENA, 1)
               + destaque('item', imagem='Item_Pena', nome='Pena de Pavão', texto='Vale mais que o seu aluguel.')
               + se('Earth1') + shake(4, 6, 30, w=False)
               + move(PORTA, [rc(35), rc(16), rc(15, 8), rc(17), rc(15, 8), rc(18), rc(15, 8), rc(19)], w=True)
               + se('Open5')
               + narr('A grande porta de pedra do templo se abre!')
               + move(PV, [rc(37), rc(29, 3), RIGHT, RIGHT, RIGHT, DOWN, rc(16), rc(38)], w=True)
               + switch(S_PAVAO)
               + bgm('Templo_Xavasca', vol=70))
    derrota = (fadein()
               + pavao('HAHAHA! Volte quando tiver mais', 'glamour, querida!')
               + kuma('Respira, Baratelli. A gente tenta de novo!', i=1)
               + bgm('Templo_Xavasca', vol=70))
    return (balloon(PV, 1)
            + pavao('Alto lá, plebeias!')
            + pavao('Ninguém entra no Templo da Xavasca Leprosa', 'sem passar pela minha BELEZA!')
            + bar('Que bicho é esse, gente?!', 'Um pavão... hipopótamo?!')
            + kuma('Ele tem a elegância de um pavão...', '...e o peso de um hipopótamo.', i=3)
            + pavao('Duas toneladas de puro glamour, querida.', 'Quer entrar? Vai ter que me vencer!')
            + bar('Então segura esse leque, que lá vou eu!')
            + kuma('Eu fico na torcida! VAI, BARATELLI!', i=2)
            + tutorial
            + var_set(V_LUTA, 0)
            + plugin('LutaArena', 'lutar', {'variavel': V_LUTA, 'heroi': 'SV_Baratelli_Cigana'})
            + var_eq(V_LUTA, 1, vitoria, derrota))


def eventos_coracao(m, info):
    links, grade, trilha, chao = info['links'], info['grade'], info['trilha'], info['chao']
    rng = random.Random(171)
    m.add_event('Ambiente', 0, 0, [page(tint([-24, -6, -20, 20], 0) + [cmd(214, [])], trigger=4, priority=0)])
    ocupado = set()
    m.add_event('Chegada', 0, m.h - 1, [
        page(wait(10) + narr('O Coração de Mauara.', 'Aqui a floresta fica ainda mais fechada...')
             + kuma('Sinto cheiro de flor... e de bicho grande.', i=1)
             + switch(S_CORACAO), trigger=3, priority=0),
        page([], priority=0, sw1=S_CORACAO),
    ])
    galhos = galhos_mortos(links, trilha)
    rng.shuffle(galhos)
    feito_bau = False
    n_cipo = 0
    for (p, n, celulas) in galhos:
        if not feito_bau:
            ponta = max(celulas, key=lambda c: len(caminho(links, p, c) or []))
            x, y = grade.centro(ponta)
            bau(m, x, y, IT_CENOURA, 3, 'Item_Cenoura', 'Cenoura Dourada x3', 'Cada uma recupera 300 de vida.')
            ocupado.add((x, y)); feito_bau = True
        elif n_cipo < 2:
            i = trilha.index(p)
            dx, dy = grade.centro(trilha[max(0, i - 2)])
            tiles = [t for t in grade.ligacao(p, n) if t in chao]
            armadilha_cipo(m, tiles, (dx, dy), M_CORACAO)
            ocupado |= set(tiles)
            n_cipo += 1
    proib = [INI2, FIM2] + [c for cl in CL2 for c in clareira_links(cl)[0]]
    esp = escolher_espinhos(links, trilha, INI2, FIM2, 1, rng, proibidos=proib)
    for k, l in enumerate(esp):
        a, b = tuple(l)
        ocupado |= set(espinhos(m, grade, a, b, S_ESPINHOS2[k]))
    info['espinhos'] = esp
    i, j = CL2[0]
    cx, cy = grade.ox + i * P + 1, grade.oy + j * P + 1
    k_meio = min(range(len(trilha)), key=lambda k: abs(trilha[k][0] - i) + abs(trilha[k][1] - j))
    volta = grade.centro(trilha[max(0, k_meio - 1)])
    for (x, y) in [(cx + 2, cy + 2), (cx + 4, cy + 3)]:
        if (x, y) in chao:
            areia_movedica(m, x, y, volta); ocupado.add((x, y))
    for k, c in enumerate([(7, 2), (2, 0)]):
        x, y = grade.centro(c)
        if (x, y) not in ocupado:
            if k == 0:
                inimigo(m, x, y, 'capivara', TR_CAPIVARA, kuma('Essa capivara nunca pulou o dia de perna.', i=2))
            else:
                inimigo(m, x, y, 'arara', TR_MISTO, bar('Fofoca encerrada!'))
            ocupado.add((x, y))
    for k in range(2, len(trilha) - 1, 3):
        x, y = grade.centro(trilha[k])
        if (x, y) not in ocupado:
            fala_gatilho(m, x, y); ocupado.add((x, y))
    # musica: floresta embaixo, templo na praca
    xf, yf = grade.centro(FIM2)
    for x in (xf, xf + 1):
        m.add_event('Música do templo', x, OY2 - 1, [page(bgm('Templo_Xavasca', vol=70), trigger=1, priority=0)])
        m.add_event('Música da floresta', x, OY2 + 1, [page(bgm('Floresta_Mauara', vol=70), trigger=1, priority=0)])
    # templo
    for (x, y) in [(12, 13), (26, 13), (14, 9), (24, 9), (16, 5), (22, 5)]:
        flame(m, x, y, 0, 2)
    PORTA = m.add_event('Porta do templo', CORACAO_PORTA[0], CORACAO_PORTA[1], [
        page(narr('Uma porta de pedra enorme, coberta de', 'glifos de penas e perucas.'), image=img('!Templo2', 0, 2),
             trigger=1, dir_fix=False, walk=False),
        page(se('Door1') + transfer(M_T1, T1_CHEGADA[0], T1_CHEGADA[1], 8), image=img('!Templo2', 0, 8),
             trigger=1, priority=1, dir_fix=True, walk=False, sw1=S_PAVAO),
    ])
    BARR = []
    for x in (18, 20):
        BARR.append(m.add_event('Barreira', x, 17, [
            page(pavao('Ei! Furar fila não, querida!'), trigger=0),
            page([], priority=0, through=True, sw1=S_PAVAO)]))
    PV = len(m.events)
    m.add_event('Pavão-Hipopótamo', 19, 17, [
        page(luta_pavao(PV, PORTA, BARR), image=img('$Pavao_Hipopotamo', 0, 2), step=True),
        page(pavao('Pode passar, rainha.', 'Mas não pisa no meu leque!'), image=img('$Pavao_Hipopotamo', 0, 4),
             sw1=S_PAVAO, step=True),
    ])
    m.add_event('Posição do Pavão', 0, 1, [page([], priority=0),
                                           page(script(f'$gameMap.event({PV}).locate(23, 18);') + [cmd(214, [])],
                                                trigger=4, priority=0, sw1=S_PAVAO)])
    placa_tile(m, 16, 18, 137, 'TEMPLO DA XAVASCA LEPROSA', 'Proibida a entrada de feias.',
               '(Embaixo, a lápis: "e de Raulete")')
    m.add_event('Para a floresta', 18, m.h - 1, [page(transfer(M_MAUARA, MAUARA_FIM[0], MAUARA_FIM[1], 2, fade=0), trigger=1, priority=0)])
    m.add_event('Para a floresta', 19, m.h - 1, [page(transfer(M_MAUARA, MAUARA_FIM[0], MAUARA_FIM[1], 2, fade=0), trigger=1, priority=0)])
    info['ocupado'] = ocupado
    return info


# ================================================================ eventos comuns
def ce_cipo():
    return (wait(6) + se('Jump2')
            + move(-1, [rc(14, 0, 0)], w=True)
            + fadeout()
            + script(f'$gameVariables.setValue({V_MAPA}, $gameMap.mapId());')
            + [cmd(201, [1, V_MAPA, V_DX, V_DY, 2, 2])]
            + script("$gamePlayer.pose('');")
            + wait(10) + fadein()
            + sorteio(FALAS_ARMADILHA))


def ce_areia():
    return (se('Water3', pitch=60) + balloon(-1, 1)
            + move(-1, [rc(42, 170), rc(15, 8), rc(42, 90), rc(15, 8), rc(42, 0)], w=True)
            + se('Dive', vol=70)
            + fadeout()
            + script(f'$gameVariables.setValue({V_MAPA}, $gameMap.mapId()); $gamePlayer.setOpacity(255);')
            + [cmd(201, [1, V_MAPA, V_DX, V_DY, 2, 2])]
            + wait(10) + fadein()
            + sorteio([bar('Areia movediça?! Logo hoje que eu fiz as', 'unhas!'),
                       kuma('Achei você! Toda enlameada, mas achei!', i=2),
                       bar('Eca... tem lama até dentro das chiquinhas.')]))


def ce_falas():
    return sorteio([
        kuma('Baratelli, você tá ouvindo esses tambores?') + bar('Não é tambor, Kevinho. É o meu estômago.'),
        bar('Essa floresta tem mais armadilha que', 'contrato de celular!'),
        kuma('Com essas orelhas eu escuto TUDO.', 'Inclusive a sua barriga.', i=2),
        bar('Se eu morrer aqui, quero ser enterrada de', 'peruca.') + kuma('Que peruca?') + bar('A que eu ainda não tenho!'),
        kuma('Sabia que cavalo dorme em pé?', 'Eu tô quase.'),
        bar('O rastro da peruca tá ficando mais forte...', '...ou é cheiro de mato mesmo.'),
        kuma('Se a gente se perder, eu relincho bem alto', 'e alguém acha a gente.') + bar('Quem acharia a gente aqui?!')
        + kuma('...o Curupira?', i=3),
        bar('Leandra... Gusrola... eu sinto vocês nas', 'minhas cartas.'),
        kuma('Umamusume de verdade não se perde!', '...a gente tá perdido?', i=3) + bar('Claro que não. Estamos explorando.'),
        bar('Essa umidade tá acabando com as minhas', 'chiquinhas.'),
        kuma('Quando isso acabar, eu quero um balde', 'de cenoura.', i=2),
        bar('Mato... mais mato... e olha só: MATO!'),
        kuma('Ontem você leu a minha mão e disse que', 'ia dar tudo certo.') + bar('Eu disse "vai dar tudo certo...', 'provavelmente".'),
        bar('Ai, pisei em alguma coisa mole.', 'Não olha, Kevinho. NÃO OLHA.'),
    ])


# ================================================================ verificacao
def verificar(m, info, inicio, fim_tiles, nome):
    links, grade = info['links'], info['grade']
    alc = m.reach(inicio)
    assert any(t in alc for t in fim_tiles), f'{nome}: saida inalcancavel'
    # com todos os espinhos fechados, toda celula ainda chega na saida
    esp = set(info.get('espinhos', []))
    todas = {c for l in links for c in l}
    fim_cel = next(iter(c for c in todas if any(t in grade.tiles(c) for t in fim_tiles))) if False else None
    for c in todas:
        assert caminho(links, c, info['trilha'][-1], sem=esp), f'{nome}: celula {c} ilhada pelos espinhos'
    return len(alc)
