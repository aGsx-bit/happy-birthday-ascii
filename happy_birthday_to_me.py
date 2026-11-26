import math as m
import time

import numpy as np

__author__ = "Mahamad (aGsx / @aGsx-bit)"
__copyright__ = "Copyright (c) 2026 Mahamad (aGsx / @aGsx-bit)"

SIZE = 8
FPS = 30
SS = 1
ASPECT = 1.102
MAXROWS = 74
CW_GLYPH = 6
CH_GLYPH = 10

T_RAIN0 = 0.05
T_RAIN_END = 3.90
T_CANDLE0 = 4.25
T_CONFETTI0 = 7.50
T_TEXT0 = 7.75
T_TEXT_END = 10.50
T_FINAL = 11.20

RAMP_SHADER = " .:-=+*oae0O8@#"
NR = len(RAMP_SHADER) - 1
EXTRA_CHARS = "/\\|~^_()$&%,<>.'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_ALL_CHARS = RAMP_SHADER + "".join(ch for ch in dict.fromkeys(EXTRA_CHARS) if ch not in RAMP_SHADER)
RAMP = _ALL_CHARS
CIDX = {c: i for i, c in enumerate(RAMP)}
QL = 24

_FONT5X9 = {
    " ": (0, 0, 0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0, 4, 4, 0),
    ",": (0, 0, 0, 0, 0, 0, 4, 4, 8),
    ":": (0, 0, 4, 4, 0, 0, 4, 4, 0),
    "-": (0, 0, 0, 0, 14, 0, 0, 0, 0),
    "=": (0, 0, 0, 14, 0, 14, 0, 0, 0),
    "+": (0, 0, 4, 4, 31, 4, 4, 0, 0),
    "*": (0, 0, 21, 14, 31, 14, 21, 0, 0),
    "~": (0, 0, 0, 10, 21, 0, 0, 0, 0),
    "^": (0, 4, 10, 17, 0, 0, 0, 0, 0),
    "_": (0, 0, 0, 0, 0, 0, 0, 0, 31),
    "|": (4, 4, 4, 4, 4, 4, 4, 4, 4),
    "/": (0, 1, 2, 2, 4, 8, 8, 16, 0),
    "\\": (0, 16, 8, 8, 4, 2, 2, 1, 0),
    "(": (2, 4, 8, 8, 8, 8, 8, 4, 2),
    ")": (8, 4, 2, 2, 2, 2, 2, 4, 8),
    "<": (0, 2, 4, 8, 16, 8, 4, 2, 0),
    ">": (0, 8, 4, 2, 1, 2, 4, 8, 0),
    "'": (4, 4, 8, 0, 0, 0, 0, 0, 0),
    "o": (0, 0, 0, 14, 17, 17, 17, 14, 0),
    "a": (0, 0, 0, 14, 1, 15, 17, 15, 0),
    "e": (0, 0, 0, 14, 17, 31, 16, 14, 0),
    "0": (0, 14, 17, 19, 21, 25, 17, 14, 0),
    "O": (0, 14, 17, 17, 17, 17, 17, 14, 0),
    "8": (0, 14, 17, 17, 14, 17, 17, 14, 0),
    "@": (0, 14, 17, 23, 21, 23, 16, 14, 0),
    "#": (0, 10, 10, 31, 10, 31, 10, 10, 0),
    "$": (4, 15, 20, 14, 5, 5, 30, 4, 0),
    "%": (0, 25, 26, 2, 4, 8, 11, 19, 0),
    "&": (0, 12, 18, 18, 12, 21, 18, 13, 0),
    "1": (0, 4, 12, 4, 4, 4, 4, 14, 0),
    "2": (0, 14, 17, 1, 6, 8, 16, 31, 0),
    "3": (0, 14, 17, 1, 6, 1, 17, 14, 0),
    "4": (0, 2, 6, 10, 18, 31, 2, 2, 0),
    "5": (0, 31, 16, 30, 1, 1, 17, 14, 0),
    "6": (0, 6, 8, 16, 30, 17, 17, 14, 0),
    "7": (0, 31, 1, 2, 4, 8, 8, 8, 0),
    "9": (0, 14, 17, 17, 15, 1, 2, 12, 0),
    "A": (0, 14, 17, 17, 31, 17, 17, 17, 0),
    "B": (0, 30, 17, 17, 30, 17, 17, 30, 0),
    "C": (0, 14, 17, 16, 16, 16, 17, 14, 0),
    "D": (0, 28, 18, 17, 17, 17, 18, 28, 0),
    "E": (0, 31, 16, 16, 30, 16, 16, 31, 0),
    "F": (0, 31, 16, 16, 30, 16, 16, 16, 0),
    "G": (0, 14, 17, 16, 23, 17, 17, 14, 0),
    "H": (0, 17, 17, 17, 31, 17, 17, 17, 0),
    "I": (0, 14, 4, 4, 4, 4, 4, 14, 0),
    "J": (0, 7, 2, 2, 2, 18, 18, 12, 0),
    "K": (0, 17, 18, 20, 24, 20, 18, 17, 0),
    "L": (0, 16, 16, 16, 16, 16, 16, 31, 0),
    "M": (0, 17, 27, 21, 21, 17, 17, 17, 0),
    "N": (0, 17, 25, 21, 19, 17, 17, 17, 0),
    "P": (0, 30, 17, 17, 30, 16, 16, 16, 0),
    "Q": (0, 14, 17, 17, 17, 21, 18, 13, 0),
    "R": (0, 30, 17, 17, 30, 20, 18, 17, 0),
    "S": (0, 14, 17, 16, 14, 1, 17, 14, 0),
    "T": (0, 31, 4, 4, 4, 4, 4, 4, 0),
    "U": (0, 17, 17, 17, 17, 17, 17, 14, 0),
    "V": (0, 17, 17, 17, 17, 10, 10, 4, 0),
    "W": (0, 17, 17, 17, 21, 21, 27, 17, 0),
    "X": (0, 17, 17, 10, 4, 10, 17, 17, 0),
    "Y": (0, 17, 17, 10, 4, 4, 4, 4, 0),
    "Z": (0, 31, 1, 2, 4, 8, 16, 31, 0),
    "b": (0, 16, 16, 30, 17, 17, 17, 30, 0),
    "c": (0, 0, 0, 14, 17, 16, 17, 14, 0),
    "d": (0, 1, 1, 15, 17, 17, 17, 15, 0),
    "f": (0, 6, 9, 8, 28, 8, 8, 8, 0),
    "g": (0, 0, 0, 15, 17, 15, 1, 14, 0),
    "h": (0, 16, 16, 30, 17, 17, 17, 17, 0),
    "i": (0, 4, 0, 12, 4, 4, 4, 14, 0),
    "j": (0, 2, 0, 6, 2, 2, 18, 12, 0),
    "k": (0, 16, 16, 18, 20, 24, 20, 18, 0),
    "l": (0, 12, 4, 4, 4, 4, 4, 14, 0),
    "m": (0, 0, 0, 26, 21, 21, 21, 21, 0),
    "n": (0, 0, 0, 30, 17, 17, 17, 17, 0),
    "p": (0, 0, 0, 30, 17, 30, 16, 16, 0),
    "q": (0, 0, 0, 15, 17, 15, 1, 1, 0),
    "r": (0, 0, 0, 22, 25, 16, 16, 16, 0),
    "s": (0, 0, 0, 14, 16, 14, 1, 30, 0),
    "t": (0, 8, 8, 28, 8, 8, 9, 6, 0),
    "u": (0, 0, 0, 17, 17, 17, 17, 15, 0),
    "v": (0, 0, 0, 17, 17, 17, 10, 4, 0),
    "w": (0, 0, 0, 17, 17, 21, 21, 10, 0),
    "x": (0, 0, 0, 17, 10, 4, 10, 17, 0),
    "y": (0, 0, 0, 17, 17, 15, 1, 14, 0),
    "z": (0, 0, 0, 31, 2, 4, 8, 31, 0),
}

