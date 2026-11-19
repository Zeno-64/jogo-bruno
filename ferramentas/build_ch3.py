# Monta o Capitulo 3: casa da Baratelli, Morro do Macaco, casa da vidente e a batalha contra o Gusrola sapo.
import copy, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ch1 as B
import build_ch2 as B2
import build_morro as BM
from fx import destaque, capitulo, move_pic_e, pose
from build_ch1 import (Map, rect, building, cmd, text, narr, se, bgm, me, wait, balloon, tint, flash, shake,
                       transfer, switch, self_sw, pic, move_pic, erase_pic, anim, rc, move, page, ambient,
                       map_json, audio, load, save, A2, A3, A4, C0, D0, END, NORMAL, DOWN, LEFT, RIGHT, UP)
from build_ch2 import (sub, if_, choices, script, item, party_add, party_remove, followers, fadeout, fadein,
                       stop_bgm, bgs, stop_bgs, battle, set_self_js, img, flame, paint, mk_skill, tpage, A5)

PROJ = B.PROJ

M_CASA_B, M_MORRO, M_VIDENTE = 12, 13, 14
S_C3_INICIO, S_C3_KEV, S_C3_TOPO, S_C3_RITUAL, S_C3_FIM = 15, 16, 17, 18, 19
S_C3_CASA = 20
BARATELLI, KEVINHO = 1, 5
CLS_CIGANA, CLS_AMIGO = 11, 12
SK3 = 245
EN_SAPO = TROOP_SAPO = 7


def bar(*lines):
    return text(list(lines), face='Baratelli', idx=0, name='Baratelli')


def kev(*lines, i=0):
    return text(list(lines), face='Kevinho', idx=i, name='Kevinho')


def gus(*lines):
    return text(list(lines), face='People1', idx=2, name='Gusrola')


def sapo(*lines):
    return text(list(lines), face='Gusrola_Sapo', idx=0, name='Gusrola')


def mk(*lines):
    return text(list(lines), name='Monark')


def vid(*lines, i=0):
    return text(list(lines), face='Vidente', idx=i, name='Vidente')


def leandra_velha(*lines):
    return text(list(lines), face='Leandra', idx=3, name='Leandra')


RESET_PLAYER = ("$gamePlayer.setTransparent(false); $gamePlayer.setThrough(false);\n"
                "$gamePlayer.setDirectionFix(false); $gamePlayer.setOpacity(255);\n"
                "$gamePlayer.setMoveSpeed(4); $gamePlayer.showFollowers(); $gamePlayer.refresh(); $gamePlayer.pose('');")


# ============================================================ 12. CASA DA BARATELLI
def build_casa_b():
    m = Map(15, 11, 3)
    B.room(m, 0, 0, 14, 10, 20, 28, 0, door=(7, 10))
    m.auto(rect(5, 5, 9, 8), A2 + 19 * 48, 0)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for (x, y, t) in [(2, 2, 157), (2, 3, 165), (3, 2, 157), (3, 3, 165), (12, 3, 168), (12, 4, 176), (10, 3, 204),
                      (10, 2, 118), (5, 1, 85), (9, 1, 85), (7, 2, 130), (3, 7, 114), (2, 7, 101), (4, 7, 101),
                      (1, 3, C0 + 86), (13, 9, C0 + 87), (1, 9, C0 + 86)]:
        b(x, y, t)
    b(3, 7, C0 + 123, 3)
    return m


