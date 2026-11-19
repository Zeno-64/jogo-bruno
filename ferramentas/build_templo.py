# Capitulo 4: Templo da Xavasca Leprosa (3 andares, enigmas, chaves, portais, porta selada),
# a cena da Vera Verao, o roubo da peruca, a corrida e o final do capitulo.
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ch4_comum import *
import sokoban

E_FAIXA_H, E_FAIXA_V, E_CHEGADA = E0 + 0, E0 + 1, E0 + 2
E_PODIO = {1: E0 + 3, 2: E0 + 4, 3: E0 + 5}
E_FERRADURA, E_PLACA_PERUCA, E_GLIFO, E_FAIXA_OURO = E0 + 6, E0 + 7, E0 + 8, E0 + 9
E_SOL = (E0 + 10, E0 + 11, E0 + 18, E0 + 19)
E_SERPENTE, E_MURAL_UMA, E_MURAL_PERUCA, E_ARCO_IRIS, E_ESCURO, E_SERPENTE_E = E0 + 12, E0 + 13, E0 + 14, E0 + 15, E0 + 16, E0 + 17
PAREDE = {'arenito': (18, 26), 'musgo': (20, 28), 'ouro': (35, 43)}
CHAO_A5 = {'piso': 29, 'decor': 25, 'decor_b': 26, 'terra': 36, 'ouro_sol': 118, 'ouro_lua': 119, 'pedra': 32}
TAPETE = A2 + 19 * 48
CERCA = A2 + 22 * 48
HEXAGRAMA = [[80, 81, 82], [88, 89, 90], [96, 97, 98]]
HEXAGRAMA_ACESO = [[83, 84, 85], [91, 92, 93], [99, 100, 101]]


def registrar_tileset_templo():
    ts = load('Tilesets.json')
    t = ts[4]
    t['tilesetNames'][8] = 'Templo_E'
    for n in range(0, 8):
        t['flags'][E0 + n] = 0x600
    t['flags'][E_ARCO_IRIS] = 0x600
    for n in (E_GLIFO, E_FAIXA_OURO, E_SERPENTE, E_MURAL_UMA, E_MURAL_PERUCA, E_ESCURO, E_SERPENTE_E) + E_SOL:
        t['flags'][n] = 0x60f
    save('Tilesets.json', ts)
    B.TILESETS[:] = ts


def sala(w, h, parede, chao_fn, aberturas=(), divisoria=None):
    """Sala com teto ('#') na borda, parede de 2 linhas no alto e chao. 'divisoria' = linha de teto+parede interna."""
    rows = []
    for y in range(h):
        linha = ''
        for x in range(w):
            if (x, y) in aberturas:
                linha += '.'
            elif x in (0, w - 1) or y in (0, h - 1):
                linha += '#'
            elif y in (1, 2):
                linha += 'W'
            elif divisoria and y == divisoria:
                linha += '#'
            elif divisoria and y in (divisoria + 1, divisoria + 2):
                linha += 'W'
            else:
                linha += '.'
        rows.append(linha)
    m = Map(w, h, 4)
    top, side = PAREDE[parede]
    paint(m, rows, top, side, chao_fn)
    return m, rows


def pilar(m, x, y):
    """Pilar dourado do templo (3 tiles de altura; a base em (x, y))."""
    m.put(x, y - 2, 3, C0 + 2); m.put(x, y - 1, 3, C0 + 10); m.put(x, y, 2, C0 + 18)
    m.region([(x, y), (x, y - 1), (x, y - 2)])


def braseiro(m, x, y):
    m.add_event('Braseiro', x, y, [page([], image=img('!Templo1', 6, 4), step=True, dir_fix=True, walk=False)])


def porta_trancada(m, x, y, chave, sw, nome_chave, destino, msg_fechada, antes=()):
    abrir = (se('Key') + narr(f'Clec! A {nome_chave} serviu direitinho!') + item(chave, -1)
             + move(0, [rc(35), rc(17), rc(15, 8), rc(18), rc(15, 8), rc(19)], w=True)
             + se('Open5') + switch(sw))
    fechada = se('Buzzer1', vol=60) + narr(*msg_fechada)
    m.add_event('Porta trancada', x, y, [
        page(tem_item(chave, abrir, fechada), image=img('!Templo2', 0, 2), trigger=1, dir_fix=False, walk=False),
        page(se('Door1') + list(antes) + transfer(*destino), image=img('!Templo2', 0, 8), trigger=1, dir_fix=True, walk=False, sw1=sw),
    ])


def portal(m, x, y, andar):
    ativar = (se('Teleport') + flash([150, 230, 255, 160], 20) + switch(S_PORTAL[andar - 1])
              + destaque('evento', titulo='PORTAL ATIVADO', nome=f'Portal do {andar}º Andar',
                         texto='Fique em cima dele e aperte a tecla de ação para viajar.'))
    if andar == 3:
        ativar += narr('Agora o portal também leva de volta à', 'entrada da Floresta de Mauara (e vice-versa)!')
    m.add_event(f'Portal {andar}', x, y, [
        page(ativar, image=img('!Templo2', 5, 2), trigger=1, priority=0, dir_fix=True, walk=False),
        page(var_set(V_PORTAL_AQUI, andar) + call(CE_PORTAL), image=img('!Templo2', 5, 4), priority=0, step=True,
             dir_fix=True, walk=False, sw1=S_PORTAL[andar - 1]),
    ])


def ambiente(m, tom, extra=()):
    m.add_event('Ambiente', 0, 0, [page(tint(tom, 0) + list(extra) + [cmd(214, [])], trigger=4, priority=0)])


