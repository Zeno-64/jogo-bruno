# Troca as aparicoes de itens/eventos dos capitulos 2 e 3 pelo plugin Destaques.
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(path, reps):
    path = os.path.join(HERE, path)
    src = open(path, encoding='utf-8').read()
    for a, b in reps:
        n = src.count(a)
        assert n == 1, (path, n, a[:80])
        src = src.replace(a, b)
    open(path, 'w', encoding='utf-8').write(src)
    print('patched', path, len(reps))


BS = '\\'

patch('build_ch2.py', [
    ("import build_ch1 as B\n", "import build_ch1 as B\nfrom fx import destaque, capitulo, move_pic_e\n"),
    ("             + pic(1, 'Capitulo2', 408, 312) + fadein() + wait(150) + fadeout() + erase_pic(1)\n",
     "             + capitulo('Capitulo2')\n"),
    ("    lst = (se('Coin') + [cmd(122, [V_ESMOLAS, V_ESMOLAS, 1, 0, 1])]\n"
     "           + narr('Esmolas: " + BS + BS + "V[4] de 5')\n",
     "    lst = ([cmd(122, [V_ESMOLAS, V_ESMOLAS, 1, 0, 1])]\n"
     "           + destaque('moeda', imagem='Item_Esmola', nome='+1 esmola!', texto='Esmolas: " + BS + BS + "V[4] de 5')\n"),
    ("              + party_add(LEONA_ACTOR) + switch(S_LEONA)\n"
     "              + me('Item')\n"
     "              + narr('Leona entrou para o grupo!')\n",
     "              + party_add(LEONA_ACTOR) + switch(S_LEONA)\n"
     "              + destaque('membro', rosto='Leona', indice=0, nome='Leona',\n"
     "                         texto='A Arrogante. Se acha melhor que todo mundo.')\n"),
    ("             + me('Item') + item(IT_GRAMPO, 1)\n"
     "             + narr('Leandra encontrou um Grampo de cabelo!')\n",
     "             + item(IT_GRAMPO, 1)\n"
     "             + destaque('item', imagem='Item_Grampo', nome='Grampo de cabelo',\n"
     "                        texto='Enferrujado, mas dá pra abrir fechaduras.')\n"),
    ("    certo = (se('Chime2') + narr('SENHA CORRETA. ACESSO LIBERADO.')\n",
     "    certo = (destaque('evento', imagem='Evento_Cadeado', titulo='ACESSO LIBERADO', nome='Senha correta: HAIR',\n"
     "                      texto='A porta do meio foi destravada.')\n"),
    ("        lst = pic(10, f'Papel_{letter}', 408, 222, opacity=0) + se('Book1') + move_pic(10, 408, 222, 255, 15, w=True)\n"
     "        for t in texts:\n"
     "            lst += narr(*t)\n"
     "        lst += move_pic(10, 408, 222, 0, 15, w=True) + erase_pic(10)\n",
     "        pos = 'HAIR'.index(letter) + 1\n"
     "        lst = (pic(10, f'Papel_{letter}', 470, 236, opacity=0, scale=90) + se('Book1')\n"
     "               + move_pic_e(10, 408, 222, 255, 24, scale=100, easing=2, w=True))\n"
     "        for t in texts:\n"
     "            lst += narr(*t)\n"
     "        lst += (move_pic_e(10, 360, 210, 0, 18, scale=94, easing=1, w=True) + erase_pic(10)\n"
     "                + destaque('aviso', imagem=f'Papel_{letter}', nome=f'Pista: letra {letter}',\n"
     "                           texto=f'Letra {pos} de 4 da senha'))\n"),
    ("           + move(LE, [rc(41, '$Leona_Cavalo', 0)], w=True)\n"
     "           + se('Horse')\n",
     "           + move(LE, [rc(41, '$Leona_Cavalo', 0)], w=True)\n"
     "           + se('Horse')\n"
     "           + destaque('evento', rosto='Leona', indice=3, titulo='TRANSFORMAÇÃO', nome='Leona Umamusume',\n"
     "                      texto='Orelhas, cauda... e muita velocidade.')\n"),
    ("           + narr('Raulete coloca o cabelo de Leandra na', 'própria cabeça careca...')\n",
     "           + narr('Raulete coloca o cabelo de Leandra na', 'própria cabeça careca...')\n"
     "           + destaque('evento', rosto='Raulete', indice=1, titulo='CABELO ROUBADO', nome='Raulete de peruca loira',\n"
     "                      texto='Os cabelos dourados da Leandra.')\n"),
    ("           + se('Saint3') + pic(7, 'Peruca_Ouro', 408, 230, opacity=0, scale=70)\n"
     "           + move_pic(7, 408, 210, 255, 50, scale=100, w=True)\n"
     "           + rau('Agora, finalmente... poderemos farejar', 'a PERUCA DE OURO!', i=1)\n"
     "           + move_pic(7, 408, 190, 0, 40, scale=110, w=True) + erase_pic(7)\n",
     "           + rau('Agora, finalmente... poderemos farejar', 'a PERUCA DE OURO!', i=1)\n"
     "           + destaque('evento', imagem='Peruca_Ouro', titulo='O ALVO DOS RAULETE', nome='Peruca de Ouro',\n"
     "                      texto='Com o faro da Leona, a caçada começou.')\n"),
    ("           + pic(8, 'FimCapitulo2', 408, 312) + fadein()\n"
     "           + wait(300) + fadeout() + erase_pic(8)\n",
     "           + capitulo('FimCapitulo2')\n"),
])

