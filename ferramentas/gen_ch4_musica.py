# Capitulo 4: musicas originais geradas por sintese (numpy) e codificadas em OGG com ponto de loop.
#  - Floresta_Mauara: groove funk sincopado + ocarina misteriosa de floresta (melodias proprias).
#  - Templo_Xavasca: balada pop dramatica + romance frances (orgao, acordeao, coro "ah").
#  - Corrida_Uma: tema de corrida heroico, galope e metais.
import math, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = 'K:/Kevin/workspace/jogo-bruno'
BGM = PROJ + '/audio/bgm/'
OUT_WAV = HERE + '/musica/'
os.makedirs(OUT_WAV, exist_ok=True)
SR = 44100
RNG = np.random.default_rng(7)

NOMES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
         'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11}


def midi(n):
    if isinstance(n, (int, float)):
        return n
    nome, oit = n[:-1], int(n[-1])
    return 12 * (oit + 1) + NOMES[nome]


def freq(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tempo(dur):
    return np.arange(int(round(dur * SR))) / SR


# ---------------------------------------------------------------- envelopes e filtros
def adsr(n_nota, n_total, a=0.01, d=0.1, s=0.7, r=0.1):
    e = np.zeros(n_total)
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = max(1, min(na, n_nota)); nd = max(1, min(nd, max(1, n_nota - na)))
    e[:na] = np.linspace(0, 1, na, endpoint=False)
    e[na:na + nd] = np.linspace(1, s, nd, endpoint=False)
    if na + nd < n_nota:
        e[na + nd:n_nota] = s
    nivel = e[n_nota - 1] if n_nota > 0 else 0
    fim = min(n_total, n_nota + nr)
    if fim > n_nota:
        e[n_nota:fim] = nivel * np.exp(-np.linspace(0, 6, fim - n_nota))
    return e


def filtro_fft(x, lo=None, hi=None, ordem=2):
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    H = np.ones_like(f)
    if hi:
        H *= 1 / np.sqrt(1 + (f / hi) ** (2 * ordem))
    if lo:
        H *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * ordem))
    return np.fft.irfft(X * H, n)


def aditivo(f0, dur, amps, vib=0.0, vib_hz=5.5, vib_atraso=0.15, detune=0.0, fase0=None):
    t = tempo(dur)
    f = f0 * 2 ** (detune / 1200)
    if vib:
        rampa = np.clip((t - vib_atraso) / 0.25, 0, 1)
        inst = f * (1 + vib * rampa * np.sin(2 * np.pi * vib_hz * t))
        fase = 2 * np.pi * np.cumsum(inst) / SR
    else:
        fase = 2 * np.pi * f * t
    out = np.zeros_like(t)
    for k, a in enumerate(amps, 1):
        if a == 0 or k * f > SR * 0.45:
            continue
        ph = RNG.uniform(0, 2 * np.pi) if fase0 is None else fase0
        out += a * np.sin(k * fase + ph)
    return out


def serra(n, rolloff=0.0):
    return [1 / k * math.exp(-rolloff * (k - 1)) for k in range(1, n + 1)]


def quadrada(n, rolloff=0.0):
    return [(1 / k if k % 2 else 0) * math.exp(-rolloff * (k - 1)) for k in range(1, n + 1)]


# ---------------------------------------------------------------- instrumentos (retornam mono)
def i_kick(dur, vel):
    t = tempo(0.42)
    f = 46 + 110 * np.exp(-t * 28)
    fase = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(fase) * np.exp(-t * 7.5)
    clique = RNG.normal(0, 1, len(t)) * np.exp(-t * 400) * 0.35
    return (x + clique) * vel


def i_snare(dur, vel):
    t = tempo(0.3)
    ruido = filtro_fft(RNG.normal(0, 1, len(t)), lo=1200, hi=9000) * np.exp(-t * 17)
    corpo = np.sin(2 * np.pi * 186 * t) * np.exp(-t * 26) * 0.7
    return (ruido * 0.9 + corpo) * vel * 0.8


def i_clap(dur, vel):
    t = tempo(0.32)
    base = filtro_fft(RNG.normal(0, 1, len(t)), lo=900, hi=6000)
    env = np.zeros_like(t)
    for k in range(3):
        a = int(k * 0.011 * SR)
        env[a:] += np.exp(-(t[:len(t) - a]) * 90) * (0.7 if k < 2 else 1)
    env += np.exp(-t * 14) * 0.35
    return base * env * vel * 0.8


