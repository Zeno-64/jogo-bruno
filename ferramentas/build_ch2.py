# Monta o Capitulo 2: Diademonius, casa da Leandra, calabouco (cela, laboratorio, rio) e a batalha contra Kura.
import copy, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ch1 as B
from fx import destaque, capitulo, move_pic_e, pose
from build_ch1 import (Map, rect, building, value_noise, cmd, text, narr, se, bgm, me, wait, balloon, tint,
                       flash, shake, transfer, switch, var_set, self_sw, pic, move_pic, erase_pic, anim, rc,
                       move, page, ambient, map_json, audio, load, save, A1, A2, A3, A4, C0, D0, END,
                       NORMAL, DOWN, LEFT, RIGHT, UP)

A5 = 1536
PROJ = B.PROJ

# ------------------------------------------------------------ constantes
M_DIADE, M_CASA, M_CELA, M_LAB, M_RIO = 7, 8, 9, 10, 11
(S_INICIO, S_ESMOLAS, S_VENDIDA, S_LEONA, S_GRAMPO, S_CELA, S_PC, S_SENHA, S_PONTE, S_FIM2) = range(5, 15)
V_ESMOLAS = 4
CE_ESMOLA, CE_PONTE = 2, 3
IT_GRAMPO = 31
TROOP_KURA = EN_KURA = 6
LEANDRA, LEONA_ACTOR, TERMINAL = 2, 3, 4
CLS_LEANDRA, CLS_LEONA = 9, 10
SK0 = 236
OPEN = [rc(17), rc(15, 3), rc(18), rc(15, 3), rc(19), rc(15, 3)]


# ------------------------------------------------------------ falas
def lea(*lines, i=0):
    return text(list(lines), face='Leandra', idx=i, name='Leandra')


def leo(*lines, i=0):
    return text(list(lines), face='Leona', idx=i, name='Leona')


def kura(*lines):
    return text(list(lines), face='Kura', idx=0, name='Kura')


def rau(*lines, i=0):
    return text(list(lines), face='Raulete', idx=i, name='Raulete')


def mae(*lines):
    return text(list(lines), face='People1', idx=5, name='Mãe')


def capuz(*lines):
    return text(list(lines), face='Evil', idx=7, name='Encapuzado')


def who(name, face, idx):
    return lambda *lines: text(list(lines), face=face, idx=idx, name=name)


# ------------------------------------------------------------ fluxo de eventos
def sub(lst, k=1):
    return [dict(c, indent=c['indent'] + k) for c in lst]


def if_(params, then, els=None):
    out = [cmd(111, params)] + sub(then) + [cmd(0, [], 1)]
    if els is not None:
        out += [cmd(411, [])] + sub(els) + [cmd(0, [], 1)]
    return out + [cmd(412, [])]


def choices(branches, cancel=-1):
    out = [cmd(102, [[b[0] for b in branches], cancel, 0, 2, 0])]
    for i, (label, body) in enumerate(branches):
        out += [cmd(402, [i, label])] + sub(body) + [cmd(0, [], 1)]
    return out + [cmd(404, [])]


def script(js):
    lines = js.split('\n')
    return [cmd(355, [lines[0]])] + [cmd(655, [l]) for l in lines[1:]]


def gold(n):
    return [cmd(125, [0 if n >= 0 else 1, 0, abs(n)])]


def item(iid, n):
    return [cmd(126, [iid, 0 if n >= 0 else 1, 0, abs(n)])]


def party_add(aid):
    return [cmd(129, [aid, 0, True])]


def party_remove(aid):
    return [cmd(129, [aid, 1, False])]


def followers(show):
    return [cmd(216, [0 if show else 1])]


def fadeout():
    return [cmd(221, [])]


def fadein():
    return [cmd(222, [])]


def stop_bgm(sec=1):
    return [cmd(242, [sec])]


def bgs(name, vol=50):
    return [cmd(245, [audio(name, vol)])]


def stop_bgs(sec=1):
    return [cmd(246, [sec])]


def call(ce):
    return [cmd(117, [ce])]


def battle(troop, can_escape=False, can_lose=True):
    return [cmd(301, [0, troop, can_escape, can_lose]), cmd(601, []), cmd(0, [], 1),
            cmd(603, []), cmd(0, [], 1), cmd(604, [])]


def set_self_js(map_id, ids, on=True):
    v = 'true' if on else 'false'
    return ' '.join(f"$gameSelfSwitches.setValue([{map_id}, {i}, 'A'], {v});" for i in ids)


def img(name, idx=0, d=2, pat=1, tile=0):
    return {'characterName': name, 'characterIndex': idx, 'direction': d, 'pattern': pat, 'tileId': tile}


def flame(m, x, y, idx=0, d=2, prio=1):
    m.add_event('Fogo', x, y, [page([], image=img('!Flame', idx, d), priority=prio, step=True, dir_fix=True, walk=False)])


def paint(m, rows, top, side, floor_id, region_skip=()):
    """'#' teto (A4 topo), 'W' parede (A4 lado); o resto e chao (floor_id(x, y, ch))."""
    H, W = len(rows), len(rows[0])
    ceil = {(x, y) for y in range(H) for x in range(W) if rows[y][x] == '#'}
    wall = {(x, y) for y in range(H) for x in range(W) if rows[y][x] == 'W'}
    m.auto(ceil, A4 + top * 48, 0)
    m.auto(wall, A4 + side * 48, 0, wall=True)
    for y in range(H):
        for x in range(W):
            ch = rows[y][x]
            if ch not in '#W':
                m.put(x, y, 0, floor_id(x, y, ch))
    m.region(ceil - set(region_skip))


def near_reachable(reach, x, y):
    return any((x + dx, y + dy) in reach for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ============================================================ 7. DIADEMONIUS
def build_diade():
    m = Map(32, 22, 2)
    W, H = m.w, m.h
    m.auto(rect(0, 0, W - 1, H - 1), A2 + 8 * 48, 0)
    stream = {(x, y) for x in (19, 20) for y in range(H)} | {(x, y) for x in range(21, W) for y in (15, 16)}
    road = ({(x, y) for x in range(W) for y in (7, 8)} | {(x, y) for x in (24, 25) for y in range(H)}) - stream
    m.auto(road, A2 + 10 * 48, 0)
    m.auto(stream, A1 + 14 * 48, 0)
    building(m, 2, 6, 1, 2, 3, 4, 5, 12)                 # casa da Leandra
    m.auto(rect(9, 1, 12, 2), A3 + 4 * 48, 0, wall=True)    # casa com o telhado desabado
    m.auto(rect(9, 3, 15, 4), A3 + 8 * 48, 0, wall=True)
    building(m, 1, 6, 11, 12, 13, 14, 5, 12)
    building(m, 9, 15, 11, 12, 13, 14, 6, 14)
    houses = rect(2, 1, 6, 4) | rect(9, 1, 15, 4) | rect(1, 11, 6, 14) | rect(9, 11, 15, 14)
    n1 = value_noise(W, H, 3, 3, 71)
    n2 = value_noise(W, H, 4, 3, 72)
    free = {(x, y) for x in range(W) for y in range(H)} - stream - road - houses
    soil = {c for c in free if n1[c[1], c[0]] > 0.58}
    m.auto(soil, A2 + 15 * 48, 1)
    m.auto({c for c in free - soil if n2[c[1], c[0]] > 0.64}, A2 + 7 * 48, 1)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y) in [(4, 4), (11, 4), (3, 14), (12, 14)]:
        b(x, y, 131)
    for (x, y, t) in [(3, 3, 97), (6, 13, 96), (14, 13, 98), (10, 3, 99), (5, 3, 52), (2, 4, 53), (14, 3, 54),
                      (1, 13, 55), (10, 14, 52), (15, 13, 53)]:
        b(x, y, t)
    for (x, y) in [(3, 1), (5, 2), (2, 11), (5, 12), (10, 11), (14, 12), (11, 2)]:
        b(x, y, 169)
    for (x, y, t) in [(13, 1, C0 + 26), (14, 1, C0 + 29), (15, 2, C0 + 30), (13, 2, 183), (15, 1, 171), (14, 2, 171)]:
        b(x, y, t)
    for (x, y) in [(19, 7), (20, 7), (19, 8), (20, 8)]:
        b(x, y, 83)
    for (x, y) in [(24, 15), (25, 15), (24, 16), (25, 16)]:
        b(x, y, 82)
    for dy, row in enumerate([[5, 6, 7], [13, 14, 15], [21, 22, 23]]):
        for dx, t in enumerate(row):
            b(27 + dx, 9 + dy, t)
    for (x, y) in [(8, 1), (17, 2), (0, 9), (17, 11), (30, 0), (22, 20), (31, 12), (7, 17), (0, 18)]:
        b(x, y, 232); b(x, y + 1, 240)
    stuff = [(27, 3, 181), (29, 3, 182), (30, 4, 189), (26, 5, 190), (23, 4, 147), (22, 2, 149), (23, 2, 149),
             (9, 9, 156), (13, 17, 139), (29, 18, 142), (31, 18, 143), (30, 20, 142), (28, 20, 143),
             (6, 20, C0 + 24), (16, 19, C0 + 25), (2, 16, C0 + 26), (15, 9, C0 + 29), (11, 18, 164),
             (5, 10, 141), (8, 15, 144), (3, 19, 171), (26, 13, 171), (30, 7, 148), (17, 16, 239), (12, 20, 247),
             (21, 1, 239), (28, 14, 247), (1, 6, 182), (7, 6, 181), (16, 6, 239), (14, 6, 137), (18, 4, 241),
             (10, 19, 241), (23, 12, 239), (4, 9, 247), (26, 19, 247)]
    for (x, y, t) in stuff:
        b(x, y, t)
    return m


