# Imagens dos itens e eventos importantes (para o plugin Destaques).
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_assets import PROJ

PREV = HERE + '/prev/'
S = 4          # desenha em 4x e reduz (bordas suaves)
W = 256


def canvas():
    im = Image.new('RGBA', (W * S, W * S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def p(*v):
    return tuple(int(x * S) for x in v)


def finish(im, name, outline=(40, 26, 30, 255), glow=None):
    small = im.resize((W, W), Image.LANCZOS)
    a = small.split()[3].point(lambda v: 255 if v > 40 else 0)
    edge = Image.new('RGBA', small.size, (0, 0, 0, 0))
    dil = a.filter(ImageFilter.MaxFilter(5))
    edge.paste(Image.new('RGBA', small.size, outline), (0, 0), dil)
    out = Image.new('RGBA', small.size, (0, 0, 0, 0))
    if glow:
        g = Image.new('RGBA', small.size, glow)
        g.putalpha(a.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.7)))
        out.alpha_composite(g)
    out.alpha_composite(edge)
    out.alpha_composite(small)
    out.save(PROJ + f'/img/pictures/{name}.png')
    return out


def grampo():
    im, d = canvas()
    rust = (150, 96, 70, 255); metal = (196, 176, 168, 255); hi = (240, 232, 226, 255); dark = (110, 70, 54, 255)
    # grampo em U, uma perna ondulada
    d.line([p(70, 40), p(70, 200)], fill=metal, width=S * 12)
    pts = []
    for i in range(0, 161, 4):
        y = 40 + i
        x = 104 + math.sin(i / 12) * 8
        pts.append(p(x, y))
    d.line(pts, fill=metal, width=S * 12, joint='curve')
    d.arc(p(70 - 6, 200 - 22, 104 + 6, 200 + 22), 0, 180, fill=metal, width=S * 12)
    d.line([p(66, 46), p(66, 192)], fill=hi, width=S * 3)
    rng = random.Random(3)
    for _ in range(18):
        x = rng.choice([70, 104]) + rng.randint(-5, 5)
        y = rng.randint(50, 210)
        r = rng.randint(3, 7)
        d.ellipse(p(x - r, y - r, x + r, y + r), fill=rust if rng.random() < 0.7 else dark)
    # florzinha de enfeite na ponta (como o laco da caveira)
    for k in range(5):
        a = k / 5 * 2 * math.pi - math.pi / 2
        x, y = 70 + math.cos(a) * 16, 34 + math.sin(a) * 16
        d.ellipse(p(x - 12, y - 12, x + 12, y + 12), fill=(244, 150, 180, 255))
    d.ellipse(p(60, 24, 80, 44), fill=(255, 214, 90, 255))
    d.ellipse(p(64, 28, 70, 34), fill=(255, 250, 220, 255))
    # brilho
    d.polygon([p(178, 60), p(184, 82), p(206, 88), p(184, 94), p(178, 116), p(172, 94), p(150, 88), p(172, 82)], fill=(255, 255, 240, 230))
    return finish(im, 'Item_Grampo', glow=(255, 230, 160, 255))


def pocao():
    im, d = canvas()
    d.rounded_rectangle(p(108, 30, 148, 74), S * 6, fill=(150, 104, 64, 255))
    d.rectangle(p(112, 70, 144, 92), fill=(200, 220, 230, 230))
    d.ellipse(p(56, 80, 200, 224), fill=(200, 220, 230, 235))
    d.chord(p(64, 88, 192, 216), 10, 170, fill=(220, 40, 70, 255))
    d.chord(p(64, 110, 192, 216), 20, 160, fill=(190, 20, 50, 255))
    for (x, y, r) in ((104, 150, 7), (140, 170, 5), (120, 186, 4), (152, 146, 4)):
        d.ellipse(p(x - r, y - r, x + r, y + r), fill=(255, 150, 170, 220))
    d.arc(p(70, 94, 186, 210), 200, 260, fill=(255, 255, 255, 220), width=S * 7)
    d.rounded_rectangle(p(96, 136, 160, 168), S * 4, fill=(250, 240, 210, 255))
    d.text(p(110, 140), '', fill=(0, 0, 0, 255))
    d.line([p(106, 152), p(150, 152)], fill=(170, 40, 60, 255), width=S * 4)
    d.line([p(128, 142), p(128, 162)], fill=(170, 40, 60, 255), width=S * 4)
    return finish(im, 'Item_Pocao', glow=(255, 140, 160, 255))