def i_hat(dur, vel, aberto=False):
    t = tempo(0.5 if aberto else 0.09)
    x = filtro_fft(RNG.normal(0, 1, len(t)), lo=6500, hi=15000)
    return x * np.exp(-t * (9 if aberto else 70)) * vel * 0.5


def i_shaker(dur, vel):
    t = tempo(0.08)
    x = filtro_fft(RNG.normal(0, 1, len(t)), lo=4000, hi=11000)
    env = np.minimum(t / 0.015, 1) * np.exp(-t * 45)
    return x * env * vel * 0.32


def i_conga(dur, vel, f0=220):
    t = tempo(0.3)
    f = f0 * (1 + 0.25 * np.exp(-t * 40))
    fase = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(fase) * np.exp(-t * 16) + 0.15 * RNG.normal(0, 1, len(t)) * np.exp(-t * 120)) * vel * 0.6


def i_crash(dur, vel):
    t = tempo(2.6)
    x = filtro_fft(RNG.normal(0, 1, len(t)), lo=3000, hi=14000)
    return x * np.exp(-t * 1.6) * vel * 0.45


def i_timpani(dur, vel, f0=73.4):
    t = tempo(1.2)
    x = (np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 1.5 * t) + 0.25 * np.sin(2 * np.pi * f0 * 1.98 * t))
    return (x * np.exp(-t * 3.2) + 0.2 * filtro_fft(RNG.normal(0, 1, len(t)), hi=800) * np.exp(-t * 30)) * vel * 0.55


def nota_generica(f0, dur, vel, amps, a, d, s, r, vib=0.0, detunes=(0,), brilho_env=None):
    n_nota = int(dur * SR)
    n_total = n_nota + int(r * SR) + 10
    x = np.zeros(n_total)
    for dt in detunes:
        x += aditivo(f0, n_total / SR, amps, vib=vib, detune=dt)
    x /= len(detunes)
    return x * adsr(n_nota, n_total, a, d, s, r) * vel


def i_baixo(f0, dur, vel):
    n_nota = int(dur * SR); n_total = n_nota + int(0.06 * SR)
    t = tempo(n_total / SR)
    amps = [1, 0.55, 0.42, 0.3, 0.22, 0.16, 0.11, 0.08, 0.05, 0.03]
    x = aditivo(f0, n_total / SR, amps)
    pluck = 1 + 0.8 * np.exp(-t * 18)
    x = x * pluck / 1.8 + 0.5 * np.sin(2 * np.pi * f0 * t)
    return x * adsr(n_nota, n_total, 0.004, 0.12, 0.65, 0.05) * vel * 0.8


def i_ocarina(f0, dur, vel):
    n_nota = int(dur * SR); n_total = n_nota + int(0.12 * SR)
    t = tempo(n_total / SR)
    x = aditivo(f0, n_total / SR, [1, 0.12, 0.05, 0.02], vib=0.006, vib_hz=5.2, vib_atraso=0.12)
    sopro = filtro_fft(RNG.normal(0, 1, n_total), lo=f0 * 1.5, hi=f0 * 4) * (0.05 + 0.25 * np.exp(-t * 18))
    return (x + sopro) * adsr(n_nota, n_total, 0.035, 0.08, 0.85, 0.1) * vel * 0.7


def i_flauta(f0, dur, vel):
    return i_ocarina(f0 * 2, dur, vel * 0.6)


def i_pad(f0, dur, vel):
    return nota_generica(f0, dur, vel * 0.35, serra(10, 0.35), 0.35, 0.5, 0.8, 0.8, vib=0.002, detunes=(-8, 0, 7))


def i_cordas(f0, dur, vel):
    return nota_generica(f0, dur, vel * 0.42, serra(14, 0.22), 0.18, 0.3, 0.85, 0.45, vib=0.005, detunes=(-6, 5))


def i_orgao(f0, dur, vel):
    n_nota = int(dur * SR); n_total = n_nota + int(0.12 * SR)
    t = tempo(n_total / SR)
    x = (aditivo(f0 / 2, n_total / SR, [1]) * 0.5 + aditivo(f0, n_total / SR, [1, 0.6, 0.35, 0.3, 0, 0.18, 0, 0.12]))
    trem = 1 + 0.12 * np.sin(2 * np.pi * 6.2 * t)
    return x * trem * adsr(n_nota, n_total, 0.02, 0.05, 0.92, 0.1) * vel * 0.32