def beg_npc(m, name, x, y, image, idle, opts, ok, amount, after, move_type=0):
    branches = []
    for i, (label, body) in enumerate(opts):
        if i == ok:
            body = body + gold(amount) + call(CE_ESMOLA) + self_sw()
        branches.append((label, body))
    branches.append(('Deixa pra lá', []))
    p1 = idle + choices(branches, cancel=len(branches) - 1)
    kw = dict(move_type=move_type, speed=2, freq=2) if move_type else {}
    return m.add_event(name, x, y, [page(p1, image=image, **kw),
                                    page(after, image=image, self_switch='A', **kw)])


def events_diade(m):
    m.add_event('Ambiente', 0, 0, [page(tint([-20, -24, -34, 40], 0) + [cmd(214, [])], trigger=4, priority=0)])
    m.add_event('Casa da Leandra', 4, 4, [
        page(lea('(Ainda não consegui cinco esmolas...', 'Se eu voltar agora, a mamãe me mata!)', i=1)
             + move(-1, [DOWN], w=True), trigger=1, priority=0, sw1=S_INICIO),
        page(se('Door1') + transfer(M_CASA, 6, 8, 8), trigger=1, priority=0, sw1=S_ESMOLAS),
    ])
    m.add_event('Casa desabada', 11, 4, [page(narr('Não tem ninguém aí dentro.', 'Metade da casa desabou.'))])
    m.add_event('Porta', 3, 14, [page(narr('A porta está pregada com tábuas.'))])
    m.add_event('Porta', 12, 14, [page(narr('"NÃO BATA. NÃO TEMOS NADA. NEM PORTA."', '...a porta cai no chão quando você encosta.'))])
    m.add_event('Placa', 14, 6, [page(narr('DIADEMONIUS', 'Cidade vizinha da Mansão Raulete.', '(A prefeitura agradece a sua visita... ou não.)'))])
    flame(m, 23, 4, 3, 2)
    flame(m, 30, 7, 3, 2)
    m.add_event('Túmulos', 29, 18, [page(narr('"Aqui jaz um morador de Diademonius.', 'Morreu careca e sem dinheiro."'))])

    joaq = who('Seu Joaquim', 'People2', 0)
    beg_npc(m, 'Seu Joaquim', 8, 10, img('People2', 0, 2),
            joaq('Hmpf. Mais uma criança pedindo', 'dinheiro. Nessa cidade, até os ratos', 'pedem esmola.'),
            [('Contar a verdade', lea('A minha mãe me mandou pedir...', 'O bolsa família dela não caiu.', i=1)
              + joaq('...Pelo menos você é honesta, menina.', 'Toma uns trocados. E não conta pra', 'ninguém, hein?')),
             ('Inventar uma história triste', lea('Moço, eu tenho doze irmãos e um', 'cachorro de três pernas...', i=1)
              + joaq('Conta outra! Ontem eram oito irmãos', 'e um papagaio!')),
             ('Exigir o dinheiro', lea('Passa o dinheiro, velho!')
              + joaq('Mas que menina mais mal-educada!', 'Xô! Xô!'))],
            0, 3, joaq('Já te dei, menina. Vai pra casa antes', 'que escureça.'))

    perp = who('Dona Perpétua', 'People3', 1)
    beg_npc(m, 'Dona Perpétua', 14, 17, img('People3', 1, 2),
            perp('Ai, que cidade horrorosa...', 'Nem tenho onde exibir a minha peruca', 'nova.'),
            [('Elogiar o cabelo dela', lea('Que cabelo lindo, senhora!', 'Parece cabelo de rainha!', i=2)
              + perp('Ai, que gracinha! É peruca, querida...', 'da loja oficial da família Raulete!')
              + perp('Toma, compra um pirulito. E nunca', 'corte esse seu cabelo, viu?', 'Ele vale ouro.')),
             ('Perguntar se é peruca', lea('Isso aí na sua cabeça é peruca?')
              + perp('COMO OUSA?! Saia daqui, pirralha!')),
             ('Pedir direto', lea('Me dá um dinheirinho, moça?')
              + perp('Eu não falo com crianças sujas antes', 'do almoço.'))],
            0, 5, perp('Cuide bem desse cabelo, loirinha.', 'Tem gente que pagaria caro por ele...'))

    ze = who('Zé do Córrego', 'People1', 4)
    beg_npc(m, 'Zé do Córrego', 21, 11, img('People1', 4, 4),
            ze('Pesquei três pneus e uma bota hoje.', 'Dia bom de pescaria!'),
            [('Contar uma piada', lea('Por que o peixe não usa computador?')
              + lea('Porque ele tem medo da rede!', i=2)
              + ze('HAHAHAHA! Essa foi boa, menina!', 'Toma, pela risada.')),
             ('Ajudar a pescar', lea('Posso ajudar o senhor a pescar?')
              + ze('Aqui só tem esgoto, menina. Vai que', 'você cai e vira um mutante.')),
             ('Chorar alto', lea('BUÁÁÁÁÁÁ!', i=1)
              + ze('Ô, menina, chorar aqui só deixa o', 'córrego mais salgado. E ele já é roxo.'))],
            0, 2, ze('Volta amanhã com outra piada, que eu', 'te dou mais um trocado!'))

    bento = who('Guarda Bento', 'People3', 6)
    beg_npc(m, 'Guarda Bento', 22, 5, img('People3', 6, 2),
            bento('Tô de folga. Nem adianta me pedir', 'nada.'),
            [('Cantar uma música', lea('Lá-lá-láááá! Diademonius, cidade', 'linda, nunca vi coisa igual!', i=2)
              + se('Buzzer1')
              + bento('PARA! PARA! Toma o dinheiro, toma!', 'Mas pelo amor de tudo, para de cantar!')),
             ('Bater continência', lea('Sim, senhor, capitão!')
              + bento('Sou só soldado raso, menina. Não tenho', 'dinheiro nem pra mim.')),
             ('Dançar', lea('Olha, eu sei dançar!', i=2)
              + bento('Isso aí é dança ou você pisou num', 'prego?'))],
            0, 4, bento('Pelo menos você parou de cantar...'))

    sab = who('Sabino', 'People2', 4)
    beg_npc(m, 'Sabino', 28, 5, img('People2', 4, 2),
            sab('Vendo de tudo! Tudo quebrado, mas', 'vendo!'),
            [('Oferecer ajuda', lea('Posso carregar as suas caixas em', 'troca de uma moedinha?')
              + sab('Uma trabalhadora! Gostei. Mãos à obra!')
              + fadeout() + se('Push') + wait(20) + se('Push') + wait(30) + fadein()
              + narr('Leandra carrega caixas por um tempão...')
              + sab('Bom trabalho! Aqui está o seu', 'pagamento.')),
             ('Fingir que é cliente', lea('Quanto custa essa panela furada?')
              + sab('Pra você? 50G. Tem? Não?', 'Então tchau.')),
             ('Fazer cara de coitada', narr('Leandra faz os olhinhos mais tristes do', 'mundo.')
              + sab('Comerciante não tem coração, menina.', 'Só tem caixa registradora.'))],
            0, 5, sab('Precisando de trabalho, é só voltar!', 'Pago mal, mas pago!'))

    nena = who('Tia Nena', 'People4', 1)
    beg_npc(m, 'Tia Nena', 28, 12, img('People4', 1, 2),
            nena('Olha o pastel de vento! Só tem vento,', 'mas é quentinho!'),
            [('Fazer cara de pidona', narr('Leandra arregala os olhos e faz', 'biquinho.')
              + nena('Ai, que dó... Toma, filha.', 'E leva um pastel de vento pra viagem.')),
             ('Reclamar do pastel', lea('Pastel de vento não enche barriga...')
              + nena('Então vai comer brisa, malcriada!')),
             ('Pedir um pastel de carne', lea('Tem pastel de carne?')
              + nena('Carne? Em Diademonius? HAHAHA!', 'Essa foi a piada do ano.'))],
            0, 2, nena('Volta sempre, loirinha! O vento é', 'por conta da casa.'))

    beg_npc(m, 'Capivara', 23, 19, img('$Capivara', 0, 2),
            narr('A capivara mastiga um pneu com toda a', 'calma do mundo.'),
            [('Fazer carinho', narr('Leandra faz um cafuné na capivara...')
              + narr('A capivara fecha os olhos... e cospe', 'uma moeda brilhante! PLOC!')
              + lea('Obrigada, dona capivara!', i=2)),
             ('Pedir esmola pra capivara', lea('Me dá um dinheirinho, capivara?')
              + narr('A capivara te encara. Ela não entendeu', 'nada, mas te julgou mesmo assim.')),
             ('Imitar a capivara', narr('Leandra mastiga o ar bem devagarinho.', 'A capivara não se impressiona.'))],
            0, 1, narr('A capivara voltou a mastigar o pneu.', 'Ela parece satisfeita.'), move_type=1)


