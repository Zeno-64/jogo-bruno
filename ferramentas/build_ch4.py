# Monta o Capitulo 4 (Gloriosa Saborosa): banco de dados, mapas 15 a 20, eventos comuns,
# ligacao com o fim do Capitulo 3 e o menu "Capitulos".
import copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ch4_comum import *
import build_mauara as BMa
import build_templo as BT

PLUGINS = [
    ('LutaArena', 'Minigame de luta em tempo real contra o Pavão-Hipopótamo.'),
    ('CorridaUma', 'Corrida no estilo Umamusume do templo até a saída da floresta.'),
    ('Templo', 'Enigmas do Templo da Xavasca Leprosa (estátuas empurráveis).'),
]


# ================================================================ banco de dados
def itens():
    it = load('Items.json')
    while len(it) <= IT_GUARANA:
        it.append(None)
    chave, pocao = it[41], it[7]

    def k(iid, nome, icone, desc):
        x = copy.deepcopy(chave); x.update({'id': iid, 'name': nome, 'iconIndex': icone, 'description': desc})
        it[iid] = x

    def consumivel(iid, nome, icone, desc, efeitos, anim):
        x = copy.deepcopy(pocao)
        x.update({'id': iid, 'name': nome, 'iconIndex': icone, 'description': desc, 'effects': efeitos,
                  'animationId': anim, 'price': 60})
        it[iid] = x
    k(IT_PERUCA, 'Peruca Dourada', 310, 'A lendária Peruca de Ouro.\nFormada do pó do crânio de Leandra.')
    k(IT_MEIA, 'Metade da Peruca', 310, 'Metade da Peruca Dourada.\nA outra metade está com a Leona.')
    k(IT_JADE, 'Chave de Jade', 195, 'Abre a porta do 1º andar do templo.')
    k(IT_FERRADURA, 'Chave de Ferradura', 195, 'Abre a porta do 2º andar do templo.')
    k(IT_ARCOIRIS, 'Chave Arco-Íris', 195, 'Abre a porta do santuário.')
    k(IT_PENA, 'Pena de Pavão', 296, 'Lembrança do Pavão-Hipopótamo.\nVale mais que o seu aluguel.')
    consumivel(IT_CENOURA, 'Cenoura Dourada', 256, 'Comida oficial das Umamusumes.\nRecupera 300 de vida.',
               [{'code': 11, 'dataId': 0, 'value1': 0, 'value2': 300}], 41)
    consumivel(IT_GUARANA, 'Guaraná da Floresta', 273, 'Bebida da Floresta de Mauara.\nRecupera 50 de PM.',
               [{'code': 12, 'dataId': 0, 'value1': 0, 'value2': 50}], 45)
    save('Items.json', it)