patch('build_ch3.py', [
    ("import build_ch2 as B2\n", "import build_ch2 as B2\nfrom fx import destaque, capitulo, move_pic_e\n"),
    ("            + pic(1, 'Capitulo3', 408, 312) + fadein() + wait(150) + fadeout() + erase_pic(1)\n",
     "            + capitulo('Capitulo3')\n"),
    ("            + narr('Gusrola se transforma em um sapo', 'humanoide!')\n",
     "            + narr('Gusrola se transforma em um sapo', 'humanoide!')\n"
     "            + destaque('evento', rosto='Gusrola_Sapo', titulo='FORMA VERDADEIRA', nome='Gusrola Sapo',\n"
     "                       texto='O sobrinho era um sapo o tempo todo!')\n"),
    ("            + party_add(KEVINHO) + switch(S_C3_KEV)\n"
     "            + me('Item')\n"
     "            + narr('Kevinho entrou para o grupo!')\n",
     "            + party_add(KEVINHO) + switch(S_C3_KEV)\n"
     "            + destaque('membro', rosto='Kevinho', nome='Kevinho',\n"
     "                       texto='O Amigo Fiel. Conhece todas as lendas da região.')\n"),
    ("             + item(7, 3) + me('Item') + narr('Dentro do baú: 3 Poções!'), image=img('!Chest', 0, 2, 0)),\n",
     "             + item(7, 3) + destaque('item', imagem='Item_Pocao', nome='Poção x3',\n"
     "                                     texto='Cada uma recupera 500 de vida.'), image=img('!Chest', 0, 2, 0)),\n"),
    ("              + me('Fanfare2')\n"
     "              + pic(7, 'Carta_Maquinista', 408, 320, opacity=0, scale=50)\n"
     "              + move_pic(7, 408, 300, 255, 40, scale=80, w=True)\n"
     "              + wait(100)\n"
     "              + move_pic(7, 408, 205, 255, 30, scale=56, w=True)\n"
     "              + narr('Baratelli ganhou a carta de tarô:', 'A MAQUINISTA!')\n"
     "              + move_pic(7, 408, 180, 0, 30, scale=60, w=True) + erase_pic(7)\n",
     "              + destaque('item', imagem='Carta_Maquinista', titulo='CARTA DE TARÔ', nome='A Maquinista',\n"
     "                         texto='Baratelli despertou os seus poderes!', tamanho=330)\n"),
    ("              + narr('A aparência de Baratelli muda: rabo de', 'cavalo, chiquinhas e um vestido vermelho!')\n",
     "              + destaque('evento', personagem='$Baratelli_Cigana', titulo='NOVO VISUAL', nome='Baratelli, a Cigana',\n"
     "                         texto='Chiquinhas, rabo de cavalo e vestido vermelho!')\n"),
    ("        + se('Item3')\n"
     "        + narr('Baratelli pega o crânio de Leandra.')\n",
     "        + narr('Baratelli pega o crânio de Leandra.')\n"
     "        + item(32, 1) + destaque('item', imagem='Item_Cranio', titulo='ITEM IMPORTANTE', nome='Crânio da Leandra',\n"
     "                                 texto='Uma promessa de vingança.')\n"),
    ("        + pic(9, 'Final_Cap3', 408, 312) + bgm('Scene8', vol=60) + fadein()\n",
     "        + pic(9, 'Final_Cap3', 408, 312) + move_pic_e(9, 408, 300, 255, 600, scale=110, easing=0)\n"
     "        + bgm('Scene8', vol=60) + fadein()\n"),
    ("        + pic(8, 'FimCapitulo3', 408, 312) + fadein() + wait(300) + fadeout() + erase_pic(8)\n",
     "        + capitulo('FimCapitulo3')\n"),
    ("    save('Troops.json', tr)\n",
     "    save('Troops.json', tr)\n\n"
     "    it = load('Items.json')\n"
     "    while len(it) <= 32:\n"
     "        it.append(None)\n"
     "    cr = copy.deepcopy(it[31])\n"
     "    cr.update({'id': 32, 'name': 'Crânio da Leandra', 'iconIndex': 1,\n"
     "               'description': 'O crânio da vidente Leandra." + BS + "nBaratelli jurou vingança.'})\n"
     "    it[32] = cr\n"
     "    save('Items.json', it)\n"),
    ("    print('ok: pulos', njumps,",
     "    pl = open(f'{PROJ}/js/plugins.js', encoding='utf-8').read()\n"
     "    if '\"Destaques\"' not in pl:\n"
     "        entry = '{\"name\":\"Destaques\",\"status\":true,\"description\":\"Mostra itens e eventos importantes com imagem, animação e transição.\",\"parameters\":{}}'\n"
     "        pl = pl.replace('" + BS + "n];', '," + BS + "n' + entry + '" + BS + "n];')\n"
     "        open(f'{PROJ}/js/plugins.js', 'w', encoding='utf-8', newline='" + BS + "n').write(pl)\n"
     "    print('ok: pulos', njumps,"),
])