def cranio():
    im, d = canvas()
    bone = (238, 232, 216, 255); shade = (200, 192, 172, 255); hole = (40, 26, 34, 255)
    d.ellipse(p(52, 30, 204, 182), fill=bone)
    d.rounded_rectangle(p(86, 150, 170, 222), S * 18, fill=bone)
    d.arc(p(52, 30, 204, 182), 20, 160, fill=shade, width=S * 8)
    for cx in (100, 156):
        d.ellipse(p(cx - 24, 102, cx + 24, 146), fill=hole)
        d.ellipse(p(cx - 8, 112, cx + 2, 122), fill=(120, 170, 255, 255))
    d.polygon([p(128, 150), p(118, 172), p(138, 172)], fill=hole)
    for x in range(100, 160, 12):
        d.rounded_rectangle(p(x, 190, x + 9, 214), S * 2, fill=(250, 246, 236, 255), outline=shade, width=S * 2)
    d.line([p(150, 52), p(140, 76), p(152, 92)], fill=shade, width=S * 3)
    # lacinho rosa da Leandra
    d.polygon([p(150, 40), p(196, 18), p(190, 62)], fill=(244, 120, 160, 255))
    d.polygon([p(150, 40), p(170, 84), p(132, 74)], fill=(244, 120, 160, 255))
    d.ellipse(p(140, 30, 162, 52), fill=(250, 170, 200, 255))
    return finish(im, 'Item_Cranio', glow=(160, 200, 255, 255))


def moeda():
    im, d = canvas()
    d.ellipse(p(36, 36, 220, 220), fill=(190, 136, 30, 255))
    d.ellipse(p(44, 40, 214, 210), fill=(246, 196, 64, 255))
    d.ellipse(p(66, 62, 192, 188), outline=(200, 146, 30, 255), width=S * 6)
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 46 if k % 2 == 0 else 20
        pts.append(p(129 + math.cos(a) * r, 125 + math.sin(a) * r))
    d.polygon(pts, fill=(255, 236, 140, 255))
    d.arc(p(56, 52, 200, 196), 200, 280, fill=(255, 250, 210, 255), width=S * 8)
    return finish(im, 'Item_Esmola', outline=(110, 70, 10, 255), glow=(255, 220, 100, 255))


def flor():
    im, d = canvas()
    aura = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(aura).ellipse(p(30, 30, 226, 226), fill=(130, 40, 200, 150))
    im.alpha_composite(aura.filter(ImageFilter.GaussianBlur(S * 16)))
    d = ImageDraw.Draw(im)
    d.line([p(128, 130), p(124, 170), p(132, 236)], fill=(60, 130, 60, 255), width=S * 7, joint='curve')
    d.ellipse(p(132, 182, 170, 204), fill=(70, 150, 70, 255))
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        x, y = 128 + math.cos(a) * 42, 106 + math.sin(a) * 42
        d.ellipse(p(x - 30, y - 30, x + 30, y + 30), fill=(222, 30, 70, 255))
        d.ellipse(p(x - 16, y - 20, x + 6, y), fill=(250, 110, 140, 255))
    d.ellipse(p(108, 86, 148, 126), fill=(255, 214, 60, 255))
    # petala caindo
    d.ellipse(p(176, 186, 204, 206), fill=(222, 30, 70, 255))
    d.ellipse(p(196, 218, 216, 232), fill=(222, 30, 70, 200))
    return finish(im, 'Evento_Flor', outline=(70, 10, 40, 255))


def cadeado():
    im, d = canvas()
    gold = (240, 192, 64, 255); gold_d = (180, 128, 30, 255)
    d.arc(p(70, 20, 170, 140), 180, 360, fill=(170, 170, 180, 255), width=S * 16)
    d.line([p(78, 80), p(78, 106)], fill=(170, 170, 180, 255), width=S * 16)
    d.rounded_rectangle(p(60, 110, 196, 226), S * 16, fill=gold)
    d.rounded_rectangle(p(60, 110, 196, 130), S * 8, fill=(255, 226, 120, 255))
    d.ellipse(p(116, 148, 140, 172), fill=gold_d)
    d.polygon([p(122, 166), p(134, 166), p(138, 198), p(118, 198)], fill=gold_d)
    # check verde
    d.ellipse(p(148, 22, 236, 110), fill=(60, 190, 90, 255))
    d.line([p(168, 66), p(186, 86), p(216, 46)], fill=(255, 255, 255, 255), width=S * 10, joint='curve')
    return finish(im, 'Evento_Cadeado', glow=(140, 255, 160, 255))


