# Capitulo 2: sprites e rostos de Leandra, Leona, Kura e Raulete.
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, sheet, PROJ

G.PREV = HERE + '/prev/'
os.makedirs(G.PREV, exist_ok=True)
preview = G.preview


def blank(w=48, h=48):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def darker(c, k=0.7):
    return tuple(int(v * k) for v in c[:3]) + (255,)


def lighter(c, k=0.35):
    return tuple(int(v + (255 - v) * k) for v in c[:3]) + (255,)


WHITE = C(255, 255, 255)
EYE_D = C(34, 28, 40)
MOUTH = C(196, 104, 104)

# ---------------------------------------------------------------- paletas
SKIN = C(248, 216, 188); SKIN_D = C(224, 182, 150); BLUSH = C(244, 156, 156)
GOLD = C(250, 214, 96); GOLD_L = C(255, 240, 168); GOLD_D = C(212, 164, 52); GOLD_DD = C(170, 124, 34)
EYE_BLUE = C(58, 116, 210)
RAG = C(200, 176, 134); RAG_L = C(224, 204, 164); RAG_D = C(158, 132, 94)
PATCH1 = C(92, 126, 186); PATCH2 = C(194, 82, 82)
OUT_L = C(64, 42, 34)

BLK = C(40, 34, 50); BLK_L = C(92, 82, 116); BLK_D = C(22, 18, 28)
WINE = C(146, 34, 64); WINE_L = C(186, 64, 94); WINE_D = C(100, 20, 44); TRIM = C(236, 196, 86)
PALE = C(252, 230, 216); PALE_D = C(228, 196, 182)
EYE_RED = C(170, 36, 70)
SHOE_B = C(44, 34, 44)
EAR = C(120, 74, 46); EAR_L = C(160, 108, 70); EAR_IN = C(236, 170, 170)
OUT_V = C(40, 22, 36)


def hem_poly(x0, x1, y, amp=2, step=2):
    pts = [(x0, y - 1)]
    for i, x in enumerate(range(x0, x1 + 1, step)):
        pts.append((x, y + (amp if i % 2 else 0)))
    pts.append((x1, y - 1))
    return pts


# ================================================================ LEANDRA
def lea_down(p, bald=False):
    im, d = blank()
    if not bald:
        d.polygon([(14, 15), (34, 15), (35, 36), (33, 40), (15, 40), (13, 36)], fill=GOLD_D)
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.rectangle((19, 38, 21, ly), fill=SKIN); d.rectangle((26, 38, 28, ry), fill=SKIN)
    d.line((19, ly, 21, ly), fill=SKIN_D); d.line((26, ry, 28, ry), fill=SKIN_D)
    d.polygon([(18, 27), (30, 27), (32, 39), (16, 39)], fill=RAG)
    d.polygon(hem_poly(16, 32, 40), fill=RAG)
    d.line((18, 27, 16, 39), fill=RAG_D); d.line((30, 27, 32, 39), fill=RAG_D)
    d.rectangle((19, 33, 21, 35), fill=PATCH1); d.point((20, 34), fill=RAG_L)
    d.rectangle((27, 30, 28, 31), fill=PATCH2)
    d.line((24, 29, 24, 38), fill=RAG_D)
    d.rectangle((15, 28, 17, 35), fill=SKIN); d.rectangle((31, 28, 33, 35), fill=SKIN)
    d.point((15, 35), fill=SKIN_D); d.point((33, 35), fill=SKIN_D)
    d.rectangle((15, 27, 17, 29), fill=RAG_L); d.rectangle((31, 27, 33, 29), fill=RAG_L)
    if bald:
        d.ellipse((15, 8, 33, 28), fill=SKIN)
        d.arc((18, 10, 28, 18), 200, 300, fill=WHITE)
    else:
        d.ellipse((14, 8, 34, 26), fill=GOLD)
        d.ellipse((16, 11, 32, 29), fill=SKIN)
    for ex in (19, 27):
        d.rectangle((ex, 19, ex + 2, 22), fill=EYE_BLUE)
        d.line((ex, 19, ex + 2, 19), fill=EYE_D)
        d.point((ex, 20), fill=WHITE)
    d.line((23, 25, 25, 25), fill=MOUTH)
    d.point((18, 24), fill=BLUSH); d.point((30, 24), fill=BLUSH)
    if not bald:
        d.polygon([(15, 10), (33, 10), (33, 17), (30, 15), (27, 18), (24, 15), (21, 18), (18, 15), (15, 17)], fill=GOLD)
        d.line((19, 11, 18, 15), fill=GOLD_L); d.line((25, 11, 24, 15), fill=GOLD_L)
        d.polygon([(13, 13), (17, 14), (18, 30), (16, 38), (13, 35)], fill=GOLD)
        d.polygon([(35, 13), (31, 14), (30, 30), (32, 38), (35, 35)], fill=GOLD)
        d.line((15, 16, 15, 34), fill=GOLD_L); d.line((33, 16, 33, 34), fill=GOLD_L)
        d.arc((16, 8, 30, 16), 200, 330, fill=GOLD_L)
    return outline(im, OUT_L)


