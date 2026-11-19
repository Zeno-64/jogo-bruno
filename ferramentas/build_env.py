# Cenarios interativos: objetos para examinar, interacoes com humor, bichos, vida e particulas em todos os mapas.
import copy, os, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_ch1 as B
from build_ch1 import (Map, cmd, text, se, me, wait, balloon, shake, flash, page, rc, self_sw, audio, load, save,
                       END, C0, D0)
from build_ch2 import if_, choices, script, item, img, gold
from fx import destaque, pose

V_RAND = 5
IT = dict(tampinha=33, bilhete=34, chinelo=35, pedrinha=36, pastel=37, coco=38, banana=39, banana_dourada=40, chave=41)

# falas -------------------------------------------------------------------------------------------
FACES = {
    'b': ('Baratelli', 0, 'Baratelli'), 'l': ('Leandra', 0, 'Leandra'), 'L': ('Leandra', 1, 'Leandra'),
    'o': ('Leona', 0, 'Leona'), 'k': ('Kevinho', 0, 'Kevinho'), 'v': ('Vidente', 0, 'Vidente'),
    'g': ('People1', 2, 'Gusrola'), 'n': ('', 0, ''),
}


def say(spk, *lines):
    face, idx, name = FACES[spk]
    return text(list(lines), face=face, idx=idx, name=name)


def N(*lines):
    return say('n', *lines)


def rand(*options):
    """Cada opcao e uma lista de comandos; uma e sorteada a cada interacao."""
    if len(options) == 1:
        return list(options[0])
    lst = [cmd(122, [V_RAND, V_RAND, 0, 2, 0, len(options) - 1])]
    for i, opt in enumerate(options):
        lst += if_([1, V_RAND, 0, i, 0], list(opt))
    return lst