GLYPH_MASK = np.zeros((len(RAMP), CH_GLYPH, CW_GLYPH, 1), dtype=np.uint8)
for _i, _ch in enumerate(RAMP):
    _rows = _FONT5X9.get(_ch, _FONT5X9[" "])
    for _r in range(9):
        _bits = _rows[_r]
        for _c in range(5):
            if (_bits >> (4 - _c)) & 1:
                GLYPH_MASK[_i, _r, _c, 0] = 1
GLYPH_BG = ((1 - GLYPH_MASK) * np.array([4, 4, 6], dtype=np.uint8)).astype(np.uint8)

_BLOCK_LETTERS = {
    "H": (
        "/--\\  /--\\",
        "|##|  |##|",
        "|##|__|##|",
        "|########|",
        "|##|--|##|",
        "|##|  |##|",
        "|##|  |##|",
        "\\__/  \\__/",
    ),
    "A": (
        "   /--\\   ",
        "  /####\\  ",
        " /##/\\##\\ ",
        "|##|__|##|",
        "|########|",
        "|##|--|##|",
        "|##|  |##|",
        "\\__/  \\__/",
    ),
    "P": (
        "/------\\  ",
        "|##--\\##\\ ",
        "|##|  |##|",
        "|##|__/##/",
        "|#######/ ",
        "|##|      ",
        "|##|      ",
        "\\__/      ",
    ),
    "Y": (
        "/--\\  /--\\",
        "\\##\\  /##/",
        " \\##\\/##/ ",
        "  \\####/  ",
        "   |##|   ",
        "   |##|   ",
        "   |##|   ",
        "   \\__/   ",
    ),
    "B": (
        "/------\\  ",
        "|##--\\##\\ ",
        "|##|__|#/ ",
        "|#######\\ ",
        "|##|--\\##\\",
        "|##|  |##|",
        "|##|__/##/",
        "\\_______/ ",
    ),
    "I": (
        "/--\\",
        "|##|",
        "|##|",
        "|##|",
        "|##|",
        "|##|",
        "|##|",
        "\\__/",
    ),
    "R": (
        "/------\\  ",
        "|##--\\##\\ ",
        "|##|  |##|",
        "|##|__/##/",
        "|#######\\ ",
        "|##|\\###\\ ",
        "|##| \\###\\",
        "\\__/  \\__/",
    ),
    "T": (
        "/--------\\",
        "|########|",
        "\\__\\##/__/",
        "   |##|   ",
        "   |##|   ",
        "   |##|   ",
        "   |##|   ",
        "   \\__/   ",
    ),
    "D": (
        "/------\\  ",
        "|##--\\##\\ ",
        "|##|  \\##\\",
        "|##|  |##|",
        "|##|  |##|",
        "|##|  /##/",
        "|##|_/##/ ",
        "\\______/  ",
    ),
    "M": (
        "/--\\   /--\\",
        "|###\\ /###|",
        "|##\\###/##|",
        "|##|\\#/|##|",
        "|##|   |##|",
        "|##|   |##|",
        "|##|   |##|",
        "\\__/   \\__/",
    ),
    "O": (
        " /------\\ ",
        "/########\\",
        "|##/--\\##|",
        "|##|  |##|",
        "|##|  |##|",
        "|##\\__/##|",
        "\\########/",
        " \\______/ ",
    ),
    "E": (
        "/--------\\",
        "|########|",
        "|##\\_____/",
        "|#######\\ ",
        "|##/----/ ",
        "|##/-----\\",
        "|########|",
        "\\________/",
    ),
    " ": (
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
        "    ",
    ),
}

TAU = 2.0 * m.pi
R_CAKE = 1.92
TOP_H = 0.96
A0, A1 = -0.44, 0.44
SLICE_CENTER = np.array([1.02, 0.0, 0.0], dtype=np.float32)
CANDLE_POS = np.array([1.02, 0.0, 0.0], dtype=np.float32)

MAT_CRUST = 0
MAT_SPONGE = 1
MAT_CREAM = 2
MAT_FROST = 3
MAT_CANDLE = 4
MAT_RED = 5
MAT_PLATE = 6
MAT_GOLD = 7
MAT_SPRINKLE = 8
MAT_FLAME = 9
MAT_CORE = 10