def i_acordeao(f0, dur, vel):
    amps = [1, 0.8, 0.65, 0.5, 0.45, 0.32, 0.25, 0.18, 0.12, 0.08, 0.05]
    return nota_generica(f0, dur, vel * 0.32, amps, 0.04, 0.1, 0.85, 0.12, vib=0.0, detunes=(-11, 0, 12))


def i_coro(f0, dur, vel):
    n_nota = int(dur * SR); n_total = n_nota + int(0.6 * SR)
    amps = []
    for k in range(1, 30):
        fk = f0 * k
        a = (math.exp(-((fk - 750) / 220) ** 2) + 0.7 * math.exp(-((fk - 1150) / 260) ** 2)
             + 0.25 * math.exp(-((fk - 2800) / 400) ** 2) + 0.05) / k ** 0.3
        amps.append(a)
    x = np.zeros(n_total)
    for dt in (-9, 0, 8):
        x += aditivo(f0, n_total / SR, amps, vib=0.004, vib_hz=4.8, detune=dt)
    return x / 3 * adsr(n_nota, n_total, 0.3, 0.4, 0.85, 0.6) * vel * 0.28


def i_voz(f0, dur, vel):
    """Lead 'cantado' sem palavras (formantes de 'aa' + vibrato)."""
    n_nota = int(dur * SR); n_total = n_nota + int(0.25 * SR)
    amps = []
    for k in range(1, 24):
        fk = f0 * k
        a = (math.exp(-((fk - 800) / 180) ** 2) + 0.8 * math.exp(-((fk - 1200) / 220) ** 2)
             + 0.3 * math.exp(-((fk - 2900) / 380) ** 2) + 0.06) / k ** 0.15
        amps.append(a)
    x = aditivo(f0, n_total / SR, amps, vib=0.009, vib_hz=5.4, vib_atraso=0.2)
    return x * adsr(n_nota, n_total, 0.05, 0.2, 0.85, 0.22) * vel * 0.3


def i_piano(f0, dur, vel):
    n_total = int((dur + 0.8) * SR)
    t = tempo(n_total / SR)
    x = (np.sin(2 * np.pi * f0 * t) + 0.4 * np.sin(2 * np.pi * 2 * f0 * t) * np.exp(-t * 3)
         + 0.15 * np.sin(2 * np.pi * 3.01 * f0 * t) * np.exp(-t * 5) + 0.08 * np.sin(2 * np.pi * 7.1 * f0 * t) * np.exp(-t * 14))
    env = np.exp(-t * (1.6 + f0 / 900)) * np.minimum(t / 0.004, 1)
    n_nota = int(dur * SR)
    if n_nota < n_total:
        env[n_nota:] *= np.exp(-np.arange(n_total - n_nota) / SR * 9)
    return x * env * vel * 0.4


def i_marimba(f0, dur, vel):
    t = tempo(0.9)
    x = np.sin(2 * np.pi * f0 * t) * np.exp(-t * 6) + 0.35 * np.sin(2 * np.pi * f0 * 3.93 * t) * np.exp(-t * 22)
    return x * np.minimum(t / 0.002, 1) * vel * 0.45


def i_metal(f0, dur, vel):
    n_nota = int(dur * SR); n_total = n_nota + int(0.15 * SR)
    t = tempo(n_total / SR)
    brilho = np.clip(t / 0.06, 0, 1) * 0.6 + 0.4
    x = np.zeros(n_total)
    for k in range(1, 18):
        if k * f0 > SR * 0.45:
            break
        peso = (1 / k) * np.exp(-(k - 1) * (0.55 - 0.35 * brilho))
        x += peso * np.sin(2 * np.pi * k * f0 * t * (1 - 0.012 * np.exp(-t * 30)) + k)
    return x * adsr(n_nota, n_total, 0.025, 0.12, 0.8, 0.12) * vel * 0.32


def i_lead_sinte(f0, dur, vel):
    return nota_generica(f0, dur, vel * 0.3, serra(16, 0.12), 0.012, 0.15, 0.75, 0.12, vib=0.004, detunes=(-6, 6))


INSTR = {'kick': i_kick, 'snare': i_snare, 'clap': i_clap, 'hat': i_hat, 'hat_aberto': lambda d, v: i_hat(d, v, True),
         'shaker': i_shaker, 'crash': i_crash}