def lea_left(p, bald=False):
    im, d = blank()
    if not bald:
        d.polygon([(23, 10), (34, 12), (36, 28), (35, 39), (29, 41), (25, 33), (23, 20)], fill=GOLD_D)
    fx = {-1: 16, 0: 20, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 19}[p]
    d.rectangle((bx, 38, bx + 2, 43), fill=SKIN_D)
    d.rectangle((fx, 38, fx + 2, 44), fill=SKIN); d.line((fx - 1, 44, fx + 2, 44), fill=SKIN_D)
    d.polygon([(19, 27), (29, 27), (31, 39), (17, 39)], fill=RAG)
    d.polygon(hem_poly(17, 31, 40), fill=RAG)
    d.line((29, 27, 31, 39), fill=RAG_D)
    d.rectangle((24, 33, 26, 35), fill=PATCH1)
    d.rectangle((21, 28, 23, 35), fill=SKIN); d.point((21, 35), fill=SKIN_D)
    d.rectangle((21, 27, 24, 29), fill=RAG_L)
    if bald:
        d.ellipse((14, 8, 32, 28), fill=SKIN)
        d.arc((17, 10, 27, 18), 200, 300, fill=WHITE)
    else:
        d.ellipse((15, 8, 34, 26), fill=GOLD)
        d.ellipse((14, 11, 29, 29), fill=SKIN)
    d.point((13, 21), fill=SKIN)
    d.rectangle((17, 19, 18, 22), fill=EYE_BLUE); d.line((17, 19, 18, 19), fill=EYE_D); d.point((17, 20), fill=WHITE)
    d.point((16, 24), fill=BLUSH)
    d.line((15, 25, 16, 25), fill=MOUTH)
    if not bald:
        d.polygon([(14, 10), (30, 9), (33, 14), (24, 14), (21, 17), (19, 14), (15, 16)], fill=GOLD)
        d.polygon([(24, 12), (34, 12), (35, 30), (31, 37), (27, 33), (25, 22)], fill=GOLD)
        d.line((30, 15, 31, 33), fill=GOLD_L)
        d.arc((17, 8, 31, 16), 200, 330, fill=GOLD_L)
    return outline(im, OUT_L)


def lea_up(p, bald=False):
    im, d = blank()
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.rectangle((19, 38, 21, ly), fill=SKIN); d.rectangle((26, 38, 28, ry), fill=SKIN)
    d.polygon([(18, 27), (30, 27), (32, 39), (16, 39)], fill=RAG)
    d.polygon(hem_poly(16, 32, 40), fill=RAG)
    d.rectangle((25, 34, 27, 36), fill=PATCH2)
    d.rectangle((15, 28, 17, 35), fill=SKIN); d.rectangle((31, 28, 33, 35), fill=SKIN)
    if bald:
        d.ellipse((15, 8, 33, 28), fill=SKIN); d.arc((19, 10, 29, 18), 200, 340, fill=WHITE)
    else:
        d.ellipse((14, 8, 34, 26), fill=GOLD)
        d.polygon([(14, 16), (34, 16), (35, 36), (32, 40), (16, 40), (13, 36)], fill=GOLD)
        for x in (18, 22, 26, 30):
            d.line((x, 14, x + (1 if x > 24 else -1), 38), fill=GOLD_D)
        d.line((20, 12, 19, 37), fill=GOLD_L); d.line((28, 12, 29, 37), fill=GOLD_L)
        d.arc((18, 9, 30, 16), 200, 340, fill=GOLD_L)
    return outline(im, OUT_L)


# ================================================================ LEONA
def leona_legs(d, p, side=False):
    if side:
        fx = {-1: 16, 0: 20, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 19}[p]
        d.rectangle((bx, 38, bx + 2, 42), fill=PALE_D); d.rectangle((bx - 1, 42, bx + 2, 44), fill=darker(SHOE_B, 0.8))
        d.rectangle((fx, 38, fx + 2, 42), fill=PALE); d.rectangle((fx - 1, 42, fx + 2, 44), fill=SHOE_B)
        return
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((19, 38, 21, ly), fill=PALE); d.rectangle((26, 38, 28, ry), fill=PALE)
    d.rectangle((18, ly, 21, ly + 2), fill=SHOE_B); d.rectangle((26, ry, 29, ry + 2), fill=SHOE_B)


def leona_dress_front(d):
    d.rectangle((19, 26, 29, 31), fill=WINE)
    d.polygon([(19, 30), (29, 30), (33, 39), (15, 39)], fill=WINE)
    d.line((15, 39, 33, 39), fill=TRIM); d.line((16, 38, 32, 38), fill=WINE_D)
    for x in range(17, 32, 3):
        d.line((x, 32, x - (1 if x < 24 else -1), 38), fill=WINE_L)
    d.line((19, 30, 29, 30), fill=TRIM)
    d.polygon([(20, 26), (28, 26), (24, 29)], fill=WHITE)
    d.point((24, 30), fill=TRIM)
    d.rectangle((15, 27, 17, 34), fill=WINE); d.rectangle((31, 27, 33, 34), fill=WINE)
    d.rectangle((15, 34, 17, 35), fill=PALE); d.rectangle((31, 34, 33, 35), fill=PALE)


def leona_face_front(d, smug=True):
    d.ellipse((16, 11, 32, 29), fill=PALE)
    for ex in (19, 27):
        d.rectangle((ex, 20, ex + 2, 22), fill=EYE_RED)
        d.line((ex - 1, 19, ex + 3, 19), fill=EYE_D)
        d.point((ex + 2, 20), fill=WHITE)
    d.line((19, 17, 21, 16), fill=BLK_D); d.line((27, 16, 29, 17), fill=BLK_D)
    d.line((23, 25, 25, 24), fill=MOUTH)