def ce_esmola():
    lst = ([cmd(122, [V_ESMOLAS, V_ESMOLAS, 1, 0, 1])]
           + destaque('moeda', imagem='Item_Esmola', nome='+1 esmola!', texto='Esmolas: \\V[4] de 5')
           + if_([1, V_ESMOLAS, 0, 5, 1],
                 if_([0, S_ESMOLAS, 1],
                     switch(S_ESMOLAS) + me('Item')
                     + lea('Consegui cinco esmolas!', 'A mamãe vai ficar tão orgulhosa!', i=2)
                     + lea('Hora de voltar pra casa!', i=2))))
    return {'id': CE_ESMOLA, 'list': lst + [END], 'name': 'Esmola recebida', 'switchId': 1, 'trigger': 0}


# ============================================================ 8. CASA DA LEANDRA
def build_casa():
    m = Map(13, 10, 3)
    B.room(m, 0, 0, 12, 9, 16, 24, 2, door=(6, 9))
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y, t) in [(2, 3, 174), (2, 4, 182), (7, 5, 238), (6, 5, 239), (8, 5, 239), (10, 3, 237), (11, 3, 236),
                      (1, 8, 228), (10, 8, 220), (11, 7, 212), (4, 2, 216), (9, 1, 36), (2, 1, 44), (1, 5, 248)]:
        b(x, y, t)
    b(7, 5, C0 + 29, 3)
    b(9, 7, C0 + 25)
    return m


def events_casa(m):
    ambient(m, NORMAL)
    mae_e = m.add_event('Mãe', 7, 4, [
        page(mae('Ainda tá aqui?! Vai pedir esmola!', 'E só volta com cinco, hein!'), image=img('People1', 5, 2)),
    ])
    men = []
    for (x, y, d) in [(5, 4, 2), (9, 4, 2), (9, 6, 4)]:
        men.append(m.add_event('Encapuzado', x, y, [
            page([], priority=0, through=True),
            page(capuz('...'), image=img('Evil', 7, d), sw1=S_ESMOLAS),
        ]))
    intro = (fadeout() + stop_bgm(1)
             + party_remove(1) + party_add(LEANDRA) + followers(True)
             + tint(NORMAL, 0)
             + capitulo('Capitulo2')
             + narr('Enquanto isso, no Continente Sodoma de', 'Calvice...')
             + narr('Diademonius: uma cidade em ruínas,', 'vizinha da mansão de Raulete.')
             + narr('Casas caindo aos pedaços e córregos tão', 'poluídos que brilham no escuro.')
             + bgm('Scene3', vol=70)
             + fadein()
             + balloon(mae_e, 5)
             + mae('LEANDRA! Acorda, menina!')
             + balloon(-1, 1)
             + lea('B-bom dia, mamãe!', i=2)
             + mae('Bom dia nada. O bolsa família ainda', 'não caiu e a geladeira tá vazia.')
             + mae('Vai pra rua pedir esmola.', 'E só volta com CINCO esmolas, no mínimo!')
             + lea('De novo, mamãe? Ontem ninguém', 'me deu nada...', i=1)
             + mae('Então capricha nessa carinha de', 'loirinha inocente! Anda logo!')
             + lea('T-tá bom, mamãe!')
             + lea('(Eu vou conseguir! Vou deixar a', 'mamãe orgulhosa de mim!)', i=2)
             + narr('Peça esmola para as pessoas de Diademonius.', 'Cada uma se convence de um jeito: preste',
                    'atenção no que elas dizem!')
             + narr('Consiga pelo menos 5 esmolas e depois', 'volte para casa.')
             + var_set(V_ESMOLAS, 0) + switch(S_INICIO))
    m.add_event('Introdução', 0, 9, [page(intro, trigger=3, priority=0),
                                       page([], priority=0, sw1=S_INICIO)])
    venda = (wait(20)
             + lea('Mamãe! Consegui cinco esmolas!', i=2)
             + balloon(-1, 1)
             + narr('Mas, dentro de casa, a mãe de Leandra está', 'cercada de homens encapuzados...')
             + bgm('Scene4', vol=70)
             + lea('Mamãe...? Quem são esses moços?', i=1)
             + mae('Ah, filha, chegou na hora certinha.', 'Passa as esmolas pra cá.')
             + se('Coin') + gold(-9999)
             + narr('A mãe pega todas as moedas da mão de', 'Leandra.')
             + capuz('É essa a loirinha?')
             + mae('Essa mesma! Olha só esse cabelo:', 'liso, comprido, dourado... de primeira!')
             + capuz('O Mestre Raulete vai ficar satisfeito.', 'Aqui está o pagamento, como combinado.')
             + se('Coin') + wait(10) + se('Coin')
             + lea('P-pagamento...? Mamãe, do que eles', 'estão falando?', i=1)
             + mae('Filha... a mamãe te vendeu.')
             + me('Shock1') + balloon(-1, 1)
             + lea('O QUÊ?!', i=1)
             + mae('Ué, o bolsa família não caiu, e eu', 'queria fazer um churrasquinho!')
             + mae('Picanha e uma cervejinha bem', 'geladinha... Você entende, né, filha?')
             + balloon(-1, 6)
             + lea('N-não... NÃO!', i=1)
             + capuz('Peguem a menina!')
             + move(-1, [rc(16)], w=True)
             + se('Jump1') + move(men[2], [rc(37), rc(14, -3, 3)], w=True)
             + balloon(-1, 1)
             + move(-1, [rc(17), rc(15, 12), rc(18), rc(15, 12)], w=True)
             + move(men[0], [rc(37), rc(29, 5), DOWN, DOWN, DOWN, RIGHT], w=True)
             + move(-1, [rc(19)], w=True)
             + pose(men[0], 'soco', olhar=-1, espera=8)
             + se('Blow3') + flash([255, 255, 255, 255], 20) + shake(7, 9, 15) + pose(-1, 'dor', espera=20)
             + pose(-1, 'queda', segurar=True)
             + lea('Ai...!', i=1)
             + fadeout() + stop_bgm(2)
             + wait(60)
             + narr('Tudo fica escuro.')
             + narr('Leandra perdeu os sentidos...')
             + switch(S_VENDIDA)
             + transfer(M_CELA, 4, 4, 2, fade=2))
    m.add_event('Venda', 12, 9, [page([], priority=0),
                                  page(venda, trigger=3, priority=0, sw1=S_ESMOLAS),
                                  page([], priority=0, sw1=S_VENDIDA)])
    m.add_event('Saída', 6, 9, [page(se('Door1') + transfer(M_DIADE, 4, 5, 2), trigger=1, priority=0, sw1=S_INICIO)])
    m.add_event('Aviso', 4, 2, [page(narr('Um papel pregado na parede:', '"AVISO DE CORTE: conta de luz atrasada', 'há 14 meses."')
                                     + lea('A gente nem tem luz...', i=1))])
    m.add_event('Cama', 2, 4, [page(narr('A cama da Leandra. Tem mais mola do', 'que colchão.'))])
    m.add_event('Barril', 10, 3, [page(narr('Um barril de cerveja... vazio.', 'A mamãe bebeu tudo de novo.'))])
    return mae_e


# ============================================================ 9. CALABOUCO - CELA
CELA_ROWS = [
    '###################',
    '#WWWWWWW#WWWWW#WWW#',
    '#WWWWWWW#WWWWW#WWW#',
    '#ccccccc#ccccc#...#',
    '#ccccccc#ccccc#...#',
    '#ccccccc#ccccc#...#',
    '#ccccccc#ccccc#...#',
    '#bbbbbbb#bbbbb#...#',
    '#.................#',
    '#.................#',
    '###################',
]


