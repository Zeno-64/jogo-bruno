# Capitulo 4: numeros (mapas, switches, variaveis, itens...) e atalhos de evento usados pelos builders do capitulo.
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ch1 as B
from build_ch1 import (Map, rect, cmd, text, narr, se, bgm, me, wait, balloon, tint, flash, shake, transfer, switch,
                       var_set, self_sw, pic, move_pic, erase_pic, anim, rc, move, page, map_json, audio, load, save,
                       A2, A3, A4, C0, D0, E0, END, NORMAL, DOWN, LEFT, RIGHT, UP)
from build_ch2 import (sub, if_, choices, script, item, party_add, party_remove, followers, fadeout, fadein,
                       stop_bgm, bgs, stop_bgs, call, set_self_js, img, flame, paint, mk_skill, tpage, A5)
from fx import destaque, capitulo, move_pic_e, pose

PROJ = B.PROJ

# ---------------------------------------------------------------- mapas
M_VIDENTE = 14
M_CAMPO, M_MAUARA, M_CORACAO, M_T1, M_T2, M_T3 = 15, 16, 17, 18, 19, 20

# ---------------------------------------------------------------- switches
S_C4_INICIO = 22          # abertura vista (cartas e bencao)
S_C4_UMA = 23             # Kevinho virou Umamusume
S_C4_FLORESTA = 24        # entrou na floresta
S_ESPINHOS = [25, 26, 27]
S_PAVAO = 28              # Pavao-Hipopotamo vencido (porta do templo aberta)
S_PORTAL = [29, 30, 31]   # portais do 1o, 2o e 3o andar ativados
S_T1_OK, S_T2_OK, S_T3_OK = 32, 33, 34
S_PORTA = [35, 36, 37]    # portas trancadas abertas (para o 2o andar, 3o andar e santuario)
S_VERA = 38               # cena da Vera vista (corrida em seguida)
S_CORRIDA = 39            # alcancou a Leona
S_C4_FIM = 40
S_CORACAO = 41            # chegou no coracao da floresta
S_SELADA = 42             # ouviu a porta selada
S_ESPINHOS2 = [43]        # espinhos do coracao da floresta

# ---------------------------------------------------------------- variaveis
V_RAND = 5
V_MAO = 7                 # peruca na mao (0 nenhuma, 1 loira, 2 ruiva, 3 azul, 4 preta)
V_BUSTOS = [8, 9, 10, 11]
V_ESFINGE = 12
V_CORRIDA = 13
V_LUTA = 14
V_DX, V_DY, V_MAPA = 16, 17, 18
V_NOME = 21
V_PORTAL_AQUI = 22

# ---------------------------------------------------------------- banco de dados
IT_CRANIO = 32
IT_PERUCA, IT_MEIA, IT_JADE, IT_FERRADURA, IT_ARCOIRIS, IT_CENOURA, IT_PENA, IT_GUARANA = 42, 43, 44, 45, 46, 47, 48, 49
SK_VIDENTE, SK_SAPO, SK_TRAVECO, SK_COICE, SK_GALOPE, SK_RELINCHO = 255, 256, 257, 258, 259, 260
SK_FOFOCA, SK_BICADA, SK_SUPINO, SK_CALMA = 261, 262, 263, 264
EN_ARARA, EN_CAPIVARA = 8, 9
TR_ARARAS, TR_CAPIVARA, TR_MISTO = 8, 9, 10
CLS_CIGANA, CLS_AMIGO, CLS_UMA, CLS_DIVA = 11, 12, 13, 14
CE_FALAS, CE_PORTAL, CE_CIPO, CE_AREIA, CE_TROPECO = 6, 7, 8, 9, 10
BARATELLI, KEVINHO = 1, 5

PERUCA_COR = {1: 'Loira', 2: 'Ruiva', 3: 'Azul', 4: 'Preta'}
SOLUCAO_BUSTOS = [3, 2, 1, 4]         # da esquerda para a direita: Azul, Ruiva, Loira, Preta

