# Coloca as poses de acao (chute, soco, dor, queda, choro...) nas cenas dos 3 capitulos e nas interacoes dos cenarios.
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(path, reps):
    full = os.path.join(HERE, path)
    src = open(full, encoding='utf-8').read()
    for a, b in reps:
        n = src.count(a)
        assert n == 1, (path, n, a[:90])
        src = src.replace(a, b)
    open(full, 'w', encoding='utf-8').write(src)
    print('patched', path, len(reps))


I12 = ' ' * 12
I14 = ' ' * 14
I13 = ' ' * 13
I11 = ' ' * 11
I8 = ' ' * 8

# ------------------------------------------------------------------ Capitulo 1
patch('build_ch1.py', [
    ("from fx import destaque, capitulo\n", "from fx import destaque, capitulo, pose\n"),
    (I12 + "+ se('Blow1') + shake(5, 8, 12)\n",
     I12 + "+ se('Blow1') + shake(5, 8, 12) + pose(-1, 'dor')\n"),
    (I12 + "+ se('Blow3') + shake(7, 9, 15)\n"
     + I12 + "+ move(-1, [rc(35), rc(14, -1, 0), rc(36)], w=True)\n"
     + I12 + "+ balloon(-1, 6)\n"
     + I12 + "+ bar('M-me desculpa... por favor...')\n"
     + I12 + "+ se('Cry1', vol=70)\n",
     I12 + "+ pose(monark, 'soco', olhar=-1, espera=8)\n"
     + I12 + "+ se('Blow3') + shake(7, 9, 15) + pose(-1, 'dor')\n"
     + I12 + "+ move(-1, [rc(35), rc(14, -1, 0), rc(36)], w=True)\n"
     + I12 + "+ pose(-1, 'queda', segurar=True)\n"
     + I12 + "+ balloon(-1, 6)\n"
     + I12 + "+ bar('M-me desculpa... por favor...')\n"
     + I12 + "+ se('Cry1', vol=70) + pose(-1, 'choro', repetir=True, segurar=True)\n"),
    (I12 + "+ npc('Monark', 'Lá eu te ensino as artes de ler o', 'futuro. Hahaha!')\n",
     I12 + "+ pose(monark, 'riso', repetir=True, segurar=True)\n"
     + I12 + "+ npc('Monark', 'Lá eu te ensino as artes de ler o', 'futuro. Hahaha!')\n"
     + I12 + "+ pose(monark, '')\n"),
    (I12 + "+ switch(S_MONARK)\n" + I12 + "+ wait(30)\n",
     I12 + "+ switch(S_MONARK) + pose(-1, '')\n" + I12 + "+ wait(30)\n"),
    (I12 + "+ bar('Aaaah, que felicidade! Hihihi!')\n",
     I12 + "+ pose(-1, 'riso', espera=10)\n" + I12 + "+ bar('Aaaah, que felicidade! Hihihi!')\n"),
    (I11 + "+ bar('Aaai! Um rato me mordeu!')\n",
     I11 + "+ pose(-1, 'dor')\n" + I11 + "+ bar('Aaai! Um rato me mordeu!')\n"),
    (I14 + "+ bar('AAAAAI! Que dor!!')\n",
     I14 + "+ pose(-1, 'dor', segurar=True)\n" + I14 + "+ bar('AAAAAI! Que dor!!')\n"),
    (I14 + "+ narr('Uma flor começou a brotar da cabeça', 'de Baratelli!')\n",
     I14 + "+ pose(-1, '')\n" + I14 + "+ narr('Uma flor começou a brotar da cabeça', 'de Baratelli!')\n"),
    (I14 + "+ npc(MK, 'Hahahaha! Caiu direitinho!')\n",
     I14 + "+ pose(monark_eid, 'riso', repetir=True, segurar=True)\n"
     + I14 + "+ npc(MK, 'Hahahaha! Caiu direitinho!')\n" + I14 + "+ pose(monark_eid, '')\n"),
    (I14 + "+ npc(MK, 'Mande lembranças ao Fuhrer Raulete!', 'Hahahaha!')\n",
     I14 + "+ pose(monark_eid, 'riso', repetir=True, segurar=True)\n"
     + I14 + "+ npc(MK, 'Mande lembranças ao Fuhrer Raulete!', 'Hahahaha!')\n" + I14 + "+ pose(monark_eid, '')\n"),
    (I14 + "+ bar('Snif... snif...', 'Ele me enganou...')\n",
     I14 + "+ pose(-1, 'choro', repetir=True, segurar=True)\n" + I14 + "+ bar('Snif... snif...', 'Ele me enganou...')\n"),
    (I14 + "+ bar('Nunca mais vou cair na conversa', 'de ninguém!')\n",
     I14 + "+ pose(-1, '')\n" + I14 + "+ bar('Nunca mais vou cair na conversa', 'de ninguém!')\n"),
    (I14 + "+ bar('Eu vou encontrar a grande', 'PERUCA DOURADA!')\n",
     I14 + "+ pose(-1, 'magia', repetir=True, segurar=True)\n"
     + I14 + "+ bar('Eu vou encontrar a grande', 'PERUCA DOURADA!')\n" + I14 + "+ pose(-1, '')\n"),
])