def events_casa_b(m):
    ambient(m, NORMAL)
    monark = m.add_event('Monark', 6, 4, [page([], image=img('$Monark', 0, 6)),
                                          page([], priority=0, through=True, sw1=S_C3_INICIO)])
    gusrola = m.add_event('Gusrola', 7, 4, [page([], image=img('People1', 2, 4)),
                                            page([], priority=0, through=True, sw1=S_C3_INICIO)])
    portal = m.add_event('Portal', 7, 3, [page([], priority=0, through=True),
                                          page([], image=img('!$Portal', 0, 2), priority=0, through=True, step=True,
                                               dir_fix=True, walk=False, self_switch='A')])
    kevinho = m.add_event('Kevinho', 7, 10, [page([], priority=0, through=True),
                                             page([], image=img('$Kevinho', 0, 8), self_switch='A'),
                                             page([], priority=0, through=True, sw1=S_C3_KEV)])
    cena = (fadeout() + stop_bgm(1) + stop_bgs(1)
            + script(RESET_PLAYER)
            + party_remove(2) + party_remove(3) + party_add(BARATELLI)
            + [cmd(322, [BARATELLI, '$Baratelli_Flor', 0, 'Baratelli', 0, ''])]
            + tint(NORMAL, 0)
            + capitulo('Capitulo3')
            + narr('Logo depois da maldição na Luz da Sé...')
            + narr('Baratelli corre para casa, desesperada para', 'contar tudo ao Gusrola.')
            + fadein()
            + bar('Gusrola! Você não vai acreditar', 'no que me aconteceu...')
            + balloon(-1, 1)
            + balloon(monark, 4, w=False) + balloon(gusrola, 4)
            + narr('Monark e Gusrola estão se beijando no meio', 'da sala!')
            + me('Shock1')
            + balloon(-1, 5)
            + bar('MONARK?! GUSROLA?!')
            + bar('Seus... seus TRAIDORES!')
            + move(monark, [rc(16)], w=False) + move(gusrola, [rc(16)], w=True)
            + narr('Cega de ódio, Baratelli parte pra cima dos', 'dois...')
            + move(-1, [rc(29, 5), UP, UP, UP], w=True)
            + se('Blow1') + pose(-1, 'queda', segurar=True)
            + move(-1, [rc(35), rc(14, 0, 1), rc(36), rc(29, 4)], w=True) + shake(5, 9, 15)
            + narr('...mas tropeça no tapete e cai de cara', 'no chão!')
            + se('Laugh')
            + balloon(monark, 3, w=False) + balloon(gusrola, 3)
            + pose(monark, 'riso', repetir=True, segurar=True) + pose(gusrola, 'riso', repetir=True, segurar=True)
            + gus('Hahahaha! Olha só a titia!')
            + mk('Hahaha! Caiu de novo!')
            + pose(-1, '') + pose(monark, '') + pose(gusrola, '')
            + bar('P-por quê, Gusrola...?')
            + gus('Titia... eu nunca fui seu sobrinho', 'de verdade.')
            + gus('Eu sirvo ao Mestre Raulete.', 'Sempre servi.')
            + gus('Tudo foi um plano pra que a maldição', 'caísse em você!')
            + pose(monark, 'riso', espera=4)
            + mk('E você caiu direitinho. Hahahaha!')
            + gus('Chega de disfarce! Veja a minha', 'VERDADEIRA forma!')
            + pose(gusrola, 'magia', repetir=True, segurar=True)
            + se('Darkness2') + anim(gusrola, 101, w=False) + flash([120, 255, 120, 180], 30, w=False) + wait(20)
            + move(gusrola, [rc(41, '$Gusrola_Sapo', 0)], w=True) + se('Frog') + pose(gusrola, '')
            + narr('Gusrola se transforma em um sapo', 'humanoide!')
            + destaque('evento', rosto='Gusrola_Sapo', titulo='FORMA VERDADEIRA', nome='Gusrola Sapo',
                       texto='O sobrinho era um sapo o tempo todo!')
            + pose(gusrola, 'riso', espera=4)
            + sapo('Croac! Croac! Hahahaha!')
            + se('Fire2') + anim(monark, 66, w=False) + flash([255, 160, 60, 180], 30, w=False) + wait(20)
            + move(monark, [rc(41, '$Mula_Sem_Cabeca', 0)], w=True) + se('Horse')
            + narr('E Monark vira uma mula sem cabeça, com fogo', 'no lugar do pescoço!')
            + se('Teleport') + script(set_self_js(M_CASA_B, [portal], True)) + wait(30)
            + sapo('Adeus, titia! Croac!')
            + move(gusrola, [rc(37), UP, rc(39)], w=True)
            + move(monark, [rc(37), RIGHT, UP, rc(39)], w=True)
            + se('Teleport') + script(set_self_js(M_CASA_B, [portal], False))
            + narr('Os dois atravessam um portal e', 'desaparecem!')
            + bgm('Scene2', vol=65)
            + balloon(-1, 6)
            + pose(-1, 'choro', repetir=True, segurar=True)
            + bar('Snif... snif...')
            + bar('Ninguém me ama de verdade...')
            + wait(40)
            + pose(-1, '')
            + se('Door1') + script(set_self_js(M_CASA_B, [kevinho], True))
            + move(kevinho, [UP, UP, UP], w=True)
            + kev('Baratelli? Que bagunça é essa?!', 'Ouvi uns coaxos lá de fora...')
            + move(-1, [rc(16)], w=True)
            + bar('Kevinho...! O Gusrola e o Monark me', 'traíram... e eu fui amaldiçoada...')
            + narr('Baratelli conta tudo para Kevinho.')
            + kev('Calma, Baratelli. Eu conheço um jeito', 'de te ajudar a achar a Peruca Dourada.')
            + kev('Segundo uma lenda local, uma vidente', 'mora no Morro do Macaco.')
            + kev('Dizem que ela consegue adivinhar', 'qualquer coisa!')
            + balloon(-1, 1)
            + bar('Sério?! Então vamos agora mesmo!')
            + move(kevinho, [rc(37), UP], w=True)
            + party_add(KEVINHO)
            + script(f'$gamePlayer.followers().follower(0).locate($gameMap.event({kevinho}).x, $gameMap.event({kevinho}).y);')
            + switch(S_C3_KEV)
            + destaque('membro', rosto='Kevinho', nome='Kevinho',
                       texto='O Amigo Fiel. Conhece todas as lendas da região.')
            + narr('O Morro do Macaco fica numa montanha a', 'leste de São Matheos.')
            + switch(S_C3_INICIO)
            + narr('Quando estiver pronta, saia pela porta para', 'ir ao Morro do Macaco.'))
    m.add_event('Abertura', 0, 10, [page(cena, trigger=3, priority=0), page([], priority=0, sw1=S_C3_INICIO)])
    m.add_event('Saída', 7, 10, [page([], priority=0),
                                 page(se('Door1') + transfer(M_MORRO, BM.INICIO[0], BM.INICIO[1], 8, fade=0), trigger=1, priority=0,
                                      sw1=S_C3_INICIO)])


