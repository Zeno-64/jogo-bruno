# Troca o miado ('Cat') dos macacos pelo som novo 'Macaco' (o macaco que ronca usa 'Sleep').
# Altera os builders (para as proximas montagens) e o Map013.json direto, com troca atomica do
# arquivo (o jogo aberto nunca le um arquivo pela metade; a mudanca vale ao entrar no morro de novo).
import json, os, re, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = 'K:/Kevin/workspace/jogo-bruno'


def novo_tom(p):
    return {90: 100, 110: 100, 120: 105, 130: 110, 140: 115, 150: 120, 160: 125}.get(p, 110)


# ---- builders
for nome in ('build_morro.py', 'build_env.py'):
    path = os.path.join(HERE, nome)
    s = open(path, encoding='utf-8').read()
    s = s.replace("se('Cat', pitch=90, vol=50) + balloon(0, 10) + narr('O macaco do ninho ronca.",
                  "se('Sleep', vol=60) + balloon(0, 10) + narr('O macaco do ninho ronca.")
    s = re.sub(r"se\('Cat', pitch=(\d+)\)", lambda m: f"se('Macaco', pitch={novo_tom(int(m.group(1)))})", s)
    open(path, 'w', encoding='utf-8').write(s)
    print(nome, 'Cat restantes:', s.count("'Cat'"))

# ---- Map013.json (Morro do Macaco)
path = PROJ + '/data/Map013.json'
j = json.load(open(path, encoding='utf-8-sig'))
n = 0
for ev in j['events']:
    if not ev:
        continue
    for pg in ev['pages']:
        for c in pg['list']:
            if c['code'] == 250 and c['parameters'][0].get('name') == 'Cat':
                a = c['parameters'][0]
                if a.get('pitch') == 90:
                    a.update({'name': 'Sleep', 'pitch': 100, 'volume': 60})
                else:
                    a.update({'name': 'Macaco', 'pitch': novo_tom(a.get('pitch', 100))})
                n += 1
tmp = path + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(j, f, ensure_ascii=False, separators=(',', ':'))
for tentativa in range(20):
    try:
        os.replace(tmp, path)
        break
    except PermissionError:
        time.sleep(0.25)
print('Map013: sons trocados =', n)
