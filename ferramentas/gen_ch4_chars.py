# Capitulo 4: Baratelli Diva, Kevinho Umamusume, Leona adulta, Vera Verao, Pavao-Hipopotamo,
# Arara Barraqueira, Capivara Marombeira e Curupira (sprites e rostos).
import math, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, sheet, PROJ
import gen_ch2_chars as C2
import gen_ch3_assets as G3
from gen_ch2_chars import (blank, fcanvas, face_eyes, brows, mouth, face_base, scale_face, face_sheet,
                           make_char, darker, lighter, WHITE, EYE_D)

PREV4 = HERE + '/prev4/'
os.makedirs(PREV4, exist_ok=True)
G.PREV = PREV4

RB = [(232, 52, 60), (250, 140, 40), (250, 214, 50), (84, 190, 92), (62, 132, 222), (150, 92, 206)]


def rad(a):
    return math.radians(a)


# ================================================================ BARATELLI DIVA
SK, SK_D = G.SKIN, G.SKIN_D
LILAC = C(198, 162, 236); LILAC_D = C(150, 112, 200)
UMB = C(255, 214, 40); UMB_L = C(255, 242, 150); UMB_D = C(206, 152, 18)
PUFF = C(255, 170, 214); PUFF_D = C(230, 120, 180)
OUTB = G3.OUTB


def rainbow_skirt(d, cx, top, bottom, wtop, wbot, sway=0, bands=RB[2:]):
    n = len(bands)
    for i, col in enumerate(bands):
        t0, t1 = i / n, (i + 1) / n
        y0, y1 = top + (bottom - top) * t0, top + (bottom - top) * t1
        w0, w1 = wtop + (wbot - wtop) * t0, wtop + (wbot - wtop) * t1
        d.polygon([(cx - w0 + sway * t0, y0), (cx + w0 + sway * t0, y0),
                   (cx + w1 + sway * t1, y1), (cx - w1 + sway * t1, y1)], fill=C(*col))
    d.line((cx - wbot + sway, bottom, cx + wbot + sway, bottom), fill=C(110, 60, 150))
    for x in range(int(cx - wbot + 2 + sway), int(cx + wbot + sway), 3):
        d.point((x, bottom - 1), fill=C(255, 250, 230))


def heel(d, x, y, back_left=True):
    d.rectangle((x, y, x + 3, y + 2), fill=LILAC)
    d.point((x if back_left else x + 3, y + 2), fill=LILAC_D)
    d.point((x + 1, y), fill=lighter(LILAC, 0.5))


def umbrella(d, cx, cy, r, hand):
    d.line((cx, cy, hand[0], hand[1]), fill=C(140, 96, 52))
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=UMB)
    d.pieslice((cx - r + 2, cy - r + 2, cx + r - 3, cy + r - 2), 205, 255, fill=UMB_L)
    for a in (216, 252, 288, 324):
        d.line((cx, cy, cx + r * math.cos(rad(a)), cy + r * math.sin(rad(a))), fill=UMB_D)
    seg = 2 * r / 4
    for k in range(4):
        x0 = cx - r + k * seg
        d.arc((x0, cy - 2, x0 + seg, cy + 2), 0, 180, fill=UMB_D)
    d.point((cx, cy - r - 1), fill=UMB_D)


def diva_body_front(d, p):
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    heel(d, 18, ly); heel(d, 27, ry, back_left=False)
    rainbow_skirt(d, 24, 30, 43, 7, 11, sway=p)
    d.rectangle((18, 24, 30, 27), fill=C(*RB[0])); d.rectangle((18, 28, 30, 31), fill=C(*RB[1]))
    d.line((19, 24, 24, 29), fill=C(255, 246, 236)); d.line((29, 24, 24, 29), fill=C(255, 246, 236))
    d.point((24, 30), fill=C(255, 230, 120))
    d.rectangle((15, 27, 17, 32), fill=SK); d.rectangle((31, 27, 33, 32), fill=SK)
    d.ellipse((13, 22, 19, 28), fill=PUFF); d.ellipse((29, 22, 35, 28), fill=PUFF)
    d.arc((13, 22, 19, 28), 30, 150, fill=PUFF_D); d.arc((29, 22, 35, 28), 30, 150, fill=PUFF_D)


def diva_down(p):
    im, d = blank()
    umbrella(d, 37, 9, 10, (33, 31))
    diva_body_front(d, p)
    G3.bc_head_front(d)
    return outline(im, OUTB)


def diva_left(p):
    im, d = blank()
    umbrella(d, 35, 8, 10, (23, 31))
    fx = {-1: 15, 0: 19, 1: 22}[p]; bx = {-1: 26, 0: 24, 1: 19}[p]
    heel(d, bx, 43, back_left=False); heel(d, fx, 43, back_left=False)
    rainbow_skirt(d, 24, 30, 43, 5, 10, sway=-p)
    d.rectangle((20, 24, 28, 27), fill=C(*RB[0])); d.rectangle((20, 28, 28, 31), fill=C(*RB[1]))
    d.rectangle((22, 27, 24, 33), fill=SK); d.ellipse((20, 22, 27, 28), fill=PUFF)
    # rabo de cavalo e chiquinha de tras (igual a cigana)
    HR, HR_L, HR_D = G3.HR, G3.HR_L, G3.HR_D
    d.polygon([(28, 9), (35, 11), (37, 22), (35, 30), (31, 24), (29, 15)], fill=HR_D)
    G.curls(d, (30, 12, 36, 28), HR_L)
    d.ellipse((15, 5, 32, 18), fill=HR)
    d.ellipse((14, 10, 26, 25), fill=SK)
    d.point((13, 16), fill=SK); d.point((13, 17), fill=SK_D)
    d.polygon([(14, 19), (23, 19), (25, 23), (21, 27), (16, 26), (14, 23)], fill=G.BEARD)
    d.line((14, 21, 16, 21), fill=G.MOUTH)
    d.rectangle((15, 13, 18, 16), outline=G.GLASS, fill=G.LENS); d.line((19, 14, 23, 14), fill=G.GLASS)
    d.rectangle((15, 14, 15, 15), fill=G.EYE)
    d.polygon([(14, 9), (28, 8), (30, 12), (22, 12), (18, 13), (14, 12)], fill=HR)
    G3.pigtail(d, 27, 11, 1)
    G3.flower(d, 17, 7)
    return outline(im, OUTB)


def diva_up(p):
    im, d = blank()
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    heel(d, 18, ly); heel(d, 27, ry, back_left=False)
    rainbow_skirt(d, 24, 30, 43, 7, 11, sway=-p)
    d.rectangle((18, 24, 30, 27), fill=C(*RB[0])); d.rectangle((18, 28, 30, 31), fill=C(*RB[1]))
    d.rectangle((15, 27, 17, 32), fill=SK); d.rectangle((31, 27, 33, 32), fill=SK)
    d.ellipse((13, 22, 19, 28), fill=PUFF); d.ellipse((29, 22, 35, 28), fill=PUFF)
    HR, HR_L, HR_D = G3.HR, G3.HR_L, G3.HR_D
    d.ellipse((15, 5, 33, 24), fill=HR)
    G.curls(d, (16, 7, 32, 22), HR_L)
    G3.pigtail(d, 15, 11, -1); G3.pigtail(d, 33, 11, 1)
    d.polygon([(21, 16), (27, 16), (28 + p, 30), (24 + p, 35), (20 + p, 30)], fill=HR_D)
    G.curls(d, (21, 18, 28, 33), HR_L)
    d.rectangle((22, 14, 26, 17), fill=G3.RIB)
    G3.flower(d, 29, 7)
    umbrella(d, 13, 9, 10, (16, 30))
    return outline(im, OUTB)


