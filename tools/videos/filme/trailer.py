#!/usr/bin/env python3
"""Ankuendigungs-Trailer fuer MegaBuild Sky - schneller Teaser in WQHD (2560 x 1440).

Kaltstart auf Schwarz mit Herzschlag und Mala, Drop in die Musik (komponiert mit ElevenLabs Music, trailer_musik.py),
drei Biom-Bilder, Titeltafel, fuenf Feature-Einblendungen, die Figuren, eine
Stille vor dem Logo und das neue MB-Logo mit Beta-Hinweis. Jedes Bild kommt nur
einmal vor. Malas Zeilen sind eigene Trailer-Aufnahmen (stimmen/, nicht im Spiel).
Nur auf Deutsch. Alle Schnitte liegen auf Zaehlzeiten
(0,5 s), der Drop liegt bei 8,0 s.

Die Bilder sind die Shader-Originale (2940 px breit) in trailer-bilder/, damit
WQHD ohne Hochskalieren scharf bleibt.

    python3 trailer_stimme.py      # Malas Trailer-Zeilen (stimmen/texte.json), nur bei neuen Texten
    python3 bauen.py trailer --crf 16
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


@functools.lru_cache(maxsize=1)
def _bauchbinden_schatten():
    """Weicher dunkler Fleck unten links, damit die Einblendung auch auf hellen Bildern lesbar bleibt."""
    k = 8
    m = Image.new("L", (TW // k, TH // k), 0)
    ImageDraw.Draw(m).ellipse((-TW // k * .25, TH // k * .5, TW // k * .62, TH // k * 1.2), fill=170)
    m = m.filter(ImageFilter.GaussianBlur(28)).resize((TW, TH), Image.BILINEAR)
    out = Image.new("RGBA", (TW, TH), (6, 4, 14, 0))
    out.putalpha(m)
    return out


def bauchbinde(e, t, t0, titel, unter=None, alpha=1.0):
    """Grosse Einblendung unten links: Titel in gesperrten Grossbuchstaben, Zeile darunter."""
    u = aus_kubisch(phase(t, t0, t0 + .3)) * alpha
    if u <= .003:
        return
    x, y = 150, TH - BALKEN - 250
    mc.einfuegen(e, _bauchbinden_schatten(), 0, 0, u)
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

def puls(schlaege):
    """Schwarzes Bild mit violettem Lichtpuls auf jedem Herzschlag (Spannung vor dem Drop)."""
    def zeichne(e, t, d):
        st = 0.0
        for t0 in schlaege:
            if t >= t0:
                st = max(st, math.exp(-(t - t0) / .35))
        st *= 1 - ein_kubisch(phase(t, d - .15, d))
        if st > .01:
            r = int(520 + 160 * st)
            mc.einfuegen(e, glanz(r, (169, 88, 255), int(140 * st)), TW / 2 - r, TH / 2 - r, 1)
    return zeichne


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


PIP_CHAT = [  # (Zeit in der Szene, Zeile)
    (.9, "§7Du → Pip: Hey Pip, was machst du gerade?"),
    (1.8, "§fPip §b(KI)§7: §fIch ernte Weizen! Willst du handeln?"),
    (3.0, "§7Du → Pip: handeln"),
    (3.8, "§fPip §b(KI)§7: §fGern! Soll ich dir 16 Brot backen? Du zahlst in Mana."),
    (5.6, "§fPip §b(KI)§7: §fUnd hast du 64 Bruchstein? Die brauch ich für unseren Brunnen."),
]
KANN = [  # Hinweise unter den Figuren
    ("SCHREIBEN IM CHAT", (120, 220, 255)),
    ("HANDELN MIT MANA & WARE", (140, 255, 184)),
    ("AUFTRÄGE & TAUSCH", (255, 210, 90)),
    ("VERTRAUEN AUFBAUEN", (230, 160, 255)),
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
    # Chat wie im Spiel: "Du → Pip" grau, die Antwort als "Pip (KI)" (siehe sb/bewohner.md)
    zeilen = chatzeilen([(t0, txt) for t0, txt in PIP_CHAT])
    sichtbar = [(t0, z) for t0, z in zeilen if t >= t0][-6:]
    y = BALKEN + 140
    for t0, z in sichtbar:
        v = aus_kubisch(phase(t, t0, t0 + .25)) * a
        b = mc.chat_zeile_bild(z, 5)
        mc.einfuegen(e, b, TW / 2 - b.width / 2, y + 12 * (1 - v), v)
        y += b.height
    # Was Bewohner koennen - im Takt, als eigene Reihe (gehoert zu allen, nicht zu einer Figur)
    pillen = [abzeichen(text, farbe=f, text_farbe=tuple(min(255, c + 40) for c in f)) for text, f in KANN]
    luecke, faktor = 36, 1.3
    x = TW / 2 - (sum(p_.width * faktor for p_ in pillen) + luecke * (len(pillen) - 1)) / 2
    for i, p_ in enumerate(pillen):
        w = p_.width * faktor
        v = rueckschwung(phase(t, 2.4 + i * SCHLAG, 2.75 + i * SCHLAG))
        if v > 0:
            skaliert(e, p_, x + w / 2, 1180, w * v, p_.height * faktor * v, alpha=a, glatt=True)
        x += w + luecke


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
    """Malas Untertitel im unteren Kinobalken: erste Zeile der Name (Aqua), darunter ihr Text."""
    if alpha <= .003 or not text:
        return
    zeilen = ["§bMala"] + mc_umbruch("§f" + text, 300)
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
        if sz is self.szenen[-1]:  # am Ende weich ins Schwarz
            mc.einfuegen(f, ebene, 0, 0, 1 - ein_aus(phase(lt, sz["dauer"] - 1.6, sz["dauer"])))
        else:
            f.alpha_composite(ebene)
        schwarz = Image.new("RGBA", (TW, BALKEN), (0, 0, 0, 255))
        f.alpha_composite(schwarz, (0, 0))
        f.alpha_composite(schwarz, (0, TH - BALKEN))
        aktuell = [u for u in self.untertitel if u[0] - .2 <= t < u[1] + .3]
        if aktuell:
            t0, t1, text = aktuell[-1]
            untertitel_gross(f, text, aus_kubisch(phase(t, t0 - .2, t0)) * (1 - phase(t, t1, t1 + .3)))
        return f


# Jedes Bild kommt genau einmal vor (es gibt neun Shader-Aufnahmen). Mala erzaehlt durchgehend:
# jede Szene hat ihre Zeile, die Laenge der Feature-Szenen richtet sich nach Malas Satz.
AUFTAKT = [
    ("ballon-abendrot", (1.0, 1.06), (.2, -.2)),
    ("kirschhain", (1.08, 1.0), (0, .2)),
    ("rankenbruecken", (1.0, 1.07), (-.2, .2)),
]

FEATURES = [  # Bild, Titel, Zeile, Zoom, Schwenk, Malas Zeile, Schlaege
    ("dschungelinsel", L("Deine eigene Inselwelt", "Your own island world"),
     L("auf einem eigenen Server – mit bis zu 25 Freunden", "on a server of its own – with up to 25 friends"),
     (1.0, 1.08), (-.3, .3), "trailer-server", 8),
    ("blasser-garten", L("Eine Welt, die wächst", "A world that grows"),
     L("neue Inseln entstehen beim Erkunden", "new islands appear as you explore"), (1.08, 1.0), (.3, -.3),
     "trailer-waechst", 7),
    ("pilzland-nacht", L("Custom-Biome", "Custom biomes"),
     L("mit Mana im Skilltree freischalten", "unlocked with Mana in the skill tree"), (1.0, 1.08), (.3, -.2),
     "trailer-biome", 8),
    ("wuestenhaus", L("Dörfer, Ruinen, Höhlen", "Villages, ruins, caves"),
     L("Quests und Erfolge an jeder Ecke", "quests and achievements everywhere"), (1.08, 1.0), (-.2, .3),
     "trailer-doerfer", 11),
    ("wald", L("Java & Bedrock", "Java & Bedrock"),
     L("zusammen auf einem Server", "together on one server"), (1.0, 1.08), (-.3, .2), "trailer-zusammen", 12),
]

# Kaltstart: ein Einschlag, alles bricht weg, Leere. Dann Herzschlag, Mala leise, eine Atempause,
# "Man hat sich geirrt." - und erst danach der Drop.
KALT = 9.0
HERZ1 = [2.3, 3.3, 4.3, 5.25, 6.1, 6.85, 7.5, 8.05, 8.5]
SZENEN = [dict(dauer=KALT, zeichne=puls([0.0] + HERZ1),  # Einschlag auch im Bild
               ton=[(0, "datei:musik/trailer-leere.mp3", 1.0)] + [(t, "sfx:herz", .9) for t in HERZ1]
               + [(2.2, "mala:trailer-nichts"), (6.4, "mala:trailer-geirrt")])]
SZENEN += [dict(dauer=4 * SCHLAG, zeichne=schnitt(n, z=z, fx=fx, stoss=.04, staerke=.45)) for n, z, fx in AUFTAKT]
SZENEN[1]["ton"] = [(0, "sfx:boom", 1.2), (.3, "mala:trailer-inseln")]
SZENEN += [dict(dauer=4 * SCHLAG, zeichne=szene_titel, ton=[(0, "sfx:boom", 1.1), (1.0, "sfx:boom", .8)])]
SZENEN += [dict(dauer=n_schlag * SCHLAG, zeichne=schnitt(n, z=z, fx=fx, stoss=.03, titel=ti, unter=un, staerke=.25),
                ton=[(.3, "mala:" + zeile)])
           for n, ti, un, z, fx, zeile, n_schlag in FEATURES]
SZENEN += [dict(dauer=18 * SCHLAG, zeichne=szene_figuren,
                ton=[(.1 + i * SCHLAG, "sfx:pop", .6) for i in range(4)]
                + [(t0, "pool:goblin/" + ("freude_1" if i == 1 else "frage_1"), .35)
                   for i, (t0, z) in enumerate(PIP_CHAT) if "(KI)" in z]
                + [(2.4 + i * SCHLAG, "sfx:pop", .4) for i in range(4)]
                + [(.8, "mala:trailer-handeln"), (5.1, "mala:trailer-allein")])]
# Stille vor dem Logo: die Musik blendet aus, Herzschlag, Mala fluestert
HERZ2 = [.25, 1.05, 1.75, 2.35, 2.85, 3.3, 3.65]
SZENEN += [dict(dauer=4.0, zeichne=puls(HERZ2),
                ton=[(t, "sfx:herz", .7) for t in HERZ2] + [(.9, "mala:trailer-bereit")])]
SZENEN += [dict(dauer=16 * SCHLAG, zeichne=szene_logo, ton=[(1.2, "mala:trailer-beta")])]

_stille = sum(sz["dauer"] for sz in SZENEN[:-2])  # Musik laeuft bis zur Stille vor dem Logo
# Das Hauptstueck (34 s) ist 12 s kuerzer als der Film bis zur Stille: nach 22 s geht es bei 10 s
# weiter, die Takte 10-22 s (sechs Takte) kommen also ein zweites Mal. Beide Schnittstellen liegen auf Taktgrenzen (120 BPM, 2-s-Takte).
_m0 = KALT - 6.0
_verlaengerung = _stille - _m0 - 34.0
assert abs(_verlaengerung - 12.0) < .01, f"Musik passt nicht: {_verlaengerung:.2f} s statt 12 s Verlaengerung"
_kurve_aus = [(0, 1.0), (24.0 - 3.0, 1.0), (24.0, 0.0)]  # vor der Stille weich ausblenden statt hart abbrechen
FILM = Trailer("trailer", SZENEN, wortmarke=False,
               musik=dict(art="dateien", pegel=.35, stuecke=[  # Musik bewusst leise: Stimme und Effekte vorn
                   # im Kaltstart leise unter Herzschlag und Mala, voll ab dem Drop
                   (_m0, "musik/trailer-haupt.mp3", [(0, .22), (5.5, .3), (6.0, 1.0)], (0, 22.04)),
                   (_m0 + 22.0, "musik/trailer-haupt.mp3", _kurve_aus, (10.0, 34.0)),
                   (_stille + 4.0, "musik/trailer-logo.mp3", [(0, .5)]),  # Logo-Schlag, gedaempft
               ]))
FILM.musik_hall = False  # die komponierte Musik bringt ihren Raum selbst mit
FILM.lautheit_linear = True  # sonst zieht loudnorm die leise gestellte Musik wieder hoch
FILM.ducken = .82  # die dichte Musik muss unter Malas Stimme deutlich leiser werden
FILM.poster = KALT + 6 * 2 * SCHLAG + 2 * SCHLAG + 1.5  # erste Feature-Einblendung
