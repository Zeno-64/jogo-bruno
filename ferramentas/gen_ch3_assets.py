# Capitulo 3: Baratelli cigana, Kevinho, vidente, Gusrola sapo, mula sem cabeca, portal, macaco e imagens.
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_assets as G
from gen_assets import C, outline, sheet, PROJ
import gen_ch1_assets as G1
import gen_ch2_chars as C2
from gen_ch2_chars import (blank, fcanvas, face_eyes, brows, mouth, face_base, scale_face, face_sheet,
                           make_char, add_shadow, darker, lighter, WHITE, EYE_D, MOUTH)

G.PREV = HERE + '/prev/'


# ================================================================ BARATELLI CIGANA (vestido vermelho, chiquinhas)
SK, SK_D = G.SKIN, G.SKIN_D
HR, HR_L, HR_D = G.HAIR, G.HAIR_L, G.HAIR_D
RED = C(204, 42, 60); RED_L = C(236, 98, 108); RED_D = C(150, 24, 42); RED_DD = C(110, 16, 30)
RIB = C(250, 210, 60)
OUTB = C(46, 24, 30)


def red_skirt(d, cx, top, bottom, wtop, wbot, sway=0):
    d.polygon([(cx - wtop, top), (cx + wtop, top), (cx + wbot + sway, bottom), (cx - wbot + sway, bottom)], fill=RED)
    for yy in range(top + 4, bottom + 1, 4):
        t = (yy - top) / (bottom - top)
        w = int(wtop + (wbot - wtop) * t); s = int(sway * t)
        d.line((cx - w + s, yy - 1, cx + w + s, yy - 1), fill=RED_L)
        d.line((cx - w + s, yy, cx + w + s, yy), fill=RED_D)
    d.line((cx - wbot + sway, bottom, cx + wbot + sway, bottom), fill=RED_DD)
    for x in range(cx - wbot + 1 + sway, cx + wbot + sway, 3):
        d.point((x, bottom - 1), fill=C(250, 230, 200))


def pigtail(d, x0, y0, flip=1):
    pts = [(x0, y0), (x0 + 6 * flip, y0 + 2), (x0 + 7 * flip, y0 + 12), (x0 + 4 * flip, y0 + 20), (x0 - 1 * flip, y0 + 14)]
    d.polygon(pts, fill=HR)
    G.curls(d, (min(x0, x0 + 7 * flip), y0 + 2, max(x0, x0 + 7 * flip), y0 + 18), HR_L)
    d.rectangle((x0 - 1, y0 - 1, x0 + 2, y0 + 2), fill=RIB)


def flower(d, x, y):
    for k in range(5):
        a = k / 5 * 2 * math.pi
        px, py = x + math.cos(a) * 2, y + math.sin(a) * 2
        d.ellipse((px - 1.5, py - 1.5, px + 1.5, py + 1.5), fill=C(230, 30, 70))
    d.point((x, y), fill=C(255, 220, 60))


def bc_head_front(d):
    d.ellipse((15, 5, 33, 18), fill=HR)
    d.ellipse((17, 10, 31, 25), fill=SK)
    d.rectangle((17, 16, 18, 21), fill=G.BEARD); d.rectangle((30, 16, 31, 21), fill=G.BEARD)
    d.polygon([(18, 20), (30, 20), (30, 23), (27, 27), (21, 27), (18, 23)], fill=G.BEARD)
    d.line((20, 19, 28, 19), fill=G.BEARD); d.line((21, 24, 27, 24), fill=G.BEARD_L); d.line((22, 22, 26, 22), fill=G.MOUTH)
    d.rectangle((18, 13, 22, 16), outline=G.GLASS, fill=G.LENS); d.rectangle((26, 13, 30, 16), outline=G.GLASS, fill=G.LENS)
    d.line((23, 14, 25, 14), fill=G.GLASS)
    d.rectangle((20, 14, 20, 15), fill=G.EYE); d.rectangle((28, 14, 28, 15), fill=G.EYE)
    d.polygon([(16, 9), (32, 9), (32, 12), (28, 11), (24, 13), (20, 11), (16, 12)], fill=HR)
    G.curls(d, (17, 6, 31, 11), HR_L)
    pigtail(d, 15, 11, -1); pigtail(d, 33, 11, 1)
    flower(d, 19, 7)


def bc_down(p):
    im, d = blank()
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.rectangle((18, ly, 21, ly + 2), fill=G.SHOE); d.rectangle((27, ry, 30, ry + 2), fill=G.SHOE)
    red_skirt(d, 24, 30, 43, 7, 11, sway=p)
    d.rectangle((18, 24, 30, 31), fill=RED); d.line((18, 31, 30, 31), fill=RED_D)
    d.line((19, 24, 24, 29), fill=C(250, 236, 220)); d.line((29, 24, 24, 29), fill=C(250, 236, 220))
    d.rectangle((15, 27, 17, 32), fill=SK); d.rectangle((31, 27, 33, 32), fill=SK)
    d.ellipse((13, 22, 19, 28), fill=RED_L); d.ellipse((29, 22, 35, 28), fill=RED_L)
    bc_head_front(d)
    return outline(im, OUTB)


def bc_left(p):
    im, d = blank()
    fx = {-1: 15, 0: 19, 1: 22}[p]; bx = {-1: 26, 0: 24, 1: 19}[p]
    d.rectangle((bx, 43, bx + 4, 45), fill=G.SHOE_D); d.rectangle((fx, 43, fx + 4, 45), fill=G.SHOE)
    red_skirt(d, 24, 30, 43, 5, 10, sway=-p)
    d.rectangle((20, 24, 28, 31), fill=RED); d.line((20, 31, 28, 31), fill=RED_D)
    d.rectangle((22, 27, 24, 33), fill=SK); d.ellipse((20, 22, 27, 28), fill=RED_L)
    # rabo de cavalo e chiquinha de tras
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
    pigtail(d, 27, 11, 1)
    flower(d, 17, 7)
    return outline(im, OUTB)


