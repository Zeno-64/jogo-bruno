# Ratos mais dificeis no patio da Luz da Se: patrulhas com faro, manada saindo da toca,
# porta trancada com a chave no fim do corredor de cima e falas sorteadas na mordida.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'build_ch1.py')
s = open(p, encoding='utf-8').read()


def troca(velho, novo):
    global s
    assert s.count(velho) == 1, velho[:60]
    s = s.replace(velho, novo)


# ---- constantes do tileset E e dos itens novos
troca("C0, D0 = 256, 512\n", '''C0, D0, E0 = 256, 512, 768
E_TOCA = E0 + 5
IT_CHAVE, IT_BANANA_DOURADA = 41, 40


def registrar_tileset_e():
    """Folha E do Exterior (Morro_E): cascas de banana, rachadura, tabua de ponte, toca de rato e cocos."""
    ts = load('Tilesets.json')
    t = ts[2]
    t['tilesetNames'][8] = 'Morro_E'
    for n in (0, 1, 2, 3, 4):
        t['flags'][E0 + n] = 0x600       # passaveis, por baixo dos personagens
    t['flags'][E0 + 5] = 0x610           # toca: estrela (desenhada por cima)
    t['flags'][E0 + 6] = 0x60f           # monte de cocos: bloqueia
    save('Tilesets.json', ts)
    TILESETS[:] = ts
''')

# ---- tocas da manada na cerca do corredor y=10
troca('''    for (x, y) in [(2, 16), (22, 16), (4, 17), (20, 17), (1, 15), (23, 15)]:
        m.put(x, y, 2, rng.choice([181, 141, C0 + 26]))
    return m
''', '''    for (x, y) in [(2, 16), (22, 16), (4, 17), (20, 17), (1, 15), (23, 15)]:
        m.put(x, y, 2, rng.choice([181, 141, C0 + 26]))
    # tocas de onde sai a manada de ratos (y=10)
    m.put(0, 10, 3, E_TOCA); m.put(W - 1, 10, 3, E_TOCA)
    return m
''')

# ---- eventos do patio
ini = s.index("def events_patio(m):")
fim = s.index("def ce_pego():")
s = s[:ini] + '''def rato(m, x, y, chamada, speed=4, d=4):
    """Rato com movimento esperto (plugin Patrulhas): morde ao encostar."""
    m.add_event('Rato', x, y, [page(
        [cmd(117, [1])], image={'characterName': '$Rato', 'direction': d},
        trigger=2, move_type=3, speed=speed, freq=5,
        mroute=route([rc(45, chamada)], repeat=True, skippable=True, wait=False))])


def events_patio(m):
    ambient(m, DARK)
    m.add_event('Chegada', 0, 18, [
        page(bgm('Dungeon3', vol=70)
             + narr('Luz da Sé... uma estação de trem abandonada,', 'cercada de destroços.')
             + se('Cat', pitch=150, vol=60)
             + balloon(-1, 1)
             + bar('Ratos! Muitos ratos!', 'Se eles me pegarem...')
             + narr('Chegue até a porta da estação sem ser pega',
                    'pelos ratos. Segure Shift para correr.')
             + narr('Cuidado: alguns ratos farejam quem chega', 'perto, e os da toca correm em bando!')
             + self_sw(), trigger=3, priority=0),
        page([], priority=0, self_switch='A'),
    ])
    # porta trancada: a chave fica no fim do corredor de cima, a esquerda
    abrir = (se('Key') + narr('Clec! O cadeado enferrujado abre.') + item(IT_CHAVE, -1) + self_sw('A')
             + se('Door2') + transfer(M_ESTACAO, 10, 11, 8))
    primeira = (se('Buzzer1') + bar('Trancada?! Tem um cadeado enferrujado', 'aqui!')
                + narr('Lá no fim do corredor, à esquerda, alguma', 'coisa brilha...')
                + self_sw('B'))
    m.add_event('Porta da estação', 12, 3, [
        page(if_([8, IT_CHAVE], abrir,
                 if_([2, 'B', 0], se('Buzzer1') + bar('Trancada! Cadê aquela chave...'), primeira)),
             trigger=1, priority=1),
        page(se('Door2') + transfer(M_ESTACAO, 10, 11, 8), trigger=1, priority=0, self_switch='A'),
    ])
    m.add_event('Chave', 1, 4, [
        page(se('Item1') + item(IT_CHAVE, 1)
             + destaque('item', imagem='Item_Chave', nome='Chave Enferrujada', texto='Abre o cadeado da estação.')
             + bar('A chave! Agora é voltar até a porta...', 'sem virar petisco de rato.') + self_sw(),
             image={'characterName': '!$Brilho', 'direction': 2}, trigger=1, priority=0, step=True),
        page([], priority=0, self_switch='A'),
    ])
    m.add_event('Placa', 11, 3, [page(narr('ESTAÇÃO LUZ DA SÉ', '(desativada)'))])
    for x in (2, 22):
        m.add_event('Checkpoint', x, 8, [
            page([cmd(111, [1, V_CHECK, 0, 2, 0])] + [cmd(0, [], 1), cmd(411, [])]
                 + var_set(V_CHECK, 2, ind=1) + se('Save2', ind=1)
                 + destaque('aviso', icone=212, nome='Checkpoint!', texto='Se um rato te pegar, você volta pra cá.', ind=1)
                 + [cmd(0, [], 1), cmd(412, [])], trigger=1, priority=0),
        ])
    m.add_event('Voltar', 12, 18, [page(transfer(M_MUNDO, 44, 31, 2), trigger=1, priority=0)])
    # corredor 1 (y 12-13): um rato de ponta a ponta, dois vigiando as entradas
    # e um farejador perto da saida do meio
    rato(m, 8, 12, 'this.patrulhar(1, 23, 0)', speed=4, d=6)
    rato(m, 5, 13, 'this.patrulhar(1, 6, 0)', speed=3, d=4)
    rato(m, 19, 13, 'this.patrulhar(18, 23, 0)', speed=3, d=6)
    rato(m, 12, 13, 'this.patrulhar(9, 15, 3, 5, 12, 13)', speed=3, d=4)
    # corredor 2 (y 9-10): manada saindo da toca da direita, patrulheiro e farejador na saida esquerda
    for k in range(3):
        rato(m, W_PATIO - 1, 10, f'this.correrLinha({W_PATIO - 1}, 0, 34, 0, false, {k * 16})', speed=5, d=4)
    rato(m, 12, 9, 'this.patrulhar(10, 15, 0)', speed=4, d=6)
    rato(m, 3, 9, 'this.patrulhar(1, 4, 2, 5, 9, 10)', speed=3, d=4)
    # corredor 3 (y 6-7): dois ratos se cruzando, um bem rapido
    rato(m, 20, 6, 'this.patrulhar(1, 23, 0)', speed=5, d=4)
    rato(m, 6, 7, 'this.patrulhar(1, 23, 0)', speed=4, d=6)
    # corredor da porta (y 4): um rato rapido entre a chave e a porta
    rato(m, 16, 4, 'this.patrulhar(4, 20, 0)', speed=5, d=4)


''' + s[fim:]

