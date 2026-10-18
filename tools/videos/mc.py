"""Minecraft-Optik fuer die Wiki-Videos: Schrift, Menues, Tooltips, Chat, Tablist, HUD.

Alles wird in GUI-Pixeln gedacht und mit einem ganzzahligen Faktor S hart
vergroessert, wie der Client bei GUI-Skalierung S. Die Schrift kommt aus dem
Client-Jar (ascii, accented, nonlatin_european), die Ausrufezeichen aus
MBDefault, die Icons aus Connector-Pack, Manager-Pack und clan_icons.py.
"""
import functools
import json
import os
import re
import sys

from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
# Minecraft-Schrift: nicht im Repo (Mojang), sondern einmal aus einem Client-Jar entpackt
# nach .cache/mcfont - siehe hole_schrift().
MC = os.path.join(HIER, ".cache", "mcfont", "assets", "minecraft")
# Repo mit tools/gen_icons.py und dem Manager-Pack: MBSKY_REPO, sonst der Hauptordner.
REPO = os.environ.get("MBSKY_REPO") or "/Users/kay/IdeaProjects/MBSkyManager"
CONNECTOR = os.environ.get("MBSC_TEXTUREN") or \
    "/Users/kay/IdeaProjects/MBSkyConnector/resourcepack_mbsky_connector/assets/mbsc/textures"
MANAGER = os.path.join(REPO, "resourcepack_mbsky_biomes", "assets", "mbsky", "textures")
MANAGER_ITEMS = os.path.join(MANAGER, "item")
POOL = os.environ.get("MBSKY_POOLS", os.path.expanduser("~/Coding/pools"))
ALERT = "/Users/kay/IdeaProjects/Datapacks/MBDefault/assets/megabuild/textures/font/alert"

sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, HIER)
import gen_icons  # noqa: E402
import clan_icons  # noqa: E402


def hole_schrift():
    """Entpackt ascii/accented/nonlatin_european aus dem neuesten Client-Jar."""
    import glob
    import zipfile
    if os.path.exists(os.path.join(MC, "font", "include", "default.json")):
        return
    jars = sorted(glob.glob(os.path.expanduser("~/Library/Application Support/minecraft/versions/*/*.jar")),
                  key=os.path.getmtime, reverse=True)
    if not jars:
        raise SystemExit("Keine Minecraft-Schrift: .cache/mcfont fehlt und kein Client-Jar gefunden.")
    ziel = os.path.join(HIER, ".cache", "mcfont")
    with zipfile.ZipFile(jars[0]) as z:
        for name in z.namelist():
            if name.startswith("assets/minecraft/font/") and name.endswith(".json") \
                    or name in ("assets/minecraft/textures/font/ascii.png", "assets/minecraft/textures/font/accented.png",
                                "assets/minecraft/textures/font/nonlatin_european.png"):
                z.extract(name, ziel)


hole_schrift()

FARBEN = {
    "0": (0, 0, 0), "1": (0, 0, 170), "2": (0, 170, 0), "3": (0, 170, 170),
    "4": (170, 0, 0), "5": (170, 0, 170), "6": (255, 170, 0), "7": (170, 170, 170),
    "8": (85, 85, 85), "9": (85, 85, 255), "a": (85, 255, 85), "b": (85, 255, 255),
    "c": (255, 85, 85), "d": (255, 85, 255), "e": (255, 255, 85), "f": (255, 255, 255),
}

# Farbige Ausrufezeichen (MBDefault): rot, gruen, gelb, blau, magenta, tuerkis
ALARM = {name: chr(0xE019 + i) for i, name in enumerate(("rot", "gruen", "gelb", "blau", "magenta", "tuerkis"))}


# ── Schrift ─────────────────────────────────────────────────────────────────

class Glyphe:
    __slots__ = ("bild", "vorschub", "oben", "farbig", "glatt")

    def __init__(self, bild, vorschub, oben, farbig=False, glatt=False):
        self.bild = bild          # Zelle in Quellpixeln (RGBA)
        self.vorschub = vorschub  # in GUI-Pixeln
        self.oben = oben          # Abstand der Oberkante zur Zeilenoberkante, GUI-Pixel
        self.farbig = farbig
        self.glatt = glatt        # hochaufgeloeste Grafik: weich verkleinern