# ================================================================ KEVINHO UMAMUSUME
KS = C(124, 80, 54); KS_D = C(96, 60, 40); KS_L = C(150, 104, 74)
AF = C(36, 26, 24); AF_L = C(74, 54, 46)
EARU = C(122, 80, 50); EARU_IN = C(236, 168, 168)
UNI = C(248, 248, 248); UNI_D = C(206, 212, 218)
GRN = C(58, 150, 96); GRN_D = C(36, 104, 64); GRN_L = C(110, 196, 140)
TAILK = C(44, 32, 30)
SNK = C(244, 244, 244); SNK_R = C(214, 52, 62)
OUTK = C(30, 22, 24)


def afro(d, box):
    x0, y0, x1, y1 = box
    d.ellipse(box, fill=AF)
    for (cx, cy) in [(x0 + 4, y0 + 6), (x0 + 9, y0 + 3), (x0 + 15, y0 + 2), (x1 - 9, y0 + 3), (x1 - 4, y0 + 6),
                     (x0 + 3, y0 + 11), (x1 - 3, y0 + 11), (x0 + 12, y0 + 7), (x1 - 11, y0 + 8)]:
        d.arc((cx - 2, cy - 2, cx + 2, cy + 2), 180, 360, fill=AF_L)


def horse_ears(d, lx, rx, y, color=EARU, inner=EARU_IN, h=7):
    for ex, flip in ((lx, 1), (rx, -1)):
        d.polygon([(ex, y), (ex + 1 * flip, y - h), (ex + 5 * flip, y - 1)], fill=color)
        d.polygon([(ex + 1 * flip, y - 1), (ex + 2 * flip, y - h + 3), (ex + 4 * flip, y - 1)], fill=inner)


def kevu_legs_front(d, p):
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((19, 34, 22, ly), fill=KS); d.rectangle((26, 34, 29, ry), fill=KS)
    d.rectangle((19, ly - 3, 22, ly), fill=WHITE); d.rectangle((26, ry - 3, 29, ry), fill=WHITE)
    d.rectangle((18, ly, 22, ly + 3), fill=SNK); d.line((18, ly + 3, 22, ly + 3), fill=SNK_R)
    d.rectangle((26, ry, 30, ry + 3), fill=SNK); d.line((26, ry + 3, 30, ry + 3), fill=SNK_R)


def kevu_down(p):
    im, d = blank()
    d.polygon([(14, 30), (10 - p, 35), (9 - p, 44), (13, 42), (16, 35)], fill=TAILK)
    kevu_legs_front(d, p)
    d.rectangle((18, 30, 30, 35), fill=GRN); d.line((24, 31, 24, 35), fill=GRN_D)
    d.polygon([(16, 20), (32, 20), (33, 31), (15, 31)], fill=UNI)
    d.line((16, 21, 15, 31), fill=GRN); d.line((32, 21, 33, 31), fill=GRN)
    d.rectangle((20, 24, 28, 29), fill=WHITE); d.rectangle((20, 24, 28, 29), outline=GRN_D)
    d.line((23, 25, 25, 25), fill=EYE_D); d.line((23, 25, 23, 27), fill=EYE_D); d.line((23, 27, 25, 27), fill=EYE_D)
    d.line((25, 27, 25, 28), fill=EYE_D); d.line((23, 28, 25, 28), fill=EYE_D)
    d.polygon([(20, 20), (28, 20), (24, 23)], fill=GRN)
    d.rectangle((12, 21, 15, 26), fill=UNI); d.rectangle((33, 21, 36, 26), fill=UNI)
    d.rectangle((12, 26, 15, 32), fill=KS); d.rectangle((33, 26, 36, 32), fill=KS)
    afro(d, (11, 0, 37, 19))
    d.ellipse((16, 7, 32, 23), fill=KS)
    d.ellipse((14, 12, 17, 17), fill=KS_D); d.ellipse((31, 12, 34, 17), fill=KS_D)
    d.polygon([(15, 9), (33, 9), (31, 12), (27, 10), (22, 12), (17, 10)], fill=AF)
    d.rectangle((20, 14, 21, 16), fill=EYE_D); d.rectangle((27, 14, 28, 16), fill=EYE_D)
    d.point((20, 14), fill=WHITE); d.point((27, 14), fill=WHITE)
    d.arc((21, 16, 27, 21), 20, 160, fill=C(90, 40, 40))
    horse_ears(d, 13, 35, 6)
    d.rectangle((30, 3, 33, 5), fill=GRN_L); d.point((31, 4), fill=WHITE)
    return outline(im, OUTK)


def kevu_left(p):
    im, d = blank()
    fx = {-1: 14, 0: 19, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 18}[p]
    d.polygon([(27, 30), (33, 31), (39 - p, 38), (37 - p, 44), (31, 38)], fill=TAILK)
    d.rectangle((bx, 34, bx + 3, 42), fill=KS_D); d.rectangle((bx, 39, bx + 3, 42), fill=UNI_D)
    d.rectangle((bx - 1, 42, bx + 4, 45), fill=C(214, 214, 214))
    d.rectangle((fx, 34, fx + 3, 42), fill=KS); d.rectangle((fx, 39, fx + 3, 42), fill=WHITE)
    d.rectangle((fx - 2, 42, fx + 4, 45), fill=SNK); d.line((fx - 2, 45, fx + 4, 45), fill=SNK_R)
    d.rectangle((19, 30, 29, 35), fill=GRN)
    d.polygon([(18, 20), (30, 20), (31, 31), (17, 31)], fill=UNI)
    d.line((30, 21, 31, 31), fill=GRN)
    d.rectangle((21, 21, 25, 27), fill=UNI_D); d.rectangle((21, 27, 25, 33), fill=KS)
    afro(d, (13, 1, 36, 20))
    d.ellipse((13, 7, 28, 23), fill=KS)
    d.point((12, 15), fill=KS)
    d.ellipse((23, 12, 26, 17), fill=KS_D)
    d.rectangle((16, 14, 17, 16), fill=EYE_D); d.point((16, 14), fill=WHITE)
    d.line((14, 19, 17, 19), fill=C(90, 40, 40))
    d.polygon([(13, 9), (27, 8), (26, 12), (19, 11), (14, 12)], fill=AF)
    d.polygon([(24, 6), (26, -1), (30, 5)], fill=EARU)
    d.polygon([(25, 5), (26, 1), (28, 5)], fill=EARU_IN)
    d.rectangle((31, 4, 34, 6), fill=GRN_L)
    return outline(im, OUTK)


