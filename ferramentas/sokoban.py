# Solucionador do quebra-cabeca das estatuas (2o andar do templo): estatuas distintas, cada uma no seu alvo.
from collections import deque

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def alcance(livres, bloq, ini):
    vis = {ini}; q = deque([ini])
    while q:
        x, y = q.popleft()
        for dx, dy in DIRS:
            n = (x + dx, y + dy)
            if n in livres and n not in bloq and n not in vis:
                vis.add(n); q.append(n)
    return vis


def resolver(livres, estatuas, alvos, jogador, limite=400000):
    """estatuas/alvos: tuplas na mesma ordem (estatua i vai para alvo i). Retorna (empurroes, caminho) ou None."""
    ini = (min(alcance(livres, set(estatuas), jogador)), tuple(estatuas))
    vistos = {ini: None}; q = deque([(ini, 0)])
    while q:
        (pj, est), n = q.popleft()
        if est == tuple(alvos):
            caminho = []; s = (pj, est)
            while vistos[s]:
                s, mov = vistos[s]; caminho.append(mov)
            return n, caminho[::-1]
        bloq = set(est)
        area = alcance(livres, bloq, pj)
        for i, (sx, sy) in enumerate(est):
            for dx, dy in DIRS:
                atras = (sx - dx, sy - dy); frente = (sx + dx, sy + dy)
                if atras in area and frente in livres and frente not in bloq:
                    nova = list(est); nova[i] = frente
                    nova = tuple(nova)
                    npj = min(alcance(livres, set(nova), (sx, sy)))
                    s = (npj, nova)
                    if s not in vistos:
                        vistos[s] = ((pj, est), (i, (dx, dy)))
                        q.append((s, n + 1))
                        if len(vistos) > limite:
                            return None
    return None


def de_ascii(linhas, x0=0, y0=0):
    livres = set(); est = {}; alvos = {}; jog = None
    for y, l in enumerate(linhas):
        for x, ch in enumerate(l):
            p = (x0 + x, y0 + y)
            if ch != '#':
                livres.add(p)
            if ch in 'DPB':
                est[ch] = p
            if ch in 'dpb':
                alvos[ch.upper()] = p
            if ch == '@':
                jog = p
    return livres, est, alvos, jog


if __name__ == '__main__':
    import sys
    # D = Dourada, P = Prata, B = Bronze; minusculas = placas (p=1o, b=2o, d=3o)
    sala = [
        '###############',
        '#....b.p.d....#',
        '#.##.......##.#',
        '#....#.#.#....#',
        '#.#.P..#..B.#.#',
        '#...#.....#...#',
        '#.#...#D#...#.#',
        '#...#.....#...#',
        '#.....#@#.....#',
        '###############',
    ]
    livres, est, alvos, jog = de_ascii(sala)
    ordem = ['D', 'P', 'B']
    r = resolver(livres, [est[k] for k in ordem], [alvos[k] for k in ordem], jog)
    print('empurroes:', r[0] if r else None)