def habilidades():
    s = load('Skills.json')
    while len(s) <= SK_CALMA:
        s.append(None)
    t = s[1]

    def cap(sid, name, desc, icon, an, formula, scope, hit, mp, msg, effects=(), dtype=1):
        sk = mk_skill(t, sid, name, desc, icon, an, formula, dtype, scope, hit, mp, msg, effects)
        sk['damage']['variance'] = 0
        return sk
    s[SK_VIDENTE] = cap(SK_VIDENTE, 'A Vidente Calva', 'A careca da vidente revela os pontos fracos. (até 100)', 79, 96,
                        'Math.min(100, 50 + a.mat)', 1, 2, 10, '%1 tira a carta A Vidente Calva!',
                        [{'code': 32, 'dataId': 3, 'value1': 3, 'value2': 0}])
    s[SK_SAPO] = cap(SK_SAPO, 'O Sapo Sacudo', 'Um sapo sarado cai sobre os inimigos. (até 100)', 79, 87,
                     'Math.min(100, 30 + a.mat)', 2, 2, 14, '%1 tira a carta O Sapo Sacudo!',
                     [{'code': 21, 'dataId': 13, 'value1': 0.3, 'value2': 0}])
    s[SK_TRAVECO] = cap(SK_TRAVECO, 'O Traveco', 'Extrai o potencial latente do grupo.', 79, 53, '0', 8, 0, 20,
                        '%1 tira a carta O Traveco! Potencial latente!',
                        [{'code': 31, 'dataId': 2, 'value1': 3, 'value2': 0}, {'code': 31, 'dataId': 4, 'value1': 3, 'value2': 0},
                         {'code': 31, 'dataId': 6, 'value1': 3, 'value2': 0}], dtype=0)
    s[SK_COICE] = cap(SK_COICE, 'Coice de Cavala', 'Um coice de Umamusume. (até 100)', 77, 21, 'Math.min(100, 45 + a.atk)',
                      1, 1, 4, '%1 dá um coice de cavala!')
    s[SK_GALOPE] = cap(SK_GALOPE, 'Galope Relâmpago', 'Dois golpes velozes em inimigos aleatórios. (até 100)', 77, 77,
                       'Math.min(100, 25 + a.agi)', 5, 1, 8, '%1 dispara num Galope Relâmpago!')
    s[SK_RELINCHO] = cap(SK_RELINCHO, 'Relincho Motivador', 'Aumenta a agilidade do grupo e cura um pouco.', 84, 51, '0', 8, 0, 6,
                         '%1 relincha: VAMOS, GALERA!',
                         [{'code': 31, 'dataId': 6, 'value1': 3, 'value2': 0}, {'code': 11, 'dataId': 0, 'value1': 0.1, 'value2': 0}],
                         dtype=0)
    s[SK_FOFOCA] = mk_skill(t, SK_FOFOCA, 'Fofoca Venenosa', '', 0, 59, '25 + a.mat - b.mdf / 2', 1, 1, 2, 0,
                            '%1 espalha uma fofoca venenosa!', [{'code': 21, 'dataId': 4, 'value1': 0.4, 'value2': 0}])
    s[SK_BICADA] = mk_skill(t, SK_BICADA, 'Bicada Barraqueira', '', 0, 16, '30 + a.atk - b.def', 1, 1, 1, 0,
                            '%1 dá uma bicada barraqueira!')
    s[SK_SUPINO] = mk_skill(t, SK_SUPINO, 'Supino na Cara', '', 0, 39, '40 + a.atk - b.def', 1, 1, 1, 0,
                            '%1 faz um supino... na sua cara!')
    s[SK_CALMA] = mk_skill(t, SK_CALMA, 'Calmaria de Capivara', '', 0, 41, '120', 3, 11, 0, 0,
                           '%1 medita e recupera a paz interior.')
    save('Skills.json', s)


def classes():
    c = load('Classes.json')
    while len(c) <= CLS_DIVA:
        c.append(None)
    tpl = c[1]

    def mk_class(cid, name, p0, g, skills):
        params = [[int(p0[i] + g[i] * max(lv - 1, 0)) for lv in range(100)] for i in range(8)]
        traits = [t for t in tpl['traits'] if t['code'] in (22, 23)] + [{'code': 41, 'dataId': 2, 'value': 1}]
        return {'id': cid, 'expParams': [30, 20, 30, 30], 'traits': traits,
                'learnings': [{'level': 1, 'note': '', 'skillId': s} for s in skills], 'name': name, 'note': '', 'params': params}
    c[CLS_UMA] = mk_class(CLS_UMA, 'Umamusume', [1000, 70, 62, 40, 25, 35, 48, 25], [40, 4, 4, 3, 1, 2, 3, 1],
                          [249, 250, 251, SK_COICE, SK_GALOPE, SK_RELINCHO])
    c[CLS_DIVA] = mk_class(CLS_DIVA, 'Diva Musume Saborosa', [760, 140, 46, 36, 62, 46, 36, 36], [32, 7, 3, 2, 5, 3, 2, 2],
                           [245, 246, 247, 248, SK_VIDENTE, SK_SAPO, SK_TRAVECO])
    save('Classes.json', c)