def _lade_schrift():
    glyphen = {" ": Glyphe(None, 4, 0)}
    provider = json.load(open(os.path.join(MC, "font", "include", "default.json")))["providers"]
    for p in provider:
        datei = p["file"].split(":", 1)[1]
        blatt = Image.open(os.path.join(MC, "textures", datei)).convert("RGBA")
        zeilen = p["chars"]
        spalten = max(len(z) for z in zeilen)
        zw, zh = blatt.width // spalten, blatt.height // len(zeilen)
        hoehe = p.get("height", 8)
        skala = hoehe / zh
        assert skala == 1, (datei, skala)
        for zy, zeile in enumerate(zeilen):
            for zx, ch in enumerate(zeile):
                if ch in ("\x00", " ") or ch in glyphen:
                    continue
                zelle = blatt.crop((zx * zw, zy * zh, zx * zw + zw, zy * zh + zh))
                alpha = zelle.getchannel("A")
                box = alpha.getbbox()
                breite = box[2] if box else 0
                glyphen[ch] = Glyphe(zelle, int(0.5 + breite * skala) + 1, 7 - p["ascent"])
    for name, ch in ALARM.items():
        bild = Image.open(os.path.join(ALERT, name + ".png")).convert("RGBA")
        skala = 8 / bild.height
        breite = bild.getchannel("A").getbbox()[2]
        glyphen[ch] = Glyphe(bild, int(0.5 + breite * skala) + 1, 0, farbig=True, glatt=True)
    return glyphen


GLYPHEN = _lade_schrift()


def teile(text, farbe="f"):
    """'§b§lClan §7x' -> [(text, rgb, fett, unterstrichen)]"""
    out = []
    rgb, fett, unter = FARBEN[farbe], False, False
    puffer = ""
    i = 0
    while i < len(text):
        if text[i] == "§" and i + 1 < len(text):
            if puffer:
                out.append((puffer, rgb, fett, unter))
                puffer = ""
            c = text[i + 1].lower()
            if c in FARBEN:
                rgb, fett, unter = FARBEN[c], False, False
            elif c == "l":
                fett = True
            elif c == "n":
                unter = True
            elif c == "r":
                rgb, fett, unter = FARBEN[farbe], False, False
            i += 2
            continue
        puffer += text[i]
        i += 1
    if puffer:
        out.append((puffer, rgb, fett, unter))
    return out


def breite(text):
    """Breite in GUI-Pixeln (ohne Schatten)."""
    b = 0
    for stueck, _, fett, _ in teile(text):
        for ch in stueck:
            g = GLYPHEN.get(ch) or GLYPHEN["?"]
            b += g.vorschub + (1 if fett else 0)
    return b