# ============================================================ 13. MORRO DO MACACO
# Fica em build_morro.py (Rei Macaco, bananas douradas, cascas, pedras frageis e cocos).


# ============================================================ 14. CASA DA VIDENTE
VID_ROWS = ['#' * 17, '#' + 'W' * 15 + '#', '#' + 'W' * 15 + '#'] + ['#' + '.' * 15 + '#'] * 9 + ['########.########']


def build_vidente():
    m = Map(17, 13, 4)
    paint(m, VID_ROWS, 17, 25, lambda x, y, ch: A5 + 16)
    m.auto(rect(4, 5, 12, 10), A2 + 27 * 48, 0)
    b = lambda x, y, t, z=2: m.put(x, y, z, t)
    for row in range(3):
        for col in range(3):
            b(7 + col, 6 + row, D0 + 8 + row * 8 + col)
    for (x, y, t) in [(2, 2, C0 + 197), (2, 3, C0 + 205), (3, 2, C0 + 198), (3, 3, C0 + 206), (4, 2, C0 + 199),
                      (4, 3, C0 + 207), (13, 2, C0 + 196), (13, 3, C0 + 204), (15, 3, C0 + 134), (15, 4, C0 + 142),
                      (12, 4, C0 + 149), (11, 4, C0 + 240), (8, 1, 166), (5, 1, C0 + 230), (5, 2, C0 + 238),
                      (11, 1, C0 + 230), (11, 2, C0 + 238), (1, 10, 242), (14, 10, 45), (2, 9, 45), (1, 4, 230),
                      (15, 9, 231)]:
        b(x, y, t)
    return m


def battle_loop():
    return ([cmd(118, ['luta'])]
            + [cmd(132, [audio('Battle5', 90)])]
            + [cmd(301, [0, TROOP_SAPO, False, True]), cmd(601, []), cmd(0, [], 1), cmd(603, [])]
            + sub([cmd(314, [0, 0])] + sapo('Croac! Fracos! Hahahaha!')
                  + kev('Levanta, Baratelli! Mais uma vez!', i=1) + [cmd(119, ['luta'])])
            + [cmd(0, [], 1), cmd(604, [])])