# ================================================================ 18. 1o ANDAR: GALERIA DAS PERUCAS
RELEVO = (112, 113, 120, 121)          # piso de pedra entalhada (2x2)
RELEVO_RUINA = (114, 115, 122, 123)


def relevo(x, y, ruina=False):
    return A5 + (RELEVO_RUINA if ruina else RELEVO)[(y % 2) * 2 + (x % 2)]


def construir_t1():
    piso = lambda x, y, ch: relevo(x, y)
    m, rows = sala(25, 19, 'arenito', piso, aberturas={(12, 18)})
    m.auto(rect(11, 7, 13, 17), TAPETE, 1)
    for x in (4, 6, 18, 20):
        m.put(x, 1, 2, E_GLIFO); m.put(x, 2, 2, E_MURAL_PERUCA)
    for x0 in (9, 14):
        for k, (dx, y) in enumerate([(0, 1), (1, 1), (0, 2), (1, 2)]):
            m.put(x0 + dx, y, 2, E_SOL[k])
    for x in (2, 22):
        pilar(m, x, 5); pilar(m, x, 16)
    m.put(12, 8, 2, 177)
    for x in (6, 10, 14, 18):
        m.put(x, 7, 2, E_PLACA_PERUCA)
    return m


INSCRICAO = [
    narr('GALERIA DAS PERUCAS SAGRADAS', 'Vista cada Diva com a peruca certa,', 'da esquerda para a direita:'),
    narr('1. A Ruiva tem medo de altura:', 'nunca fica nas pontas.'),
    narr('2. A Loira fica sempre logo à direita', 'da Ruiva. São melhores amigas.'),
    narr('3. A Azul é tímida: gosta de ficar', 'num canto.'),
    narr('4. A Preta e a Ruiva brigaram por causa', 'de um secador. Nunca ficam lado a lado.'),
]