def bc_up(p):
    im, d = blank()
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.rectangle((18, ly, 21, ly + 2), fill=G.SHOE); d.rectangle((27, ry, 30, ry + 2), fill=G.SHOE)
    red_skirt(d, 24, 30, 43, 7, 11, sway=-p)
    d.rectangle((18, 24, 30, 31), fill=RED)
    d.rectangle((15, 27, 17, 32), fill=SK); d.rectangle((31, 27, 33, 32), fill=SK)
    d.ellipse((13, 22, 19, 28), fill=RED_L); d.ellipse((29, 22, 35, 28), fill=RED_L)
    d.ellipse((15, 5, 33, 24), fill=HR)
    G.curls(d, (16, 7, 32, 22), HR_L)
    pigtail(d, 15, 11, -1); pigtail(d, 33, 11, 1)
    d.polygon([(21, 16), (27, 16), (28 + p, 30), (24 + p, 35), (20 + p, 30)], fill=HR_D)
    G.curls(d, (21, 18, 28, 33), HR_L)
    d.rectangle((22, 14, 26, 17), fill=RIB)
    flower(d, 29, 7)
    return outline(im, OUTB)


# ================================================================ KEVINHO
KSK = C(232, 192, 160); KSK_D = C(204, 160, 128)
KHR = C(58, 40, 30); KHR_L = C(96, 70, 52)
HOOD = C(58, 142, 92); HOOD_L = C(92, 180, 124); HOOD_D = C(36, 100, 62)
JEAN = C(58, 82, 132); JEAN_D = C(40, 58, 98)
SNK = C(244, 244, 244); SNK_R = C(210, 50, 60)


def kev_down(p):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((18, 33, 22, ly), fill=JEAN); d.rectangle((26, 33, 30, ry), fill=JEAN)
    d.line((22, 33, 22, ly), fill=JEAN_D); d.line((26, 33, 26, ry), fill=JEAN_D)
    d.rectangle((17, ly, 22, ly + 3), fill=SNK); d.line((17, ly + 3, 22, ly + 3), fill=SNK_R)
    d.rectangle((26, ry, 31, ry + 3), fill=SNK); d.line((26, ry + 3, 31, ry + 3), fill=SNK_R)
    d.polygon([(15, 21), (33, 21), (34, 35), (14, 35)], fill=HOOD)
    d.rectangle((19, 29, 29, 34), fill=HOOD_D)
    d.line((21, 22, 21, 27), fill=WHITE); d.line((27, 22, 27, 27), fill=WHITE)
    d.rectangle((11, 22, 15, 33), fill=HOOD_L); d.rectangle((33, 22, 37, 33), fill=HOOD_L)
    d.rectangle((11, 33, 15, 35), fill=KSK); d.rectangle((33, 33, 37, 35), fill=KSK)
    d.ellipse((15, 17, 33, 23), fill=HOOD_D)
    d.ellipse((16, 5, 32, 22), fill=KSK)
    d.ellipse((14, 11, 17, 16), fill=KSK_D); d.ellipse((31, 11, 34, 16), fill=KSK_D)
    d.rectangle((20, 13, 21, 15), fill=EYE_D); d.rectangle((27, 13, 28, 15), fill=EYE_D)
    d.point((20, 13), fill=WHITE); d.point((27, 13), fill=WHITE)
    d.arc((21, 15, 27, 20), 20, 160, fill=C(150, 70, 60))
    d.polygon([(15, 9), (17, 3), (21, 5), (24, 2), (28, 5), (31, 3), (33, 9), (32, 11), (27, 9), (22, 10), (16, 11)], fill=KHR)
    d.line((19, 5, 22, 8), fill=KHR_L); d.line((26, 4, 28, 7), fill=KHR_L)
    return outline(im, C(30, 26, 30))


def kev_left(p):
    im, d = blank()
    fx = {-1: 14, 0: 19, 1: 23}[p]; bx = {-1: 26, 0: 23, 1: 18}[p]
    d.rectangle((bx, 33, bx + 4, 42), fill=JEAN_D); d.rectangle((bx - 1, 42, bx + 4, 45), fill=C(210, 210, 210))
    d.rectangle((fx, 33, fx + 4, 42), fill=JEAN); d.rectangle((fx - 2, 42, fx + 4, 45), fill=SNK)
    d.line((fx - 2, 45, fx + 4, 45), fill=SNK_R)
    d.polygon([(17, 21), (31, 21), (32, 35), (16, 35)], fill=HOOD)
    d.polygon([(26, 18), (33, 20), (32, 28), (27, 25)], fill=HOOD_D)
    d.rectangle((21, 23, 25, 33), fill=HOOD_L); d.rectangle((21, 33, 25, 35), fill=KSK)
    d.ellipse((14, 5, 30, 22), fill=KSK)
    d.ellipse((24, 11, 27, 16), fill=KSK_D)
    d.point((13, 14), fill=KSK)
    d.rectangle((17, 13, 18, 15), fill=EYE_D); d.point((17, 13), fill=WHITE)
    d.line((15, 18, 18, 18), fill=C(150, 70, 60))
    d.polygon([(14, 9), (16, 3), (20, 4), (24, 2), (29, 5), (31, 10), (29, 14), (26, 10), (20, 9), (15, 11)], fill=KHR)
    d.line((22, 4, 25, 7), fill=KHR_L)
    return outline(im, C(30, 26, 30))


def kev_up(p):
    im, d = blank()
    ly = 42 + (1 if p == -1 else 0); ry = 42 + (1 if p == 1 else 0)
    d.rectangle((18, 33, 22, ly), fill=JEAN); d.rectangle((26, 33, 30, ry), fill=JEAN)
    d.rectangle((17, ly, 22, ly + 3), fill=SNK); d.rectangle((26, ry, 31, ry + 3), fill=SNK)
    d.rectangle((11, 22, 15, 33), fill=HOOD_L); d.rectangle((33, 22, 37, 33), fill=HOOD_L)
    d.polygon([(15, 21), (33, 21), (34, 35), (14, 35)], fill=HOOD)
    d.ellipse((17, 17, 31, 28), fill=HOOD_D)
    d.ellipse((16, 5, 32, 22), fill=KHR)
    d.ellipse((14, 11, 17, 16), fill=KSK_D); d.ellipse((31, 11, 34, 16), fill=KSK_D)
    d.polygon([(15, 9), (17, 3), (21, 5), (24, 2), (28, 5), (31, 3), (33, 9)], fill=KHR)
    d.line((20, 6, 21, 18), fill=KHR_L); d.line((27, 6, 27, 17), fill=KHR_L)
    return outline(im, C(30, 26, 30))