def inimigos_e_tropas():
    e = load('Enemies.json')
    while len(e) <= EN_CAPIVARA:
        e.append(None)
    base = e[7]
    act = lambda sid, r: {'conditionParam1': 0, 'conditionParam2': 0, 'conditionType': 0, 'rating': r, 'skillId': sid}
    e[EN_ARARA] = dict(copy.deepcopy(base), id=EN_ARARA, name='Arara Barraqueira', battlerName='Arara_Barraqueira',
                       actions=[act(1, 5), act(SK_FOFOCA, 5), act(SK_BICADA, 5)], exp=45, gold=30,
                       dropItems=[{'dataId': IT_GUARANA, 'denominator': 3, 'kind': 1}, {'dataId': 1, 'denominator': 1, 'kind': 0},
                                  {'dataId': 1, 'denominator': 1, 'kind': 0}],
                       params=[260, 0, 42, 22, 40, 20, 50, 20],
                       note='<vivo:flutuar>\n<escala:0.7>\n<sombra:0.45>')
    e[EN_CAPIVARA] = dict(copy.deepcopy(base), id=EN_CAPIVARA, name='Capivara Marombeira', battlerName='Capivara_Marombeira',
                          actions=[act(1, 5), act(SK_SUPINO, 6), act(SK_CALMA, 3)], exp=55, gold=25,
                          dropItems=[{'dataId': IT_CENOURA, 'denominator': 3, 'kind': 1}, {'dataId': 1, 'denominator': 1, 'kind': 0},
                                     {'dataId': 1, 'denominator': 1, 'kind': 0}],
                          params=[340, 0, 50, 34, 10, 22, 22, 15],
                          note='<vivo:respirar>\n<escala:0.68>\n<sombra:0.6>')
    save('Enemies.json', e)
    tr = load('Troops.json')
    while len(tr) <= TR_MISTO:
        tr.append(None)
    arara = lambda *l: text(list(l), name='Arara Barraqueira')
    tr[TR_ARARAS] = {'id': TR_ARARAS, 'name': 'Araras Barraqueiras', 'members': [
        {'enemyId': EN_ARARA, 'x': 170, 'y': 360, 'hidden': False}, {'enemyId': EN_ARARA, 'x': 290, 'y': 440, 'hidden': False}],
        'pages': [tpage(arara('Fofoca quentinha: a sua peruca é FALSA!') + bar('Eu nem tenho peruca ainda!'), turn=0)]}
    tr[TR_CAPIVARA] = {'id': TR_CAPIVARA, 'name': 'Capivara Marombeira', 'members': [
        {'enemyId': EN_CAPIVARA, 'x': 240, 'y': 440, 'hidden': False}],
        'pages': [tpage(narr('A capivara flexiona o bíceps e encara', 'vocês.') + kuma('Ela não pulou o dia de perna...', i=3), turn=0)]}
    tr[TR_MISTO] = {'id': TR_MISTO, 'name': 'Arara e Capivara', 'members': [
        {'enemyId': EN_ARARA, 'x': 160, 'y': 360, 'hidden': False}, {'enemyId': EN_CAPIVARA, 'x': 300, 'y': 450, 'hidden': False}],
        'pages': [tpage(arara('Capivara, segura ela que eu falo mal!') + bar('Que dupla do mal!'), turn=0)]}
    save('Troops.json', tr)


def eventos_comuns():
    ce = load('CommonEvents.json')
    while len(ce) <= 10:
        ce.append(None)

    def mk(cid, nome, lst):
        ce[cid] = {'id': cid, 'list': lst + [END], 'name': nome, 'switchId': 1, 'trigger': 0}
    mk(CE_FALAS, 'Cap.4: falas da floresta', BMa.ce_falas())
    mk(CE_PORTAL, 'Cap.4: portal do templo', script('$gamePlayer.showFollowers(); $gamePlayer.refresh();') + BT.ce_portal())
    mk(CE_CIPO, 'Cap.4: cipó-laço', BMa.ce_cipo())
    mk(CE_AREIA, 'Cap.4: areia movediça', BMa.ce_areia())
    mk(10, 'Cap.4: pista resolvida', se('Applause1') + flash([255, 240, 180, 200], 30)
       + narr('As três Umamusumes de pedra cruzam a linha', 'de chegada... na ordem certa!')
       + se('Chest2') + narr('Um baú surge perto da placa da corrida!')
       + kuma('ISSO! Pódio perfeito!', i=2))
    save('CommonEvents.json', ce)