def build_cela():
    m = Map(19, 11, 4)
    paint(m, CELA_ROWS, 16, 24, lambda x, y, ch: A5 + (96 if ch == 'c' else 23))
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x0, x1, door) in ((1, 7, 4), (9, 13, 11)):
        for x in range(x0, x1 + 1):
            k = (x - x0) % 2
            b(x, 6, 245 + k, 3)
            if x != door:
                b(x, 7, 253 + k)
    for (x, y, t) in [(1, 3, C0 + 151), (1, 4, C0 + 159), (1, 6, 230), (3, 2, C0 + 131), (4, 2, C0 + 132),
                      (5, 2, C0 + 133), (6, 2, 8), (2, 1, 1), (7, 1, 176), (10, 5, 242), (13, 3, C0 + 151),
                      (13, 4, C0 + 159), (9, 6, 231), (17, 4, C0 + 149), (16, 4, C0 + 157), (15, 6, 220),
                      (17, 6, 238), (16, 2, 2), (1, 9, 124), (6, 9, 125), (12, 1, 9), (10, 2, 16)]:
        b(x, y, t)
    return m


def events_cela(m):
    m.add_event('Ambiente', 0, 0, [page(tint([-40, -40, -24, 30], 0) + [cmd(214, [])], trigger=4, priority=0)])
    leona = m.add_event('Leona', 2, 4, [
        page(leo('...'), image=img('$Leona', 0, 6)),
        page([], priority=0, through=True, sw1=S_LEONA),
    ])
    mural = (pic(5, 'Mural_Raulete', 408, 222, opacity=0) + move_pic(5, 408, 222, 255, 40, w=True)
             + leo('Esse mural conta a história da', 'família Raulete.')
             + move_pic(5, 794, 200, 255, 50, scale=160, w=True)
             + leo('Diz a lenda que, por causa de uma', 'maldição, todos os membros da família', 'Raulete nascem carecas.')
             + move_pic(5, 403, 200, 255, 50, scale=160, w=True)
             + leo('Eles usam perucas, claro... mas as', 'perucas apodrecem em pouco tempo', 'na cabeça deles.')
             + move_pic(5, 14, 200, 255, 50, scale=160, w=True)
             + leo('Então, por pura ganância e vaidade,', 'eles roubam o cabelo de crianças', 'e jovens.')
             + leo('Dizem que cabelo jovem é mais puro...', 'e dura muito mais naquelas cabeças', 'lisas.')
             + move_pic(5, 408, 222, 0, 40, scale=100, w=True) + erase_pic(5))
    acorda = (pose(-1, 'queda', segurar=True) + bgs('Drips', 45) + wait(60)
              + narr('...')
              + fadein()
              + balloon(-1, 8)
              + lea('Ai... minha cabeça...', i=1)
              + lea('Onde... onde eu tô?', i=1)
              + se('Chain', vol=60)
              + leo('Finalmente acordou, loirinha.')
              + pose(-1, '') + move(-1, [rc(14, 0, 0)], w=True)
              + move(-1, [rc(17)], w=True)
              + balloon(-1, 1)
              + lea('Quem é você?!', i=1)
              + leo('Leona. E pode parar de me olhar com', 'essa cara de pobre.')
              + pose(leona, 'riso', espera=6)
              + leo('Achei que você tinha morrido igual', 'àquele ali.')
              + move(leona, [rc(19)], w=True)
              + balloon(-1, 1)
              + move(-1, [rc(14, 0, 0)], w=False)
              + lea('UM ESQUELETO?!', i=1)
              + lea('Onde a gente tá? O que tá', 'acontecendo?!', i=1)
              + move(leona, [rc(18)], w=True)
              + leo('No calabouço da família Raulete.')
              + leo('É aqui que eles arrancam o cabelo das', 'crianças pra fazer as perucas da', 'família deles.')
              + lea('Perucas?! Mas por quê?!', i=1)
              + leo('Tá vendo aquele mural na parede?', 'Eu já li umas cem vezes. Não tinha', 'mais nada pra fazer aqui.')
              + move(-1, [rc(19)], w=True)
              + mural
              + move(-1, [rc(17)], w=True)
              + lea('Então... eles vão pegar o meu cabelo?!', i=1)
              + leo('O seu e o meu. E o meu é MUITO mais', 'bonito, então eu devo ser a próxima.')
              + lea('A gente precisa fugir daqui!')
              + leo('Até que enfim uma ideia boa.')
              + leo('Tá bom, loirinha. Vamos juntar forças.', 'Só dessa vez, hein?')
              + move(leona, [rc(37), RIGHT, RIGHT], w=True)
              + party_add(LEONA_ACTOR)
              + script(f'$gamePlayer.followers().follower(0).locate($gameMap.event({leona}).x, $gameMap.event({leona}).y);')
              + switch(S_LEONA)
              + destaque('membro', rosto='Leona', indice=0, nome='Leona',
                         texto='A Arrogante. Se acha melhor que todo mundo.')
              + leo('Procura alguma coisa nessa cela que', 'abra aquela porta. Eu não vou sujar', 'as minhas mãos.')
              + self_sw())
    m.add_event('Despertar', 0, 10, [page([], priority=0),
                                       page(acorda, trigger=3, priority=0, sw1=S_VENDIDA),
                                       page([], priority=0, self_switch='A')])
    m.add_event('Esqueleto', 7, 3, [
        page(narr('Um esqueleto... de alguém que ficou', 'preso aqui antes.')
             + narr('Na caveira ainda tem um laço de fita...', 'mas nenhum fio de cabelo.')
             + lea('Coitadinho...', i=1)
             + narr('Entre os ossos, alguma coisa brilha.')
             + item(IT_GRAMPO, 1)
             + destaque('item', imagem='Item_Grampo', nome='Grampo de cabelo',
                        texto='Enferrujado, mas dá pra abrir fechaduras.')
             + leo('Um grampo? Isso abre fechadura, sabia?', 'Pelo menos nos filmes abre.')
             + switch(S_GRAMPO), image=img('', 0, 2, 0, tile=250)),
        page(lea('Obrigada, esqueleto. Eu prometo que', 'vou sair daqui.', i=1), image=img('', 0, 2, 0, tile=250), sw1=S_GRAMPO),
    ])
    jail = img('!Door2', 2, 2, 0)
    m.add_event('Porta da cela', 4, 7, [
        page(if_([8, IT_GRAMPO],
                 lea('Deixa eu tentar com o grampo...') + se('Key') + wait(30) + se('Key') + wait(20)
                 + se('Open1') + move(0, OPEN, w=True) + self_sw() + item(IT_GRAMPO, -1) + switch(S_CELA)
                 + leo('Uau. Onde você aprendeu isso?', i=1)
                 + lea('A mamãe trancava a geladeira.')
                 + leo('...Isso explica muita coisa.'),
                 narr('A porta da cela está trancada.')
                 + leo('Dã. Por isso que se chama PRISÃO.')), image=jail, walk=False),
        page([], image=dict(jail, direction=8), priority=0, through=True, walk=False, self_switch='A'),
    ])
    m.add_event('Outra cela', 11, 7, [page(narr('Outra cela... vazia.', 'Só ossos e silêncio.'), image=jail, walk=False)])
    m.add_event('Mural', 4, 2, [page(pic(5, 'Mural_Raulete', 408, 222, opacity=0) + move_pic(5, 408, 222, 255, 20, w=True)
                                     + leo('Carecas, gananciosos e vaidosos.', 'Que família, hein?')
                                     + move_pic(5, 408, 222, 0, 20, w=True) + erase_pic(5))])
    m.add_event('Palha', 1, 4, [page(narr('Palha velha e mofada...') + balloon(-1, 1) + lea('...e uma barata!', i=1))])
    m.add_event('Balde', 1, 6, [page(narr('Um balde enferrujado. Melhor nem saber', 'o que tem dentro.'))])
    m.add_event('Rachadura', 6, 2, [page(narr('Uma rachadura na parede... pequena', 'demais pra passar.'))])
    flame(m, 15, 1, 0, 2, prio=0)
    flame(m, 17, 1, 0, 2, prio=0)
    m.add_event('Escada', 16, 2, [page(se('Move1') + transfer(M_LAB, 12, 15, 8), trigger=1, priority=0)])
    return leona


# ============================================================ 10. LABORATORIO DAS PERUCAS
LAB_ROWS = [
    '#########################',
    '#WWWW#WWWW#WWW#WWWW#WWWW#',
    '#WWWW#WWWW#WWW#WWWW#WWWW#',
    '#rrrr#rrrr#mmm#rrrr#rrrr#',
    '#rrrr#rrrr#mmm#rrrr#rrrr#',
    '#rrrr#rrrr#mmm#rrrr#rrrr#',
    '##m####m####m####m####m##',
    '#WmWWWWmWWWWmWWWWmWWWWmW#',
    '#WmWWWWmWWWWmWWWWmWWWWmW#',
    '#.......................#',
    '#.......................#',
    '#.......................#',
    '#.......................#',
    '#.......................#',
    '#.......................#',
    '#.......................#',
    '############S############',
    '#########################',
]
DOORS = {2: (5, 0), 7: (6, 1), 12: (4, 2), 17: (6, 2), 22: (5, 2)}