# ---------------------------------------------------------------- mixagem
class Musica:
    def __init__(self, bpm, compassos, intro=0):
        self.bpm = bpm
        self.batida = 60 / bpm
        self.intro = intro
        self.total_b = compassos * 4
        self.n = int((self.total_b * self.batida + 4) * SR)
        self.pistas = {}

    def pista(self, nome, ganho=1.0, pan=0.0, reverb=0.15):
        if nome not in self.pistas:
            self.pistas[nome] = {'x': np.zeros(self.n), 'ganho': ganho, 'pan': pan, 'rev': reverb}
        return self.pistas[nome]['x']

    def por(self, nome, beat, som):
        x = self.pista(nome)
        a = int(beat * self.batida * SR)
        b = min(len(x), a + len(som))
        if a < len(x):
            x[a:b] += som[:b - a]

    def nota(self, nome, instr, beat, dur_b, nota, vel=0.8):
        for m in (nota if isinstance(nota, (list, tuple)) else [nota]):
            self.por(nome, beat, instr(freq(midi(m)), dur_b * self.batida, vel))

    def bateria(self, nome, instr, beat0, padrao, vel=0.8, passo=0.25):
        for i, ch in enumerate(padrao):
            if ch in 'xX':
                v = vel * (1.0 if ch == 'X' else 0.7)
                self.por(nome, beat0 + i * passo, instr(0, v))

    def melodia(self, nome, instr, beat0, notas, vel=0.8):
        b = beat0
        for item in notas:
            n, d = item[0], item[1]
            v = item[2] if len(item) > 2 else vel
            if n is not None:
                self.nota(nome, instr, b, d * 0.95, n, v)
            b += d
        return b

    def mixar(self, loop_ini_b, nome):
        ir_n = int(2.2 * SR)
        t = np.arange(ir_n) / SR
        irs = []
        for s in (1, 2):
            r = np.random.default_rng(100 + s)
            graves = filtro_fft(r.normal(0, 1, ir_n), hi=2500) * np.exp(-t / 0.55)
            agudos = filtro_fft(r.normal(0, 1, ir_n), lo=2500) * np.exp(-t / 0.25)
            ir = (graves + 0.6 * agudos)
            ir[:int(0.012 * SR)] = 0
            irs.append(ir / np.sqrt(np.sum(ir ** 2)))
        L = np.zeros(self.n); R = np.zeros(self.n); env_rev = np.zeros(self.n)
        for p in self.pistas.values():
            x = p['x'] * p['ganho']
            ang = (p['pan'] + 1) * np.pi / 4
            L += x * np.cos(ang); R += x * np.sin(ang)
            env_rev += x * p['rev']
        tam = 1 << int(np.ceil(np.log2(self.n + ir_n)))
        E = np.fft.rfft(env_rev, tam)
        rl = np.fft.irfft(E * np.fft.rfft(irs[0], tam), tam)[:self.n]
        rr = np.fft.irfft(E * np.fft.rfft(irs[1], tam), tam)[:self.n]
        L += rl * 0.9; R += rr * 0.9
        a = int(loop_ini_b * self.batida * SR)
        fim = int(self.total_b * self.batida * SR)
        cauda = self.n - fim
        for ch in (L, R):
            ch[a:a + cauda] += ch[fim:fim + cauda]
        L, R = L[:fim], R[:fim]
        pico = max(np.max(np.abs(L)), np.max(np.abs(R)))
        L, R = L / pico * 1.15, R / pico * 1.15
        L = np.tanh(L * 1.1) / np.tanh(1.1) * 0.89
        R = np.tanh(R * 1.1) / np.tanh(1.1) * 0.89
        estereo = (np.stack([L, R], axis=1) * 32767).astype(np.int16)
        wav = OUT_WAV + nome + '.wav'
        with wave.open(wav, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(estereo.tobytes())
        ogg = BGM + nome + '.ogg'
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '5',
               '-metadata', f'LOOPSTART={a}', '-metadata', f'LOOPLENGTH={fim - a}', ogg]
        subprocess.run(cmd, check=True)
        rms = np.sqrt(np.mean((estereo.astype(float) / 32767) ** 2))
        print(f'{nome}: {fim / SR:.1f}s, loop em {a / SR:.1f}s, rms {rms:.3f}')


