"""Grundgeruest der Wiki-Videos: Zeit, Schrift, Hintergrund, Beschriftung, Bausteine.

Entstanden aus dem Clan-Vorschauvideo vom 13.10.2026 (render.py), damit alle
Filme gleich aussehen: Himmel mit Wolken und schwebenden Inseln, links Kicker,
Titel und Text in Avenir Next, rechts Minecraft-Optik aus mc.py.

Ein Film (filme/*.py) legt SZENEN an und ruft am Ende basis.film(...) auf.
Gerendert wird mit bauen.py. Texte sind zweisprachig: L("Deutsch", "English").
Die Sprache kommt aus der Umgebungsvariable SPRACHE (de oder en).
"""
import functools
import math
import os
import random
import re

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import mc

W, H, FPS = 1920, 1080, 30
HIER = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(os.path.dirname(HIER))
LOGO = "/Users/kay/IdeaProjects/Datapacks/MBDefault/assets/megabuild/textures/font/logo"
CX = 1330  # Mitte der rechten Bildhaelfte
SPRACHE = os.environ.get("SPRACHE", "de")


def L(de, en=None):
    """Text in der Sprache des Films."""
    return en if SPRACHE == "en" and en is not None else de


# ── Zeit ────────────────────────────────────────────────────────────────────

def phase(t, a, b):
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    return (t - a) / (b - a)


def aus_kubisch(x):
    return 1 - (1 - x) ** 3


def ein_kubisch(x):
    return x ** 3


def ein_aus(x):
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def rueckschwung(x, s=1.70158):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def umkehr_ein_aus(y):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        if ein_aus(m) < y:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def tausender(n):
    s = str(n)
    if len(s) <= 3:
        return s
    trenner = "," if SPRACHE == "en" else " "
    return tausender(int(s[:-3])) + trenner + s[-3:]


def tippen(text, t, t0, t1):
    n = int(round(len(text) * phase(t, t0, t1)))
    return text[:n]


# ── Avenir ──────────────────────────────────────────────────────────────────

AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
GEWICHT = {"bold": 0, "demi": 2, "medium": 5, "regular": 7, "heavy": 8}


@functools.lru_cache(maxsize=None)
def schrift(groesse, gewicht):
    return ImageFont.truetype(AVENIR, groesse, index=GEWICHT[gewicht])


def textbreite(text, groesse, gewicht, sperrung=0):
    f = schrift(groesse, gewicht)
    if sperrung:
        return sum(f.getlength(c) for c in text) + sperrung * max(0, len(text) - 1)
    return f.getlength(text)