def build_lab():
    m = Map(25, 18, 6)
    paint(m, LAB_ROWS, 1, 9, lambda x, y, ch: A5 + {'r': 97, 'm': 17}.get(ch, 49))
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    D = D0
    for (x, y, t) in [
            # sala A (I)
            (3, 3, 250), (1, 3, D + 0), (4, 2, 181), (4, 3, 189), (1, 5, D + 7),
            # sala B (R)
            (8, 3, 250), (6, 3, D + 4), (9, 3, D + 5), (9, 4, 214), (9, 5, 222),
            # sala C (H)
            (16, 3, 250), (15, 2, C0 + 118), (15, 3, C0 + 126), (18, 2, C0 + 118), (18, 3, C0 + 126), (18, 5, D + 1),
            # sala D (A)
            (21, 3, 250), (23, 2, C0 + 98), (23, 3, C0 + 106), (20, 2, C0 + 98), (20, 3, C0 + 106), (23, 5, D + 2),
            # corredor e escada
            (12, 2, 1), (12, 1, C0 + 30), (11, 2, 57), (13, 2, 59),
            # salao
            (12, 12, 250), (11, 10, C0 + 245), (12, 10, C0 + 246), (13, 10, C0 + 247),
            (11, 11, C0 + 253), (12, 11, C0 + 254), (13, 11, C0 + 255),
            (2, 10, D + 4), (4, 10, D + 5), (20, 10, D + 4), (22, 10, D + 5),
            (3, 15, D + 0), (5, 15, D + 1), (19, 15, D + 2), (21, 15, D + 3),
            (8, 12, D + 7), (16, 13, D + 7), (7, 14, D + 7), (17, 10, D + 7),
            (8, 10, 248), (16, 10, 249),
            (4, 7, C0 + 112), (5, 7, D + 6), (9, 7, C0 + 113), (10, 7, C0 + 151), (14, 7, C0 + 151),
            (15, 7, C0 + 112), (19, 7, D + 6), (20, 7, C0 + 113), (11, 8, 67), (13, 8, 51),
            (12, 16, 9)]:
        b(x, y, t)
    for (x, y, t) in [(3, 3, 143), (8, 3, 143), (16, 3, 143), (21, 3, 143), (12, 12, 129), (8, 10, 125), (16, 10, 130)]:
        b(x, y, t, 3)
    return m


def events_lab(m):
    m.add_event('Ambiente', 0, 0, [page(tint([-10, 0, 10, 0], 0) + [cmd(214, [])], trigger=4, priority=0)])
    doors = {}
    for x, (idx, pat) in DOORS.items():
        im = img('!SF_Door1', idx, 2, pat)
        if x == 12:
            locked = narr('PORTA DE SEGURANÇA.', 'ACESSO SOMENTE COM SENHA.')
        else:
            locked = narr('Trancada. Um aviso diz:', '"ABERTURA PELO TERMINAL CENTRAL."')
        doors[x] = m.add_event('Porta', x, 8, [
            page(locked, image=im, walk=False),
            page([], image=dict(im, direction=8), priority=0, through=True, walk=False, self_switch='A'),
        ])
    side = [doors[x] for x in (2, 7, 17, 22)]
    center = doors[12]
    open_js = set_self_js(M_LAB, side, True)
    close_js = set_self_js(M_LAB, side, False)
    m.add_event('Chegada', 0, 17, [
        page([], priority=0),
        page(wait(15) + balloon(-1, 1)
             + leo('Que lugar é esse? Parece um', 'laboratório...', i=1)
             + lea('Olha quanta peruca... e tem cabelo', 'dentro desses tubos!', i=1)
             + leo('Que nojo. Vamos achar a saída logo.')
             + lea('Aquele computador no meio da sala', 'deve controlar as portas!')
             + self_sw(), trigger=3, priority=0, sw1=S_CELA),
        page([], priority=0, self_switch='A'),
    ])
    primeiro = (narr('Leandra aperta um botão qualquer...')
                + se('Computer') + wait(20)
                + se('Siren') + flash([255, 40, 40, 160], 30)
                + narr('ALERTA! INVASORAS DETECTADAS!')
                + narr('PORTAS DE MANUTENÇÃO DESTRAVADAS.')
                + se('Autodoor'))
    for d in side:
        primeiro += move(d, OPEN, w=False)
    primeiro += (wait(24) + script(open_js)
                 + narr('BLOQUEIO TOTAL EM 5 MINUTOS.', 'DIGITE A SENHA PARA LIBERAR A SAÍDA.')
                 + [cmd(124, [0, 300])] + switch(S_PC)
                 + leo('Uma senha?! A gente não sabe senha', 'nenhuma!', i=1)
                 + lea('Talvez a resposta esteja nessas salas', 'que abriram!'))
    certo = (destaque('evento', imagem='Evento_Cadeado', titulo='ACESSO LIBERADO', nome='Senha correta: HAIR',
                      texto='A porta do meio foi destravada.')
             + [cmd(124, [1])] + switch(S_SENHA)
             + se('Autodoor') + move(center, OPEN, w=True) + script(set_self_js(M_LAB, [center], True))
             + se('Siren') + flash([255, 30, 30, 200], 30, w=False)
             + narr('ALERTA MÁXIMO! FUGA EM ANDAMENTO!')
             + bgm('Battle2', vol=80)
             + leo('A porta do meio abriu! CORRE,', 'LEANDRA!', i=1)
             + lea('Tô correndo, tô correndo!', i=1))
    errado = (se('Buzzer2') + narr('SENHA INCORRETA.')
              + leo('Errou! Procura nos papéis das salas:', 'cada um tem uma letra e a ordem dela!', i=1))
    senha = (narr('O terminal pede uma senha de 4 letras.')
             + choices([('Digitar a senha', [cmd(320, [TERMINAL, ''])] + [cmd(303, [TERMINAL, 4])]
                         + if_([12, "$gameActors.actor(4).name().toUpperCase() === 'HAIR'"], certo, errado)),
                        ('Sair', [])], cancel=1))
    m.add_event('Computador', 12, 12, [
        page(primeiro),
        page(senha, sw1=S_PC),
        page(narr('ACESSO LIBERADO.', 'TENHA UM ÓTIMO DIA DE FUGA.'), sw1=S_SENHA),
    ])
    relogio = if_([3, 0, 1],
                  [cmd(124, [1])]
                  + se('Siren') + flash([255, 30, 30, 200], 40, w=False) + shake(6, 9, 30, w=False)
                  + narr('TEMPO ESGOTADO!', 'BLOQUEIO TOTAL ATIVADO.')
                  + fadeout()
                  + script(close_js)
                  + transfer(M_LAB, 12, 13, 8, fade=2)
                  + wait(15) + fadein()
                  + narr('O sistema reiniciou e as portas se', 'fecharam de novo.')
                  + leo('Droga! Vamos ter que ligar esse treco', 'de novo!', i=1)
                  + switch(S_PC, False))
    m.add_event('Cronômetro', 24, 17, [page([], priority=0), page(relogio, trigger=4, priority=0, sw1=S_PC)])
    alarme = se('Siren', vol=40) + tint([68, -20, -20, 0], 30, w=True) + tint([0, 0, 0, 0], 30, w=True)
    m.add_event('Alarme', 24, 0, [page([], priority=0), page(alarme, trigger=4, priority=0, sw1=S_SENHA)])
    docs = [
        (16, 3, 'H', [('MEMORANDO 01 - Por ordem do Mestre', 'Raulete, a senha do terminal foi trocada.'),
                      ('Para ninguém esquecer, cada sala guarda', 'UMA letra. Esta é a PRIMEIRA: H.')]),
        (21, 3, 'A', [('MEMORANDO 02 - A peruca nº 347 apodreceu', 'na cabeça do patrão em apenas 3 dias.'),
                      ('Precisamos de cabelo mais jovem.', 'Segunda letra da senha: A.')]),
        (3, 3, 'I', [('MEMORANDO 03 - Proibido usar condicionador', 'barato nas perucas. O patrão ficou com',
                      'caspa até no monóculo.'), ('Terceira letra da senha: I.',)]),
        (8, 3, 'R', [('MEMORANDO 04 - Dica para os esquecidos:', 'a senha é aquilo que o patrão mais deseja...',
                      'em inglês.'), ('Quarta letra da senha: R.',)]),
    ]
    for (x, y, letter, texts) in docs:
        pos = 'HAIR'.index(letter) + 1
        lst = (pic(10, f'Papel_{letter}', 470, 236, opacity=0, scale=90) + se('Book1')
               + move_pic_e(10, 408, 222, 255, 24, scale=100, easing=2, w=True))
        for t in texts:
            lst += narr(*t)
        lst += (move_pic_e(10, 360, 210, 0, 18, scale=94, easing=1, w=True) + erase_pic(10)
                + destaque('aviso', imagem=f'Papel_{letter}', nome=f'Pista: letra {letter}',
                           texto=f'Letra {pos} de 4 da senha'))
        m.add_event(f'Documento {letter}', x, y, [page(lst)])
    for (x, y) in [(2, 10), (20, 10), (6, 3)]:
        m.add_event('Tubo', x, y, [page(narr('Um tubo cheio de líquido verde...', 'com mechas de cabelo LOIRO boiando.'))])
    for (x, y) in [(4, 10), (22, 10), (9, 3)]:
        m.add_event('Tubo', x, y, [page(narr('Um tubo com cabelo preto boiando.', 'Tem uma etiqueta: "LOTE 12 - FRESCO".'))])
    for (x, y) in [(3, 15), (5, 15), (19, 15), (21, 15), (1, 3), (18, 5), (23, 5)]:
        m.add_event('Peruca', x, y, [page(narr('Uma cabeça de manequim usando uma', 'peruca. O cabelo parece de verdade...')
                                         + leo('Não quero nem pensar de quem era.', i=1))])
    m.add_event('Máquina', 12, 11, [page(narr('Uma máquina enorme com um aviso:', '"SECADOR INDUSTRIAL DE PERUCAS".'))])
    m.add_event('Escada', 12, 2, [page(se('Move1') + transfer(M_RIO, 12, 16, 8), trigger=1, priority=0)])
    m.add_event('Escada de volta', 12, 16, [page(leo('Voltar pra cela? Nem pensar!', i=1)
                                                 + move(-1, [UP], w=True), trigger=1, priority=0)])
    return doors