# ================================================================ FLORESTA DE MAUARA (112 bpm, F# dorico)
def floresta():
    m = Musica(112, 20, intro=4)
    m.pista('kick', 1.0, 0, 0.05); m.pista('snare', 0.55, 0.05, 0.2); m.pista('hat', 0.35, 0.3, 0.1)
    m.pista('shaker', 0.4, -0.35, 0.15); m.pista('conga', 0.5, -0.2, 0.2)
    m.pista('baixo', 0.85, 0, 0.04); m.pista('pad', 0.5, 0, 0.45); m.pista('ocarina', 0.75, 0.1, 0.4)
    m.pista('flauta', 0.5, -0.25, 0.5); m.pista('marimba', 0.45, 0.35, 0.3)
    # baixo (riff proprio, em semicolcheias): (passo, duracao em passos, nota)
    riff_a = [(0, 2, 'F#2'), (3, 1, 'F#2'), (6, 2, 'A2'), (8, 2, 'E2'), (11, 1, 'F#2'), (12, 1, 'A2'), (14, 2, 'B2')]
    riff_b = [(0, 2, 'F#2'), (3, 1, 'F#2'), (6, 2, 'C#3'), (8, 1, 'B2'), (10, 1, 'A2'), (12, 2, 'E2'), (14, 2, 'G#2')]
    riff_c = [(0, 3, 'D2'), (3, 1, 'D2'), (6, 2, 'F#2'), (8, 2, 'C#2'), (11, 1, 'C#2'), (12, 2, 'E2'), (14, 2, 'G#2')]
    riff_d = [(0, 3, 'B1'), (3, 1, 'B1'), (6, 2, 'D2'), (8, 2, 'C#2'), (10, 2, 'C#2'), (12, 2, 'E#2'), (14, 2, 'G#2')]

    def riff(b0, r):
        for (p, d, n) in r:
            m.nota('baixo', i_baixo, b0 + p * 0.25, d * 0.25 * 0.9, n, 0.85)

    for c in range(20):
        b0 = c * 4
        # bateria
        m.bateria('kick', INSTR['kick'], b0, 'X......x..X.....' if c % 2 == 0 else 'X......x..X...x.', 0.9)
        if c >= 2:
            m.bateria('snare', INSTR['clap'], b0, '....X.......X...', 0.75)
            m.bateria('hat', INSTR['hat'], b0, 'x.X.x.X.x.X.x.Xx', 0.6)
        m.bateria('shaker', INSTR['shaker'], b0, 'xxxxxxxxxxxxxxxx', 0.6)
        if c >= 4:
            for (p, f0) in ((2, 230), (5, 180), (9, 230), (10, 180), (13, 260), (15, 180)):
                m.por('conga', b0 + p * 0.25, i_conga(0, 0.55, f0))
        # baixo
        if c < 4:
            riff(b0, riff_a if c % 2 == 0 else riff_b)
        elif c < 12:
            riff(b0, riff_a if c % 2 == 0 else riff_b)
        else:
            riff(b0, [riff_c, riff_b, riff_d, riff_b][c % 4])
    # acordes (pad) e marimba
    acordes_a = [['F#3', 'A3', 'C#4', 'E4'], ['B3', 'D#4', 'F#4', 'A4'], ['F#3', 'A3', 'C#4', 'E4'], ['E3', 'G#3', 'B3', 'C#4']]
    acordes_b = [['D3', 'F#3', 'A3', 'C#4'], ['C#3', 'E3', 'G#3', 'B3'], ['B2', 'D3', 'F#3', 'A3'], ['C#3', 'E#3', 'G#3', 'B3']]
    for c in range(2, 20):
        ac = (acordes_a if c < 12 else acordes_b)[c % 4]
        m.nota('pad', i_pad, c * 4, 3.9, ac, 0.55)
        if c >= 4:
            for k, p in enumerate((0, 3, 6, 10, 12)):
                m.nota('marimba', i_marimba, c * 4 + p * 0.25, 0.2, ac[k % len(ac)].replace('3', '5').replace('4', '5').replace('2', '5'), 0.35)
    # ocarina (secao A, compassos 4-11)
    mel_a = [(None, 1), ('C#5', .5), ('E5', .5), ('F#5', 1), ('E5', .5), ('C#5', .5),
             ('B4', 1.5), ('A4', .5), ('B4', 1), (None, 1),
             (None, .5), ('A4', .5), ('B4', .5), ('C#5', .5), ('E5', 1), ('D#5', 1),
             ('C#5', 3), (None, 1),
             (None, 1), ('F#5', .5), ('G#5', .5), ('A5', 1), ('G#5', .5), ('F#5', .5),
             ('E5', 1), ('C#5', 1), ('D#5', .5), ('E5', .5), ('C#5', 1),
             ('B4', .5), ('C#5', .5), ('E5', 1), ('F#5', 1.5), ('E5', .5),
             ('F#5', 3), (None, 1)]
    m.melodia('ocarina', i_ocarina, 16, mel_a, 0.8)
    # secao B (compassos 12-19): flauta e ocarina conversam
    mel_b = [('F#5', 2), ('A5', 1), ('C#6', 1), ('B5', 2), ('G#5', 2), ('A5', 1.5), ('F#5', .5), ('D5', 2), ('E#5', 2), ('G#5', 2),
             ('F#5', 1), ('A5', 1), ('C#6', 1), ('E6', 1), ('D#6', 2), ('B5', 2), ('A5', 1), ('F#5', 1), ('D5', 1), ('F#5', 1), ('C#5', 4)]
    m.melodia('ocarina', i_ocarina, 48, mel_b, 0.75)
    contra = [(None, 2), ('A4', 2), (None, 2), ('E4', 2), (None, 2), ('F#4', 2), (None, 2), ('B4', 2),
              (None, 2), ('C#5', 2), (None, 2), ('A4', 2), (None, 2), ('F#4', 2), ('G#4', 4)]
    m.melodia('flauta', i_flauta, 48, contra, 0.5)
    m.mixar(16, 'Floresta_Mauara')


