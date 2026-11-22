#!/usr/bin/env python3
"""The World in One Day - Sunday 22 November 2026. Self-contained stdlib-only
front-page generator. Pure-Python PNG encoder + hand-typed 5x7 bitmap font +
drawing primitives. Deterministic: same input -> byte-identical output."""
import struct, zlib

W, H = 1024, 1024

# ---------- palette ----------
INK    = (26, 26, 26)
PAPER  = (246, 241, 230)
CREAM  = (250, 246, 238)
NAVY   = (16, 32, 64)
NAVY2  = (24, 48, 96)
RED    = (178, 34, 34)
RED2   = (139, 0, 0)
GOLD   = (201, 162, 39)
GREY   = (110, 110, 108)
LGREY  = (210, 205, 192)
WHITE  = (255, 255, 255)
BLACK  = (10, 10, 10)
SKY    = (135, 180, 210)
DAWN   = (232, 148, 72)
DAWN2  = (244, 196, 120)
SEA    = (18, 42, 78)
NIGHT  = (14, 24, 54)
MOON   = (240, 234, 205)
FIRE   = (232, 98, 24)
FIRE2  = (250, 196, 60)
GREEN  = (34, 110, 70)
TEAL   = (0, 110, 105)
BROWN  = (122, 82, 40)
PINK   = (214, 120, 120)
LBLUE  = (90, 140, 190)

# ---------- 5x7 bitmap font: rows top->bottom, 5 bits each ----------
F = {}
def _g(ch, rows):
    F[ch] = [int(r, 2) for r in rows]