# ------------------------------------------------------------------ Capitulo 2
patch('build_ch2.py', [
    ("from fx import destaque, capitulo, move_pic_e\n", "from fx import destaque, capitulo, move_pic_e, pose\n"),
    (I13 + "+ move(-1, [rc(19)], w=True)\n"
     + I13 + "+ se('Blow3') + flash([255, 255, 255, 255], 20) + shake(7, 9, 15)\n"
     + I13 + "+ lea('Ai...!', i=1)\n",
     I13 + "+ move(-1, [rc(19)], w=True)\n"
     + I13 + "+ pose(men[0], 'soco', olhar=-1, espera=8)\n"
     + I13 + "+ se('Blow3') + flash([255, 255, 255, 255], 20) + shake(7, 9, 15) + pose(-1, 'dor', espera=20)\n"
     + I13 + "+ pose(-1, 'queda', segurar=True)\n"
     + I13 + "+ lea('Ai...!', i=1)\n"),
    ("    acorda = (bgs('Drips', 45) + wait(60)\n",
     "    acorda = (pose(-1, 'queda', segurar=True) + bgs('Drips', 45) + wait(60)\n"),
    (I14 + "+ leo('Finalmente acordou, loirinha.')\n",
     I14 + "+ leo('Finalmente acordou, loirinha.')\n" + I14 + "+ pose(-1, '') + move(-1, [rc(14, 0, 0)], w=True)\n"),
    (I14 + "+ leo('Achei que você tinha morrido igual', 'àquele ali.')\n",
     I14 + "+ pose(leona, 'riso', espera=6)\n" + I14 + "+ leo('Achei que você tinha morrido igual', 'àquele ali.')\n"),
    (I14 + "+ lea('UM ESQUELETO?!', i=1)\n",
     I14 + "+ move(-1, [rc(14, 0, 0)], w=False)\n" + I14 + "+ lea('UM ESQUELETO?!', i=1)\n"),
    (I11 + "+ narr('Leandra e Leona caem de joelhos, sem', 'forças para continuar.')\n",
     I11 + "+ pose(-1, 'cansado', repetir=True, segurar=True) + pose(LE, 'cansado', repetir=True, segurar=True)\n"
     + I11 + "+ narr('Leandra e Leona caem de joelhos, sem', 'forças para continuar.')\n"),
    (I11 + "+ leo('O que eu preciso fazer para virar', 'uma Umamusume?', i=2)\n",
     I11 + "+ pose(LE, '')\n" + I11 + "+ leo('O que eu preciso fazer para virar', 'uma Umamusume?', i=2)\n"),
    (I11 + "+ lea('L-Leona...? A gente ia fugir', 'juntas...', i=1)\n",
     I11 + "+ pose(-1, '')\n" + I11 + "+ lea('L-Leona...? A gente ia fugir', 'juntas...', i=1)\n"),
    (I11 + "+ se('Slash1') + move(LE, [rc(14, 0, 0)], w=False) + move(RA, [rc(14, 0, 0)], w=False)\n",
     I11 + "+ pose(LE, 'facada', segurar=True) + pose(RA, 'soco', olhar=-1)\n"
     + I11 + "+ se('Slash1') + pose(-1, 'dor', segurar=True)\n"),
    (I11 + "+ move(-1, [rc(37), rc(35), rc(14, 1, 0)], w=True)\n",
     I11 + "+ pose(-1, 'queda', segurar=True) + pose(LE, '')\n"
     + I11 + "+ move(-1, [rc(37), rc(35), rc(14, 1, 0)], w=True)\n"),
    (I11 + "+ se('Magic7') + anim(LE, 117, w=False)",
     I11 + "+ pose(LE, 'magia', repetir=True, segurar=True)\n" + I11 + "+ se('Magic7') + anim(LE, 117, w=False)"),
    (I11 + "+ move(LE, [rc(41, '$Leona_Cavalo', 0)], w=True)\n",
     I11 + "+ move(LE, [rc(41, '$Leona_Cavalo', 0)], w=True) + pose(LE, '')\n"),
    (I11 + "+ leo('Eu me sinto tão... RÁPIDA!', i=3)\n",
     I11 + "+ move(LE, [rc(14, 0, 0)], w=False)\n" + I11 + "+ leo('Eu me sinto tão... RÁPIDA!', i=3)\n"),
    (I11 + "+ rau('HAHAHAHAHA!', i=1)\n",
     I11 + "+ pose(RA, 'riso', repetir=True, segurar=True)\n" + I11 + "+ rau('HAHAHAHAHA!', i=1)\n"),
    (I11 + "+ switch(S_FIM2)\n", I11 + "+ pose(RA, '')\n" + I11 + "+ switch(S_FIM2)\n"),
])