def events_vidente(m):
    ambient(m, [-20, -20, 10, 20])
    for (x, y) in [(6, 5), (10, 5), (6, 9), (10, 9)]:
        flame(m, x, y, 1, 6)
    V = m.add_event('Vidente', 8, 4, [page(vid('...'), image=img('$Vidente', 0, 2))])
    GU = m.add_event('Gusrola', 13, 5, [page([], priority=0, through=True),
                                        page([], image=img('$Gusrola_Sapo', 0, 4), self_switch='A'),
                                        page([], priority=0, through=True, self_switch='B')])
    KE = m.add_event('Kevinho', 8, 11, [page([], priority=0, through=True),
                                        page([], image=img('$Kevinho', 0, 8), self_switch='A')])
    PO = m.add_event('Portal', 13, 5, [page([], priority=0, through=True),
                                       page([], image=img('!$Portal', 0, 2), priority=0, through=True, step=True,
                                            dir_fix=True, walk=False, self_switch='A')])
    luta = (
        kev('Ei, sapo! Deixa ela em paz!', i=1)
        + bgm('Battle5', vol=85)
        + move(KE, [rc(29, 5), rc(37), rc(14, 3, -2), rc(38)], w=True)
        + pose(KE, 'chute', olhar=GU, espera=8)
        + se('Blow3') + anim(GU, 1, w=False) + shake(6, 9, 12) + pose(GU, 'dor', olhar=KE)
        + sapo('Croac!')
        + move(GU, [rc(37), rc(14, 0, 2), rc(38)], w=True)
        + bar('Toma essa, sapo traidor!')
        + pose(-1, 'magia', olhar=GU, espera=10)
        + se('Fire1') + pose(GU, 'dor') + anim(GU, 66, w=True)
        + sapo('Isso foi tudo, titia?!')
        + pose(GU, 'soco', olhar=-1, espera=6)
        + se('Darkness2') + anim(-1, 101, w=False) + flash([120, 0, 160, 160], 20) + shake(5, 9, 10) + pose(-1, 'dor')
        + move(KE, [rc(14, 0, 2)], w=True)
        + pose(KE, 'soco', olhar=GU, espera=6)
        + se('Blow5') + anim(GU, 39, w=False) + shake(6, 9, 10) + pose(GU, 'dor')
        + pose(GU, 'chute', olhar=KE, espera=6)
        + se('Slash1') + pose(KE, 'dor') + anim(KE, 16, w=True)
        + kev('Pega ele, Baratelli!', i=1)
        + pose(-1, 'magia', olhar=GU, espera=8)
        + se('Ice1') + pose(GU, 'dor') + anim(GU, 71, w=True)
        + pose(-1, 'magia', espera=4)
        + se('Thunder3') + anim(GU, 76, w=False) + flash([255, 255, 160, 200], 20) + shake(8, 9, 20) + pose(GU, 'dor')
        + sapo('CROOOAC!')
        + pose(GU, 'magia', espera=8)
        + se('Water1') + pose(-1, 'dor') + pose(KE, 'dor') + anim(-1, 81, w=False) + anim(KE, 81, w=True)
        + move(GU, [rc(14, -1, 0)], w=False) + move(KE, [rc(14, 1, 0)], w=True)
        + pose(GU, 'chute', olhar=KE) + pose(KE, 'chute', olhar=GU, espera=6)
        + se('Blow8') + flash([255, 255, 255, 200], 15) + shake(9, 9, 20)
        + se('Breath')
        + pose(-1, 'cansado', repetir=True, segurar=True) + pose(KE, 'cansado', repetir=True, segurar=True)
        + pose(GU, 'cansado', repetir=True, segurar=True)
        + balloon(-1, 6, w=False) + balloon(KE, 6, w=False) + balloon(GU, 6)
        + narr('A luta é tão épica que os três ficam', 'completamente exaustos...')
        + sapo('Croac... croac... Chega!', 'Vou acabar com vocês de uma vez!')
        + battle_loop()
        + [cmd(314, [0, 0])]
        + stop_bgm(1)
        + se('Darkness1') + flash([255, 255, 255, 200], 30)
        + move(GU, [rc(41, 'People1', 2)], w=True)
        + pose(-1, '') + pose(KE, '') + pose(GU, '')
        + narr('Derrotado, Gusrola volta à forma humana.')
        + pose(GU, 'choro', repetir=True, segurar=True)
        + gus('Titia... me perdoa...', 'Eu me arrependo de tudo...')
        + bar('Não dá mais pra confiar em você,', 'Gusrola.')
        + pose(-1, 'magia', olhar=GU, segurar=True)
        + se('Saint7') + anim(GU, 100, w=False) + flash([255, 240, 200, 220], 40) + pose(GU, 'dor', segurar=True)
        + bar('Morra, monstro! Você não pertence à', 'minha leitura de signos, bobinho!')
        + pose(-1, '')
        + se('Collapse4')
        + move(GU, [rc(42, 180), rc(15, 6), rc(42, 110), rc(15, 6), rc(42, 50), rc(15, 6), rc(42, 0)], w=True)
        + script(f"$gameSelfSwitches.setValue([{M_VIDENTE}, {GU}, 'B'], true);")
        + narr('Gusrola desaparece para sempre.')
        + bgm('Scene2', vol=65)
        + wait(30)
        + pose(V, 'rastejar', repetir=True, segurar=True, velocidade=10)
        + move(V, [rc(29, 1), rc(10)], w=True)
        + vid('Baratelli...', i=1)
        + vid('Eu preciso te contar quem eu sou', 'de verdade.', i=1)
        + leandra_velha('Eu sou... a Leandra.')
        + leandra_velha('Fui sequestrada pelo Raulete...', 'Ele arrancou os meus cabelos.')
        + leandra_velha('E fui traída pela minha amiga...', 'Ela tinha um rabo de cavalo igualzinho', 'ao seu...')
        + balloon(-1, 1)
        + pose(-1, 'choro', repetir=True, segurar=True)
        + bar('Leandra...!')
        + narr('Leandra não resiste...')
        + se('Darkness4') + flash([60, 40, 80, 200], 40)
        + move(V, [rc(45, 'this.setTileImage(250)')], w=True)
        + narr('...e o seu corpo se desfaz em um', 'esqueleto.')
        + wait(30)
        + pose(-1, '')
        + bar('Leandra... eu juro que vou te vingar.')
        + narr('Baratelli pega o crânio de Leandra.')
        + item(32, 1) + destaque('item', imagem='Item_Cranio', titulo='ITEM IMPORTANTE', nome='Crânio da Leandra',
                                 texto='Uma promessa de vingança.')
        + switch(S_C3_FIM)
        + fadeout() + stop_bgm(3)
        + pic(9, 'Final_Cap3', 408, 312) + move_pic_e(9, 408, 300, 255, 600, scale=110, easing=0)
        + bgm('Scene8', vol=60) + fadein()
        + wait(60)
        + narr('Baratelli segura o crânio de Leandra', 'enquanto olha para a lua...', bg=1)
        + se('Fall', vol=70)
        + narr('...e mais uma mecha do seu cabelo cai.', bg=1)
        + wait(60) + fadeout() + erase_pic(9) + stop_bgm(2)
        + me('Mystery')
        + capitulo('FimCapitulo3')
        + [cmd(354, [])])
    chegada = (wait(20) + bgm('Scene6', vol=65)
               + narr('Velas, estrelas pintadas no teto e um', 'cheiro forte de incenso...')
               + balloon(V, 1)
               + vid('Visitantes? Aqui no alto do morro?')
               + vid('Fiquem à vontade... só não mexam no', 'meu incenso.')
               + kev('É ela! A vidente da lenda!', 'Vai lá falar com ela, Baratelli.')
               + switch(S_C3_CASA))
    ritual = (fadeout()
              + script('$gamePlayer.locate(8, 5); $gamePlayer.setDirection(8);\n'
                       '$gamePlayer.followers().synchronize(8, 6, 8);')
              + fadein()
              # Kevinho sai do caminho: vira evento ao lado do pentagrama
              + script(f"const f = $gamePlayer.followers().follower(0); const k = $gameMap.event({KE});\n"
                       f"k.locate(f.x, f.y); k.setDirection(8);\n" + set_self_js(M_VIDENTE, [KE], True))
              + followers(False)
              + move(KE, [LEFT, rc(19)], w=True)
              + bar('Ó vidente, por favor... nos ajude a', 'encontrar a Peruca Dourada!')
              + me('Shock1') + balloon(V, 1)
              + vid('A... Peruca Dourada?!', i=1)
              + vid('Por que você procura a Peruca Dourada,', 'menina?')
              + bar('Eu fui amaldiçoada pelo Raulete e pelo', 'Monark...')
              + bar('Se eu não achar a peruca, vou ficar', 'calva para sempre!')
              + vid('Hmm... Me dê a sua mão.', 'Vou ler o seu futuro.')
              + se('Magic1') + anim(-1, 45, w=True)
              + narr('A vidente pega a mão de Baratelli...')
              + wait(30)
              + se('Cry2', vol=70) + balloon(V, 6)
              + narr('...e começa a chorar.')
              + bar('O que foi? O que você viu?!')
              + vid('Menina... você é a criança', 'predestinada.', i=1)
              + vid('Você descende de Henri Cristo e Hebe', 'Camargo, os antigos líderes da nação.', i=1)
              + vid('Eles tinham o poder da clarividência e', 'da astrologia avançada!', i=1)
              + balloon(-1, 1)
              + bar('EU?! Descendente da Hebe?!')
              + kev('Isso explica muita coisa...')
              + vid('Venha até o pentagrama, no centro da', 'sala.')
              + move(-1, [rc(35), DOWN, DOWN, rc(36), rc(19)], w=True)
              + stop_bgm(2) + bgs('Darkness', 60)
              + vid('Ossos da lua, estrelas do destino...', 'venham trabalhar!')
              + tint([-60, -50, 0, 40], 40, w=True)
              + pose(-1, 'magia', repetir=True, segurar=True)
              + vid('OSSOS DA LUA, ESTRELAS DO DESTINO...', 'VENHAM TRABALHAR!')
              + se('Saint5') + pic(6, 'Raio_Lua', 288, 70, opacity=0, origin=0) + move_pic(6, 288, 70, 230, 40, origin=0, w=True)
              + anim(-1, 117, w=True)
              + narr('A luz da lua atravessa a janela e', 'ilumina Baratelli!')
              + flash([255, 255, 255, 255], 40) + shake(5, 7, 30)
              + narr('Baratelli desperta os seus poderes!')
              + destaque('item', imagem='Carta_Maquinista', titulo='CARTA DE TARÔ', nome='A Maquinista',
                         texto='Baratelli despertou os seus poderes!', tamanho=330)
              + flash([255, 220, 220, 255], 30)
              + [cmd(322, [BARATELLI, '$Baratelli_Cigana', 0, 'Baratelli', 0, ''])]
              + destaque('evento', personagem='$Baratelli_Cigana', titulo='NOVO VISUAL', nome='Baratelli, a Cigana',
                         texto='Chiquinhas, rabo de cavalo e vestido vermelho!')
              + move_pic(6, 288, 70, 0, 40, origin=0, w=True) + erase_pic(6)
              + tint([-20, -20, 10, 20], 40) + stop_bgs(2)
              + pose(-1, '')
              + bar('Eu me sinto... FORTE!')
              + bar('Agora eu sei onde está a Peruca', 'Dourada!')
              + switch(S_C3_RITUAL)
              + se('Crash') + flash([120, 255, 120, 200], 20) + shake(7, 9, 20)
              + script(set_self_js(M_VIDENTE, [PO], True)) + se('Teleport') + wait(20)
              + script(set_self_js(M_VIDENTE, [GU], True)) + se('Frog')
              + sapo('CROAC! Achou que ia se livrar de mim,', 'titia?!')
              + move(GU, [rc(37), rc(14, -4, -1), rc(38)], w=True)
              + script(set_self_js(M_VIDENTE, [PO], False))
              + pose(GU, 'soco', olhar=V, espera=6)
              + se('Slash3') + anim(V, 16, w=False) + flash([255, 60, 60, 200], 20) + shake(6, 9, 15) + pose(V, 'dor')
              + narr('Gusrola ataca a vidente com a língua!')
              + vid('Aaah...!', i=1)
              + move(V, [rc(35), rc(14, -1, 0), rc(36)], w=True)
              + sapo('Croac! Então a velha te deu poderes?', 'Que pena... vou acabar com os dois!')
              + luta)
    m.events[V]['pages'].append(page(ritual, image=img('$Vidente', 0, 2), sw1=S_C3_CASA))
    m.add_event('Ritual', 0, 12, [page(chegada, trigger=3, priority=0, sw1=S_C3_TOPO),
                                   page([], priority=0, sw1=S_C3_CASA)])
    m.add_event('Saída', 8, 12, [page(bar('Não vou embora agora!') + move(-1, [UP], w=True), trigger=1, priority=0)])


