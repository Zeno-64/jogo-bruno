# Batalha em visao lateral, inimigos vivos e registro dos plugins novos.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_ch1 import PROJ, load, save

PLUGINS = [
    ('Patrulhas', 'Bichos com movimento esperto: patrulha com faro e corrida em fila.'),
    ('MapaVivo', 'Tiles que mudam, pedras que desmoronam, chão escorregadio e pulos seguros.'),
    ('BatalhaViva', 'Inimigos vivos na batalha e ajustes da visão lateral.'),
]

# inimigo -> (nota, posicao na tropa em visao lateral)
INIMIGOS = {
    6: ('<vivo:flutuar>\n<escala:0.82>\n<sombra:0.5>', (236, 418)),                          # Kura
    7: ('<vivo:pular>\n<somPulo:Frog>\n<escala:0.85>\n<sombra:0.62>\n<sombraY:-14>', (240, 430)),  # Gusrola Sapo
}


def main():
    s = load('System.json')
    s['optSideView'] = True
    save('System.json', s)

    a = load('Actors.json')
    for ator in a[1:6]:
        if ator:
            ator['battlerName'] = ''   # o plugin usa SV_<sprite do mapa>
    save('Actors.json', a)

    en = load('Enemies.json')
    tr = load('Troops.json')
    for eid, (nota, (x, y)) in INIMIGOS.items():
        en[eid]['note'] = nota
        for t in tr:
            if t and t['members'] and all(m['enemyId'] == eid for m in t['members']):
                for m in t['members']:
                    m['x'], m['y'] = x, y
    save('Enemies.json', en)
    save('Troops.json', tr)

    path = PROJ + '/js/plugins.js'
    pl = open(path, encoding='utf-8').read()
    pl = pl.replace('"description":"Bloqueia a passagem nos tiles marcados com a região 1."',
                    '"description":"Região 1 bloqueia a passagem; região 2 é chão seguro (pontes)."')
    for nome, desc in PLUGINS:
        if f'"name":"{nome}"' not in pl:
            entry = json.dumps({'name': nome, 'status': True, 'description': desc, 'parameters': {}},
                               ensure_ascii=False, separators=(',', ':'))
            pl = pl.replace('\n];', ',\n' + entry + '\n];')
    open(path, 'w', encoding='utf-8', newline='\n').write(pl)
    print('batalha lateral: ok')


if __name__ == '__main__':
    main()