# ================================================================ VIDENTE (Leandra envelhecida e careca)
OLD = C(236, 206, 182); OLD_D = C(206, 170, 146); WR = C(186, 146, 122)
SHAWL = C(108, 58, 140); SHAWL_L = C(146, 96, 180); SHAWL_D = C(74, 36, 100); GOLDT = C(236, 196, 86)
STAFF = C(120, 82, 48)


def vid_down(p):
    im, d = blank()
    d.line((36, 14, 37, 45), fill=STAFF, width=2); d.ellipse((34, 11, 39, 16), fill=C(150, 200, 255))
    d.polygon([(14, 22), (34, 22), (37, 44), (11, 44)], fill=SHAWL)
    for x in range(13, 37, 4):
        d.line((x, 43, x + 1, 44), fill=GOLDT)
    d.line((14, 44, 36, 44), fill=SHAWL_D)
    d.polygon([(13, 20), (35, 20), (30, 30), (24, 33), (18, 30)], fill=SHAWL_L)
    d.line((18, 30, 24, 33), fill=GOLDT); d.line((30, 30, 24, 33), fill=GOLDT)
    d.rectangle((33, 26, 36, 30), fill=OLD)
    d.ellipse((16, 6, 32, 23), fill=OLD)
    d.arc((19, 7, 29, 14), 190, 300, fill=WHITE)
    d.line((20, 10, 28, 10), fill=WR)
    d.ellipse((14, 12, 17, 17), fill=OLD_D); d.ellipse((31, 12, 34, 17), fill=OLD_D)
    for ex in (20, 27):
        d.rectangle((ex, 14, ex + 1, 15), fill=C2.EYE_BLUE)
        d.line((ex - 1, 13, ex + 2, 13), fill=WR)
    d.line((19, 17, 20, 18), fill=WR); d.line((29, 17, 28, 18), fill=WR)
    d.line((22, 20, 26, 20), fill=C(150, 90, 90))
    return outline(im, C(40, 24, 40))


def vid_left(p):
    im, d = blank()
    d.line((14, 14, 13, 45), fill=STAFF, width=2); d.ellipse((11, 11, 16, 16), fill=C(150, 200, 255))
    d.polygon([(17, 22), (33, 22), (38, 44), (14, 44)], fill=SHAWL)
    d.line((15, 44, 37, 44), fill=GOLDT)
    d.polygon([(16, 20), (33, 20), (34, 30), (20, 30)], fill=SHAWL_L)
    d.rectangle((15, 26, 18, 30), fill=OLD)
    d.ellipse((15, 6, 31, 23), fill=OLD)
    d.arc((18, 7, 28, 14), 190, 300, fill=WHITE)
    d.ellipse((24, 12, 27, 17), fill=OLD_D)
    d.point((14, 15), fill=OLD)
    d.rectangle((18, 14, 19, 15), fill=C2.EYE_BLUE); d.line((17, 13, 20, 13), fill=WR)
    d.line((15, 20, 17, 20), fill=C(150, 90, 90)); d.line((19, 17, 20, 18), fill=WR)
    return outline(im, C(40, 24, 40))


def vid_up(p):
    im, d = blank()
    d.line((36, 14, 37, 45), fill=STAFF, width=2)
    d.polygon([(14, 22), (34, 22), (37, 44), (11, 44)], fill=SHAWL)
    d.line((14, 44, 36, 44), fill=GOLDT)
    d.polygon([(13, 18), (35, 18), (33, 36), (15, 36)], fill=SHAWL_L)
    d.ellipse((16, 6, 32, 23), fill=OLD)
    d.arc((19, 8, 29, 16), 200, 340, fill=WHITE)
    d.ellipse((14, 12, 17, 17), fill=OLD_D); d.ellipse((31, 12, 34, 17), fill=OLD_D)
    return outline(im, C(40, 24, 40))


# ================================================================ GUSROLA SAPO
FRG = C(94, 168, 76); FRG_L = C(140, 204, 108); FRG_D = C(60, 118, 48); BELLY = C(214, 228, 150)
VEST = C(120, 70, 40); VEST_D = C(84, 46, 26)


def frog_down(p):
    im, d = blank()
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.ellipse((14, ly - 3, 23, ly + 2), fill=FRG_D); d.ellipse((25, ry - 3, 34, ry + 2), fill=FRG_D)
    d.ellipse((13, 20, 35, 42), fill=FRG)
    d.ellipse((17, 24, 31, 40), fill=BELLY)
    d.polygon([(13, 24), (19, 22), (20, 36), (14, 34)], fill=VEST); d.polygon([(35, 24), (29, 22), (28, 36), (34, 34)], fill=VEST)
    d.ellipse((8, 26, 14, 36), fill=FRG); d.ellipse((34, 26, 40, 36), fill=FRG)
    d.ellipse((12, 6, 36, 24), fill=FRG)
    d.ellipse((12, 3, 21, 12), fill=FRG_L); d.ellipse((27, 3, 36, 12), fill=FRG_L)
    d.ellipse((14, 5, 19, 10), fill=WHITE); d.ellipse((29, 5, 34, 10), fill=WHITE)
    d.rectangle((16, 6, 17, 9), fill=EYE_D); d.rectangle((31, 6, 32, 9), fill=EYE_D)
    d.arc((15, 12, 33, 22), 20, 160, fill=FRG_D, width=2)
    d.point((22, 14), fill=FRG_D); d.point((26, 14), fill=FRG_D)
    d.point((18, 18), fill=C(230, 120, 120)); d.point((30, 18), fill=C(230, 120, 120))
    return outline(im, C(24, 50, 20))


def frog_left(p):
    im, d = blank()
    fx = {-1: 14, 0: 18, 1: 22}[p]
    d.ellipse((fx, 39, fx + 11, 45), fill=FRG_D)
    d.ellipse((14, 20, 36, 42), fill=FRG)
    d.ellipse((15, 24, 25, 40), fill=BELLY)
    d.polygon([(24, 22), (34, 24), (33, 36), (24, 36)], fill=VEST)
    d.ellipse((18, 28, 26, 36), fill=FRG)
    d.ellipse((8, 7, 32, 24), fill=FRG)
    d.ellipse((14, 2, 25, 12), fill=FRG_L)
    d.ellipse((15, 4, 21, 10), fill=WHITE); d.rectangle((16, 5, 17, 8), fill=EYE_D)
    d.line((8, 17, 20, 19), fill=FRG_D, width=2)
    return outline(im, C(24, 50, 20))


