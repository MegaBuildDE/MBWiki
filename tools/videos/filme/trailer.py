#!/usr/bin/env python3
"""Ankuendigungs-Trailer fuer MegaBuild Sky - im Stil eines Kino-Teasers.

Anders als die Feature-Filme: Kinobalken statt Beschriftung links, Screenshots
randlos, Malas Story-Zeilen als roter Faden (fall, magic, name, island,
resident-grow, farewell) und am Ende Logo und Beta-Hinweis.

    python3 bauen.py trailer [--sprache en]
"""
import functools
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

ASSETS = os.path.join(WIKI, ".gitbook", "assets")
SHOT = os.path.join(ASSETS, "screenshots")
ALT_HALLE = os.path.join(ASSETS, "2024-09-05_23.07.27.png")
BALKEN = 132  # Hoehe der Kinobalken oben und unten
# Das neue MB-Logo (Wortmarke mit Glow, transparent) aus dem MBLogo-Repo
MB_LOGO = Image.open(os.path.join(os.environ.get("MBLOGO", os.path.expanduser("~/Coding/MBLogo")),
                                   "mblogo-wortmarke-1024.png")).convert("RGBA")
BETA_LINK = "megabuild.de/dc"


def s(name):
    return os.path.join(SHOT, "mbsky-" + name + ".webp")


# ── Bausteine ───────────────────────────────────────────────────────────────

def blende(t, d, ein=.5, aus=.5):
    """Ein- und Ausblenden einer Szene (aus Schwarz, nach Schwarz)."""
    a = aus_kubisch(phase(t, 0, ein)) if ein > 0 else 1.0
    b = 1 - ein_kubisch(phase(t, d - aus, d)) if aus > 0 else 1.0
    return min(a, b)


@functools.lru_cache(maxsize=24)
def bild_quelle(pfad, art="normal"):
    """Screenshot in Originalgroesse, auf 16:9 beschnitten (alt: grau und dunkler)."""
    img = Image.open(pfad).convert("RGB")
    h = min(img.height, round(img.width * 9 / 16))
    w = round(h * 16 / 9)
    img = img.crop(((img.width - w) // 2, (img.height - h) // 2, (img.width - w) // 2 + w, (img.height - h) // 2 + h))
    if art == "alt":
        img = ImageOps.grayscale(img).convert("RGB")
        img = ImageEnhance.Brightness(img).enhance(.62)
        img = ImageEnhance.Contrast(img).enhance(1.15)
    return img


def vollbild(e, pfad, t, d, zoom=(1.0, 1.05), schwenk=(0.0, 0.0), alpha=1.0, art="normal"):
    """Screenshot randlos mit langsamem Zoom (Faktor von->bis) und Schwenk (-1..1 in x).

    Der Ausschnitt wird in einem Schritt aus dem Original auf 1920 x 1080 gebracht
    (Lanczos, leicht nachgeschaerft), damit das Bild scharf bleibt."""
    if alpha <= .003:
        return
    src = bild_quelle(pfad, art)
    u = ein_aus(phase(t, 0, d)) * .6 + phase(t, 0, d) * .4
    z = zoom[0] + (zoom[1] - zoom[0]) * u
    bw, bh = src.width / z, src.height / z
    sx = schwenk[0] + (schwenk[1] - schwenk[0]) * u
    ox = (src.width - bw) * (.5 + .5 * sx)
    oy = (src.height - bh) * .5
    aus = src.resize((W, H), Image.LANCZOS, box=(ox, oy, ox + bw, oy + bh))
    aus = aus.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))
    mc.einfuegen(e, aus.convert("RGBA"), 0, 0, alpha)