def leona_down(p, horse=False):
    im, d = blank()
    if not horse:
        d.polygon([(14, 14), (34, 14), (35, 38), (33, 41), (15, 41), (13, 38)], fill=BLK_D)
    else:
        # rabo de cavalo (cabelo) balancando atras da cabeca e cauda de cavalo
        sw = p
        d.polygon([(30, 9), (37, 12), (38 + sw, 24), (36 + sw, 32), (33, 26), (31, 16)], fill=BLK_D)
        d.polygon([(14, 33), (11 - sw, 37), (9 - sw, 44), (13, 43), (16, 38)], fill=C(54, 40, 40))
    leona_legs(d, p)
    leona_dress_front(d)
    d.ellipse((14, 8, 34, 26), fill=BLK)
    leona_face_front(d)
    # franja reta (corte hime)
    d.polygon([(15, 10), (33, 10), (33, 17), (15, 17)], fill=BLK)
    d.line((16, 17, 32, 17), fill=BLK_D)
    d.arc((17, 9, 31, 16), 200, 330, fill=BLK_L)
    if not horse:
        d.polygon([(13, 13), (17, 13), (17, 31), (13, 31)], fill=BLK)
        d.polygon([(35, 13), (31, 13), (31, 31), (35, 31)], fill=BLK)
        d.line((15, 15, 15, 30), fill=BLK_L)
        d.line((33, 15, 33, 30), fill=BLK_L)
        d.rectangle((29, 9, 31, 11), fill=TRIM)
    else:
        d.polygon([(14, 13), (17, 13), (17, 24), (14, 22)], fill=BLK)
        d.polygon([(34, 13), (31, 13), (31, 24), (34, 22)], fill=BLK)
        for ex, flip in ((15, 1), (29, -1)):
            d.polygon([(ex, 10), (ex + 2 * flip, 1), (ex + 5 * flip, 9)], fill=EAR)
            d.polygon([(ex + flip, 9), (ex + 2 * flip, 4), (ex + 4 * flip, 9)], fill=EAR_IN)
        d.rectangle((22, 8, 26, 10), fill=TRIM)
    return outline(im, OUT_V)


def leona_left(p, horse=False):
    im, d = blank()
    if not horse:
        d.polygon([(23, 10), (34, 12), (36, 30), (35, 40), (28, 41), (25, 32), (23, 20)], fill=BLK_D)
    else:
        sw = p
        d.polygon([(30, 8), (37, 9), (40 + sw, 20), (39 + sw, 30), (35, 24), (32, 14)], fill=BLK_D)
        d.polygon([(28, 32), (34, 33), (39 - sw, 40), (37 - sw, 45), (31, 39)], fill=C(54, 40, 40))
    leona_legs(d, p, side=True)
    d.rectangle((20, 26, 28, 31), fill=WINE)
    d.polygon([(20, 30), (28, 30), (31, 39), (17, 39)], fill=WINE)
    d.line((17, 39, 31, 39), fill=TRIM); d.line((20, 30, 28, 30), fill=TRIM)
    d.line((27, 31, 30, 38), fill=WINE_D)
    d.rectangle((21, 27, 23, 34), fill=WINE); d.rectangle((21, 34, 23, 35), fill=PALE)
    d.ellipse((15, 8, 34, 26), fill=BLK)
    d.ellipse((14, 11, 29, 29), fill=PALE)
    d.point((13, 21), fill=PALE)
    d.rectangle((17, 20, 18, 22), fill=EYE_RED); d.line((16, 19, 19, 19), fill=EYE_D)
    d.line((16, 17, 18, 16), fill=BLK_D)
    d.line((15, 25, 16, 24), fill=MOUTH)
    d.polygon([(14, 10), (30, 9), (31, 16), (14, 16)], fill=BLK)
    d.line((15, 16, 26, 16), fill=BLK_D)
    if not horse:
        d.polygon([(24, 12), (34, 12), (35, 31), (30, 34), (26, 30), (25, 20)], fill=BLK)
        d.line((30, 15, 31, 31), fill=BLK_L)
    else:
        d.polygon([(24, 12), (33, 12), (33, 20), (27, 23), (25, 18)], fill=BLK)
        d.polygon([(22, 9), (24, 0), (28, 8)], fill=EAR)
        d.polygon([(23, 8), (24, 3), (26, 8)], fill=EAR_IN)
    d.arc((17, 8, 31, 15), 200, 330, fill=BLK_L)
    return outline(im, OUT_V)


def leona_up(p, horse=False):
    im, d = blank()
    leona_legs(d, p)
    d.rectangle((19, 26, 29, 31), fill=WINE)
    d.polygon([(19, 30), (29, 30), (33, 39), (15, 39)], fill=WINE)
    d.line((15, 39, 33, 39), fill=TRIM)
    d.rectangle((15, 27, 17, 34), fill=WINE); d.rectangle((31, 27, 33, 34), fill=WINE)
    d.line((24, 27, 24, 31), fill=TRIM)
    if not horse:
        d.ellipse((14, 8, 34, 26), fill=BLK)
        d.polygon([(14, 16), (34, 16), (35, 38), (33, 41), (15, 41), (13, 38)], fill=BLK)
        for x in (18, 22, 26, 30):
            d.line((x, 14, x, 39), fill=BLK_D)
        d.line((20, 12, 20, 38), fill=BLK_L); d.line((28, 12, 28, 38), fill=BLK_L)
        d.rectangle((29, 9, 31, 11), fill=TRIM)
    else:
        sw = p
        d.polygon([(19, 36), (29, 36), (28 + sw, 45), (20 + sw, 45)], fill=C(54, 40, 40))
        d.ellipse((14, 8, 34, 26), fill=BLK)
        d.rectangle((22, 7, 26, 10), fill=TRIM)
        d.polygon([(21, 10), (27, 10), (28 + sw, 30), (24 + sw, 34), (20 + sw, 30)], fill=BLK)
        d.line((24, 11, 24 + sw, 32), fill=BLK_L)
        for ex, flip in ((15, 1), (33, -1)):
            d.polygon([(ex, 11), (ex + 2 * flip, 2), (ex + 5 * flip, 10)], fill=EAR)
    d.arc((18, 9, 30, 16), 200, 340, fill=BLK_L)
    return outline(im, OUT_V)


# ================================================================ KURA (sombra encapuzada)
CLK = C(30, 22, 42); CLK_L = C(62, 44, 86); CLK_D = C(16, 12, 24); VOID = C(6, 4, 10)
RED = C(255, 44, 64); RED_L = C(255, 170, 170); CLAW = C(120, 104, 140)


def kura_hem(d, y, x0, x1, p):
    pts = [(x0, y - 4)]
    for i, x in enumerate(range(x0, x1 + 1, 3)):
        pts.append((x, y + (2 if (i + p) % 2 else -1)))
    pts.append((x1, y - 4))
    d.polygon(pts, fill=CLK)