def kevu_up(p):
    im, d = blank()
    kevu_legs_front(d, p)
    d.rectangle((18, 30, 30, 35), fill=GRN)
    d.polygon([(19, 30), (29, 30), (28 + p, 44), (20 + p, 44)], fill=TAILK)
    d.line((24, 31, 24 + p, 43), fill=C(80, 62, 58))
    d.polygon([(16, 20), (32, 20), (33, 31), (15, 31)], fill=UNI)
    d.line((16, 21, 15, 31), fill=GRN); d.line((32, 21, 33, 31), fill=GRN)
    d.rectangle((12, 21, 15, 26), fill=UNI); d.rectangle((33, 21, 36, 26), fill=UNI)
    d.rectangle((12, 26, 15, 32), fill=KS); d.rectangle((33, 26, 36, 32), fill=KS)
    d.rectangle((21, 23, 27, 27), fill=GRN_D)
    afro(d, (11, 0, 37, 23))
    horse_ears(d, 13, 35, 6)
    d.rectangle((15, 3, 18, 5), fill=GRN_L)
    return outline(im, OUTK)


# ================================================================ LEONA ADULTA
LP = C2.PALE; LP_D = C2.PALE_D
LH = C2.BLK; LH_L = C2.BLK_L; LH_D = C2.BLK_D
SUIT = C(72, 34, 100); SUIT_L = C(108, 60, 146); SUIT_D = C(44, 20, 64)
TRIMG = C2.TRIM; TIGHT = C(30, 24, 38); BOOT = C(18, 14, 22)
EYER = C2.EYE_RED
EARL = C(64, 46, 50); EARL_IN = C(200, 140, 150)
TAILL = C(30, 24, 30)
OUTL = C(22, 12, 26)


def leoa_legs_front(d, p):
    ly = 41 + (1 if p == -1 else 0); ry = 41 + (1 if p == 1 else 0)
    d.rectangle((20, 31, 22, ly), fill=TIGHT); d.rectangle((26, 31, 28, ry), fill=TIGHT)
    d.rectangle((19, ly - 3, 22, ly + 3), fill=BOOT); d.rectangle((26, ry - 3, 29, ry + 3), fill=BOOT)
    d.line((19, ly - 3, 22, ly - 3), fill=TRIMG); d.line((26, ry - 3, 29, ry - 3), fill=TRIMG)


def leoa_suit_front(d):
    d.polygon([(17, 18), (31, 18), (32, 31), (16, 31)], fill=SUIT)
    d.line((24, 19, 24, 31), fill=TRIMG)
    d.line((17, 29, 31, 29), fill=TRIMG)
    d.polygon([(19, 18), (29, 18), (27, 21), (21, 21)], fill=SUIT_L)
    d.rectangle((13, 18, 16, 21), fill=SUIT_L); d.rectangle((32, 18, 35, 21), fill=SUIT_L)
    d.line((13, 18, 16, 18), fill=TRIMG); d.line((32, 18, 35, 18), fill=TRIMG)
    d.rectangle((14, 21, 16, 29), fill=SUIT); d.rectangle((32, 21, 34, 29), fill=SUIT)
    d.rectangle((14, 29, 16, 31), fill=LP); d.rectangle((32, 29, 34, 31), fill=LP)
    d.polygon([(22, 23), (26, 23), (24, 26)], fill=C(200, 40, 70))


def leoa_down(p):
    im, d = blank()
    sw = p
    d.polygon([(28, 2), (35, 4), (38 + sw, 16), (37 + sw, 28), (33, 22), (30, 10)], fill=LH_D)
    d.polygon([(14, 28), (10 - sw, 33), (8 - sw, 43), (12, 41), (16, 34)], fill=TAILL)
    leoa_legs_front(d, p)
    leoa_suit_front(d)
    d.ellipse((17, 4, 31, 19), fill=LH)
    d.ellipse((18, 6, 30, 19), fill=LP)
    d.polygon([(17, 6), (31, 6), (31, 10), (26, 9), (21, 12), (17, 11)], fill=LH)
    d.line((19, 11, 23, 9), fill=LH_L)
    for ex in (20, 26):
        d.line((ex, 13, ex + 2, 13), fill=EYER); d.point((ex + 1, 14), fill=EYER)
    d.line((19, 11, 22, 12), fill=LH_D); d.line((26, 12, 29, 11), fill=LH_D)
    d.line((22, 17, 25, 16), fill=C(160, 60, 80))
    horse_ears(d, 17, 31, 6, EARL, EARL_IN, h=6)
    d.rectangle((22, 3, 26, 4), fill=TRIMG)
    return outline(im, OUTL)


def leoa_left(p):
    im, d = blank()
    sw = p
    d.polygon([(26, 2), (33, 2), (38 + sw, 12), (38 + sw, 26), (34, 20), (30, 9)], fill=LH_D)
    d.polygon([(27, 28), (33, 29), (39 - sw, 37), (37 - sw, 44), (31, 37)], fill=TAILL)
    fx = {-1: 16, 0: 20, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 19}[p]
    d.rectangle((bx, 31, bx + 2, 41), fill=darker(TIGHT, 0.8)); d.rectangle((bx - 1, 38, bx + 2, 44), fill=darker(BOOT, 0.8))
    d.rectangle((fx, 31, fx + 2, 41), fill=TIGHT); d.rectangle((fx - 2, 38, fx + 2, 44), fill=BOOT)
    d.line((fx - 2, 38, fx + 2, 38), fill=TRIMG)
    d.polygon([(19, 18), (29, 18), (30, 31), (18, 31)], fill=SUIT)
    d.line((19, 29, 29, 29), fill=TRIMG); d.line((20, 19, 19, 31), fill=TRIMG)
    d.rectangle((21, 19, 24, 28), fill=SUIT_L); d.rectangle((21, 28, 24, 30), fill=LP)
    d.ellipse((17, 4, 31, 19), fill=LH)
    d.ellipse((15, 6, 27, 19), fill=LP)
    d.point((14, 13), fill=LP)
    d.line((17, 13, 18, 13), fill=EYER); d.line((16, 11, 19, 12), fill=LH_D)
    d.line((15, 17, 17, 16), fill=C(160, 60, 80))
    d.polygon([(15, 5), (29, 4), (29, 10), (22, 9), (16, 11)], fill=LH)
    d.polygon([(23, 5), (25, -1), (28, 4)], fill=EARL)
    d.polygon([(24, 4), (25, 1), (27, 4)], fill=EARL_IN)
    return outline(im, OUTL)


def leoa_up(p):
    im, d = blank()
    sw = p
    leoa_legs_front(d, p)
    d.polygon([(19, 29), (29, 29), (28 + sw, 44), (20 + sw, 44)], fill=TAILL)
    d.polygon([(17, 18), (31, 18), (32, 31), (16, 31)], fill=SUIT)
    d.line((17, 29, 31, 29), fill=TRIMG)
    d.rectangle((13, 18, 16, 21), fill=SUIT_L); d.rectangle((32, 18, 35, 21), fill=SUIT_L)
    d.rectangle((14, 21, 16, 31), fill=SUIT); d.rectangle((32, 21, 34, 31), fill=SUIT)
    d.ellipse((17, 4, 31, 19), fill=LH)
    d.rectangle((22, 3, 26, 5), fill=TRIMG)
    d.polygon([(21, 5), (27, 5), (28 + sw, 26), (24 + sw, 30), (20 + sw, 26)], fill=LH_D)
    d.line((24, 6, 24 + sw, 28), fill=LH_L)
    horse_ears(d, 17, 31, 7, EARL, EARL_IN, h=6)
    return outline(im, OUTL)