def vignette_bild():
    k = 8
    m = Image.new("L", (W // k, H // k), 0)
    ImageDraw.Draw(m).ellipse((-W // k * .15, -H // k * .25, W // k * 1.15, H // k * 1.25), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(26)).resize((W, H), Image.BILINEAR)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.putalpha(m.point(lambda v: int((255 - v) * .75)))
    return out


VIGNETTE = vignette_bild()


def bauchbinde(e, t, t0, text, unter=None, x=150, y=BALKEN + 70, alpha=1.0):
    """Kleine Zeile oben links im Bild, gesperrte Grossbuchstaben."""
    u = aus_kubisch(phase(t, t0, t0 + .45)) * alpha
    if u <= .003:
        return
    linie = Image.new("RGBA", (int(46 * u), 3), (201, 133, 255, 230))
    mc.einfuegen(e, linie, x, y + 17, u)
    av(e, text.upper(), x + 64 - 16 * (1 - u), y, 26, "demi", (255, 250, 255), u, schatten=.7, sperrung=4)
    if unter:
        av(e, unter, x + 64 - 16 * (1 - u), y + 44, 30, "medium", (221, 210, 238), u, schatten=.7)


def zitat(e, t, zeilen, y=H / 2 - 60, groesse=64, alpha=1.0, t0=.15):
    """Grosse weisse Zeilen in der Mitte (Texttafeln zwischen den Bildern)."""
    for i, z in enumerate(zeilen):
        u = aus_kubisch(phase(t, t0 + i * .35, t0 + .7 + i * .35)) * alpha
        av(e, z, W / 2, y + i * (groesse * 1.3) + 14 * (1 - u), groesse, "heavy" if i == 0 else "medium",
           (255, 255, 255) if i == 0 else (221, 210, 238), u, anker="m", schatten=.5)


def staub(e, t, alpha=1.0, n=34, farbe=(255, 214, 150), seed=3):
    """Aufsteigende Leuchtpunkte (Magie in den Rissen)."""
    rnd = random.Random(seed)
    for i in range(n):
        x0, ph, v, gr = rnd.uniform(0, W), rnd.uniform(0, 1), rnd.uniform(.05, .14), rnd.uniform(6, 18)
        u = (ph + t * v) % 1.0
        x = x0 + 40 * math.sin(t * .7 + i)
        y = H - BALKEN - u * (H - 2 * BALKEN) * 1.1
        a = alpha * math.sin(math.pi * u) * .9
        mc.einfuegen(e, glanz(int(gr), farbe, 160), x - gr, y - gr, a)


# ── Riss durch die alte Welt ────────────────────────────────────────────────

def _risslinie():
    rnd = random.Random(42)
    pts, y = [], -20
    x = W * .52
    while y < H + 40:
        pts.append((x, y))
        y += rnd.uniform(40, 110)
        x += rnd.uniform(-90, 90)
        x = max(W * .3, min(W * .7, x))
    return pts


RISS = _risslinie()


@functools.lru_cache(maxsize=2)
def _riss_masken():
    links = Image.new("L", (W, H), 0)
    ImageDraw.Draw(links).polygon([(0, 0)] + RISS + [(0, H)], fill=255)
    rechts = ImageOps.invert(links)
    return links, rechts


@functools.lru_cache(maxsize=1)
def _riss_leuchten():
    img = Image.new("L", (W, H), 0)
    ImageDraw.Draw(img).line(RISS, fill=255, width=10)
    weich = img.filter(ImageFilter.GaussianBlur(18))
    hart = img.filter(ImageFilter.GaussianBlur(2))
    out = Image.new("RGBA", (W, H), (255, 190, 255, 0))
    out.putalpha(Image.blend(weich, hart, .5).point(lambda v: min(255, v * 2)))
    return out


def szene_fall(e, t, d):
    a = blende(t, d, ein=1.4, aus=1.0)
    voll = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vollbild(voll, ALT_HALLE, t, d, zoom=(1.0, 1.05), art="alt")
    riss = phase(t, 4.1, 6.4)
    if riss <= 0:
        mc.einfuegen(e, voll, 0, 0, a)
    else:
        links, rechts = _riss_masken()
        off = 140 * aus_kubisch(riss)
        teil_l, teil_r = voll.copy(), voll.copy()
        teil_l.putalpha(links)
        teil_r.putalpha(rechts)
        mc.einfuegen(e, teil_l, -off, off * .35, a)
        mc.einfuegen(e, teil_r, off, -off * .35, a)
        mc.einfuegen(e, _riss_leuchten(), 0, 0, a * (1 - phase(t, 4.6, 6.6)) * min(1, riss * 6))
        staub(e, t, a * phase(t, 4.3, 5.2), n=20, farbe=(240, 170, 255))
    mc.einfuegen(e, VIGNETTE, 0, 0, a)
    if t < 4.0:
        bauchbinde(e, t, 1.6, "MegaBuild.de", L("Wie wir es kannten", "As we knew it"), alpha=1 - phase(t, 3.4, 3.9))


def szene_magie(e, t, d):
    a = blende(t, d, ein=.9, aus=.6)
    vollbild(e, s("ballon-abendrot"), t, d, zoom=(1.0, 1.06), schwenk=(.3, -.2), alpha=a)
    staub(e, t, a * .9)
    mc.einfuegen(e, VIGNETTE, 0, 0, a * .8)


def szene_mala(e, t, d):
    a = blende(t, d, ein=.4, aus=.5)
    if t < 3.4:
        vollbild(e, s("luftschiff"), t, 3.4, zoom=(1.05, 1.0), schwenk=(-.4, .2), alpha=a * (1 - phase(t, 3.1, 3.4)))
        mc.einfuegen(e, VIGNETTE, 0, 0, a * .7)
        return
    lt = t - 3.4
    hg = hintergrund(t).convert("RGBA")
    hg = ImageEnhance.Brightness(hg.convert("RGB")).enhance(.45).convert("RGBA")
    mc.einfuegen(e, hg, 0, 0, a * aus_kubisch(phase(lt, 0, .3)))
    g = rueckschwung(phase(lt, .05, .55))
    schatten(e, 1340, 880, 260 * g, .8 * a)
    sprite_boden(e, "mala_hello" if lt < 1.6 else "mala_idle", lt, 1340, 880, 560 * max(.01, g), a,
                 schleife=lt >= 1.6)
    u = aus_kubisch(phase(lt, .25, .8)) * a
    av(e, "MALA", 260 - 30 * (1 - u), 400, 150, "heavy", (255, 250, 255), u, schatten=.6, sperrung=10)
    u2 = aus_kubisch(phase(lt, .5, 1.05)) * a
    av(e, L("KAPITÄNIN DES LUFTSCHIFFS", "CAPTAIN OF THE AIRSHIP"), 268, 580, 30, "demi", (201, 133, 255), u2,
       schatten=.4, sperrung=6)


def szene_tafel(text, unter):
    def zeichne(e, t, d):
        zitat(e, t, [text, unter], alpha=blende(t, d, ein=.2, aus=.5))
    return zeichne


def szene_insel(e, t, d):
    a = blende(t, d, ein=.5, aus=.4)
    vollbild(e, s("dschungelinsel"), t, d, zoom=(1.07, 1.0), schwenk=(.5, 0), alpha=a)
    mc.einfuegen(e, VIGNETTE, 0, 0, a * .6)


def schnitt(name, titel, unter=None, zoom=(1.0, 1.04), schwenk=(-.3, .3)):
    def zeichne(e, t, d):
        a = blende(t, d, ein=.12, aus=.12)
        vollbild(e, s(name), t, d, zoom=zoom, schwenk=schwenk, alpha=a)
        mc.einfuegen(e, VIGNETTE, 0, 0, a * .6)
        bauchbinde(e, t, .2, titel, unter, alpha=a)
    return zeichne


FIGUREN = [  # Sprite, Name, Zeile, Groesse
    ("goblin_talk", L("Goblins", "Goblins"), L("KI-Bewohner", "AI residents"), 300),
    ("shroom_hello", L("Shroomlinge", "Shroomlings"), L("KI-Bewohner", "AI residents"), 300),
    ("forest_oak_happy", L("Forestlinge", "Forestlings"), L("scheue Waldelfen", "shy forest elves"), 260),
    ("warpett_idle", "Warpetts", L("bringen dich überall hin", "carry you anywhere"), 300),
]


def szene_figuren(e, t, d):
    a = blende(t, d, ein=.4, aus=.5)
    hg = ImageEnhance.Brightness(hintergrund(t + 30).convert("RGB")).enhance(.5).convert("RGBA")
    mc.einfuegen(e, hg, 0, 0, a)
    boden = 760
    for i, (sp, name, zeile, gr) in enumerate(FIGUREN):
        x = 330 + i * 420
        g = rueckschwung(phase(t, .4 + i * .9, .9 + i * .9))
        if g <= 0:
            continue
        schatten(e, x, boden, 200 * g, .8 * a)
        sprite_boden(e, sp, t, x, boden, gr * max(.01, g), a)
        u = aus_kubisch(phase(t, .6 + i * .9, 1.1 + i * .9)) * a
        av(e, name.upper(), x, boden + 34, 34, "heavy", (255, 250, 255), u, anker="m", schatten=.5, sperrung=4)
        av(e, zeile, x, boden + 84, 26, "medium", (201, 133, 255), u, anker="m", schatten=.4)
    pip = "§fPip §b(KI)§7: §f" + L("Hallo! Bist du neu hier oben?", "Hello! Are you new up here?")
    u = aus_kubisch(phase(t, 5.0, 5.4)) * a
    b = mc.chat_zeile_bild(pip, 3)
    mc.einfuegen(e, b, W / 2 - b.width / 2, BALKEN + 50, u)


def szene_abschied(e, t, d):
    a = blende(t, d, ein=.5, aus=.9)
    vollbild(e, s("luftschiff"), t, d, zoom=(1.0, 1.08), schwenk=(0, 0), alpha=a)
    staub(e, t, a * .6, n=18)
    mc.einfuegen(e, VIGNETTE, 0, 0, a * .8)


def szene_logo(e, t, d):
    # Logo
    g = aus_kubisch(phase(t, .05, .9))
    lw = 760 * (1.06 - .06 * g)
    cy = 345
    mc.einfuegen(e, glanz(380, (169, 88, 255), int(70 * g)), W / 2 - 380, cy - 380, 1)
    skaliert(e, MB_LOGO, W / 2, cy, lw, lw, alpha=g, glatt=True)
    funkenkranz(e, W / 2, cy, t, .1, radius=300, n=8, farbe=(230, 200, 255))
    # Schriftzug
    u = aus_kubisch(phase(t, .7, 1.3))
    av(e, "MEGABUILD SKY", W / 2, 560 + 12 * (1 - u), 64, "heavy", (255, 250, 255), u, anker="m", sperrung=14)
    # Beta
    u2 = rueckschwung(phase(t, 1.6, 2.1))
    if u2 > 0:
        p = abzeichen(L("BETA  ·  BALD", "BETA  ·  SOON"), farbe=(140, 255, 184), text_farbe=(180, 255, 210))
        skaliert(e, p, W / 2, 680, p.width * 1.3 * u2, p.height * 1.3 * u2, glatt=True)
    u3 = aus_kubisch(phase(t, 2.6, 3.2))
    av(e, L("Jetzt für die Beta anmelden", "Sign up for the beta now"), W / 2, 760, 40, "demi", (255, 250, 255), u3,
       anker="m")
    av(e, BETA_LINK + "   ·   Java & Bedrock", W / 2, 822, 32, "medium", (201, 133, 255), u3, anker="m")


class Trailer(Film):
    """Film ohne Seitenbeschriftung und Fortschrittsbalken, dafuer mit Kinobalken."""

    def bild(self, t):
        f = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        sz, lt = self.szene_bei(t)
        ebene = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sz["zeichne"](ebene, lt, sz["dauer"])
        f.alpha_composite(ebene)
        schwarz = Image.new("RGBA", (W, BALKEN), (0, 0, 0, 255))
        f.alpha_composite(schwarz, (0, 0))
        f.alpha_composite(schwarz, (0, H - BALKEN))
        # Immer nur ein Stueck zeigen: das neueste, das schon begonnen hat
        aktuell = [u for u in self.untertitel if u[0] - .2 <= t < u[1] + .3]
        if aktuell:
            t0, t1, text = aktuell[-1]
            u = aus_kubisch(phase(t, t0 - .2, t0)) * (1 - phase(t, t1, t1 + .3))
            untertitel(f, text, u, y=H - 34, S=3)
        return f


SZENEN = [
    dict(dauer=7.5, zeichne=szene_fall, ton=[(1.3, "mala:fall"), (4.1, "sfx:boom", 1.2)]),
    dict(dauer=7.0, zeichne=szene_magie, ton=[(.5, "mala:magic"), (1.0, "sfx:funkeln", .4)]),
    dict(dauer=7.5, zeichne=szene_mala, ton=[(.4, "mala:name"), (3.4, "sfx:boom", .5)]),
    dict(dauer=4.0, zeichne=szene_tafel(L("Wir bauen etwas Neues.", "We're building something new."),
                                        L("Eine Welt aus Inseln über den Wolken.", "A world of islands above the clouds.")),
         ton=[(.1, "sfx:boom", 1.0)]),
    dict(dauer=6.0, zeichne=szene_insel, ton=[(.4, "mala:island")]),
    dict(dauer=2.2, zeichne=schnitt("kirschhain", L("Deine eigene Inselwelt", "Your own island world"),
                                    L("auf einem eigenen Server", "on a server of its own"))),
    dict(dauer=2.2, zeichne=schnitt("rankenbruecken", L("Eine Welt, die wächst", "A world that grows"),
                                    L("neue Inseln entstehen beim Erkunden", "new islands appear as you explore"),
                                    schwenk=(.3, -.3))),
    dict(dauer=2.2, zeichne=schnitt("pilzland-nacht", L("Custom-Biome", "Custom biomes"),
                                    L("mit Mana im Skilltree freischalten", "unlocked with Mana in the skill tree"))),
    dict(dauer=2.2, zeichne=schnitt("wuestenhaus", L("Dörfer, Ruinen, Höhlen", "Villages, ruins, caves"),
                                    L("und Erze, die sich lohnen", "and ores worth mining"), schwenk=(.3, -.3))),
    dict(dauer=2.2, zeichne=schnitt("blasser-garten", L("Quests & Erfolge", "Quests & achievements"),
                                    L("jeden Tag etwas Neues", "something new every day"))),
    dict(dauer=2.6, zeichne=schnitt("wald", L("Java & Bedrock", "Java & Bedrock"),
                                    L("zusammen auf einem Server", "together on one server"), schwenk=(.3, -.3)),
),
    dict(dauer=9.5, zeichne=szene_figuren,
         ton=[(.0, "sfx:boom", .8), (.6, "mala:resident-grow")]
         + [(.4 + i * .9, "sfx:pop", .5) for i in range(4)] + [(5.0, "pool:goblin/frage_1", .6)]),
    dict(dauer=6.5, zeichne=szene_abschied, ton=[(.4, "mala:farewell"), (4.6, "sfx:swell", .8)]),
    dict(dauer=8.5, zeichne=szene_logo, ton=[(.0, "sfx:boom", 1.3), (.1, "sfx:chime", .7), (1.6, "sfx:erfolg", .6)]),
]

FILM = Trailer("trailer", SZENEN, musik=dict(tonart="D", tempo=66, stimmung="dunkel"), wortmarke=False)
FILM.whoosh = False  # die Rausch-Whooshes zwischen den Szenen passen nicht zum Trailer
FILM.poster = sum(sz["dauer"] for sz in SZENEN[:2]) + 4.0