# ============================================================ 11. RIO SUBTERRANEO (PONTE)
RIO_ROWS = ['#' * 25, 'W' * 25, 'W' * 25] + ['.' * 25] * 4 + ['W' * 25] + ['~' * 25] * 4 + ['.' * 25] * 6 + ['#' * 25]


def build_rio():
    m = Map(25, 19, 4)
    W, H = m.w, m.h
    ceil = {(x, y) for x in range(W) for y in (0, 18)}
    m.auto(ceil, A4 + 1 * 48, 0)
    m.auto({(x, y) for x in range(W) for y in (1, 2)}, A4 + 9 * 48, 0, wall=True)
    banks = {(x, y) for x in range(W) for y in list(range(3, 7)) + list(range(12, 18))}
    m.auto(banks, A4 + 37 * 48, 0)
    m.auto({(x, 7) for x in range(W)}, A4 + 45 * 48, 0, wall=True)
    m.region(ceil)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for y in range(6, 13):
        b(11, y, D0 + 0); b(12, y, D0 + 1); b(13, y, D0 + 2)
    for (x, y, t) in [(4, 9, D0 + 3), (19, 10, D0 + 3), (7, 11, D0 + 3), (16, 8, D0 + 4), (22, 9, D0 + 4),
                      (2, 10, D0 + 4), (12, 2, 160), (12, 17, 28), (2, 4, 41), (21, 5, 41), (4, 14, 41),
                      (20, 15, 41), (8, 16, 41), (5, 13, 33), (19, 4, 33), (15, 16, 33), (3, 5, 33), (22, 13, 45),
                      (1, 16, 45), (23, 4, 120), (17, 14, 33)]:
        b(x, y, t)
    return m


def log_route(r):
    steps = ([RIGHT] * 10 + [rc(39)] + [RIGHT] * 4 + [rc(40)] + [RIGHT] * 10
             + [rc(39), rc(45, f'this.locate(0, {r})'), rc(40)])
    return B.route(steps, repeat=True, skippable=True, wait=False)


def events_rio(m):
    m.add_event('Ambiente', 0, 0, [page(tint([-30, -20, 0, 20], 0) + [cmd(214, [])], trigger=4, priority=0)])
    for r, spd in ((9, 6), (10, 5)):
        m.add_event('Tronco', 0, r, [page([], image=img('!$Tronco', 0, 2), priority=0, through=True, move_type=3,
                                          speed=spd, freq=5, walk=False, step=True, dir_fix=True,
                                          mroute=log_route(r))])
    for (x, y, idx) in [(6, 1, 0), (18, 1, 0), (10, 13, 2), (14, 13, 2), (10, 5, 2), (14, 5, 2)]:
        flame(m, x, y, idx, 2, prio=0 if y == 1 else 1)
    leona = m.add_event('Leona', 12, 10, [page([], priority=0, through=True),
                                          page([], image=img('$Leona', 0, 8), self_switch='A')])
    kura_e = m.add_event('Kura', 12, 7, [page([], priority=0, through=True),
                                         page([], image=img('$Kura', 0, 2), self_switch='A')])
    rau_e = m.add_event('Raulete', 13, 11, [page([], priority=0, through=True),
                                            page([], image=img('$Raulete', 0, 8), self_switch='A')])
    m.add_event('Chegada', 0, 18, [
        page([], priority=0),
        page(wait(15) + balloon(-1, 1)
             + leo('Que barulho é esse?!', i=1)
             + lea('Um rio subterrâneo... olha a força', 'dessa correnteza!', i=1)
             + leo('Tem uma ponte ali! Vamos atravessar,', 'rápido!')
             + self_sw(), trigger=3, priority=0, sw1=S_SENHA),
        page([], priority=0, self_switch='A'),
    ])
    for x in (11, 12, 13):
        m.add_event('Meio da ponte', x, 9, [page(call(CE_PONTE), trigger=1, priority=0),
                                            page([], priority=0, sw1=S_PONTE)])
    m.add_event('Escada', 12, 17, [page(leo('Voltar? Tá maluca?! Atravessa essa', 'ponte logo!', i=1))])
    return leona, kura_e, rau_e


def ce_ponte(LE, KU, RA):
    MR = M_RIO
    lst = (stop_bgm(1) + switch(S_PONTE)
           + se('Darkness1') + flash([150, 60, 200, 200], 30, w=False) + shake(6, 9, 30, w=False)
           + script(f"$gamePlayer.locate(13, 9); $gamePlayer.setDirection(8);\n"
                    f"const l = $gameMap.event({LE}); l.locate(12, 9); l.setDirection(8);\n"
                    + set_self_js(MR, [LE], True))
           + followers(False)
           + wait(40)
           + se('Darkness3') + anim(KU, 101, w=False)
           + script(set_self_js(MR, [KU], True))
           + wait(40)
           + balloon(-1, 1, w=False) + balloon(LE, 1)
           + bgm('Scene6', vol=75)
           + kura('Aonde pensam que vão, mocinhas?')
           + leo('Q-quem é você?!', i=1)
           + kura('Eu sou Kura.', 'A sombra da família Raulete.')
           + kura('Nenhum fio de cabelo sai deste', 'calabouço sem a minha permissão.')
           + lea('Leona... o que a gente faz?!', i=1)
           + leo('A gente luta, ora!', 'Ninguém encosta no MEU cabelo!')
           + [cmd(132, [audio('Battle4', 90)])]
           + battle(TROOP_KURA)
           + [cmd(314, [0, 0])]
           + stop_bgm(1) + wait(30)
           + pose(-1, 'cansado', repetir=True, segurar=True) + pose(LE, 'cansado', repetir=True, segurar=True)
           + narr('Leandra e Leona caem de joelhos, sem', 'forças para continuar.')
           + lea('Ele é forte demais...', i=1)
           + se('Laugh', vol=70)
           + rau('Hehehehe...')
           + balloon(-1, 1, w=False) + balloon(LE, 1)
           + se('Darkness3') + anim(RA, 101, w=False)
           + script(set_self_js(MR, [RA], True))
           + wait(30)
           + move(RA, [UP], w=True)
           + bgm('Scene6', vol=70)
           + move(-1, [rc(16)], w=False) + move(LE, [rc(16)], w=True)
           + rau('Muito bem, Kura. Muito bem.')
           + move(KU, [DOWN], w=True)
           + kura('Mestre Raulete.')
           + kura('A loirinha tem o cabelo que o senhor', 'encomendou.')
           + move(LE, [rc(19)], w=False) + move(-1, [rc(19)], w=True)
           + kura('Mas esta aqui...')
           + kura('Esta aqui tem potencial para se tornar', 'uma Umamusume.')
           + balloon(LE, 1)
           + leo('Uma... Umamusume?', i=1)
           + leo('...')
           + pose(LE, '')
           + leo('O que eu preciso fazer para virar', 'uma Umamusume?', i=2)
           + kura('Simples.')
           + kura('Você só precisa do sangue de uma loira.')
           + balloon(-1, 1)
           + move(LE, [rc(18)], w=False) + move(-1, [rc(17)], w=True)
           + pose(-1, '')
           + lea('L-Leona...? A gente ia fugir', 'juntas...', i=1)
           + leo('Desculpa, loirinha.', i=2)
           + leo('Mas eu nasci pra ser muito mais do', 'que uma prisioneira careca.', i=2)
           + stop_bgm(0)
           + pose(LE, 'facada', segurar=True) + pose(RA, 'soco', olhar=-1)
           + se('Slash1') + pose(-1, 'dor', segurar=True)
           + se('Wind7')
           + flash([255, 30, 30, 220], 30, w=False) + shake(8, 9, 20, w=False)
           + anim(-1, 91, w=False)
           + [cmd(322, [LEANDRA, '$Leandra_Careca', 0, 'Leandra', 3, ''])]
           + wait(40)
           + narr('Leona apunhala Leandra, enquanto Raulete', 'rouba os seus cabelos dourados!')
           + lea('Aaah...!', i=3)
           + pose(-1, 'queda', segurar=True) + pose(LE, '')
           + move(-1, [rc(37), rc(35), rc(14, 1, 0)], w=True)
           + se('Dive') + anim(-1, 82, w=False)
           + move(-1, [rc(29, 6)] + [RIGHT] * 7 + [rc(39)], w=True)
           + bgm('Scene2', vol=65)
           + narr('Leandra cai no rio e desaparece na', 'correnteza...')
           + wait(40)
           + move(LE, [rc(16)], w=True)
           + pose(LE, 'magia', repetir=True, segurar=True)
           + se('Magic7') + anim(LE, 117, w=False) + flash([255, 255, 255, 255], 40, w=False)
           + wait(40)
           + move(LE, [rc(41, '$Leona_Cavalo', 0)], w=True) + pose(LE, '')
           + se('Horse')
           + destaque('evento', rosto='Leona', indice=3, titulo='TRANSFORMAÇÃO', nome='Leona Umamusume',
                      texto='Orelhas, cauda... e muita velocidade.')
           + narr('O sangue loiro desperta algo dentro de', 'Leona...')
           + balloon(LE, 1)
           + leo('Orelhas... uma cauda...', 'Que poder é esse?!', i=3)
           + move(LE, [rc(14, 0, 0)], w=False)
           + leo('Eu me sinto tão... RÁPIDA!', i=3)
           + kura('Finalmente temos o material suficiente', 'para iniciarmos os nossos planos.')
           + move(RA, [rc(16)], w=True) + move(KU, [rc(16)], w=True)
           + se('Equip1') + anim(RA, 120, w=False)
           + move(RA, [rc(41, '$Raulete_Peruca', 0)], w=True)
           + narr('Raulete coloca o cabelo de Leandra na', 'própria cabeça careca...')
           + destaque('evento', rosto='Raulete', indice=1, titulo='CABELO ROUBADO', nome='Raulete de peruca loira',
                      texto='Os cabelos dourados da Leandra.')
           + se('Laugh')
           + pose(RA, 'riso', repetir=True, segurar=True)
           + rau('HAHAHAHAHA!', i=1)
           + rau('Finalmente encontramos alguém', 'compatível com o gene de cavala!', i=1)
           + rau('Agora, finalmente... poderemos farejar', 'a PERUCA DE OURO!', i=1)
           + destaque('evento', imagem='Peruca_Ouro', titulo='O ALVO DOS RAULETE', nome='Peruca de Ouro',
                      texto='Com o faro da Leona, a caçada começou.')
           + pose(RA, '')
           + switch(S_FIM2)
           + wait(30) + fadeout() + stop_bgm(3) + stop_bgs(3)
           + me('Mystery')
           + capitulo('FimCapitulo2')
           + [cmd(354, [])])
    return {'id': CE_PONTE, 'list': lst + [END], 'name': 'Cena da ponte', 'switchId': 1, 'trigger': 0}