# ================================================================ VERA VERAO (espirito glamouroso)
VS = C(112, 70, 52); VS_D = C(86, 52, 38)
VH = C(250, 214, 112); VH_L = C(255, 242, 186); VH_D = C(212, 162, 66)
GOWN = C(204, 28, 74); GOWN_L = C(255, 214, 110); GOWN_D = C(140, 14, 50)
BOA = C(255, 196, 228); BOA_L = C(255, 255, 255)
LIPS = C(206, 30, 80)
OUTV = C(70, 36, 30)


def boa(d, pts):
    for i, (x, y) in enumerate(pts):
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=BOA if i % 2 else BOA_L)


def sparkle(d, x, y, col=C(255, 255, 240)):
    d.point((x, y), fill=col)
    d.point((x - 1, y), fill=col); d.point((x + 1, y), fill=col)
    d.point((x, y - 1), fill=col); d.point((x, y + 1), fill=col)


def vera_gown(d, p, side=False):
    if side:
        d.polygon([(19, 24), (29, 24), (33 + p, 46), (13 + p, 46)], fill=GOWN)
    else:
        d.polygon([(18, 24), (30, 24), (32, 36), (37 + p, 46), (11 + p, 46), (16, 36)], fill=GOWN)
    for k, (x, y) in enumerate([(20, 30), (27, 33), (23, 39), (17, 43), (30, 42), (25, 45)]):
        d.point((x + p, y), fill=GOWN_L if (k + p) % 2 else GOWN_D)
    d.line((12 + p, 46, 36 + p, 46), fill=GOWN_D)


def vera_down(p):
    im, d = blank()
    d.ellipse((8, 0, 40, 26), fill=VH)
    for (x, y) in [(11, 8), (14, 3), (20, 1), (28, 1), (34, 3), (37, 8), (10, 15), (38, 15), (12, 21), (36, 21)]:
        d.arc((x - 3, y - 3, x + 3, y + 3), 160, 380, fill=VH_L)
    vera_gown(d, p)
    d.rectangle((14, 25, 16, 33), fill=VS); d.rectangle((32, 25, 34, 33), fill=VS)
    d.ellipse((17, 7, 31, 23), fill=VS)
    d.polygon([(16, 9), (32, 9), (31, 13), (26, 11), (21, 12), (17, 13)], fill=VH)
    d.line((19, 14, 22, 14), fill=EYE_D, width=1); d.line((26, 14, 29, 14), fill=EYE_D)
    d.point((20, 15), fill=EYE_D); d.point((27, 15), fill=EYE_D)
    d.line((19, 13, 21, 12), fill=C(170, 90, 210)); d.line((27, 12, 29, 13), fill=C(170, 90, 210))
    d.line((22, 19, 26, 19), fill=LIPS); d.point((24, 20), fill=LIPS)
    d.point((17, 18), fill=GOWN_L); d.point((31, 18), fill=GOWN_L)
    boa(d, [(14, 25), (17, 23), (21, 24), (24, 25), (27, 24), (31, 23), (34, 25), (15, 29), (34, 29), (14, 33), (35, 33)])
    for (x, y) in [(19, 3), (24, 1), (29, 3)]:
        d.polygon([(x - 2, y + 3), (x, y - 1), (x + 2, y + 3)], fill=C(255, 250, 220))
    sparkle(d, 9 + (p + 1) * 2, 34 - p * 3); sparkle(d, 39 - (p + 1) * 2, 28 + p * 2)
    return outline(im, OUTV)


def vera_left(p):
    im, d = blank()
    d.ellipse((12, 0, 40, 26), fill=VH)
    for (x, y) in [(16, 3), (24, 1), (32, 3), (37, 9), (38, 16), (36, 22)]:
        d.arc((x - 3, y - 3, x + 3, y + 3), 160, 380, fill=VH_L)
    vera_gown(d, p, side=True)
    d.rectangle((22, 25, 24, 34), fill=VS)
    d.ellipse((14, 8, 28, 23), fill=VS)
    d.point((13, 15), fill=VS)
    d.polygon([(14, 9), (28, 8), (27, 12), (19, 11), (15, 13)], fill=VH)
    d.line((15, 14, 17, 14), fill=EYE_D); d.point((16, 15), fill=EYE_D)
    d.line((15, 13, 17, 12), fill=C(170, 90, 210))
    d.line((14, 19, 16, 19), fill=LIPS)
    d.point((22, 18), fill=GOWN_L)
    boa(d, [(18, 25), (21, 23), (25, 24), (28, 26), (29, 30), (17, 29)])
    for (x, y) in [(20, 3), (26, 2)]:
        d.polygon([(x - 2, y + 3), (x, y - 1), (x + 2, y + 3)], fill=C(255, 250, 220))
    sparkle(d, 10, 30 - p * 3); sparkle(d, 38, 36 + p * 2)
    return outline(im, OUTV)


def vera_up(p):
    im, d = blank()
    vera_gown(d, p)
    d.rectangle((14, 25, 16, 33), fill=VS); d.rectangle((32, 25, 34, 33), fill=VS)
    boa(d, [(14, 25), (17, 23), (31, 23), (34, 25), (15, 29), (34, 29), (14, 33), (35, 33)])
    d.ellipse((8, 0, 40, 30), fill=VH)
    for (x, y) in [(11, 8), (14, 3), (20, 1), (28, 1), (34, 3), (37, 8), (10, 15), (38, 15), (13, 23), (35, 23), (20, 26), (28, 26)]:
        d.arc((x - 3, y - 3, x + 3, y + 3), 160, 380, fill=VH_L)
    for (x, y) in [(19, 3), (24, 1), (29, 3)]:
        d.polygon([(x - 2, y + 3), (x, y - 1), (x + 2, y + 3)], fill=C(255, 250, 220))
    sparkle(d, 9 + (p + 1) * 2, 36 - p * 3)
    return outline(im, OUTV)


# ================================================================ PAVAO-HIPOPOTAMO (personagem grande 96x96)
HIP = C(140, 118, 164); HIP_L = C(176, 156, 198); HIP_D = C(104, 84, 128)
SNOUT = C(198, 168, 196); SNOUT_D = C(160, 128, 162)
FAN = C(36, 122, 112); FAN_L = C(70, 170, 140); FAN_D = C(20, 80, 80)
EYE_GOLD = C(236, 196, 70); EYE_BLUE = C(40, 90, 200); EYE_NAVY = C(16, 26, 70)
CREST = C(40, 140, 200)
OUTP = C(40, 26, 50)


