#!/usr/bin/env python3
"""Ankuendigungs-Trailer fuer MegaBuild Sky - schneller Teaser in WQHD (2560 x 1440).

Kaltstart mit Text auf Schwarz, dann Beat (120 BPM) und Biom-Schnitte im Takt,
Feature-Einblendungen, die Figuren, ein zweiter schneller Block, Malas Abschied
und das neue MB-Logo mit Beta-Hinweis. Alle Schnitte liegen auf Zaehlzeiten
(0,5 s), die Musik setzt bei 4,0 s ein.

Die Bilder sind die Shader-Originale (2940 px breit) in trailer-bilder/, damit
WQHD ohne Hochskalieren scharf bleibt.

    python3 bauen.py trailer --crf 16 [--sprache en]
"""
import functools
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

TW, TH = 2560, 1440  # Ausgabegroesse dieses Films
K = TW / 1920  # Faktor gegenueber dem 1080p-Raster der anderen Filme
BILDER = os.path.join(HIER, "trailer-bilder")
BALKEN = 150  # Kinobalken oben und unten
SCHLAG = .5  # 120 BPM
MB_LOGO = Image.open(os.path.join(os.environ.get("MBLOGO", os.path.expanduser("~/Coding/MBLogo")),
                                  "mblogo-wortmarke-1024.png")).convert("RGBA")
BETA_LINK = "megabuild.de/dc"
LILA = (201, 133, 255)
HELL = (255, 250, 255)
SANFT = (221, 210, 238)


# ── Bausteine ───────────────────────────────────────────────────────────────

def blende(t, d, ein=.5, aus=.5):
    """Ein- und Ausblenden einer Szene (aus Schwarz, nach Schwarz)."""
    a = aus_kubisch(phase(t, 0, ein)) if ein > 0 else 1.0
    b = 1 - ein_kubisch(phase(t, d - aus, d)) if aus > 0 else 1.0
    return min(a, b)


@functools.lru_cache(maxsize=12)
def quelle(name):
    """Shader-Original auf 16:9 beschnitten, in voller Aufloesung."""
    img = Image.open(os.path.join(BILDER, name + ".webp")).convert("RGB")
    h = min(img.height, round(img.width * 9 / 16))
    w = round(h * 16 / 9)
    x0, y0 = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x0, y0, x0 + w, y0 + h))


def vollbild(e, name, t, d, z=(1.0, 1.04), fx=(0.0, 0.0), fy=0.0, alpha=1.0, stoss=0.0):
    """Bild randlos: Zoom z von->bis, Bildmitte fx (von->bis) und fy in -1..1.

    stoss > 0 laesst den Schnitt mit einem kurzen Zoom-Ruck einsetzen (peppiger).
    Der Ausschnitt geht in einem Schritt aus dem Original auf 2560 x 1440."""
    if alpha <= .003:
        return
    src = quelle(name)
    u = phase(t, 0, d)
    zoom = z[0] + (z[1] - z[0]) * u + stoss * (1 - aus_kubisch(phase(t, 0, .35)))
    bw, bh = src.width / zoom, src.height / zoom
    mx = fx[0] + (fx[1] - fx[0]) * u
    ox = (src.width - bw) * (.5 + .5 * mx)
    oy = (src.height - bh) * (.5 + .5 * fy)
    aus = src.resize((TW, TH), Image.LANCZOS, box=(ox, oy, ox + bw, oy + bh))
    aus = aus.filter(ImageFilter.UnsharpMask(radius=1.4, percent=40, threshold=2))
    mc.einfuegen(e, aus.convert("RGBA"), 0, 0, alpha)


