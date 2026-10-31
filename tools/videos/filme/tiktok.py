#!/usr/bin/env python3
"""TikTok-Fassung des Ankuendigungs-Trailers - Hochformat 1080 x 1920, rund 27 s.

Kein ruhiger Kaltstart wie im Trailer: TikTok entscheidet in den ersten zwei Sekunden.
Darum steigt der Film direkt mit dem Besonderen ein - KI-Bewohner, die im Chat
antworten - und die Musik setzt sofort beim Drop ein. Danach kurz der Titel,
vier schnelle Bilder mit Malas Zeilen und am Ende Logo und Beta-Hinweis.

Alles Wichtige liegt in der sicheren Zone: Handys mit 19,5:9 schneiden links und
rechts je ~100 px ab, dazu verdeckt die TikTok-Oberflaeche oben ~180 px, unten
~380 px und rechts die Knoepfe. Im ersten Bild steht die Ueberschrift schon da. Bilder, Stimmen und
Musik sind dieselben wie im Trailer (trailer-bilder/, stimmen/, musik/).

    python3 bauen.py tiktok --crf 18
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

TW, TH = 1080, 1920  # Hochformat
BILDER = os.path.join(HIER, "trailer-bilder")
SCHLAG = .5  # 120 BPM wie die Trailer-Musik
MB_LOGO = Image.open(os.path.join(os.environ.get("MBLOGO", os.path.expanduser("~/Coding/MBLogo")),
                                  "mblogo-wortmarke-1024.png")).convert("RGBA")
BETA_LINK = "megabuild.de/dc"
LILA = (201, 133, 255)
HELL = (255, 250, 255)
SANFT = (221, 210, 238)
MITTE_X = 480  # Mitte der sicheren Zone (rechts liegen TikToks Knoepfe)
TEXT_BREITE = 620  # 160..800 px - bleibt auch bei beschnittenem Bild lesbar
UNTERTITEL_Y = 1450


# ── Bausteine ───────────────────────────────────────────────────────────────

def blende(t, d, ein=.5, aus=.5):
    a = aus_kubisch(phase(t, 0, ein)) if ein > 0 else 1.0
    b = 1 - ein_kubisch(phase(t, d - aus, d)) if aus > 0 else 1.0
    return min(a, b)


@functools.lru_cache(maxsize=8)
def quelle(name, fx=0.0):
    """Shader-Original auf 9:16 beschnitten (fx verschiebt den Ausschnitt, -1..1)."""
    img = Image.open(os.path.join(BILDER, name + ".webp")).convert("RGB")
    h = img.height
    w = round(h * 9 / 16)
    x0 = (img.width - w) * (.5 + .5 * fx)
    return img.crop((round(x0), 0, round(x0) + w, h))


def vollbild(e, name, t, d, z=(1.0, 1.06), fx=0.0, stoss=0.0):
    src = quelle(name, fx)
    u = phase(t, 0, d)
    zoom = z[0] + (z[1] - z[0]) * u + stoss * (1 - aus_kubisch(phase(t, 0, .35)))
    bw, bh = src.width / zoom, src.height / zoom
    ox, oy = (src.width - bw) / 2, (src.height - bh) / 2
    aus = src.resize((TW, TH), Image.LANCZOS, box=(ox, oy, ox + bw, oy + bh))
    aus = aus.filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2))
    mc.einfuegen(e, aus.convert("RGBA"), 0, 0)


@functools.lru_cache(maxsize=1)
def _verlauf():
    """Abdunkelung oben und in der unteren Haelfte, damit Text auf hellen Bildern lesbar bleibt."""
    m = Image.new("L", (1, TH), 0)
    for y in range(TH):
        v = max(0.0, 1 - y / 420) * 150 + max(0.0, (y - 900) / 700) * 190
        m.putpixel((0, y), int(min(220, v)))
    out = Image.new("RGBA", (TW, TH), (8, 4, 18, 0))
    out.putalpha(m.resize((TW, TH)))
    return out


WEISS = Image.new("RGBA", (TW, TH), (255, 255, 255, 255))


def blitz(e, t, staerke=.4, dauer=.16):
    a = staerke * (1 - phase(t, 0, dauer))
    if a > .003:
        mc.einfuegen(e, WEISS, 0, 0, a)


def passend(text, groesse, gewicht="heavy", sperrung=0, maxb=TEXT_BREITE):
    """Schriftgroesse so weit verkleinern, dass der Text in die sichere Zone passt."""
    while groesse > 30 and textbreite(text, groesse, gewicht, sperrung) > maxb:
        groesse -= 2
    return groesse


def punch(e, t, t0, text, y, groesse, farbe, gewicht="heavy", sperrung=0):
    """Zeile springt auf den Schlag ins Bild."""
    u = rueckschwung(phase(t, t0, t0 + .28))
    if u <= 0:
        return
    g = passend(text, groesse, gewicht, sperrung)
    b, rand, breite = av_bild(text, g, gewicht, farbe, .7, sperrung)
    s = .7 + .3 * u
    skaliert(e, b, MITTE_X, y + b.height / 2 - rand, b.width * s, b.height * s, alpha=min(1, u), glatt=True)


def staub(e, t, alpha=1.0, n=30, farbe=(230, 200, 255), seed=3):
    rnd = random.Random(seed)
    for i in range(n):
        x0, ph, v, gr = rnd.uniform(0, TW), rnd.uniform(0, 1), rnd.uniform(.05, .14), rnd.uniform(6, 18)
        u = (ph + t * v) % 1.0
        x = x0 + 40 * math.sin(t * .7 + i)
        y = TH - u * TH * 1.1
        mc.einfuegen(e, glanz(int(gr), farbe, 160), x - gr, y - gr, alpha * math.sin(math.pi * u) * .9)


@functools.lru_cache(maxsize=1)
def _buehne():
    """Dunkler Lila-Hintergrund mit Lichtkegel (Farben von megabuild.de)."""
    k = 8
    img = Image.new("RGB", (TW // k, TH // k), (23, 13, 41))
    licht = Image.new("L", img.size, 0)
    ImageDraw.Draw(licht).ellipse((-img.width * .2, img.height * .25, img.width * 1.2, img.height * .95), fill=255)
    licht = licht.filter(ImageFilter.GaussianBlur(30))
    img = Image.composite(Image.new("RGB", img.size, (66, 43, 108)), img, licht)
    return img.resize((TW, TH), Image.BILINEAR).convert("RGBA")


# ── Szenen ──────────────────────────────────────────────────────────────────

CHAT = [  # (Zeit in der Szene, Zeile) - wie im Spiel, siehe sb/bewohner.md
    (.25, "§7Du → Pip: Hey Pip, was machst du gerade?"),
    (.95, "§fPip §b(KI)§7: §fIch ernte Weizen! Willst du handeln?"),
    (2.0, "§7Du → Pip: handeln"),
    (2.6, "§fPip §b(KI)§7: §fGern! 16 Brot gegen Mana?"),
    (3.9, "§fPip §b(KI)§7: §fUnd hast du 64 Bruchstein für unseren Brunnen?"),
]


def szene_haken(e, t, d):
    """Der Aufhaenger: vom ersten Bild an Text, Figuren und ein Chat, der antwortet."""
    a = blende(t, d, ein=0, aus=.15)
    mc.einfuegen(e, _buehne(), 0, 0, a)
    staub(e, t, a * .5)
    punch(e, t, -1.0, "MINECRAFT-BEWOHNER,", 230, 84, SANFT)  # ab dem ersten Bild da
    punch(e, t, -1.0, "DIE MIT DIR CHATTEN", 320, 96, HELL)
    zeilen = chatzeilen(CHAT, breite_gui=150)
    y = 520
    for t0, z in [(t0, z) for t0, z in zeilen if t >= t0][-10:]:
        v = aus_kubisch(phase(t, t0, t0 + .2)) * a
        b = mc.chat_zeile_bild(z, 4, breite_gui=154)
        mc.einfuegen(e, b, MITTE_X - b.width / 2, y + 10 * (1 - v), v)
        y += b.height
    boden = 1360
    for i, (sp, x, gr) in enumerate([("goblin_talk", MITTE_X - 170, 360), ("shroom_hello", MITTE_X + 170, 340)]):
        g = 1.0 if i == 0 else rueckschwung(phase(t, .1, .45))  # Pip steht von Anfang an da
        if g > 0:
            schatten(e, x, boden, 200 * g, .8 * a)
            sprite_boden(e, sp, t, x, boden, gr * max(.01, g), a)
    if t >= 4.6:  # "(KI)" als Abzeichen - das ist der Punkt
        p = abzeichen("ECHTE KI-ANTWORTEN", farbe=(120, 220, 255), text_farbe=(170, 235, 255))
        v = rueckschwung(phase(t, 4.6, 4.95))
        skaliert(e, p, MITTE_X, 455, p.width * 1.4 * v, p.height * 1.4 * v, alpha=a, glatt=True)


def szene_titel(e, t, d):
    a = 1 - ein_kubisch(phase(t, d - .2, d))
    ebene = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    mc.einfuegen(ebene, glanz(560, (169, 88, 255), int(70 * phase(t, 0, .4))), MITTE_X - 560, TH / 2 - 640, 1)
    punch(ebene, t, 0.0, "MEGABUILD SKY", TH / 2 - 190, 120, HELL, sperrung=8)
    punch(ebene, t, SCHLAG * 2, "CUSTOM SKYBLOCK", TH / 2 - 30, 70, LILA, sperrung=6)
    mc.einfuegen(e, ebene, 0, 0, a)


def schnitt(name, zeilen, unter, fx=0.0, z=(1.0, 1.07)):
    def zeichne(e, t, d):
        vollbild(e, name, t, d, z=z, fx=fx, stoss=.05)
        mc.einfuegen(e, _verlauf(), 0, 0)
        y = 1020
        for i, zeile in enumerate(zeilen):
            punch(e, t, .1 + i * .18, zeile, y, 104, HELL, sperrung=3)
            y += 118
        u = aus_kubisch(phase(t, .5, .8))
        g = passend(unter, 50, "medium")
        av(e, unter, MITTE_X, y + 14 + 12 * (1 - u), g, "medium", SANFT, u, anker="m", schatten=.8)
        balken = Image.new("RGBA", (int(220 * u) + 1, 8), LILA + (255,))
        mc.einfuegen(e, balken, MITTE_X - balken.width / 2, 990, u)
        blitz(e, t)
    return zeichne


def szene_logo(e, t, d):
    g = aus_kubisch(phase(t, .02, .7))
    lw = 560 * (1.08 - .08 * g)
    cy = 520
    mc.einfuegen(e, glanz(420, (169, 88, 255), int(70 * g)), MITTE_X - 420, cy - 420, 1)
    skaliert(e, MB_LOGO, MITTE_X, cy, lw, lw, alpha=g, glatt=True)
    funkenkranz(e, MITTE_X, cy, t, .05, radius=240, n=8, farbe=(230, 200, 255), groesse=20)
    u = aus_kubisch(phase(t, .4, .9))
    av(e, "MEGABUILD SKY", MITTE_X, 830 + 14 * (1 - u), passend("MEGABUILD SKY", 84, sperrung=12), "heavy", HELL, u,
       anker="m", sperrung=12)
    u2 = rueckschwung(phase(t, .8, 1.2))
    if u2 > 0:
        p = abzeichen("BETA  ·  BALD", farbe=(140, 255, 184), text_farbe=(180, 255, 210))
        skaliert(e, p, MITTE_X, 975, p.width * 1.5 * u2, p.height * 1.5 * u2, glatt=True)
    u3 = aus_kubisch(phase(t, 1.3, 1.8))
    av(e, "Jetzt für die Beta anmelden", MITTE_X, 1060, passend("Jetzt für die Beta anmelden", 54, "demi"), "demi", HELL, u3, anker="m")
    av(e, BETA_LINK, MITTE_X, 1140, passend(BETA_LINK, 62), "heavy", LILA, u3, anker="m")
    av(e, "Java & Bedrock", MITTE_X, 1226, 42, "medium", SANFT, u3, anker="m")


# ── Film ────────────────────────────────────────────────────────────────────

def untertitel_hoch(e, text, alpha, S=4):
    """Malas Untertitel: erste Zeile der Name (Aqua), darunter ihr Text, in der sicheren Zone."""
    if alpha <= .003 or not text:
        return
    zeilen = ["§bMala"] + mc_umbruch("§f" + text, 150)
    hoehe = len(zeilen) * 11 * S
    y0 = UNTERTITEL_Y - hoehe / 2
    deck = Image.new("RGBA", (int(160 * S), int(hoehe + 6 * S)), (0, 0, 0, 110))
    mc.einfuegen(e, deck, MITTE_X - deck.width / 2, y0 - 4 * S, alpha)
    for i, z in enumerate(zeilen):
        mct(e, MITTE_X, y0 + i * 11 * S, z, S, alpha, anker="m")


class TikTok(Film):
    """Hochformat ohne Wortmarke, Seitenbeschriftung und Fortschrittsbalken."""

    groesse = (TW, TH)
    whoosh = False

    def bild(self, t):
        f = Image.new("RGBA", (TW, TH), (0, 0, 0, 255))
        sz, lt = self.szene_bei(t)
        ebene = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
        sz["zeichne"](ebene, lt, sz["dauer"])
        if sz is self.szenen[-1]:  # am Ende weich ins Schwarz
            mc.einfuegen(f, ebene, 0, 0, 1 - ein_aus(phase(lt, sz["dauer"] - 1.0, sz["dauer"])))
        else:
            f.alpha_composite(ebene)
        aktuell = [u for u in self.untertitel if u[0] - .2 <= t < u[1] + .3]
        if aktuell:
            t0, t1, text = aktuell[-1]
            untertitel_hoch(f, text, aus_kubisch(phase(t, t0 - .2, t0)) * (1 - phase(t, t1, t1 + .3)))
        return f


FEATURES = [  # Bild, Titelzeilen, Unterzeile, Ausschnitt, Malas Zeile, Schlaege
    ("dschungelinsel", ["DEINE INSEL.", "DEIN SERVER."], "mit bis zu 25 Freunden", -.2, "trailer-server", 7),
    ("pilzland-nacht", ["CUSTOM-", "BIOME"], "mit Mana im Skilltree freischalten", .3, "trailer-biome", 7),
    ("blasser-garten", ["DIE WELT", "WÄCHST MIT"], "neue Inseln beim Erkunden", 0.0, "trailer-waechst", 6),
    ("wald", ["JAVA &", "BEDROCK"], "zusammen auf einem Server", -.3, "trailer-zusammen", 9),
]

HAKEN = 12 * SCHLAG
SZENEN = [dict(dauer=HAKEN, zeichne=szene_haken,
               ton=[(0, "sfx:boom", 1.0)] + [(.1 + i * SCHLAG, "sfx:pop", .6) for i in range(2)]
               + [(t0, "pool:goblin/" + ("freude_1" if i == 1 else "frage_1"), .35)
                  for i, (t0, z) in enumerate(CHAT) if "(KI)" in z]
               + [(4.6, "sfx:pop", .5), (1.6, "mala:trailer-handeln")])]
SZENEN += [dict(dauer=4 * SCHLAG, zeichne=szene_titel, ton=[(0, "sfx:boom", 1.1), (1.0, "sfx:boom", .7)])]
SZENEN += [dict(dauer=n * SCHLAG, zeichne=schnitt(bild, zeilen, unter, fx), ton=[(0, "sfx:boom", .6),
                                                                                  (.35, "mala:" + zeile)])
           for bild, zeilen, unter, fx, zeile, n in FEATURES]
SZENEN += [dict(dauer=11 * SCHLAG, zeichne=szene_logo, ton=[(.9, "mala:trailer-beta")])]

_logo = sum(sz["dauer"] for sz in SZENEN[:-1])
FILM = TikTok("tiktok", SZENEN, wortmarke=False,
              musik=dict(art="dateien", pegel=.42, stuecke=[
                  # sofort ab dem Drop (6 s ins Hauptstueck), vor dem Logo weich aus
                  (0, "musik/trailer-haupt.mp3", [(0, 1.0), (_logo - 1.0, 1.0), (_logo + .3, 0.0)],
                   (6.0, 6.0 + _logo + .5)),
                  (_logo, "musik/trailer-logo.mp3", [(0, .55)]),
              ]))
FILM.musik_hall = False
FILM.lautheit_linear = True
FILM.ducken = .8
FILM.poster = 3.2  # Chat mit Pips Antwort - zeigt sofort, worum es geht