@functools.lru_cache(maxsize=4096)
def _glyphe_skaliert(ch, S, rgb):
    g = GLYPHEN.get(ch) or GLYPHEN["?"]
    if g.bild is None:
        return None
    if g.glatt:
        z = g.bild.resize((max(1, round(g.bild.width * 8 * S / g.bild.height)), 8 * S), Image.LANCZOS)
    else:
        z = g.bild.resize((g.bild.width * S, g.bild.height * S), Image.NEAREST)
    if rgb != (255, 255, 255):
        r, gg, b, a = z.split()
        r = r.point(lambda v: v * rgb[0] // 255)
        gg = gg.point(lambda v: v * rgb[1] // 255)
        b = b.point(lambda v: v * rgb[2] // 255)
        z = Image.merge("RGBA", (r, gg, b, a))
    return z


@functools.lru_cache(maxsize=2048)
def text_bild(text, S, schatten=True, farbe="f"):
    """Eine Zeile als Bild. Die Zeilenoberkante liegt 3*S unter dem Bildrand,
    weil Akzente (accented.png) bis 3 Pixel darueber reichen."""
    stuecke = teile(text, farbe)
    w = breite(text) + 2
    bild = Image.new("RGBA", ((w + 1) * S, 14 * S), (0, 0, 0, 0))
    for durchgang in ((1, 0) if schatten else (0,)):
        x = 0
        for stueck, rgb, fett, unter in stuecke:
            farbe_hier = tuple(v // 4 for v in rgb) if durchgang else rgb
            versatz = S if durchgang else 0
            x0 = x
            for ch in stueck:
                g = GLYPHEN.get(ch) or GLYPHEN["?"]
                z = _glyphe_skaliert(ch, S, farbe_hier)
                if z is not None:
                    y = (3 + g.oben) * S + versatz
                    bild.alpha_composite(z, (x * S + versatz, y))
                    if fett:
                        bild.alpha_composite(z, ((x + 1) * S + versatz, y))
                x += g.vorschub + (1 if fett else 0)
            if unter:
                d = ImageDraw.Draw(bild)
                d.rectangle((x0 * S + versatz, (3 + 8) * S + versatz, x * S - 1 + versatz, (3 + 9) * S - 1 + versatz), fill=farbe_hier + (255,))
    return bild


def zeichne_text(ziel, x, y, text, S, schatten=True, farbe="f", alpha=1.0):
    """Zeile mit Oberkante (x, y) in Bildschirmpixeln."""
    b = text_bild(text, S, schatten, farbe)
    einfuegen(ziel, b, x, y - 3 * S, alpha)
    return breite(text) * S


def einfuegen(ziel, quelle, x, y, alpha=1.0):
    """alpha_composite mit Beschnitt am Rand und Deckkraft."""
    x, y = int(round(x)), int(round(y))
    if alpha <= 0.003:
        return
    if alpha < 0.997:
        quelle = mit_alpha(quelle, alpha)
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1 = min(quelle.width, ziel.width - x)
    sy1 = min(quelle.height, ziel.height - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    if (sx0, sy0, sx1, sy1) != (0, 0, quelle.width, quelle.height):
        quelle = quelle.crop((sx0, sy0, sx1, sy1))
    ziel.alpha_composite(quelle, (x + sx0, y + sy0))


def mit_alpha(bild, alpha):
    a = bild.getchannel("A").point(lambda v: int(v * alpha + 0.5))
    neu = bild.copy()
    neu.putalpha(a)
    return neu


# ── Icons ───────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=None)
def icon16(name):
    """Icon als 64x64 (16 Rasterpixel x 4)."""
    if name in clan_icons.NEU:
        return gen_icons.zeichne(clan_icons.NEU[name])
    if name in clan_icons.KOEPFE:
        return gen_icons.zeichne(clan_icons.KOEPFE[name])
    for ordner in (os.path.join(CONNECTOR, "item"), MANAGER_ITEMS, os.path.join(MANAGER, "block")):
        pfad = os.path.join(ordner, name + ".png")
        if os.path.exists(pfad):
            bild = Image.open(pfad).convert("RGBA")
            if bild.height > bild.width:  # animierte Streifen: erstes Bild
                bild = bild.crop((0, 0, bild.width, bild.width))
            return bild.resize((64, 64), Image.NEAREST)
    raise KeyError("Icon fehlt: " + name)


@functools.lru_cache(maxsize=None)
def icon(name, px):
    """Icon in px x px, hart skaliert."""
    if name.startswith("wappen:"):
        _, farbe, motiv = name.split(":")
        return wappen(farbe, motiv).resize((px, px), Image.NEAREST)
    return icon16(name).resize((px, px), Image.NEAREST)


def hex_rgb(h):
    n = int(h.lstrip("#"), 16)
    return (n >> 16 & 255, n >> 8 & 255, n & 255)


def _lum(rgb):
    return (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255


@functools.lru_cache(maxsize=None)
def wappen(farbe_hex, motiv):
    """Wappen 16x16 wie drawEmblem auf der Konzeptseite."""
    c = hex_rgb(farbe_hex)
    dunkel = tuple(max(0, min(255, round(v * .68))) for v in c)
    rand = (38, 30, 46)
    hell = _lum(c) > .62
    fg = (38, 30, 46) if hell else (245, 248, 255)
    fg2 = (90, 80, 100) if hell else (190, 200, 215)
    bild = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = bild.load()
    for y, z in enumerate(clan_icons.SCHILD):
        for x, ch in enumerate(z):
            if ch != "." and x + 1 < 16 and y + 1 < 16:
                px[x + 1, y + 1] = (18, 16, 26, 110)
    for y, z in enumerate(clan_icons.SCHILD):
        for x, ch in enumerate(z):
            if ch == "k":
                px[x, y] = rand + (255,)
            elif ch == "F":
                px[x, y] = c + (255,)
            elif ch == "f":
                px[x, y] = dunkel + (255,)
    ox, oy = clan_icons.MOTIV_POS[motiv]
    for y, z in enumerate(clan_icons.MOTIVE[motiv]):
        for x, ch in enumerate(z):
            if ch == "#":
                px[ox + x, oy + y] = fg + (255,)
            elif ch == "+":
                px[ox + x, oy + y] = fg2 + (255,)
    return bild


@functools.lru_cache(maxsize=None)
def wappen_zeichen(farbe_hex, motiv, S):
    """Schriftzeichen 8x8 (Tablist/Chat), wie drawGlyph."""
    c = hex_rgb(farbe_hex)
    d = tuple(max(0, min(255, round(v * .7))) for v in c)
    g = clan_icons.GLYPHE[motiv]
    oy = max(0, (8 - len(g)) // 2)
    bild = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    px = bild.load()
    for y, z in enumerate(g):
        for x, ch in enumerate(z):
            if ch in "#+":
                px[x, y + oy] = (c if ch == "#" else d) + (255,)
    return bild.resize((8 * S, 8 * S), Image.NEAREST)


# ── Menue ───────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=None)
def menue_hintergrund(reihen, S):
    bg = Image.open(os.path.join(CONNECTOR, "font", "gui_bg_%d.png" % reihen)).convert("RGBA")
    bg = bg.crop((0, 0, 176, 17 + 18 * reihen + 1))
    return bg.resize((bg.width * S, bg.height * S), Image.NEAREST)


def slot_xy(slot):
    """Linke obere Ecke des Items in GUI-Pixeln."""
    return 8 + 18 * (slot % 9), 18 + 18 * (slot // 9)


def menue_bild(titel, reihen, slots, S):
    """slots: {platz: iconname}. Gibt das Menue als Bild zurueck."""
    bild = menue_hintergrund(reihen, S).copy()
    zeichne_text(bild, 8 * S, 6 * S, titel, S, schatten=False)
    for platz, name in slots.items():
        x, y = slot_xy(platz)
        einfuegen(bild, icon(name, 16 * S), x * S, y * S)
    return bild


def slot_markierung(S):
    return Image.new("RGBA", (16 * S, 16 * S), (255, 255, 255, 110))


# ── Tooltip ─────────────────────────────────────────────────────────────────

def tooltip_bild(zeilen, S):
    """Klassischer Tooltip: dunkler Grund, lila Verlaufsrahmen. zeilen[0] ist der Name."""
    w = max(breite(z) for z in zeilen)
    h = 8 if len(zeilen) == 1 else 10 * len(zeilen)
    bw, bh = w + 8, h + 8
    bild = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(bild)
    grund = (16, 0, 16, 240)
    d.rectangle((1, 0, bw - 2, bh - 1), fill=grund)
    d.rectangle((0, 1, bw - 1, bh - 2), fill=grund)
    oben, unten = (80, 0, 255), (40, 0, 127)
    for y in range(1, bh - 1):
        t = (y - 1) / max(1, bh - 3)
        c = tuple(round(oben[i] + (unten[i] - oben[i]) * t) for i in range(3))
        for x in (1, bw - 2):
            _mische(bild, x, y, c, 80)
    for x in range(1, bw - 1):
        _mische(bild, x, 1, oben, 80)
        _mische(bild, x, bh - 2, unten, 80)
    bild = bild.resize((bw * S, bh * S), Image.NEAREST)
    y = 4
    for i, z in enumerate(zeilen):
        zeichne_text(bild, 4 * S, y * S, z, S)
        y += 12 if i == 0 else 10
    return bild


def _mische(bild, x, y, rgb, a):
    r0, g0, b0, a0 = bild.getpixel((x, y))
    f = a / 255
    bild.putpixel((x, y), (round(r0 * (1 - f) + rgb[0] * f), round(g0 * (1 - f) + rgb[1] * f), round(b0 * (1 - f) + rgb[2] * f), a0))


# ── Mauszeiger ──────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=None)
def mauszeiger(groesse=44):
    """Pfeil wie unter macOS: schwarz mit weissem Rand, weich gezeichnet."""
    k = 4
    form = [(0, 0), (0, 15.5), (3.6, 12.2), (6.2, 18), (8.6, 17), (6.1, 11.4), (11, 11.4)]
    s = groesse / 18
    big = Image.new("RGBA", (int(groesse * 1.0 + 8) * k, int(groesse * 1.15 + 8) * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    pts = [((x * s + 3) * k, (y * s + 3) * k) for x, y in form]
    schatten = [((x * s + 5) * k, (y * s + 6) * k) for x, y in form]
    d.polygon(schatten, fill=(0, 0, 0, 70))
    d.polygon(pts, fill=(255, 255, 255, 255))
    innen = _schrumpfe(form, 1.25 / s * s)
    d.polygon([((x * s + 3) * k, (y * s + 3) * k) for x, y in innen], fill=(0, 0, 0, 255))
    return big.resize((big.width // k, big.height // k), Image.LANCZOS)


def _schrumpfe(form, um):
    """Polygon grob nach innen versetzen (Schwerpunkt-Skalierung)."""
    cx = sum(p[0] for p in form) / len(form)
    cy = sum(p[1] for p in form) / len(form)
    out = []
    for x, y in form:
        dx, dy = x - cx, y - cy
        l = (dx * dx + dy * dy) ** .5 or 1
        f = max(0, (l - um) / l)
        out.append((cx + dx * f, cy + dy * f))
    return out


# ── Chat ────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=256)
def chat_zeile_bild(text, S, breite_gui=320, deck=115):
    """Eine Chatzeile mit halbdurchsichtigem Grund, 9 GUI-Pixel hoch."""
    bild = Image.new("RGBA", (breite_gui * S, 9 * S), (0, 0, 0, deck))
    zeichne_text(bild, 1 * S, 1 * S, text, S)
    return bild


_WAPPEN_ZEICHEN = {}


def wappen_char(farbe_hex, motiv):
    """Wappen als Schriftzeichen (8x8, Vorschub 9) fuer Chat und Tablist.
    Davor muss weiss stehen (§f), sonst faerbt der Client es ein - wie im Spiel."""
    key = (farbe_hex, motiv)
    if key not in _WAPPEN_ZEICHEN:
        ch = chr(0xF100 + len(_WAPPEN_ZEICHEN))
        GLYPHEN[ch] = Glyphe(wappen_zeichen(farbe_hex, motiv, 1), 9, 0, farbig=True)
        _WAPPEN_ZEICHEN[key] = ch
    return _WAPPEN_ZEICHEN[key]


@functools.lru_cache(maxsize=None)
def hud_bild(name):
    for ordner in (os.path.join(CONNECTOR, "font"), os.path.join(MANAGER, "font")):
        pfad = os.path.join(ordner, name + ".png")
        if os.path.exists(pfad):
            return Image.open(pfad).convert("RGBA")
    raise KeyError("HUD-Bild fehlt: " + name)


def balken_bild(breite_gui, anteil, S, fuellung="bar_fill64"):
    """HUD-Balken aus bar_track/bar_fill (6 GUI-Pixel hoch)."""
    bild = Image.new("RGBA", (breite_gui, 6), (0, 0, 0, 0))
    spur, voll = hud_bild("bar_track64"), hud_bild(fuellung) if isinstance(fuellung, str) else fuellung
    x = 0
    while x < breite_gui:
        bild.alpha_composite(spur.crop((0, 0, min(64, breite_gui - x), 6)), (x, 0))
        x += 64
    fb = int(round(breite_gui * max(0.0, min(1.0, anteil))))
    x = 0
    while x < fb:
        bild.alpha_composite(voll.crop((0, 0, min(64, fb - x), 6)), (x, 0))
        x += 64
    return bild.resize((breite_gui * S, 6 * S), Image.NEAREST)


@functools.lru_cache(maxsize=None)
def gefaerbt(name, rgb):
    """bar_fill in anderer Farbe (Helligkeit bleibt)."""
    src = hud_bild(name)
    grau = src.convert("L")
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    px, g, a = out.load(), grau.load(), src.getchannel("A").load()
    for y in range(src.height):
        for x in range(src.width):
            f = g[x, y] / 160
            px[x, y] = tuple(max(0, min(255, int(c * f))) for c in rgb) + (a[x, y],)
    return out


def pille_bild(breite_gui, S):
    """HUD-Pille (16 GUI-Pixel hoch) aus hud_pill_left/mid/right."""
    links, rechts, mitte = hud_bild("hud_pill_left"), hud_bild("hud_pill_right"), hud_bild("hud_pill_mid1")
    bild = Image.new("RGBA", (breite_gui, 16), (0, 0, 0, 0))
    bild.alpha_composite(links, (0, 0))
    for x in range(links.width, breite_gui - rechts.width):
        bild.alpha_composite(mitte, (x, 0))
    bild.alpha_composite(rechts, (breite_gui - rechts.width, 0))
    return bild.resize((breite_gui * S, 16 * S), Image.NEAREST)
