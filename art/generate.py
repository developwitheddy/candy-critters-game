#!/usr/bin/env python3
"""
Printable Wall Art generator.

Produces 100 distinct, print-ready SVG posters in a 4:5 ratio (ideal for
8x10, 16x20, 18x22.5 framing). Every piece is pure vector, so it stays
crisp at any size. Run this script to regenerate everything:

    python3 art/generate.py

Outputs:
    art/prints/*.svg   – the 100 posters
    art/manifest.json  – list of every piece (file, title, category)
    index.html         – a browsable gallery (written at repo root)
"""

import json
import math
import os
import random

# ---------------------------------------------------------------------------
# Canvas (4:5 portrait — the most popular framing ratio for wall prints)
# ---------------------------------------------------------------------------
W, H = 1600, 2000
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "prints")

# ---------------------------------------------------------------------------
# Curated colour palettes. Each: (name, background, [ink colours...])
# ---------------------------------------------------------------------------
PALETTES = [
    ("Dune",        "#f3ead9", ["#d98b48", "#c25b3a", "#7a4b2b", "#e9c46a"]),
    ("Sage",        "#eef0e6", ["#6b8f71", "#3f5e4e", "#a7c4a0", "#cfa15a"]),
    ("Midnight",    "#11151c", ["#e0c879", "#5b8fb0", "#b6eada", "#f0f0f0"]),
    ("Blush",       "#fbe9e7", ["#e08a91", "#b23a48", "#7a3b69", "#f4c95d"]),
    ("Ocean",       "#e8f1f2", ["#1b6ca8", "#0a2463", "#3fa7d6", "#f4d35e"]),
    ("Terracotta",  "#f6e7d8", ["#c1502e", "#e3a857", "#5a7a6b", "#2e2a26"]),
    ("Mono Ink",    "#f7f6f2", ["#1a1a1a", "#555555", "#9a9a9a", "#1a1a1a"]),
    ("Plum",        "#efe7f1", ["#6d3b75", "#a25aa0", "#3a2e44", "#e6a4c4"]),
    ("Citrus",      "#fff7e6", ["#f08a24", "#e34a33", "#2a9d8f", "#264653"]),
    ("Slate Rose",  "#eceaf0", ["#5d6d7e", "#d98c8c", "#34495e", "#e8b04b"]),
    ("Forest",      "#e9efe6", ["#22543d", "#3a7d44", "#88b04b", "#d9a23b"]),
    ("Cobalt",      "#eaf0fb", ["#274690", "#1f8fff", "#0b1d51", "#ffb703"]),
    ("Sandstone",   "#f0e4d0", ["#9c6644", "#7f5539", "#c9a26b", "#3d2b1f"]),
    ("Mint Noir",   "#0f1c1a", ["#7fd1ae", "#39a78e", "#d6f5e3", "#f2c14e"]),
    ("Coral Reef",  "#fdeee3", ["#ff6f61", "#ffa552", "#2ec4b6", "#264653"]),
]


def palette(rng):
    return rng.choice(PALETTES)


# ---------------------------------------------------------------------------
# SVG document helpers
# ---------------------------------------------------------------------------
def doc(body, bg, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<defs>{defs}</defs>'
        f'<rect width="{W}" height="{H}" fill="{bg}"/>'
        f'{body}'
        f'</svg>'
    )


def matte(bg_ink):
    """A thin inner keyline that makes pieces look framed/gallery-ready."""
    m = 70
    return (
        f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" '
        f'fill="none" stroke="{bg_ink}" stroke-width="3" opacity="0.5"/>'
    )


def poly(points, fill, extra=""):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" {extra}/>'


def title_block(text, sub, ink):
    """Small caption strip used by several minimalist pieces."""
    return (
        f'<text x="{W/2}" y="{H-150}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="46" letter-spacing="8" '
        f'fill="{ink}">{text}</text>'
        f'<text x="{W/2}" y="{H-95}" text-anchor="middle" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="26" '
        f'letter-spacing="14" fill="{ink}" opacity="0.7">{sub}</text>'
    )


# ===========================================================================
# GENERATOR FAMILIES
# Each returns (svg_string, title, category)
# ===========================================================================