def eventos_t1(m):
    ambiente(m, [-10, -14, -20, 10])
    m.add_event('Chegada', 0, 18, [
        page(wait(10) + narr('1º Andar do Templo: a Galeria das Perucas', 'Sagradas.')
             + kuma('Uau, quantas perucas! Parece o camarim', 'de uma diva.', i=2)
             + bar('Quatro bustos carecas... e quatro perucas.', 'Isso tem cara de enigma.')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    for (x, y) in [(5, 4), (19, 4), (5, 14), (19, 14)]:
        braseiro(m, x, y)
    # bustos: paginas pela variavel (0 careca, 1 loira, 2 ruiva, 3 azul, 4 preta)
    for i, x in enumerate((6, 10, 14, 18)):
        v = V_BUSTOS[i]
        acao = (script(_JS_BUSTO.replace('VB', str(v)))
                + var_eq(V_RAND, 0, narr('Um busto careca, esperando uma peruca.'))
                + var_eq(V_RAND, 1, se('Equip1') + narr('Você coloca a peruca \\V[21] no busto.'))
                + var_eq(V_RAND, 2, se('Equip2') + narr('Você pega a peruca \\V[21] de volta.'))
                + var_eq(V_RAND, 3, se('Equip1') + narr('Você troca as perucas. Agora está', 'segurando a \\V[21].'))
                + call_checagem())
        paginas = [page(acao, image=img('!Templo1', 0, 2))]
        for valor, (idx, d) in enumerate([(0, 4), (0, 6), (0, 8), (1, 2)], 1):
            paginas.append(page(acao, image=img('!Templo1', idx, d), var=(v, valor)))
        m.add_event(f'Busto {i + 1}', x, 6, paginas)
    # suportes com as perucas
    for (x, y, cor) in [(3, 9, 1), (3, 12, 3), (21, 9, 2), (21, 12, 4)]:
        nome = PERUCA_COR[cor]
        pegar = (if_([1, V_MAO, 0, 0, 0],
                     se('Equip2') + var_set(V_MAO, cor) + self_sw('A') + narr(f'Você pega a Peruca {nome}.'),
                     narr('Você já está segurando uma peruca.')))
        devolver = (if_([1, V_MAO, 0, cor, 0],
                        se('Equip1') + var_set(V_MAO, 0) + self_sw('A', False) + narr(f'Você devolve a Peruca {nome}.'),
                        narr('Um suporte vazio.')))
        d = {1: 2, 2: 4, 3: 6, 4: 8}[cor]
        m.add_event(f'Peruca {nome}', x, y, [
            page(pegar, image=img('!Templo1', 2, d)),
            page(devolver, image=img('!Templo1', 3, 2), self_switch='A'),
        ])
    m.add_event('Inscrição', 12, 8, [page(sum(INSCRICAO, []))])
    m.add_event('Baú da chave', 12, 5, [
        page([], priority=0, through=True),
        page(se('Chest1') + self_sw() + item(IT_JADE, 1)
             + destaque('item', imagem='Item_Chave_Jade', nome='Chave de Jade', texto='Abre a porta para o 2º andar.'),
             image=img('!Chest', 2, 2, 0), sw1=S_T1_OK),
        page([], image=img('!Chest', 2, 8, 0), sw1=S_T1_OK, self_switch='A'),
    ])
    porta_trancada(m, *T1_PORTA, IT_JADE, S_PORTA[0], 'Chave de Jade', (M_T2, T2_CHEGADA[0], T2_CHEGADA[1], 8, 0),
                   ('Trancada. A fechadura tem a forma de', 'uma peruca de jade.'))
    portal(m, *PORTAIS[1][1:], 1)
    m.add_event('Saída', 12, 18, [page(transfer(M_CORACAO, CORACAO_PORTA[0], CORACAO_PORTA[1] + 1, 2), trigger=1, priority=0)])


_JS_BUSTO = """const mao = $gameVariables.value(7); const b = $gameVariables.value(VB);
const nomes = ['', 'Loira', 'Ruiva', 'Azul', 'Preta'];
let acao = 0;
if (mao && !b) acao = 1; else if (!mao && b) acao = 2; else if (mao && b) acao = 3;
$gameVariables.setValue(21, nomes[acao === 2 ? b : acao === 3 ? b : mao]);
$gameVariables.setValue(7, b); $gameVariables.setValue(VB, mao);
$gameVariables.setValue(5, acao);"""


def call_checagem():
    valores = ','.join(f'$gameVariables.value({v})' for v in V_BUSTOS)
    cond_cheio = [12, ' && '.join(f'$gameVariables.value({v}) > 0' for v in V_BUSTOS)]
    cond_certo = [12, f'[{valores}].join() === "{",".join(map(str, SOLUCAO_BUSTOS))}"']
    resolvido = (se('Saint7') + flash([255, 240, 180, 200], 30) + shake(3, 6, 20)
                 + narr('As quatro Divas brilham!', 'Ouve-se um "AHHH" celestial...')
                 + se('Chest2') + narr('Um baú surge no meio da galeria!')
                 + switch(S_T1_OK)
                 + kuma('Que combinação perfeita!', 'Isso sim é glamour!', i=2))
    errado = (narr('As Divas fazem cara de nojo:', '"Que combinação é essa, querida?!"')
              + bar('Hmm... vou ler a inscrição de novo.'))
    return if_([0, S_T1_OK, 1], if_(cond_cheio, if_(cond_certo, resolvido, errado)))


# ================================================================ 19. 2o ANDAR: PISTA SAGRADA DAS UMAMUSUMES
SALA_UMA = [
    '###############',
    '#....b.p.d....#',
    '#.##.......##.#',
    '#....#.#.#....#',
    '#.#.P..#..B.#.#',
    '#...#.....#...#',
    '#.#...#D#...#.#',
    '#...#.....#...#',
    '#.....#@#.....#',
    '#######.#######',
]
SALA_X0, SALA_Y0 = 6, 4
EMPURROES_MIN = 25      # resultado do sokoban.resolver para esta sala


def dados_sala_uma():
    livres, est, alvos, jog = sokoban.de_ascii(SALA_UMA, SALA_X0, SALA_Y0)
    paredes = set()
    for y, l in enumerate(SALA_UMA):
        for x, ch in enumerate(l):
            if ch == '#':
                paredes.add((SALA_X0 + x, SALA_Y0 + y))
    return livres, est, alvos, jog, paredes


def construir_t2():
    def piso(x, y, ch):
        dentro = SALA_X0 <= x < SALA_X0 + 15 and SALA_Y0 <= y < SALA_Y0 + 10
        return A5 + CHAO_A5['terra'] if dentro else relevo(x, y, ruina=True)
    m, rows = sala(27, 21, 'musgo', piso, aberturas={(13, 20)})
    livres, est, alvos, jog, paredes = dados_sala_uma()
    borda = {(x, y) for (x, y) in paredes if x in (SALA_X0, SALA_X0 + 14) or y in (SALA_Y0, SALA_Y0 + 9)}
    m.auto(borda, CERCA, 1)
    for (x, y) in paredes - borda:
        m.put(x, y, 2, 41)
    m.region(paredes)
    for k, cor in {'P': 1, 'B': 2, 'D': 3}.items():
        x, y = alvos[k]
        m.put(x, y, 1, E_PODIO[cor])
    for x in (3, 7, 19, 23):
        m.put(x, 1, 2, E_GLIFO); m.put(x, 2, 2, E_MURAL_UMA)
    for x0 in (10, 15):
        for k, (dx, y) in enumerate([(0, 1), (1, 1), (0, 2), (1, 2)]):
            m.put(x0 + dx, y, 2, E_SOL[k])
    for y in range(15, 20):
        m.put(13, y, 1, E_FAIXA_V)
    m.put(11, 14, 2, 178)
    for x in (2, 24):
        pilar(m, x, 6); pilar(m, x, 12)
    return m


def eventos_t2(m):
    livres, est, alvos, jog, paredes = dados_sala_uma()
    ambiente(m, [-20, -6, -14, 10], followers(False))
    m.add_event('Chegada', 0, 20, [
        page(wait(10) + narr('2º Andar: a Pista Sagrada das Umamusumes.')
             + kuma('Uma pista de corrida! E estátuas de', 'Umamusumes!', i=2)
             + kuma('Vou ficar aqui torcendo. Se eu entrar, eu', 'saio correndo e não volto mais.', i=0)
             + bar('Fica aí, então. Eu resolvo.')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    m.add_event('Kevinho', 15, 19, [page(sorteio([kuma('Empurra as estátuas pro pódio certo!', i=2),
                                                  kuma('Se travar, puxa a alavanca que volta tudo.'),
                                                  kuma('Lê a placa da corrida! A ordem importa!', i=1)]),
                                         image=img('$Kevinho_Uma', 0, 8))])
    ids = {}
    nomes = {'D': ('Dourada', 0), 'P': ('Prata', 1), 'B': ('Bronze', 2)}
    for k, (nome, d_idx) in nomes.items():
        x, y = est[k]
        d = {0: 2, 1: 4, 2: 6}[d_idx]
        ids[k] = m.add_event(f'Estátua {nome}', x, y, [
            page(script(f'Templo.empurrar(this._eventId, {S_T2_OK});'), image=img('!Templo1', 4, d), dir_fix=True, walk=False),
            page(narr(f'A Umamusume de {nome} brilha no pódio.'), image=img('!Templo1', 4, d), dir_fix=True, walk=False, sw1=S_T2_OK),
        ])
    # posicoes salvas, alvos e solucao (para o plugin Templo)
    alvo_js = ', '.join(f'[{ids[k]}, {alvos[k][0]}, {alvos[k][1]}, {est[k][0]}, {est[k][1]}]' for k in 'DPB')
    m.add_event('Regras da pista', 0, 1, [page(script(f'Templo.definirPista({M_T2}, [{alvo_js}], {S_T2_OK});')
                                               + [cmd(214, [])], trigger=4, priority=0)])
    m.add_event('Alavanca', 20, 15, [
        page(se('Switch1') + script(f'Templo.reiniciarPista({M_T2});')
             + narr('Clunc! As estátuas voltam para a largada.'), image=img('!Templo1', 5, 2), dir_fix=True, walk=False),
        page(narr('A alavanca está travada. A corrida já', 'acabou!'), image=img('!Templo1', 5, 4), dir_fix=True, walk=False, sw1=S_T2_OK),
    ])
    m.add_event('Placa da corrida', 11, 14, [page(
        narr('RESULTADO DA GRANDE CORRIDA ANCESTRAL', '(coloque cada Umamusume no seu lugar do pódio)')
        + narr('A Bronze largou na frente, mas foi passada', 'pela Prata na curva.')
        + narr('Na reta final, a Dourada passou as duas...', '...e tropeçou na própria crina.')
        + narr('Quem riu por último foi a Prata.'))])
    m.add_event('Baú da chave', 13, 16, [
        page([], priority=0, through=True),
        page(se('Chest1') + self_sw() + item(IT_FERRADURA, 1)
             + destaque('item', imagem='Item_Chave_Ferradura', nome='Chave de Ferradura', texto='Abre a porta para o 3º andar.'),
             image=img('!Chest', 2, 2, 0), sw1=S_T2_OK),
        page([], image=img('!Chest', 2, 8, 0), sw1=S_T2_OK, self_switch='A'),
    ])
    porta_trancada(m, *T2_PORTA, IT_FERRADURA, S_PORTA[1], 'Chave de Ferradura', (M_T3, T3_CHEGADA[0], T3_CHEGADA[1], 8, 0),
                   ('Trancada. A fechadura tem a forma de', 'uma ferradura.'), antes=followers(True))
    portal(m, *PORTAIS[2][1:], 2)
    m.add_event('Descer', 13, 20, [page(followers(True) + transfer(M_T1, T1_PORTA[0], T1_PORTA[1] + 1, 2), trigger=1, priority=0)])
    return ids


# ================================================================ 20. 3o ANDAR: SANTUARIO
def construir_t3():
    def piso(x, y, ch):
        if y <= 8:
            return A5 + (CHAO_A5['ouro_sol'] if (x + y) % 2 == 0 else CHAO_A5['ouro_lua'])
        return A5 + CHAO_A5['decor']
    m, rows = sala(27, 26, 'arenito', piso, aberturas={(13, 25)}, divisoria=9)
    for dy in range(3):
        for dx in range(3):
            m.put(12 + dx, 4 + dy, 1, C0 + HEXAGRAMA[dy][dx])
    for x in (3, 8, 18, 23):
        m.put(x, 1, 2, E_GLIFO); m.put(x, 2, 2, E_MURAL_PERUCA)
    for k, (x, y) in enumerate([(12, 1), (13, 1), (12, 2), (13, 2)]):
        m.put(x, y, 2, E_SOL[k])
    for x in (4, 22):
        pilar(m, x, 5); pilar(m, x, 8)
    for x in (3, 9, 17, 23):
        m.put(x, 10, 2, E_MURAL_UMA); m.put(x, 11, 2, E_GLIFO)
    m.auto(rect(12, 12, 14, 24), TAPETE, 1)
    for x in (2, 24):
        pilar(m, x, 15); pilar(m, x, 22)
    for (x, y) in rect(11, 13, 15, 15):
        m.put(x, y, 1, E_ARCO_IRIS)
    return m


PERGUNTAS = [
    ('Qual era a senha do computador do', 'laboratório do Raulete?', ['HAIR', 'PERUCA', 'CABELO', '1234'], 0),
    ('Quem virou Umamusume na ponte do rio', 'subterrâneo?', ['Leandra', 'Leona', 'Kura', 'Gusrola'], 1),
    ('Com qual gene o Raulete queria farejar', 'a Peruca de Ouro?', ['Gene de sapo', 'Gene careca', 'Gene de cavala', 'Gene de pavão'], 2),
    ('O que acontece quando a última pétala da', 'flor da Baratelli cair?', ['Ela vira sapo', 'Ela vira Umamusume', 'Ela ganha uma peruca', 'Ela fica calva'], 3),
]


def quiz():
    out = (se('Stare') + esfinge('Eu sou a Esfinge Careca.', 'Guardiã do Santuário da Peruca.')
           + esfinge('Responda às minhas quatro perguntas sobre', 'perucas e Umamusumes... ou sofra!'))
    errou = (se('Buzzer2') + flash([255, 60, 60, 160], 20)
             + esfinge('ERRADO!')
             + se('Fall') + pose(-1, 'dor', espera=10)
             + narr('Uma peruca de palha velha cai do teto', 'bem na cabeça de Baratelli!')
             + bar('Que coceira! Isso aqui tem até piolho', 'de museu!')
             + esfinge('Volte quando souber a história.', 'Começaremos de novo.')
             + var_set(V_ESFINGE, 99))
    for k, (l1, l2, ops, certa) in enumerate(PERGUNTAS):
        corpo = esfinge(f'Pergunta {k + 1}: {l1}', l2)
        ramos = []
        for i, op in enumerate(ops):
            ramos.append((op, (se('Chime2') + esfinge('Correto.') + var_set(V_ESFINGE, k + 1)) if i == certa else errou))
        corpo += choices(ramos)
        out += if_([1, V_ESFINGE, 0, k, 0], corpo)
    acertou = (se('Saint7') + flash([255, 255, 220, 200], 30)
               + esfinge('Muito bem... você conhece a história da', 'peruca como ninguém.')
               + narr('A Esfinge sorri... e a careca dela brilha', 'como um sol!')
               + se('Chest2') + narr('Um baú surge diante da Esfinge!')
               + switch(S_T3_OK))
    out += if_([1, V_ESFINGE, 0, 4, 0], acertou)
    out += if_([1, V_ESFINGE, 0, 99, 0], var_set(V_ESFINGE, 0))
    return out


def eventos_t3(m):
    ambiente(m, [-6, -14, -20, 10])
    m.add_event('Chegada', 0, 25, [
        page(wait(10) + narr('3º Andar: o Santuário.', 'Ao norte, uma porta com as cores do arco-íris.')
             + kuma('E aquela cabeçona careca no meio da sala?', i=3)
             + bar('Careca e de pedra. Já gostei dela.')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    for (x, y) in [(10, 13), (16, 13), (6, 19), (20, 19)]:
        braseiro(m, x, y)
    m.add_event('Esfinge Careca', 13, 16, [
        page(var_set(V_ESFINGE, 0) + quiz(), image=img('!Templo1', 7, 2), dir_fix=True, walk=False),
        page(esfinge('A Peruca te espera além da porta', 'do arco-íris.'), image=img('!Templo1', 7, 4), dir_fix=True,
             walk=False, sw1=S_T3_OK),
    ])
    m.add_event('Baú da chave', 13, 18, [
        page([], priority=0, through=True),
        page(se('Chest1') + self_sw() + item(IT_ARCOIRIS, 1)
             + destaque('item', imagem='Item_Chave_ArcoIris', nome='Chave Arco-Íris', texto='Abre a porta do santuário.'),
             image=img('!Chest', 2, 2, 0), sw1=S_T3_OK),
        page([], image=img('!Chest', 2, 8, 0), sw1=S_T3_OK, self_switch='A'),
    ])
    # porta selada: so abre com um item especial (mais para a frente no jogo)
    misterio = (stop_bgm(1) + bgs('Darkness', 70) + se('Darkness3', pitch=70) + wait(20)
                + move(0, [rc(35), rc(17), rc(15, 20)], w=True)
                + me('Mystery') + wait(40)
                + narr('Uma porta selada, com uma meia-lua', 'entalhada no centro...')
                + narr('Um som misterioso ecoa do outro lado.', 'Parece... uma respiração?')
                + kuma('Arrepiei até a cauda.', i=3)
                + bar('Tem um encaixe vazio no meio da porta.', 'A gente ainda não tem nada que sirva aqui.')
                + move(0, [rc(16)], w=True)
                + stop_bgs(2) + bgm('Templo_Xavasca', vol=70) + switch(S_SELADA))
    m.add_event('Porta selada', 6, 11, [page(misterio, image=img('!Templo2', 1, 2), dir_fix=False, walk=False)])
    porta_trancada(m, 13, 11, IT_ARCOIRIS, S_PORTA[2], 'Chave Arco-Íris', (M_T3, 13, 8, 8, 0),
                   ('Trancada. A fechadura brilha com as cores', 'do arco-íris.'))
    portal(m, *PORTAIS[3][1:], 3)
    m.add_event('Descer', 13, 25, [page(transfer(M_T2, T2_PORTA[0], T2_PORTA[1] + 1, 2), trigger=1, priority=0)])
    m.add_event('Voltar ao salão', 13, 9, [page(transfer(M_T3, 13, 12, 2, 0), trigger=1)])
    return m


# ================================================================ cena da Vera Verao, roubo, corrida
def cena_vera(m, VE, LE, KE, CIRC, CRANIO):
    js_circulo = ' '.join(f'MapaVivo.mudarTile({12 + dx}, {4 + dy}, 1, {C0 + HEXAGRAMA_ACESO[dy][dx]});'
                          for dy in range(3) for dx in range(3))
    historia = []
    textos = [
        ('Há muitos séculos, existia o Reino de', 'Divilândia, comandado por Hebe Prime: a', 'primeira Diva.'),
        ('Do outro lado governava Vera Verão Prime,', 'uma bicha maligna que queria roubar todo', 'o glamour do mundo.'),
        ('Heróis de todos os lados uniram forças', 'para acabar com as duas imperatrizes...'),
        ('...e o mundo viveu em paz por muito', 'tempo.'),
        ('Menos a família Araújo, a linhagem do', 'Raulete. Eles sempre agiram como cobras', 'gananciosas.'),
        ('Então eles deram um golpe militar e', 'caçaram todas as bichas e divas que', 'restaram...'),
        ('...mas mal sabiam eles que a filha da', 'Hebe com o Ratinho tinha fugido.'),
        ('A filha da Hebe se casou com um cartomante', 'e teve um filho. E esse sangue divino foi', 'passando de geração em geração...'),
    ]
    for k, linhas in enumerate(textos, 1):
        historia += (pic(10, f'Historia_{k}', 408, 230, opacity=0, scale=96)
                     + move_pic_e(10, 408, 226, 255, 24, scale=100, w=True)
                     + vera(*linhas, i=2)
                     + move_pic_e(10, 408, 222, 0, 18, scale=104, w=True))
    historia += erase_pic(10)
    reluxa = ('Reluxabaria Xerebebe!', 'Lambida de lagartixa e dedo no pudim,', 'leite de cabra e gemido de anta!')
    lst = (
        fadeout()
        + script("$gamePlayer.locate(13, 7); $gamePlayer.setDirection(8);"
                 f"$gameMap.event({KE}).locate(11, 7); $gameMap.event({KE}).setDirection(8);")
        + script(set_self_js(M_T3, [KE], True))
        + followers(False)
        + fadein()
        + bar('Um círculo mágico...')
        + kuma('Encosta não, Baratelli! Da última vez que', 'você encostou num pentagrama, deu sapo.', i=3)
        + bar('Eu sinto o rastro mais forte do que nunca.', 'É aqui!')
        + stop_bgm(2)
        + se('Magic7') + script(js_circulo) + flash([255, 230, 255, 200], 30)
        + anim(CIRC, 117, w=False) + se('Saint5') + wait(40)
        + shake(4, 8, 30) + se('Thunder8', pitch=130)
        + me('Fanfare2')
        + flash([255, 255, 255, 255], 50)
        + script(set_self_js(M_T3, [VE], True))
        + anim(VE, 120, w=True)
        + bgm('Templo_Xavasca', vol=80)
        + destaque('evento', rosto='Vera_Verao', indice=1, titulo='A PRIMEIRA SABOROSA', nome='Vera Verão',
                   texto='Gloriosa, glamourosa e eterna.')
        + vera('Minha pequena tolinha...', 'Vejo que veio em busca de respostas.')
        + bar('V-Vera Verão?! A própria?!')
        + narr('Baratelli conta toda a sua história:', 'a maldição, a flor, a vidente, o crânio...')
        + bar('...e eu vim seguindo o rastro do cheiro', 'da Peruca Dourada!')
        + vera('Hahaha! Querida...', i=1)
        + vera('Você não sentiu o cheiro da peruca.', i=2)
        + vera('Na verdade, você sentiu o cheiro dos seus', 'antepassados.', i=2)
        + balloon(-1, 1)
        + stop_bgm(2) + bgm('Scene6', vol=65)
        + vera('Deixe-me te mostrar...', i=2)
        + historia
        + vera('...até despertar em você, querida Baratelli.', i=2)
        + vera('Na verdade, você é uma DIVA MUSUME SABOROSA:', 'o ser mais angelical e abençoado deste', 'mundo.')
        + vera('Só você pode acabar com os planos do', 'Raulete com os seus dons divinos.')
        # transformacao
        + stop_bgm(1) + se('Saint9') + anim(-1, 118, w=False) + wait(30)
        + pose(-1, 'magia', repetir=True, segurar=True)
        + flash([255, 200, 255, 255], 40) + shake(6, 8, 30)
        + visual(BARATELLI, '$Baratelli_Diva', 'Baratelli')
        + classe(BARATELLI, CLS_DIVA)
        + aprender(BARATELLI, SK_VIDENTE) + aprender(BARATELLI, SK_SAPO)
        + me('Fanfare3') + pose(-1, '')
        + destaque('evento', personagem='$Baratelli_Diva', titulo='TRANSFORMAÇÃO', nome='Baratelli, a Diva Musume Saborosa',
                   texto='Vestido arco-íris, salto lilás e guarda-chuva amarelo!')
        + bgm('Templo_Xavasca', vol=75)
        + pose(-1, 'choro', repetir=True, segurar=True)
        + bar('Snif... então eu sou especial...', 'E fico tão feliz!')
        + bar('Finalmente eu posso ajudar o mundo pelo', 'bem maior!')
        + pose(-1, '')
        + kuma('Baratelli... você tá LINDA!', i=2)
        + bar('Mas e a Peruca Dourada? Onde está?')
        + se('Laugh', pitch=120) + vera('Hahahaha! Estava pertinho de você esse', 'tempo todo, bobinha.', i=1)
        # o cranio vira a peruca
        + item(IT_CRANIO, -1)
        + script(set_self_js(M_T3, [CRANIO], True))
        + narr('Vera pega o crânio de Leandra...')
        + se('Crash') + script(f"$gameMap.event({CRANIO}).setDirection(4);") + shake(5, 8, 10) + wait(20)
        + se('Break') + script(f"$gameMap.event({CRANIO}).setDirection(6);") + shake(6, 8, 15)
        + narr('...e o quebra em vários pedaços, até virar', 'pó.')
        + vera(*reluxa, i=0)
        + se('Saint5') + script(f"$gameMap.event({CRANIO}).setDirection(8);") + anim(CRANIO, 120, w=True)
        + narr('O pó começa a brilhar em um tom dourado...', '...e forma a PERUCA DOURADA!')
        + script(set_self_js(M_T3, [CRANIO], False))
        + me('Item') + item(IT_PERUCA, 1)
        + destaque('item', imagem='Peruca_Ouro', titulo='ITEM LENDÁRIO', nome='Peruca Dourada', texto='Finalmente!')
        + bar('A Peruca Dourada... é minha!')
        + wait(30) + se('Down2') + balloon(-1, 6)
        + bar('Mas... a flor continua na minha cabeça.', 'A maldição não se desfez?!')
        + vera('Ainda não, querida.', i=2)
        + vera('Você deve usar a peruca na lua cheia, com o', 'sangue do Raulete, no topo da mansão dele.', i=2)
        + vera('E essa lua cheia acontecerá daqui a', 'dois dias.', i=2)
        + vera('Minha energia espiritual chegou ao fim.', 'Minha mensagem foi passada para a nova', 'geração.', i=2)
        + vera('Não deixe que os erros dos nossos', 'antepassados se repitam nesta geração.', i=2)
        + se('Saint7') + anim(VE, 100, w=False) + flash([255, 220, 255, 255], 40)
        + se('Starlight') + script(set_self_js(M_T3, [VE], False))
        + narr('Vera Verão desaparece em uma explosão de', 'purpurina mágica!')
        + wait(30)
        + bar('Eu vou pôr um fim à tirania do Raulete', 'e dos seus aliados!')
        # o roubo
        + stop_bgm(1) + se('Thunder3', pitch=140) + flash([200, 120, 255, 255], 15)
        + script(set_self_js(M_T3, [LE], True))
        + move(LE, [rc(29, 6), rc(37), UP, UP, rc(38)], w=True)
        + item(IT_PERUCA, -1)
        + se('Wind4') + balloon(-1, 1)
        + narr('Alguém rápido como um raio arranca a', 'peruca da mão de Baratelli!')
        + move(LE, [rc(29, 6), rc(37), UP, UP, rc(38), rc(16)], w=True)
        + bgm('Battle8', vol=70)
        + se('Laugh', pitch=90)
        + destaque('evento', rosto='Leona_Adulta', indice=1, titulo='A UMAMUSUME DE KURA', nome='Leona',
                   texto='Adulta, veloz e com um olhar maligno.')
        + leona('Hahaha! Então foi você a boba que achou a', 'peruca pro nosso mestre Raulete?', i=1)
        + bar('Quem é você, sua boba?!')
        + leona('Eu sou Leona, a Umamusume do Kura...', i=0)
        + leona('...o braço direito do Raulete! HAHAHAHA!', i=1)
        # a vidente revela o passado
        + bar('Leona...? Esse rabo de cavalo...')
        + pose(-1, 'magia', segurar=True)
        + se('Magic3') + anim(-1, 117, w=False)
        + destaque('item', imagem='Carta_Vidente_Calva', titulo='CLARIVIDÊNCIA', nome='A Vidente Calva',
                   texto='Baratelli acena a carta e vê o passado de Leandra...', tamanho=300)
        + pose(-1, '')
        + tint([40, 20, -40, 80], 20, w=True)
        + pic(10, 'Lembranca_Ponte', 408, 230, opacity=0) + move_pic_e(10, 408, 226, 255, 30, w=True)
        + narr('A ponte do rio subterrâneo... Leandra', 'apunhalada pela amiga de rabo de cavalo...', bg=1)
        + narr('...enquanto o Raulete roubava os cabelos', 'dela.', bg=1)
        + move_pic_e(10, 408, 222, 0, 24, w=True) + erase_pic(10) + tint([0, 0, 0, 0], 20, w=True)
        + bar('FOI VOCÊ! Você traiu a Leandra e ajudou a', 'roubar os cabelos dela!')
        + bar('Devolva o sonho da Leandra, sua', 'vagabunda!')
        + leona('Nunca! HAHAHAHA!', i=2)
        + se('Thunder9', pitch=150) + flash([200, 120, 255, 255], 20)
        + move(LE, [rc(29, 6), rc(37), DOWN, DOWN, DOWN, DOWN, DOWN, rc(39)], w=True)
        + script(set_self_js(M_T3, [LE], False))
        + narr('Leona dispara na velocidade da luz!')
        + kuma('Ela é rápida demais! A gente nunca vai', 'alcançar!', i=3)
        # carta do traveco
        + bar('...Nunca diga nunca, Kevinho.')
        + se('Saint9') + anim(-1, 118, w=False) + flash([255, 240, 255, 255], 30)
        + destaque('item', imagem='Carta_Traveco', titulo='CARTA DE TARÔ', nome='O Traveco',
                   texto='Extrai o potencial latente de quem a usa!', tamanho=330)
        + aprender(BARATELLI, SK_TRAVECO)
        + bar('Carta do Traveco! Extraia o nosso', 'potencial latente!')
        + se('Powerup') + anim(-1, 53, w=False) + anim(KE, 53, w=True)
        + narr('Baratelli e Kevinho ganham a velocidade de', 'Umamusumes perfeitas!')
        + kuma('ESTOU VOANDO! Vamos pegar ela!', i=2)
        + narr('CORRIDA UMAMUSUME!', 'Segure → ou Z para acelerar (gasta fôlego).')
        + narr('↑ ↓ trocam de raia. X usa a Carta do Traveco', '(uma vez por corrida).')
        + switch(S_VERA)
        + var_set(V_CORRIDA, 0)
        + plugin('CorridaUma', 'correr', {'variavel': V_CORRIDA, 'musica': 'Corrida_Uma'})
        + switch(S_CORRIDA)
        + item(IT_MEIA, 1)
        + script(set_self_js(M_T3, [KE], False))
        + followers(True)
        + transfer(M_MAUARA, 4, 28, 2, fade=2))
    return lst


def eventos_santuario(m):
    KE = m.add_event('Kevinho', 11, 7, [page([], priority=0, through=True),
                                        page([], image=img('$Kevinho_Uma', 0, 8), self_switch='A')])
    VE = m.add_event('Vera Verão', 13, 4, [page([], priority=0, through=True),
                                          page([], image=img('$Vera_Verao', 0, 2), step=True, self_switch='A', through=True)])
    LE = m.add_event('Leona', 13, 10, [page([], priority=0, through=True),
                                       page([], image=img('$Leona_Adulta', 0, 8), self_switch='A', through=True)])
    CRANIO = m.add_event('Crânio', 13, 5, [page([], priority=0, through=True),
                                           page([], image=img('!Templo2', 7, 2), priority=0, through=True, step=True,
                                                dir_fix=False, walk=False, self_switch='A')])
    CIRC = m.add_event('Círculo mágico', 13, 5, [
        page([], priority=0),
        page(cena_vera(m, VE, LE, KE, None, CRANIO), priority=0, trigger=0, sw1=S_PORTA[2]),
        page(narr('O círculo mágico ainda brilha baixinho.'), priority=0, sw1=S_VERA),
    ])
    # o comando do circulo usa o proprio evento como alvo das animacoes
    for pg in m.events[CIRC]['pages']:
        for c in pg['list']:
            if c['code'] == 212 and c['parameters'][0] is None:
                c['parameters'][0] = 0
    m.add_event('Brilho do círculo', 13, 3, [page(narr('Um brilho dourado escapa do círculo mágico.')
                                                  + bar('O rastro termina aqui... no círculo!'), priority=0, trigger=1,
                                                  sw1=S_PORTA[2]), page([], priority=0, sw1=S_VERA)])
    return dict(KE=KE, VE=VE, LE=LE, CRANIO=CRANIO, CIRC=CIRC)


# ================================================================ final (na entrada da Floresta de Mauara)
def final_capitulo(m):
    KE = m.add_event('Kevinho (final)', 9, 28, [
        page([], priority=0, through=True),
        page([], image=img('$Kevinho_Uma', 0, 4), self_switch='A'),
    ])
    lst = (wait(20)
           + script("$gamePlayer.locate(4, 28); $gamePlayer.setDirection(6);")
           + followers(False)
           + bgs('Wind1', 40)
           + pose(-1, 'cansado', repetir=True, segurar=True)
           + se('Breath')
           + narr('Na saída da Floresta de Mauara...')
           + narr('Baratelli alcançou a Leona e arrancou METADE', 'da peruca da mão dela.')
           + narr('Mas Leona escapou com a outra metade e', 'sumiu de vista.')
           + destaque('item', imagem='Item_Peruca_Metade', titulo='ITEM IMPORTANTE', nome='Metade da Peruca Dourada',
                      texto='A outra metade está com a Leona.')
           + bar('Hah... hah... ela sumiu...')
           + script(set_self_js(M_MAUARA, [KE], True))
           + move(KE, [rc(29, 5), LEFT, LEFT, LEFT], w=True)
           + kuma('Baratelli! Hah... hah... você pegou ela?', i=3)
           + pose(-1, 'choro', repetir=True, segurar=True)
           + stop_bgs(2) + bgm('Scene2', vol=60)
           + bar('Só metade, Kevinho...', 'Eu perdi metade da peruca...')
           + wait(40) + pose(-1, '')
           + bar('...Mas isso não importa mais.')
           + bar('Nós vamos até a mansão do Raulete.')
           + bar('E vamos ter o sangue dele...', '...e a outra metade da peruca!')
           + kuma('E a lua cheia é daqui a dois dias.', 'Bora!', i=1)
           + switch(S_C4_FIM)
           + fadeout() + stop_bgm(3)
           + pic(9, 'Final_Cap4', 408, 312) + move_pic_e(9, 408, 312, 255, 500, scale=108, easing=0)
           + bgm('Scene8', vol=60) + fadein()
           + wait(70)
           + narr('Baratelli segura a metade da peruca dourada...', bg=1)
           + se('Thunder2', vol=60, pitch=80)
           + narr('...e olha com raiva, direto para você.', bg=1)
           + wait(60) + fadeout() + erase_pic(9) + stop_bgm(2)
           + me('Mystery')
           + capitulo('FimCapitulo4')
           + [cmd(354, [])])
    m.add_event('Final do capítulo', 0, 37, [
        page([], priority=0),
        page(lst, trigger=3, priority=0, sw1=S_CORRIDA),
        page([], priority=0, sw1=S_C4_FIM),
    ])


# ================================================================ eventos comuns
def ce_portal():
    js = f"""const aqui = $gameVariables.value({V_PORTAL_AQUI});
const ops = [], dest = [];
const add = (nome, cond, d) => {{ if (cond) {{ ops.push(nome); dest.push(d); }} }};
add('1º Andar do Templo', aqui !== 1 && $gameSwitches.value({S_PORTAL[0]}), [{M_T1}, {PORTAIS[1][1]}, {PORTAIS[1][2]}]);
add('2º Andar do Templo', aqui !== 2 && $gameSwitches.value({S_PORTAL[1]}), [{M_T2}, {PORTAIS[2][1]}, {PORTAIS[2][2]}]);
add('3º Andar do Templo', aqui !== 3 && $gameSwitches.value({S_PORTAL[2]}), [{M_T3}, {PORTAIS[3][1]}, {PORTAIS[3][2]}]);
add('Entrada da Floresta de Mauara', aqui !== 0 && $gameSwitches.value({S_PORTAL[2]}), [{M_MAUARA}, {PORTAIS[0][1]}, {PORTAIS[0][2]}]);
ops.push('Ficar aqui'); dest.push(null);
$gameTemp._portalDestino = null;
$gameMessage.setBackground(0); $gameMessage.setPositionType(2);
$gameMessage.add('O portal brilha. Para onde você quer ir?');
$gameMessage.setChoices(ops, 0, ops.length - 1);
$gameMessage.setChoiceBackground(0); $gameMessage.setChoicePositionType(2);
$gameMessage.setChoiceCallback(n => {{ $gameTemp._portalDestino = dest[n]; }});
this.setWaitMode('message');"""
    vai = """const d = $gameTemp._portalDestino;
if (d) {
  AudioManager.playSe({name: 'Teleport', volume: 90, pitch: 100, pan: 0});
  $gamePlayer.reserveTransfer(d[0], d[1], d[2], 2, 0);
  this.setWaitMode('transfer');
}"""
    return script(js) + script(vai)