_g('A', ["01110","10001","10001","11111","10001","10001","10001"])
_g('B', ["11110","10001","10001","11110","10001","10001","11110"])
_g('C', ["01110","10001","10000","10000","10000","10001","01110"])
_g('D', ["11110","10001","10001","10001","10001","10001","11110"])
_g('E', ["11111","10000","10000","11110","10000","10000","11111"])
_g('F', ["11111","10000","10000","11110","10000","10000","10000"])
_g('G', ["01110","10001","10000","10111","10001","10001","01111"])
_g('H', ["10001","10001","10001","11111","10001","10001","10001"])
_g('I', ["01110","00100","00100","00100","00100","00100","01110"])
_g('J', ["00111","00010","00010","00010","00010","10010","01100"])
_g('K', ["10001","10010","10100","11000","10100","10010","10001"])
_g('L', ["10000","10000","10000","10000","10000","10000","11111"])
_g('M', ["10001","11011","10101","10101","10001","10001","10001"])
_g('N', ["10001","11001","10101","10011","10001","10001","10001"])
_g('O', ["01110","10001","10001","10001","10001","10001","01110"])
_g('P', ["11110","10001","10001","11110","10000","10000","10000"])
_g('Q', ["01110","10001","10001","10001","10101","10010","01101"])
_g('R', ["11110","10001","10001","11110","10100","10010","10001"])
_g('S', ["01111","10000","10000","01110","00001","00001","11110"])
_g('T', ["11111","00100","00100","00100","00100","00100","00100"])
_g('U', ["10001","10001","10001","10001","10001","10001","01110"])
_g('V', ["10001","10001","10001","10001","10001","01010","00100"])
_g('W', ["10001","10001","10001","10101","10101","11011","10001"])
_g('X', ["10001","10001","01010","00100","01010","10001","10001"])
_g('Y', ["10001","10001","01010","00100","00100","00100","00100"])
_g('Z', ["11111","00001","00010","00100","01000","10000","11111"])
_g('a', ["00000","00000","01110","00001","01111","10001","01111"])
_g('b', ["10000","10000","11110","10001","10001","10001","11110"])
_g('c', ["00000","00000","01110","10000","10000","10001","01110"])
_g('d', ["00001","00001","01111","10001","10001","10001","01111"])
_g('e', ["00000","00000","01110","10001","11111","10000","01110"])
_g('f', ["00110","01001","01000","11110","01000","01000","01000"])
_g('g', ["00000","01111","10001","10001","01111","00001","01110"])
_g('h', ["10000","10000","11110","10001","10001","10001","10001"])
_g('i', ["00100","00000","01100","00100","00100","00100","01110"])
_g('j', ["00010","00000","00110","00010","00010","10010","01100"])
_g('k', ["10000","10000","10010","10100","11000","10100","10010"])
_g('l', ["01100","00100","00100","00100","00100","00100","01110"])
_g('m', ["00000","00000","11010","10101","10101","10101","10101"])
_g('n', ["00000","00000","11110","10001","10001","10001","10001"])
_g('o', ["00000","00000","01110","10001","10001","10001","01110"])
_g('p', ["00000","00000","11110","10001","10001","11110","10000"])
_g('q', ["00000","00000","01111","10001","10001","01111","00001"])
_g('r', ["00000","00000","10110","11001","10000","10000","10000"])
_g('s', ["00000","00000","01111","10000","01110","00001","11110"])
_g('t', ["01000","01000","11100","01000","01000","01000","00110"])
_g('u', ["00000","00000","10001","10001","10001","10011","01101"])
_g('v', ["00000","00000","10001","10001","10001","01010","00100"])
_g('w', ["00000","00000","10001","10101","10101","10101","01010"])
_g('x', ["00000","00000","10001","01010","00100","01010","10001"])
_g('y', ["00000","00000","10001","10001","01111","00001","01110"])
_g('z', ["00000","00000","11111","00010","00100","01000","11111"])
_g('0', ["01110","10001","10011","10101","11001","10001","01110"])
_g('1', ["00100","01100","00100","00100","00100","00100","01110"])
_g('2', ["01110","10001","00001","00110","01000","10000","11111"])
_g('3', ["11111","00010","00100","00010","00001","10001","01110"])
_g('4', ["00010","00110","01010","10010","11111","00010","00010"])
_g('5', ["11111","10000","11110","00001","00001","10001","01110"])
_g('6', ["00110","01000","10000","11110","10001","10001","01110"])
_g('7', ["11111","00001","00010","00100","01000","01000","01000"])
_g('8', ["01110","10001","10001","01110","10001","10001","01110"])
_g('9', ["01110","10001","10001","01111","00001","00010","01100"])
_g(' ', ["00000","00000","00000","00000","00000","00000","00000"])
_g('.', ["00000","00000","00000","00000","00000","01100","01100"])
_g(',', ["00000","00000","00000","00000","01100","00100","01000"])
_g(':', ["00000","01100","01100","00000","01100","01100","00000"])
_g(';', ["00000","01100","01100","00000","01100","00100","01000"])
_g('!', ["00100","00100","00100","00100","00100","00000","00100"])
_g('?', ["01110","10001","00001","00110","00100","00000","00100"])
_g('-', ["00000","00000","00000","01110","00000","00000","00000"])
_g('/', ["00001","00010","00010","00100","01000","01000","10000"])
_g('(', ["00010","00100","01000","01000","01000","00100","00010"])
_g(')', ["01000","00100","00010","00010","00010","00100","01000"])
_g('%', ["11001","11010","00010","00100","01000","01011","10011"])
_g('+', ["00000","00100","00100","11111","00100","00100","00000"])
_g('=', ["00000","00000","11111","00000","11111","00000","00000"])
_g('&', ["01100","10010","10100","01000","10101","10010","01101"])
_g("'", ["00100","00100","01000","00000","00000","00000","00000"])
_g('"', ["01010","01010","00000","00000","00000","00000","00000"])
_g('$', ["00100","01111","10100","01110","00101","11110","00100"])
_g('*', ["00000","00100","10101","01110","10101","00100","00000"])
_g('#', ["01010","01010","11111","01010","11111","01010","01010"])
_g('@', ["01110","10001","10111","10101","10110","10000","01110"])
_g('_', ["00000","00000","00000","00000","00000","00000","11111"])
_g('[', ["01110","01000","01000","01000","01000","01000","01110"])
_g(']', ["01110","00010","00010","00010","00010","00010","01110"])
_g('~', ["00000","00000","01001","10110","00000","00000","00000"])
_g('x', ["00000","00000","10001","01010","00100","01010","10001"])
_g('>', ["01000","00100","00010","00001","00010","00100","01000"])
_g('<', ["00010","00100","01000","10000","01000","00100","00010"])
_g('^', ["00100","01010","10001","00000","00000","00000","00000"])
# unicode mapped to ascii glyphs
F['\u2019'] = F["'"]
F['\u2018'] = F["'"]
F['\u201c'] = F['"']
F['\u201d'] = F['"']
F['\u2013'] = F['-']
F['\u2014'] = [0b00000,0b00000,0b00000,0b11111,0b00000,0b00000,0b00000]
F['\u00b7'] = [0b00000,0b00000,0b00000,0b01100,0b01100,0b00000,0b00000]
F['\u2022'] = [0b00000,0b01110,0b11111,0b11111,0b01110,0b00000,0b00000]
F['\u00d7'] = [0b00000,0b10001,0b01010,0b00100,0b01010,0b10001,0b00000]
F['\u2192'] = [0b00000,0b00000,0b00100,0b00010,0b11111,0b00010,0b00100]
F['\u00b0'] = [0b00100,0b01010,0b00100,0b00000,0b00000,0b00000,0b00000]
F['\u00e9'] = F['e']
F['\u00e8'] = F['e']
F['\u00fc'] = F['u']
F['\u00f6'] = F['o']
F['\u00e4'] = F['a']
F['\u00df'] = F['s']

# ---------- canvas ----------
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))
    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i+3] = bytes(c)
    def get(self, x, y):
        i = (y * self.w + x) * 3
        return tuple(self.px[i:i+3])
    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            if 0 <= yy < self.h:
                x0 = max(x, 0); x1 = min(x + w, self.w)
                if x1 > x0:
                    i = (yy * self.w + x0) * 3
                    self.px[i:(yy * self.w + x1) * 3] = bytes(c) * (x1 - x0)
    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)
    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)
    def box(self, x, y, w, h, c, t=1):
        self.hline(x, y, w, c, t); self.hline(x, y + h - t, w, c, t)
        self.vline(x, y, h, c, t); self.vline(x + w - t, y, h, c, t)
    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy
    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) <= r else 0
            self.hline(cx - dx, yy, 2 * dx + 1, c)
    def ring(self, cx, cy, r, c, t=1):
        for k in range(t):
            rr = r - k
            for a in range(0, 360):
                import math
                self.set(cx + int(rr * math.cos(math.radians(a))),
                         cy + int(rr * math.sin(math.radians(a))), c)
    def poly(self, pts, c):
        # scanline fill, pts = [(x,y),...]
        if not pts:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.hline(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), c)
    def tri(self, x0, y0, x1, y1, x2, y2, c):
        self.poly([(x0, y0), (x1, y1), (x2, y2)], c)