def big_blank():
    im = Image.new('RGBA', (96, 96), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def eyespot(d, x, y, s):
    d.ellipse((x - s, y - s * 1.3, x + s, y + s * 1.3), fill=EYE_GOLD)
    d.ellipse((x - s * 0.7, y - s * 0.9, x + s * 0.7, y + s * 0.9), fill=EYE_BLUE)
    d.ellipse((x - s * 0.35, y - s * 0.45, x + s * 0.35, y + s * 0.45), fill=EYE_NAVY)


def fan(d, cx, cy, r, a0, a1, rows=((0.82, 7), (0.58, 5))):
    d.pieslice((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=FAN)
    d.pieslice((cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7), a0, a1, fill=FAN_L)
    n = 13
    for k in range(n + 1):
        a = rad(a0 + (a1 - a0) * k / n)
        d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)), fill=FAN_D)
    for (rr, cnt) in rows:
        for k in range(cnt):
            a = rad(a0 + (a1 - a0) * (k + 0.5) / cnt)
            eyespot(d, cx + r * rr * math.cos(a), cy + r * rr * math.sin(a), 4 if rr > 0.7 else 3)


def crest(d, x, y, flip=1):
    for (dx, dy) in ((-7, -14), (0, -17), (7, -14)):
        d.line((x, y, x + dx * flip, y + dy), fill=C(60, 70, 110))
        d.ellipse((x + dx * flip - 2, y + dy - 3, x + dx * flip + 2, y + dy + 1), fill=CREST)


def pavao_down(p):
    im, d = big_blank()
    fan(d, 48, 60, 46, 190, 350)
    ly = 82 + (1 if p == -1 else 0); ry = 82 + (1 if p == 1 else 0)
    for x, yy in ((22, ry), (64, ly)):
        d.rectangle((x, 72, x + 10, yy + 8), fill=HIP_D)
    d.ellipse((16, 44, 80, 88), fill=HIP)
    d.ellipse((26, 58, 70, 86), fill=HIP_L)
    for x, yy in ((28, ly), (58, ry)):
        d.rectangle((x, 78, x + 10, yy + 10), fill=HIP)
        for t in range(3):
            d.point((x + 2 + t * 3, yy + 10), fill=C(240, 230, 240))
    d.ellipse((26, 22, 70, 62), fill=HIP)
    d.ellipse((22, 44, 74, 72), fill=SNOUT)
    d.ellipse((36, 50, 43, 56), fill=SNOUT_D); d.ellipse((53, 50, 60, 56), fill=SNOUT_D)
    d.arc((30, 56, 66, 70), 20, 160, fill=SNOUT_D, width=2)
    for ex in (36, 60):
        d.ellipse((ex - 4, 33, ex + 4, 41), fill=WHITE); d.ellipse((ex - 2, 35, ex + 2, 40), fill=EYE_D)
        for k in (-3, 0, 3):
            d.line((ex + k, 33, ex + k * 1.6, 29), fill=EYE_D)
    d.ellipse((24, 22, 32, 30), fill=HIP_D); d.ellipse((64, 22, 72, 30), fill=HIP_D)
    d.ellipse((26, 46, 33, 51), fill=C(240, 150, 190)); d.ellipse((63, 46, 70, 51), fill=C(240, 150, 190))
    crest(d, 48, 24)
    return outline(im, OUTP)


def pavao_left(p):
    im, d = big_blank()
    fan(d, 64, 52, 34, 230, 400, rows=((0.8, 6), (0.55, 4)))
    fx = {-1: 18, 0: 24, 1: 30}[p]; bx = {-1: 62, 0: 58, 1: 54}[p]
    d.rectangle((bx, 70, bx + 10, 90), fill=HIP_D); d.rectangle((fx + 6, 70, fx + 16, 90), fill=HIP_D)
    d.ellipse((22, 40, 86, 84), fill=HIP)
    d.ellipse((30, 58, 80, 84), fill=HIP_L)
    d.rectangle((fx, 72, fx + 10, 92), fill=HIP); d.rectangle((bx + 8, 72, bx + 18, 92), fill=HIP)
    d.ellipse((8, 30, 48, 68), fill=HIP)
    d.ellipse((2, 42, 34, 70), fill=SNOUT)
    d.ellipse((6, 46, 12, 52), fill=SNOUT_D)
    d.arc((4, 54, 30, 68), 30, 150, fill=SNOUT_D, width=2)
    d.ellipse((24, 36, 32, 44), fill=WHITE); d.ellipse((24, 37, 28, 42), fill=EYE_D)
    for k in (-2, 1, 4):
        d.line((26 + k, 36, 26 + k * 1.5, 32), fill=EYE_D)
    d.ellipse((34, 28, 42, 36), fill=HIP_D)
    d.ellipse((14, 50, 20, 55), fill=C(240, 150, 190))
    crest(d, 30, 32)
    return outline(im, OUTP)


def pavao_up(p):
    im, d = big_blank()
    ly = 82 + (1 if p == -1 else 0); ry = 82 + (1 if p == 1 else 0)
    for x, yy in ((22, ly), (64, ry)):
        d.rectangle((x, 74, x + 10, yy + 10), fill=HIP_D)
    d.ellipse((16, 44, 80, 90), fill=HIP)
    d.ellipse((28, 30, 68, 64), fill=HIP)
    d.ellipse((26, 26, 34, 34), fill=HIP_D); d.ellipse((62, 26, 70, 34), fill=HIP_D)
    crest(d, 48, 30)
    fan(d, 48, 66, 46, 180, 360, rows=((0.85, 8), (0.62, 6), (0.4, 4)))
    return outline(im, OUTP)


def make_big_char(name, fd, fl, fu):
    down = [fd(p) for p in (-1, 0, 1)]
    left = [fl(p) for p in (-1, 0, 1)]
    right = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in left]
    up = [fu(p) for p in (-1, 0, 1)]
    sh = Image.new('RGBA', (288, 384), (0, 0, 0, 0))
    for r, frames in enumerate([down, left, right, up]):
        for c, f in enumerate(frames):
            sh.alpha_composite(f, (c * 96, r * 96))
    sh.save(PROJ + f'/img/characters/{name}.png')
    G.preview(sh, name.strip('$!') + '.png', 2)
    return sh


# ================================================================ ARARA BARRAQUEIRA
ARR = C(222, 40, 46); ARR_L = C(250, 96, 90); ARR_D = C(160, 22, 30)
ABL = C(40, 96, 210); AYL = C(250, 210, 50)
BEAK = C(230, 226, 214); BEAK_D = C(60, 56, 60)
OUTA = C(60, 16, 20)