def frog_up(p):
    im, d = blank()
    ly = 43 + (1 if p == -1 else 0); ry = 43 + (1 if p == 1 else 0)
    d.ellipse((14, ly - 3, 23, ly + 2), fill=FRG_D); d.ellipse((25, ry - 3, 34, ry + 2), fill=FRG_D)
    d.ellipse((8, 26, 14, 36), fill=FRG); d.ellipse((34, 26, 40, 36), fill=FRG)
    d.ellipse((13, 20, 35, 42), fill=VEST)
    d.line((24, 22, 24, 40), fill=VEST_D)
    d.ellipse((12, 6, 36, 24), fill=FRG)
    d.ellipse((12, 3, 21, 12), fill=FRG_L); d.ellipse((27, 3, 36, 12), fill=FRG_L)
    for (x, y) in ((18, 15), (28, 13), (23, 19)):
        d.ellipse((x, y, x + 3, y + 3), fill=FRG_D)
    return outline(im, C(24, 50, 20))


# ================================================================ MULA SEM CABECA
MULE = C(120, 80, 50); MULE_L = C(156, 110, 72); MULE_D = C(84, 54, 32)


def fire(d, cx, cy, s, phase):
    rng = random.Random(phase)
    for k, col in enumerate([(255, 120, 30), (255, 190, 60), (255, 240, 170)]):
        r = s - k * s // 3
        pts = [(cx - r, cy)]
        for i in range(5):
            x = cx - r + (2 * r) * (i + 0.5) / 5
            pts.append((x, cy - r * 2.2 - rng.randint(0, 3) + (k * 2)))
            pts.append((cx - r + (2 * r) * (i + 1) / 5, cy - r * 1.2))
        pts.append((cx + r, cy))
        d.polygon(pts, fill=col + (255,))


def mule_down(p):
    im, d = blank()
    for (x, off) in ((14, p), (30, -p)):
        d.rectangle((x, 34, x + 3, 44 + (1 if off > 0 else 0)), fill=MULE_D)
    d.ellipse((11, 18, 37, 40), fill=MULE)
    d.ellipse((14, 20, 34, 30), fill=MULE_L)
    d.rectangle((19, 12, 29, 24), fill=MULE)
    d.rectangle((19, 12, 29, 14), fill=MULE_D)
    for (x, off) in ((19, -p), (26, p)):
        d.rectangle((x, 36, x + 3, 45 + (1 if off > 0 else 0)), fill=MULE)
    im = outline(im, C(40, 24, 14))
    d = ImageDraw.Draw(im)
    fire(d, 24, 13, 6, p + 2)
    return im


def mule_left(p):
    im, d = blank()
    off = {-1: (-2, 2), 0: (0, 0), 1: (2, -2)}[p]
    for x, o in ((34, off[0]), (16, off[1])):
        d.rectangle((x + o, 32, x + o + 3, 43), fill=MULE_D)
    d.ellipse((12, 18, 42, 36), fill=MULE)
    d.ellipse((15, 19, 39, 26), fill=MULE_L)
    d.polygon([(10, 22), (16, 14), (21, 16), (18, 26)], fill=MULE)
    d.line((41, 22, 45, 30), fill=MULE_D, width=2)
    for x, o in ((30, off[1]), (19, off[0])):
        d.rectangle((x + o, 33, x + o + 3, 45), fill=MULE)
    im = outline(im, C(40, 24, 14))
    d = ImageDraw.Draw(im)
    fire(d, 14, 15, 6, p + 5)
    return im


def mule_up(p):
    im, d = blank()
    for (x, off) in ((14, p), (30, -p)):
        d.rectangle((x, 34, x + 3, 44 + (1 if off > 0 else 0)), fill=MULE_D)
    d.ellipse((11, 16, 37, 40), fill=MULE)
    d.line((24, 36, 24 + p, 44), fill=MULE_D, width=3)
    im = outline(im, C(40, 24, 14))
    d = ImageDraw.Draw(im)
    fire(d, 24, 16, 5, p + 8)
    return im


# ================================================================ MACACO
MAC = C(130, 84, 48); MAC_L = C(176, 128, 84); MAC_F = C(230, 196, 160)


def mac_down(p):
    im, d = blank()
    d.line([(32, 36), (38, 30 + p), (36, 22)], fill=MAC, width=2)
    d.ellipse((15, 26, 33, 43), fill=MAC)
    d.ellipse((19, 30, 29, 41), fill=MAC_L)
    d.rectangle((16, 40, 20, 44 + (1 if p < 0 else 0)), fill=MAC); d.rectangle((28, 40, 32, 44 + (1 if p > 0 else 0)), fill=MAC)
    d.ellipse((13, 13, 35, 31), fill=MAC)
    d.ellipse((10, 18, 16, 24), fill=MAC_F); d.ellipse((32, 18, 38, 24), fill=MAC_F)
    d.ellipse((17, 17, 31, 30), fill=MAC_F)
    d.rectangle((20, 20, 21, 22), fill=EYE_D); d.rectangle((27, 20, 28, 22), fill=EYE_D)
    d.arc((20, 23, 28, 28), 20, 160, fill=C(120, 60, 50))
    return outline(im, C(50, 30, 16))


def mac_left(p):
    im, d = blank()
    d.line([(32, 38), (40, 34 - p), (41, 25)], fill=MAC, width=2)
    d.ellipse((16, 26, 34, 43), fill=MAC)
    d.rectangle((18 + p, 40, 22 + p, 45), fill=MAC); d.rectangle((26 - p, 40, 30 - p, 45), fill=MAC)
    d.ellipse((12, 13, 32, 31), fill=MAC)
    d.ellipse((24, 17, 30, 23), fill=MAC_F)
    d.ellipse((10, 17, 22, 29), fill=MAC_F)
    d.rectangle((14, 20, 15, 22), fill=EYE_D)
    d.line((11, 26, 14, 26), fill=C(120, 60, 50))
    return outline(im, C(50, 30, 16))


def mac_up(p):
    im, d = blank()
    d.ellipse((15, 26, 33, 43), fill=MAC)
    d.rectangle((16, 40, 20, 44 + (1 if p < 0 else 0)), fill=MAC); d.rectangle((28, 40, 32, 44 + (1 if p > 0 else 0)), fill=MAC)
    d.line([(24, 40), (26 + p, 45), (30, 46)], fill=MAC_L, width=2)
    d.ellipse((13, 13, 35, 31), fill=MAC)
    d.ellipse((10, 18, 16, 24), fill=MAC_F); d.ellipse((32, 18, 38, 24), fill=MAC_F)
    return outline(im, C(50, 30, 16))