def sistema():
    s = load('System.json')
    nomes_sw = {S_C4_INICIO: 'Cap.4: abertura vista', S_C4_UMA: 'Cap.4: Kevinho Umamusume', S_C4_FLORESTA: 'Cap.4: entrou na floresta',
                S_ESPINHOS[0]: 'Cap.4: espinhos 1', S_ESPINHOS[1]: 'Cap.4: espinhos 2', S_ESPINHOS[2]: 'Cap.4: espinhos 3',
                S_PAVAO: 'Cap.4: Pavão vencido', S_PORTAL[0]: 'Cap.4: portal 1º andar', S_PORTAL[1]: 'Cap.4: portal 2º andar',
                S_PORTAL[2]: 'Cap.4: portal 3º andar', S_T1_OK: 'Cap.4: perucas certas', S_T2_OK: 'Cap.4: pódio certo',
                S_T3_OK: 'Cap.4: esfinge respondida', S_PORTA[0]: 'Cap.4: porta do 1º andar', S_PORTA[1]: 'Cap.4: porta do 2º andar',
                S_PORTA[2]: 'Cap.4: porta do santuário', S_VERA: 'Cap.4: Vera Verão', S_CORRIDA: 'Cap.4: alcançou a Leona',
                S_C4_FIM: 'Fim do Capítulo 4', S_CORACAO: 'Cap.4: coração da floresta', S_SELADA: 'Cap.4: porta selada ouvida',
                S_ESPINHOS2[0]: 'Cap.4: espinhos do coração'}
    while len(s['switches']) <= max(nomes_sw):
        s['switches'].append('')
    for k, v in nomes_sw.items():
        s['switches'][k] = v
    nomes_var = {V_MAO: 'Templo: peruca na mão', V_BUSTOS[0]: 'Templo: busto 1', V_BUSTOS[1]: 'Templo: busto 2',
                 V_BUSTOS[2]: 'Templo: busto 3', V_BUSTOS[3]: 'Templo: busto 4', V_ESFINGE: 'Templo: esfinge',
                 V_CORRIDA: 'Corrida: resultado', V_LUTA: 'Luta: resultado', V_DX: 'Armadilha: x', V_DY: 'Armadilha: y',
                 V_MAPA: 'Armadilha: mapa', V_NOME: 'Templo: nome da peruca', V_PORTAL_AQUI: 'Portal: andar atual'}
    while len(s['variables']) <= max(nomes_var):
        s['variables'].append('')
    for k, v in nomes_var.items():
        s['variables'][k] = v
    save('System.json', s)


# ================================================================ ligacoes com o resto do jogo
def ligar_fim_do_cap3():
    j = load(f'Map{M_VIDENTE:03d}.json')
    for ev in j['events']:
        if not ev:
            continue
        for pg in ev['pages']:
            lst = pg['list']
            for i, c in enumerate(lst):
                if c['code'] == 354:
                    lst[i:i + 1] = transfer(M_CAMPO, 8, 8, 6, fade=2)
                    save(f'Map{M_VIDENTE:03d}.json', j)
                    return True
    return False


def menu_capitulos():
    p = f'{PROJ}/js/plugins/Capitulos.js'
    s = open(p, encoding='utf-8').read()
    if 'Capítulo 4' not in s:
        s = s.replace('        { name: "Capítulo 3 - Baratelli, a Cigana Vingativa", mapId: 12, x: 7, y: 9, dir: 8, party: [1] },\n',
                      '        { name: "Capítulo 3 - Baratelli, a Cigana Vingativa", mapId: 12, x: 7, y: 9, dir: 8, party: [1] },\n'
                      f'        {{ name: "Capítulo 4 - Gloriosa Saborosa", mapId: {M_CAMPO}, x: 8, y: 8, dir: 6, party: [1, 5] }},\n')
        open(p, 'w', encoding='utf-8', newline='\n').write(s)


def registrar_plugins():
    path = f'{PROJ}/js/plugins.js'
    pl = open(path, encoding='utf-8').read()
    for nome, desc in PLUGINS:
        if f'"name":"{nome}"' not in pl:
            entry = json.dumps({'name': nome, 'status': True, 'description': desc, 'parameters': {}},
                               ensure_ascii=False, separators=(',', ':'))
            pl = pl.replace('\n];', ',\n' + entry + '\n];')
    open(path, 'w', encoding='utf-8', newline='\n').write(pl)


# ================================================================ mapas
def salvar_mapa(template, mid, m, nome, bgm_nome, nota, battle=None, bgm_vol=70):
    j = map_json(template, m, nome, bgm_nome, '', nota, bgm_vol=bgm_vol)
    j.update({'parallaxLoopX': False, 'parallaxLoopY': False, 'parallaxSx': 0, 'parallaxSy': 0})
    if battle:
        j.update({'specifyBattleback': True, 'battleback1Name': battle[0], 'battleback2Name': battle[1]})
    save(f'Map{mid:03d}.json', j)