# ============================================================ banco de dados
def mk_skill(tpl, sid, name, desc, icon, anim_id, formula, dtype, scope, hit, mp, msg, effects=(), stype=2):
    d = copy.deepcopy(tpl)
    d.update({'id': sid, 'name': name, 'description': desc, 'iconIndex': icon, 'animationId': anim_id,
              'damage': {'critical': False, 'elementId': 0, 'formula': formula, 'type': dtype, 'variance': 20},
              'effects': list(effects), 'hitType': hit, 'mpCost': mp, 'message1': msg, 'message2': '',
              'note': '', 'occasion': 1, 'scope': scope, 'stypeId': stype, 'tpGain': 5, 'messageType': 1})
    return d


def tpage(lst, turn=None, turn_end=False):
    return {'conditions': {'actorHp': 50, 'actorId': 1, 'actorValid': False, 'enemyHp': 50, 'enemyIndex': 0,
                           'enemyValid': False, 'switchId': 1, 'switchValid': False,
                           'turnA': turn or 0, 'turnB': 0, 'turnEnding': turn_end, 'turnValid': turn is not None},
            'list': lst + [END], 'span': 0}


def update_database():
    ts = load('Tilesets.json')
    ts[4]['tilesetNames'][7] = 'Calabouco_D'
    for n in (0, 1, 2):
        ts[4]['flags'][D0 + n] = 0x600
    for n in (3, 4):
        ts[4]['flags'][D0 + n] = 0x60f
    ts[6]['tilesetNames'][7] = 'Laboratorio_D'
    for n in range(7):
        ts[6]['flags'][D0 + n] = 0x60f
    ts[6]['flags'][D0 + 7] = 0x600
    save('Tilesets.json', ts)
    B.TILESETS = ts

    a = load('Actors.json')
    base = copy.deepcopy(a[2])
    common = dict(battlerName='', equips=[0, 0, 0, 0, 0], initialLevel=1, maxLevel=99, traits=[], note='',
                  characterIndex=0, faceIndex=0)
    a[2] = dict(base, **common, id=2, name='Leandra', nickname='A Loirinha', classId=CLS_LEANDRA,
                characterName='$Leandra', faceName='Leandra',
                profile='Criança de Diademonius com longos\ncabelos dourados.')
    a[3] = dict(base, **common, id=3, name='Leona', nickname='A Arrogante', classId=CLS_LEONA,
                characterName='$Leona', faceName='Leona',
                profile='Presa no calabouço dos Raulete.\nSe acha melhor que todo mundo.')
    a[4] = dict(base, **common, id=4, name='', nickname='', classId=1, characterName='', faceName='Terminal', profile='')
    save('Actors.json', a)

    c = load('Classes.json')
    while len(c) <= CLS_LEONA:
        c.append(None)
    tpl = c[1]

    def mk_class(cid, name, p0, g, skills):
        params = [[int(p0[i] + g[i] * max(lv - 1, 0)) for lv in range(100)] for i in range(8)]
        traits = [t for t in tpl['traits'] if t['code'] in (22, 23)] + [{'code': 41, 'dataId': 2, 'value': 1}]
        return {'id': cid, 'expParams': [30, 20, 30, 30], 'traits': traits,
                'learnings': [{'level': 1, 'note': '', 'skillId': s} for s in skills],
                'name': name, 'note': '', 'params': params}
    c[CLS_LEANDRA] = mk_class(CLS_LEANDRA, 'Pedinte', [260, 30, 18, 14, 12, 12, 22, 20], [25, 3, 2, 2, 2, 2, 2, 2],
                              [SK0, SK0 + 1, SK0 + 2])
    c[CLS_LEONA] = mk_class(CLS_LEONA, 'Herdeira Mimada', [280, 40, 22, 16, 18, 16, 18, 14], [26, 4, 3, 2, 3, 2, 2, 1],
                            [SK0 + 3, SK0 + 4, SK0 + 5])
    save('Classes.json', c)

    s = load('Skills.json')
    while len(s) <= SK0 + 8:
        s.append(None)
    t = s[1]
    s[SK0 + 0] = mk_skill(t, SK0 + 0, 'Chute na Canela', 'Um chute certeiro na canela do inimigo.', 77, 39,
                          'a.atk * 2 + 10 - b.def', 1, 1, 1, 0, '%1 dá um chute na canela!')
    s[SK0 + 1] = mk_skill(t, SK0 + 1, 'Pedra do Córrego', 'Joga uma pedra tirada do córrego poluído.', 70, 86,
                          'a.atk * 3 - b.def', 1, 1, 1, 3, '%1 joga uma pedra do córrego!')
    s[SK0 + 2] = mk_skill(t, SK0 + 2, 'Olhar Pidão', 'Faz cara de pidona. Às vezes funciona.', 84, 54,
                          '0', 0, 1, 0, 2, '%1 faz cara de pidona!', [{'code': 32, 'dataId': 2, 'value1': 3, 'value2': 0}])
    s[SK0 + 3] = mk_skill(t, SK0 + 3, 'Chicote de Cabelo', 'Gira os cabelos negros como um chicote.', 76, 7,
                          'a.atk * 3 - b.def', 1, 1, 1, 0, '%1 chicoteia com o cabelo!')
    s[SK0 + 4] = mk_skill(t, SK0 + 4, 'Desdém', 'Um olhar tão arrogante que enfraquece a defesa.', 85, 55,
                          '0', 0, 1, 0, 3, '%1 olha com desdém!', [{'code': 32, 'dataId': 3, 'value1': 3, 'value2': 0}])
    s[SK0 + 5] = mk_skill(t, SK0 + 5, 'Grito Mimado', 'Um grito tão estridente que machuca.', 79, 34,
                          'a.mat * 2 + 10 - b.mdf', 1, 2, 2, 5, '%1 dá um grito mimado!')
    s[SK0 + 6] = mk_skill(t, SK0 + 6, 'Garra das Sombras', '', 0, 17, '25 + a.atk - b.def', 1, 1, 1, 0,
                          '%1 ataca com garras de sombra!')
    s[SK0 + 7] = mk_skill(t, SK0 + 7, 'Riso Sombrio', '', 0, 0, '0', 0, 11, 0, 0, '%1 dá uma risada sinistra!',
                          [{'code': 31, 'dataId': 2, 'value1': 2, 'value2': 0}])
    s[SK0 + 8] = mk_skill(t, SK0 + 8, 'Chicote de Sombras', '', 0, 101, '15 + a.mat / 2 - b.mdf / 2', 1, 2, 2, 0,
                          '%1 lança chicotes de sombra!')
    save('Skills.json', s)

    e = load('Enemies.json')
    while len(e) <= EN_KURA:
        e.append(None)
    act = lambda sid, r: {'conditionParam1': 0, 'conditionParam2': 0, 'conditionType': 0, 'rating': r, 'skillId': sid}
    e[EN_KURA] = {'id': EN_KURA, 'actions': [act(SK0 + 6, 5), act(SK0 + 7, 4), act(SK0 + 8, 4)],
                  'battlerHue': 0, 'battlerName': 'Kura',
                  'dropItems': [{'dataId': 1, 'denominator': 1, 'kind': 0} for _ in range(3)],
                  'exp': 0, 'gold': 0, 'name': 'Kura', 'note': '',
                  'params': [99999, 999, 30, 30, 30, 30, 30, 10],
                  'traits': [{'code': 22, 'dataId': 0, 'value': 0.95}, {'code': 22, 'dataId': 1, 'value': 0.05},
                             {'code': 31, 'dataId': 1, 'value': 0}]}
    save('Enemies.json', e)

    tr = load('Troops.json')
    while len(tr) <= TROOP_KURA:
        tr.append(None)
    golpe = (kura('Chega de brincadeira.')
             + [cmd(337, [0, 103, False])] + wait(50)
             + se('Darkness5') + flash([120, 0, 170, 255], 40, w=False) + shake(9, 9, 40, w=False)
             + narr('Kura desfere um único golpe de sombra!')
             + [cmd(311, [0, 0, 1, 0, 9999, True])])
    tr[TROOP_KURA] = {'id': TROOP_KURA, 'members': [{'enemyId': EN_KURA, 'x': 408, 'y': 436, 'hidden': False}],
                      'name': 'Kura (ponte)', 'pages': [
                          tpage(kura('Vamos ver do que vocês são capazes,', 'mocinhas.')
                                + leo('Leandra, vai! Bate nele!', i=1)
                                + lea('Mas eu nunca briguei com ninguém!', i=1), turn=0),
                          tpage(leo('Ele nem sente os nossos golpes!', i=1), turn=2),
                          tpage(kura('Hehehe... é só isso?'), turn=3),
                          tpage(golpe, turn=4, turn_end=True),
                      ]}
    save('Troops.json', tr)

    it = load('Items.json')
    while len(it) <= IT_GRAMPO:
        it.append(None)
    g = copy.deepcopy(it[7])
    g.update({'id': IT_GRAMPO, 'animationId': 0, 'consumable': False, 'effects': [], 'iconIndex': 195, 'itypeId': 2,
              'name': 'Grampo de cabelo', 'occasion': 3, 'price': 0, 'scope': 0,
              'description': 'Um grampo enferrujado, achado entre os ossos.\nDá pra abrir fechaduras.'})
    it[IT_GRAMPO] = g
    save('Items.json', it)

    sysd = load('System.json')
    names = {S_INICIO: 'Cap.2: introdução vista', S_ESMOLAS: 'Cap.2: 5 esmolas', S_VENDIDA: 'Cap.2: Leandra vendida',
             S_LEONA: 'Cap.2: Leona no grupo', S_GRAMPO: 'Cap.2: achou o grampo', S_CELA: 'Cap.2: cela aberta',
             S_PC: 'Cap.2: computador ligado', S_SENHA: 'Cap.2: senha certa', S_PONTE: 'Cap.2: cena da ponte',
             S_FIM2: 'Fim do Capítulo 2'}
    for k, v in names.items():
        sysd['switches'][k] = v
    sysd['variables'][V_ESMOLAS] = 'Esmolas'
    sysd['terms']['messages']['defeat'] = '%1 foi derrotada.'
    save('System.json', sysd)