def _vignette():
    k = 8
    m = Image.new("L", (TW // k, TH // k), 0)
    ImageDraw.Draw(m).ellipse((-TW // k * .15, -TH // k * .25, TW // k * 1.15, TH // k * 1.25), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(30)).resize((TW, TH), Image.BILINEAR)
    out = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    out.putalpha(m.point(lambda v: int((255 - v) * .7)))
    return out


VIGNETTE = _vignette()
WEISS = Image.new("RGBA", (TW, TH), (255, 255, 255, 255))


def blitz(e, t, staerke=.45, dauer=.16):
    """Kurzer heller Blitz am Schnitt."""
    a = staerke * (1 - phase(t, 0, dauer))
    if a > .003:
        mc.einfuegen(e, WEISS, 0, 0, a)


def bauchbinde(e, t, t0, titel, unter=None, alpha=1.0):
    """Grosse Einblendung unten links: Titel in gesperrten Grossbuchstaben, Zeile darunter."""
    u = aus_kubisch(phase(t, t0, t0 + .3)) * alpha
    if u <= .003:
        return
    x, y = 150, TH - BALKEN - 250
    balken = Image.new("RGBA", (int(10 * u) + 1, 150), LILA + (255,))
    mc.einfuegen(e, balken, x, y, u)
    dx = -30 * (1 - u)
    av(e, titel.upper(), x + 44 + dx, y - 6, 66, "heavy", HELL, u, schatten=.75, sperrung=5)
    if unter:
        u2 = aus_kubisch(phase(t, t0 + .12, t0 + .42)) * alpha
        av(e, unter, x + 46 + dx, y + 86, 42, "medium", SANFT, u2, schatten=.75)


def staub(e, t, alpha=1.0, n=40, farbe=(255, 214, 150), seed=3):
    """Aufsteigende Leuchtpunkte."""
    rnd = random.Random(seed)
    for i in range(n):
        x0, ph, v, gr = rnd.uniform(0, TW), rnd.uniform(0, 1), rnd.uniform(.05, .14), rnd.uniform(8, 22)
        u = (ph + t * v) % 1.0
        x = x0 + 50 * math.sin(t * .7 + i)
        y = TH - BALKEN - u * (TH - 2 * BALKEN) * 1.1
        mc.einfuegen(e, glanz(int(gr), farbe, 160), x - gr, y - gr, alpha * math.sin(math.pi * u) * .9)


@functools.lru_cache(maxsize=1)
def _buehne():
    """Dunkler Lila-Hintergrund mit Lichtkegel (Farben von megabuild.de)."""
    k = 8
    img = Image.new("RGB", (TW // k, TH // k), (23, 13, 41))
    licht = Image.new("L", img.size, 0)
    ImageDraw.Draw(licht).ellipse((img.width * .15, img.height * .05, img.width * .85, img.height * 1.1), fill=255)
    licht = licht.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", img.size, (66, 43, 108)), img, licht)
    return img.resize((TW, TH), Image.BILINEAR).convert("RGBA")


def zeilen_punch(e, t, zeilen, y, groessen, farben, takte):
    """Zeilen, die nacheinander auf den Beat ins Bild springen."""
    for z, g, f, t0 in zip(zeilen, groessen, farben, takte):
        u = rueckschwung(phase(t, t0, t0 + .28))
        if u <= 0:
            continue
        b, rand, breite = av_bild(z, g, "heavy", f, .5, int(g * .08))
        s = .7 + .3 * u
        skaliert(e, b, TW / 2, y + b.height / 2 - rand, b.width * s, b.height * s, alpha=min(1, u), glatt=True)
        y += g * 1.25


# ── Szenen ──────────────────────────────────────────────────────────────────

def szene_kalt(e, t, d):
    a1 = aus_kubisch(phase(t, .3, 1.0)) * (1 - phase(t, 1.6, 1.9))
    av(e, L("Es war lange still.", "It's been quiet for a while."), TW / 2, TH / 2 - 50, 72, "medium", SANFT, a1,
       anker="m", schatten=0)
    a2 = aus_kubisch(phase(t, 2.1, 2.5)) * (1 - phase(t, 3.6, 3.95))
    av(e, L("Zu still.", "Too quiet."), TW / 2, TH / 2 - 60, 96, "heavy", HELL, a2, anker="m", schatten=0)


def schnitt(name, z=(1.0, 1.05), fx=(0.0, 0.0), fy=0.0, stoss=.06, titel=None, unter=None, staerke=.4):
    def zeichne(e, t, d):
        vollbild(e, name, t, d, z=z, fx=fx, fy=fy, stoss=stoss)
        mc.einfuegen(e, VIGNETTE, 0, 0, .65)
        if titel:
            bauchbinde(e, t, .12, titel, unter)
        blitz(e, t, staerke)
    return zeichne


def szene_titel(e, t, d):
    a = 1 - ein_kubisch(phase(t, d - .2, d))
    ebene = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    mc.einfuegen(ebene, glanz(700, (169, 88, 255), int(60 * phase(t, 0, .5))), TW / 2 - 700, TH / 2 - 700, 1)
    zeilen_punch(ebene, t, [L("WIR ARBEITEN WIEDER AN", "WE'RE WORKING ON"), L("ETWAS GROSSEM.", "SOMETHING BIG.")],
                 TH / 2 - 150, [80, 150], [SANFT, HELL], [0, SCHLAG * 2])
    mc.einfuegen(e, ebene, 0, 0, a)


FIGUREN = [  # Sprite, Name, Zeile, Groesse (1080p-Raster)
    ("goblin_talk", "Goblins", L("reden mit dir im Chat", "chat with you"), 300),
    ("shroom_hello", L("Shroomlinge", "Shroomlings"), L("arbeiten und handeln", "work and trade"), 300),
    ("forest_oak_happy", L("Forestlinge", "Forestlings"), L("schenken dir ihren Segen", "grant you blessings"), 270),
    ("warpett_idle", "Warpetts", L("bringen dich überall hin", "carry you anywhere"), 300),
]


def szene_figuren(e, t, d):
    a = blende(t, d, ein=.1, aus=.15)
    mc.einfuegen(e, _buehne(), 0, 0, a)
    staub(e, t, a * .5, n=24, farbe=(230, 200, 255))
    u = aus_kubisch(phase(t, 0, .3)) * a
    av(e, L("KI-BEWOHNER, DIE MIT DIR LEBEN", "AI RESIDENTS WHO LIVE WITH YOU"), TW / 2, BALKEN + 60, 54, "heavy",
       HELL, u, anker="m", schatten=.4, sperrung=6)
    boden = 1000
    for i, (sp, name, zeile, gr) in enumerate(FIGUREN):
        x = TW / 2 + (i - 1.5) * 560
        g = rueckschwung(phase(t, .1 + i * SCHLAG, .45 + i * SCHLAG))
        if g <= 0:
            continue
        schatten(e, x, boden, 260 * g, .8 * a)
        sprite_boden(e, sp, t, x, boden, gr * K * max(.01, g), a)
        v = aus_kubisch(phase(t, .25 + i * SCHLAG, .55 + i * SCHLAG)) * a
        av(e, name.upper(), x, boden + 40, 46, "heavy", HELL, v, anker="m", schatten=.5, sperrung=5)
        av(e, zeile, x, boden + 106, 34, "medium", LILA, v, anker="m", schatten=.4)
    pip = "§fPip §b(KI)§7: §f" + L("Hallo! Bist du neu hier oben?", "Hello! Are you new up here?")
    v = aus_kubisch(phase(t, 2.2, 2.5)) * a
    b = mc.chat_zeile_bild(pip, 4)
    mc.einfuegen(e, b, TW / 2 - b.width / 2, BALKEN + 170, v)


def szene_abschied(e, t, d):
    a = blende(t, d, ein=.15, aus=.6)
    vollbild(e, "ballon-abendrot", t, d, z=(1.0, 1.09), fx=(.25, -.1), alpha=a)
    staub(e, t, a * .8)
    mc.einfuegen(e, VIGNETTE, 0, 0, a * .8)


def szene_logo(e, t, d):
    g = aus_kubisch(phase(t, .02, .7))
    lw = 1000 * (1.08 - .08 * g)
    cy = 470
    mc.einfuegen(e, glanz(520, (169, 88, 255), int(70 * g)), TW / 2 - 520, cy - 520, 1)
    skaliert(e, MB_LOGO, TW / 2, cy, lw, lw, alpha=g, glatt=True)
    funkenkranz(e, TW / 2, cy, t, .05, radius=400, n=8, farbe=(230, 200, 255), groesse=24)
    u = aus_kubisch(phase(t, .5, 1.0))
    av(e, "MEGABUILD SKY", TW / 2, 760 + 14 * (1 - u), 88, "heavy", HELL, u, anker="m", sperrung=18)
    u2 = rueckschwung(phase(t, 1.0, 1.4))
    if u2 > 0:
        p = abzeichen(L("BETA  ·  BALD", "BETA  ·  SOON"), farbe=(140, 255, 184), text_farbe=(180, 255, 210))
        skaliert(e, p, TW / 2, 915, p.width * 1.75 * u2, p.height * 1.75 * u2, glatt=True)
    u3 = aus_kubisch(phase(t, 1.6, 2.1))
    av(e, L("Jetzt für die Beta anmelden", "Sign up for the beta now"), TW / 2, 1010, 54, "demi", HELL, u3, anker="m")
    av(e, BETA_LINK + "   ·   Java & Bedrock", TW / 2, 1090, 42, "medium", LILA, u3, anker="m")


# ── Film ────────────────────────────────────────────────────────────────────

def untertitel_gross(e, text, alpha, S=4):
    """Malas Untertitel im unteren Kinobalken (wie im Spiel: Name in Aqua)."""
    if alpha <= .003 or not text:
        return
    zeilen = mc_umbruch("§f" + text, 300)
    zeilen[0] = "§bMala§7: " + zeilen[0]
    hoehe = len(zeilen) * 11 * S
    y0 = TH - BALKEN / 2 - hoehe / 2
    for i, z in enumerate(zeilen):
        mct(e, TW / 2, y0 + i * 11 * S, z, S, alpha, anker="m")


class Trailer(Film):
    """Film in eigener Groesse, ohne Seitenbeschriftung und Fortschrittsbalken, mit Kinobalken."""

    groesse = (TW, TH)
    whoosh = False  # Rausch-Whooshes zwischen den Szenen passen nicht zum Trailer

    def bild(self, t):
        f = Image.new("RGBA", (TW, TH), (0, 0, 0, 255))
        sz, lt = self.szene_bei(t)
        ebene = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
        sz["zeichne"](ebene, lt, sz["dauer"])
        f.alpha_composite(ebene)
        schwarz = Image.new("RGBA", (TW, BALKEN), (0, 0, 0, 255))
        f.alpha_composite(schwarz, (0, 0))
        f.alpha_composite(schwarz, (0, TH - BALKEN))
        aktuell = [u for u in self.untertitel if u[0] - .2 <= t < u[1] + .3]
        if aktuell:
            t0, t1, text = aktuell[-1]
            untertitel_gross(f, text, aus_kubisch(phase(t, t0 - .2, t0)) * (1 - phase(t, t1, t1 + .3)))
        return f


# Erster schneller Block: ein Schnitt je zwei Schlaege
BLOCK1 = [
    ("ballon-abendrot", (1.0, 1.06), (.2, -.2)),
    ("kirschhain", (1.08, 1.0), (0, .2)),
    ("pilzland-nacht", (1.0, 1.07), (-.3, .1)),
    ("rankenbruecken", (1.07, 1.0), (.2, -.2)),
    ("wuestenhaus", (1.0, 1.06), (0, .3)),
    ("dschungelinsel", (1.06, 1.0), (.3, 0)),
    ("blasser-garten", (1.0, 1.07), (-.2, .2)),
    ("wald", (1.07, 1.0), (0, -.2)),
]

FEATURES = [  # Bild, Titel, Zeile, Zoom, Schwenk
    ("kirschhain", L("Deine eigene Inselwelt", "Your own island world"),
     L("auf einem eigenen Server – mit bis zu 25 Freunden", "on a server of its own – with up to 25 friends"),
     (1.0, 1.08), (-.3, .3)),
    ("rankenbruecken", L("Eine Welt, die wächst", "A world that grows"),
     L("neue Inseln entstehen beim Erkunden", "new islands appear as you explore"), (1.08, 1.0), (.3, -.3)),
    ("pilzland-nacht", L("Custom-Biome", "Custom biomes"),
     L("mit Mana im Skilltree freischalten", "unlocked with Mana in the skill tree"), (1.0, 1.08), (.3, -.2)),
    ("wuestenhaus", L("Dörfer, Ruinen, Höhlen", "Villages, ruins, caves"),
     L("und Erze, die sich lohnen", "and ores worth mining"), (1.08, 1.0), (-.2, .3)),
    ("blasser-garten", L("Quests & Erfolge", "Quests & achievements"),
     L("jeden Tag etwas Neues", "something new every day"), (1.0, 1.08), (.2, -.2)),
    ("wald", L("Java & Bedrock", "Java & Bedrock"),
     L("zusammen auf einem Server", "together on one server"), (1.08, 1.0), (-.3, .2)),
]

# Zweiter Block: Detailausschnitte, ein Schnitt je Schlag (Zoom bis 1,15 bleibt ohne Hochskalieren)
BLOCK2 = [
    ("pilzland-nacht", .4, .1), ("kirschhain", -.2, -.6), ("dschungelinsel", -.5, -.2), ("wuestenhaus", .3, -.4),
    ("rankenbruecken", .1, .2), ("ballon-abendrot", -.1, -.7), ("wald", .5, .3), ("blasser-garten", 0, -.2),
]

SZENEN = [dict(dauer=4.0, zeichne=szene_kalt, ton=[(2.0, "sfx:swell", .7)])]
SZENEN += [dict(dauer=2 * SCHLAG, zeichne=schnitt(n, z=z, fx=fx)) for n, z, fx in BLOCK1]
SZENEN[1]["ton"] = [(0, "sfx:boom", .9), (.5, "mala:island")]
SZENEN += [dict(dauer=4 * SCHLAG, zeichne=szene_titel, ton=[(0, "sfx:boom", 1.1), (1.0, "sfx:boom", .8)])]
SZENEN += [dict(dauer=4 * SCHLAG, zeichne=schnitt(n, z=z, fx=fx, stoss=.04, titel=ti, unter=un, staerke=.25))
           for n, ti, un, z, fx in FEATURES]
SZENEN += [dict(dauer=8 * SCHLAG, zeichne=szene_figuren,
                ton=[(.1 + i * SCHLAG, "sfx:pop", .6) for i in range(4)] + [(2.2, "pool:goblin/frage_1", .6)])]
SZENEN += [dict(dauer=SCHLAG, zeichne=schnitt(n, z=(1.15, 1.12), fx=(x, x), fy=y, stoss=.05, staerke=.5))
           for n, x, y in BLOCK2]
SZENEN += [dict(dauer=10 * SCHLAG, zeichne=szene_abschied,
                ton=[(0, "sfx:boom", .7), (.3, "mala:farewell"), (3.0, "sfx:swell", .9)])]
SZENEN += [dict(dauer=16 * SCHLAG, zeichne=szene_logo,
                ton=[(0, "sfx:boom", 1.3), (.05, "sfx:chime", .7), (1.0, "sfx:erfolg", .6)])]

_ende_beat = sum(sz["dauer"] for sz in SZENEN[:-2])  # Beat bis zum Abschied
_logo = sum(sz["dauer"] for sz in SZENEN[:-1])
FILM = Trailer("trailer", SZENEN, wortmarke=False,
               musik=dict(tonart="D", tempo=120, stimmung="hell", ab=4.0, ende=_logo, beat=True, beat_bis=_ende_beat))
FILM.poster = 4.0 + 12 * 2 * SCHLAG + 1.2  # mitten in der ersten Feature-Einblendung