# ------------------------------------------------------------------ Capitulo 3
patch('build_ch3.py', [
    ("from fx import destaque, capitulo, move_pic_e\n", "from fx import destaque, capitulo, move_pic_e, pose\n"),
    ('"$gamePlayer.setMoveSpeed(4); $gamePlayer.showFollowers(); $gamePlayer.refresh();")',
     '"$gamePlayer.setMoveSpeed(4); $gamePlayer.showFollowers(); $gamePlayer.refresh(); $gamePlayer.pose(\'\');")'),
    (I12 + "+ se('Blow1') + move(-1, [rc(35), rc(14, 0, 1), rc(36), rc(29, 4)], w=True) + shake(5, 9, 15)\n",
     I12 + "+ se('Blow1') + pose(-1, 'queda', segurar=True)\n"
     + I12 + "+ move(-1, [rc(35), rc(14, 0, 1), rc(36), rc(29, 4)], w=True) + shake(5, 9, 15)\n"),
    (I12 + "+ gus('Hahahaha! Olha só a titia!')\n",
     I12 + "+ pose(monark, 'riso', repetir=True, segurar=True) + pose(gusrola, 'riso', repetir=True, segurar=True)\n"
     + I12 + "+ gus('Hahahaha! Olha só a titia!')\n"),
    (I12 + "+ bar('P-por quê, Gusrola...?')\n",
     I12 + "+ pose(-1, '') + pose(monark, '') + pose(gusrola, '')\n" + I12 + "+ bar('P-por quê, Gusrola...?')\n"),
    (I12 + "+ mk('E você caiu direitinho. Hahahaha!')\n",
     I12 + "+ pose(monark, 'riso', espera=4)\n" + I12 + "+ mk('E você caiu direitinho. Hahahaha!')\n"),
    (I12 + "+ se('Darkness2') + anim(gusrola, 101, w=False)",
     I12 + "+ pose(gusrola, 'magia', repetir=True, segurar=True)\n" + I12 + "+ se('Darkness2') + anim(gusrola, 101, w=False)"),
    (I12 + "+ move(gusrola, [rc(41, '$Gusrola_Sapo', 0)], w=True) + se('Frog')\n",
     I12 + "+ move(gusrola, [rc(41, '$Gusrola_Sapo', 0)], w=True) + se('Frog') + pose(gusrola, '')\n"),
    (I12 + "+ sapo('Croac! Croac! Hahahaha!')\n",
     I12 + "+ pose(gusrola, 'riso', espera=4)\n" + I12 + "+ sapo('Croac! Croac! Hahahaha!')\n"),
    (I12 + "+ bar('Snif... snif...')\n",
     I12 + "+ pose(-1, 'choro', repetir=True, segurar=True)\n" + I12 + "+ bar('Snif... snif...')\n"),
    (I12 + "+ se('Door1') + script(set_self_js(M_CASA_B, [kevinho], True))\n",
     I12 + "+ pose(-1, '')\n" + I12 + "+ se('Door1') + script(set_self_js(M_CASA_B, [kevinho], True))\n"),
    (I14 + "+ vid('OSSOS DA LUA, ESTRELAS DO DESTINO...', 'VENHAM TRABALHAR!')\n",
     I14 + "+ pose(-1, 'magia', repetir=True, segurar=True)\n"
     + I14 + "+ vid('OSSOS DA LUA, ESTRELAS DO DESTINO...', 'VENHAM TRABALHAR!')\n"),
    (I14 + "+ bar('Eu me sinto... FORTE!')\n", I14 + "+ pose(-1, '')\n" + I14 + "+ bar('Eu me sinto... FORTE!')\n"),
    (I14 + "+ se('Slash3') + anim(V, 16, w=False) + flash([255, 60, 60, 200], 20) + shake(6, 9, 15)\n",
     I14 + "+ pose(GU, 'soco', olhar=V, espera=6)\n"
     + I14 + "+ se('Slash3') + anim(V, 16, w=False) + flash([255, 60, 60, 200], 20) + shake(6, 9, 15) + pose(V, 'dor')\n"),
    # luta encenada
    (I8 + "+ se('Blow3') + anim(GU, 1, w=False) + shake(6, 9, 12)\n",
     I8 + "+ pose(KE, 'chute', olhar=GU, espera=8)\n"
     + I8 + "+ se('Blow3') + anim(GU, 1, w=False) + shake(6, 9, 12) + pose(GU, 'dor', olhar=KE)\n"),
    (I8 + "+ se('Fire1') + anim(GU, 66, w=True)\n",
     I8 + "+ pose(-1, 'magia', olhar=GU, espera=10)\n" + I8 + "+ se('Fire1') + pose(GU, 'dor') + anim(GU, 66, w=True)\n"),
    (I8 + "+ se('Darkness2') + anim(-1, 101, w=False) + flash([120, 0, 160, 160], 20) + shake(5, 9, 10)\n",
     I8 + "+ pose(GU, 'soco', olhar=-1, espera=6)\n"
     + I8 + "+ se('Darkness2') + anim(-1, 101, w=False) + flash([120, 0, 160, 160], 20) + shake(5, 9, 10) + pose(-1, 'dor')\n"),
    (I8 + "+ se('Blow5') + anim(GU, 39, w=False) + shake(6, 9, 10)\n",
     I8 + "+ pose(KE, 'soco', olhar=GU, espera=6)\n"
     + I8 + "+ se('Blow5') + anim(GU, 39, w=False) + shake(6, 9, 10) + pose(GU, 'dor')\n"),
    (I8 + "+ se('Slash1') + anim(KE, 16, w=True)\n",
     I8 + "+ pose(GU, 'chute', olhar=KE, espera=6)\n" + I8 + "+ se('Slash1') + pose(KE, 'dor') + anim(KE, 16, w=True)\n"),
    (I8 + "+ se('Ice1') + anim(GU, 71, w=True)\n",
     I8 + "+ pose(-1, 'magia', olhar=GU, espera=8)\n" + I8 + "+ se('Ice1') + pose(GU, 'dor') + anim(GU, 71, w=True)\n"),
    (I8 + "+ se('Thunder3') + anim(GU, 76, w=False) + flash([255, 255, 160, 200], 20) + shake(8, 9, 20)\n",
     I8 + "+ pose(-1, 'magia', espera=4)\n"
     + I8 + "+ se('Thunder3') + anim(GU, 76, w=False) + flash([255, 255, 160, 200], 20) + shake(8, 9, 20) + pose(GU, 'dor')\n"),
    (I8 + "+ se('Water1') + anim(-1, 81, w=False) + anim(KE, 81, w=True)\n",
     I8 + "+ pose(GU, 'magia', espera=8)\n"
     + I8 + "+ se('Water1') + pose(-1, 'dor') + pose(KE, 'dor') + anim(-1, 81, w=False) + anim(KE, 81, w=True)\n"),
    (I8 + "+ move(GU, [rc(14, -1, 0)], w=False) + move(KE, [rc(14, 1, 0)], w=True)\n",
     I8 + "+ move(GU, [rc(14, -1, 0)], w=False) + move(KE, [rc(14, 1, 0)], w=True)\n"
     + I8 + "+ pose(GU, 'chute', olhar=KE) + pose(KE, 'chute', olhar=GU, espera=6)\n"),
    (I8 + "+ se('Breath')\n",
     I8 + "+ se('Breath')\n"
     + I8 + "+ pose(-1, 'cansado', repetir=True, segurar=True) + pose(KE, 'cansado', repetir=True, segurar=True)\n"
     + I8 + "+ pose(GU, 'cansado', repetir=True, segurar=True)\n"),
    (I8 + "+ narr('Derrotado, Gusrola volta à forma humana.')\n",
     I8 + "+ pose(-1, '') + pose(KE, '') + pose(GU, '')\n" + I8 + "+ narr('Derrotado, Gusrola volta à forma humana.')\n"),
    (I8 + "+ gus('Titia... me perdoa...', 'Eu me arrependo de tudo...')\n",
     I8 + "+ pose(GU, 'choro', repetir=True, segurar=True)\n" + I8 + "+ gus('Titia... me perdoa...', 'Eu me arrependo de tudo...')\n"),
    (I8 + "+ se('Saint7') + anim(GU, 100, w=False) + flash([255, 240, 200, 220], 40)\n",
     I8 + "+ pose(-1, 'magia', olhar=GU, segurar=True)\n"
     + I8 + "+ se('Saint7') + anim(GU, 100, w=False) + flash([255, 240, 200, 220], 40) + pose(GU, 'dor', segurar=True)\n"),
    (I8 + "+ se('Collapse4')\n", I8 + "+ pose(-1, '')\n" + I8 + "+ se('Collapse4')\n"),
    (I8 + "+ move(V, [rc(29, 1), rc(10)], w=True)\n",
     I8 + "+ pose(V, 'rastejar', repetir=True, segurar=True, velocidade=10)\n" + I8 + "+ move(V, [rc(29, 1), rc(10)], w=True)\n"),
    (I8 + "+ bar('Leandra...!')\n", I8 + "+ pose(-1, 'choro', repetir=True, segurar=True)\n" + I8 + "+ bar('Leandra...!')\n"),
    (I8 + "+ bar('Leandra... eu juro que vou te vingar.')\n",
     I8 + "+ pose(-1, '')\n" + I8 + "+ bar('Leandra... eu juro que vou te vingar.')\n"),
])