def main():
    template = load('Map001.json')
    update_database()
    dia = build_diade(); events_diade(dia)
    casa = build_casa(); events_casa(casa)
    cela = build_cela(); events_cela(cela)
    lab = build_lab(); events_lab(lab)
    rio = build_rio(); LE, KU, RA = events_rio(rio)

    # ---- verificacoes de caminho
    r = dia.reach((4, 5))
    for name, (x, y) in {'Joaquim': (8, 10), 'Perpetua': (14, 17), 'Ze': (21, 11), 'Bento': (22, 5),
                         'Sabino': (28, 5), 'Nena': (28, 12), 'Capivara': (23, 19)}.items():
        assert near_reachable(r, x, y), ('diademonius', name)
    assert (4, 4) in r or dia.passable(4, 4), 'porta da Leandra'
    c = casa.reach((6, 8))
    assert (7, 6) in c and (6, 9) in c and (4, 5) in c, 'casa'
    ce_ = cela.reach((4, 4))
    assert (6, 3) in ce_ or (7, 4) in ce_, 'esqueleto'
    assert (4, 6) in ce_ and (4, 7) in ce_ and (16, 3) in ce_ and cela.passable(16, 2), 'cela'
    lb = lab.reach((12, 15))
    for cell in [(12, 13), (3, 4), (8, 4), (16, 4), (21, 4), (12, 3)]:
        assert cell in lb, ('lab', cell)
    assert lab.passable(12, 2) and lab.passable(12, 16), 'escadas do lab'
    rr = rio.reach((12, 16))
    assert all((x, 9) in rr for x in (11, 12, 13)), 'ponte'
    assert (5, 9) not in rr and not rio.passable(5, 9), 'rio deveria bloquear'

    maps = [
        (M_DIADE, dia, 'Diademonius', 'Town6', 'Wind2', ''),
        (M_CASA, casa, 'Casa da Leandra', '', '', ''),
        (M_CELA, cela, 'Calabouço', 'Dungeon2', 'Drips', ''),
        (M_LAB, lab, 'Laboratório das Perucas', 'Dungeon4', '', ''),
        (M_RIO, rio, 'Rio Subterrâneo', '', 'River', ''),
    ]
    for mid, m, disp, bgmn, bgsn, note in maps:
        j = map_json(template, m, disp, bgmn, bgsn, note, bgm_vol=65, bgs_vol=55)
        if mid == M_RIO:
            j.update({'parallaxName': '!Correnteza', 'parallaxLoopX': True, 'parallaxLoopY': False,
                      'parallaxSx': -12, 'parallaxSy': 0, 'parallaxShow': True,
                      'specifyBattleback': True, 'battleback1Name': 'RockCave', 'battleback2Name': 'RockCave'})
        else:
            j.update({'parallaxLoopX': False, 'parallaxLoopY': False, 'parallaxSx': 0, 'parallaxSy': 0})
        save(f'Map{mid:03d}.json', j)

    mi = load('MapInfos.json')
    while len(mi) <= M_RIO:
        mi.append(None)
    info = [(M_DIADE, 'Cap.2 - Diademonius', 0), (M_CASA, 'Casa da Leandra', M_DIADE),
            (M_CELA, 'Calabouço - Cela', 0), (M_LAB, 'Calabouço - Laboratório', M_CELA),
            (M_RIO, 'Calabouço - Rio Subterrâneo', M_CELA)]
    for o, (mid, name, parent) in enumerate(info, 7):
        mi[mid] = {'id': mid, 'expanded': True, 'name': name, 'order': o, 'parentId': parent, 'scrollX': 0, 'scrollY': 0}
    save('MapInfos.json', mi)

    ce = load('CommonEvents.json')
    while len(ce) <= CE_PONTE:
        ce.append(None)
    ce[CE_ESMOLA] = ce_esmola()
    ce[CE_PONTE] = ce_ponte(LE, KU, RA)
    save('CommonEvents.json', ce)

    pl = open(f'{PROJ}/js/plugins.js', encoding='utf-8').read()
    for name, desc in (('Capitulos', 'Adiciona \\"Capítulos\\" na tela de título.'),
                       ('SenhaTeclado', 'Permite digitar no teclado na tela de entrada de nome.')):
        if f'"{name}"' not in pl:
            pl = pl.replace('\n];', f',\n{{"name":"{name}","status":true,"description":"{desc}","parameters":{{}}}}\n];')
    open(f'{PROJ}/js/plugins.js', 'w', encoding='utf-8', newline='\n').write(pl)
    print('ok: eventos', {disp: len(m.events) - 1 for _, m, disp, *_ in maps})


if __name__ == '__main__':
    main()