MAT_COLORS = np.array([
    [0.52, 0.31, 0.15],
    [0.84, 0.59, 0.30],
    [0.99, 0.94, 0.85],
    [0.95, 0.91, 0.84],
    [0.97, 0.95, 0.92],
    [0.94, 0.22, 0.30],
    [0.56, 0.60, 0.66],
    [0.92, 0.71, 0.30],
    [0.24, 0.84, 1.00],
    [1.00, 0.58, 0.16],
    [1.00, 0.98, 0.86],
], dtype=np.float32)

SPRINKLE_PAL = np.array([
    [0.22, 0.85, 1.00],
    [1.00, 0.36, 0.66],
    [0.42, 0.92, 0.45],
    [1.00, 0.82, 0.28],
    [1.00, 0.48, 0.26],
], dtype=np.float32)

CONFETTI_PAL = np.array([
    [0.24, 0.85, 1.00],
    [1.00, 0.38, 0.68],
    [1.00, 0.82, 0.30],
    [0.42, 0.94, 0.50],
    [1.00, 0.45, 0.32],
    [0.64, 0.68, 1.00],
], dtype=np.float32)

S = {"last": 0.0}


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    u = 1.0 - t
    return 1.0 - u * u * u


def ring_vec(a):
    return np.stack([np.cos(a), np.zeros_like(a), np.sin(a)], axis=-1).astype(np.float32)


def frosting_y(x, z):
    a = np.arctan2(z, x)
    r = np.hypot(x, z)
    return TOP_H + 0.024 * np.sin(5.0 * a) + 0.014 * np.cos(7.5 * r)


def build_cake_cloud():
    rng = np.random.default_rng(27)
    pts, norms, mats, sp_col = [], [], [], []

    def add(p, n, mat_id, sc=None):
        pts.append(p.astype(np.float32))
        norms.append(n.astype(np.float32))
        mats.append(np.full(len(p), mat_id, dtype=np.int32))
        if sc is None:
            sp_col.append(np.full(len(p), -1, dtype=np.int32))
        else:
            sp_col.append(sc.astype(np.int32))

    for a_wall, side in ((A0, +1.0), (A1, -1.0)):
        nw = 4800
        rw = rng.uniform(0.0, R_CAKE, nw)
        yw = rng.uniform(0.025, TOP_H + 0.02, nw)
        rv_w = np.array([m.cos(a_wall), 0.0, m.sin(a_wall)], dtype=np.float32)
        pw = rw[:, None] * rv_w[None, :]
        pw[:, 1] = yw
        fy_w = frosting_y(pw[:, 0], pw[:, 2])
        is_fr = yw >= fy_w - 0.060
        is_cr = (yw < 0.085) | (rw > R_CAKE - 0.032)
        is_cm = ((yw > 0.34) & (yw < 0.42)) | ((yw > 0.54) & (yw < 0.62))
        mat = np.where(is_fr, MAT_FROST, np.where(is_cm, MAT_CREAM, np.where(is_cr, MAT_CRUST, MAT_SPONGE)))
        nv = np.tile(np.array([-side * m.sin(a_wall), 0.0, side * m.cos(a_wall)], dtype=np.float32), (nw, 1))
        for mid in (MAT_CRUST, MAT_SPONGE, MAT_CREAM, MAT_FROST):
            sel = mat == mid
            if sel.any():
                add(pw[sel], nv[sel], mid)

    no = 4800
    ao = rng.uniform(A0, A1, no)
    yo = rng.uniform(0.025, TOP_H + 0.03, no)
    rvo = ring_vec(ao)
    drip_o = TOP_H * 0.52 + 0.13 * np.sin(ao * 10.0) + 0.055 * np.cos(ao * 17.0)
    is_fo = yo >= drip_o
    rad_o = R_CAKE + np.where(is_fo, 0.024 + 0.010 * np.sin(ao * 20.0), 0.0)
    po = rad_o[:, None] * rvo
    po[:, 1] = yo
    is_cro = (yo < 0.085) & (~is_fo)
    is_cmo = (((yo > 0.34) & (yo < 0.42)) | ((yo > 0.54) & (yo < 0.62))) & (~is_fo)
    for mid, sel in (
        (MAT_FROST, is_fo),
        (MAT_CREAM, is_cmo),
        (MAT_CRUST, is_cro),
        (MAT_SPONGE, (~is_fo) & (~is_cmo) & (~is_cro)),
    ):
        if sel.any():
            add(po[sel], rvo[sel], mid)

    nt = 6000
    rt = R_CAKE * np.sqrt(rng.uniform(0.0, 1.0, nt))
    at = rng.uniform(A0, A1, nt)
    pt = rt[:, None] * ring_vec(at)
    pt[:, 1] = frosting_y(pt[:, 0], pt[:, 2])
    eps = 0.01
    nx = -(frosting_y(pt[:, 0] + eps, pt[:, 2]) - pt[:, 1]) / eps
    nz = -(frosting_y(pt[:, 0], pt[:, 2] + eps) - pt[:, 1]) / eps
    nv = np.stack([nx, np.ones(nt, dtype=np.float32), nz], axis=-1)
    nv /= np.linalg.norm(nv, axis=-1, keepdims=True)
    add(pt, nv, MAT_FROST)

    base_y = float(frosting_y(np.array([CANDLE_POS[0]]), np.array([CANDLE_POS[2]]))[0]) - 0.03
    nc = 1800
    ac = rng.uniform(0.0, TAU, nc)
    yc = rng.uniform(0.0, 0.64, nc)
    rad = ring_vec(ac)
    pc = CANDLE_POS[None, :] + 0.056 * rad
    pc[:, 1] = base_y + yc
    is_red = np.sin(ac + yc * 16.0) > 0.22
    add(pc[~is_red], rad[~is_red], MAT_CANDLE)
    add(pc[is_red], rad[is_red], MAT_RED)
    w_y = np.linspace(0.0, 0.055, 22)
    wp = CANDLE_POS[None, :] + np.stack([np.zeros_like(w_y), base_y + 0.64 + w_y, np.zeros_like(w_y)], axis=-1).astype(np.float32)
    add(wp, np.tile(np.array([0.0, 1.0, 0.0], dtype=np.float32), (len(w_y), 1)), MAT_CRUST)

    np_d = 2100
    ap = rng.uniform(0.0, TAU, np_d)
    up = np.sqrt(rng.uniform(0.0, 1.0, np_d))
    rim_d = 1.22 + 0.055 * np.sin(ap * 12.0)
    rp = up * rim_d
    pp = SLICE_CENTER[None, :] + np.stack([rp * np.cos(ap), -0.04 + 0.042 * (up ** 4), rp * np.sin(ap)], axis=-1).astype(np.float32)
    ny = np.tile(np.array([0.0, 1.0, 0.0], dtype=np.float32), (np_d, 1))
    is_gold = up > 0.90
    add(pp[~is_gold], ny[~is_gold], MAT_PLATE)
    add(pp[is_gold], ny[is_gold], MAT_GOLD)

    ar = rng.uniform(0.0, TAU, 2000)
    yr = rng.uniform(-0.08, 0.012, 2000)
    rim_r = 1.22 + 0.055 * np.sin(ar * 12.0)
    add(
        SLICE_CENTER[None, :] + np.stack([rim_r * np.cos(ar), yr, rim_r * np.sin(ar)], axis=-1).astype(np.float32),
        ring_vec(ar),
        MAT_GOLD,
    )

    for i in range(36):
        col_i = i % len(SPRINKLE_PAL)
        rs = rng.uniform(0.24, R_CAKE - 0.12)
        as_ = rng.uniform(A0 + 0.07, A1 - 0.07)
        c = np.array([rs * m.cos(as_), 0.0, rs * m.sin(as_)], dtype=np.float32)
        if np.hypot(c[0] - CANDLE_POS[0], c[2] - CANDLE_POS[2]) < 0.16:
            continue
        c[1] = float(frosting_y(np.array([c[0]]), np.array([c[2]]))[0]) + 0.025
        d = rng.normal(size=3).astype(np.float32) * np.array([1.0, 0.12, 1.0], dtype=np.float32)
        d /= np.linalg.norm(d) + 1e-6
        s = np.linspace(-0.020, 0.020, 3)[:, None]
        add(c[None, :] + s * d[None, :], np.tile(np.array([0.0, 1.0, 0.0], dtype=np.float32), (3, 1)), MAT_SPRINKLE, np.full(3, col_i))

    P = np.concatenate(pts, axis=0)
    N = np.concatenate(norms, axis=0)
    M = np.concatenate(mats, axis=0)
    SC = np.concatenate(sp_col, axis=0)
    order = np.clip((P[:, 1] + 0.12) / 1.78 + rng.uniform(-0.04, 0.08, len(P)), 0.0, 1.0).astype(np.float32)
    fly = np.stack([
        rng.normal(0.0, 0.36, len(P)),
        rng.uniform(0.85, 2.05, len(P)),
        rng.normal(0.0, 0.36, len(P)),
    ], axis=-1).astype(np.float32)
    spin = rng.uniform(-1.8, 1.8, len(P)).astype(np.float32)
    grain = rng.uniform(-0.14, 0.14, len(P)).astype(np.float32)
    wick_top = np.array([CANDLE_POS[0], base_y + 0.695, CANDLE_POS[2]], dtype=np.float32)
    return P, N, M, SC, order, fly, spin, grain, wick_top