# ================================================================ PORTAL (objeto animado)
def make_portal():
    frames = []
    for k in range(3):
        f = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
        glow = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((4, 8, 44, 46), fill=(150, 60, 220, 200))
        f.alpha_composite(glow.filter(ImageFilter.GaussianBlur(3)))
        d = ImageDraw.Draw(f)
        d.ellipse((8, 11, 40, 44), fill=(40, 10, 70, 255))
        for i in range(3):
            a0 = k * 40 + i * 120
            d.arc((10 + i * 3, 13 + i * 3, 38 - i * 3, 42 - i * 3), a0, a0 + 200, fill=(200, 140, 255, 255), width=2)
        d.ellipse((20, 23, 28, 32), fill=(10, 0, 20, 255))
        frames.append(f)
    sh = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for r in range(4):
        for c, f in enumerate(frames):
            sh.alpha_composite(f, (c * 48, r * 48))
    sh.save(PROJ + '/img/characters/!$Portal.png')


# ================================================================ ROSTOS
def kevinho_face(expr):
    im, d = fcanvas()
    face_base(d, KSK, KSK_D, HOOD, HOOD_D)
    d.line((28, 60, 28, 72), fill=WHITE); d.line((44, 60, 44, 72), fill=WHITE)
    d.polygon([(20, 58), (52, 58), (56, 64), (16, 64)], fill=HOOD_D)
    face_eyes(d, 'normal', C(80, 56, 40))
    brows(d, 'angry' if expr == 'serious' else 'normal', KHR)
    mouth(d, 'frown' if expr == 'serious' else 'smile')
    d.polygon([(14, 26), (16, 10), (24, 14), (30, 4), (38, 12), (46, 4), (52, 12), (58, 10), (58, 28), (52, 22),
               (44, 26), (36, 20), (28, 26), (20, 22), (15, 30)], fill=KHR)
    for (a, b) in (((24, 14), (28, 22)), ((38, 12), (40, 20)), ((46, 6), (48, 14))):
        d.line(a + b, fill=KHR_L, width=2)
    return scale_face(im, 'kevinho')


def vidente_face(expr):
    im, d = fcanvas()
    face_base(d, OLD, OLD_D, SHAWL, SHAWL_D)
    d.polygon([(18, 56), (36, 70), (54, 56), (60, 64), (36, 72), (12, 64)], fill=SHAWL_L)
    d.line((22, 60, 36, 70), fill=GOLDT); d.line((50, 60, 36, 70), fill=GOLDT)
    d.ellipse((16, 8, 56, 52), fill=OLD)
    d.polygon([(18, 38), (54, 38), (50, 52), (36, 60), (22, 52)], fill=OLD)
    d.ellipse((14, 34, 19, 44), fill=OLD); d.ellipse((53, 34, 58, 44), fill=OLD)
    d.arc((22, 10, 44, 28), 190, 290, fill=WHITE, width=2)
    for y in (22, 26):
        d.arc((26, y - 4, 46, y + 4), 200, 340, fill=WR)
    face_eyes(d, 'smug' if expr == 'normal' else 'pain', C2.EYE_BLUE)
    for (x, s) in ((20, 1), (52, -1)):
        d.line((x, 38, x - 3 * s, 36), fill=WR); d.line((x, 40, x - 3 * s, 41), fill=WR)
    brows(d, 'sad', C(200, 180, 170))
    d.line((26, 48, 30, 52), fill=WR); d.line((46, 48, 42, 52), fill=WR)
    mouth(d, 'frown' if expr == 'normal' else 'open')
    if expr != 'normal':
        d.line((22, 42, 21, 52), fill=C(150, 200, 255), width=2); d.line((50, 42, 51, 52), fill=C(150, 200, 255), width=2)
    return scale_face(im, 'vidente')


def sapo_face():
    im, d = fcanvas()
    d.polygon([(4, 72), (10, 60), (26, 56), (46, 56), (62, 60), (68, 72)], fill=VEST)
    d.polygon([(24, 56), (48, 56), (44, 72), (28, 72)], fill=BELLY)
    d.ellipse((8, 18, 64, 62), fill=FRG)
    d.ellipse((12, 30, 60, 62), fill=FRG_L)
    for cx in (20, 52):
        d.ellipse((cx - 13, 4, cx + 13, 30), fill=FRG)
        d.ellipse((cx - 9, 8, cx + 9, 26), fill=WHITE)
        d.ellipse((cx - 4, 12, cx + 4, 24), fill=EYE_D)
        d.rectangle((cx - 3, 13, cx - 2, 15), fill=WHITE)
    d.arc((14, 32, 58, 56), 15, 165, fill=FRG_D, width=3)
    d.point((32, 36), fill=FRG_D); d.point((40, 36), fill=FRG_D)
    d.ellipse((16, 40, 22, 44), fill=C(230, 140, 140)); d.ellipse((50, 40, 56, 44), fill=C(230, 140, 140))
    for (x, y) in ((28, 22), (44, 24), (36, 28)):
        d.ellipse((x, y, x + 4, y + 4), fill=FRG_D)
    return scale_face(im, 'sapo')