# ============================================================ banco de dados
def update_database():
    ts = load('Tilesets.json')
    for n in (8, 9, 10, 16, 17, 18, 24, 25, 26):
        ts[4]['flags'][D0 + n] = 0x600
    save('Tilesets.json', ts)
    B.TILESETS = ts

    a = load('Actors.json')
    a[1].update({'classId': CLS_CIGANA, 'equips': [0, 0, 0, 0, 0], 'initialLevel': 1, 'battlerName': ''})
    base = copy.deepcopy(a[5])
    a[5] = dict(base, id=5, name='Kevinho', nickname='O Amigo Fiel', classId=CLS_AMIGO, characterName='$Kevinho',
                characterIndex=0, faceName='Kevinho', faceIndex=0, battlerName='', equips=[0, 0, 0, 0, 0],
                initialLevel=1, maxLevel=99, traits=[], note='',
                profile='Amigo da Baratelli. Conhece todas\nas lendas da região.')
    save('Actors.json', a)

    c = load('Classes.json')
    while len(c) <= CLS_AMIGO:
        c.append(None)
    tpl = c[1]

    def mk_class(cid, name, p0, g, skills):
        params = [[int(p0[i] + g[i] * max(lv - 1, 0)) for lv in range(100)] for i in range(8)]
        traits = [t for t in tpl['traits'] if t['code'] in (22, 23)] + [{'code': 41, 'dataId': 2, 'value': 1}]
        return {'id': cid, 'expParams': [30, 20, 30, 30], 'traits': traits,
                'learnings': [{'level': 1, 'note': '', 'skillId': s} for s in skills],
                'name': name, 'note': '', 'params': params}
    c[CLS_CIGANA] = mk_class(CLS_CIGANA, 'Cigana Vingativa', [650, 120, 40, 30, 50, 40, 30, 30],
                             [30, 6, 3, 2, 4, 3, 2, 2], [SK3, SK3 + 1, SK3 + 2, SK3 + 3])
    c[CLS_AMIGO] = mk_class(CLS_AMIGO, 'Amigo Fiel', [1000, 60, 55, 40, 20, 30, 28, 20],
                            [40, 3, 4, 3, 1, 2, 2, 1], [SK3 + 4, SK3 + 5, SK3 + 6])
    save('Classes.json', c)

    s = load('Skills.json')
    while len(s) <= SK3 + 9:
        s.append(None)
    t = s[1]
    s[1]['damage'] = dict(s[1]['damage'], formula='Math.min(100, a.atk * 4 - b.def * 2)', critical=False, variance=0)

    def cap(sid, name, desc, icon, an, formula, scope, hit, mp, msg, effects=(), dtype=1):
        sk = mk_skill(t, sid, name, desc, icon, an, formula, dtype, scope, hit, mp, msg, effects)
        sk['damage']['variance'] = 0
        return sk
    s[SK3 + 0] = cap(SK3 + 0, 'Leitura de Mão', 'Lê o destino do inimigo... e o destino dói. (até 100)', 79, 96,
                     'Math.min(100, 40 + a.mat)', 1, 2, 4, '%1 lê a mão do inimigo!')
    s[SK3 + 1] = cap(SK3 + 1, 'Chuva de Signos', 'Os doze signos caem do céu. (até 100)', 79, 98,
                     'Math.min(100, 20 + a.mat)', 2, 2, 8, '%1 invoca a Chuva de Signos!')
    s[SK3 + 2] = cap(SK3 + 2, 'Carta da Maquinista', 'O poder da carta de tarô. (até 100)', 79, 117,
                     'Math.min(100, 60 + a.mat)', 1, 2, 12, '%1 tira a carta A Maquinista!')
    s[SK3 + 3] = cap(SK3 + 3, 'Cura Cigana', 'Recupera a vida de um aliado.', 72, 41,
                     'Math.min(300, 150 + a.mat * 2)', 7, 0, 10, '%1 usa a Cura Cigana!', dtype=3)
    s[SK3 + 4] = cap(SK3 + 4, 'Soco Amigo', 'Um soco de quem é parceiro. (até 100)', 77, 1,
                     'Math.min(100, 30 + a.atk)', 1, 1, 0, '%1 dá um Soco Amigo!')
    s[SK3 + 5] = cap(SK3 + 5, 'Voadora', 'Uma voadora de respeito. (até 100)', 77, 39,
                     'Math.min(100, 50 + a.atk)', 1, 1, 5, '%1 dá uma voadora!')
    s[SK3 + 6] = cap(SK3 + 6, 'Grito de Torcida', 'Aumenta o ataque do grupo.', 84, 51, '0', 8, 0, 6,
                     '%1 grita: VAI, BARATELLI!', [{'code': 31, 'dataId': 2, 'value1': 3, 'value2': 0}], dtype=0)
    s[SK3 + 7] = mk_skill(t, SK3 + 7, 'Linguada', '', 0, 16, '45 + a.atk - b.def', 1, 1, 1, 0, '%1 ataca com a língua!')
    s[SK3 + 8] = mk_skill(t, SK3 + 8, 'Coaxar Ensurdecedor', '', 0, 34, '30 + a.mat / 2 - b.mdf / 2', 1, 2, 2, 0,
                          '%1 solta um coaxar ensurdecedor!')
    s[SK3 + 9] = mk_skill(t, SK3 + 9, 'Gosma Venenosa', '', 0, 59, '20 + a.mat - b.mdf', 1, 1, 2, 0,
                          '%1 cospe uma gosma venenosa!', [{'code': 21, 'dataId': 4, 'value1': 0.5, 'value2': 0}])
    save('Skills.json', s)

    e = load('Enemies.json')
    while len(e) <= EN_SAPO:
        e.append(None)
    act = lambda sid, r: {'conditionParam1': 0, 'conditionParam2': 0, 'conditionType': 0, 'rating': r, 'skillId': sid}
    e[EN_SAPO] = {'id': EN_SAPO, 'actions': [act(SK3 + 7, 5), act(SK3 + 8, 4), act(SK3 + 9, 4)],
                  'battlerHue': 0, 'battlerName': 'Gusrola_Sapo',
                  'dropItems': [{'dataId': 1, 'denominator': 1, 'kind': 0} for _ in range(3)],
                  'exp': 300, 'gold': 0, 'name': 'Gusrola Sapo', 'note': '',
                  'params': [1000, 300, 50, 30, 45, 30, 28, 10],
                  'traits': [{'code': 22, 'dataId': 0, 'value': 0.95}, {'code': 22, 'dataId': 1, 'value': 0.05},
                             {'code': 31, 'dataId': 1, 'value': 0}]}
    save('Enemies.json', e)

    tr = load('Troops.json')
    while len(tr) <= TROOP_SAPO:
        tr.append(None)
    meio = {'conditions': {'actorHp': 50, 'actorId': 1, 'actorValid': False, 'enemyHp': 50, 'enemyIndex': 0,
                           'enemyValid': True, 'switchId': 1, 'switchValid': False, 'turnA': 0, 'turnB': 0,
                           'turnEnding': False, 'turnValid': False},
            'list': sapo('Croac... vocês são mais fortes do que', 'eu pensava!') + bar('É o poder da Maquinista!') + [END],
            'span': 0}
    tr[TROOP_SAPO] = {'id': TROOP_SAPO, 'members': [{'enemyId': EN_SAPO, 'x': 408, 'y': 430, 'hidden': False}],
                      'name': 'Gusrola Sapo', 'pages': [
                          tpage(sapo('Croac! Vou transformar vocês dois em', 'girinos!')
                                + kev('Vamos com tudo, Baratelli!'), turn=0),
                          meio]}
    save('Troops.json', tr)

    it = load('Items.json')
    while len(it) <= 32:
        it.append(None)
    cr = copy.deepcopy(it[31])
    cr.update({'id': 32, 'name': 'Crânio da Leandra', 'iconIndex': 1,
               'description': 'O crânio da vidente Leandra.\nBaratelli jurou vingança.'})
    it[32] = cr
    save('Items.json', it)

    sysd = load('System.json')
    for k, v in {S_C3_INICIO: 'Cap.3: abertura vista', S_C3_KEV: 'Cap.3: Kevinho no grupo',
                 S_C3_TOPO: 'Cap.3: chegou na vidente', S_C3_RITUAL: 'Cap.3: ritual feito',
                 S_C3_CASA: 'Cap.3: entrou na casa da vidente',
                 S_C3_FIM: 'Fim do Capítulo 3'}.items():
        sysd['switches'][k] = v
    sysd['terms']['messages'].update({'victory': '%1 foi vitoriosa!', 'obtainExp': 'Ganhou %1 de %2!',
                                      'levelUp': '%1 subiu para o %2 %3!'})
    BM.sistema(sysd)
    save('System.json', sysd)