# mapa --------------------------------------------------------------------------------------------
class Mapa:
    def __init__(self, mid):
        self.mid = mid
        self.j = load(f'Map{mid:03d}.json')
        self.m = Map(self.j['width'], self.j['height'], self.j['tilesetId'])
        self.m.data = self.j['data']
        self.ev = self.j['events']
        self.novos = []

    def save(self):
        save(f'Map{self.mid:03d}.json', self.j)

    def at(self, x, y):
        return [e for e in self.ev if e and e['x'] == x and e['y'] == y]

    def by_name(self, name):
        return [e for e in self.ev if e and e['name'] == name]

    def add(self, name, x, y, pages, check='examinar'):
        assert not self.at(x, y), (self.mid, name, x, y, 'ja tem evento')
        eid = len(self.ev)
        self.ev.append({'id': eid, 'name': name, 'note': '', 'pages': pages, 'x': x, 'y': y})
        self.novos.append((name, x, y, check))
        return eid

    def tile(self, x, y, z, tid):
        self.m.put(x, y, z, tid)

    def nota(self, txt):
        self.j['note'] = (self.j.get('note') or '') + txt

    def bgs(self, name, vol=40):
        self.j['autoplayBgs'] = True
        self.j['bgs'] = audio(name, vol)

    def verificar(self, start, jumps=False):
        pulos = {(e['x'], e['y']) for e in self.ev if e and e['name'] == 'Pulo'} if jumps else set()
        seen = {start}; q = deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in seen and self.m.passable(*n) and not self.bloqueado(n):
                    seen.add(n); q.append(n)
                elif n in pulos:
                    l = (x + 2 * dx, y + 2 * dy)
                    if l not in seen and self.m.passable(*l):
                        seen.add(l); q.append(l)
        ruins = []
        for (name, x, y, check) in self.novos:
            viz = any((x + dx, y + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if check == 'examinar' and not viz:
                ruins.append((name, x, y, 'ninguem alcanca'))
            if check == 'examinar' and self.m.passable(x, y):
                ruins.append((name, x, y, 'tile andavel (bloquearia caminho)'))
            if check == 'chao' and (x, y) not in seen and not viz:
                ruins.append((name, x, y, 'fora do caminho'))
        return ruins

    def bloqueado(self, c):
        for e in self.at(*c):
            if e['name'].startswith('Porta'):
                continue
            for p in e['pages'][:1]:
                if p['priorityType'] == 1 and not p['through']:
                    return True
        return False


def examinar(mp, x, y, name, *options):
    return mp.add(name, x, y, [page(rand(*options))])


def uma_vez(mp, x, y, name, primeiro, depois, image=None, check='examinar', prio=1):
    pg1 = page(primeiro + self_sw(), image=image, priority=prio, step=bool(image), dir_fix=bool(image), walk=not image)
    pg2 = page(rand(*depois) if depois else [], priority=prio if depois else 0, self_switch='A')
    return mp.add(name, x, y, [pg1, pg2], check=check)


def brilho(mp, x, y, name, cmds):
    return uma_vez(mp, x, y, name, N('Algo brilha no chão...') + cmds, [], image=img('!$Brilho', 0, 2, 1), check='chao')


def bicho(mp, x, y, name, image, *options, som=None, pitch=100, speed=3):
    s = se(som, pitch=pitch) if som else []
    return mp.add(name, x, y, [page(s + rand(*options), image=image, move_type=1, speed=speed, freq=3)], check='chao')


# O jogador foge correndo (pose de corrida) para o lado mais livre e o bicho corre atras latindo,
# enquanto a legenda aparece no topo da tela. Depois o bicho desiste e o jogador fica ofegante.
JS_PERSEGUICAO = """const dog = $gameMap.event(this._eventId);
const p = $gamePlayer;
const C = Game_Character;
const MOV = {2: C.ROUTE_MOVE_DOWN, 4: C.ROUTE_MOVE_LEFT, 6: C.ROUTE_MOVE_RIGHT, 8: C.ROUTE_MOVE_UP};
const R = (code, parameters) => ({code: code, parameters: parameters || []});
const late = (pitch) => R(C.ROUTE_PLAY_SE, [{name: 'Dog', volume: 90, pitch: pitch, pan: 0}]);
const lados = (d) => { const l = (d === 2 || d === 8) ? [4, 6] : [2, 8]; return Math.random() < 0.5 ? l : l.reverse(); };
// caminho de fuga: segue reto enquanto der e vira nas esquinas, nunca volta para o bicho
let x = p.x, y = p.y, dir = p.reverseDir(p.direction());
const caminho = [], visto = new Set([x + ',' + y, dog.x + ',' + dog.y]);
while (caminho.length < 5) {
  const ok = [dir].concat(lados(dir)).find(d => {
    const nx = $gameMap.roundXWithDirection(x, d), ny = $gameMap.roundYWithDirection(y, d);
    return p.canPass(x, y, d) && !visto.has(nx + ',' + ny);
  });
  if (!ok) break;
  x = $gameMap.roundXWithDirection(x, ok); y = $gameMap.roundYWithDirection(y, ok);
  visto.add(x + ',' + y); caminho.push(ok); dir = ok;
}
const n = caminho.length;
const vel = p.moveSpeed();
const rp = [R(C.ROUTE_SCRIPT, ['$gameTemp.requestBalloon(this, 1)']), R(C.ROUTE_WAIT, [8])];
if (n > 0) {
  rp.push(R(C.ROUTE_CHANGE_SPEED, [5]));
  for (const d of caminho) rp.push(R(MOV[d]));
  rp.push(R(C.ROUTE_CHANGE_SPEED, [vel]));
} else {
  rp.push(R(C.ROUTE_JUMP, [0, 0]));
}
rp.push(R(C.ROUTE_SCRIPT, ['this.turnTowardCharacter($gameMap.event(' + dog.eventId() + ')); this.pose("cansado")']), R(C.ROUTE_END));
const rd = [late(120), R(C.ROUTE_JUMP, [0, 0]), R(C.ROUTE_CHANGE_SPEED, [5])];
for (let i = 0; i <= Math.max(n, 1); i++) {
  rd.push(R(C.ROUTE_MOVE_TOWARD));
  if (i % 2 === 1) rd.push(late(i === 1 ? 135 : 115));
}
rd.push(late(100), R(C.ROUTE_WAIT, [20]), R(C.ROUTE_CHANGE_SPEED, [3]), R(C.ROUTE_TURN_AWAY),
        R(C.ROUTE_SCRIPT, ['$gameTemp.requestBalloon(this, 6)']), R(C.ROUTE_MOVE_AWAY), R(C.ROUTE_WAIT, [30]), R(C.ROUTE_END));
dog._prelockDirection = 0;
p.forceMoveRoute({list: rp, repeat: false, skippable: true, wait: false});
dog.forceMoveRoute({list: rd, repeat: false, skippable: true, wait: false});"""

JS_ESPERAR_BICHO = "this._characterId = 0;\nthis.setWaitMode('route');"


def perseguicao_do_cachorro():
    return (script(JS_PERSEGUICAO)
            + text(['AU! AU! AU! O cachorro dispara atrás de', 'você... e depois desiste, sem fôlego.'], pos=0)
            + script(JS_ESPERAR_BICHO)
            + say('l', 'Ufa! Nesta cidade nem o cachorro dá', 'esmola... só susto!'))


def vida(mp, nomes, baloes=(3, 8, 10, 4, 1, 9), intervalo=170):
    ids = [e['id'] for n in nomes for e in mp.by_name(n)]
    if not ids:
        return
    js = ("if (!$gameMap.isEventRunning()) {\n"
          f"  const ids = {ids}; const bs = {list(baloes)};\n"
          "  const e = $gameMap.event(ids[Math.randomInt(ids.length)]);\n"
          "  if (e && e.characterName() && !e.isTransparent()) $gameTemp.requestBalloon(e, bs[Math.randomInt(bs.length)]);\n"
          "}")
    mp.add('Vida', 0, mp.j['height'] - 1 if not mp.at(0, mp.j['height'] - 1) else 1,
           [page(script(js) + wait(intervalo), trigger=4, priority=0)], check='nenhum')


def trocar_falas(mp, name, x, y, lst, pagina=0):
    alvo = [e for e in mp.at(x, y) if e['name'] == name]
    assert alvo, (mp.mid, name, x, y)
    alvo[0]['pages'][pagina]['list'] = lst + [END]


def trocar_todas(mp, name, lst, pagina=0):
    alvos = mp.by_name(name)
    assert alvos, (mp.mid, name)
    for e in alvos:
        e['pages'][pagina]['list'] = lst + [END]


def achado(chave, nome, texto, imagem, quem, reacao):
    return item(IT[chave], 1) + destaque('item', imagem=imagem, titulo='CURIOSIDADE', nome=nome, texto=texto) + say(quem, *reacao)


# =================================================================================================
def recife():
    mp = Mapa(1)
    janelas = [
        N('Pela janela: uma vovó assistindo novela', 'no volume máximo.') + say('b', 'Ela tá chorando... deve ser o', 'capítulo final!'),
        N('Pela janela: alguém fazendo cuscuz.', 'O cheiro é divino.') + say('b', 'Ai, que fome... mas tô atrasada!'),
        N('Pela janela: um gato te encara sem piscar.') + say('b', 'Ele sabe de tudo. Gatos sempre sabem.'),
        N('Pela janela: uma família dançando forró', 'na sala, às oito da manhã.'),
        N('Pela janela: alguém cantando no chuveiro.', 'Muito desafinado.') + say('b', 'Hihihi! Que vergonha alheia!'),
    ]
    for x in (2, 4, 8, 10, 15, 16, 22, 23):
        examinar(mp, x, 5, 'Janela', *janelas)
    trocar_falas(mp, 'Porta', 3, 5, N('Toc, toc!') + N('Uma voz lá de dentro: "Se for cobrança,', 'não tô!"')
                 + say('b', 'Mas eu só queria dizer bom dia...'))
    trocar_falas(mp, 'Porta', 9, 5, N('Um bilhete na porta: "Volto já."')
                 + N('O papel está amarelado. Deve estar ali', 'desde 2009.'))
    for x in (18, 20):
        examinar(mp, x, 5, 'Placa mística',
                 N('Placa: "LEITURA DE MÃO — hoje com 50% de', 'desconto pra quem tem calo."'),
                 N('Placa: "Aprenda tarô em 3 dias!', '(O quarto dia é pra chorar.)"'))
    chute = (pose(-1, 'chute', espera=12) + N('Baratelli chuta o coqueiro com toda a força!')
             + se('Blow2') + shake(5, 9, 10) + wait(20) + se('Blow1') + flash([255, 255, 255, 160], 10)
             + pose(-1, 'dor') + N('TOC! Um coco cai bem na cabeça dela!') + balloon(-1, 6)
             + say('b', 'Aiii! ...pelo menos agora tem água', 'de coco!')
             + item(IT['coco'], 1)
             + destaque('item', imagem='Item_Coco', nome='Água de Coco', texto='Recupera 200 de vida. Geladinha!'))
    for (x, y) in [(2, 10), (16, 10), (22, 12)]:
        uma_vez(mp, x, y, 'Coqueiro',
                N('Um coqueiro carregado de cocos.') + choices([('Chutar o coqueiro', chute), ('Deixar quieto', [])], cancel=1),
                [N('O coqueiro não tem mais coco maduro.', 'Só uns verdinhos lá no alto.')])
    for (x, y) in [(8, 12), (25, 9), (5, 14), (19, 14)]:
        examinar(mp, x, y, 'Coqueiro',
                 N('Um coqueiro. Uma capivara dorme na', 'sombra dele... ou dormia, até você chegar.'),
                 N('Alguém escreveu no tronco: "B + M".', 'Baratelli fica vermelha.') + balloon(-1, 4))
    brilho(mp, 10, 15, 'Tampinha',
           achado('tampinha', 'Tampinha de Garrafa', 'Achada na praia de Recife. Vale ouro! (Não vale.)',
                  'Item_Tampinha', 'b', ('Vou guardar de lembrança!',)))
    mar = [
        N('A água do mar de Recife: morninha e', 'salgada.') + se('Water1'),
        se('Damage1') + pose(-1, 'dor') + shake(4, 9, 8) + N('Um caranguejo belisca o dedo da Baratelli!') + say('b', 'AI! Caranguejo mal-educado!'),
        N('Uma concha. Encostando no ouvido, dá pra', 'ouvir o mar... e um podcast.'),
    ]
    for x in (6, 14, 21):
        examinar(mp, x, 16, 'Mar', *mar)
    trocar_todas(mp, 'Capivara', rand(
        N('A capivara te olha com toda a calma do', 'mundo.'),
        N('A capivara boceja. Ela não tem pressa', 'nenhuma. Diferente de você.') + say('b', 'Que inveja dessa paz...'),
        N('Uma capivara com um passarinho nas costas.', 'Os dois te ignoram.')))
    trocar_todas(mp, 'Ovelha', se('Sheep') + rand(
        say('n', 'Béééé!'),
        N('Bééé... a ovelha mastiga a barra do', 'vestido da Baratelli.') + say('b', 'Ei! Esse vestido é de festa!'),
        N('A ovelha dorme em pé. Está roncando.')))
    vida(mp, ['Capivara', 'Ovelha'], baloes=(3, 10, 4, 8))
    mp.nota('<particulas:petalas>')
    return mp, (1, 7), False


def matheos():
    mp = Mapa(3)
    trocar_falas(mp, 'Porta', 2, 4, N('Um bilhete na porta: "Fui ali e volto', 'mês que vem."'))
    trocar_falas(mp, 'Porta', 16, 4, N('Toc, toc!') + N('Lá de dentro: "Não tem ninguém em casa!"')
                 + say('b', '...Mas quem respondeu, então?'))
    trocar_falas(mp, 'Porta', 15, 11, se('Collapse1') + shake(4, 9, 8) + N('Você bate na porta e ela cai inteira no', 'chão!')
                 + say('b', 'Ai, meu Deus! Desculpa!') + N('Baratelli encosta a porta de volta, toda', 'envergonhada.'))
    lixo = [
        N('Lixo. Muito lixo. Uma barata acena pra', 'você.'),
        N('Uma caixa escrita "PROJETO DE REFORMA DA', 'CIDADE". Está vazia.'),
        N('Restos de uma marmita... de 2015.') + say('b', 'Eca!'),
        N('Um rádio quebrado tocando sozinho.', 'Só chiado... e um forró ao fundo.'),
    ]
    for (x, y) in [(5, 5), (6, 5), (12, 5), (13, 5), (19, 6), (0, 6), (5, 13), (0, 13)]:
        examinar(mp, x, y, 'Lixo', *lixo)
    uma_vez(mp, 11, 8, 'Lixo', N('Revirando o lixo, Baratelli encontra...')
            + achado('chinelo', 'Pé de Chinelo Esquerdo', 'Procura-se o pé direito.', 'Item_Chinelo', 'b',
                     ('Só o esquerdo? Cadê o direito?!',)), [lixo[0], lixo[3]])
    uma_vez(mp, 19, 9, 'Lixo', N('No meio do lixo, uma moeda brilha!') + gold(5)
            + destaque('moeda', imagem='Item_Esmola', nome='+5G', texto='O lixo de São Matheos é mais rico que você.'),
            [lixo[1], lixo[2]])
    examinar(mp, 6, 3, 'Árvore seca', N('Uma árvore seca. Nem a árvore quis', 'ficar em São Matheos.'))
    trocar_todas(mp, 'Rato', rand(
        se('Cancel2') + say('b', 'Eca, um rato!'),
        N('O rato te encara... e rouba uma migalha', 'do seu bolso.'),
        N('Um rato usando uma tampinha de chapéu.', 'Muito elegante.')))
    bicho(mp, 14, 12, 'Cachorro', img('Nature', 0, 2),
          N('Au! Au! O cachorro abana o rabo.'),
          N('O cachorro rola no lixo e fica feliz da', 'vida.') + say('b', 'Que fofo! ...e que cheiro!'), som='Dog')
    vida(mp, ['Rato', 'Cachorro'], baloes=(1, 8, 3))
    mp.nota('<particulas:moscas>')
    return mp, (10, 13), False


def gusrola():
    mp = Mapa(4)
    examinar(mp, 2, 4, 'Cama', N('A cama do Gusrola. O lençol está', 'molhado... e tem cheiro de lagoa.')
             + say('b', 'Esse menino precisa trocar a roupa', 'de cama!'))
    examinar(mp, 10, 3, 'Estante', N('Uma estante tombada. Atrás dela, um pote:', '"MOSCAS CROCANTES — NÃO MEXER".')
             + say('b', 'Deve ser ração pro peixinho dele.', 'Que fofo!'))
    examinar(mp, 6, 2, 'Janela', N('Pela janela, um sapo te encara.', 'Ele parece... familiar.'))
    examinar(mp, 3, 2, 'Bilhete', N('Um bilhete na parede: "Relatório semanal', 'pro Mestre R. NÃO DEIXAR A TITIA VER."')
             + say('b', 'Mestre R? Deve ser o professor de', 'karatê dele. Que orgulho!'))
    examinar(mp, 8, 5, 'Mesa', N('Na mesa: uma xícara de chá de... água', 'de lagoa? Com uma mosca boiando.'))
    examinar(mp, 11, 8, 'Barril', N('Um barril de água parada. Tem uns', 'ovinhos gelatinosos boiando.')
             + say('b', 'Sagu! O Gusrola adora sobremesa!'))
    examinar(mp, 1, 6, 'Saco', N('Um saco cheio de perucas.')
             + say('b', 'Ele disse que é pra uma festa à', 'fantasia. Que criativo!'))
    examinar(mp, 1, 8, 'Caixa', N('Uma caixa: "PRESENTES PRA TITIA".', 'Está vazia.'))
    examinar(mp, 11, 4, 'Vaso', N('Um vaso quebrado com uma coleção de', 'cascas de besouro.'))
    mp.nota('<particulas:poeira>')
    mp.bgs('Clock', 35)
    return mp, (6, 8), False


def patio():
    mp = Mapa(5)
    lixo = [
        N('Entulho da estação. Um rato faz "shhh"', 'pra você.'),
        N('Uma placa caída: "PRÓXIMO TREM EM:', '37 ANOS".'),
        N('Um carrinho de pipoca abandonado... sem', 'pipoca. Os ratos foram mais rápidos.'),
    ]
    for (x, y) in [(5, 9), (9, 9), (16, 9), (19, 9), (7, 13), (17, 13)]:
        examinar(mp, x, y, 'Entulho', *lixo)
    return mp, (12, 16), False


def estacao():
    mp = Mapa(6)
    for x in (3, 16):
        examinar(mp, x, 2, 'Janela', N('Pela janela quebrada entra um vento', 'gelado... e um morcego. Ops.'),
                 N('Lá fora, a lua cheia ilumina os trilhos.'))
    caixa = [N('Uma caixa: "ENCOMENDA PARA RAULETE —', 'URGENTE". Está aqui há 20 anos.'),
             N('"FRÁGIL". Chegou quebrada, claro.')]
    for (x, y) in [(17, 10), (19, 9), (19, 11)]:
        examinar(mp, x, y, 'Caixa', *caixa)
    examinar(mp, 18, 10, 'Barril', N('Óleo de trem. Cheira a ferrugem e', 'aventura.'))
    examinar(mp, 8, 10, 'Ossos', N('Ossos de... galinha? Alguém fez um', 'churrasco na estação.'))
    for (x, y) in [(1, 3), (13, 4)]:
        examinar(mp, x, y, 'Coluna', N('Uma coluna rachada. Alguém riscou:', '"O trem das 18h nunca veio."'))
    brilho(mp, 6, 9, 'Bilhete', achado('bilhete', 'Bilhete de Trem', 'Recife → Luz da Sé. Validade: 1987.',
                                       'Item_Bilhete', 'b', ('Validade: 1987?!', 'Esse trem não vem mais não...')))
    mp.nota('<particulas:poeira><vinheta:0.4>')
    return mp, (10, 11), False


def diademonius():
    mp = Mapa(7)
    kind14 = range(B.A1 + 14 * 48, B.A1 + 15 * 48)
    for y in range(mp.j['height']):
        for x in range(mp.j['width']):
            if mp.m.get(x, y, 0) in kind14:
                # corrego roxo: bloqueado; nas pontes, regiao 2 = chao seguro (sem dano e sem afundar)
                mp.m.region([(x, y)], 2 if mp.m.get(x, y, 2) in (82, 83) else 1)
    janelas = [
        N('Pela janela: um velhinho careca se', 'olhando no espelho e chorando.'),
        N('Pela janela: um gato dormindo em cima de', 'uma TV de tubo.'),
        N('Pela janela: uma senhora penteando a', 'peruca como se fosse um gatinho.') + say('l', 'Aqui todo mundo usa peruca...'),
    ]
    for (x, y) in [(3, 4), (10, 4), (6, 14), (14, 14)]:
        examinar(mp, x, y, 'Janela', *janelas)
    fogo = rand(N('Alguém está assando... um sapato.', 'O cheiro é melhor do que parece.'),
                N('Uma fogueira quentinha. Leandra esquenta', 'as mãos.') + say('l', 'Ahhh... que gostoso!'))
    for (x, y) in [(23, 4), (30, 7)]:
        trocar_falas(mp, 'Fogo', x, y, fogo)
    examinar(mp, 22, 2, 'Barricada', N('Uma barricada com uma placa: "PROIBIDO', 'PASSAR — ordem do Prefeito (careca)".'))
    examinar(mp, 9, 9, 'Toco', N('Um toco de árvore com um rabisco:', '"O Raulete é careca."')
             + N('Embaixo, outra letra: "E daí? Eu também', 'sou."'))
    poco_jogar = (gold(-1) + se('Water1') + wait(30) + rand(
        N('Ploc! ...O poço devolve a moeda com um', 'bilhete: "Aqui nem desejo se realiza."') + gold(1),
        N('Ploc! Leandra faz um desejo... e nada', 'acontece. Típico de Diademonius.'),
        N('Ploc! Lá do fundo, uma voz: "Valeu!"') + say('L', '...Tem alguém morando aí embaixo?!')))
    poco = (N('Um poço velho. Dizem que ele realiza', 'desejos.')
            + choices([('Jogar uma moeda', if_([7, 1, 0], poco_jogar,
                                              say('L', 'Não tenho nem uma moedinha...'))),
                       ('Só olhar', N('Lá no fundo só tem escuridão... e um', 'pé de chinelo. O direito!'))], cancel=1))
    examinar(mp, 13, 17, 'Poço', poco)
    for (x, y), t in zip([(31, 18), (30, 20), (28, 20)],
                         [('"Aqui jaz Dona Cotinha. Foi comprar pão e', 'o padeiro era o Raulete."'),
                          ('"Aqui jaz um careca. A peruca foi', 'enterrada separada."'),
                          ('"Aqui jaz o último fio de cabelo de', 'Diademonius. Saudades eternas."')]):
        examinar(mp, x, y, 'Túmulo', N(*t))
    loja = [N('Mercadoria do Sabino: "Guarda-chuva sem', 'pano — 30G".'),
            N('Mercadoria do Sabino: "Pente para', 'carecas — 5G". O mais vendido da cidade!'),
            N('Mercadoria do Sabino: "Peruca usada', '(pouco usada, juro)".')]
    for (x, y) in [(27, 3), (29, 3), (30, 4), (26, 5)]:
        examinar(mp, x, y, 'Mercadoria', *loja)
    arvore = [N('Uma árvore seca, sem nenhuma folha.') + say('l', 'Até as árvores daqui são carecas...'),
              N('Na árvore tem um ninho... vazio. Até os', 'passarinhos se mudaram.')]
    for (x, y) in [(8, 2), (17, 3), (17, 12), (31, 13), (7, 18)]:
        examinar(mp, x, y, 'Árvore seca', *arvore)
    corrego = [N('O córrego brilha num roxo meio', 'fluorescente.'),
               N('Um peixe de três olhos pula do córrego e', 'pisca pra você.') + say('l', 'Ele piscou com os três olhos!'),
               N('O córrego borbulha. Cheira a ovo podre', 'e a desilusão.')]
    for (x, y) in [(19, 11), (22, 15)]:
        examinar(mp, x, y, 'Córrego', *corrego)
    entulho = [N('Entulho. No meio dele, um pente sem', 'nenhum dente. Faz sentido aqui.'),
               N('Um tijolo com um recado: "Prefeitura —', 'obra iniciada em 1998."')]
    for (x, y) in [(6, 20), (16, 19), (2, 16), (15, 9)]:
        examinar(mp, x, y, 'Entulho', *entulho)
    examinar(mp, 5, 10, 'Barril', N('Um barril de "água potável". Ela está', 'verde.') + say('l', 'Acho que vou passar...'))
    examinar(mp, 8, 15, 'Vaso', N('Um vaso com uma planta de plástico.', 'A coisa mais viva da rua.'))
    bicho(mp, 23, 9, 'Porco', img('Nature', 2, 2),
          N('Óinc! O porco está mais bem alimentado', 'que a cidade inteira.'),
          N('O porco rola na lama roxa do córrego.', 'Ele parece muito feliz.'))
    bicho(mp, 10, 17, 'Cachorro', img('Nature', 0, 2),
          perseguicao_do_cachorro(),
          N('O cachorro cheira o seu pé e espirra.') + say('l', 'Saúde!'), som='Dog')
    vida(mp, ['Seu Joaquim', 'Dona Perpétua', 'Zé do Córrego', 'Guarda Bento', 'Sabino', 'Tia Nena', 'Capivara',
              'Porco', 'Cachorro'], baloes=(8, 3, 10, 6, 1, 7))
    mp.nota('<particulas:cinzas>')
    return mp, (4, 5), False


def casa_leandra():
    mp = Mapa(8)
    examinar(mp, 7, 5, 'Mesa', N('Uma caneca com um resto de cerveja quente.')
             + N('A mamãe guarda pra "mais tarde".'))
    examinar(mp, 1, 5, 'Saco', N('Um saco de arroz com três grãos dentro.')
             + say('l', 'Um, dois, três... o almoço da semana!'))
    uma_vez(mp, 1, 8, 'Caixa', N('Uma caixa: "BRINQUEDOS DA LEANDRA".', 'Dentro, uma pedra com olhinhos desenhados.')
            + achado('pedrinha', 'Pedrinha', 'A melhor amiga da Leandra. Tem olhinhos desenhados.', 'Item_Pedrinha',
                     'l', ('Vem comigo, Pedrinha! A gente vai', 'pedir esmola juntas.')),
            [N('A caixa de brinquedos está vazia agora.', 'A Pedrinha está no bolso da Leandra.')])
    examinar(mp, 11, 3, 'Vaso', N('Um vaso quebrado com uma flor de', 'plástico. A única flor que sobrevive aqui.'))
    for x in (6, 8):
        examinar(mp, x, 5, 'Banquinho', N('Um banquinho bambo. Sentar nele exige', 'equilíbrio de circo.'))
    examinar(mp, 10, 8, 'Tábuas', N('Tábuas soltas. A mamãe chama isso de', '"reforma".'))
    examinar(mp, 11, 7, 'Barril', N('Um barril de água com uma rachadura. A', 'água foi embora junto com a esperança.'))
    for x in (3, 9):
        examinar(mp, x, 2, 'Rachadura', N('Uma rachadura na parede. Dá pra ver o', 'vizinho... e o vizinho te vê também.')
                 + say('l', 'Oi, vizinho!'))
    mp.nota('<particulas:poeira>')
    mp.j['autoplayBgs'] = True; mp.j['bgs'] = audio('Clock', 30)
    return mp, (6, 8), False


def cela():
    mp = Mapa(9)
    examinar(mp, 10, 7, 'Grades', N('Pelas grades: outro esqueleto... usando', 'uma peruca torta. Ironia pura.'))
    examinar(mp, 17, 4, 'Mesa', N('A mesa do carcereiro: um baralho, meio', 'pão e um bilhete:')
             + N('"Turno da noite: NÃO DORMIR (de novo)."'))
    examinar(mp, 15, 6, 'Caixa', N('Uma caixa: "CONDICIONADOR PARA PERUCAS', '— USO EXCLUSIVO DA FAMÍLIA".'))
    examinar(mp, 17, 6, 'Barril', N('Um barril de "xampu anticaspa', 'industrial". O cheiro arde o nariz.')
             + say('o', 'Argh! Até o meu cabelo ficou com medo.'))
    for x in (1, 6):
        examinar(mp, x, 9, 'Entulho', N('Entulho. Um rato carcereiro faz a ronda', 'por aqui.'))
    bicho(mp, 9, 9, 'Rato', img('$Rato', 0, 4), se('Cancel2') + N('O rato carcereiro te olha feio.'),
          N('O rato está roendo uma peruca velha.'), speed=4)
    mp.nota('<particulas:poeira><vinheta:0.55>')
    return mp, (8, 8), False


def laboratorio():
    mp = Mapa(10)
    monitores = [N('O monitor mostra: "CABELO.EXE parou de', 'funcionar."'),
                 N('Câmera de segurança ao vivo: o Raulete', 'escovando a peruca e cantando.'),
                 N('Na tela: "Peruca nº 348 — status:', 'APODRECENDO".')]
    for x in (4, 9, 15, 20):
        examinar(mp, x, 8, 'Monitor', *monitores)
    alarme = (N('Um botão vermelho: "NÃO APERTE".')
              + choices([('Apertar', pose(-1, 'soco', espera=8) + se('Siren') + flash([255, 40, 40, 200], 20) + shake(5, 9, 15)
                          + N('UÓÓÓÓ! Uma voz robótica anuncia:') + N('"PEGADINHA DO MALANDRO!"')
                          + say('o', 'Que tipo de laboratório tem isso?!')),
                         ('Não apertar', say('l', 'Melhor não...'))], cancel=1))
    for x in (10, 14):
        examinar(mp, x, 8, 'Botão', alarme)
    for x in (5, 19):
        examinar(mp, x, 8, 'Cartaz', N('Cartaz: "RAULETE — Funcionário do Mês.', 'Todo mês. Desde sempre."'))
    examinar(mp, 11, 8, 'Placa', N('Placa: "CUIDADO: ÁREA DE CALVÍCIE', 'CONTAGIOSA".') + say('o', 'Não respira, Leandra!'))
    examinar(mp, 13, 8, 'Placa', N('Placa: "PROIBIDO ENTRAR DE BONÉ".'))
    examinar(mp, 4, 3, 'Pastas', N('Pastas: "Clientes satisfeitos: 0.', 'Clientes carecas: todos."'))
    examinar(mp, 9, 5, 'Maca', N('Uma maca com um secador de cabelo', 'gigante preso no teto.') + say('l', 'Melhor não deitar aí...'))
    for x in (15, 18):
        examinar(mp, x, 3, 'Manequim', N('Um manequim com a peruca "Rapunzel', 'Deluxe". Preço: uma infância inteira.'))
    for x in (20, 23):
        examinar(mp, x, 3, 'Servidor', N('Servidores zumbindo. Etiqueta: "BACKUP', 'DAS PERUCAS — NÃO DESLIGAR".'))
    examinar(mp, 8, 10, 'Tubos de ensaio', N('Tubos de ensaio: "Fórmula do cabelo loiro', '— tentativa nº 2.847". Todas deram errado.'))
    examinar(mp, 16, 10, 'Notebook', N('Um notebook aberto em "perucas baratas —', 'compre 3 e leve 1 careca".'))
    mp.tile(1, 11, 2, 211)
    mp.tile(1, 12, 2, 219)
    chutar = (pose(-1, 'chute', espera=10) + N('Leandra dá um chute na máquina!') + se('Blow3') + shake(6, 9, 12) + wait(20)
              + se('Item3') + N('POC! Cai alguma coisa lá embaixo...')
              + item(IT['pastel'], 1)
              + destaque('item', imagem='Item_Pastel', nome='Pastel de Vento',
                         texto='Só tem vento dentro. Recupera 1 de vida (e a esperança).')
              + say('o', 'Você roubou uma máquina de lanche.', 'Estou orgulhosa.'))
    uma_vez(mp, 1, 12, 'Máquina de lanches',
            N('Máquina de lanches: "PASTEL DE VENTO —', 'R$ 0,00 — ESGOTADO".')
            + choices([('Chutar a máquina', chutar), ('Deixar pra lá', [])], cancel=1),
            [N('A máquina pisca: "AGORA SIM, ESGOTADO".')])
    return mp, (12, 15), False


def rio():
    mp = Mapa(11)
    mp.tile(9, 14, 2, 177)
    examinar(mp, 9, 14, 'Placa', N('Placa: "PONTE DA FAMÍLIA RAULETE. Proibido', 'correr, pular, gritar e fugir."')
             + N('Embaixo, rabiscado: "...e ser feliz".'))
    pedras = [N('Uma pedra com uma inscrição: "Kura esteve', 'aqui". Embaixo: "Kura é chato".'),
              N('Uma pedra lisinha, lisinha... igual à', 'cabeça do Raulete.')]
    for (x, y) in [(4, 14), (20, 15), (8, 16)]:
        examinar(mp, x, y, 'Pedra', *pedras)
    agua = [N('A correnteza é fortíssima. Passa boiando', 'um chinelo... e depois o outro chinelo.'),
            N('A água ruge lá embaixo.') + say('o', 'Se alguém cair aí, nunca mais volta.')]
    for x in (6, 18):
        examinar(mp, x, 11, 'Rio', *agua)
    mp.nota('<neblina:45><particulas:gotas>')
    return mp, (12, 16), False


def casa_baratelli():
    mp = Mapa(12)
    for x in (2, 3):
        examinar(mp, x, 3, 'Estante', N('Livros: "Astrologia para Iniciantes",', '"Leitura de Mão sem Calo" e...')
                 + N('..."Como Esquecer um Cigano em 7 Dias",', 'marcado na página 1.'))
    examinar(mp, 10, 3, 'Espelho', N('Baratelli se olha no espelho... a flor na', 'cabeça perdeu mais uma pétala.')
             + balloon(-1, 6) + say('b', 'Calma, florzinha. Eu vou te salvar.'))
    examinar(mp, 12, 4, 'Cama', N('A cama ainda tem o formato da Baratelli.')
             + say('b', 'Dá vontade de deitar e chorar... mas', 'a vingança não espera!'))
    examinar(mp, 7, 2, 'Quadro', N('Um quadro de Recife ao pôr do sol.')
             + say('b', 'Saudade de quando o maior problema era', 'chegar atrasada na aula...'))
    examinar(mp, 3, 7, 'Bola de cristal', N('A bola de cristal mostra... a cara da', 'própria Baratelli.')
             + say('k', 'Isso é o reflexo, Baratelli.'))
    for (x, y) in [(1, 3), (13, 9), (1, 9)]:
        examinar(mp, x, y, 'Planta', N('Uma planta que a Baratelli rega todo dia.')
                 + say('b', 'Pelo menos você nunca me traiu,', 'Dona Samambaia.'))
    for x in (5, 9):
        examinar(mp, x, 2, 'Janela', N('Pela janela: São Matheos ao longe... e um', 'portal roxo se fechando no céu.'))
    mp.nota('<particulas:poeira>')
    mp.j['autoplayBgs'] = True; mp.j['bgs'] = audio('Clock', 30)
    return mp, (7, 9), False


def morro():
    mp = Mapa(13)
    sacudir = (pose(-1, 'soco', espera=8) + N('Baratelli sacode a árvore com força!') + se('Wind4') + shake(4, 9, 12) + wait(20)
               + rand(item(IT['banana'], 1) + se('Item1')
                      + destaque('item', imagem='Item_Banana', nome='Banana', texto='Recupera 150 de vida. Os macacos que lutem.'),
                      se('Macaco', pitch=115) + N('Cai uma banana... e um macaco pega no', 'ar e sai correndo!')
                      + say('k', 'Que ladrão!')))
    import build_morro as BM
    for (x, y) in BM.ARVORES:
        uma_vez(mp, x, y, 'Árvore', N('Uma árvore com cachos de banana.')
                + choices([('Sacudir a árvore', sacudir), ('Deixar quieta', [])], cancel=1),
                [N('A árvore já foi sacudida. Só sobrou', 'casca de banana no chão.')])
    examinar(mp, BM.MIRANTE[0], BM.MIRANTE[1], 'Mirante', N('Daqui de cima dá pra ver São Matheos', 'inteira... e o lixo de São Matheos inteiro.'),
             N('Lá longe, algo brilha no norte... é a', 'Mansão Raulete ou a careca dele?') + say('k', 'Com certeza é a careca.'))
    mp.nota('<particulas:folhas>')
    return mp, BM.INICIO, True


def vidente():
    mp = Mapa(14)
    for x in (2, 3, 4):
        examinar(mp, x, 3, 'Estante', N('Livros: "Horóscopo do Mês Passado",', '"Tarô para Leigos" e...')
                 + N('..."Como Prever o Futuro e Mesmo Assim', 'Ser Surpreendida".'))
    examinar(mp, 13, 3, 'Frascos', N('Frascos: "Chá de Arruda", "Óleo de', 'Peroba" e "Tônico Capilar (vencido)".'))
    examinar(mp, 15, 4, 'Cama', N('Embaixo do travesseiro da vidente: uma', 'foto rasgada de uma menina loira.')
             + say('b', '...Quem será?'))
    examinar(mp, 12, 4, 'Mesa', N('Cartas de tarô espalhadas na mesa.', 'A de cima é "A Traição".')
             + say('k', 'Isso não é um bom sinal...'))
    examinar(mp, 1, 4, 'Pote', N('Um pote com cheiro de incenso de lavanda...', 'e de mistério.'))
    examinar(mp, 15, 9, 'Pote', N('Um pote de "cinzas sagradas".') + say('k', 'Ou é só cinza de incenso?'))
    for (x, y) in [(14, 10), (2, 9)]:
        examinar(mp, x, y, 'Cristal', N('Um cristal enorme. Ele brilha mais forte', 'quando você pensa na Peruca Dourada.'))
    examinar(mp, 1, 10, 'Ossos', N('Ossos no canto da sala.') + say('v', 'De um cliente que não pagou a', 'consulta. Hihihi!'))
    for x in (5, 11):
        examinar(mp, x, 2, 'Tapeçaria', N('Uma tapeçaria antiga com duas figuras', 'lendárias...')
                 + N('...uma delas parece dizer "que gracinha!".'))
    mp.nota('<particulas:estrelinhas><vinheta:0.45>')
    mp.j['autoplayBgs'] = True; mp.j['bgs'] = audio('Fire1', 25)
    return mp, (8, 11), False


# =================================================================================================
def itens():
    it = load('Items.json')
    while len(it) <= max(IT.values()):
        it.append(None)
    chave = it[31]
    pocao = it[7]

    def k(iid, nome, icon, desc):
        d = copy.deepcopy(chave)
        d.update({'id': iid, 'name': nome, 'iconIndex': icon, 'description': desc})
        it[iid] = d

    def c(iid, nome, icon, desc, hp):
        d = copy.deepcopy(pocao)
        d.update({'id': iid, 'name': nome, 'iconIndex': icon, 'description': desc, 'price': 0})
        d['effects'] = [{'code': 11, 'dataId': 0, 'value1': 0, 'value2': hp}]
        it[iid] = d
    k(IT['tampinha'], 'Tampinha de Garrafa', 162, 'Achada na praia de Recife.\nVale ouro! (Não vale.)')
    k(IT['bilhete'], 'Bilhete de Trem', 197, 'Recife → Luz da Sé.\nValidade: 1987.')
    k(IT['chinelo'], 'Pé de Chinelo Esquerdo', 293, 'Achado no lixo de São Matheos.\nProcura-se o pé direito.')
    k(IT['pedrinha'], 'Pedrinha', 160, 'A melhor amiga da Leandra.\nTem olhinhos desenhados.')
    c(IT['pastel'], 'Pastel de Vento', 266, 'Só tem vento dentro.\nRecupera 1 de vida (e a esperança).', 1)
    c(IT['coco'], 'Água de Coco', 273, 'Direto do coqueiro de Recife.\nRecupera 200 de vida.', 200)
    c(IT['banana'], 'Banana', 265, 'Do Morro do Macaco.\nRecupera 150 de vida.', 150)
    k(IT['banana_dourada'], 'Banana Dourada', 265, 'O pedágio do Rei Macaco.\nEle quer três.')
    k(IT['chave'], 'Chave Enferrujada', 195, 'Abre o cadeado da Estação Luz da Sé.')
    save('Items.json', it)

    s = load('System.json')
    s['variables'][V_RAND] = 'Aleatório (cenário)'
    save('System.json', s)


def main():
    B.TILESETS = load('Tilesets.json')
    itens()
    total = 0
    for fn in (recife, matheos, gusrola, patio, estacao, diademonius, casa_leandra, cela, laboratorio, rio,
               casa_baratelli, morro, vidente):
        mp, start, jumps = fn()
        ruins = mp.verificar(start, jumps)
        for r in ruins:
            print('  AVISO mapa', mp.mid, r)
        mp.save()
        total += len(mp.novos)
        print(f'mapa {mp.mid:2d}: +{len(mp.novos)} eventos')
    pl = open(f'{B.PROJ}/js/plugins.js', encoding='utf-8').read()
    if '"Ambiente"' not in pl:
        entry = '{"name":"Ambiente","status":true,"description":"Partículas e vinheta por mapa.","parameters":{}}'
        pl = pl.replace('\n];', ',\n' + entry + '\n];')
        open(f'{B.PROJ}/js/plugins.js', 'w', encoding='utf-8', newline='\n').write(pl)
    print('total de eventos novos:', total)


if __name__ == '__main__':
    main()