CAKE_P, CAKE_N, CAKE_M, CAKE_SC, CAKE_ORD, CAKE_FLY, CAKE_SPIN, CAKE_GRAIN, WICK_TOP = build_cake_cloud()

_FLAME_RNG = np.random.default_rng(7)
_FLAME_U = _FLAME_RNG.uniform(-1.0, 1.0, 900).astype(np.float32)
_FLAME_V = _FLAME_RNG.uniform(0.0, 1.0, 900).astype(np.float32)
_FLAME_Z = _FLAME_RNG.uniform(-0.015, 0.015, 900).astype(np.float32)
_FLAME_J = _FLAME_RNG.integers(0, 6, 900)
_FLAME_CORE = (np.abs(_FLAME_U) < 0.58) & (_FLAME_V > 0.08) & (_FLAME_V < 0.65)
_CORE_GLYPHS = np.array([CIDX[c] for c in ("#", "0", "8", "B", "$", "Q")], dtype=np.int32)
_OUT_GLYPHS = np.array([CIDX[c] for c in ("o", "a", "0", "&", "e", "Q")], dtype=np.int32)

_STAR_RNG = np.random.default_rng(11)
NSTARS = 55
STX = _STAR_RNG.uniform(0.02, 0.98, NSTARS).astype(np.float32)
STY = _STAR_RNG.uniform(0.03, 0.92, NSTARS).astype(np.float32)
STP = _STAR_RNG.uniform(0.0, TAU, NSTARS).astype(np.float32)

_CONF_RNG = np.random.default_rng(2727)
NCONF = 110
CONF_X0 = _CONF_RNG.uniform(0.02, 0.98, NCONF).astype(np.float32)
CONF_Y0 = _CONF_RNG.uniform(0.0, 1.0, NCONF).astype(np.float32)
CONF_SPD = _CONF_RNG.uniform(0.085, 0.195, NCONF).astype(np.float32)
CONF_SWAY = _CONF_RNG.uniform(0.008, 0.028, NCONF).astype(np.float32)
CONF_FRQ = _CONF_RNG.uniform(1.4, 3.6, NCONF).astype(np.float32)
CONF_PH = _CONF_RNG.uniform(0.0, TAU, NCONF).astype(np.float32)
CONF_COL_I = _CONF_RNG.integers(0, len(CONFETTI_PAL), NCONF)
CONF_DELAY = _CONF_RNG.uniform(0.0, 1.8, NCONF).astype(np.float32)