# ---------- text ----------
def tw(s, sc):
    return len(s) * 6 * sc - sc

def draw_text(cv, s, x, y, sc, c):
    cx = x
    for ch in s:
        g = F.get(ch, F[' '])
        for r in range(7):
            bits = g[r]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    cv.rect(cx + col * sc, y + r * sc, sc, sc, c)
        cx += 6 * sc
    return cx

def wrap(s, maxw, sc):
    words = s.split(' ')
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if tw(t, sc) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(cv, lines, x, y, sc, c, lh=None):
    lh = lh or (7 * sc + 2)
    for ln in lines:
        draw_text(cv, ln, x, y, sc, c)
        y += lh
    return y

def center_text(cv, s, cx, y, sc, c):
    draw_text(cv, s, cx - tw(s, sc) // 2, y, sc, c)

# ---------- PNG encoder ----------
def _chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)

def save_png(cv, path):
    raw = bytearray()
    w = cv.w
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * w * 3:(y + 1) * w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

# ---------- hero scenes ----------
def scene_cop31(cv, x, y, w, h):
    # dawn sky bands
    for i, c in enumerate([DAWN, (238, 170, 100), DAWN2, (248, 220, 160), (250, 236, 200)]):
        cv.rect(x, y + i * h // 5, w, h // 5 + 1, c)
    # sun disc + glow
    cv.disc(x + w - 52, y + 30, 20, (255, 240, 180))
    cv.disc(x + w - 52, y + 30, 14, (255, 214, 110))
    # skyline silhouettes
    base = y + h
    for bx, bw, bh in [(0, 34, 46), (30, 26, 62), (54, 40, 40), (92, 24, 70), (114, 36, 52),
                       (148, 28, 78), (174, 30, 44), (202, 34, 66), (234, 26, 50), (258, 30, 60),
                       (286, 34, 42)]:
        cv.rect(x + bx, base - bh, bw, bh, NAVY)
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                cv.rect(wx, wy, 3, 4, (255, 220, 130))
    # clock tower
    cv.rect(x + w - 92, base - 88, 16, 88, NAVY)
    cv.disc(x + w - 84, base - 88, 11, WHITE)
    cv.disc(x + w - 84, base - 88, 9, PAPER)
    cv.line(x + w - 84, base - 88, x + w - 84, base - 96, INK)
    cv.line(x + w - 84, base - 88, x + w - 78, base - 86, INK)
    # ground
    cv.rect(x, base - 8, w, 8, (60, 50, 40))

def scene_bahrain(cv, x, y, w, h):
    cv.rect(x, y, w, h, NIGHT)
    # moon + stars
    cv.disc(x + w - 46, y + 24, 12, MOON)
    for sx, sy in [(20, 18), (60, 30), (110, 14), (160, 26), (210, 16), (250, 34), (90, 40)]:
        cv.disc(x + sx, y + sy, 1, WHITE)
    # sea
    cv.rect(x, y + h - 34, w, 34, SEA)
    for wy in range(y + h - 30, y + h - 4, 7):
        cv.hline(x + 8, wy, w - 16, (60, 100, 150), 1)
    # ship silhouette
    bx, by = x + 40, y + h - 62
    cv.rect(bx, by, 180, 26, (8, 12, 22))
    cv.rect(bx + 20, by - 18, 50, 18, (8, 12, 22))
    cv.rect(bx + 80, by - 12, 60, 12, (30, 40, 60))
    cv.rect(bx + 150, by - 24, 8, 24, (8, 12, 22))
    for wx in range(bx + 8, bx + 172, 14):
        cv.rect(wx, by + 6, 5, 5, (255, 200, 90))
    # flames
    for fx, fh in [(bx + 30, 22), (bx + 60, 30), (bx + 95, 18), (bx + 130, 26), (bx + 160, 20)]:
        cv.tri(fx, by, fx + 7, by - fh, fx + 14, by, FIRE)
        cv.tri(fx + 3, by, fx + 7, by - fh + 8, fx + 11, by, FIRE2)
    # smoke
    for sx, sy, sr in [(bx + 40, by - 34, 8), (bx + 70, by - 44, 10), (bx + 105, by - 36, 7), (bx + 140, by - 46, 9)]:
        cv.disc(sx, sy, sr, (120, 120, 125))

def scene_kyiv(cv, x, y, w, h):
    cv.rect(x, y, w, h, NIGHT)
    cv.disc(x + w - 50, y + 26, 13, MOON)
    for sx, sy in [(16, 20), (48, 12), (90, 26), (130, 14), (180, 30), (230, 18), (270, 28), (70, 36)]:
        cv.disc(x + sx, y + sy, 1, WHITE)
    # drone dots with dotted trails
    for dx, dy in [(60, 40), (120, 30), (180, 46), (240, 34), (290, 44), (90, 55), (210, 58)]:
        cv.disc(x + dx, y + dy, 2, FIRE2)
        for k in range(1, 5):
            cv.set(x + dx - k * 6, y + dy + k, (200, 160, 60))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 40, 40), (38, 30, 58), (66, 44, 34), (108, 26, 66), (132, 36, 46),
                       (166, 28, 72), (192, 34, 40), (224, 30, 56), (252, 32, 44), (282, 38, 62)]:
        cv.rect(x + bx, base - bh, bw, bh, (6, 10, 26))
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                cv.rect(wx, wy, 3, 4, (255, 210, 110))
    # fires on the ground
    for fx in [x + 50, x + 150, x + 250]:
        cv.tri(fx, base - 4, fx + 5, base - 16, fx + 10, base - 4, FIRE)
    cv.rect(x, base - 6, w, 6, (8, 10, 20))