# ================================================================ GUSROLA SAPO (inimigo)
def make_frog_battler(sombra=True, destino=None):
    S = 2
    W, H = 330, 400
    im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sc = lambda *v: tuple(int(x * S) for x in v)
    fg, fl, fd = (94, 168, 76, 255), (140, 204, 108, 255), (58, 116, 46, 255)
    belly = (214, 228, 150, 255); vest = (120, 70, 40, 255)
    if sombra:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse(sc(60, 370, 270, 398), fill=(0, 0, 0, 90))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    for x0 in (80, 190):
        d.ellipse(sc(x0 - 10, 330, x0 + 70, 385), fill=fd)
        d.ellipse(sc(x0 + 10, 300, x0 + 50, 360), fill=fg)
    d.ellipse(sc(70, 150, 260, 360), fill=fg)
    d.ellipse(sc(105, 190, 225, 350), fill=belly)
    d.polygon(sc(70, 200, 120, 170, 125, 330, 85, 320), fill=vest)
    d.polygon(sc(260, 200, 210, 170, 205, 330, 245, 320), fill=vest)
    for side in (-1, 1):
        cx = 165 + side * 105
        d.ellipse(sc(cx - 25, 190, cx + 25, 280), fill=fg)
        d.ellipse(sc(cx - 30 + side * 10, 265, cx + 30 + side * 10, 300), fill=fl)
        for k in range(3):
            x = cx + side * 10 + (k - 1) * 18
            d.ellipse(sc(x - 8, 290, x + 8, 306), fill=fl)
    d.ellipse(sc(60, 50, 270, 200), fill=fg)
    d.ellipse(sc(80, 110, 250, 200), fill=fl)
    for cx in (110, 220):
        d.ellipse(sc(cx - 42, 18, cx + 42, 100), fill=fg)
        d.ellipse(sc(cx - 30, 30, cx + 30, 90), fill=(255, 255, 240, 255))
        d.ellipse(sc(cx - 14, 40, cx + 14, 82), fill=(20, 16, 20, 255))
        d.ellipse(sc(cx - 10, 46, cx - 2, 56), fill=(255, 255, 255, 255))
    d.chord(sc(95, 120, 235, 190), 10, 170, fill=(150, 40, 60, 255))
    d.line(sc(95, 150, 235, 150), fill=fd, width=4 * S)
    tongue = [(165, 170), (175, 200), (168, 230), (180, 255)]
    d.line([sc(*p) for p in tongue], fill=(230, 100, 130, 255), width=14 * S, joint='curve')
    d.ellipse(sc(168, 245, 194, 268), fill=(230, 100, 130, 255))
    for (x, y, r) in ((130, 75, 8), (200, 70, 7), (165, 95, 6), (95, 140, 7), (240, 135, 8)):
        d.ellipse(sc(x - r, y - r, x + r, y + r), fill=fd)
    d.ellipse(sc(130, 165, 140, 172), fill=(240, 140, 140, 255)); d.ellipse(sc(190, 165, 200, 172), fill=(240, 140, 140, 255))
    im = im.resize((W, H), Image.LANCZOS)
    im = outline(im, C(24, 50, 20))
    im.save(destino or PROJ + '/img/enemies/Gusrola_Sapo.png')
    if destino:
        return im
    G1.preview = None
    pv = Image.new('RGBA', im.size, (90, 90, 110, 255)); pv.alpha_composite(im); pv.save(G.PREV + 'sapo_battler.png')


# ================================================================ PENTAGRAMA (folha D do calabouco)
def make_pentagram():
    path = PROJ + '/img/tilesets/Calabouco_D.png'
    sheet_img = Image.open(path).convert('RGBA')
    S = 4
    big = Image.new('RGBA', (144 * S, 144 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    c = 72 * S; R = 64 * S
    glow = Image.new('RGBA', big.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse((c - R, c - R, c + R, c + R), outline=(190, 90, 255, 200), width=10 * S)
    big.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6 * S)))
    d = ImageDraw.Draw(big)
    col = (214, 150, 255, 255)
    d.ellipse((c - R, c - R, c + R, c + R), outline=col, width=3 * S)
    d.ellipse((c - R + 9 * S, c - R + 9 * S, c + R - 9 * S, c + R - 9 * S), outline=col, width=2 * S)
    pts = []
    r2 = R - 9 * S
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        pts.append((c + math.cos(a) * r2, c + math.sin(a) * r2))
    order = [0, 2, 4, 1, 3, 0]
    d.line([pts[i] for i in order], fill=col, width=3 * S, joint='curve')
    rng = random.Random(6)
    for k in range(20):
        a = k / 20 * 2 * math.pi
        x, y = c + math.cos(a) * (R - 4.5 * S), c + math.sin(a) * (R - 4.5 * S)
        d.ellipse((x - 1.5 * S, y - 1.5 * S, x + 1.5 * S, y + 1.5 * S), fill=(255, 230, 255, 255))
    small = big.resize((144, 144), Image.LANCZOS)
    for row in range(3):
        for colm in range(3):
            n = 8 + row * 8 + colm
            x, y = C2_tile_pos(n)
            sheet_img.paste((0, 0, 0, 0), (x, y, x + 48, y + 48))
            sheet_img.alpha_composite(small.crop((colm * 48, row * 48, colm * 48 + 48, row * 48 + 48)), (x, y))
    sheet_img.save(path)
    pv = Image.new('RGBA', (144, 144), (110, 50, 70, 255)); pv.alpha_composite(small)
    pv.resize((288, 288), Image.NEAREST).save(G.PREV + 'pentagrama.png')


