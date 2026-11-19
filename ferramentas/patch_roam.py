# Libera a exploracao antes de tres cenas: casa do Gusrola (cap.1), casa da Baratelli e casa da vidente (cap.3).
# Tambem faz os novos membros do grupo aparecerem onde o personagem estava.
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(path, reps):
    path = os.path.join(HERE, path)
    src = open(path, encoding='utf-8').read()
    for a, b in reps:
        n = src.count(a)
        assert n == 1, (path, n, a[:90])
        src = src.replace(a, b)
    open(path, 'w', encoding='utf-8').write(src)
    print('patched', os.path.basename(path), len(reps))


patch('build_ch1.py', [
    ("    m.add_event('Conversa', 0, 9, [page(cena, trigger=3, priority=0, sw1=S_MONARK),\n"
     "                                   page([], priority=0, sw1=S_NOITE)])\n",
     "    # a cena comeca quando a Baratelli fala com o Gusrola (antes disso, a casa pode ser explorada)\n"
     "    m.events[gus]['pages'].insert(1, page(cena, image={'characterName': 'People1', 'characterIndex': 2, 'direction': 2},\n"
     "                                          sw1=S_MONARK))\n"
     "    chegada = (bar('Gusrola! Cheguei!')\n"
     "               + npc('Gusrola', 'Hehehe... entra, titia. Fica à vontade.', **G)\n"
     "               + narr('Explore a casa e fale com o Gusrola quando', 'quiser contar a novidade.')\n"
     "               + self_sw())\n"
     "    m.add_event('Conversa', 0, 9, [page(chegada, trigger=3, priority=0, sw1=S_MONARK),\n"
     "                                   page([], priority=0, self_switch='A')])\n"),
])

patch('build_ch2.py', [
    ("              + party_add(LEONA_ACTOR) + switch(S_LEONA)\n",
     "              + party_add(LEONA_ACTOR)\n"
     "              + script(f'$gamePlayer.followers().follower(0).locate($gameMap.event({leona}).x, $gameMap.event({leona}).y);')\n"
     "              + switch(S_LEONA)\n"),
])

patch('build_ch3.py', [
    ("S_C3_INICIO, S_C3_KEV, S_C3_TOPO, S_C3_RITUAL, S_C3_FIM = 15, 16, 17, 18, 19\n",
     "S_C3_INICIO, S_C3_KEV, S_C3_TOPO, S_C3_RITUAL, S_C3_FIM = 15, 16, 17, 18, 19\n"
     "S_C3_CASA = 20\n"),
    # casa da Baratelli: depois que o Kevinho entra, da pra andar pela casa e sair pela porta
    ("            + party_add(KEVINHO) + switch(S_C3_KEV)\n",
     "            + party_add(KEVINHO)\n"
     "            + script(f'$gamePlayer.followers().follower(0).locate($gameMap.event({kevinho}).x, $gameMap.event({kevinho}).y);')\n"
     "            + switch(S_C3_KEV)\n"),
    ("            + narr('O Morro do Macaco fica numa montanha a', 'leste de São Matheos.')\n"
     "            + fadeout() + switch(S_C3_INICIO)\n"
     "            + transfer(M_MORRO, 12, 27, 8, fade=2))\n"
     "    m.add_event('Abertura', 0, 10, [page(cena, trigger=3, priority=0), page([], priority=0, sw1=S_C3_INICIO)])\n",
     "            + narr('O Morro do Macaco fica numa montanha a', 'leste de São Matheos.')\n"
     "            + switch(S_C3_INICIO)\n"
     "            + narr('Quando estiver pronta, saia pela porta para', 'ir ao Morro do Macaco.'))\n"
     "    m.add_event('Abertura', 0, 10, [page(cena, trigger=3, priority=0), page([], priority=0, sw1=S_C3_INICIO)])\n"
     "    m.add_event('Saída', 7, 10, [page([], priority=0),\n"
     "                                 page(se('Door1') + transfer(M_MORRO, 12, 27, 8, fade=0), trigger=1, priority=0,\n"
     "                                      sw1=S_C3_INICIO)])\n"),
    # casa da vidente: chegada curta, exploracao livre e o ritual comeca ao falar com ela
    ("    ritual = (wait(20) + bgm('Scene6', vol=65)\n"
     "              + narr('Velas, estrelas pintadas no teto e um', 'cheiro forte de incenso...')\n"
     "              + balloon(V, 1)\n"
     "              + vid('Visitantes? Aqui no alto do morro?')\n"
     "              + move(-1, [UP, UP, UP, UP, UP, UP], w=True)\n",
     "    chegada = (wait(20) + bgm('Scene6', vol=65)\n"
     "               + narr('Velas, estrelas pintadas no teto e um', 'cheiro forte de incenso...')\n"
     "               + balloon(V, 1)\n"
     "               + vid('Visitantes? Aqui no alto do morro?')\n"
     "               + vid('Fiquem à vontade... só não mexam no', 'meu incenso.')\n"
     "               + kev('É ela! A vidente da lenda!', 'Vai lá falar com ela, Baratelli.')\n"
     "               + switch(S_C3_CASA))\n"
     "    ritual = (fadeout()\n"
     "              + script('$gamePlayer.locate(8, 5); $gamePlayer.setDirection(8);\\n'\n"
     "                       '$gamePlayer.followers().synchronize(8, 6, 8);')\n"
     "              + fadein()\n"),
    ("    m.add_event('Ritual', 0, 12, [page(ritual, trigger=3, priority=0, sw1=S_C3_TOPO),\n"
     "                                   page([], priority=0, sw1=S_C3_RITUAL)])\n",
     "    m.events[V]['pages'].append(page(ritual, image=img('$Vidente', 0, 2), sw1=S_C3_CASA))\n"
     "    m.add_event('Ritual', 0, 12, [page(chegada, trigger=3, priority=0, sw1=S_C3_TOPO),\n"
     "                                   page([], priority=0, sw1=S_C3_CASA)])\n"),
    ("                 S_C3_TOPO: 'Cap.3: chegou na vidente', S_C3_RITUAL: 'Cap.3: ritual feito',\n",
     "                 S_C3_TOPO: 'Cap.3: chegou na vidente', S_C3_RITUAL: 'Cap.3: ritual feito',\n"
     "                 S_C3_CASA: 'Cap.3: entrou na casa da vidente',\n"),
])
