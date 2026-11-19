# Som de macaco ("u-u-a-a-A!") feito por sintese de voz com formantes, para trocar o miado ('Cat') dos macacos.
import math, os, subprocess, tempfile, wave
import numpy as np

SR = 44100
PROJ = 'K:/Kevin/workspace/jogo-bruno'
RNG = np.random.default_rng(3)
VOGAL = {'u': [(320, 80), (850, 120), (2400, 200)], 'o': [(500, 90), (900, 120), (2500, 200)],
         'a': [(780, 110), (1180, 130), (2700, 220)], 'e': [(560, 90), (1800, 150), (2600, 220)]}


def chamado(dur, f_ini, f_fim, v_ini, v_fim, vol=1.0, curva=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = (t / dur) ** curva
    f0 = f_ini * (f_fim / f_ini) ** x
    f0 *= 1 + 0.03 * np.sin(2 * np.pi * 28 * t)          # tremor da garganta
    fase = 2 * np.pi * np.cumsum(f0) / SR
    forms = [(np.array([a[0] for a in VOGAL[v_ini]]), np.array([b[0] for b in VOGAL[v_fim]])),
             (np.array([a[1] for a in VOGAL[v_ini]]), np.array([b[1] for b in VOGAL[v_fim]]))]
    F = np.outer(1 - x, forms[0][0]) + np.outer(x, forms[0][1])      # (n, 3) frequencias
    Bw = np.outer(1 - x, forms[1][0]) + np.outer(x, forms[1][1])
    out = np.zeros(n)
    for k in range(1, 40):
        fk = k * f0
        if np.all(fk > SR * 0.45):
            break
        amp = np.zeros(n)
        for i, peso in enumerate((1.0, 0.75, 0.25)):
            amp += peso * np.exp(-((fk - F[:, i]) / Bw[:, i]) ** 2)
        amp *= (fk < SR * 0.45) / k ** 0.3
        out += amp * np.sin(k * fase + k * 0.7)
    sopro = RNG.normal(0, 1, n)
    sopro = np.convolve(sopro, np.ones(6) / 6, mode='same') * 0.04
    env = np.minimum(1, t / 0.012) * np.minimum(1, (dur - t) / 0.04)
    env *= 0.75 + 0.25 * np.sin(np.pi * x)
    return (out + sopro) * env * vol


def silencio(d):
    return np.zeros(int(d * SR))


partes = [
    chamado(0.13, 380, 520, 'u', 'o', 0.7), silencio(0.05),
    chamado(0.13, 420, 600, 'u', 'o', 0.75), silencio(0.06),
    chamado(0.12, 620, 820, 'o', 'a', 0.85), silencio(0.04),
    chamado(0.12, 660, 900, 'o', 'a', 0.9), silencio(0.05),
    chamado(0.24, 850, 1250, 'a', 'e', 1.0, curva=0.6),
]
sinal = np.concatenate(partes)
sinal = sinal / np.max(np.abs(sinal)) * 0.85
sinal = np.concatenate([sinal, np.zeros(int(0.08 * SR))])
pcm = (sinal * 32767).astype(np.int16)

tmp = tempfile.mkdtemp()
wav = os.path.join(tmp, 'macaco.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
destino = PROJ + '/audio/se/Macaco.ogg'
temp_ogg = os.path.join(tmp, 'Macaco.ogg')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '6', temp_ogg], check=True)
os.replace(temp_ogg, destino) if os.path.splitdrive(temp_ogg)[0].lower() == os.path.splitdrive(destino)[0].lower() else None
if not os.path.exists(destino):
    import shutil
    shutil.copyfile(temp_ogg, destino + '.tmp')
    os.replace(destino + '.tmp', destino)
print('ok', round(len(sinal) / SR, 2), 's ->', destino)