def _build_word_cells(word, top_row, center_col, spacing, palette_rgb, start_delay=0.0, letter_step=0.17):
    widths = [len(_BLOCK_LETTERS[ch][0]) for ch in word]
    total_w = sum(widths) + (len(word) - 1) * spacing
    lx = center_col - total_w // 2
    rng = np.random.default_rng(len(word) * 31 + top_row)
    cells = []
    shades = ("8", "B", "$", "%", "0", "Q", "&", "#")
    for li, ch in enumerate(word):
        pat = _BLOCK_LETTERS[ch]
        w_ch = len(pat[0])
        h_ch = len(pat)
        for rr in range(h_ch):
            row_s = pat[rr]
            for cc in range(w_ch):
                g = row_s[cc]
                if g == " ":
                    continue
                if g == "#":
                    glyph = shades[int(rng.integers(0, len(shades)))]
                    br = 0.96 + 0.08 * (1.0 - rr / max(1, h_ch - 1))
                else:
                    glyph = g
                    br = 0.72
                delay = start_delay + li * letter_step + cc * 0.014 + rng.uniform(0.0, 0.025)
                cells.append((top_row + rr, lx + cc, glyph, palette_rgb * br, delay, g == "#"))
        lx += w_ch + spacing
    return cells


def init(cw, ch, rows):
    global CW, CH, ROWS, COLS, W, H, PPM_HDR, Q_TO_U8
    global HAPPY_CELLS, BDAY_CELLS, ALL_TEXT_CELLS, STAR_R, STAR_C
    global TEXT_R, TEXT_C, TEXT_CH, TEXT_RGB, TEXT_DELAY, TEXT_FILL, TEXT_PHASE
    CW = CW_GLYPH
    CH = CH_GLYPH
    ROWS = MAXROWS
    COLS = 136
    W, H = COLS * CW, ROWS * CH
    PPM_HDR = f"P6\n{W} {H}\n255\n".encode("ascii")
    Q_TO_U8 = np.array([v * 255 // (QL - 1) for v in range(QL)], dtype=np.uint8)

    STAR_R = np.clip((STY * ROWS).astype(np.int32), 1, ROWS - 2)
    STAR_C = np.clip((STX * COLS).astype(np.int32), 1, COLS - 2)

    gold = np.array([0.98, 0.79, 0.36], dtype=np.float32)
    rose = np.array([0.95, 0.56, 0.72], dtype=np.float32)
    purple = np.array([0.74, 0.42, 0.98], dtype=np.float32)
    HAPPY_CELLS = _build_word_cells("HAPPY", top_row=1, center_col=COLS // 2, spacing=1, palette_rgb=gold, start_delay=0.0, letter_step=0.18)
    BDAY_CELLS = _build_word_cells("BIRTHDAY", top_row=10, center_col=COLS // 2, spacing=1, palette_rgb=rose, start_delay=0.72, letter_step=0.14)
    NAME_CELLS = _build_word_cells("TO ME", top_row=19, center_col=COLS // 2, spacing=1, palette_rgb=purple, start_delay=1.75, letter_step=0.17)
    ALL_TEXT_CELLS = [c for c in (HAPPY_CELLS + BDAY_CELLS + NAME_CELLS) if 0 <= c[0] < ROWS and 0 <= c[1] < COLS]
    TEXT_R = np.array([c[0] for c in ALL_TEXT_CELLS], dtype=np.int32)
    TEXT_C = np.array([c[1] for c in ALL_TEXT_CELLS], dtype=np.int32)
    TEXT_CH = np.array([CIDX[c[2]] for c in ALL_TEXT_CELLS], dtype=np.int32)
    TEXT_RGB = np.array([c[3] for c in ALL_TEXT_CELLS], dtype=np.float32)
    TEXT_DELAY = np.array([c[4] for c in ALL_TEXT_CELLS], dtype=np.float32)
    TEXT_FILL = np.array([c[5] for c in ALL_TEXT_CELLS], dtype=bool)
    TEXT_PHASE = (TEXT_C * 0.38 + TEXT_R * 0.65).astype(np.float32)
    reset()


def reset():
    S["last"] = 0.0


def flicker(t):
    return 0.84 + 0.09 * m.sin(t * 13.0) + 0.05 * m.sin(t * 29.0) + 0.02 * m.cos(t * 43.0)


def project_points(pts, t):
    yaw = 1.18 + 0.35 * m.sin(t * 0.38)
    pitch = 0.30 + 0.02 * m.cos(t * 0.30)
    cy, sy = m.cos(yaw), m.sin(yaw)
    cp, sp = m.cos(pitch), m.sin(pitch)

    x = pts[:, 0] - SLICE_CENTER[0]
    y = pts[:, 1] - 0.55
    z = pts[:, 2] - SLICE_CENTER[2]
    rx = x * cy - z * sy
    rz = x * sy + z * cy
    ry = y * cp + rz * sp
    tz = -y * sp + rz * cp + 5.35

    fov = 2.90
    inv_z = fov / np.maximum(tz, 0.4)
    col = ((0.50 + rx * inv_z * 0.33 * H / float(W)) * COLS).astype(np.int32)
    row = ((0.70 - ry * inv_z * 0.33) * ROWS).astype(np.int32)
    return row, col, tz, yaw, pitch


def _draw_hud_str(idx, fg, r, c, text, col_rgb):
    if r < 0 or r >= ROWS:
        return
    for i, ch in enumerate(text):
        cc = c + i
        if 0 <= cc < COLS and ch != " " and ch in CIDX:
            idx[r, cc] = CIDX[ch]
            fg[r, cc] = col_rgb


def render_cells(t, dt):
    S["last"] = t
    idx = np.zeros((ROWS, COLS), dtype=np.int32)
    fg = np.zeros((ROWS, COLS, 3), dtype=np.float32)
    zbuf = np.full((ROWS, COLS), 1e9, dtype=np.float32)

    twk = 0.25 + 0.40 * (np.sin(t * 2.1 + STP * 4.0) ** 2)
    idx[STAR_R, STAR_C] = CIDX["."]
    fg[STAR_R, STAR_C] = np.array([0.45, 0.50, 0.62], dtype=np.float32)[None, :] * twk[:, None]

    u_rain = np.clip((t - T_RAIN0 - CAKE_ORD * 2.45) / 0.85, 0.0, 1.0)
    k_rain = u_rain * u_rain * (3.0 - 2.0 * u_rain)
    inv_k = 1.0 - k_rain
    ang = CAKE_SPIN * inv_k
    ca, sa = np.cos(ang), np.sin(ang)
    fx = CAKE_FLY[:, 0] * inv_k
    fz = CAKE_FLY[:, 2] * inv_k
    p_cur = CAKE_P.copy()
    p_cur[:, 0] += fx * ca - fz * sa
    p_cur[:, 1] += CAKE_FLY[:, 1] * inv_k * inv_k
    p_cur[:, 2] += fx * sa + fz * ca

    flame_grow = ease((t - T_CANDLE0) / 1.15)
    flk = flicker(t) if flame_grow > 0.02 else 0.0

    row_c, col_c, depth_c, yaw_now, _ = project_points(p_cur, t)
    in_flight_vis = (k_rain > 0.80) | ((k_rain > 0.15) & ((np.arange(len(k_rain)) % 7) == 0))
    ok = (row_c >= 0) & (row_c < ROWS) & (col_c >= 0) & (col_c < COLS) & in_flight_vis

    if ok.any():
        ro, co, zo = row_c[ok], col_c[ok], depth_c[ok]
        no = CAKE_N[ok]
        mo = CAKE_M[ok]
        sco = CAKE_SC[ok]
        po = p_cur[ok]
        ko = k_rain[ok]
        go = CAKE_GRAIN[ok]

        lx, ly, lz = -0.35, 0.72, -0.58
        lnorm = m.sqrt(lx * lx + ly * ly + lz * lz)
        ndotl = np.clip((no[:, 0] * lx + no[:, 1] * ly + no[:, 2] * lz) / lnorm, 0.0, 1.0)
        d_wick = po - WICK_TOP[None, :]
        dist2 = np.sum(d_wick * d_wick, axis=-1) + 0.04
        candle_glow = np.clip(0.55 * flame_grow * flk / dist2, 0.0, 0.85) * (0.35 + 0.65 * np.maximum(0.0, no[:, 1]))
        lum = np.clip(0.24 + 0.70 * ndotl + candle_glow + go * 0.36, 0.10, 1.0) * (0.35 + 0.65 * ko)

        col_pts = MAT_COLORS[mo].copy()
        sp_mask = sco >= 0
        frost_mask = (mo == MAT_FROST) | (mo == MAT_CANDLE) | (mo == MAT_CREAM)
        lum = np.where(frost_mask, np.maximum(lum, 0.56), lum)
        lum = np.where(mo == MAT_PLATE, np.maximum(lum, 0.40), lum)
        lum = np.where(mo == MAT_GOLD, np.maximum(lum, 0.52), lum)
        if sp_mask.any():
            col_pts[sp_mask] = SPRINKLE_PAL[sco[sp_mask]]
            lum[sp_mask] = 1.0
            zo[sp_mask] -= 0.08

        warm = np.array([1.00, 0.72, 0.34], dtype=np.float32)
        col_pts = col_pts * (0.34 + 0.72 * lum[:, None]) + warm[None, :] * (candle_glow[:, None] * 0.36)

        flat_idx = ro * COLS + co
        order = np.argsort(zo)[::-1]
        zbuf_flat = zbuf.ravel()
        idx_flat = idx.ravel()
        fg_flat = fg.reshape(-1, 3)

        ci_pts = np.clip((lum * NR + 0.5).astype(np.int32), 1, NR)
        frost_g = np.where(lum > 0.62, CIDX["N"], np.where(lum > 0.44, CIDX["n"], np.where(go > 0.0, CIDX["~"], CIDX["^"])))
        sponge_g = np.where((lum > 0.62), CIDX["0"], np.where(lum > 0.45, CIDX["o"], np.where(lum > 0.28, CIDX["e"], CIDX[":"])))
        ci_pts = np.where(mo == MAT_SPONGE, sponge_g, ci_pts)
        ci_pts = np.where(mo == MAT_CRUST, np.where(lum > 0.35, CIDX["+"], CIDX["-"]), ci_pts)
        ci_pts = np.where(mo == MAT_CREAM, CIDX["="], ci_pts)
        ci_pts = np.where(mo == MAT_FROST, frost_g, ci_pts)
        ci_pts = np.where((mo == MAT_CANDLE) | (mo == MAT_RED), np.where(go > 0.02, CIDX["e"], CIDX["o"]), ci_pts)
        ci_pts = np.where(mo == MAT_PLATE, np.where(lum > 0.46, CIDX[":"], CIDX["."]), ci_pts)
        ci_pts = np.where(mo == MAT_GOLD, np.where(go > 0.0, CIDX["-"], CIDX["="]), ci_pts)
        ci_pts = np.where(sp_mask, CIDX["*"], ci_pts)

        fi_ord = flat_idx[order]
        zo_ord = zo[order]
        ci_ord = ci_pts[order]
        col_ord = np.clip(col_pts[order], 0.0, 1.0)
        mat_ord = mo[order]

        mat_map = np.full(ROWS * COLS, -1, dtype=np.int32)
        zbuf_flat[fi_ord] = zo_ord
        idx_flat[fi_ord] = ci_ord
        fg_flat[fi_ord] = col_ord
        mat_map[fi_ord] = mat_ord
        mat_2d = mat_map.reshape(ROWS, COLS)

        if t >= 3.2:
            occ = (mat_2d >= 0) & (mat_2d != MAT_PLATE) & (mat_2d != MAT_GOLD) & (mat_2d != MAT_SPRINKLE)
            occ[:2, :] = False
            occ[-4:, :] = False
            up_e = occ & (~np.roll(occ, 1, axis=0))
            dn_e = occ & (~np.roll(occ, -1, axis=0))
            lf_e = occ & (~np.roll(occ, 1, axis=1))
            rt_e = occ & (~np.roll(occ, -1, axis=1))
            idx[up_e & (~lf_e) & (~rt_e)] = CIDX["^"]
            idx[dn_e & (~lf_e) & (~rt_e)] = CIDX["-"]
            idx[lf_e & (~up_e) & (~dn_e)] = CIDX["|"]
            idx[rt_e & (~up_e) & (~dn_e)] = CIDX["|"]
            idx[(up_e & lf_e) | (dn_e & rt_e)] = CIDX["/"]
            idx[(up_e & rt_e) | (dn_e & lf_e)] = CIDX["\\"]

    if flame_grow > 0.02:
        w = 0.160 * np.sin(m.pi * (_FLAME_V ** 0.60)) * (1.0 - 0.24 * _FLAME_V) * flame_grow
        lean = 0.036 * m.sin(t * 2.4) + 0.014 * m.sin(t * 7.2)
        hgt = 0.62 * flk * flame_grow
        lat = _FLAME_U * w + lean * (_FLAME_V ** 1.6)
        cy_f, sy_f = m.cos(yaw_now), m.sin(yaw_now)
        pf = np.stack([
            WICK_TOP[0] + lat * cy_f + _FLAME_Z * sy_f,
            WICK_TOP[1] + (_FLAME_V - 0.08) * hgt,
            WICK_TOP[2] - lat * sy_f + _FLAME_Z * cy_f,
        ], axis=-1).astype(np.float32)
        rf, cf, zf, _, _ = project_points(pf, t)
        ok_f = (rf >= 0) & (rf < ROWS) & (cf >= 0) & (cf < COLS)
        if ok_f.any():
            rc_mid = int(np.median(rf[ok_f]))
            cc_mid = int(np.median(cf[ok_f]))
            for dr in range(-6, 7):
                for dc in range(-9, 10):
                    rr, cc = rc_mid + dr, cc_mid + dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS and idx[rr, cc] == 0:
                        d_a = m.hypot(dr * 1.25, dc)
                        if 1.3 < d_a < 8.4:
                            fall = m.exp(-d_a * 0.34) * flame_grow * flk
                            if fall > 0.045:
                                idx[rr, cc] = CIDX["."] if fall < 0.26 else CIDX[":"]
                                fg[rr, cc] = np.array([1.0, 0.62, 0.16], dtype=np.float32) * min(0.95, fall * 2.8)

            rfo, cfo, zfo = rf[ok_f], cf[ok_f], zf[ok_f].copy()
            core_o = _FLAME_CORE[ok_f]
            vo = _FLAME_V[ok_f]
            uo = _FLAME_U[ok_f]
            jo = _FLAME_J[ok_f]
            zfo = np.where(core_o, zfo - 0.12, zfo)
            edge_ch = np.where(
                vo < 0.22,
                np.where(uo < 0.0, CIDX["\\"], CIDX["/"]),
                np.where(vo < 0.56, CIDX["|"], np.where(uo < 0.0, CIDX["/"], CIDX["\\"])),
            )
            shell_ch = np.where(np.abs(uo) > 0.72, edge_ch, _OUT_GLYPHS[jo])
            tip_ch = np.where(uo < -0.25, CIDX["/"], np.where(uo > 0.25, CIDX["\\"], CIDX["|"]))
            c_idx = np.where(core_o, _CORE_GLYPHS[jo], np.where(vo < 0.80, shell_ch, tip_ch))
            c_rgb = np.where(
                core_o[:, None],
                MAT_COLORS[MAT_CORE][None, :] * (0.98 + 0.12 * flk),
                np.where(
                    (vo < 0.72)[:, None],
                    MAT_COLORS[MAT_FLAME][None, :] * (0.96 + 0.16 * flk),
                    np.array([[1.00, 0.44, 0.10]], dtype=np.float32) * (0.92 + 0.18 * flk),
                ),
            )
            order_f = np.argsort(zfo)[::-1]
            for k in order_f:
                rr, cc = int(rfo[k]), int(cfo[k])
                if zfo[k] <= zbuf[rr, cc] + 0.15:
                    zbuf[rr, cc] = zfo[k]
                    idx[rr, cc] = int(c_idx[k])
                    fg[rr, cc] = np.clip(c_rgb[k], 0.0, 1.0)

    if t >= T_TEXT0:
        dt_v = t - T_TEXT0 - TEXT_DELAY
        vis = dt_v > 0.0
        if vis.any():
            dt_on = dt_v[vis]
            u_raw = np.clip(dt_on / 0.16, 0.0, 1.0)
            inv_u = 1.0 - u_raw
            u_v = 1.0 - inv_u * inv_u * inv_u
            fl_mask = dt_on < 0.09
            star_mask = (dt_on < 0.045) & TEXT_FILL[vis]
            ch_out = np.where(star_mask, CIDX["*"], TEXT_CH[vis])
            spark = 0.85 + 0.15 * np.sin(t * 4.2 + TEXT_PHASE[vis]) * (0.5 + 0.5 * flk)
            col_set = TEXT_RGB[vis] * ((0.45 + 0.55 * u_v) * spark)[:, None]
            flash_rgb = np.array([1.0, 0.98, 0.88], dtype=np.float32)
            col_fl = TEXT_RGB[vis] * 0.40 + flash_rgb[None, :] * (0.65 * np.clip(1.0 - dt_on / 0.09, 0.0, 1.0))[:, None]
            col_out = np.clip(np.where(fl_mask[:, None], col_fl, col_set), 0.0, 1.0)
            rr_v, cc_v = TEXT_R[vis], TEXT_C[vis]
            idx[rr_v, cc_v] = ch_out
            fg[rr_v, cc_v] = col_out

        if t >= T_TEXT0 + 0.85:
            sp_k = 0.5 + 0.5 * m.sin(t * 4.8)
            if sp_k > 0.55:
                glint = np.array([1.0, 0.96, 0.82], dtype=np.float32) * sp_k
                gx = COLS // 2 + 13
                idx[1, gx] = CIDX["*"]
                fg[1, gx] = glint
                if sp_k > 0.72:
                    idx[0, gx] = CIDX["|"]
                    fg[0, gx] = glint * 0.70
                    idx[0, gx - 2] = CIDX["\\"]
                    fg[0, gx - 2] = glint * 0.55
                    idx[0, gx + 2] = CIDX["/"]
                    fg[0, gx + 2] = glint * 0.55

        if t >= T_TEXT0 + 2.55:
            sp_p = 0.5 + 0.5 * m.cos(t * 4.4)
            if sp_p > 0.55:
                p_glint = np.array([0.85, 0.58, 1.00], dtype=np.float32) * sp_p
                px = COLS // 2 - 20
                idx[19, px] = CIDX["*"]
                fg[19, px] = p_glint
                if sp_p > 0.74:
                    idx[18, px] = CIDX["|"]
                    fg[18, px] = p_glint * 0.72
                    idx[18, px - 1] = CIDX["\\"]
                    fg[18, px - 1] = p_glint * 0.55
                    idx[18, px + 1] = CIDX["/"]
                    fg[18, px + 1] = p_glint * 0.55

    conf_count = 0
    if t >= T_CONFETTI0:
        dt_c = t - T_CONFETTI0
        conf_glyphs = ("|", "/", "-", "\\", "o", "*")
        for i in range(NCONF):
            tc_age = dt_c - CONF_DELAY[i]
            if tc_age <= 0.0:
                continue
            conf_count += 1
            yy = (CONF_Y0[i] + tc_age * CONF_SPD[i]) % 1.02
            xx = (CONF_X0[i] + CONF_SWAY[i] * m.sin(tc_age * CONF_FRQ[i] + CONF_PH[i])) % 1.0
            rr = int(yy * (ROWS - 4))
            cc = int(xx * COLS)
            if 0 <= rr < ROWS - 3 and 0 <= cc < COLS and idx[rr, cc] == 0:
                gch = conf_glyphs[int((tc_age * 7.5 + i) % len(conf_glyphs))]
                idx[rr, cc] = CIDX[gch]
                fg[rr, cc] = CONFETTI_PAL[CONF_COL_I[i]]

    hud_dim = np.array([0.48, 0.50, 0.56], dtype=np.float32)
    hud_red = np.array([0.92, 0.30, 0.35], dtype=np.float32)
    hud_gold = np.array([0.85, 0.72, 0.42], dtype=np.float32)
    _draw_hud_str(idx, fg, 1, COLS - 12, ".", hud_red)
    _draw_hud_str(idx, fg, 1, COLS - 10, f"t {t:05.2f}s", hud_dim)
    _draw_hud_str(idx, fg, ROWS - 3, 2, "aGsx - Nov 27, 2026  |  Mahamad", hud_gold)
    c_state = "candle lit" if flame_grow > 0.25 else "candle off"
    _draw_hud_str(idx, fg, ROWS - 2, 2, f"{c_state}   flame {flk:0.2f}   confetti {conf_count:3d}", hud_dim)

    q = np.clip((np.clip(fg, 0.0, 1.0) * (QL - 0.01)).astype(np.int16), 0, QL - 1)
    return idx, q


def render_ppm_bytes(idx, q):
    fg_u8 = Q_TO_U8[q]
    rgb = (GLYPH_MASK[idx] * fg_u8[:, :, None, None, :] + GLYPH_BG[idx]).transpose(0, 2, 1, 3, 4).reshape(H, W, 3)
    return PPM_HDR + rgb.tobytes()


def main():
    import tkinter as tk

    root = tk.Tk()
    root.title("Happy Birthday To Me (Nov 27) — aGsx")
    root.resizable(False, False)
    init(CW_GLYPH, CH_GLYPH, MAXROWS)
    scr_w, scr_h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{W}x{H}+{(scr_w - W) // 2}+{max(0, (scr_h - H) // 2 - 20)}")
    cv = tk.Canvas(root, width=W, height=H, bg="#040406", highlightthickness=0)
    cv.pack()

    photo = tk.PhotoImage(width=W, height=H)
    cv.create_image(0, 0, anchor="nw", image=photo)
    st = {"t0": time.perf_counter(), "paused": False, "pause_t": 0.0, "after_id": None}

    def draw_at(t_val, dt_val=0.0):
        idx, q = render_cells(t_val, dt_val)
        photo.configure(data=render_ppm_bytes(idx, q))

    def quit_app(_=None):
        if st["after_id"] is not None:
            try:
                root.after_cancel(st["after_id"])
            except Exception:
                pass
        root.destroy()

    def restart(_=None):
        st["t0"] = time.perf_counter()
        st["pause_t"] = 0.0
        st["paused"] = False
        reset()
        draw_at(0.0, 0.0)

    def toggle_pause(_=None):
        now = time.perf_counter()
        if st["paused"]:
            st["t0"] = now - st["pause_t"]
            S["last"] = st["pause_t"]
            st["paused"] = False
        else:
            st["pause_t"] = now - st["t0"]
            st["paused"] = True

    def go_final(_=None):
        now = time.perf_counter()
        st["t0"] = now - T_FINAL
        st["pause_t"] = T_FINAL
        S["last"] = T_FINAL
        draw_at(T_FINAL, 0.0)

    root.protocol("WM_DELETE_WINDOW", quit_app)
    root.bind("<Escape>", quit_app)
    root.bind("r", restart)
    root.bind("R", restart)
    root.bind("<space>", toggle_pause)
    root.bind("a", go_final)
    root.bind("A", go_final)

    def tick():
        if st["paused"]:
            st["after_id"] = root.after(40, tick)
            return
        t0 = time.perf_counter()
        t = t0 - st["t0"]
        dt = min(max(t - S["last"], 0.0), 0.1)
        draw_at(t, dt)
        el = (time.perf_counter() - t0) * 1000
        st["after_id"] = root.after(max(1, int(1000 / FPS - el)), tick)

    st["after_id"] = root.after(50, tick)
    root.mainloop()


if __name__ == "__main__":
    main()
