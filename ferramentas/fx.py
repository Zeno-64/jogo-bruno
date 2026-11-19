# Atalhos para o plugin Destaques: itens e eventos importantes com imagem, animacao e transicao.


def _cmd(code, params, ind=0):
    return {'code': code, 'indent': ind, 'parameters': params}


def destaque(tipo, nome='', texto='', titulo='', imagem='', rosto='', personagem='', indice=0, icone=0,
             tamanho=0, ind=0):
    args = {'tipo': tipo, 'imagem': imagem, 'rosto': rosto, 'personagem': personagem, 'indice': str(indice),
            'icone': str(icone), 'tamanho': str(tamanho), 'titulo': titulo, 'nome': nome, 'texto': texto}
    return [_cmd(357, ['Destaques', 'mostrar', 'Mostrar destaque', args], ind)]


def capitulo(imagem, ind=0):
    """Cartao de capitulo em tela cheia: escurece, aproxima devagar, faixa de brilho e faiscas."""
    return destaque('capitulo', imagem=imagem, ind=ind)


def move_pic_e(pid, x, y, opacity, dur, scale=100, origin=1, easing=2, w=False, ind=0):
    """Mover imagem com suavizacao (0 constante, 1 acelera, 2 desacelera, 3 os dois)."""
    return [_cmd(232, [pid, None, origin, 0, x, y, scale, scale, opacity, 0, dur, w, easing], ind)]


def _alvo(char):
    if char == -1:
        return '$gamePlayer'
    if char == 0:
        return 'this.character(0)'
    if isinstance(char, str):
        return char
    return f'$gameMap.event({char})'


def pose(char, nome='', segurar=False, repetir=False, velocidade=7, espera=0, olhar=None, ind=0):
    """Pose de acao (plugin Poses): chute, soco, dor, queda, magia, cansado, choro, riso, pulo, facada, rastejar."""
    a = _alvo(char)
    js = f'{a}.turnTowardCharacter({_alvo(olhar)}); ' if olhar is not None else ''
    js += (f"{a}.pose('{nome}', {{segurar: {str(segurar).lower()}, repetir: {str(repetir).lower()}, "
           f"velocidade: {velocidade}}});")
    return [_cmd(355, [js], ind)] + ([_cmd(230, [espera], ind)] if espera else [])