# ================================================================ TEMPLO DA XAVASCA LEPROSA (88 bpm, do menor)
def templo():
    m = Musica(88, 20, intro=4)
    m.pista('kick', 0.9, 0, 0.12); m.pista('snare', 0.6, 0, 0.45); m.pista('hat', 0.25, 0.25, 0.2); m.pista('crash', 0.45, -0.2, 0.3)
    m.pista('orgao', 0.7, -0.15, 0.4); m.pista('coro', 0.65, 0.1, 0.6); m.pista('acordeao', 0.7, 0.2, 0.35)
    m.pista('voz', 0.8, 0, 0.5); m.pista('piano', 0.55, -0.3, 0.35); m.pista('marimba', 0.4, 0.4, 0.3)
    m.pista('baixo', 0.75, 0, 0.08); m.pista('cordas', 0.55, 0, 0.5)
    v_ac = [['C3', 'Eb3', 'G3', 'C4'], ['Ab2', 'C3', 'Eb3', 'Ab3'], ['Eb3', 'G3', 'Bb3', 'Eb4'], ['Bb2', 'D3', 'F3', 'Bb3'],
            ['C3', 'Eb3', 'G3', 'C4'], ['Ab2', 'C3', 'Eb3', 'Ab3'], ['F2', 'Ab2', 'C3', 'F3'], ['G2', 'B2', 'D3', 'G3']]
    r_ac = [['Ab2', 'C3', 'Eb3', 'Ab3'], ['Eb3', 'G3', 'Bb3', 'Eb4'], ['Bb2', 'D3', 'F3', 'Bb3'], ['C3', 'Eb3', 'G3', 'C4'],
            ['Ab2', 'C3', 'Eb3', 'Ab3'], ['Eb3', 'G3', 'Bb3', 'Eb4'], ['Bb2', 'D3', 'F3', 'Bb3'], ['G2', 'B2', 'D3', 'G3']]
    for c in range(20):
        b0 = c * 4
        refrao = c >= 12
        ac = (r_ac if refrao else v_ac)[c % 8] if c >= 4 else v_ac[c % 8]
        m.nota('orgao', i_orgao, b0, 3.95, ac, 0.75 if not refrao else 0.6)
        m.nota('baixo', i_baixo, b0, 1.9, ac[0].replace('3', '2') if '3' in ac[0] else ac[0].replace('2', '1'), 0.8)
        m.nota('baixo', i_baixo, b0 + 2.5, 1.4, ac[0].replace('3', '2') if '3' in ac[0] else ac[0].replace('2', '1'), 0.65)
        if c < 4 or not refrao:
            for k in range(8):
                nota = ac[[0, 2, 1, 3, 2, 1, 3, 2][k]].replace('2', '4').replace('3', '4')
                m.nota('marimba', i_marimba, b0 + k * 0.5, 0.4, nota, 0.32 if c >= 4 else 0.4)
        if c >= 4:
            m.bateria('kick', INSTR['kick'], b0, 'X.........x.....' if not refrao else 'X.....x...X.....', 0.85)
            m.bateria('snare', INSTR['snare'], b0, '........X.......' if not refrao else '....X.......X...', 0.7)
            m.bateria('hat', INSTR['hat'], b0, 'x...x...x...x...' if not refrao else 'x.x.x.x.x.x.x.xX', 0.5)
        if refrao:
            m.nota('coro', i_coro, b0, 3.9, [n.replace('2', '4').replace('3', '4') for n in ac[1:]], 0.7)
            m.nota('cordas', i_cordas, b0, 3.9, [ac[0].replace('2', '3'), ac[2].replace('3', '4').replace('2', '4')], 0.55)
            for k in range(4):
                m.nota('piano', i_piano, b0 + k, 0.9, ac[(k + 1) % 4].replace('2', '5').replace('3', '5'), 0.4)
        if c in (12, 16):
            m.por('crash', b0, i_crash(0, 0.8))
    # verso: acordeao (compassos 4-11)
    verso = [('G4', 1), ('Eb4', .5), ('F4', .5), ('G4', 1.5), ('Ab4', .5),
             ('C5', 1), ('Bb4', .5), ('Ab4', .5), ('G4', 2),
             ('Bb4', 1), ('G4', .5), ('Ab4', .5), ('Bb4', 1.5), ('C5', .5),
             ('D5', 1), ('C5', .5), ('Bb4', .5), ('F4', 2),
             ('G4', .5), ('G4', .5), ('C5', 1), ('Eb5', 1), ('D5', 1),
             ('C5', 1.5), ('Bb4', .5), ('Ab4', 1), ('G4', 1),
             ('Ab4', 1), ('C5', 1), ('F5', 1), ('Eb5', .5), ('D5', .5),
             ('D5', 2), ('B4', 2)]
    m.melodia('acordeao', i_acordeao, 16, verso, 0.8)
    # refrao (compassos 12-19): voz sem palavras, grande e dramatica
    refr = [('C5', .5), ('Eb5', .5), ('Ab5', 2), ('G5', 1),
            ('G5', 1.5), ('F5', .5), ('Eb5', 1), ('Bb4', 1),
            ('D5', .5), ('F5', .5), ('Bb5', 2), ('Ab5', 1),
            ('G5', 3), ('Eb5', 1),
            ('C6', 2), ('Bb5', 1), ('Ab5', 1),
            ('G5', 2), ('Eb5', 1), ('F5', 1),
            ('D5', 1), ('F5', 1), ('Bb5', 1), ('Ab5', 1),
            ('G5', 2), ('B4', 1), ('D5', 1)]
    m.melodia('voz', i_voz, 48, refr, 0.85)
    m.melodia('acordeao', i_acordeao, 48, [(None, 3), ('Eb5', 1), (None, 3), ('Bb4', 1), (None, 3), ('F5', 1), (None, 3), ('C5', 1),
                                           (None, 3), ('Eb5', 1), (None, 3), ('G5', 1), (None, 3), ('F5', 1), (None, 2), ('D5', 1), ('B4', 1)], 0.45)
    m.mixar(16, 'Templo_Xavasca')