# ------------------------------------------------------------------ cenarios
patch('build_env.py', [
    ("from fx import destaque\n", "from fx import destaque, pose\n"),
    ("    chute = (N('Baratelli chuta o coqueiro com toda a força!')\n",
     "    chute = (pose(-1, 'chute', espera=12) + N('Baratelli chuta o coqueiro com toda a força!')\n"),
    ("             + N('TOC! Um coco cai bem na cabeça dela!') + balloon(-1, 6)\n",
     "             + pose(-1, 'dor') + N('TOC! Um coco cai bem na cabeça dela!') + balloon(-1, 6)\n"),
    ("        se('Damage1') + shake(4, 9, 8) + N('Um caranguejo",
     "        se('Damage1') + pose(-1, 'dor') + shake(4, 9, 8) + N('Um caranguejo"),
    ("    chutar = (N('Leandra dá um chute na máquina!') + se('Blow3')",
     "    chutar = (pose(-1, 'chute', espera=10) + N('Leandra dá um chute na máquina!') + se('Blow3')"),
    ("    sacudir = (N('Baratelli sacode a árvore com força!') + se('Wind4')",
     "    sacudir = (pose(-1, 'soco', espera=8) + N('Baratelli sacode a árvore com força!') + se('Wind4')"),
    ("              + choices([('Apertar', se('Siren')",
     "              + choices([('Apertar', pose(-1, 'soco', espera=8) + se('Siren')"),
])