# ---------- card pictograms (drawn in a small box) ----------
def pic_vote(cv, x, y, w, h):
    cv.rect(x + w // 2 - 16, y + h - 22, 32, 20, RED)
    cv.rect(x + w // 2 - 20, y + h - 26, 40, 5, RED2)
    cv.rect(x + w // 2 - 4, y + 4, 8, 4, INK)
    cv.line(x + w // 2 - 12, y + 16, x + w // 2 - 4, y + 26, WHITE)
    cv.line(x + w // 2 - 4, y + 26, x + w // 2 + 14, y + 6, WHITE)

def pic_race(cv, x, y, w, h):
    cy = y + h - 18
    cv.rect(x + 8, cy - 8, 52, 8, RED)
    cv.rect(x + 20, cy - 16, 26, 9, RED)
    cv.rect(x + 46, cy - 13, 12, 3, INK)
    cv.disc(x + 18, cy + 2, 5, INK); cv.disc(x + 18, cy + 2, 2, LGREY)
    cv.disc(x + 50, cy + 2, 5, INK); cv.disc(x + 50, cy + 2, 2, LGREY)
    cv.line(x + 8, cy + 8, x + 62, cy + 8, INK)

def pic_cricket(cv, x, y, w, h):
    cv.rect(x + 30, y + 6, 6, 26, BROWN)
    cv.rect(x + 28, y + 30, 10, 14, BROWN)
    cv.disc(x + 52, y + 16, 6, RED)
    cv.disc(x + 52, y + 16, 3, WHITE)
    cv.line(x + 10, y + h - 6, x + 60, y + h - 6, GREEN)

def pic_boat(cv, x, y, w, h):
    cv.tri(x + 12, y + 22, x + 58, y + 22, x + 50, y + 34, BROWN)
    cv.rect(x + 30, y + 6, 3, 16, INK)
    cv.tri(x + 33, y + 6, x + 33, y + 20, x + 48, y + 20, WHITE)
    for wy in (y + 38, y + 44):
        cv.hline(x + 6, wy, w - 12, LBLUE, 2)

def pic_bolt(cv, x, y, w, h):
    cv.poly([(x + 38, y + 2), (x + 18, y + 26), (x + 30, y + 26), (x + 24, y + 46),
             (x + 46, y + 20), (x + 34, y + 20)], FIRE2)

def pic_star(cv, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 - 2
    pts = []
    import math
    for i in range(10):
        r = 16 if i % 2 == 0 else 7
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
    cv.poly(pts, GOLD)
    cv.disc(cx, cy, 3, RED)

def pic_truck(cv, x, y, w, h):
    cv.rect(x + 8, y + 14, 34, 18, WHITE)
    cv.box(x + 8, y + 14, 34, 18, INK)
    cv.rect(x + 42, y + 20, 14, 12, RED)
    cv.disc(x + 18, y + 34, 5, INK); cv.disc(x + 48, y + 34, 5, INK)
    cv.disc(x + 25, y + 20, 4, RED)

def pic_planet(cv, x, y, w, h):
    cv.disc(x + w // 2, y + h // 2, 13, LBLUE)
    cv.disc(x + w // 2 - 4, y + h // 2 - 4, 4, (180, 210, 230))
    cv.line(x + 6, y + h // 2 + 8, x + w - 6, y + h // 2 - 8, GOLD)
    cv.line(x + 6, y + h // 2 + 11, x + w - 6, y + h // 2 - 5, GOLD)

def pic_probe(cv, x, y, w, h):
    cv.ring(x + 24, y + 18, 11, INK, 3)
    cv.line(x + 32, y + 26, x + 44, y + 38, INK)
    cv.line(x + 44, y + 40, x + 58, y + 24, RED)
    cv.line(x + 58, y + 24, x + 62, y + 30, RED)
    cv.line(x + 44, y + 40, x + 52, y + 40, RED)

def pic_hosp(cv, x, y, w, h):
    cv.rect(x + w // 2 - 5, y + 4, 10, 34, RED)
    cv.rect(x + w // 2 - 16, y + 14, 32, 10, RED)
    cv.line(x + 8, y + h - 4, x + w - 8, y + h - 4, GREY)

PICS = {'vote': pic_vote, 'race': pic_race, 'cricket': pic_cricket, 'boat': pic_boat,
        'bolt': pic_bolt, 'star': pic_star, 'truck': pic_truck, 'planet': pic_planet,
        'probe': pic_probe, 'hosp': pic_hosp}

# ---------- world map ----------
NA = [(-168,66),(-158,58),(-152,60),(-140,60),(-135,57),(-130,54),(-125,49),(-124,42),
      (-120,34),(-114,29),(-110,24),(-105,20),(-97,16),(-92,15),(-86,12),(-83,9),
      (-79,9),(-81,13),(-84,16),(-87,21),(-90,21),(-91,19),(-97,26),(-93,30),
      (-89,30),(-84,30),(-81,25),(-80,32),(-76,35),(-74,40),(-70,42),(-68,44),
      (-65,44),(-60,47),(-55,47),(-60,50),(-65,50),(-68,55),(-72,58),(-78,62),
      (-85,66),(-92,66),(-95,69),(-110,68),(-125,70),(-140,70),(-155,71),(-165,68)]
GL = [(-58,64),(-52,60),(-43,60),(-40,64),(-32,68),(-25,70),(-20,74),(-25,76),
      (-35,77),(-50,76),(-58,74),(-60,70)]
SA = [(-79,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),
      (-72,-37),(-73,-44),(-74,-50),(-70,-54),(-66,-55),(-68,-50),(-65,-45),
      (-62,-41),(-58,-38),(-52,-33),(-48,-28),(-41,-23),(-39,-17),(-35,-9),
      (-35,-6),(-40,-3),(-44,-2),(-50,0),(-53,4),(-58,6),(-62,9),(-68,11),
      (-72,12),(-76,10)]
AF = [(-6,35),(-10,31),(-15,27),(-17,21),(-17,15),(-15,11),(-12,8),(-8,5),
      (-4,5),(0,6),(6,4),(9,4),(9,-1),(12,-5),(13,-10),(12,-17),(15,-23),
      (17,-29),(19,-34),(26,-34),(32,-28),(35,-24),(36,-18),(40,-15),(40,-10),
      (42,-4),(46,-1),(51,2),(51,11),(48,11),(44,11),(43,12),(40,15),(38,18),
      (37,22),(35,28),(33,31),(30,31),(25,32),(20,32),(15,32),(10,34),(11,37),
      (6,37),(0,36)]
EU = [(-10,36),(-9,38),(-9,43),(-2,44),(-2,48),(-4,48),(-1,49),(0,51),(2,51),
      (4,53),(8,54),(8,57),(10,58),(6,58),(5,60),(10,62),(13,65),(18,69),
      (25,71),(32,70),(40,68),(45,68),(52,68),(60,69),(68,70),(75,72),(85,73),
      (95,74),(105,76),(115,73),(125,72),(135,72),(145,72),(155,70),(162,66),
      (170,66),(178,65),(178,62),(170,60),(162,60),(158,56),(156,51),(150,59),
      (142,59),(141,52),(140,46),(135,43),(130,42),(127,40),(126,38),(122,38),
      (120,32),(122,28),(118,25),(110,21),(108,18),(105,10),(103,8),(100,8),
      (98,10),(94,16),(92,21),(89,22),(86,20),(83,17),(80,13),(77,8),(75,11),
      (72,20),(70,23),(66,25),(62,25),(58,26),(56,27),(54,26),(51,28),(50,29),
      (48,30),(44,29),(42,27),(39,21),(38,20),(36,21),(35,28),(34,31),(36,36),
      (33,36),(30,36),(27,37),(23,36),(22,37),(20,39),(19,42),(16,40),(14,42),
      (12,44),(8,44),(6,43),(3,43),(0,40),(-2,37),(-6,36)]
AU = [(113,-22),(114,-30),(115,-35),(118,-35),(124,-33),(129,-32),(132,-32),
      (135,-35),(138,-35),(140,-38),(145,-38),(147,-39),(150,-37),(153,-32),
      (153,-27),(150,-23),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),
      (132,-12),(130,-13),(126,-14),(122,-17),(118,-20)]

def draw_map(cv, mx, my, mw, mh, pins):
    cv.rect(mx, my, mw, mh, NAVY)
    def proj(lon, lat):
        px = mx + (lon + 180.0) / 360.0 * mw
        py = my + (85.0 - max(-60.0, min(85.0, lat))) / 145.0 * mh
        return int(px), int(py)
    for cont in (NA, GL, SA, AF, EU, AU):
        cv.poly([proj(lon, lat) for lon, lat in cont], (232, 222, 198))
    offs = {1: (-16, -12), 3: (0, -14), 10: (12, 12), 2: (14, 12), 8: (14, -12)}
    for num, (lon, lat) in pins.items():
        px, py = proj(lon, lat)
        ox, oy = offs.get(num, (0, 0))
        tx, ty = px + ox, py + oy
        if (ox, oy) != (0, 0):
            cv.line(px, py, tx, ty, WHITE)
            cv.disc(px, py, 2, WHITE)
        cv.disc(tx, ty, 8, RED)
        cv.ring(tx, ty, 8, WHITE, 1)
        s = str(num)
        draw_text(cv, s, tx - tw(s, 1) // 2, ty - 3, 1, WHITE)

# ---------- story data ----------
TAGC = {'CONFIRMED': GREEN, 'REPORTED': NAVY2, 'CLAIM': RED}
REGC = {'EUROPE': NAVY2, 'MIDDLE EAST': RED, 'ASIA-PAC': TEAL, 'AMERICAS': GREEN,
        'AFRICA': BROWN, 'OCEANIA': LBLUE, 'WORLD': (90, 90, 90)}

HEROES = [
 dict(num=1, region='WORLD', loc='ANTALYA, TURKIYE', tag='REPORTED', scene=scene_cop31,
      head="COP31's final text lands at dawn — with no mention of fossil fuels",
      deck="Ten-page package drops the $120bn target, keeps a 35% electricity goal for 2035, and admits 1.5°C will be overshot. Objections close 03:00 GMT.",
      src="BBC · Reuters · Guardian", pin=(30.7, 36.9)),
 dict(num=2, region='MIDDLE EAST', loc='MANAMA, BAHRAIN', tag='CLAIM', scene=scene_bahrain,
      head="Iran claims strikes on US bases in Bahrain",
      deck="IRGC says it hit two Patriot radars at al-Riffa and Awali Sakir; Bahrain says defences intercepted the attack and only a civilian site burned. No casualties.",
      src="Al Jazeera · Reuters · IRGC statement", pin=(50.6, 26.2)),
 dict(num=3, region='EUROPE', loc='KYIV, UKRAINE', tag='REPORTED', scene=scene_kyiv,
      head="Russia's overnight barrage: 186 drones, 161 downed",
      deck="Moscow fires 186 drones and three ballistic missiles at Ukraine overnight; air defences shoot down or jam 161. Strikes recorded at 18 sites.",
      src="Ukrainian Air Force · Kyiv Independent", pin=(30.5, 50.5)),
]

CARDS = [
 dict(num=4, region='ASIA-PAC', pic='vote', tag='CONFIRMED',
      head="Hong Kong elects its Election Committee",
      deck="856 candidates for 723 seats; turnout 93.55% by 14:00.", src="SCMP", pin=(114.2, 22.3)),
 dict(num=5, region='AMERICAS', pic='race', tag='CONFIRMED',
      head="Verstappen wins the Las Vegas GP",
      deck="Beats Norris and Piastri; Russell hits the wall, finishes 9th.", src="Reuters · F1", pin=(-115.1, 36.2)),
 dict(num=6, region='OCEANIA', pic='cricket', tag='CONFIRMED',
      head="India declare 720/9 — a record in NZ",
      deck="Pant 128, Rahul 136; highest total ever in New Zealand.", src="Reuters · AP", pin=(174.8, -41.3)),
 dict(num=7, region='AFRICA', pic='boat', tag='REPORTED',
      head="Bayelsa boat toll rises to 26",
      deck="Mourners' boat capsized Friday; recovery goes on.", src="RIA · Vanguard", pin=(6.3, 4.9)),
 dict(num=8, region='MIDDLE EAST', pic='bolt', tag='REPORTED',
      head="Iran starts rationing electricity",
      deck="Two-hour daily cuts begin as gas output falls.", src="Tavani · RFE/RL", pin=(51.4, 35.7)),
 dict(num=9, region='AMERICAS', pic='star', tag='CONFIRMED',
      head="'El Chapo Isidro' caught in Sinaloa",
      deck="FBI top-ten fugitive held after a shoot-out; 11 dead.", src="Sky News · BBC", pin=(-108.5, 25.6)),
 dict(num=10, region='MIDDLE EAST', pic='truck', tag='REPORTED',
      head="Hamas seeks urgent talks after aid strike",
      deck="Three die in a drone strike on a food vehicle in Gaza City.", src="Al Jazeera · Anadolu", pin=(34.5, 31.5)),
 dict(num=11, region='WORLD', pic='planet', tag='REPORTED',
      head="BepiColombo enters Mercury orbit",
      deck="Eight-year journey ends; telescope takes first readings.", src="AP · ESA", pin=None),
 dict(num=12, region='AMERICAS', pic='probe', tag='CONFIRMED',
      head="Nvidia faces an SEC probe",
      deck="Accounting inquiry at an early stage as AI shares slide.", src="Straits Times · CNBC", pin=(-77.0, 38.9)),
 dict(num=13, region='AMERICAS', pic='hosp', tag='CONFIRMED',
      head="Bolsonaro in intensive care",
      deck="Bowel obstruction, stable, breathing on his own.", src="Al Jazeera · Reuters", pin=(-47.9, -15.8)),
]

ALSO = [
 (14, "Kryvyi Rih missile: 2 killed, 58 hurt — BBC"),
 (15, "Russian cargo ship Sparta II ablaze; all 16 crew off; Finland blames Ukraine — Reuters"),
 (16, "Saudi downs Houthi missile aimed at Riyadh; intercepted 01:42 local — Anadolu"),
 (17, "EU and Indonesia sign trade deal after ten years — DW"),
 (18, "Germany's coalition talks grind on"),
 (19, "England hammer New Zealand 37-12 at Twickenham — Reuters"),
 (20, "Premier League: Leeds 4-1 Chelsea; Arsenal 2-2 Newcastle"),
 (21, "Sanchez faces TV debate before Spain votes 29 Nov"),
 (22, "Lebanon: Aoun demands Israel withdrawal — Al Jazeera"),
 (23, "Israel: Eisenkot invites Likud to coalition talks — Straits Times"),
 (24, "West Bank killing probed"),
 (25, "Cikande factory fire: 3 dead, 36 missing — Reuters"),
 (26, "Pakistan FM hopes for US-Iran deal"),
 (27, "Japan Tobacco books $8.9bn Russia loss"),
 (28, "Manipur toxic-liquor toll rises to 19; 600+ in hospital"),
 (29, "St Johns River breaks flood record; crest expected Sunday — Forecasters"),
 (30, "Trump holds press conference, fresh off China trip"),
 (31, "Bedard has shoulder surgery; MacKinnon out 12 weeks"),
 (32, "Peru quake toll rises to 1 dead, 16 hurt — 170 homes in Junin (quake was 20 Nov)"),
 (33, "Sudan: army seizes Bau district in Blue Nile"),
 (34, "Congo: leaders meet in Oyo on Sunday"),
 (35, "UNICEF: 1,144 children killed or hurt in Ukraine in 2026"),
]

NUMBERS = [("~200", "NATIONS AT THE COP31 TALKS"), ("03:00", "GMT OBJECTIONS DEADLINE"),
           ("186", "DRONES FIRED OVERNIGHT"), ("2", "US BASES HIT IN BAHRAIN"),
           ("856", "HONG KONG CANDIDATES"), ("720/9", "INDIA'S RECORD TOTAL IN NZ")]
REGIONS = [("EUROPE", 7), ("MIDDLE EAST", 7), ("ASIA-PAC", 5), ("AMERICAS", 8),
           ("AFRICA", 3), ("OCEANIA", 1), ("WORLD", 4)]
UTC = [("03:00", "COP31 objections close"),
       ("05:30", "Las Vegas GP ends"), ("06:00", "COP31 approval session"),
       ("08:00", "161 of 186 drones downed"), ("14:00", "HK turnout 93.55%")]

PINS = {}
for h in HEROES:
    if h['pin']:
        PINS[h['num']] = h['pin']
for c in CARDS:
    if c['pin']:
        PINS[c['num']] = c['pin']

# ---------- render ----------
def render():
    cv = Canvas(W, H, PAPER)
    MX = 14
    CW = 996
    # top rule + kicker
    cv.hline(0, 4, W, RED, 2)
    cv.rect(0, 8, W, 22, NAVY)
    draw_text(cv, "THE WORLD IN ONE DAY", 14, 13, 2, GOLD)
    rk = "35 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    draw_text(cv, rk, W - 14 - tw(rk, 1), 15, 1, WHITE)
    # masthead
    center_text(cv, "Sunday 22 November 2026", W // 2, 34, 6, INK)
    cv.hline(MX, 86, CW, INK, 2)
    # deck
    deck = "COP31's final text lands at dawn · Iran claims strikes on US bases in Bahrain · 186 drones over Ukraine overnight"
    draw_lines(cv, wrap(deck, CW, 2), MX, 92, 2, RED2, 16)
    # numbers strip
    y0 = 128
    cv.hline(MX, y0, CW, INK, 1)
    cw = CW // 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = MX + i * cw
        if i:
            cv.vline(x, y0 + 4, 36, LGREY, 1)
        center_text(cv, num, x + cw // 2, y0 + 4, 4, RED if i in (1, 2, 4) else INK)
        for j, ln in enumerate(wrap(lab, cw - 8, 1)):
            center_text(cv, ln, x + cw // 2, y0 + 32 + j * 8, 1, GREY)
    cv.hline(MX, y0 + 44, CW, INK, 1)
    # region bar
    y0 = 176
    seg = CW // 7
    for i, (name, n) in enumerate(REGIONS):
        x = MX + i * seg
        cv.rect(x, y0, seg - 1, 20, REGC[name] if name in REGC else GREY)
        center_text(cv, "%s %d" % (name, n), x + seg // 2, y0 + 7, 1, WHITE)
    # UTC strip
    y0 = 200
    draw_text(cv, "THE DAY IN UTC", MX, y0 + 3, 1, RED)
    ux = MX + tw("THE DAY IN UTC", 1) + 12
    parts = []
    for t, s in UTC:
        parts.append("%s %s" % (t, s))
    ut = "  ·  ".join(parts)
    draw_text(cv, ut, ux, y0 + 3, 1, INK)
    cv.hline(MX, y0 + 14, CW, INK, 1)
    # heroes
    hx, hw, hy = MX, 326, 216
    for i, h in enumerate(HEROES):
        x = hx + i * (hw + 9)
        h['scene'](cv, x, hy, hw, 106)
        cv.box(x, hy, hw, 106, INK, 1)
        # number chip + location + tag
        ty = hy + 110
        cv.rect(x, ty, 18, 12, RED)
        draw_text(cv, str(h['num']), x + 9 - tw(str(h['num']), 1) // 2, ty + 3, 1, WHITE)
        draw_text(cv, h['loc'], x + 22, ty + 3, 1, INK)
        tag = h['tag']
        tx = x + hw - tw(tag, 1) - 4
        cv.rect(tx - 3, ty, tw(tag, 1) + 6, 12, TAGC[tag])
        draw_text(cv, tag, tx, ty + 3, 1, WHITE)
        draw_lines(cv, wrap(h['head'], hw, 2), x, ty + 16, 2, INK, 15)
        draw_lines(cv, wrap(h['deck'], hw, 1), x, ty + 62, 1, INK, 9)
        draw_text(cv, "Sources: " + h['src'], x, ty + 92, 1, GREY)
        cv.hline(x, ty + 104, hw, LGREY, 1)
    # THE DAY IN TEN header
    draw_text(cv, "THE DAY IN TEN", MX, 442, 2, INK)
    draw_text(cv, "THE STORIES THAT MOVED THE WORLD TODAY", W - 14 - tw("THE STORIES THAT MOVED THE WORLD TODAY", 1), 447, 1, GREY)
    # cards 2 rows x 5
    cw5 = (CW - 4 * 8) // 5
    for r in range(2):
        for c in range(5):
            cd = CARDS[r * 5 + c]
            x = MX + c * (cw5 + 8)
            y = 460 + r * 96
            cv.rect(x, y, cw5, 10, REGC[cd['region']])
            draw_text(cv, cd['region'], x + 3, y + 2, 1, WHITE)
            draw_text(cv, str(cd['num']), x + cw5 - tw(str(cd['num']), 1) - 4, y + 2, 1, WHITE)
            PICS[cd['pic']](cv, x + cw5 // 2 - 34, y + 12, 68, 34)
            draw_lines(cv, wrap(cd['head'], cw5 - 4, 1), x + 2, y + 48, 1, INK, 9)
            draw_lines(cv, wrap(cd['deck'], cw5 - 4, 1), x + 2, y + 66, 1, GREY, 8)
            cv.rect(x, y + 84, 16, 9, TAGC[cd['tag']])
            draw_text(cv, cd['tag'], x + 18, y + 84, 1, TAGC[cd['tag']])
            draw_text(cv, cd['src'], x + 18 + tw(cd['tag'], 1) + 6, y + 84, 1, GREY)
            cv.box(x, y, cw5, 94, LGREY, 1)
    # map + ALSO
    my0 = 654
    draw_text(cv, "WHERE IT HAPPENED — PINS MATCH STORY NUMBERS", MX, my0, 1, INK)
    draw_map(cv, MX, my0 + 12, 316, 200, PINS)
    cv.box(MX, my0 + 12, 316, 200, INK, 1)
    draw_text(cv, "11 BepiColombo is at Mercury — no pin on Earth.", MX, my0 + 218, 1, GREY)
    ax = 340
    draw_text(cv, "ALSO ON SUNDAY 22 NOVEMBER — 22 MORE STORIES", ax, my0, 2, RED)
    colw = 330
    for i, (num, txt) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        x = ax + col * (colw + 10)
        y = my0 + 22 + row * 20
        draw_text(cv, "%d" % num, x, y, 1, RED)
        draw_lines(cv, wrap(txt, colw - 22, 1), x + 20, y, 1, INK, 9)
    # DATE CHECK
    dy = 906
    cv.box(MX, dy, CW, 54, RED, 2)
    draw_text(cv, "DATE CHECK — READ THIS FIRST", MX + 8, dy + 5, 1, RED)
    dc = ("WIRES READ UP TO 08:00 UTC. Sunday 22 November 2026: every story here was reported, or still developing, "
          "on 22 November in at least one time zone. Left out on purpose: the Peru quake (Fri 20 Nov), Russia's "
          "400-drone barrage (19-20 Nov) and the Shenzhen summit (19 Nov). Tonight's barrage was 186, not 400.")
    draw_lines(cv, wrap(dc, CW - 16, 1), MX + 8, dy + 17, 1, INK, 9)
    ny = "NOT YET: COP31 adoption vote (plenary due 11:00 Antalya) · Spain votes 29 Nov · G20 peace talks ahead · Killer-robot rules by 2028."
    draw_text(cv, ny, MX + 8, dy + 42, 1, GREY)
    # legend
    draw_text(cv, "HOW TO READ THE TAGS — CONFIRMED = reported by the named source · REPORTED = wire-reported, not yet confirmed · CLAIM = one side's account, contested.", MX, 968, 1, INK)
    # footer
    draw_text(cv, "SCENES ARE DRAWN ILLUSTRATIONS, NOT PHOTOGRAPHS. SOURCES: BBC · REUTERS · AL JAZEERA · THE GUARDIAN · AP · SCMP · DW · UPI · FT · UKRAINIAN AIR FORCE · ESA", MX, 984, 1, GREY)
    draw_text(cv, "THE WORLD IN ONE DAY · SUNDAY 22 NOVEMBER 2026 · ONE PAGE", MX, 996, 1, GREY)
    return cv

# ---------- main ----------
def main():
    import os
    cv = render()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "entry.png")
    except OSError:
        path = "entry.png"
    save_png(cv, path)
    print("wrote", path, os.path.getsize(path), "bytes")

if __name__ == "__main__":
    main()