def kura_down(p):
    im, d = blank()
    d.polygon([(12, 16), (36, 16), (40, 42), (8, 42)], fill=CLK)
    kura_hem(d, 44, 8, 40, p)
    for x in (16, 24, 32):
        d.line((x, 22, x + (x - 24) // 4, 41), fill=CLK_D)
    d.line((14, 18, 10, 40), fill=CLK_L)
    # mangas e garras
    d.polygon([(10, 20), (16, 22), (15, 33), (9, 34)], fill=CLK_L)
    d.polygon([(38, 20), (32, 22), (33, 33), (39, 34)], fill=CLK_L)
    for cx in (11, 36):
        for k in range(3):
            d.line((cx + k, 34, cx + k - 1 + (k % 2), 37), fill=CLAW)
    # capuz
    d.ellipse((13, 1, 35, 24), fill=CLK)
    d.polygon([(24, 0), (28, 3), (22, 3)], fill=CLK)
    d.ellipse((17, 7, 31, 21), fill=VOID)
    d.arc((13, 1, 35, 24), 200, 340, fill=CLK_L)
    for ex in (20, 27):
        d.rectangle((ex, 13, ex + 1, 14), fill=RED); d.point((ex, 13), fill=RED_L)
    return outline(im, C(10, 6, 14))


def kura_left(p):
    im, d = blank()
    d.polygon([(14, 16), (34, 16), (39, 42), (10, 42)], fill=CLK)
    kura_hem(d, 44, 10, 39, p)
    d.line((30, 20, 34, 41), fill=CLK_D); d.line((22, 22, 20, 41), fill=CLK_D)
    d.polygon([(18, 21), (24, 21), (22, 33), (15, 33)], fill=CLK_L)
    for k in range(3):
        d.line((15 + k, 33, 14 + k, 36), fill=CLAW)
    d.ellipse((13, 1, 34, 24), fill=CLK)
    d.polygon([(30, 4), (37, 12), (32, 16)], fill=CLK)
    d.ellipse((13, 8, 24, 21), fill=VOID)
    d.rectangle((16, 13, 17, 14), fill=RED); d.point((16, 13), fill=RED_L)
    d.arc((13, 1, 34, 24), 200, 330, fill=CLK_L)
    return outline(im, C(10, 6, 14))


def kura_up(p):
    im, d = blank()
    d.polygon([(12, 16), (36, 16), (40, 42), (8, 42)], fill=CLK)
    kura_hem(d, 44, 8, 40, p)
    for x in (18, 24, 30):
        d.line((x, 20, x, 41), fill=CLK_D)
    d.polygon([(10, 20), (16, 22), (15, 33), (9, 34)], fill=CLK_L)
    d.polygon([(38, 20), (32, 22), (33, 33), (39, 34)], fill=CLK_L)
    d.ellipse((13, 1, 35, 25), fill=CLK)
    d.polygon([(19, 18), (29, 18), (24, 30)], fill=CLK)
    d.arc((14, 2, 34, 22), 200, 340, fill=CLK_L)
    return outline(im, C(10, 6, 14))


def add_shadow(sheet_img, alpha=70):
    out = sheet_img.copy()
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for r in range(4):
        for c in range(3):
            x, y = c * 48, r * 48
            sd.ellipse((x + 12, y + 41, x + 36, y + 47), fill=(0, 0, 0, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(1.5))
    sh.alpha_composite(out)
    return sh


# ================================================================ RAULETE (nobre careca)
RSK = C(240, 202, 170); RSK_D = C(214, 170, 138); RSK_L = C(255, 240, 226)
COAT = C(92, 42, 124); COAT_L = C(128, 70, 164); COAT_D = C(62, 26, 86)
CAPE = C(26, 22, 30); CAPE_IN = C(176, 30, 44)
GLOVE = C(244, 242, 236); BTN = C(240, 200, 80); MON = C(240, 200, 80)
PANT = C(36, 30, 44); BOOT = C(24, 20, 26); MUST = C(70, 46, 30)


def rau_down(p, wig=False):
    im, d = blank()
    d.polygon([(11, 19), (37, 19), (40, 42), (8, 42)], fill=CAPE)
    d.line((9, 40, 11, 21), fill=CAPE_IN); d.line((39, 40, 37, 21), fill=CAPE_IN)
    if wig:
        d.polygon([(13, 10), (35, 10), (37, 34), (33, 38), (15, 38), (11, 34)], fill=GOLD_D)
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((18, 36, 22, ly), fill=PANT); d.rectangle((26, 36, 30, ry), fill=PANT)
    d.rectangle((17, ly - 1, 22, ly + 2), fill=BOOT); d.rectangle((26, ry - 1, 31, ry + 2), fill=BOOT)
    d.polygon([(15, 20), (33, 20), (34, 38), (14, 38)], fill=COAT)
    d.line((24, 21, 24, 37), fill=COAT_D)
    for y in (24, 28, 32):
        d.point((22, y), fill=BTN); d.point((26, y), fill=BTN)
    d.line((15, 33, 33, 33), fill=COAT_D)
    d.rectangle((11, 21, 15, 32), fill=COAT_L); d.rectangle((33, 21, 37, 32), fill=COAT_L)
    d.rectangle((11, 32, 15, 35), fill=GLOVE); d.rectangle((33, 32, 37, 35), fill=GLOVE)
    d.polygon([(15, 17), (20, 21), (24, 19), (28, 21), (33, 17), (33, 21), (15, 21)], fill=GLOVE)
    d.ellipse((16, 4, 32, 22), fill=RSK)
    d.ellipse((14, 11, 17, 16), fill=RSK_D); d.ellipse((31, 11, 34, 16), fill=RSK_D)
    if not wig:
        d.arc((18, 5, 28, 13), 190, 290, fill=RSK_L, width=2)
    d.rectangle((20, 13, 21, 14), fill=EYE_D); d.rectangle((27, 13, 28, 14), fill=EYE_D)
    d.line((19, 11, 22, 11), fill=MUST); d.line((26, 11, 29, 11), fill=MUST)
    d.ellipse((25, 11, 30, 16), outline=MON)
    d.line((30, 15, 31, 21), fill=MON)
    d.line((21, 17, 27, 17), fill=MUST)
    d.point((20, 16), fill=MUST); d.point((28, 16), fill=MUST); d.point((19, 15), fill=MUST); d.point((29, 15), fill=MUST)
    d.line((22, 19, 26, 19), fill=MOUTH)
    if wig:
        d.ellipse((15, 2, 33, 14), fill=GOLD)
        d.polygon([(15, 7), (33, 7), (33, 12), (29, 10), (25, 12), (21, 10), (17, 12), (15, 12)], fill=GOLD)
        d.polygon([(13, 8), (17, 9), (17, 30), (14, 34), (12, 30)], fill=GOLD)
        d.polygon([(35, 8), (31, 9), (31, 30), (34, 34), (36, 30)], fill=GOLD)
        d.line((14, 12, 14, 30), fill=GOLD_L); d.line((34, 12, 34, 30), fill=GOLD_L)
        d.arc((18, 3, 30, 10), 200, 330, fill=GOLD_L)
    return outline(im, C(30, 18, 30))


def rau_left(p, wig=False):
    im, d = blank()
    d.polygon([(22, 19), (36, 20), (39, 42), (24, 42)], fill=CAPE)
    d.line((37, 22, 38, 40), fill=CAPE_IN)
    if wig:
        d.polygon([(22, 8), (33, 9), (35, 34), (29, 37), (25, 30), (23, 18)], fill=GOLD_D)
    fx = {-1: 14, 0: 19, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 18}[p]
    d.rectangle((bx, 36, bx + 4, 42), fill=darker(PANT)); d.rectangle((bx - 1, 41, bx + 4, 44), fill=BOOT)
    d.rectangle((fx, 36, fx + 4, 42), fill=PANT); d.rectangle((fx - 2, 41, fx + 4, 44), fill=BOOT)
    d.polygon([(17, 20), (31, 20), (32, 38), (16, 38)], fill=COAT)
    d.line((18, 22, 18, 37), fill=COAT_D)
    for y in (24, 28, 32):
        d.point((19, y), fill=BTN)
    d.rectangle((21, 21, 26, 32), fill=COAT_L); d.rectangle((21, 32, 25, 35), fill=GLOVE)
    d.polygon([(17, 17), (24, 21), (29, 17), (29, 21), (17, 21)], fill=GLOVE)
    d.ellipse((14, 4, 30, 22), fill=RSK)
    d.ellipse((24, 11, 27, 16), fill=RSK_D)
    if not wig:
        d.arc((16, 5, 26, 13), 190, 290, fill=RSK_L, width=2)
    d.point((13, 14), fill=RSK)
    d.rectangle((17, 13, 18, 14), fill=EYE_D)
    d.ellipse((15, 11, 20, 16), outline=MON); d.line((20, 15, 22, 21), fill=MON)
    d.line((14, 17, 19, 17), fill=MUST); d.point((13, 16), fill=MUST)
    d.line((15, 19, 17, 19), fill=MOUTH)
    if wig:
        d.ellipse((15, 2, 32, 14), fill=GOLD)
        d.polygon([(14, 8), (24, 7), (24, 11), (19, 10), (15, 12)], fill=GOLD)
        d.polygon([(23, 8), (33, 9), (34, 30), (30, 34), (26, 28), (25, 16)], fill=GOLD)
        d.line((29, 12, 30, 30), fill=GOLD_L)
    return outline(im, C(30, 18, 30))


def rau_up(p, wig=False):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((18, 36, 22, ly), fill=PANT); d.rectangle((26, 36, 30, ry), fill=PANT)
    d.rectangle((17, ly - 1, 22, ly + 2), fill=BOOT); d.rectangle((26, ry - 1, 31, ry + 2), fill=BOOT)
    d.rectangle((11, 21, 15, 34), fill=COAT_L); d.rectangle((33, 21, 37, 34), fill=COAT_L)
    d.polygon([(12, 19), (36, 19), (39, 42), (9, 42)], fill=CAPE)
    d.line((24, 22, 24, 40), fill=C(44, 38, 50))
    d.polygon([(15, 17), (33, 17), (33, 22), (15, 22)], fill=GLOVE)
    d.ellipse((16, 4, 32, 22), fill=RSK)
    d.ellipse((14, 11, 17, 16), fill=RSK_D); d.ellipse((31, 11, 34, 16), fill=RSK_D)
    if wig:
        d.ellipse((15, 2, 33, 18), fill=GOLD)
        d.polygon([(14, 10), (34, 10), (36, 34), (32, 38), (16, 38), (12, 34)], fill=GOLD)
        for x in (18, 22, 26, 30):
            d.line((x, 12, x, 36), fill=GOLD_D)
        d.line((20, 8, 20, 35), fill=GOLD_L)
    else:
        d.arc((19, 5, 29, 13), 200, 340, fill=RSK_L, width=2)
    return outline(im, C(30, 18, 30))


def make_char(name, fd, fl, fu, shadow=False, bg=(120, 170, 110, 255), **kw):
    down = [fd(p, **kw) for p in (-1, 0, 1)]
    left = [fl(p, **kw) for p in (-1, 0, 1)]
    right = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in left]
    up = [fu(p, **kw) for p in (-1, 0, 1)]
    sh = sheet([down, left, right, up])
    if shadow:
        sh = add_shadow(sh)
    sh.save(PROJ + f'/img/characters/{name}.png')
    preview(sh, name.strip('$!') + '.png', 3, bg=bg)
    return sh


# ================================================================ ROSTOS (72x72 ampliado 2x)
def fcanvas():
    im = Image.new('RGBA', (72, 72), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def face_eyes(d, style, iris, y=38, lx=27, rx=45):
    for i, cx in enumerate((lx, rx)):
        if style in ('happy', 'pain'):
            if style == 'happy':
                d.arc((cx - 5, y - 2, cx + 5, y + 6), 200, 340, fill=EYE_D, width=2)
            else:
                d.line((cx - 5, y + 1 + (2 if i == 0 else -2), cx + 5, y + 1 + (-2 if i == 0 else 2)), fill=EYE_D, width=2)
            continue
        if style == 'smug':
            top, h = y - 1, 7
        elif style == 'wide':
            top, h = y - 6, 12
        else:
            top, h = y - 4, 10
        d.ellipse((cx - 5, top, cx + 5, top + h), fill=WHITE)
        d.ellipse((cx - 4, top, cx + 4, top + h), fill=iris)
        d.ellipse((cx - 2, top + 2, cx + 2, top + h - 1), fill=darker(iris, 0.55))
        d.rectangle((cx - 3, top + 1, cx - 2, top + 3), fill=WHITE)
        d.point((cx + 2, top + h - 2), fill=lighter(iris, 0.5))
        d.line((cx - 6, top, cx + 6, top - (1 if i else 0)), fill=EYE_D, width=2)
        if style == 'smug':
            d.line((cx - 5, top + 1, cx + 5, top + 1), fill=EYE_D, width=1)


def brows(d, style, color, y=29, lx=27, rx=45):
    if style == 'sad':
        d.line((lx - 5, y + 1, lx + 4, y - 2), fill=color, width=2)
        d.line((rx - 4, y - 2, rx + 5, y + 1), fill=color, width=2)
    elif style == 'angry':
        d.line((lx - 5, y - 2, lx + 4, y + 2), fill=color, width=2)
        d.line((rx - 4, y + 2, rx + 5, y - 2), fill=color, width=2)
    elif style == 'smug':
        d.line((lx - 5, y, lx + 4, y + 1), fill=color, width=2)
        d.line((rx - 4, y - 1, rx + 5, y - 3), fill=color, width=2)
    else:
        d.line((lx - 5, y, lx + 4, y - 1), fill=color, width=2)
        d.line((rx - 4, y - 1, rx + 5, y), fill=color, width=2)


def mouth(d, style, y=52, cx=36):
    if style == 'smile':
        d.arc((cx - 5, y - 4, cx + 5, y + 2), 20, 160, fill=C(150, 60, 60), width=2)
    elif style == 'grin':
        d.chord((cx - 7, y - 4, cx + 7, y + 4), 0, 180, fill=C(120, 30, 40))
        d.rectangle((cx - 5, y, cx + 5, y + 1), fill=WHITE)
    elif style == 'open':
        d.ellipse((cx - 3, y - 2, cx + 3, y + 4), fill=C(120, 30, 40))
        d.ellipse((cx - 2, y + 1, cx + 2, y + 4), fill=C(220, 110, 120))
    elif style == 'frown':
        d.arc((cx - 4, y, cx + 4, y + 6), 200, 340, fill=C(150, 60, 60), width=2)
    elif style == 'smirk':
        d.line((cx - 4, y + 1, cx + 4, y - 1), fill=C(150, 60, 60), width=2)
        d.point((cx + 5, y - 2), fill=C(150, 60, 60))
    elif style == 'laugh':
        d.chord((cx - 8, y - 5, cx + 8, y + 7), 0, 180, fill=C(120, 30, 40))
        d.rectangle((cx - 6, y, cx + 6, y + 1), fill=WHITE)
        d.ellipse((cx - 3, y + 3, cx + 3, y + 6), fill=C(220, 110, 120))


def face_base(d, skin, skin_d, cloth, cloth_d, collar=None):
    d.polygon([(4, 72), (10, 62), (24, 58), (48, 58), (62, 62), (68, 72)], fill=cloth)
    d.line((10, 62, 4, 72), fill=cloth_d); d.line((62, 62, 68, 72), fill=cloth_d)
    d.rectangle((30, 52, 42, 62), fill=skin_d)
    if collar:
        d.polygon([(24, 58), (36, 66), (48, 58), (44, 57), (36, 62), (28, 57)], fill=collar)
    d.ellipse((17, 14, 55, 54), fill=skin)
    d.polygon([(18, 38), (54, 38), (50, 52), (36, 60), (22, 52)], fill=skin)
    d.line((36, 44, 36, 46), fill=skin_d); d.point((35, 47), fill=skin_d)
    d.ellipse((14, 34, 19, 44), fill=skin); d.ellipse((53, 34, 58, 44), fill=skin)


def scale_face(im, out_name, bg=(70, 80, 100, 255)):
    return outline(im, C(40, 26, 30)).resize((144, 144), Image.NEAREST)


def face_sheet(faces, name):
    fs = Image.new('RGBA', (576, 288), (0, 0, 0, 0))
    for i, f in enumerate(faces):
        fs.alpha_composite(f, ((i % 4) * 144, (i // 4) * 144))
    fs.save(PROJ + f'/img/faces/{name}.png')
    pv = Image.new('RGBA', fs.size, (70, 80, 100, 255)); pv.alpha_composite(fs)
    pv.save(G.PREV + f'face_{name}.png')


# ---- Leandra
def leandra_face(expr):
    im, d = fcanvas()
    bald = expr == 'bald'
    if not bald:
        d.polygon([(12, 22), (60, 22), (64, 66), (54, 72), (18, 72), (8, 66)], fill=GOLD_D)
    face_base(d, SKIN, SKIN_D, RAG, RAG_D)
    d.rectangle((15, 64, 20, 70), fill=PATCH1)
    if bald:
        d.ellipse((16, 8, 56, 52), fill=SKIN)
        d.polygon([(18, 38), (54, 38), (50, 52), (36, 60), (22, 52)], fill=SKIN)
        d.arc((22, 10, 44, 28), 190, 290, fill=WHITE, width=2)
        d.ellipse((14, 34, 19, 44), fill=SKIN); d.ellipse((53, 34, 58, 44), fill=SKIN)
        d.line((36, 44, 36, 46), fill=SKIN_D)
    else:
        d.ellipse((13, 4, 59, 40), fill=GOLD)
    style = {'normal': 'normal', 'sad': 'wide', 'happy': 'happy', 'bald': 'pain'}[expr]
    face_eyes(d, style, EYE_BLUE)
    brows(d, 'sad' if expr in ('sad', 'bald') else 'normal', GOLD_DD)
    mouth(d, {'normal': 'smile', 'sad': 'open', 'happy': 'grin', 'bald': 'open'}[expr])
    d.ellipse((20, 44, 26, 48), fill=BLUSH); d.ellipse((46, 44, 52, 48), fill=BLUSH)
    d.point((48, 41), fill=C(170, 130, 100)); d.point((50, 43), fill=C(170, 130, 100)); d.point((47, 44), fill=C(170, 130, 100))
    if expr in ('sad', 'bald'):
        d.line((51, 42, 52, 49), fill=C(150, 200, 255), width=2)
    if not bald:
        d.polygon([(14, 16), (58, 16), (58, 30), (52, 26), (46, 32), (40, 25), (34, 32), (28, 25), (22, 31), (16, 26), (14, 30)], fill=GOLD)
        for x in (22, 32, 42, 50):
            d.line((x, 10, x - 2, 24), fill=GOLD_L)
        d.polygon([(10, 22), (18, 24), (19, 52), (15, 66), (9, 60)], fill=GOLD)
        d.polygon([(62, 22), (54, 24), (53, 52), (57, 66), (63, 60)], fill=GOLD)
        d.line((13, 28, 13, 58), fill=GOLD_L); d.line((59, 28, 59, 58), fill=GOLD_L)
        d.arc((20, 5, 50, 22), 200, 330, fill=GOLD_L, width=2)
        d.line((30, 8, 26, 14), fill=GOLD_D); d.line((46, 8, 50, 15), fill=GOLD_D)
    return scale_face(im, 'leandra')


# ---- Leona
def leona_face(expr):
    im, d = fcanvas()
    horse = expr == 'horse'
    if not horse:
        d.polygon([(12, 20), (60, 20), (63, 72), (9, 72)], fill=BLK_D)
    else:
        d.polygon([(46, 14), (62, 20), (66, 46), (60, 70), (54, 50), (50, 26)], fill=BLK_D)
    face_base(d, PALE, PALE_D, WINE, WINE_D, collar=WHITE)
    d.line((36, 66, 36, 72), fill=TRIM)
    d.ellipse((13, 4, 59, 40), fill=BLK)
    style = {'smug': 'smug', 'worried': 'normal', 'evil': 'smug', 'horse': 'smug'}[expr]
    face_eyes(d, style, EYE_RED)
    brows(d, {'smug': 'smug', 'worried': 'angry', 'evil': 'angry', 'horse': 'smug'}[expr], BLK_D)
    mouth(d, {'smug': 'smirk', 'worried': 'frown', 'evil': 'grin', 'horse': 'smirk'}[expr])
    d.polygon([(14, 15), (58, 15), (58, 31), (14, 31)], fill=BLK)
    d.line((15, 31, 57, 31), fill=BLK_D)
    for x in (22, 30, 38, 46, 54):
        d.line((x, 18, x, 30), fill=BLK_D)
    d.arc((20, 5, 52, 22), 200, 330, fill=BLK_L, width=2)
    if not horse:
        d.polygon([(10, 22), (19, 22), (19, 62), (10, 62)], fill=BLK)
        d.polygon([(62, 22), (53, 22), (53, 62), (62, 62)], fill=BLK)
        d.line((14, 26, 14, 60), fill=BLK_L); d.line((58, 26, 58, 60), fill=BLK_L)
        d.rectangle((48, 8, 54, 12), fill=TRIM)
    else:
        d.polygon([(11, 22), (19, 22), (19, 46), (12, 42)], fill=BLK)
        d.polygon([(61, 22), (53, 22), (53, 46), (60, 42)], fill=BLK)
        for ex, flip in ((14, 1), (58, -1)):
            d.polygon([(ex, 14), (ex + 4 * flip, -2), (ex + 13 * flip, 10)], fill=EAR)
            d.polygon([(ex + 3 * flip, 11), (ex + 5 * flip, 3), (ex + 10 * flip, 10)], fill=EAR_IN)
        d.rectangle((32, 2, 40, 6), fill=TRIM)
        d.point((26, 37), fill=C(255, 220, 120)); d.point((44, 37), fill=C(255, 220, 120))
    if expr == 'worried':
        d.line((52, 26, 53, 30), fill=C(150, 200, 255), width=2)
    return scale_face(im, 'leona')


# ---- Kura
def kura_face():
    im, d = fcanvas()
    d.polygon([(2, 72), (8, 50), (18, 40), (54, 40), (64, 50), (70, 72)], fill=CLK)
    d.ellipse((8, 2, 64, 66), fill=CLK)
    d.polygon([(36, 0), (44, 6), (28, 6)], fill=CLK)
    d.arc((8, 2, 64, 66), 200, 340, fill=CLK_L, width=2)
    d.ellipse((17, 16, 55, 60), fill=VOID)
    glow = Image.new('RGBA', (72, 72), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for ex in (28, 44):
        gd.ellipse((ex - 6, 32, ex + 6, 42), fill=(255, 40, 60, 160))
    glow = glow.filter(ImageFilter.GaussianBlur(3))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    for ex in (28, 44):
        d.polygon([(ex - 5, 36), (ex + 5, 34), (ex + 3, 39), (ex - 4, 39)], fill=RED)
        d.line((ex - 3, 36, ex + 2, 35), fill=RED_L)
    for x in (14, 58):
        d.line((x, 50, x + (4 if x < 36 else -4), 70), fill=CLK_D, width=2)
    return scale_face(im, 'kura')


# ---- Raulete
def raulete_face(expr):
    im, d = fcanvas()
    wig = expr == 'wig'
    if wig:
        d.polygon([(10, 18), (62, 18), (66, 70), (6, 70)], fill=GOLD_D)
    d.polygon([(0, 72), (6, 60), (18, 56), (54, 56), (66, 60), (72, 72)], fill=CAPE)
    d.polygon([(10, 72), (16, 60), (26, 58), (46, 58), (56, 60), (62, 72)], fill=COAT)
    d.polygon([(22, 56), (36, 66), (50, 56), (52, 64), (36, 72), (20, 64)], fill=GLOVE)
    d.point((36, 70), fill=BTN)
    d.rectangle((30, 50, 42, 60), fill=RSK_D)
    d.ellipse((14, 4, 58, 56), fill=RSK)
    d.ellipse((10, 30, 18, 44), fill=RSK); d.ellipse((54, 30, 62, 44), fill=RSK)
    if not wig:
        d.arc((20, 6, 46, 30), 190, 280, fill=RSK_L, width=3)
        d.point((40, 10), fill=RSK_L); d.point((42, 11), fill=RSK_L)
    face_eyes(d, 'smug' if not wig else 'happy', C(70, 60, 50), y=36)
    brows(d, 'smug' if not wig else 'normal', MUST, y=28)
    d.ellipse((38, 28, 54, 44), outline=MON, width=2)
    d.line((53, 40, 58, 56), fill=MON)
    d.line((36, 42, 36, 45), fill=RSK_D)
    # bigode enrolado
    d.polygon([(26, 48), (36, 46), (46, 48), (44, 50), (36, 49), (28, 50)], fill=MUST)
    d.arc((20, 42, 28, 50), 90, 270, fill=MUST, width=2)
    d.arc((44, 42, 52, 50), 270, 90, fill=MUST, width=2)
    mouth(d, 'smirk' if not wig else 'laugh', y=54)
    if wig:
        d.ellipse((12, 0, 60, 30), fill=GOLD)
        d.polygon([(13, 12), (59, 12), (59, 24), (53, 20), (46, 26), (40, 20), (33, 26), (26, 20), (19, 25), (13, 21)], fill=GOLD)
        d.polygon([(8, 18), (17, 20), (17, 56), (12, 66), (6, 58)], fill=GOLD)
        d.polygon([(64, 18), (55, 20), (55, 56), (60, 66), (66, 58)], fill=GOLD)
        d.line((11, 24, 11, 58), fill=GOLD_L); d.line((61, 24, 61, 58), fill=GOLD_L)
        d.arc((20, 2, 50, 18), 200, 330, fill=GOLD_L, width=2)
    return scale_face(im, 'raulete')


# ---- Terminal (para a tela de senha)
def terminal_face():
    im, d = fcanvas()
    d.rounded_rectangle((6, 6, 66, 52), 5, fill=C(196, 196, 186))
    d.rounded_rectangle((11, 10, 61, 46), 3, fill=C(16, 40, 24))
    for y in range(12, 45, 2):
        d.line((12, y, 60, y), fill=C(22, 52, 32))
    d.text((15, 14), 'SENHA:', fill=C(90, 255, 130))
    d.text((15, 28), '_ _ _ _', fill=C(90, 255, 130))
    d.rectangle((26, 52, 46, 58), fill=C(150, 150, 140))
    d.rounded_rectangle((8, 58, 64, 70), 3, fill=C(176, 176, 166))
    for x in range(12, 62, 6):
        d.rectangle((x, 61, x + 3, 63), fill=C(120, 120, 112)); d.rectangle((x, 65, x + 3, 67), fill=C(120, 120, 112))
    d.ellipse((56, 46, 59, 49), fill=C(90, 255, 130))
    return outline(im, C(40, 40, 40)).resize((144, 144), Image.NEAREST)


if __name__ == '__main__':
    make_char('$Leandra', lea_down, lea_left, lea_up)
    make_char('$Leandra_Careca', lea_down, lea_left, lea_up, bald=True)
    make_char('$Leona', leona_down, leona_left, leona_up)
    make_char('$Leona_Cavalo', leona_down, leona_left, leona_up, horse=True)
    make_char('$Kura', kura_down, kura_left, kura_up, shadow=True, bg=(110, 110, 120, 255))
    make_char('$Raulete', rau_down, rau_left, rau_up)
    make_char('$Raulete_Peruca', rau_down, rau_left, rau_up, wig=True)
    face_sheet([leandra_face(e) for e in ('normal', 'sad', 'happy', 'bald')], 'Leandra')
    face_sheet([leona_face(e) for e in ('smug', 'worried', 'evil', 'horse')], 'Leona')
    face_sheet([kura_face()], 'Kura')
    face_sheet([raulete_face('smug'), raulete_face('wig')], 'Raulete')
    face_sheet([terminal_face()], 'Terminal')
    # previa combinada
    names = ['$Leandra', '$Leandra_Careca', '$Leona', '$Leona_Cavalo', '$Kura', '$Raulete', '$Raulete_Peruca']
    cmb = Image.new('RGBA', (144 * len(names) + 10 * len(names), 192), (120, 150, 110, 255))
    for i, n in enumerate(names):
        cmb.alpha_composite(Image.open(PROJ + f'/img/characters/{n}.png').convert('RGBA'), (i * 154, 0))
    cmb.resize((cmb.width * 2, cmb.height * 2), Image.NEAREST).save(G.PREV + 'ch2_chars.png')
    fc = Image.new('RGBA', (576 * 2 + 10, 288 * 2 + 10), (70, 80, 100, 255))
    for i, n in enumerate(['Leandra', 'Leona', 'Kura', 'Raulete']):
        fc.alpha_composite(Image.open(PROJ + f'/img/faces/{n}.png').convert('RGBA'), ((i % 2) * 586, (i // 2) * 298))
    fc.save(G.PREV + 'ch2_faces.png')
    print('ok')
