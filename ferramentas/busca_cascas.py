# Procura um bom desenho para a Ilha das Cascas (puzzle de deslizar):
# solucao com varios movimentos, banana fora do caminho obvio e nenhuma posicao sem volta.
import random
from collections import deque

COLS, ROWS = 9, 7
ENTRADA = (8, 3)          # coluna 8 (borda leste), linha do meio: chao normal
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def deslizar(pos, d, pedras):
    x, y = pos
    passou = []
    while True:
        nx, ny = x + d[0], y + d[1]
        if not (0 <= nx < COLS and 0 <= ny < ROWS) or (nx, ny) in pedras:
            break
        x, y = nx, ny
        passou.append((x, y))
        if (x, y) == ENTRADA:
            break
    return (x, y), passou


def resolver(pedras, banana):
    ini = (ENTRADA, False)
    dist = {ini: 0}
    pai = {}
    q = deque([ini])
    while q:
        st = q.popleft()
        pos, tem = st
        for d in DIRS:
            if pos == ENTRADA and d == (1, 0):
                continue  # sair da ilha
            novo, passou = deslizar(pos, d, pedras)
            if novo == pos:
                continue
            t2 = tem or banana in passou
            st2 = (novo, t2)
            if st2 not in dist:
                dist[st2] = dist[st] + 1
                pai[st2] = (st, d)
                q.append(st2)
    alvo = (ENTRADA, True)
    if alvo not in dist:
        return None
    # sem beco sem saida: de todo estado alcancado da para voltar a entrada
    for st in dist:
        pos, tem = st
        seen = {st}
        q = deque([st])
        ok = False
        while q:
            s = q.popleft()
            if s[0] == ENTRADA:
                ok = True
                break
            for d in DIRS:
                n, passou = deslizar(s[0], d, pedras)
                s2 = (n, s[1] or banana in passou)
                if n != s[0] and s2 not in seen:
                    seen.add(s2)
                    q.append(s2)
        if not ok:
            return None
    # caminho
    cam = []
    st = alvo
    while st in pai:
        st, d = pai[st]
        cam.append(d)
    cam.reverse()
    # movimentos ate pegar a banana
    ate = min(v for (p, t), v in dist.items() if t)
    return dist[alvo], ate, cam


def main():
    rng = random.Random(11)
    melhor = None
    livres = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) != ENTRADA]
    for _ in range(60000):
        n = rng.randint(8, 13)
        pedras = set(rng.sample([p for p in livres if p != (7, 3)], n))
        candidatos = [p for p in livres if p not in pedras and 1 <= p[0] <= 6 and 1 <= p[1] <= 5]
        if not candidatos:
            continue
        banana = rng.choice(candidatos)
        r = resolver(pedras, banana)
        if not r:
            continue
        total, ate, cam = r
        direcoes = len(set(cam))
        if direcoes < 4 or ate < 5:
            continue
        nota = ate * 3 + total
        if total > 13:
            continue
        if not melhor or nota > melhor[0]:
            melhor = (nota, total, ate, sorted(pedras), banana, cam)
    nota, total, ate, pedras, banana, cam = melhor
    print('movimentos ate a banana:', ate, '| ida e volta:', total)
    print('pedras =', pedras)
    print('banana =', banana)
    nomes = {(1, 0): 'L', (-1, 0): 'O', (0, 1): 'S', (0, -1): 'N'}
    print('solucao:', ''.join(nomes[d] for d in cam))
    for r in range(ROWS):
        print(''.join('E' if (c, r) == ENTRADA else 'R' if (c, r) in pedras else 'B' if (c, r) == banana else '~'
                      for c in range(COLS)))


if __name__ == '__main__':
    main()