# chegadas
CAMPO_SAIDA = (18, 7)
MAUARA_INICIO = (2, 30)
MAUARA_FIM = (42, 1)
CORACAO_INICIO = (18, 36)
CORACAO_PORTA = (19, 4)
T1_CHEGADA, T2_CHEGADA, T3_CHEGADA = (12, 17), (13, 19), (13, 24)
T1_PORTA, T2_PORTA = (12, 2), (13, 2)
PORTAIS = {1: (M_T1, 4, 16), 2: (M_T2, 7, 18), 3: (M_T3, 8, 22), 0: (M_MAUARA, 5, 27)}


# ---------------------------------------------------------------- falas
def bar(*l):
    return text(list(l), face='Baratelli', idx=0, name='Baratelli')


def kev(*l, i=0):
    return text(list(l), face='Kevinho', idx=i, name='Kevinho')


def kuma(*l, i=0):
    """Kevinho depois de virar Umamusume (0 normal, 1 serio, 2 feliz, 3 susto)."""
    return text(list(l), face='Kevinho_Uma', idx=i, name='Kevinho')


def vera(*l, i=0):
    return text(list(l), face='Vera_Verao', idx=i, name='Vera Verão')


def leona(*l, i=0):
    return text(list(l), face='Leona_Adulta', idx=i, name='Leona')


def pavao(*l):
    return text(list(l), face='Mauara', idx=0, name='Pavão-Hipopótamo')


def curupira(*l):
    return text(list(l), face='Mauara', idx=1, name='Curupira')


def esfinge(*l):
    return text(list(l), name='Esfinge Careca')


def topo(*l):
    """Legenda no topo da tela, sem janela de rosto."""
    return text(list(l), pos=0)


def sorteio(blocos, var=V_RAND):
    out = [cmd(122, [var, var, 0, 2, 0, len(blocos) - 1])]
    for i, b in enumerate(blocos):
        out += if_([1, var, 0, i, 0], b)
    return out


def batalha(troop, vitoria, fuga, derrota, bgm_nome='Battle3'):
    out = [cmd(132, [audio(bgm_nome, 90)]), cmd(301, [0, troop, True, True]), cmd(601, [])]
    out += sub(vitoria) + [cmd(0, [], 1), cmd(602, [])]
    out += sub(fuga) + [cmd(0, [], 1), cmd(603, [])]
    out += sub(derrota) + [cmd(0, [], 1), cmd(604, [])]
    return out


def plugin(nome, comando, args):
    return [cmd(357, [nome, comando, comando, {k: str(v) for k, v in args.items()}])]


def aprender(ator, skill):
    return [cmd(318, [0, ator, 0, skill])]


def visual(ator, char, face, idx=0):
    return [cmd(322, [ator, char, 0, face, idx, ''])]


def classe(ator, cls):
    return [cmd(321, [ator, cls, True])]


def tem_item(iid, entao, senao=None):
    return if_([8, iid], entao, senao)


def var_add(v, n=1):
    return [cmd(122, [v, v, 1, 0, n])]


def var_eq(v, n, entao, senao=None):
    return if_([1, v, 0, n, 0], entao, senao)


def sw_on(s, entao, senao=None):
    return if_([0, s, 0], entao, senao)


def bau(m, x, y, iid, n, imagem, nome, texto, idx=0):
    m.add_event('Baú', x, y, [
        page(se('Chest1') + self_sw() + item(iid, n) + destaque('item', imagem=imagem, nome=nome, texto=texto),
             image=img('!Chest', idx, 2, 0)),
        page([], image=img('!Chest', idx, 8, 0), self_switch='A'),
    ])


def placa_tile(m, x, y, tile, *linhas, z=2):
    m.put(x, y, z, tile)
    m.add_event('Placa', x, y, [page(narr(*linhas))])