def arara_down(p):
    im, d = blank()
    wy = {-1: -6, 0: 0, 1: 5}[p]
    for flip in (1, -1):
        x0 = 24 + flip * 6
        d.polygon([(x0, 20), (x0 + flip * 16, 16 + wy), (x0 + flip * 18, 22 + wy), (x0 + flip * 10, 30)], fill=ABL)
        d.polygon([(x0, 20), (x0 + flip * 10, 18 + wy // 2), (x0 + flip * 9, 26)], fill=AYL)
    d.polygon([(21, 34), (27, 34), (29, 46), (24, 44), (19, 46)], fill=ARR_D)
    d.line((24, 36, 24, 45), fill=ABL)
    d.ellipse((16, 16, 32, 38), fill=ARR)
    d.ellipse((19, 24, 29, 36), fill=ARR_L)
    d.ellipse((17, 5, 31, 21), fill=ARR)
    d.ellipse((18, 10, 23, 16), fill=WHITE); d.ellipse((25, 10, 30, 16), fill=WHITE)
    d.rectangle((20, 12, 21, 14), fill=EYE_D); d.rectangle((27, 12, 28, 14), fill=EYE_D)
    d.polygon([(22, 15), (26, 15), (25, 21), (24, 22), (23, 21)], fill=BEAK)
    d.polygon([(23, 19), (25, 19), (24, 22)], fill=BEAK_D)
    d.rectangle((20, 38, 22, 40), fill=C(70, 60, 60)); d.rectangle((26, 38, 28, 40), fill=C(70, 60, 60))
    return outline(im, OUTA)


def arara_left(p):
    im, d = blank()
    wy = {-1: -7, 0: 0, 1: 5}[p]
    d.polygon([(26, 30), (32, 30), (44, 44), (38, 45)], fill=ARR_D)
    d.line((30, 32, 40, 43), fill=ABL)
    d.ellipse((17, 16, 34, 36), fill=ARR)
    d.polygon([(22, 20), (40, 12 + wy), (42, 20 + wy), (30, 32)], fill=ABL)
    d.polygon([(22, 20), (32, 16 + wy // 2), (30, 26)], fill=AYL)
    d.ellipse((12, 6, 28, 22), fill=ARR)
    d.ellipse((14, 9, 21, 16), fill=WHITE); d.rectangle((16, 12, 17, 14), fill=EYE_D)
    d.polygon([(13, 13), (6, 14), (5, 19), (9, 22), (13, 19)], fill=BEAK)
    d.polygon([(6, 18), (10, 18), (9, 22)], fill=BEAK_D)
    d.rectangle((22, 36, 24, 39), fill=C(70, 60, 60))
    return outline(im, OUTA)


def arara_up(p):
    im, d = blank()
    wy = {-1: -6, 0: 0, 1: 5}[p]
    d.polygon([(21, 34), (27, 34), (29, 46), (24, 44), (19, 46)], fill=ARR_D)
    d.ellipse((16, 16, 32, 38), fill=ARR)
    for flip in (1, -1):
        x0 = 24 + flip * 4
        d.polygon([(x0, 20), (x0 + flip * 17, 15 + wy), (x0 + flip * 18, 23 + wy), (x0 + flip * 6, 34)], fill=ABL)
    d.ellipse((17, 5, 31, 21), fill=ARR)
    return outline(im, OUTA)


# ================================================================ CAPIVARA MAROMBEIRA
CAP = C(150, 104, 62); CAP_L = C(184, 138, 90); CAP_D = C(110, 74, 42)
BAND = C(226, 40, 60); IRON = C(70, 74, 86); IRON_L = C(140, 146, 160)
OUTC = C(50, 30, 18)


def dumbbell(d, x, y, vertical=False):
    if vertical:
        d.line((x, y - 4, x, y + 4), fill=IRON_L, width=1)
        d.rectangle((x - 2, y - 6, x + 2, y - 4), fill=IRON); d.rectangle((x - 2, y + 4, x + 2, y + 6), fill=IRON)
    else:
        d.line((x - 4, y, x + 4, y), fill=IRON_L)
        d.rectangle((x - 6, y - 2, x - 4, y + 2), fill=IRON); d.rectangle((x + 4, y - 2, x + 6, y + 2), fill=IRON)


def capi_down(p):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((15, 36, 20, ly + 2), fill=CAP_D); d.rectangle((28, 36, 33, ry + 2), fill=CAP_D)
    d.ellipse((10, 18, 38, 42), fill=CAP)
    d.ellipse((16, 26, 32, 42), fill=CAP_L)
    d.rectangle((9, 26, 14, 33), fill=CAP); d.rectangle((34, 26, 39, 33), fill=CAP)
    dumbbell(d, 11, 34, vertical=True); dumbbell(d, 37, 34 - p, vertical=True)
    d.ellipse((14, 4, 34, 26), fill=CAP)
    d.ellipse((17, 14, 31, 27), fill=CAP_L)
    d.ellipse((14, 4, 19, 9), fill=CAP_D); d.ellipse((29, 4, 34, 9), fill=CAP_D)
    d.rectangle((14, 9, 34, 11), fill=BAND)
    d.rectangle((19, 13, 20, 15), fill=EYE_D); d.rectangle((28, 13, 29, 15), fill=EYE_D)
    d.ellipse((20, 19, 28, 25), fill=CAP_D)
    d.point((22, 21), fill=EYE_D); d.point((26, 21), fill=EYE_D)
    return outline(im, OUTC)


def capi_left(p):
    im, d = blank()
    fx = {-1: 12, 0: 15, 1: 18}[p]; bx = {-1: 32, 0: 29, 1: 26}[p]
    d.rectangle((bx, 34, bx + 4, 44), fill=CAP_D); d.rectangle((fx + 4, 34, fx + 8, 44), fill=CAP_D)
    d.ellipse((10, 18, 42, 40), fill=CAP)
    d.ellipse((16, 28, 38, 40), fill=CAP_L)
    d.rectangle((fx, 34, fx + 4, 45), fill=CAP); d.rectangle((bx + 4, 34, bx + 8, 45), fill=CAP)
    dumbbell(d, 22, 30 - p)
    d.ellipse((4, 10, 24, 30), fill=CAP)
    d.ellipse((2, 18, 14, 30), fill=CAP_L)
    d.ellipse((17, 8, 22, 13), fill=CAP_D)
    d.rectangle((7, 13, 23, 15), fill=BAND)
    d.rectangle((11, 17, 12, 19), fill=EYE_D)
    d.point((3, 22), fill=EYE_D)
    return outline(im, OUTC)


def capi_up(p):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((15, 36, 20, ly + 2), fill=CAP_D); d.rectangle((28, 36, 33, ry + 2), fill=CAP_D)
    d.ellipse((10, 18, 38, 44), fill=CAP)
    d.rectangle((9, 26, 14, 33), fill=CAP); d.rectangle((34, 26, 39, 33), fill=CAP)
    d.ellipse((14, 6, 34, 26), fill=CAP)
    d.ellipse((14, 4, 19, 9), fill=CAP_D); d.ellipse((29, 4, 34, 9), fill=CAP_D)
    d.rectangle((14, 11, 34, 13), fill=BAND)
    d.polygon([(30, 12), (36, 16), (33, 18)], fill=BAND)
    return outline(im, OUTC)


# ================================================================ CURUPIRA (pes virados para tras)
CU_SK = C(196, 140, 96); CU_SK_D = C(160, 106, 70)
FIRE = C(250, 90, 30); FIRE_L = C(255, 190, 60); FIRE_D = C(200, 40, 20)
LEAF = C(70, 150, 60); LEAF_D = C(40, 104, 40)
OUTCU = C(56, 26, 16)


def curu_hair(d, x0, x1, y, p=0):
    for k, x in enumerate(range(x0, x1 + 1, 4)):
        h = 9 + (k % 2) * 3 + (p if k % 2 else -p)
        d.polygon([(x - 3, y + 6), (x + 1, y - h + 6), (x + 4, y + 6)], fill=FIRE)
        d.polygon([(x - 1, y + 6), (x + 1, y - h + 10), (x + 2, y + 6)], fill=FIRE_L)


def curu_down(p):
    im, d = blank()
    ly = 41 + (1 if p == -1 else 0); ry = 41 + (1 if p == 1 else 0)
    d.rectangle((19, 34, 21, ly), fill=CU_SK); d.rectangle((27, 34, 29, ry), fill=CU_SK)
    # calcanhar na frente: o pe aponta para tras
    d.ellipse((18, ly, 23, ly + 3), fill=CU_SK_D); d.ellipse((26, ry, 31, ry + 3), fill=CU_SK_D)
    d.polygon([(17, 28), (31, 28), (33, 36), (15, 36)], fill=LEAF)
    for x in range(16, 33, 3):
        d.line((x, 30, x - 1, 36), fill=LEAF_D)
    d.rectangle((18, 20, 30, 29), fill=CU_SK)
    d.rectangle((14, 21, 17, 30), fill=CU_SK); d.rectangle((31, 21, 34, 30), fill=CU_SK)
    curu_hair(d, 15, 33, 6, p)
    d.ellipse((16, 8, 32, 24), fill=CU_SK)
    d.rectangle((20, 14, 21, 16), fill=EYE_D); d.rectangle((27, 14, 28, 16), fill=EYE_D)
    d.point((20, 14), fill=WHITE); d.point((27, 14), fill=WHITE)
    d.chord((20, 17, 28, 22), 0, 180, fill=C(120, 30, 40)); d.line((21, 19, 27, 19), fill=C(150, 230, 120))
    return outline(im, OUTCU)


def curu_left(p):
    im, d = blank()
    fx = {-1: 16, 0: 20, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 19}[p]
    for x, col in ((bx, CU_SK_D), (fx, CU_SK)):
        d.rectangle((x, 34, x + 2, 42), fill=col)
        d.polygon([(x - 1, 42), (x + 8, 42), (x + 8, 45), (x - 1, 45)], fill=col)   # dedos apontando para tras (direita)
        for t in range(3):
            d.point((x + 5 + t, 44), fill=OUTCU)
    d.polygon([(18, 28), (30, 28), (31, 36), (17, 36)], fill=LEAF)
    d.rectangle((19, 20, 29, 29), fill=CU_SK)
    d.rectangle((22, 21, 25, 30), fill=CU_SK_D)
    curu_hair(d, 17, 33, 6, p)
    d.ellipse((14, 8, 30, 24), fill=CU_SK)
    d.point((13, 15), fill=CU_SK)
    d.rectangle((17, 14, 18, 16), fill=EYE_D); d.point((17, 14), fill=WHITE)
    d.chord((14, 17, 20, 21), 0, 180, fill=C(120, 30, 40))
    return outline(im, OUTCU)


def curu_up(p):
    im, d = blank()
    ly = 41 + (1 if p == -1 else 0); ry = 41 + (1 if p == 1 else 0)
    d.rectangle((19, 34, 21, ly), fill=CU_SK); d.rectangle((27, 34, 29, ry), fill=CU_SK)
    d.polygon([(18, ly), (23, ly), (23, ly + 4), (18, ly + 4)], fill=CU_SK_D)
    d.polygon([(26, ry), (31, ry), (31, ry + 4), (26, ry + 4)], fill=CU_SK_D)
    d.polygon([(17, 28), (31, 28), (33, 36), (15, 36)], fill=LEAF)
    d.rectangle((18, 20, 30, 29), fill=CU_SK)
    d.rectangle((14, 21, 17, 30), fill=CU_SK); d.rectangle((31, 21, 34, 30), fill=CU_SK)
    d.ellipse((16, 8, 32, 24), fill=FIRE)
    curu_hair(d, 15, 33, 6, p)
    return outline(im, OUTCU)


# ================================================================ ROSTOS
def kevu_face(expr):
    im, d = fcanvas()
    face_base(d, KS, KS_D, UNI, UNI_D, collar=GRN)
    d.rectangle((26, 64, 46, 72), fill=WHITE); d.rectangle((26, 64, 46, 72), outline=GRN_D)
    d.ellipse((6, -6, 66, 40), fill=AF)
    for (x, y) in [(12, 10), (20, 2), (30, -1), (42, -1), (52, 2), (60, 10), (10, 22), (62, 22), (24, 10), (48, 10)]:
        d.arc((x - 4, y - 4, x + 4, y + 4), 180, 360, fill=AF_L, width=2)
    d.ellipse((17, 16, 55, 56), fill=KS)
    d.polygon([(18, 38), (54, 38), (50, 52), (36, 60), (22, 52)], fill=KS)
    d.ellipse((14, 34, 19, 44), fill=KS); d.ellipse((53, 34, 58, 44), fill=KS)
    d.polygon([(16, 20), (56, 20), (52, 28), (44, 24), (36, 28), (28, 24), (20, 28)], fill=AF)
    st = {'normal': 'normal', 'serio': 'normal', 'feliz': 'happy', 'susto': 'wide'}[expr]
    face_eyes(d, st, C(84, 52, 34))
    brows(d, {'normal': 'normal', 'serio': 'angry', 'feliz': 'normal', 'susto': 'sad'}[expr], AF)
    mouth(d, {'normal': 'smile', 'serio': 'frown', 'feliz': 'laugh', 'susto': 'open'}[expr])
    for ex, flip in ((10, 1), (62, -1)):
        d.polygon([(ex, 12), (ex + 3 * flip, -4), (ex + 12 * flip, 6)], fill=EARU)
        d.polygon([(ex + 3 * flip, 9), (ex + 4 * flip, 0), (ex + 9 * flip, 7)], fill=EARU_IN)
    d.rectangle((48, 4, 56, 9), fill=GRN_L)
    return scale_face(im, 'kevu')


def leoa_face(expr):
    im, d = fcanvas()
    d.polygon([(44, 6), (62, 10), (68, 40), (64, 66), (56, 46), (50, 20)], fill=LH_D)
    face_base(d, LP, LP_D, SUIT, SUIT_D, collar=TRIMG)
    d.line((36, 62, 36, 72), fill=TRIMG)
    d.ellipse((14, 4, 58, 40), fill=LH)
    st = {'deboche': 'smug', 'riso': 'smug', 'raiva': 'normal'}[expr]
    face_eyes(d, st, EYER)
    for cx in (27, 45):
        d.line((cx - 6, 33, cx + 6, 35 if cx < 36 else 33), fill=EYE_D, width=2)
    brows(d, 'angry', LH_D)
    mouth(d, {'deboche': 'smirk', 'riso': 'laugh', 'raiva': 'frown'}[expr])
    d.polygon([(14, 14), (58, 14), (58, 22), (46, 20), (34, 30), (24, 24), (14, 28)], fill=LH)
    d.arc((20, 5, 52, 22), 200, 330, fill=LH_L, width=2)
    for ex, flip in ((14, 1), (58, -1)):
        d.polygon([(ex, 12), (ex + 4 * flip, -4), (ex + 13 * flip, 8)], fill=EARL)
        d.polygon([(ex + 3 * flip, 9), (ex + 5 * flip, 1), (ex + 10 * flip, 8)], fill=EARL_IN)
    d.rectangle((32, 1, 40, 5), fill=TRIMG)
    return scale_face(im, 'leoa')


def vera_face(expr):
    im, d = fcanvas()
    d.ellipse((0, -4, 72, 58), fill=VH)
    for (x, y) in [(6, 16), (12, 4), (22, -1), (36, -3), (50, -1), (60, 4), (66, 16), (4, 30), (68, 30), (8, 44), (64, 44)]:
        d.arc((x - 6, y - 6, x + 6, y + 6), 160, 380, fill=VH_L, width=2)
    face_base(d, VS, VS_D, GOWN, GOWN_D)
    for k, x in enumerate(range(6, 70, 6)):
        y = 62 + (k % 2) * 3
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=BOA if k % 2 else BOA_L)
    d.polygon([(16, 22), (56, 22), (52, 28), (36, 24), (20, 28)], fill=VH)
    for (x, y) in [(28, 6), (36, 2), (44, 6)]:
        d.polygon([(x - 4, y + 7), (x, y - 1), (x + 4, y + 7)], fill=C(255, 250, 220))
        d.point((x, y + 3), fill=C(255, 90, 160))
    for cx in (27, 45):
        d.ellipse((cx - 7, 31, cx + 7, 39), fill=C(176, 104, 220))
    st = {'normal': 'smug', 'riso': 'happy', 'serio': 'normal'}[expr]
    face_eyes(d, st, C(110, 60, 30))
    for cx in (27, 45):
        for k in (-5, -2, 1, 4):
            d.line((cx + k, 34 if st != 'happy' else 36, cx + k * 1.4, 29), fill=EYE_D)
    brows(d, 'smug' if expr != 'serio' else 'normal', C(60, 34, 24))
    if expr == 'riso':
        d.chord((27, 46, 45, 58), 0, 180, fill=C(120, 20, 50)); d.rectangle((29, 50, 43, 51), fill=WHITE)
        d.arc((27, 44, 45, 58), 0, 180, fill=LIPS, width=2)
    else:
        d.ellipse((30, 49, 42, 55), fill=LIPS); d.line((31, 52, 41, 52), fill=C(130, 10, 50))
    for x in (14, 58):
        d.ellipse((x - 3, 44, x + 3, 50), fill=GOWN_L)
    return scale_face(im, 'vera')


def pavao_face():
    im, d = fcanvas()
    d.pieslice((-14, 6, 86, 106), 190, 350, fill=FAN)
    for k in range(7):
        a = rad(195 + k * 25)
        eyespot(d, 36 + 42 * math.cos(a), 56 + 42 * math.sin(a), 5)
    d.ellipse((8, 22, 64, 72), fill=HIP)
    d.ellipse((4, 44, 68, 76), fill=SNOUT)
    d.ellipse((20, 52, 28, 60), fill=SNOUT_D); d.ellipse((44, 52, 52, 60), fill=SNOUT_D)
    for ex in (22, 50):
        d.ellipse((ex - 6, 30, ex + 6, 42), fill=WHITE); d.ellipse((ex - 3, 33, ex + 3, 41), fill=EYE_D)
        for k in (-4, 0, 4):
            d.line((ex + k, 30, ex + k * 1.5, 24), fill=EYE_D, width=2)
    d.ellipse((6, 22, 16, 32), fill=HIP_D); d.ellipse((56, 22, 66, 32), fill=HIP_D)
    d.ellipse((10, 44, 18, 50), fill=C(240, 150, 190)); d.ellipse((54, 44, 62, 50), fill=C(240, 150, 190))
    for (dx, dy) in ((-10, -20), (0, -24), (10, -20)):
        d.line((36, 24, 36 + dx, 24 + dy), fill=C(60, 70, 110), width=2)
        d.ellipse((36 + dx - 3, 24 + dy - 4, 36 + dx + 3, 24 + dy + 2), fill=CREST)
    return scale_face(im, 'pavao')


def curu_face():
    im, d = fcanvas()
    for k, x in enumerate(range(10, 66, 7)):
        h = 26 + (k % 2) * 10
        d.polygon([(x - 6, 30), (x + 1, 30 - h), (x + 7, 30)], fill=FIRE)
        d.polygon([(x - 2, 30), (x + 1, 38 - h), (x + 3, 30)], fill=FIRE_L)
    face_base(d, CU_SK, CU_SK_D, LEAF, LEAF_D)
    d.polygon([(16, 20), (56, 20), (52, 30), (44, 24), (36, 30), (28, 24), (20, 30)], fill=FIRE)
    face_eyes(d, 'happy', C(60, 120, 40))
    brows(d, 'smug', FIRE_D)
    d.chord((26, 46, 46, 60), 0, 180, fill=C(120, 30, 40)); d.rectangle((28, 50, 44, 51), fill=C(150, 230, 120))
    return scale_face(im, 'curupira')


def main():
    make_char('$Baratelli_Diva', diva_down, diva_left, diva_up)
    make_char('$Kevinho_Uma', kevu_down, kevu_left, kevu_up)
    make_char('$Leona_Adulta', leoa_down, leoa_left, leoa_up)
    make_char('$Vera_Verao', vera_down, vera_left, vera_up)
    make_char('$Arara', arara_down, arara_left, arara_up)
    make_char('$Capivara_Maromba', capi_down, capi_left, capi_up)
    make_char('$Curupira', curu_down, curu_left, curu_up)
    make_big_char('$Pavao_Hipopotamo', pavao_down, pavao_left, pavao_up)
    face_sheet([kevu_face('normal'), kevu_face('serio'), kevu_face('feliz'), kevu_face('susto')], 'Kevinho_Uma')
    face_sheet([leoa_face('deboche'), leoa_face('riso'), leoa_face('raiva')], 'Leona_Adulta')
    face_sheet([vera_face('normal'), vera_face('riso'), vera_face('serio')], 'Vera_Verao')
    face_sheet([pavao_face(), curu_face()], 'Mauara')
    names = ['$Baratelli_Diva', '$Kevinho_Uma', '$Leona_Adulta', '$Vera_Verao', '$Arara', '$Capivara_Maromba', '$Curupira']
    cmb = Image.new('RGBA', (154 * len(names), 192), (120, 150, 110, 255))
    for i, n in enumerate(names):
        cmb.alpha_composite(Image.open(PROJ + f'/img/characters/{n}.png').convert('RGBA'), (i * 154, 0))
    cmb.resize((cmb.width * 2, cmb.height * 2), Image.NEAREST).save(PREV4 + 'ch4_chars.png')
    fc = Image.new('RGBA', (576 * 2 + 10, 288 * 2 + 10), (70, 80, 100, 255))
    for i, n in enumerate(['Kevinho_Uma', 'Leona_Adulta', 'Vera_Verao', 'Mauara']):
        fc.alpha_composite(Image.open(PROJ + f'/img/faces/{n}.png').convert('RGBA'), ((i % 2) * 586, (i // 2) * 298))
    fc.save(PREV4 + 'ch4_faces.png')
    print('ok')


if __name__ == '__main__':
    main()