def main():
    BMa.registrar_tiles_floresta()
    BT.registrar_tileset_templo()
    itens(); habilidades(); classes(); inimigos_e_tropas(); eventos_comuns(); sistema()
    template = load('Map001.json')

    campo = BMa.construir_campo(); BMa.eventos_campo(campo)
    mauara, info16 = BMa.construir_mauara(); BMa.eventos_mauara(mauara, info16); BT.final_capitulo(mauara)
    coracao, info17 = BMa.construir_coracao(); BMa.eventos_coracao(coracao, info17)
    t1 = BT.construir_t1(); BT.eventos_t1(t1)
    t2 = BT.construir_t2(); BT.eventos_t2(t2)
    t3 = BT.construir_t3(); BT.eventos_t3(t3); BT.eventos_santuario(t3)

    # ---- verificacoes de caminho
    assert (18, 7) in campo.reach((8, 8)), 'acampamento: saida'
    n16 = BMa.verificar(mauara, info16, MAUARA_INICIO, [(info16['saida'][0], 0)], 'Mauara')
    n17 = BMa.verificar(coracao, info17, CORACAO_INICIO, [(19, 17)], 'Coração')
    assert (19, 5) not in coracao.reach(CORACAO_INICIO, blocked={(18, 17), (19, 17), (20, 17)}), 'o Pavão deveria bloquear a escada'
    assert (19, 5) in coracao.reach(CORACAO_INICIO), 'escada do templo'
    for (mm, ini, alvos, nome) in [(t1, T1_CHEGADA, [(12, 3), (3, 10), (21, 10), (12, 7), (4, 16)], '1º andar'),
                                   (t2, T2_CHEGADA, [(13, 3), (7, 18), (20, 16), (13, 13)], '2º andar'),
                                   (t3, T3_CHEGADA, [(13, 12), (13, 17), (6, 12), (8, 22)], '3º andar')]:
        alc = mm.reach(ini)
        for a in alvos:
            assert a in alc, f'{nome}: {a} inalcançável'
    assert (13, 7) in t3.reach((13, 8)), 'santuário'

    mapas = [
        (M_CAMPO, campo, 'Acampamento', '', '<particulas:vagalumes>\n<vinheta:0.3>', None),
        (M_MAUARA, mauara, 'Floresta de Mauara', 'Floresta_Mauara', '<particulas:folhas>\n<vinheta:0.35>', ('Grassland', 'Forest')),
        (M_CORACAO, coracao, 'Coração de Mauara', 'Floresta_Mauara', '<particulas:vagalumes>\n<vinheta:0.3>', ('Grassland', 'Forest')),
        (M_T1, t1, 'Templo - 1º Andar', 'Templo_Xavasca', '<particulas:poeira>\n<vinheta:0.4>', ('Temple', 'Temple')),
        (M_T2, t2, 'Templo - 2º Andar', 'Templo_Xavasca', '<particulas:poeira>\n<vinheta:0.4>', ('Temple', 'Temple')),
        (M_T3, t3, 'Templo - 3º Andar', 'Templo_Xavasca', '<particulas:estrelinhas>\n<vinheta:0.4>', ('Temple', 'Temple')),
    ]
    for mid, m, nome, musica, nota, battle in mapas:
        salvar_mapa(template, mid, m, nome, musica, nota, battle)

    mi = load('MapInfos.json')
    while len(mi) <= M_T3:
        mi.append(None)
    for o, (mid, name, parent) in enumerate([(M_CAMPO, 'Cap.4 - Acampamento', 0), (M_MAUARA, 'Floresta de Mauara', M_CAMPO),
                                             (M_CORACAO, 'Coração de Mauara', M_MAUARA), (M_T1, 'Templo - 1º Andar', M_CORACAO),
                                             (M_T2, 'Templo - 2º Andar', M_T1), (M_T3, 'Templo - 3º Andar', M_T2)], 15):
        mi[mid] = {'id': mid, 'expanded': True, 'name': name, 'order': o, 'parentId': parent, 'scrollX': 0, 'scrollY': 0}
    save('MapInfos.json', mi)

    ligado = ligar_fim_do_cap3()
    menu_capitulos()
    registrar_plugins()
    print('capítulo 4: ok | fim do cap.3 ligado:', ligado, '| mauara:', n16, 'tiles | coração:', n17,
          '| eventos', {nome: len(m.events) - 1 for _, m, nome, *_ in mapas})


if __name__ == '__main__':
    main()