def gen_mandala(rng):
    name, bg, inks = palette(rng)
    cx, cy = W / 2, H / 2 - 40
    rings = rng.randint(5, 8)
    petals = rng.choice([10, 12, 14, 16, 18, 24])
    body = []
    for r in range(rings, 0, -1):
        rad = 90 * r
        col = inks[r % len(inks)]
        op = 0.85 if r % 2 else 0.6
        for p in range(petals):
            a = 2 * math.pi * p / petals
            x = cx + rad * math.cos(a)
            y = cy + rad * math.sin(a)
            pr = 70 + 12 * (rings - r)
            body.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pr:.1f}" '
                f'fill="none" stroke="{col}" stroke-width="3.2" opacity="{op}"/>'
            )
    body.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{inks[0]}"/>')
    body.append(matte(inks[0]))
    body.append(title_block("MANDALA", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Mandala · {name}", "Geometric"


def gen_mountains(rng):
    name, bg, inks = palette(rng)
    body = []
    # sun/moon
    sun_y = rng.randint(420, 720)
    body.append(
        f'<circle cx="{W*0.62:.0f}" cy="{sun_y}" r="220" fill="{inks[3]}" opacity="0.9"/>'
    )
    layers = rng.randint(4, 6)
    base = H - 360
    for i in range(layers):
        col = inks[i % 3]
        y0 = base - (layers - i) * 150 - rng.randint(0, 60)
        pts = [(0, H), (0, y0)]
        x = 0
        peaks = rng.randint(3, 6)
        for k in range(peaks + 1):
            x = W * k / peaks
            y = y0 + rng.randint(-180, 180)
            pts.append((x, max(200, y)))
        pts.append((W, y0))
        pts.append((W, H))
        body.append(poly(pts, col, f'opacity="{0.95 - i*0.05:.2f}"'))
    body.append(matte("#000000"))
    body.append(title_block("ALPENGLOW", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Mountain Range · {name}", "Landscape"


def gen_sunburst(rng):
    name, bg, inks = palette(rng)
    cx, cy = W / 2, H * 0.46
    rays = rng.choice([24, 30, 36, 48])
    body = []
    R = 1500
    for i in range(rays):
        a0 = 2 * math.pi * i / rays
        a1 = 2 * math.pi * (i + 0.5) / rays
        col = inks[i % 2]
        if i % 2 == 0:
            continue
        p = [
            (cx, cy),
            (cx + R * math.cos(a0), cy + R * math.sin(a0)),
            (cx + R * math.cos(a1), cy + R * math.sin(a1)),
        ]
        body.append(poly(p, col, 'opacity="0.85"'))
    for j, rad in enumerate([520, 420, 320, 210]):
        body.append(
            f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{inks[(j+2)%len(inks)]}" '
            f'opacity="{0.55 + j*0.12:.2f}"/>'
        )
    body.append(matte(inks[0]))
    body.append(title_block("HERE COMES THE SUN", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Sunburst · {name}", "Mid-Century"


def gen_arcs(rng):
    name, bg, inks = palette(rng)
    cx, cy = W / 2, H - 360
    body = []
    n = rng.randint(7, 11)
    for i in range(n, 0, -1):
        r = 130 * i
        col = inks[i % len(inks)]
        body.append(
            f'<path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy} Z" '
            f'fill="{col}" opacity="0.92"/>'
        )
    body.append(f'<rect x="0" y="{cy}" width="{W}" height="{H-cy}" fill="{bg}"/>')
    body.append(matte(inks[0]))
    body.append(title_block("RAINBOW ARC", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Concentric Arcs · {name}", "Abstract"


def gen_bauhaus(rng):
    name, bg, inks = palette(rng)
    body = []
    cols, rows = 3, 4
    cw, ch = (W - 200) / cols, (H - 360) / rows
    ox, oy = 100, 130
    for r in range(rows):
        for c in range(cols):
            x, y = ox + c * cw, oy + r * ch
            col = inks[(r + c) % len(inks)]
            shape = rng.randint(0, 4)
            if shape == 0:
                body.append(f'<circle cx="{x+cw/2:.0f}" cy="{y+ch/2:.0f}" r="{min(cw,ch)/2.4:.0f}" fill="{col}"/>')
            elif shape == 1:
                body.append(f'<rect x="{x+20:.0f}" y="{y+20:.0f}" width="{cw-40:.0f}" height="{ch-40:.0f}" fill="{col}"/>')
            elif shape == 2:
                body.append(poly([(x+cw/2, y+20), (x+cw-20, y+ch-20), (x+20, y+ch-20)], col))
            elif shape == 3:
                body.append(f'<path d="M {x+20:.0f} {y+ch-20:.0f} A {cw-40:.0f} {ch-40:.0f} 0 0 1 {x+cw-20:.0f} {y+ch-20:.0f} Z" fill="{col}"/>')
            else:
                body.append(f'<circle cx="{x+cw/2:.0f}" cy="{y+ch/2:.0f}" r="{min(cw,ch)/2.4:.0f}" fill="none" stroke="{col}" stroke-width="22"/>')
    body.append(matte(inks[0]))
    body.append(title_block("BAUHAUS", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Bauhaus Grid · {name}", "Modernist"


def gen_spirograph(rng):
    name, bg, inks = palette(rng)
    cx, cy = W / 2, H / 2 - 40
    R = rng.randint(360, 460)
    r = rng.randint(90, 200)
    d = rng.randint(120, 260)
    col = inks[rng.randint(0, len(inks) - 1)]
    pts = []
    t = 0.0
    steps = 4000
    while t < 2 * math.pi * (r // math.gcd(R, r)):
        k = (R - r) / r
        x = cx + (R - r) * math.cos(t) + d * math.cos(k * t)
        y = cy + (R - r) * math.sin(t) - d * math.sin(k * t)
        pts.append(f"{x:.1f},{y:.1f}")
        t += 2 * math.pi / 240
    path = "M " + " L ".join(pts)
    body = [
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" '
        f'stroke-width="2.4" opacity="0.9"/>'
    ]
    body.append(matte(inks[0]))
    body.append(title_block("HARMONOGRAPH", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Spirograph · {name}", "Geometric"


def gen_waves(rng):
    name, bg, inks = palette(rng)
    body = []
    rows = rng.randint(14, 20)
    amp = rng.randint(40, 90)
    for i in range(rows):
        y = 120 + i * ((H - 400) / rows)
        col = inks[i % len(inks)]
        d = [f"M 0 {y:.0f}"]
        x = 0
        ph = rng.uniform(0, 6.28)
        while x <= W:
            yy = y + amp * math.sin(x / 130 + ph) * (0.4 + 0.6 * i / rows)
            d.append(f"L {x:.0f} {yy:.1f}")
            x += 24
        body.append(f'<path d="{" ".join(d)}" fill="none" stroke="{col}" stroke-width="3" opacity="0.8"/>')
    body.append(matte(inks[0]))
    body.append(title_block("FREQUENCIES", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Sound Waves · {name}", "Abstract"


def gen_seigaiha(rng):
    name, bg, inks = palette(rng)
    body = []
    step = 110
    rad = 90
    rows = int(H / (step * 0.55)) + 2
    cols = int(W / step) + 2
    for r in range(rows):
        for c in range(cols):
            cx = c * step - (step / 2 if r % 2 else 0)
            cy = r * step * 0.55
            for k, rr in enumerate([rad, rad * 0.72, rad * 0.44, rad * 0.2]):
                col = inks[k % len(inks)]
                body.append(
                    f'<path d="M {cx-rr:.0f} {cy:.0f} A {rr:.0f} {rr:.0f} 0 0 1 {cx+rr:.0f} {cy:.0f}" '
                    f'fill="none" stroke="{col}" stroke-width="6" opacity="0.85"/>'
                )
    body.append(f'<rect width="{W}" height="{H}" fill="{bg}" opacity="0.08"/>')
    body.append(matte(inks[0]))
    return doc("".join(body), bg), f"Seigaiha Waves · {name}", "Pattern"


def gen_moonphases(rng):
    name, bg, inks = palette(rng)
    body = []
    cols, rows = 4, 5
    n = cols * rows
    cw, ch = (W - 220) / cols, (H - 420) / rows
    ox, oy = 150, 170
    moon = inks[3]
    for i in range(n):
        c, r = i % cols, i // cols
        cx = ox + c * cw + cw / 2
        cy = oy + r * ch + ch / 2
        rad = min(cw, ch) / 2.8
        phase = i / (n - 1)
        body.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.0f}" fill="{inks[0]}" opacity="0.25"/>')
        # terminator via two arcs
        k = math.cos(math.pi * phase)
        body.append(
            f'<path d="M {cx:.0f} {cy-rad:.0f} A {rad:.0f} {rad:.0f} 0 0 1 {cx:.0f} {cy+rad:.0f} '
            f'A {abs(rad*k):.0f} {rad:.0f} 0 0 {1 if k>0 else 0} {cx:.0f} {cy-rad:.0f} Z" fill="{moon}"/>'
        )
    body.append(matte(inks[0]))
    body.append(title_block("LUNAR CYCLE", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Moon Phases · {name}", "Celestial"


def gen_constellation(rng):
    name, bg, inks = palette(rng)
    bg = PALETTES[2][1]  # force dark sky
    inks = ["#f0e9d2", "#9bb7d4", "#d9c27a", "#ffffff"]
    body = []
    stars = []
    for _ in range(70):
        x, y = rng.randint(120, W - 120), rng.randint(120, H - 380)
        rr = rng.uniform(1.5, 5)
        stars.append((x, y))
        body.append(f'<circle cx="{x}" cy="{y}" r="{rr:.1f}" fill="{inks[3]}" opacity="{rng.uniform(0.5,1):.2f}"/>')
    # draw a constellation by linking some nearby stars
    chosen = rng.sample(stars, 8)
    for i in range(len(chosen) - 1):
        x1, y1 = chosen[i]
        x2, y2 = chosen[i + 1]
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{inks[1]}" stroke-width="2" opacity="0.7"/>')
    for x, y in chosen:
        body.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{inks[2]}"/>')
    body.append(matte(inks[0]))
    body.append(title_block("NORTHERN SKY", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Constellation · {name}", "Celestial"


def gen_circlepack(rng):
    name, bg, inks = palette(rng)
    body = []
    placed = []
    attempts = 0
    while len(placed) < 140 and attempts < 6000:
        attempts += 1
        x = rng.randint(120, W - 120)
        y = rng.randint(120, H - 360)
        rmax = 130
        for (px, py, pr) in placed:
            d = math.hypot(x - px, y - py) - pr
            rmax = min(rmax, d)
            if rmax < 8:
                break
        if rmax >= 10:
            rr = min(rmax - 3, 120)
            placed.append((x, y, rr))
            col = inks[len(placed) % len(inks)]
            body.append(f'<circle cx="{x}" cy="{y}" r="{rr:.0f}" fill="none" stroke="{col}" stroke-width="3.5"/>')
            if rr > 30:
                body.append(f'<circle cx="{x}" cy="{y}" r="{rr*0.5:.0f}" fill="{col}" opacity="0.25"/>')
    body.append(matte(inks[0]))
    body.append(title_block("BUBBLES", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Circle Packing · {name}", "Generative"


def gen_lowpoly(rng):
    name, bg, inks = palette(rng)
    body = []
    cols, rows = 9, 12
    cw, ch = W / cols, (H - 240) / rows
    pts = {}
    for r in range(rows + 1):
        for c in range(cols + 1):
            jx = rng.uniform(-cw * 0.3, cw * 0.3) if 0 < c < cols else 0
            jy = rng.uniform(-ch * 0.3, ch * 0.3) if 0 < r < rows else 0
            pts[(c, r)] = (c * cw + jx, 120 + r * ch + jy)
    for r in range(rows):
        for c in range(cols):
            a = pts[(c, r)]
            b = pts[(c + 1, r)]
            cc = pts[(c, r + 1)]
            d = pts[(c + 1, r + 1)]
            shade = (r / rows)
            col = inks[(c + r) % len(inks)]
            op1 = 0.55 + 0.4 * shade
            body.append(poly([a, b, cc], col, f'opacity="{op1:.2f}"'))
            body.append(poly([b, d, cc], col, f'opacity="{op1*0.8:.2f}"'))
    body.append(matte(inks[0]))
    return doc("".join(body), bg), f"Low-Poly Facets · {name}", "Generative"


def gen_albers(rng):
    name, bg, inks = palette(rng)
    body = []
    cx, cy = W / 2, H / 2 - 40
    n = rng.randint(5, 7)
    for i in range(n):
        f = (n - i) / n
        w = (W - 280) * f
        h = (H - 480) * f
        col = inks[i % len(inks)]
        body.append(f'<rect x="{cx-w/2:.0f}" y="{cy-h/2 - i*18:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{col}"/>')
    body.append(matte(inks[0]))
    body.append(title_block("HOMAGE", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Nested Squares · {name}", "Modernist"


def gen_terrazzo(rng):
    name, bg, inks = palette(rng)
    body = []
    for _ in range(260):
        x = rng.randint(90, W - 90)
        y = rng.randint(90, H - 320)
        col = rng.choice(inks)
        s = rng.uniform(8, 26)
        ang = rng.uniform(0, 360)
        verts = rng.randint(3, 6)
        p = []
        for k in range(verts):
            aa = 2 * math.pi * k / verts + rng.uniform(-0.3, 0.3)
            p.append((x + s * math.cos(aa) * rng.uniform(0.7, 1.3),
                      y + s * math.sin(aa) * rng.uniform(0.7, 1.3)))
        body.append(poly(p, col, 'opacity="0.9"'))
    body.append(matte(inks[0]))
    body.append(title_block("TERRAZZO", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Terrazzo · {name}", "Pattern"


def gen_botanical(rng):
    name, bg, inks = palette(rng)
    body = []
    stem = inks[0]
    leaf = inks[1]
    cx = W / 2
    base = H - 320
    top = 280
    body.append(f'<line x1="{cx}" y1="{base}" x2="{cx}" y2="{top}" stroke="{stem}" stroke-width="9"/>')
    n = rng.randint(7, 11)
    for i in range(n):
        t = i / (n - 1)
        y = base - t * (base - top)
        side = -1 if i % 2 else 1
        ll = 230 * (1 - 0.5 * t) + 60
        ex = cx + side * ll
        ey = y - 70
        body.append(
            f'<path d="M {cx:.0f} {y:.0f} Q {cx+side*ll*0.5:.0f} {y-90:.0f} {ex:.0f} {ey:.0f} '
            f'Q {cx+side*ll*0.4:.0f} {y-10:.0f} {cx:.0f} {y:.0f} Z" fill="{leaf}" opacity="0.92"/>'
        )
        body.append(f'<line x1="{cx:.0f}" y1="{y:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{stem}" stroke-width="2.5" opacity="0.7"/>')
    body.append(f'<circle cx="{cx:.0f}" cy="{top:.0f}" r="40" fill="{inks[3]}"/>')
    body.append(matte(inks[0]))
    body.append(title_block("BOTANICA", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Botanical Sprig · {name}", "Botanical"


def gen_quote(rng, quote, author):
    name, bg, inks = palette(rng)
    body = []
    words = quote.split()
    # wrap to ~3 words a line for big serif type
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) > 14:
            lines.append(" ".join(cur))
            cur = []
    if cur:
        lines.append(" ".join(cur))
    fs = 150 if len(lines) <= 4 else 118
    y0 = H / 2 - (len(lines) - 1) * fs * 0.6
    for i, ln in enumerate(lines):
        body.append(
            f'<text x="{W/2}" y="{y0 + i*fs*1.15:.0f}" text-anchor="middle" '
            f'font-family="Georgia, \'Times New Roman\', serif" font-weight="bold" '
            f'font-size="{fs}" fill="{inks[0]}">{ln}</text>'
        )
    body.append(f'<line x1="{W/2-120}" y1="{y0 + len(lines)*fs*1.15 + 10:.0f}" x2="{W/2+120}" y2="{y0 + len(lines)*fs*1.15 + 10:.0f}" stroke="{inks[1]}" stroke-width="5"/>')
    body.append(
        f'<text x="{W/2}" y="{y0 + len(lines)*fs*1.15 + 80:.0f}" text-anchor="middle" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="40" letter-spacing="10" '
        f'fill="{inks[1]}">{author.upper()}</text>'
    )
    body.append(matte(inks[0]))
    return doc("".join(body), bg), f"Quote · {quote[:24]}", "Typography"


def gen_opart(rng):
    name, bg, inks = palette(rng)
    col = inks[0]
    body = []
    cx, cy = W / 2, H / 2 - 40
    for i in range(120):
        r = 14 + i * 12
        warp = 40 * math.sin(i / 6)
        body.append(
            f'<circle cx="{cx + warp:.0f}" cy="{cy:.0f}" r="{r}" fill="none" '
            f'stroke="{col}" stroke-width="{4 + 3*math.sin(i/4):.1f}" opacity="0.85"/>'
        )
    body.append(matte(inks[0]))
    body.append(title_block("OPTIC", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Op-Art Rings · {name}", "Op-Art"


def gen_flowfield(rng):
    name, bg, inks = palette(rng)
    body = []

    def angle(x, y):
        return math.sin(x / 260) * math.cos(y / 320) * math.pi

    for _ in range(900):
        x = rng.uniform(80, W - 80)
        y = rng.uniform(80, H - 320)
        col = rng.choice(inks)
        d = [f"M {x:.1f} {y:.1f}"]
        for _ in range(26):
            a = angle(x, y)
            x += math.cos(a) * 12
            y += math.sin(a) * 12
            if not (40 < x < W - 40 and 40 < y < H - 280):
                break
            d.append(f"L {x:.1f} {y:.1f}")
        body.append(f'<path d="{" ".join(d)}" fill="none" stroke="{col}" stroke-width="1.8" opacity="0.55"/>')
    body.append(matte(inks[0]))
    body.append(title_block("CURRENTS", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Flow Field · {name}", "Generative"


def gen_gradient_dawn(rng):
    name, bg, inks = palette(rng)
    gid = f"g{rng.randint(0,99999)}"
    c1, c2, c3 = inks[3], inks[0], inks[1]
    defs = (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{c1}"/>'
        f'<stop offset="55%" stop-color="{c2}"/>'
        f'<stop offset="100%" stop-color="{c3}"/>'
        f'</linearGradient>'
    )
    body = [f'<rect x="120" y="120" width="{W-240}" height="{H-360}" fill="url(#{gid})"/>']
    cy = rng.randint(500, 900)
    body.append(f'<circle cx="{W/2:.0f}" cy="{cy}" r="180" fill="{bg}" opacity="0.85"/>')
    body.append(matte(inks[0]))
    body.append(title_block("DAYBREAK", name.upper(), inks[0]))
    return doc("".join(body), bg, defs), f"Gradient Dawn · {name}", "Abstract"


def gen_grid_dots(rng):
    name, bg, inks = palette(rng)
    body = []
    cols, rows = 12, 16
    cw, ch = (W - 220) / cols, (H - 360) / rows
    ox, oy = 130, 150
    cx, cy = cols / 2, rows / 2
    for r in range(rows):
        for c in range(cols):
            x = ox + c * cw + cw / 2
            y = oy + r * ch + ch / 2
            dist = math.hypot(c - cx, r - cy)
            rr = max(3, (min(cw, ch) / 2.4) * (1 - dist / (cols * 0.8)))
            col = inks[int(dist) % len(inks)]
            body.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{col}"/>')
    body.append(matte(inks[0]))
    body.append(title_block("HALFTONE", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Dot Matrix · {name}", "Pattern"


def gen_candy_critter(rng, idx):
    """Cute candy-critter character poster — a nod to the repo theme."""
    name, bg, inks = palette(rng)
    body = []
    cx, cy = W / 2, H / 2 - 80
    body_col = inks[rng.randint(0, len(inks) - 1)]
    accent = inks[(inks.index(body_col) + 1) % len(inks)]
    kind = idx % 5
    if kind == 0:  # gumdrop
        body.append(f'<path d="M {cx-260} {cy+220} Q {cx-260} {cy-260} {cx} {cy-260} Q {cx+260} {cy-260} {cx+260} {cy+220} Z" fill="{body_col}"/>')
        body.append(f'<ellipse cx="{cx}" cy="{cy+220}" rx="260" ry="40" fill="{accent}" opacity="0.6"/>')
    elif kind == 1:  # lollipop round
        body.append(f'<circle cx="{cx}" cy="{cy}" r="260" fill="{body_col}"/>')
        for s in range(8):
            a = 2 * math.pi * s / 8
            body.append(f'<path d="M {cx} {cy} L {cx+260*math.cos(a):.0f} {cy+260*math.sin(a):.0f} A 260 260 0 0 1 {cx+260*math.cos(a+0.4):.0f} {cy+260*math.sin(a+0.4):.0f} Z" fill="{accent}" opacity="0.35"/>')
    elif kind == 2:  # candy with wrapper
        body.append(poly([(cx-360, cy-120), (cx-220, cy), (cx-360, cy+120)], accent))
        body.append(poly([(cx+360, cy-120), (cx+220, cy), (cx+360, cy+120)], accent))
        body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="240" ry="180" fill="{body_col}"/>')
    elif kind == 3:  # cupcake
        body.append(f'<path d="M {cx-220} {cy+40} L {cx-150} {cy+250} L {cx+150} {cy+250} L {cx+220} {cy+40} Z" fill="{accent}"/>')
        body.append(f'<path d="M {cx-240} {cy+40} Q {cx} {cy-280} {cx+240} {cy+40} Z" fill="{body_col}"/>')
        body.append(f'<circle cx="{cx}" cy="{cy-230}" r="34" fill="{inks[3]}"/>')
    else:  # jellybean blob
        body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="280" ry="220" fill="{body_col}" transform="rotate(-12 {cx} {cy})"/>')
    # face
    body.append(f'<circle cx="{cx-80}" cy="{cy-30}" r="26" fill="#1a1a1a"/>')
    body.append(f'<circle cx="{cx+80}" cy="{cy-30}" r="26" fill="#1a1a1a"/>')
    body.append(f'<circle cx="{cx-72}" cy="{cy-38}" r="8" fill="#fff"/>')
    body.append(f'<circle cx="{cx+88}" cy="{cy-38}" r="8" fill="#fff"/>')
    body.append(f'<path d="M {cx-60} {cy+40} Q {cx} {cy+95} {cx+60} {cy+40}" fill="none" stroke="#1a1a1a" stroke-width="9" stroke-linecap="round"/>')
    body.append(f'<circle cx="{cx-150}" cy="{cy+20}" r="22" fill="{inks[3]}" opacity="0.55"/>')
    body.append(f'<circle cx="{cx+150}" cy="{cy+20}" r="22" fill="{inks[3]}" opacity="0.55"/>')
    body.append(matte(inks[0]))
    body.append(title_block("CANDY CRITTER", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Candy Critter #{idx+1} · {name}", "Candy Critters"


def gen_concentric_squares_spin(rng):
    name, bg, inks = palette(rng)
    body = []
    cx, cy = W / 2, H / 2 - 40
    n = rng.randint(18, 26)
    for i in range(n):
        s = (n - i) * 38
        col = inks[i % len(inks)]
        ang = i * 6
        body.append(
            f'<rect x="{cx-s/2:.0f}" y="{cy-s/2:.0f}" width="{s:.0f}" height="{s:.0f}" '
            f'fill="none" stroke="{col}" stroke-width="4" transform="rotate({ang} {cx} {cy})" opacity="0.85"/>'
        )
    body.append(matte(inks[0]))
    body.append(title_block("VORTEX", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Spinning Squares · {name}", "Op-Art"


def gen_tree_rings(rng):
    name, bg, inks = palette(rng)
    body = []
    cx, cy = W / 2 + rng.randint(-120, 120), H / 2 - 40 + rng.randint(-120, 120)
    for i in range(60):
        r = 16 + i * 16
        wob = 6 * math.sin(i)
        col = inks[i % 2]
        body.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r+wob:.0f}" fill="none" stroke="{col}" stroke-width="3.4" opacity="0.8"/>')
    body.append(matte(inks[0]))
    body.append(title_block("HEARTWOOD", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Tree Rings · {name}", "Organic"


def gen_city_skyline(rng):
    name, bg, inks = palette(rng)
    body = []
    sun_y = rng.randint(420, 640)
    body.append(f'<circle cx="{W*0.5:.0f}" cy="{sun_y}" r="200" fill="{inks[3]}" opacity="0.9"/>')
    base = H - 320
    x = 80
    while x < W - 80:
        bw = rng.randint(80, 170)
        bh = rng.randint(260, 760)
        col = inks[rng.randint(0, 2)]
        body.append(f'<rect x="{x}" y="{base-bh}" width="{bw}" height="{bh}" fill="{col}"/>')
        # windows
        for wy in range(base - bh + 30, base - 30, 60):
            for wx in range(x + 18, x + bw - 18, 44):
                if rng.random() > 0.4:
                    body.append(f'<rect x="{wx}" y="{wy}" width="18" height="26" fill="{inks[3]}" opacity="0.7"/>')
        x += bw + rng.randint(6, 24)
    body.append(matte(inks[0]))
    body.append(title_block("METROPOLIS", name.upper(), inks[0]))
    return doc("".join(body), bg), f"City Skyline · {name}", "Landscape"


def gen_checker_warp(rng):
    name, bg, inks = palette(rng)
    body = []
    cols, rows = 10, 13
    cw, ch = (W - 200) / cols, (H - 340) / rows
    ox, oy = 100, 140
    a, b = inks[0], inks[1]
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                x = ox + c * cw
                y = oy + r * ch
                sk = (c - cols / 2) * 3
                body.append(poly([(x+sk, y), (x+cw+sk, y), (x+cw-sk, y+ch), (x-sk, y+ch)], a if (r+c)%4==0 else b, 'opacity="0.92"'))
    body.append(matte(inks[0]))
    body.append(title_block("WARP", name.upper(), inks[0]))
    return doc("".join(body), bg), f"Warped Checker · {name}", "Op-Art"


# ===========================================================================
# QUOTES for the typographic posters
# ===========================================================================
QUOTES = [
    ("Stay wild moon child", "Anonymous"),
    ("Less is more", "Mies van der Rohe"),
    ("Bloom where you are planted", "Proverb"),
    ("Good vibes only", "Modern"),
    ("Wander often wonder always", "Anonymous"),
    ("Home sweet home", "Classic"),
    ("Do small things with great love", "Mother Teresa"),
    ("Be the light", "Anonymous"),
    ("Slow down and breathe", "Modern"),
    ("And so the adventure begins", "Anonymous"),
    ("Make today amazing", "Modern"),
    ("Gather here with grateful hearts", "Anonymous"),
]


# ===========================================================================
# BUILD THE COLLECTION (exactly 100 pieces)
# ===========================================================================
def build():
    os.makedirs(OUT, exist_ok=True)
    # wipe previous run
    for f in os.listdir(OUT):
        if f.endswith(".svg"):
            os.remove(os.path.join(OUT, f))

    pieces = []  # (svg, title, category)

    def add(fn, *args):
        rng = random.Random(len(pieces) * 7919 + 13)
        pieces.append(fn(rng, *args))

    # Plan: distribute families so we hit exactly 100.
    plan = [
        (gen_mandala, 8),
        (gen_mountains, 7),
        (gen_sunburst, 5),
        (gen_arcs, 5),
        (gen_bauhaus, 5),
        (gen_spirograph, 5),
        (gen_waves, 4),
        (gen_seigaiha, 3),
        (gen_moonphases, 3),
        (gen_constellation, 3),
        (gen_circlepack, 4),
        (gen_lowpoly, 4),
        (gen_albers, 4),
        (gen_terrazzo, 4),
        (gen_botanical, 4),
        (gen_opart, 3),
        (gen_flowfield, 4),
        (gen_gradient_dawn, 3),
        (gen_grid_dots, 3),
        (gen_concentric_squares_spin, 3),
        (gen_tree_rings, 3),
        (gen_city_skyline, 3),
        (gen_checker_warp, 3),
    ]
    for fn, count in plan:
        for _ in range(count):
            add(fn)

    # Candy critters (themed) — 5
    for i in range(5):
        rng = random.Random(1000 + i)
        pieces.append(gen_candy_critter(rng, i))

    # Typographic quotes — fill to 100
    qi = 0
    while len(pieces) < 100:
        rng = random.Random(5000 + qi)
        q, a = QUOTES[qi % len(QUOTES)]
        pieces.append(gen_quote(rng, q, a))
        qi += 1

    pieces = pieces[:100]

    manifest = []
    for i, (svg, title, cat) in enumerate(pieces, 1):
        fname = f"{i:03d}-{slug(title)}.svg"
        with open(os.path.join(OUT, fname), "w") as fh:
            fh.write(svg)
        manifest.append({"n": i, "file": f"art/prints/{fname}", "title": title, "category": cat})

    with open(os.path.join(HERE, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)

    write_gallery(manifest)
    return manifest


def slug(s):
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -·":
            out.append("-")
    res = "".join(out)
    while "--" in res:
        res = res.replace("--", "-")
    return res.strip("-")[:48]


def write_gallery(manifest):
    cats = {}
    for m in manifest:
        cats.setdefault(m["category"], 0)
        cats[m["category"]] += 1
    chips = "".join(
        f'<button class="chip" data-cat="{c}">{c} <span>{n}</span></button>'
        for c, n in sorted(cats.items())
    )
    cards = "".join(
        f'<figure class="card" data-cat="{m["category"]}">'
        f'<a href="{m["file"]}" target="_blank" rel="noopener">'
        f'<img loading="lazy" src="{m["file"]}" alt="{m["title"]}"></a>'
        f'<figcaption><span class="num">{m["n"]:03d}</span> {m["title"]}'
        f'<a class="dl" href="{m["file"]}" download>Download</a></figcaption>'
        f'</figure>'
        for m in manifest
    )
    html = GALLERY_TEMPLATE.replace("{{CHIPS}}", chips).replace("{{CARDS}}", cards).replace("{{COUNT}}", str(len(manifest)))
    with open(os.path.join(ROOT, "index.html"), "w") as fh:
        fh.write(html)


GALLERY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Printable Wall Art — 100-piece Collection</title>
<style>
  :root { --bg:#f6f4ef; --ink:#1d1d1f; --muted:#7a766e; --card:#fff; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         background:var(--bg); color:var(--ink); }
  header { padding:54px 24px 18px; text-align:center; }
  header h1 { margin:0; font-size:clamp(28px,5vw,52px); letter-spacing:-1px; }
  header p { color:var(--muted); max-width:640px; margin:14px auto 0; line-height:1.5; }
  .filters { position:sticky; top:0; z-index:5; background:var(--bg);
             padding:16px 16px; display:flex; flex-wrap:wrap; gap:8px; justify-content:center;
             border-bottom:1px solid #e4e0d7; }
  .chip { border:1px solid #d8d3c8; background:#fff; border-radius:999px; padding:7px 14px;
          font-size:13px; cursor:pointer; color:var(--ink); transition:.15s; }
  .chip span { color:var(--muted); }
  .chip:hover { border-color:var(--ink); }
  .chip.active { background:var(--ink); color:#fff; }
  .chip.active span { color:#cfcabd; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr));
          gap:22px; padding:28px clamp(16px,4vw,48px) 80px; max-width:1500px; margin:0 auto; }
  .card { margin:0; background:var(--card); border-radius:14px; overflow:hidden;
          box-shadow:0 1px 3px rgba(0,0,0,.08); transition:transform .15s, box-shadow .15s; }
  .card:hover { transform:translateY(-4px); box-shadow:0 12px 30px rgba(0,0,0,.14); }
  .card img { width:100%; display:block; aspect-ratio:4/5; object-fit:cover; background:#eee; }
  figcaption { padding:12px 14px 14px; font-size:13.5px; line-height:1.4; }
  .num { color:var(--muted); font-variant-numeric:tabular-nums; margin-right:6px; }
  .dl { display:block; margin-top:8px; font-size:12px; color:#0a66c2; text-decoration:none; }
  .dl:hover { text-decoration:underline; }
  footer { text-align:center; color:var(--muted); padding:30px; font-size:13px; }
</style>
</head>
<body>
<header>
  <h1>Printable Wall Art</h1>
  <p>A collection of {{COUNT}} original, royalty-free vector posters in a 4:5 ratio —
     perfect for 8×10, 11×14, 16×20 or 18×22.5 frames. Click any piece to open the full-size
     SVG, then print it or download it. Filter by style below.</p>
</header>
<div class="filters">
  <button class="chip active" data-cat="all">All <span>{{COUNT}}</span></button>
  {{CHIPS}}
</div>
<div class="grid">{{CARDS}}</div>
<footer>Generated by <code>art/generate.py</code> · 100 pieces · pure SVG, scales to any size.</footer>
<script>
  const chips = document.querySelectorAll('.chip');
  const cards = document.querySelectorAll('.card');
  chips.forEach(ch => ch.addEventListener('click', () => {
    chips.forEach(c => c.classList.remove('active'));
    ch.classList.add('active');
    const cat = ch.dataset.cat;
    cards.forEach(card => {
      card.style.display = (cat === 'all' || card.dataset.cat === cat) ? '' : 'none';
    });
  }));
</script>
</body>
</html>
"""


if __name__ == "__main__":
    m = build()
    by_cat = {}
    for x in m:
        by_cat[x["category"]] = by_cat.get(x["category"], 0) + 1
    print(f"Generated {len(m)} printable art pieces into art/prints/")
    for c, n in sorted(by_cat.items()):
        print(f"  {n:3d}  {c}")
