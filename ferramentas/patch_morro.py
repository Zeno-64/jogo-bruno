# Troca o Morro do Macaco antigo pelo novo (build_morro.py) no montador do Capitulo 3
# e ajusta o cenario interativo (build_env.py) para as coordenadas novas.
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def abrir(nome):
    return open(os.path.join(HERE, nome), encoding='utf-8').read()


def gravar(nome, s):
    open(os.path.join(HERE, nome), 'w', encoding='utf-8').write(s)


def troca(s, velho, novo):
    assert s.count(velho) == 1, velho[:70]
    return s.replace(velho, novo)


# ------------------------------------------------------------------ build_ch3.py
s = abrir('build_ch3.py')
s = troca(s, "import build_ch2 as B2\n", "import build_ch2 as B2\nimport build_morro as BM\n")
s = troca(s, "transfer(M_MORRO, 12, 27, 8, fade=0)", "transfer(M_MORRO, BM.INICIO[0], BM.INICIO[1], 8, fade=0)")

# remove o morro antigo (ilhas, labirinto, pulos e eventos)
ini = s.index("# ============================================================ 13. MORRO DO MACACO")
fim = s.index("# ============================================================ 14. CASA DA VIDENTE")
s = s[:ini] + ("# ============================================================ 13. MORRO DO MACACO\n"
               "# Fica em build_morro.py (Rei Macaco, bananas douradas, cascas, pedras frageis e cocos).\n\n\n") + s[fim:]

s = troca(s, "    morro = build_morro(); njumps = events_morro(morro)\n",
          "    morro = BM.construir(); njumps = BM.eventos(morro)\n")

# verificacao antiga do morro -> verificacao nova
ini = s.index("    jumps = {}\n    for ev in morro.events[1:]:")
fim = s.index("    v = vide.reach((8, 11))")
s = s[:ini] + "    print('morro:', BM.verificar(morro))\n" + s[fim:]

s = troca(s, "        j = map_json(template, m, disp, bgmn, bgsn, '', bgm_vol=65, bgs_vol=45)\n",
          "        nota = f'<queda:{BM.CE_QUEDA}>' if mid == M_MORRO else ''\n"
          "        j = map_json(template, m, disp, bgmn, bgsn, nota, bgm_vol=65, bgs_vol=45)\n")

s = troca(s, "            lst[i:i + 1] = transfer(M_CASA_B, 7, 9, 8, fade=2)\n            break\n    save('CommonEvents.json', ce)\n",
          "            lst[i:i + 1] = transfer(M_CASA_B, 7, 9, 8, fade=2)\n            break\n"
          "    BM.eventos_comuns(ce)\n    save('CommonEvents.json', ce)\n")
gravar('build_ch3.py', s)

# switch/variavel novos no System.json (no update_database do capitulo 3)
s = abrir('build_ch3.py')
s = troca(s, "    save('System.json', sysd)\n\n\ndef main():", "    BM.sistema(sysd)\n    save('System.json', sysd)\n\n\ndef main():")
gravar('build_ch3.py', s)

# ------------------------------------------------------------------ build_env.py (cenario do morro)
s = abrir('build_env.py')
ini = s.index("def morro():")
fim = s.index("def vidente():")
corpo = s[ini:fim]
corpo = troca(corpo, "    for (x, y) in [(1, 19), (3, 19), (22, 20), (16, 27), (8, 27)]:",
              "    import build_morro as BM\n    for (x, y) in BM.ARVORES:")
corpo = troca(corpo, "    examinar(mp, 9, 7, 'Mirante',", "    examinar(mp, BM.MIRANTE[0], BM.MIRANTE[1], 'Mirante',")
corpo = troca(corpo, "    return mp, (12, 27), True", "    return mp, BM.INICIO, True")
s = s[:ini] + corpo + s[fim:]
gravar('build_env.py', s)
print('ok')