# ---- mordida: uma fala sorteada por vez
troca("""    lst = (se('Bite') + flash([255, 40, 40, 170], 20) + shake(4, 9, 10, w=False)
           + pose(-1, 'dor')
           + bar('Aaai! Um rato me mordeu!')
           + narr('Volte ao checkpoint e tente de novo!')
""", """    falas = [('Aaai! Um rato me mordeu!',), ('Socorro! Ele mordeu meu dedão!',),
             ('Ai! Esse rato tem dente de tubarão!',), ('Eca! Ele me lambeu E me mordeu!',)]
    sorteio = [cmd(122, [5, 5, 0, 2, 0, len(falas) - 1])]
    for i, f in enumerate(falas):
        sorteio += [cmd(111, [1, 5, 0, i, 0])] + bar(*f, ind=1) + [cmd(0, [], 1), cmd(412, [])]
    lst = (se('Bite') + flash([255, 40, 40, 170], 20) + shake(4, 9, 10, w=False)
           + pose(-1, 'dor')
           + sorteio
""")

troca("LANE_WALLS = {5: [12], 8: [2, 22], 11: [12], 14: [3, 21]}\n",
      "LANE_WALLS = {5: [12], 8: [2, 22], 11: [12], 14: [3, 21]}\nW_PATIO = 25\n")

troca("""def main():
    template = load('Map001.json')

    rec = build_recife()""", """def main():
    template = load('Map001.json')
    registrar_tileset_e()

    rec = build_recife()""")

# condicional e item: copias locais (o capitulo 2 importa este arquivo, entao nao da para importar de la)
troca("END = cmd(0, [])\n", '''END = cmd(0, [])


def if_(params, then, els=None):
    sub = lambda lst: [dict(c, indent=c['indent'] + 1) for c in lst]
    out = [cmd(111, params)] + sub(then) + [cmd(0, [], 1)]
    if els is not None:
        out += [cmd(411, [])] + sub(els) + [cmd(0, [], 1)]
    return out + [cmd(412, [])]


def item(iid, n):
    return [cmd(126, [iid, 0 if n >= 0 else 1, 0, abs(n)])]
''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