@functools.lru_cache(maxsize=1024)
def av_bild(text, groesse, gewicht, farbe, schatten, sperrung):
    f = schrift(groesse, gewicht)
    breite = textbreite(text, groesse, gewicht, sperrung)
    asc, desc = f.getmetrics()
    rand = max(10, groesse // 3)
    w, h = int(math.ceil(breite)) + 2 * rand, asc + desc + 2 * rand
    txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    if sperrung:
        x = rand
        for c in text:
            d.text((x, rand), c, font=f, fill=farbe + (255,))
            x += f.getlength(c) + sperrung
    else:
        d.text((rand, rand), text, font=f, fill=farbe + (255,))
    if schatten:
        a = txt.getchannel("A").filter(ImageFilter.GaussianBlur(max(1.5, groesse * 0.08)))
        a = a.point(lambda v: int(v * schatten))
        sch = Image.new("RGBA", (w, h), (2, 6, 18, 0))
        sch.putalpha(a)
        out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        mc.einfuegen(out, sch, 0, max(1, groesse // 16))
        out.alpha_composite(txt)
        txt = out
    return txt, rand, breite


def av(ziel, text, x, y, groesse, gewicht="medium", farbe=(255, 255, 255), alpha=1.0,
       schatten=0.5, sperrung=0, anker="l"):
    """Text mit Oberkante der Zeile bei y. anker l/m/r fuer x."""
    bild, rand, breite = av_bild(text, groesse, gewicht, farbe, schatten, sperrung)
    if anker == "m":
        x -= breite / 2
    elif anker == "r":
        x -= breite
    mc.einfuegen(ziel, bild, x - rand, y - rand, alpha)
    return breite


def umbruch(text, groesse, gewicht, maxb):
    zeilen = []
    for absatz in text.split("\n"):
        cur = ""
        for wort in absatz.split(" "):
            probe = (cur + " " + wort).strip()
            if not cur or textbreite(probe, groesse, gewicht) <= maxb:
                cur = probe
            else:
                zeilen.append(cur)
                cur = wort
        zeilen.append(cur)
    return zeilen


# ── MC-Hilfen ───────────────────────────────────────────────────────────────

def mct(ziel, x, y, text, S, alpha=1.0, anker="l", schatten=True):
    """MC-Schrift mit Oberkante y; anker l/m/r."""
    b = mc.breite(text) * S
    if anker == "m":
        x -= b / 2
    elif anker == "r":
        x -= b
    if alpha > 0.003:
        mc.einfuegen(ziel, mc.text_bild(text, S, schatten), x, y - 3 * S, alpha)
    return b


def mc_umbruch(text, maxb_gui):
    """MC-Text nach GUI-Pixelbreite umbrechen; Farbcodes laufen in die naechste Zeile weiter."""
    zeilen, cur, code = [], "", ""
    for wort in text.split(" "):
        probe = (cur + " " + wort) if cur else code + wort
        if cur and mc.breite(probe) > maxb_gui:
            zeilen.append(cur)
            codes = re.findall(r"§.", cur)
            code = "".join(c for c in codes[-2:] if c.lower() != "§r") if codes else ""
            cur = code + wort
        else:
            cur = probe
    zeilen.append(cur)
    return zeilen


def skaliert(ziel, bild, cx, cy, groesse_w, groesse_h=None, alpha=1.0, glatt=False):
    """Bild mittig bei (cx, cy) in der Groesse einfuegen (pixelhart oder glatt)."""
    groesse_h = groesse_w if groesse_h is None else groesse_h
    w, h = max(1, int(round(groesse_w))), max(1, int(round(groesse_h)))
    if w < 2 or h < 2:
        return
    b = bild.resize((w, h), Image.LANCZOS if glatt else Image.NEAREST)
    mc.einfuegen(ziel, b, cx - w / 2, cy - h / 2, alpha)


def wappen_bei(ziel, farbe, motiv, cx, cy, groesse, alpha=1.0):
    skaliert(ziel, mc.wappen(farbe, motiv), cx, cy, groesse, alpha=alpha)


def icon_bei(ziel, name, x, y, px, alpha=1.0):
    mc.einfuegen(ziel, mc.icon(name, px), x, y, alpha)


@functools.lru_cache(maxsize=64)
def tafel(w, h, r=18, farbe=(10, 16, 36, 218), rand=(255, 255, 255, 34)):
    k = 3
    big = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    d.rounded_rectangle((0, 0, w * k - 1, h * k - 1), r * k, fill=rand)
    d.rounded_rectangle((2 * k, 2 * k, w * k - 1 - 2 * k, h * k - 1 - 2 * k), (r - 2) * k, fill=farbe)
    return big.resize((w, h), Image.LANCZOS)


def ring(ziel, cx, cy, radius, alpha, breite=4, farbe=(255, 255, 255)):
    if alpha <= 0 or radius <= 1:
        return
    k = 3
    gr = int(radius + breite + 4)
    big = Image.new("RGBA", (gr * 2 * k, gr * 2 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    m = gr * k
    d.ellipse((m - radius * k, m - radius * k, m + radius * k, m + radius * k),
              outline=farbe + (int(255 * alpha),), width=int(breite * k))
    b = big.resize((gr * 2, gr * 2), Image.LANCZOS)
    mc.einfuegen(ziel, b, cx - gr, cy - gr)


def funkeln(ziel, cx, cy, groesse, alpha, farbe=(255, 255, 240)):
    """Vierzackiger Stern."""
    if alpha <= 0 or groesse < 2:
        return
    k = 3
    g = int(groesse)
    big = Image.new("RGBA", (g * 2 * k, g * 2 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    m = g * k
    s = groesse * k
    d.polygon([(m, m - s), (m + s * .22, m - s * .22), (m + s, m), (m + s * .22, m + s * .22),
               (m, m + s), (m - s * .22, m + s * .22), (m - s, m), (m - s * .22, m - s * .22)],
              fill=farbe + (int(255 * min(1, alpha)),))
    b = big.resize((g * 2, g * 2), Image.LANCZOS)
    mc.einfuegen(ziel, b, cx - g, cy - g)


def funkenkranz(ziel, cx, cy, t, t0, radius=190, n=6, farbe=(255, 255, 240), groesse=18):
    """Kurzer Kranz aus Funken ab t0 (fuer 'geschafft'-Momente)."""
    for i in range(n):
        w = i / n * 2 * math.pi + .4
        u = phase(t, t0 + .05 * i, t0 + .05 * i + .6)
        if 0 < u < 1:
            funkeln(ziel, cx + math.cos(w) * (radius + 40 * u), cy + math.sin(w) * (radius + 40 * u),
                    groesse * math.sin(math.pi * u), math.sin(math.pi * u), farbe)


@functools.lru_cache(maxsize=32)
def glanz(radius, farbe=(255, 255, 255), staerke=120):
    """Weicher runder Lichtfleck."""
    g = int(radius * 2)
    k = 4
    klein = Image.new("L", (max(4, g // k), max(4, g // k)), 0)
    d = ImageDraw.Draw(klein)
    m = klein.width / 2
    d.ellipse((m * .55, m * .55, m * 1.45, m * 1.45), fill=staerke)
    klein = klein.filter(ImageFilter.GaussianBlur(klein.width / 9))
    a = klein.resize((g, g), Image.BILINEAR)
    img = Image.new("RGBA", (g, g), farbe + (0,))
    img.putalpha(a)
    return img


# ── Mauszeiger ──────────────────────────────────────────────────────────────

def zeigerweg(t, punkte):
    """punkte: [(zeit, x, y)] - dazwischen weich bewegt."""
    if t <= punkte[0][0]:
        return punkte[0][1:]
    for (t0, x0, y0), (t1, x1, y1) in zip(punkte, punkte[1:]):
        if t <= t1:
            u = ein_aus(phase(t, t0, t1))
            return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return punkte[-1][1:]


def zeiger(ziel, x, y, alpha=1.0, druck=0.0):
    z = mc.mauszeiger(46)
    if druck > 0:
        z = z.resize((int(z.width * (1 - .12 * druck)), int(z.height * (1 - .12 * druck))), Image.LANCZOS)
    mc.einfuegen(ziel, z, x - 3, y - 3, alpha)


def klick(ziel, t, t0, x, y, alpha=1.0):
    """Ring an der Klickstelle."""
    if t0 <= t < t0 + .45:
        u = phase(t, t0, t0 + .45)
        ring(ziel, x, y, 10 + 40 * u, (1 - u) * alpha)


# ── Hintergrund ─────────────────────────────────────────────────────────────

def _verlauf(stops):
    streifen = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        for (ta, ca), (tb, cb) in zip(stops, stops[1:]):
            if ta <= t <= tb:
                u = (t - ta) / (tb - ta)
                streifen.putpixel((0, y), tuple(round(ca[i] + (cb[i] - ca[i]) * u) for i in range(3)))
                break
    bild = streifen.resize((W, H), Image.NEAREST)
    # weiches Licht hinter der rechten Bildhaelfte
    licht = Image.new("L", (W // 8, H // 8), 0)
    d = ImageDraw.Draw(licht)
    d.ellipse(((CX - 640) // 8, (520 - 420) // 8, (CX + 640) // 8, (520 + 420) // 8), fill=46)
    licht = licht.filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BILINEAR)
    hell = Image.new("RGB", (W, H), (150, 200, 255))
    bild = Image.composite(hell, bild, licht)
    rausch = Image.effect_noise((W, H), 1.6).convert("RGB")
    bild = ImageChops.add(bild, rausch, 1.0, -128)
    return bild.convert("RGBA")


def _wolke(rechtecke, zelle, alpha):
    w = max(x + b for x, y, b, h in rechtecke)
    h = max(y + hh for x, y, b, hh in rechtecke)
    img = Image.new("RGBA", (w * zelle, h * zelle), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for x, y, b, hh in rechtecke:
        d.rectangle((x * zelle, y * zelle, (x + b) * zelle - 1, (y + hh) * zelle - 1), fill=(255, 255, 255, alpha))
    unten = max(y + hh for x, y, b, hh in rechtecke)
    for x, y, b, hh in rechtecke:
        if y + hh == unten:
            d.rectangle((x * zelle, (unten - 1) * zelle + zelle // 2, (x + b) * zelle - 1, unten * zelle - 1),
                        fill=(200, 215, 240, int(alpha * .8)))
    return img


FORMEN = [
    [(2, 0, 5, 1), (0, 1, 11, 1), (1, 2, 8, 1)],
    [(1, 0, 3, 1), (0, 1, 7, 1)],
    [(3, 0, 6, 1), (0, 1, 13, 1), (2, 2, 10, 1)],
    [(0, 0, 4, 1), (2, 1, 6, 1)],
]
WOLKEN = [  # Form, Zelle, Alpha, y, Tempo, Start-x
    (0, 16, 34, 120, 9, 300), (1, 12, 26, 210, 14, 1400), (2, 18, 30, 900, 7, 1100),
    (3, 12, 24, 330, 11, 700), (1, 20, 22, 760, 6, 1750), (2, 14, 28, 60, 12, 1900),
    (0, 11, 24, 990, 16, 500),
]


def insel_bild(breite, tiefe, seed, zelle, alpha=1.0, dunst=0.0, gras=(88, 160, 64), gras_h=(118, 190, 82),
               baum=True, krone=((64, 138, 54), (84, 160, 66))):
    """Pixel-Insel wie im Hintergrund; mit dunst=0 und alpha=1 als Motiv im Vordergrund."""
    rnd = random.Random(seed)
    erde, erde_d = (120, 84, 52), (96, 66, 42)
    steine = [(116, 116, 126), (96, 96, 108), (78, 78, 90)]
    zellen = {}
    for x in range(breite):
        zellen[(x, 0)] = gras_h if rnd.random() < .45 else gras
        zellen[(x, 1)] = erde
        zellen[(x, 2)] = erde_d if rnd.random() < .6 else erde
    links, rechts = 0, breite
    for y in range(3, 3 + tiefe):
        links += rnd.choice((0, 1, 1, 2))
        rechts -= rnd.choice((0, 1, 1, 2))
        if rechts - links < 1:
            break
        for x in range(links, rechts):
            zellen[(x, y)] = rnd.choice(steine)
    if baum:
        tx = rnd.randint(2, max(2, breite - 4))
        for y in (-1, -2, -3):
            zellen[(tx, y)] = (104, 72, 44)
        for dy, b in ((-4, 5), (-5, 5), (-6, 3)):
            for x in range(tx - b // 2, tx + b // 2 + 1):
                zellen[(x, dy)] = krone[0] if rnd.random() < .6 else krone[1]
    xs = [k[0] for k in zellen]
    ys = [k[1] for k in zellen]
    x0, y0 = min(xs), min(ys)
    img = Image.new("RGBA", ((max(xs) - x0 + 1) * zelle, (max(ys) - y0 + 1) * zelle), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    himmel = (60, 100, 160)
    for (x, y), c in zellen.items():
        c = tuple(round(c[i] * (1 - dunst) + himmel[i] * dunst) for i in range(3))
        d.rectangle(((x - x0) * zelle, (y - y0) * zelle, (x - x0 + 1) * zelle - 1, (y - y0 + 1) * zelle - 1),
                    fill=c + (int(255 * alpha),))
    return img


HIMMEL = [(0.0, (14, 22, 50)), (0.55, (30, 60, 116)), (1.0, (74, 124, 184))]
BASIS = _verlauf(HIMMEL)
WOLKEN_BILDER = [_wolke(FORMEN[f], z, a) for f, z, a, *_ in WOLKEN]
INSELN = [  # Bild, x, y, Wippen, Phase
    (insel_bild(16, 7, 3, 9, .62, .45), -60, 820, 7, 0.0),
    (insel_bild(10, 5, 8, 6, .5, .62), 1640, 120, 5, 1.7),
    (insel_bild(13, 6, 21, 8, .58, .5), 1600, 860, 6, 3.1),
    (insel_bild(7, 4, 5, 5, .42, .7), 760, 70, 4, 4.4),
]


def hintergrund(t):
    f = BASIS.copy()
    for bild, (form, z, a, y, tempo, x0) in zip(WOLKEN_BILDER, WOLKEN):
        spanne = W + bild.width
        x = (x0 - tempo * t) % spanne - bild.width
        mc.einfuegen(f, bild, x, y)
    for bild, x, y, wip, ph in INSELN:
        mc.einfuegen(f, bild, x + 3 * math.sin(t * .21 + ph), y + wip * math.sin(t * .55 + ph))
    return f


def _blende():
    breite = 1150
    streifen = Image.new("L", (breite, 1))
    for x in range(breite):
        u = x / breite
        streifen.putpixel((x, 0), int(205 * (1 - (3 * u * u - 2 * u * u * u))))
    a = streifen.resize((breite, H))
    img = Image.new("RGBA", (breite, H), (6, 10, 26, 0))
    img.putalpha(a)
    return img


BLENDE = _blende()


def abzeichen(text, farbe=(255, 210, 90), text_farbe=(255, 222, 130)):
    """Pille oben rechts, z. B. 'VORSCHAU · noch in Planung'."""
    g = 24
    tb = textbreite(text, g, "demi", 1)
    w, h = int(tb) + 78, 50
    img = tafel(w, h, 25, (16, 20, 38, 205), farbe + (200,)).copy()
    d = ImageDraw.Draw(img)
    d.ellipse((24, h // 2 - 6, 36, h // 2 + 6), fill=farbe + (255,))
    av(img, text, 50, 10, g, "demi", text_farbe, 1.0, schatten=0, sperrung=1)
    return img


WORTMARKE = Image.open(os.path.join(LOGO, "sblogo.png")).convert("RGBA")


@functools.lru_cache(maxsize=8)
def foto(pfad, w, h):
    """Screenshot passend beschnitten (cover) in w x h."""
    img = Image.open(pfad).convert("RGB")
    f = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * f + .5), int(img.height * f + .5)), Image.LANCZOS)
    x0, y0 = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")


@functools.lru_cache(maxsize=8)
def foto_karte(pfad, w, h, r=22):
    """Screenshot mit runden Ecken und hellem Rand."""
    img = foto(pfad, w, h).copy()
    k = 3
    maske = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, w * k - 1, h * k - 1), r * k, fill=255)
    img.putalpha(maske.resize((w, h), Image.LANCZOS))
    rahmen = tafel(w + 8, h + 8, r + 4, (0, 0, 0, 0), (255, 255, 255, 60)).copy()
    rahmen.alpha_composite(img, (4, 4))
    return rahmen


# ── Beschriftung links ──────────────────────────────────────────────────────

TITEL_G, TEXT_G = 70, 34


def beschriftung(f, sz, lt, d):
    aus = 1 - ein_kubisch(phase(lt, d - .4, d - .05))
    x0 = 110
    tz = umbruch(sz["titel"], TITEL_G, "heavy", 660)
    bz = umbruch(sz["text"], TEXT_G, "medium", 640)
    hoehe = 32 + 26 + len(tz) * 82 + 22 + len(bz) * 50
    y = 548 - hoehe / 2
    for i, (zeilen, art) in enumerate(((None, "kicker"), (tz, "titel"), (bz, "text"))):
        u = aus_kubisch(phase(lt, .12 + i * .12, .62 + i * .12))
        a = u * aus
        dx = -36 * (1 - u)
        if art == "kicker":
            w = av(f, sz["nr"], x0 + dx, y, 28, "heavy", (85, 255, 255), a, schatten=.3)
            linie = Image.new("RGBA", (34, 3), (85, 255, 255, 200))
            mc.einfuegen(f, linie, x0 + dx + w + 14, y + 19, a)
            av(f, sz["kicker"].upper(), x0 + dx + w + 62, y + 3, 24, "demi", (170, 222, 255), a, schatten=.3, sperrung=3)
            y += 32 + 26
        elif art == "titel":
            for z in zeilen:
                av(f, z, x0 + dx, y, TITEL_G, "heavy", (255, 255, 255), a, schatten=.55)
                y += 82
            y += 22
        else:
            for z in zeilen:
                av(f, z, x0 + dx, y, TEXT_G, "medium", (214, 228, 248), a, schatten=.4)
                y += 50


# ── Menues, Tooltips, Chat, Tablist ─────────────────────────────────────────

def slot_mitte(slot, mx, my, S):
    x, y = mc.slot_xy(slot)
    return mx + (x + 9) * S, my + (y + 10) * S


def tooltip_bei(e, zeilen, zx, zy, S, alpha=1.0):
    tip = mc.tooltip_bild(zeilen, S)
    x, y = zx + 12 * S - 4 * S, zy - 12 * S - 4 * S
    if x + tip.width > W - 16:
        x = max(860, W - 16 - tip.width)
        if x < zx - 8 * S:
            y = zy + 14 * S
    y = max(16, min(H - 16 - tip.height, y))
    mc.einfuegen(e, tip, x, y, alpha)


@functools.lru_cache(maxsize=None)
def _menue(titel, reihen, slots_items, S):
    return mc.menue_bild(titel, reihen, dict(slots_items), S)


def menue_mit_zeiger(e, t, titel, reihen, slots, tipps, halte, mx, my, S, ein):
    """halte: [(t0, t1, slot)] - der Zeiger faehrt bis t1 auf den Slot; danach Tooltip."""
    m = _menue(titel, reihen, tuple(sorted(slots.items())), S)
    mc.einfuegen(e, m, mx, my, ein)
    punkte = [(0, mx + m.width + 120, my + m.height + 180)]
    for t0, t1, slot in halte:
        px, py = slot_mitte(slot, mx, my, S)
        punkte.append((t0, punkte[-1][1], punkte[-1][2]))
        punkte.append((t1, px, py))
    zx, zy = zeigerweg(t, punkte)
    for slot in slots:
        sx, sy = mc.slot_xy(slot)
        x0, y0 = mx + sx * S, my + sy * S
        if x0 - S <= zx < x0 + 17 * S and y0 - S <= zy < y0 + 17 * S:
            mc.einfuegen(e, mc.slot_markierung(S), x0, y0, ein)
    zeiger(e, zx, zy, ein)
    for i, (t0, t1, slot) in enumerate(halte):
        weg = halte[i + 1][0] if i + 1 < len(halte) else 99
        if t1 + .05 <= t < weg and slot in tipps:
            tooltip_bei(e, tipps[slot], zx, zy, S, ein)
    return m


def tablist(e, x, y, eintraege, S, alpha):
    breite_gui = max(mc.breite(z) for z in eintraege) + 4
    hoehe_gui = len(eintraege) * 9 + 1
    mc.einfuegen(e, Image.new("RGBA", (breite_gui * S, hoehe_gui * S), (0, 0, 0, 128)), x, y, alpha)
    zeile = Image.new("RGBA", ((breite_gui - 2) * S, 8 * S), (255, 255, 255, 32))
    for i, z in enumerate(eintraege):
        mc.einfuegen(e, zeile, x + S, y + (1 + i * 9) * S, alpha)
        mct(e, x + 2 * S, y + (1 + i * 9) * S, z, S, alpha)
    return breite_gui * S, hoehe_gui * S


def chat(e, x, y_unten, zeilen, t, S, alpha, eingabe=None, breite_gui=320):
    """zeilen: [(zeit, text)] in Reihenfolge; die neueste steht unten."""
    sichtbar = [(z0, txt) for z0, txt in zeilen if t >= z0]
    y = y_unten
    for i, (z0, txt) in enumerate(reversed(sichtbar)):
        u = aus_kubisch(phase(t, z0, z0 + .18))
        hoch = 9 * S
        mc.einfuegen(e, mc.chat_zeile_bild(txt, S, breite_gui), x, y - hoch + (1 - u) * hoch * .6 if i == 0 else y - hoch,
                     alpha * (u if i == 0 else 1))
        if i == 0:
            y -= hoch * u
        else:
            y -= hoch
    if eingabe is not None:
        mc.einfuegen(e, Image.new("RGBA", (breite_gui * S, 12 * S), (0, 0, 0, 128)), x, y_unten + 4 * S, alpha)
        mct(e, x + 2 * S, y_unten + 6 * S, eingabe, S, alpha)


def karte(e, x, y, w, h, icon, titel, zeilen=(), alpha=1.0, S=3, icon_px=64, hervor=False):
    """Tafel mit Icon links, MC-Titel und grauen Zeilen."""
    if hervor:
        mc.einfuegen(e, tafel(w + 12, h + 12, 22, (85, 255, 255, 40), (85, 255, 255, 220)), x - 6, y - 6, alpha)
    mc.einfuegen(e, tafel(w, h, 16), x, y, alpha)
    ix = x + 24
    if icon:
        icon_bei(e, icon, ix, y + (h - icon_px) / 2 if not zeilen else y + 22, icon_px, alpha)
        tx = ix + icon_px + 22
    else:
        tx = ix
    ty = y + 26 if zeilen else y + h / 2 - 4 * S
    mct(e, tx, ty, titel, S + 1 if zeilen else S + 1, alpha)
    for i, z in enumerate(zeilen):
        mct(e, tx, ty + 48 + i * 34, z, S, alpha)


# ── HUD ─────────────────────────────────────────────────────────────────────

def hud_kasten(e, x, y, icon_name, text, S, alpha=1.0, balken=None, balken_farbe=None):
    """Ein Kasten der BossBar oben: Pille mit Symbol und Text, optional Balken darunter."""
    inhalt = 14 + mc.breite(text) + 6
    pille = mc.pille_bild(inhalt, S)
    mc.einfuegen(e, pille, x, y, alpha)
    if icon_name:
        sym = mc.hud_bild(icon_name)
        skaliert(e, sym, x + 9 * S, y + 8 * S, 9 * S, 9 * S * sym.height / sym.width, alpha)
    mct(e, x + 17 * S, y + 4 * S, text, S, alpha)
    if balken is not None:
        fuell = mc.gefaerbt("bar_fill64", balken_farbe) if balken_farbe else "bar_fill64"
        b = mc.balken_bild(max(20, inhalt - 22), balken, S, fuell)
        mc.einfuegen(e, b, x + 17 * S, y + 17 * S, alpha)
    return pille.width


def mana_ruby(e, x_rechts, y, mana, ruby, S, alpha=1.0):
    """Anzeige unten rechts: Ruby ueber Mana."""
    for i, (sym, wert, farbe) in enumerate((("hud_ruby", ruby, "§c"), ("hud_mana", mana, "§d"))):
        yy = y + i * 11 * S
        b = mct(e, x_rechts - 11 * S, yy, farbe + tausender(int(round(wert))), S, alpha, anker="r")
        skaliert(e, mc.hud_bild(sym), x_rechts - 4 * S, yy + 3.5 * S, 8 * S, 8 * S, alpha)


# ── Untertitel (Mala) ───────────────────────────────────────────────────────

def untertitel(e, text, alpha, y=1012, S=4):
    """Wie im Spiel: 'Mala: …' ueber der Schnellleiste, Name in Aqua."""
    if alpha <= 0.003 or not text:
        return
    zeilen = mc_umbruch("§f" + text, 300)
    zeilen[0] = "§bMala§7: " + zeilen[0]
    hoehe = len(zeilen) * 11 * S + 6 * S
    breite_gui = max(mc.breite(z) for z in zeilen) + 8
    y0 = y - hoehe
    mc.einfuegen(e, tafel(breite_gui * S, hoehe, 12, (0, 0, 0, 150), (0, 0, 0, 0)), W / 2 - breite_gui * S / 2, y0, alpha)
    for i, z in enumerate(zeilen):
        mct(e, W / 2, y0 + 3 * S + i * 11 * S + 2 * S, z, S, alpha, anker="m")


# ── Film ────────────────────────────────────────────────────────────────────

class Film:
    """Szenenfolge mit gemeinsamem Rahmen (Hintergrund, Wortmarke, Abzeichen, Fortschritt).

    Jede Szene ist ein dict: dauer, zeichne(ebene, t, dauer), optional nr/kicker/titel/text
    (Beschriftung links), ton=[(t, quelle, lautstaerke)] mit quelle 'mala:<schluessel>',
    'pack:<pfad im Pool>' oder 'sfx:<name>', und stumm=True fuer Szenen ohne Musik-Absenkung.
    """

    def __init__(self, name, szenen, abzeichen_text=None, musik=None, wortmarke=True):
        self.name = name
        self.szenen = szenen
        self.gesamt = sum(s["dauer"] for s in szenen)
        self.abzeichen = abzeichen(abzeichen_text) if abzeichen_text else None
        self.musik = musik or {}
        self.wortmarke = wortmarke
        self.untertitel = []  # (t0, t1, text) aus den Mala-Cues, von ton.py gefuellt
        starts, t0 = [], 0.0
        for sz in szenen:
            starts.append(t0)
            t0 += sz["dauer"]
        self.starts = starts

    def szene_bei(self, t):
        for sz, t0 in zip(self.szenen, self.starts):
            if t < t0 + sz["dauer"] or sz is self.szenen[-1]:
                return sz, t - t0

    def blende_alpha(self, t):
        """Linke Abdunkelung nur in Szenen mit Beschriftung."""
        sz_liste = self.szenen
        for i, (sz, t0) in enumerate(zip(sz_liste, self.starts)):
            if t0 <= t < t0 + sz["dauer"]:
                lt, d = t - t0, sz["dauer"]
                if "titel" not in sz:
                    return 0.0
                a = 1.0
                if i > 0 and "titel" not in sz_liste[i - 1]:
                    a = min(a, aus_kubisch(phase(lt, 0, .6)))
                if i + 1 < len(sz_liste) and "titel" not in sz_liste[i + 1]:
                    a = min(a, 1 - ein_kubisch(phase(lt, d - .6, d)))
                return a
        return 0.0

    def cues(self):
        """Alle Ton-Cues mit absoluter Zeit: [(t, quelle, lautstaerke)]."""
        out = []
        for sz, t0 in zip(self.szenen, self.starts):
            for c in sz.get("ton", ()):
                zeit, quelle = c[0], c[1]
                laut = c[2] if len(c) > 2 else 1.0
                out.append((t0 + zeit, quelle, laut))
        return sorted(out)

    def bild(self, t):
        f = hintergrund(t)
        a = self.blende_alpha(t)
        if a > 0:
            mc.einfuegen(f, BLENDE, 0, 0, a)
        sz, lt = self.szene_bei(t)
        d = sz["dauer"]
        ebene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sz["zeichne"](ebene, lt, d)
        letzte = sz is self.szenen[-1]
        aus = 1.0 if letzte else 1 - ein_kubisch(phase(lt, d - .38, d - .02))
        mc.einfuegen(f, ebene, 0, 0, aus)
        if "titel" in sz:
            beschriftung(f, sz, lt, d)
        for t0, t1, text in self.untertitel:
            if t0 - .2 <= t < t1 + .3:
                u = aus_kubisch(phase(t, t0 - .2, t0)) * (1 - phase(t, t1, t1 + .3))
                untertitel(f, text, u)
        if not letzte and self.wortmarke:
            mc.einfuegen(f, WORTMARKE, 60, 46, .9)
        if self.abzeichen is not None:
            mc.einfuegen(f, self.abzeichen, W - 60 - self.abzeichen.width, 40)
        balken = Image.new("RGBA", (max(1, int(W * t / self.gesamt)), 5), (85, 255, 255, 150))
        mc.einfuegen(f, balken, 0, H - 5)
        return f


# ── 3D-Modelle (Sprites aus modelle.py) ─────────────────────────────────────

SPRITES = os.path.join(HIER, ".cache", "sprites")


@functools.lru_cache(maxsize=None)
def _sprite_dateien(name):
    ordner = os.path.join(SPRITES, name)
    if not os.path.isdir(ordner):
        raise SystemExit(f"Sprite fehlt: {name} - erst python3 modelle.py laufen lassen.")
    return sorted(os.path.join(ordner, f) for f in os.listdir(ordner) if f.endswith(".png"))


@functools.lru_cache(maxsize=600)
def _sprite_bild(pfad, groesse, spiegeln):
    b = Image.open(pfad).convert("RGBA")
    if spiegeln:
        b = b.transpose(Image.FLIP_LEFT_RIGHT)
    return b.resize((groesse, groesse), Image.LANCZOS)


def sprite(e, name, t, cx, cy, groesse, alpha=1.0, schleife=True, spiegeln=False, tempo=1.0):
    """Modell-Animation (30 Bilder/s) mittig bei (cx, cy) in groesse x groesse."""
    if alpha <= 0.003 or groesse < 2:
        return
    dateien = _sprite_dateien(name)
    i = int(max(0.0, t) * FPS * tempo)
    i = i % len(dateien) if schleife else min(i, len(dateien) - 1)
    b = _sprite_bild(dateien[i], int(groesse), spiegeln)
    mc.einfuegen(e, b, cx - groesse / 2, cy - groesse / 2, alpha)


@functools.lru_cache(maxsize=None)
def sprite_unten(name):
    """Unterkante der Figur im ersten Bild als Anteil der Bildhoehe (fuer die Fuesse)."""
    box = Image.open(_sprite_dateien(name)[0]).getchannel("A").getbbox()
    return box[3] / 512 if box else 1.0


def sprite_boden(e, name, t, cx, y_boden, groesse, alpha=1.0, **kw):
    """Wie sprite(), aber die Fuesse stehen auf y_boden."""
    cy = y_boden - (sprite_unten(name) - .5) * groesse
    sprite(e, name, t, cx, cy, groesse, alpha, **kw)


def schatten(e, cx, cy, breite, alpha=1.0):
    """Weicher Schatten unter einer Figur."""
    if breite < 8 or alpha <= 0.003:
        return
    s = _schatten_bild(int(breite))
    mc.einfuegen(e, s, cx - s.width / 2, cy - s.height / 2, alpha)


@functools.lru_cache(maxsize=16)
def _schatten_bild(breite):
    h = max(4, breite // 4)
    k = 4
    img = Image.new("L", (breite * k, h * k), 0)
    ImageDraw.Draw(img).ellipse((breite * k * .1, h * k * .2, breite * k * .9, h * k * .8), fill=90)
    img = img.filter(ImageFilter.GaussianBlur(h * k / 5)).resize((breite, h), Image.LANCZOS)
    out = Image.new("RGBA", (breite, h), (8, 12, 30, 0))
    out.putalpha(img)
    return out


def namensschild(e, cx, y, text, S=3, alpha=1.0):
    """Namensschild wie ueber einer Figur im Spiel."""
    b = mc.breite(text) + 2
    mc.einfuegen(e, Image.new("RGBA", (b * S, 10 * S), (0, 0, 0, 100)), cx - b * S / 2, y, alpha)
    mct(e, cx, y + S, text, S, alpha, anker="m", schatten=False)


# ── Pixelbilder ─────────────────────────────────────────────────────────────

def pixel_bild(zeilen, farben, zelle):
    """Raster aus Zeichen -> Bild; '.' ist durchsichtig."""
    h, w = len(zeilen), max(len(z) for z in zeilen)
    img = Image.new("RGBA", (w * zelle, h * zelle), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y, z in enumerate(zeilen):
        for x, ch in enumerate(z):
            if ch != "." and ch in farben:
                d.rectangle((x * zelle, y * zelle, (x + 1) * zelle - 1, (y + 1) * zelle - 1), fill=farben[ch])
    return img


LOEWENZAHN = pixel_bild([
    "......YY........",
    ".....YyYY.......",
    "....YYyYYY......",
    ".....YYYY.......",
    "......YY........",
    ".......G........",
    ".......G........",
    "...L...G........",
    "...LL..G..LL....",
    "....LL.G.LL.....",
    ".....LLGLL......",
    ".......G........",
    ".......G........",
], {"Y": (255, 214, 40, 255), "y": (240, 160, 20, 255), "G": (70, 150, 50, 255), "L": (90, 175, 60, 255)}, 1)


@functools.lru_cache(maxsize=8)
def luftschiff_bild(zelle=8, seile=4):
    """Kleines Pixel-Luftschiff: Ballon, Seile, Rumpf mit Planken und Wimpel."""
    w = 34
    zeilen = []
    for y in range(11):  # Ballon
        ry = (y - 5) / 5.4
        halb = int(15.5 * math.sqrt(max(0.0, 1 - ry * ry)))
        z = ""
        for x in range(w):
            dx = x - 16.5
            if abs(dx) <= halb:
                rand = abs(dx) > halb - 1 or y in (0, 10)
                hell = dx < -halb * .25 and y < 5
                streifen = int(dx + 40) % 6 == 0
                z += "k" if rand else ("H" if hell else ("b" if streifen else "B"))
            else:
                z += "."
        zeilen.append(z)
    for i in range(seile):
        z = [".."] * 17
        reihe = list("." * 34)
        for xa, xb in ((4, 7), (12, 12), (21, 21), (29, 26)):
            x = round(xa + (xb - xa) * i / max(1, seile - 1))
            reihe[x] = "r"
        if i == seile - 1:
            reihe[2] = "f"
        zeilen.append("".join(reihe))
    zeilen.append(".kffkkkkkkkkkkkkkkkkkkkkkkkkkkkk..")
    zeilen.append(".kWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWk.")
    zeilen.append("..kwwwwwwwwwwwwwwwwwwwwwwwwwwwwk..")
    zeilen.append("...kWWoWWWWWWoWWWWWWoWWWWWWoWWk...")
    zeilen.append("....kwwwwwwwwwwwwwwwwwwwwwwwwk....")
    zeilen.append(".....kkkkkkkkkkkkkkkkkkkkkkkk.....")
    farben = {"B": (126, 74, 178, 255), "b": (104, 58, 152, 255), "H": (170, 120, 220, 255), "k": (44, 30, 40, 255),
              "r": (70, 52, 40, 255), "W": (140, 98, 60, 255), "w": (112, 76, 46, 255), "o": (230, 200, 120, 255),
              "f": (255, 85, 255, 255)}
    return pixel_bild(zeilen, farben, zelle)


def leuchtfeuer(e, x, y_unten, hoehe, t, alpha=1.0, farbe=(120, 230, 255)):
    """Strahl eines Leuchtfeuers (nur fuer den Spieler sichtbar - im Bild einfach ein Lichtstrahl)."""
    if alpha <= 0:
        return
    breite = 18
    strahl = Image.new("RGBA", (breite * 3, int(hoehe)), (0, 0, 0, 0))
    d = ImageDraw.Draw(strahl)
    for i in range(int(hoehe)):
        a = int(150 * (i / hoehe) ** .6 * (0.85 + .15 * math.sin(i / 14 - t * 6)))
        d.line((breite, i, breite * 2, i), fill=farbe + (a,))
        d.line((breite - 8, i, breite * 2 + 8, i), fill=farbe + (a // 4,))
    strahl = strahl.filter(ImageFilter.GaussianBlur(2))
    mc.einfuegen(e, strahl, x - breite * 1.5, y_unten - hoehe, alpha)


def ken_burns(e, pfad, x, y, w, h, t, d, zoom=0.08, alpha=1.0):
    """Screenshot langsam heranzoomen (Ausschnitt wandert leicht)."""
    basis_bild = foto(pfad, int(w * (1 + zoom)), int(h * (1 + zoom)))
    u = ein_aus(phase(t, 0, d))
    s = 1 + zoom * (1 - u)
    bw, bh = basis_bild.width / s, basis_bild.height / s
    ox = (basis_bild.width - bw) * (.3 + .4 * u)
    oy = (basis_bild.height - bh) * .5
    aus = basis_bild.crop((int(ox), int(oy), int(ox + bw), int(oy + bh))).resize((w, h), Image.LANCZOS)
    k = 3
    maske = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, w * k - 1, h * k - 1), 22 * k, fill=255)
    aus.putalpha(maske.resize((w, h), Image.LANCZOS))
    mc.einfuegen(e, tafel(w + 8, h + 8, 26, (0, 0, 0, 0), (255, 255, 255, 60)), x - 4, y - 4, alpha)
    mc.einfuegen(e, aus, x, y, alpha)


def titelkarte(e, t, titel, unter, zeile3=None, y=230):
    """Grosser Titel in der Mitte (Intro/Outro)."""
    a1 = aus_kubisch(phase(t, .1, .7))
    av(e, titel, W / 2, y + (1 - a1) * 30, 112, "heavy", (255, 255, 255), a1, anker="m")
    a2 = aus_kubisch(phase(t, .35, .95))
    av(e, unter, W / 2, y + 160 + (1 - a2) * 20, 46, "demi", (140, 236, 255), a2, anker="m", schatten=.4)
    if zeile3:
        a3 = aus_kubisch(phase(t, .6, 1.2))
        av(e, zeile3, W / 2, y + 232, 34, "medium", (214, 228, 248), a3, anker="m", schatten=.4)


def chatzeilen(eintraege, breite_gui=316):
    """[(zeit, text)] -> umgebrochene Chatzeilen, Folgezeilen mit derselben Zeit."""
    out = []
    for zeit, text in eintraege:
        for i, z in enumerate(mc_umbruch(text, breite_gui)):
            out.append((zeit + i * .001, z))
    return out