def main():
    template = load('Map001.json')
    update_database()
    casa = build_casa_b(); events_casa_b(casa)
    morro = BM.construir(); njumps = BM.eventos(morro)
    vide = build_vidente(); events_vidente(vide)

    # ---- verificacoes de caminho (com pulos)
    c = casa.reach((7, 9))
    assert all((7, y) in c for y in range(5, 10)), 'casa da Baratelli'
    print('morro:', BM.verificar(morro))
    v = vide.reach((8, 11))
    assert (8, 5) in v and (8, 7) in v, 'casa da vidente'

    maps = [
        (M_CASA_B, casa, 'Casa da Baratelli', '', ''),
        (M_MORRO, morro, 'Morro do Macaco', 'Field3', 'Wind1'),
        (M_VIDENTE, vide, 'Casa da Vidente', '', ''),
    ]
    for mid, m, disp, bgmn, bgsn in maps:
        nota = f'<queda:{BM.CE_QUEDA}>' if mid == M_MORRO else ''
        j = map_json(template, m, disp, bgmn, bgsn, nota, bgm_vol=65, bgs_vol=45)
        j.update({'parallaxLoopX': False, 'parallaxLoopY': False, 'parallaxSx': 0, 'parallaxSy': 0})
        if mid == M_MORRO:
            j.update({'parallaxName': 'Clouds', 'parallaxLoopX': True, 'parallaxSx': 2, 'parallaxShow': True})
        if mid == M_VIDENTE:
            j.update({'specifyBattleback': True, 'battleback1Name': 'Wood2', 'battleback2Name': 'Tent'})
        save(f'Map{mid:03d}.json', j)

    mi = load('MapInfos.json')
    while len(mi) <= M_VIDENTE:
        mi.append(None)
    for o, (mid, name, parent) in enumerate([(M_CASA_B, 'Cap.3 - Casa da Baratelli', 0),
                                             (M_MORRO, 'Morro do Macaco', M_CASA_B),
                                             (M_VIDENTE, 'Casa da Vidente', M_MORRO)], 12):
        mi[mid] = {'id': mid, 'expanded': True, 'name': name, 'order': o, 'parentId': parent, 'scrollX': 0, 'scrollY': 0}
    save('MapInfos.json', mi)

    # o fim do Capitulo 2 agora segue para o Capitulo 3
    ce = load('CommonEvents.json')
    lst = ce[B2.CE_PONTE]['list']
    for i, cm in enumerate(lst):
        if cm['code'] == 354:
            lst[i:i + 1] = transfer(M_CASA_B, 7, 9, 8, fade=2)
            break
    BM.eventos_comuns(ce)
    save('CommonEvents.json', ce)
    pl = open(f'{PROJ}/js/plugins.js', encoding='utf-8').read()
    if '"Destaques"' not in pl:
        entry = '{"name":"Destaques","status":true,"description":"Mostra itens e eventos importantes com imagem, animação e transição.","parameters":{}}'
        pl = pl.replace('\n];', ',\n' + entry + '\n];')
        open(f'{PROJ}/js/plugins.js', 'w', encoding='utf-8', newline='\n').write(pl)
    print('ok: pulos', njumps, '| eventos', {disp: len(m.events) - 1 for _, m, disp, *_ in maps})


if __name__ == '__main__':
    main()