def C2_tile_pos(n):
    return (((n // 128) % 2) * 8 + n % 8) * 48, ((n % 128) // 8) * 48


# ================================================================ IMAGENS DE CENA
def make_cards():
    gold = (246, 208, 110, 255); pink = (250, 214, 230, 255)
    G1.card(PROJ + '/img/pictures/Capitulo3.png', [
        (220, 'Capítulo 3', G1.font('georgiab.ttf', 64), gold),
        (350, 'Baratelli, a Cigana Vingativa', G1.font('georgiai.ttf', 36), pink),
    ])
    G1.card(PROJ + '/img/pictures/FimCapitulo3.png', [
        (220, 'Fim do Capítulo 3', G1.font('georgiab.ttf', 58), gold),
        (350, 'A vingança está só começando...', G1.font('georgiai.ttf', 30), pink),
    ])


def make_tarot():
    S = 2
    W, H = 380, 620
    im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sc = lambda *v: tuple(int(x * S) for x in v)
    d.rounded_rectangle(sc(0, 0, W - 1, H - 1), 18 * S, fill=(244, 232, 200, 255))
    d.rounded_rectangle(sc(10, 10, W - 11, H - 11), 12 * S, fill=(48, 26, 72, 255))
    d.rounded_rectangle(sc(18, 18, W - 19, H - 19), 10 * S, outline=(232, 190, 90, 255), width=3 * S)
    # ceu e lua
    sky = Image.new('RGBA', im.size, (0, 0, 0, 0)); skd = ImageDraw.Draw(sky)
    for i in range(60):
        y = 70 + i * 6
        skd.rectangle(sc(30, y, W - 30, y + 6), fill=(70 + i, 40 + i // 2, 110 + i // 2, 255))
    im.alpha_composite(sky)
    d = ImageDraw.Draw(im)
    rng = random.Random(2)
    for _ in range(40):
        x = rng.randint(36, W - 36); y = rng.randint(76, 300)
        d.ellipse(sc(x - 1, y - 1, x + 1, y + 1), fill=(255, 250, 220, 255))
    d.ellipse(sc(260, 90, 320, 150), fill=(250, 240, 200, 255)); d.ellipse(sc(276, 84, 336, 144), fill=(84, 52, 120, 255))
    # trem ao fundo
    d.rectangle(sc(36, 330, 170, 400), fill=(60, 60, 70, 255)); d.rectangle(sc(130, 300, 170, 340), fill=(70, 70, 82, 255))
    d.rectangle(sc(50, 300, 70, 330), fill=(50, 50, 60, 255))
    for (x, y, r) in ((60, 280, 14), (78, 258, 18), (102, 236, 22)):
        d.ellipse(sc(x - r, y - r, x + r, y + r), fill=(210, 210, 220, 220))
    for cx in (60, 100, 145):
        d.ellipse(sc(cx - 16, 386, cx + 16, 418), fill=(40, 40, 46, 255)); d.ellipse(sc(cx - 7, 395, cx + 7, 409), fill=(150, 150, 160, 255))
    d.rectangle(sc(30, 418, W - 30, 430), fill=(90, 70, 60, 255))
    # Baratelli maquinista
    skin = (242, 204, 174, 255); hair = (108, 68, 38, 255); hair_l = (146, 96, 58, 255); beard = (80, 52, 32, 255)
    over = (60, 96, 170, 255); over_d = (40, 70, 130, 255)
    cx = 220
    d.polygon(sc(cx - 70, 560, cx + 70, 560, cx + 60, 400, cx - 60, 400), fill=over)
    d.rectangle(sc(cx - 30, 400, cx + 30, 470), fill=over_d)
    d.line(sc(cx - 40, 400, cx - 30, 470), fill=(240, 200, 80, 255), width=4 * S); d.line(sc(cx + 40, 400, cx + 30, 470), fill=(240, 200, 80, 255), width=4 * S)
    d.polygon(sc(cx - 46, 380, cx + 46, 380, cx + 30, 410, cx, 420, cx - 30, 410), fill=(206, 44, 60, 255))
    for side in (-1, 1):
        sx = cx + side * 60
        d.polygon(sc(sx, 410, sx + side * 40, 330, sx + side * 62, 340, sx + side * 30, 430), fill=over)
        hx, hy = sx + side * 52, 300
        d.ellipse(sc(hx - 24, hy - 26, hx + 24, hy + 26), fill=skin)
        nails = [(255, 60, 130), (80, 200, 255), (250, 220, 40), (140, 230, 90), (190, 100, 255)]
        for k in range(5):
            ang = math.radians(-150 + k * 30) if side < 0 else math.radians(-30 - k * 30)
            fx, fy = hx + math.cos(ang) * 30, hy + math.sin(ang) * 32
            d.line(sc(hx + math.cos(ang) * 14, hy + math.sin(ang) * 16, fx, fy), fill=skin, width=10 * S)
            d.ellipse(sc(fx - 5, fy - 5, fx + 5, fy + 5), fill=nails[k] + (255,))
    d.ellipse(sc(cx - 48, 250, cx + 48, 370), fill=skin)
    d.polygon(sc(cx - 46, 320, cx + 46, 320, cx + 40, 352, cx + 18, 378, cx - 18, 378, cx - 40, 352), fill=beard)
    d.chord(sc(cx - 14, 336, cx + 14, 356), 0, 180, fill=(190, 104, 104, 255))
    for ex in (cx - 22, cx + 22):
        d.ellipse(sc(ex - 16, 296, ex + 16, 326), outline=(50, 50, 60, 255), width=4 * S, fill=(226, 236, 242, 255))
        d.ellipse(sc(ex - 4, 306, ex + 4, 316), fill=(36, 26, 26, 255))
    d.line(sc(cx - 6, 310, cx + 6, 310), fill=(50, 50, 60, 255), width=3 * S)
    for side in (-1, 1):
        x0 = cx + side * 48
        for k in range(5):
            y = 280 + k * 18
            d.ellipse(sc(x0 - 14 + side * 6, y - 12, x0 + 14 + side * 6, y + 12), fill=hair if k % 2 else hair_l)
    d.chord(sc(cx - 56, 222, cx + 56, 300), 180, 360, fill=(60, 96, 170, 255))
    for k in range(5):
        x = cx - 50 + k * 22
        d.line(sc(x, 226, x, 262), fill=(240, 240, 250, 255), width=5 * S)
    d.rectangle(sc(cx - 66, 258, cx + 66, 272), fill=(40, 70, 130, 255))
    # titulo e numeral
    tf = G1.font('georgiab.ttf', 30 * S); nf = G1.font('georgiab.ttf', 24 * S)
    t = 'A MAQUINISTA'; w = d.textlength(t, font=tf)
    d.rectangle(sc(30, 548, W - 30, 594), fill=(48, 26, 72, 255))
    d.text(((W * S - w) / 2, 554 * S), t, font=tf, fill=(240, 204, 110, 255))
    t = 'XXIII'; w = d.textlength(t, font=nf)
    d.text(((W * S - w) / 2, 32 * S), t, font=nf, fill=(240, 204, 110, 255))
    im = im.resize((W, H), Image.LANCZOS)
    glow = Image.new('RGBA', (W + 60, H + 60), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((20, 20, W + 40, H + 40), 24, fill=(255, 220, 140, 160))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    glow.alpha_composite(im, (30, 30))
    glow.save(PROJ + '/img/pictures/Carta_Maquinista.png')
    glow.resize((glow.width // 2, glow.height // 2)).save(G.PREV + 'carta.png')


def make_final():
    W, H = 816, 624
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    for y in range(H):
        t = y / H
        arr[y, :, 0] = int(16 + 40 * t); arr[y, :, 1] = int(14 + 22 * t); arr[y, :, 2] = int(44 + 50 * t); arr[y, :, 3] = 255
    im = Image.fromarray(arr, 'RGBA')
    rng = random.Random(11)
    d = ImageDraw.Draw(im)
    for _ in range(140):
        x, y = rng.randint(0, W), rng.randint(0, 380)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 250, 230, rng.randint(120, 255)))
    moon = Image.new('RGBA', (W, H), (0, 0, 0, 0)); md = ImageDraw.Draw(moon)
    md.ellipse((480, 70, 700, 290), fill=(255, 246, 210, 255))
    glow = moon.filter(ImageFilter.GaussianBlur(30))
    im.alpha_composite(glow); im.alpha_composite(glow); im.alpha_composite(moon)
    d = ImageDraw.Draw(im)
    for (x, y, r) in ((560, 140, 18), (630, 200, 12), (600, 240, 9)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=(236, 224, 186, 255))
    sil = (14, 8, 22, 255)
    d.polygon([(0, 520), (150, 470), (330, 490), (520, 455), (700, 480), (816, 470), (816, 624), (0, 624)], fill=(22, 16, 34, 255))
    # silhueta da Baratelli olhando para a lua, segurando o cranio
    cx, base = 330, 500
    d.polygon([(cx - 62, base), (cx + 62, base), (cx + 34, base - 120), (cx - 34, base - 120)], fill=sil)
    d.rectangle((cx - 30, base - 170, cx + 30, base - 112), fill=sil)
    d.ellipse((cx - 30, base - 236, cx + 34, base - 168), fill=sil)
    for side in (-1, 1):
        px = cx + side * 40
        d.polygon([(px, base - 214), (px + side * 22, base - 200), (px + side * 26, base - 150), (px + side * 12, base - 120), (px - side * 4, base - 160)], fill=sil)
    d.polygon([(cx - 8, base - 222), (cx - 34, base - 230), (cx - 52, base - 196), (cx - 46, base - 150), (cx - 30, base - 190)], fill=sil)
    d.polygon([(cx + 22, base - 160), (cx + 90, base - 230), (cx + 104, base - 222), (cx + 40, base - 148)], fill=sil)
    sk = Image.new('RGBA', (W, H), (0, 0, 0, 0)); skd = ImageDraw.Draw(sk)
    skd.ellipse((cx + 86, base - 286, cx + 136, base - 236), fill=(236, 230, 214, 255))
    skd.rectangle((cx + 98, base - 248, cx + 124, base - 230), fill=(236, 230, 214, 255))
    skd.ellipse((cx + 96, base - 270, cx + 108, base - 256), fill=(30, 20, 30, 255))
    skd.ellipse((cx + 114, base - 270, cx + 126, base - 256), fill=(30, 20, 30, 255))
    skd.polygon([(cx + 110, base - 254), (cx + 107, base - 247), (cx + 113, base - 247)], fill=(30, 20, 30, 255))
    for x in range(cx + 100, cx + 124, 5):
        skd.line((x, base - 238, x, base - 232), fill=(60, 50, 60, 255), width=2)
    sk_glow = sk.filter(ImageFilter.GaussianBlur(8))
    im.alpha_composite(sk_glow); im.alpha_composite(sk)
    d = ImageDraw.Draw(im)
    d.polygon([(cx + 84, base - 240), (cx + 100, base - 262), (cx + 106, base - 238), (cx + 96, base - 226)], fill=sil)
    lock = [(cx - 50, base - 140), (cx - 58, base - 120), (cx - 50, base - 100), (cx - 60, base - 80), (cx - 52, base - 64)]
    d.line(lock, fill=(120, 80, 50, 255), width=5, joint='curve')
    d.line([(p[0] + 3, p[1]) for p in lock], fill=(160, 110, 70, 255), width=2, joint='curve')
    for (x, y) in ((cx - 70, base - 90), (cx - 40, base - 70), (cx - 64, base - 52)):
        d.line((x - 4, y, x + 4, y), fill=(255, 240, 200, 200)); d.line((x, y - 4, x, y + 4), fill=(255, 240, 200, 200))
    im.save(PROJ + '/img/pictures/Final_Cap3.png')
    im.resize((408, 312)).save(G.PREV + 'final3.png')


def make_moonbeam():
    W, H = 240, 560
    a = np.zeros((H, W), dtype=float)
    xs = np.linspace(-1, 1, W)
    for y in range(H):
        t = y / H
        width = 0.35 + 0.45 * t
        a[y] = np.clip(1 - (np.abs(xs) / width) ** 2, 0, 1) * (0.35 + 0.45 * t)
    img = np.zeros((H, W, 4), dtype=np.uint8)
    img[..., 0] = 210; img[..., 1] = 230; img[..., 2] = 255; img[..., 3] = (a * 230).astype(np.uint8)
    Image.fromarray(img, 'RGBA').filter(ImageFilter.GaussianBlur(4)).save(PROJ + '/img/pictures/Raio_Lua.png')


if __name__ == '__main__':
    make_char('$Baratelli_Cigana', bc_down, bc_left, bc_up)
    make_char('$Kevinho', kev_down, kev_left, kev_up)
    make_char('$Vidente', vid_down, vid_left, vid_up)
    make_char('$Gusrola_Sapo', frog_down, frog_left, frog_up)
    make_char('$Mula_Sem_Cabeca', mule_down, mule_left, mule_up)
    make_char('$Macaco', mac_down, mac_left, mac_up)
    make_portal()
    face_sheet([kevinho_face('normal'), kevinho_face('serious')], 'Kevinho')
    face_sheet([vidente_face('normal'), vidente_face('cry')], 'Vidente')
    face_sheet([sapo_face()], 'Gusrola_Sapo')
    make_frog_battler()
    make_pentagram()
    make_cards()
    make_tarot()
    make_final()
    make_moonbeam()
    names = ['$Baratelli_Cigana', '$Kevinho', '$Vidente', '$Gusrola_Sapo', '$Mula_Sem_Cabeca', '$Macaco', '!$Portal']
    cmb = Image.new('RGBA', (154 * len(names), 192), (120, 150, 110, 255))
    for i, n in enumerate(names):
        cmb.alpha_composite(Image.open(PROJ + f'/img/characters/{n}.png').convert('RGBA'), (i * 154, 0))
    cmb.resize((cmb.width * 2, cmb.height * 2), Image.NEAREST).save(G.PREV + 'ch3_chars.png')
    fc = Image.new('RGBA', (576 * 3 + 20, 288), (70, 80, 100, 255))
    for i, n in enumerate(['Kevinho', 'Vidente', 'Gusrola_Sapo']):
        fc.alpha_composite(Image.open(PROJ + f'/img/faces/{n}.png').convert('RGBA'), (i * 586, 0))
    fc.crop((0, 0, 576 * 3 + 20, 144)).save(G.PREV + 'ch3_faces.png')
    print('ok')