if __name__ == '__main__':
    imgs = [grampo(), pocao(), cranio(), moeda(), flor(), cadeado()]
    pv = Image.new('RGBA', (W * len(imgs), W), (60, 50, 80, 255))
    for i, im in enumerate(imgs):
        pv.alpha_composite(im, (i * W, 0))
    pv.resize((pv.width // 2, pv.height // 2)).save(PREV + 'destaques.png')
    print('ok')


# ---------------------------------------------------------------- curiosidades dos cenarios
def tampinha():
    im, d = canvas()
    d.ellipse(p(48, 60, 208, 196), fill=(170, 20, 30, 255))
    d.ellipse(p(48, 48, 208, 184), fill=(220, 40, 50, 255))
    for k in range(21):
        a = k / 21 * 2 * math.pi
        x, y = 128 + math.cos(a) * 82, 116 + math.sin(a) * 70
        d.ellipse(p(x - 9, y - 9, x + 9, y + 9), fill=(200, 30, 40, 255))
    d.ellipse(p(70, 66, 186, 166), fill=(236, 70, 80, 255))
    d.text(p(96, 100), '', fill=(255, 255, 255, 255))
    d.arc(p(80, 74, 176, 158), 200, 290, fill=(255, 200, 200, 255), width=S * 6)
    d.rounded_rectangle(p(88, 104, 168, 128), S * 6, fill=(255, 240, 240, 255))
    return finish(im, 'Item_Tampinha', outline=(90, 10, 20, 255), glow=(255, 160, 160, 255))


def bilhete():
    im, d = canvas()
    d.polygon([p(30, 80), p(226, 60), p(232, 176), p(36, 196)], fill=(236, 222, 186, 255))
    d.polygon([p(30, 80), p(226, 60), p(228, 84), p(32, 104)], fill=(196, 70, 60, 255))
    for k in range(6):
        x = 70 + k * 22
        d.line([p(x, 120 - k * 2), p(x + 14, 118 - k * 2)], fill=(80, 70, 60, 255), width=S * 4)
    d.line([p(60, 150), p(200, 136)], fill=(80, 70, 60, 255), width=S * 4)
    for k in range(7):
        y = 92 + k * 14
        d.ellipse(p(176 - 4, y - 4, 176 + 4, y + 4), fill=(200, 186, 150, 255))
    d.ellipse(p(150, 140, 214, 192), outline=(60, 90, 160, 220), width=S * 5)
    return finish(im, 'Item_Bilhete', glow=(255, 230, 170, 255))


def chinelo():
    im, d = canvas()
    d.rounded_rectangle(p(70, 30, 186, 230), S * 50, fill=(60, 140, 220, 255))
    d.rounded_rectangle(p(80, 40, 176, 220), S * 44, fill=(250, 250, 250, 255))
    d.line([p(128, 70), p(92, 120)], fill=(60, 140, 220, 255), width=S * 14)
    d.line([p(128, 70), p(164, 120)], fill=(60, 140, 220, 255), width=S * 14)
    d.ellipse(p(118, 60, 138, 80), fill=(40, 110, 190, 255))
    d.text(p(110, 180), '', fill=(0, 0, 0, 255))
    d.ellipse(p(100, 170, 156, 200), fill=(230, 230, 230, 255))
    return finish(im, 'Item_Chinelo', glow=(160, 210, 255, 255))


def pedrinha():
    im, d = canvas()
    d.ellipse(p(44, 70, 212, 206), fill=(140, 136, 130, 255))
    d.ellipse(p(56, 76, 196, 180), fill=(170, 166, 158, 255))
    d.ellipse(p(70, 84, 120, 120), fill=(196, 192, 186, 255))
    for cx in (104, 152):
        d.ellipse(p(cx - 14, 112, cx + 14, 140), fill=(255, 255, 255, 255))
        d.ellipse(p(cx - 7, 120, cx + 7, 136), fill=(30, 30, 40, 255))
    d.arc(p(108, 140, 148, 168), 20, 160, fill=(40, 30, 30, 255), width=S * 4)
    d.ellipse(p(84, 146, 100, 156), fill=(240, 150, 160, 255)); d.ellipse(p(156, 146, 172, 156), fill=(240, 150, 160, 255))
    return finish(im, 'Item_Pedrinha', glow=(255, 220, 230, 255))


def pastel():
    im, d = canvas()
    d.chord(p(30, 70, 226, 250), 180, 360, fill=(232, 176, 80, 255))
    d.chord(p(40, 80, 216, 240), 180, 360, fill=(246, 204, 110, 255))
    for k in range(10):
        x = 40 + k * 19
        d.ellipse(p(x - 8, 152, x + 8, 168), fill=(214, 150, 60, 255))
    for (x, y, r) in ((96, 120, 6), (150, 110, 5), (124, 136, 4)):
        d.ellipse(p(x - r, y - r, x + r, y + r), fill=(255, 236, 170, 255))
    for k, (x, y) in enumerate(((150, 60), (176, 38), (128, 34))):
        d.arc(p(x - 18, y - 12, x + 18, y + 12), 200 + k * 20, 340, fill=(200, 230, 255, 230), width=S * 4)
    return finish(im, 'Item_Pastel', glow=(255, 220, 140, 255))


def coco():
    im, d = canvas()
    d.ellipse(p(44, 54, 212, 222), fill=(90, 150, 60, 255))
    d.ellipse(p(56, 60, 200, 200), fill=(120, 184, 80, 255))
    d.ellipse(p(96, 46, 160, 90), fill=(236, 236, 220, 255))
    d.ellipse(p(108, 54, 148, 82), fill=(214, 240, 230, 255))
    d.line([p(140, 66), p(180, 10)], fill=(250, 110, 150, 255), width=S * 8)
    d.line([p(176, 16), p(196, 4)], fill=(250, 110, 150, 255), width=S * 8)
    d.arc(p(70, 80, 180, 190), 200, 260, fill=(180, 230, 140, 255), width=S * 7)
    return finish(im, 'Item_Coco', glow=(200, 255, 170, 255))


def banana():
    im, d = canvas()
    for k, off in enumerate((0, 22, 44)):
        pts = []
        for i in range(21):
            t = i / 20
            a = math.pi * (0.15 + 0.7 * t)
            pts.append(p(128 + math.cos(a) * (100 - off * 0.5) - 10 + off * 0.6, 40 + off * 0.5 + math.sin(a) * (110 - off)))
        d.line(pts, fill=(246, 214, 60, 255), width=S * 26, joint='curve')
        d.line(pts[2:-2], fill=(255, 236, 120, 255), width=S * 8, joint='curve')
    d.rounded_rectangle(p(180, 24, 204, 64), S * 6, fill=(120, 90, 40, 255))
    return finish(im, 'Item_Banana', outline=(110, 80, 10, 255), glow=(255, 236, 140, 255))


def brilho_chao():
    frames = []
    for k, (s, a) in enumerate(((9, 200), (14, 255), (6, 150))):
        f = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); fd = ImageDraw.Draw(f)
        g = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse((24 - s, 34 - s, 24 + s, 34 + s), fill=(255, 250, 200, a // 2))
        f.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)))
        fd = ImageDraw.Draw(f)
        c = (24, 34)
        fd.polygon([(c[0], c[1] - s), (c[0] + s / 4, c[1] - s / 4), (c[0] + s, c[1]), (c[0] + s / 4, c[1] + s / 4),
                    (c[0], c[1] + s), (c[0] - s / 4, c[1] + s / 4), (c[0] - s, c[1]), (c[0] - s / 4, c[1] - s / 4)],
                   fill=(255, 255, 230, a))
        frames.append(f)
    sh = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for r in range(4):
        for c, f in enumerate(frames):
            sh.alpha_composite(f, (c * 48, r * 48))
    sh.save(PROJ + '/img/characters/!$Brilho.png')


def curiosidades():
    imgs = [tampinha(), bilhete(), chinelo(), pedrinha(), pastel(), coco(), banana()]
    brilho_chao()
    pv = Image.new('RGBA', (W * len(imgs), W), (60, 50, 80, 255))
    for i, im in enumerate(imgs):
        pv.alpha_composite(im, (i * W, 0))
    pv.resize((pv.width // 2, pv.height // 2)).save(PREV + 'curiosidades.png')