# ================================================================ CORRIDA UMAMUSUME (162 bpm, re maior)
def corrida():
    m = Musica(162, 20, intro=4)
    m.pista('kick', 1.0, 0, 0.06); m.pista('snare', 0.6, 0.05, 0.25); m.pista('hat', 0.35, 0.3, 0.12); m.pista('crash', 0.45, -0.2, 0.25)
    m.pista('timpani', 0.7, -0.1, 0.3); m.pista('baixo', 0.8, 0, 0.05); m.pista('cordas', 0.55, -0.25, 0.35)
    m.pista('metal', 0.75, 0.15, 0.3); m.pista('lead', 0.7, 0.05, 0.3); m.pista('piano', 0.4, -0.35, 0.25)
    ac_a = [['D3', 'F#3', 'A3'], ['C#3', 'E3', 'A3'], ['B2', 'D3', 'F#3'], ['G2', 'B2', 'D3'], ['D3', 'F#3', 'A3'], ['A2', 'C#3', 'E3'], ['G2', 'B2', 'D3'], ['A2', 'C#3', 'E3']]
    ac_b = [['B2', 'D3', 'F#3'], ['G2', 'B2', 'D3'], ['D3', 'F#3', 'A3'], ['A2', 'C#3', 'E3'], ['B2', 'D3', 'F#3'], ['G2', 'B2', 'D3'], ['E2', 'G2', 'B2'], ['A2', 'C#3', 'G3']]
    # introducao: fanfarra
    m.melodia('metal', i_metal, 0, [('D5', .5), ('D5', .5), ('D5', .5), ('A5', 2.5), ('G5', .5), ('G5', .5), ('F#5', .5), ('E5', 2.5),
                                    ('D5', .5), ('E5', .5), ('F#5', .5), ('A5', .5), ('B5', 1), ('C#6', 1), ('D6', 4)], 0.9)
    m.melodia('metal', i_metal, 0, [('A4', .5), ('A4', .5), ('A4', .5), ('F#5', 2.5), ('E5', .5), ('E5', .5), ('D5', .5), ('C#5', 2.5),
                                    ('A4', .5), ('C#5', .5), ('D5', .5), ('F#5', .5), ('G5', 1), ('A5', 1), ('A5', 4)], 0.7)
    for k in range(16):
        m.por('timpani', k * 0.25 + 12, i_timpani(0, 0.4 + k * 0.03, 73.4))
    m.por('timpani', 0, i_timpani(0, 0.9, 73.4)); m.por('timpani', 4, i_timpani(0, 0.9, 55))
    m.por('crash', 16, i_crash(0, 1.0))
    for c in range(4, 20):
        b0 = c * 4
        ac = (ac_a if c < 12 else ac_b)[(c - 4) % 8]
        raiz = ac[0]
        m.bateria('kick', INSTR['kick'], b0, 'X...x...X...x..x', 0.9)
        m.bateria('snare', INSTR['snare'], b0, '....X..x....X.xx', 0.7)
        m.bateria('hat', INSTR['hat'], b0, 'x.xxx.xxx.xxx.xx', 0.5)
        for k in range(8):
            nb = raiz.replace('3', '2') if '3' in raiz else raiz.replace('2', '1')
            alvo = nb if k % 2 == 0 else (nb[:-1] + str(int(nb[-1]) + 1))
            m.nota('baixo', i_baixo, b0 + k * 0.5, 0.42, alvo, 0.8)
        for k in range(16):
            n = ac[[0, 1, 2, 1][k % 4]].replace('2', '4').replace('3', '4')
            m.nota('cordas', i_cordas, b0 + k * 0.25, 0.22, n, 0.45)
        m.nota('metal', i_metal, b0, 0.4, [x.replace('2', '4').replace('3', '4') for x in ac], 0.55)
        m.nota('metal', i_metal, b0 + 1.5, 0.3, [x.replace('2', '4').replace('3', '4') for x in ac], 0.45)
        if c in (4, 12):
            m.por('crash', b0, i_crash(0, 0.9))
    lead_a = [('F#5', 1), ('A5', 1), ('D6', 1.5), ('C#6', .5),
              ('B5', 1), ('A5', 1), ('E5', 2),
              ('F#5', 1), ('B5', 1), ('D6', 1), ('C#6', .5), ('B5', .5),
              ('A5', 3), ('G5', .5), ('F#5', .5),
              ('F#5', .5), ('G5', .5), ('A5', 1), ('D6', 1), ('E6', 1),
              ('F#6', 2), ('E6', 1), ('C#6', 1),
              ('D6', 1), ('B5', 1), ('G5', 1), ('A5', 1),
              ('A5', 4)]
    lead_b = [('D6', 1.5), ('C#6', .5), ('B5', 2),
              ('B5', 1), ('A5', 1), ('G5', 2),
              ('A5', 1.5), ('F#5', .5), ('D5', 1), ('F#5', 1),
              ('E5', 3), (None, 1),
              ('F#5', 1), ('B5', 1), ('D6', 1), ('F#6', 1),
              ('E6', 2), ('D6', 1), ('B5', 1),
              ('G5', 1), ('B5', 1), ('E6', 1), ('G6', 1),
              ('F#6', 1), ('E6', 1), ('C#6', 1), ('A5', 1)]
    m.melodia('lead', i_lead_sinte, 16, lead_a, 0.8)
    m.melodia('lead', i_lead_sinte, 48, lead_b, 0.8)
    m.melodia('piano', i_piano, 48, [(n, d) for (n, d) in lead_b], 0.35)
    m.mixar(16, 'Corrida_Uma')


if __name__ == '__main__':
    qual = sys.argv[1:] or ['floresta', 'templo', 'corrida']
    if 'floresta' in qual:
        floresta()
    if 'templo' in qual:
        templo()
    if 'corrida' in qual:
        corrida()
