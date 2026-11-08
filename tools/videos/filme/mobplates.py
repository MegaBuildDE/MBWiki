#!/usr/bin/env python3
"""Mobplates auf MegaBuild Skyblock: Mobs einfangen und woanders wieder freisetzen.

Inhalt nach MBSkyManager/docs/MOBPLATES.md (Stand 04.11.2026). Die Plates kommen bei jedem
Bau frisch aus dem Pool (assets/items/mobplates), Ziegel, Scherben, Herzen und Hotbar aus dem
Client-Jar. Der Enderman hat 20 Herzen und zeigt deshalb den Mana-Apfel. Mala erklaert jede
Szene (nur Deutsch).

    python3 bauen.py mobplates
"""
import functools
import glob
import io
import math
import os
import random
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

PLATES = os.path.join(mc.POOL, "assets", "items", "mobplates")
PINK = (255, 105, 200)
SCHERBEN = ["angler", "archer", "arms_up", "blade", "brewer", "burn", "danger", "explorer"]


@functools.lru_cache(maxsize=None)
def plate(name):
    """Bild aus dem Pool: leer und scherbe aus den Vorlagen, sonst die gefuellte Plate."""
    datei = {"leer": "vorlagen/mob_template", "scherbe": "vorlagen/mob_pre_template"}.get(name, name)
    return Image.open(os.path.join(PLATES, datei + ".png")).convert("RGBA")


@functools.lru_cache(maxsize=None)
def figur(name):
    """Nur die Figur einer Plate: alles, was von der leeren Vorlage abweicht."""
    bild, leer = plate(name), plate("leer")
    aus = Image.new("RGBA", bild.size, (0, 0, 0, 0))
    for y in range(bild.height):
        for x in range(bild.width):
            if bild.getpixel((x, y)) != leer.getpixel((x, y)):
                aus.putpixel((x, y), bild.getpixel((x, y)))
    return aus.crop(aus.getbbox())


@functools.lru_cache(maxsize=None)
def jar(pfad):
    """Textur aus dem neuesten Client-Jar, z. B. item/brick."""
    neuestes = max(glob.glob(os.path.expanduser("~/Library/Application Support/minecraft/versions/*/*.jar")),
                   key=os.path.getmtime)
    with zipfile.ZipFile(neuestes) as z:
        return Image.open(io.BytesIO(z.read("assets/minecraft/textures/" + pfad + ".png"))).convert("RGBA")


@functools.lru_cache(maxsize=None)
def insel(seed, gras=(88, 160, 64), gras_h=(118, 190, 82)):
    return insel_bild(13, 4, seed, 30, gras=gras, gras_h=gras_h, baum=False)


def buehne(e, cx, boden, alpha, seed=31, **farben):
    bild = insel(seed, **farben)
    mc.einfuegen(e, bild, cx - bild.width / 2, boden, alpha)


def mob(e, name, cx, boden, k, alpha=1.0, s=1.0):
    """Figur auf dem Boden, k Bildpunkte je Pixel, s skaliert fuers Erscheinen."""
    bild = figur(name)
    w, h = bild.width * k * s, bild.height * k * s
    if w >= 2 and h >= 2:
        schatten(e, cx, boden + 4, w * 1.1, .5 * alpha)
        skaliert(e, bild, cx, boden - h / 2, w, h, alpha)


def rot(name):
    """Die Figur beim Treffer."""
    bild = figur(name).copy()
    rote = Image.new("RGBA", bild.size, (255, 40, 40, 150))
    return Image.composite(Image.alpha_composite(bild, rote), bild, bild.getchannel("A"))


def funken(e, cx, unten, breite, hoehe, t, alpha, n=16):
    """Die pinken Partikel des markierten Mobs."""
    rnd = random.Random(7)
    for _ in range(n):
        versatz, tempo = rnd.random(), rnd.uniform(.45, .9)
        x = cx + rnd.uniform(-breite, breite)
        g = rnd.choice((10, 14, 18))
        u = (t * tempo + versatz) % 1
        mc.einfuegen(e, Image.new("RGBA", (g, g), PINK + (255,)), x, unten - u * hoehe, alpha * math.sin(math.pi * u))


def herzen(e, x, y, voll, alpha, S=4):
    """Zehn Herzen je Reihe, wie in der Anzeige des Spiels."""
    leer, herz = jar("gui/sprites/hud/heart/container"), jar("gui/sprites/hud/heart/full")
    for i in range(20):
        hx, hy = x + i % 10 * 8 * S, y + i // 10 * 10 * S
        skaliert(e, leer, hx + 4.5 * S, hy + 4.5 * S, 9 * S, alpha=alpha)
        if i < voll:
            skaliert(e, herz, hx + 4.5 * S, hy + 4.5 * S, 9 * S, alpha=alpha)


HOTBAR_X, HOTBAR_Y, HOTBAR_S = 966, 730, 4


def hotbar_mitte(i):
    return HOTBAR_X + (11 + 20 * i) * HOTBAR_S, HOTBAR_Y + 11 * HOTBAR_S


def hotbar(e, inhalt, alpha):
    bild = jar("gui/sprites/hud/hotbar")
    mc.einfuegen(e, bild.resize((bild.width * HOTBAR_S, bild.height * HOTBAR_S), Image.NEAREST), HOTBAR_X, HOTBAR_Y, alpha)
    for i, item in inhalt.items():
        mx, my = hotbar_mitte(i)
        skaliert(e, item, mx, my, 64, alpha=alpha)


def hand(e, x, y, item, alpha, druck=0.0):
    """Mauszeiger mit dem Gegenstand, den er haelt."""
    if item is not None:
        skaliert(e, item, x + 46, y + 46, 76, alpha=alpha)
    zeiger(e, x, y, alpha, druck)


def flug(e, item, von, nach, u, alpha, groesse=64):
    """Gegenstand im Bogen von einem Punkt zum anderen."""
    if 0 < u < 1:
        p = ein_aus(u)
        x = von[0] + (nach[0] - von[0]) * p
        y = von[1] + (nach[1] - von[1]) * p - 120 * math.sin(math.pi * p)
        skaliert(e, item, x, y, groesse, alpha=alpha)


def zeit_tafel(e, sekunden, alpha, x=1600, y=170):
    mc.einfuegen(e, tafel(230, 82, 14), x, y, alpha)
    rest = max(0, int(math.ceil(sekunden)))
    mct(e, x + 115, y + 22, f"§d{rest // 60:02d}:{rest % 60:02d}", 5, alpha, anker="m")


# ── Werkbank ────────────────────────────────────────────────────────────────

Z = 96


@functools.lru_cache(maxsize=None)
def slot_bild(g):
    b = Image.new("RGBA", (g, g), (139, 139, 139, 255))
    d = ImageDraw.Draw(b)
    d.rectangle((0, 0, g - 1, 4), fill=(55, 55, 55, 255))
    d.rectangle((0, 0, 4, g - 1), fill=(55, 55, 55, 255))
    d.rectangle((0, g - 5, g - 1, g - 1), fill=(255, 255, 255, 255))
    d.rectangle((g - 5, 0, g - 1, g - 1), fill=(255, 255, 255, 255))
    return b


RAND = [0, 1, 2, 5, 8, 7, 6, 3]
SCHRITT = .21


def werkbank(e, t, mitte, rund, ergebnis, name, ein, zeiten):
    """zeiten: wann die Mitte kommt, der Rand beginnt und das Ergebnis erscheint."""
    t_mitte, t_rund, fertig = zeiten
    x0, y0 = 930, 250
    mc.einfuegen(e, tafel(880, 400, 20), x0 - 50, y0 - 50, ein)
    for i in range(9):
        mc.einfuegen(e, slot_bild(Z), x0 + i % 3 * Z, y0 + i // 3 * Z, ein)
    s = rueckschwung(phase(t, t_mitte, t_mitte + .3))
    if s > 0:
        skaliert(e, mitte(t), x0 + Z + Z / 2, y0 + Z + Z / 2, 72 * s, alpha=ein)
    for k, i in enumerate(RAND):
        s = rueckschwung(phase(t, t_rund + k * SCHRITT, t_rund + k * SCHRITT + .3))
        if s > 0:
            skaliert(e, rund, x0 + i % 3 * Z + Z / 2, y0 + i // 3 * Z + Z / 2, 72 * s, alpha=ein)
    pfeil = Image.new("RGBA", (116, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(pfeil)
    d.rectangle((0, 22, 76, 37), fill=(190, 190, 190, 255))
    d.polygon([(76, 0), (115, 30), (76, 59)], fill=(190, 190, 190, 255))
    mc.einfuegen(e, pfeil, x0 + 3 * Z + 30, y0 + 1.5 * Z - 30, ein)
    ex, ey = x0 + 3 * Z + 190, y0 + Z / 2 - 12
    mc.einfuegen(e, slot_bild(Z + 24), ex, ey, ein)
    s = rueckschwung(phase(t, fertig, fertig + .4))
    if s > 0:
        mc.einfuegen(e, glanz(150, PINK, 150), ex + (Z + 24) / 2 - 150, ey + (Z + 24) / 2 - 150, ein)
        skaliert(e, ergebnis, ex + (Z + 24) / 2, ey + (Z + 24) / 2, 92 * s, alpha=ein)
        funkenkranz(e, ex + (Z + 24) / 2, ey + (Z + 24) / 2, t, fertig, radius=110, n=7, farbe=(255, 190, 235))
        mct(e, ex + (Z + 24) / 2, ey + Z + 56, name, 4, ein * aus_kubisch(phase(t, fertig + .2, fertig + .6)), anker="m")


def werkbank_ton(zeiten):
    t_mitte, t_rund, fertig = zeiten
    return [(t_mitte, "sfx:klick", .5)] + [(t_rund + k * SCHRITT, "sfx:klick", .5) for k in range(len(RAND))] + [(fertig, "sfx:funkeln")]


# ── Szenen ──────────────────────────────────────────────────────────────────

RUNDE = ["cat", "wolf", "horse", "villager", "creeper", "zombie", "sheep", "enderman", "pig", "cow", "skeleton", "chicken"]


def szene_intro(e, t, d):
    titelkarte(e, t, "Mobplates", "Mobs einfangen und woanders freisetzen", y=120)
    n = len(RUNDE)
    for i, name in enumerate(RUNDE):
        s = rueckschwung(phase(t, .8 + i * .1, 1.2 + i * .1))
        if s <= 0:
            continue
        w = math.pi * (i / n * 2 + .05) + t * .12
        x = W / 2 + math.cos(w) * 560
        y = 700 + math.sin(w) * 190 + 8 * math.sin(t * 2 + i)
        skaliert(e, plate(name), x, y, 104 * s)
    s = rueckschwung(phase(t, 1.5, 2.0))
    if s > 0:
        mc.einfuegen(e, glanz(190, PINK, 150), W / 2 - 190, 700 - 190)
        skaliert(e, plate("leer"), W / 2, 700 + 8 * math.sin(t * 2), 192 * s)


ZEITEN_SCHERBE = (3.4, 4.9, 7.0)
ZEITEN_PLATE = (3.0, 4.2, 6.4)


def szene_scherbe(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    scherbe = lambda z: jar(f"item/{SCHERBEN[int(z / .7) % len(SCHERBEN)]}_pottery_sherd")  # noqa: E731
    werkbank(e, t, scherbe, jar("item/brick"), plate("scherbe"), "§dBlasse Scherbe", ein, ZEITEN_SCHERBE)
    mct(e, 930, 690, "§fTöpferscherbe §7– jede geht – und §f8 Ziegel", 4, ein * aus_kubisch(phase(t, 2.6, 3.1)))


def szene_plate(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    werkbank(e, t, lambda z: plate("scherbe"), mc.icon16("mana_orb"), plate("leer"), "§dMobplate", ein, ZEITEN_PLATE)
    mct(e, 930, 690, "§fBlasse Scherbe §7und §d8 Mana-Kugeln", 4, ein * aus_kubisch(phase(t, 2.3, 2.8)))


CX, BODEN = 1330, 600
KLICK_M = 2.0


def szene_markieren(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN, ein)
    mob(e, "enderman", CX, BODEN, 30, ein)
    if t >= KLICK_M:
        funken(e, CX, BODEN, 110, 320, t, ein)
        funkenkranz(e, CX, BODEN - 150, t, KLICK_M, radius=130, n=8, farbe=(255, 190, 235))
        zeit_tafel(e, 600 - (t - KLICK_M), ein * aus_kubisch(phase(t, KLICK_M + .2, KLICK_M + .6)))
    x, y = zeigerweg(t, [(.3, 1720, 720), (KLICK_M, CX + 30, BODEN - 170), (KLICK_M + 1.0, 1640, 660)])
    hand(e, x, y, plate("leer") if t < KLICK_M else None, ein * (1 - phase(t, KLICK_M + .6, KLICK_M + 1.0)),
         1 - phase(t, KLICK_M, KLICK_M + .2) if t >= KLICK_M else 0)
    klick(e, t, KLICK_M, CX + 30, BODEN - 170, ein)
    chat(e, 880, 905, chatzeilen([(KLICK_M + .3, "§dMarkiert! §7Töte den Mob innerhalb von §f10 Minuten§7, dann füllt sich "
                                                 "deine Plate. Ein Mana-Apfel nimmt ihm vorher die Hälfte seiner Herzen.")]),
         t, 3, ein)


KLICK_A = 2.9


def szene_apfel(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN, ein)
    mob(e, "enderman", CX, BODEN, 30, ein)
    funken(e, CX, BODEN, 110, 320, t, ein)
    voll = 20 - int(round(10 * ein_aus(phase(t, KLICK_A + .7, KLICK_A + 1.7))))
    herzen(e, CX - 160, 150, voll, ein)
    mct(e, CX, 110, f"§f{voll} Herzen", 4, ein, anker="m")
    x, y = zeigerweg(t, [(.3, 1720, 720), (KLICK_A, CX + 30, BODEN - 170), (KLICK_A + 1.0, 1640, 660)])
    hand(e, x, y, mc.icon16("mana_apple") if t < KLICK_A else None, ein * (1 - phase(t, KLICK_A + .6, KLICK_A + 1.0)))
    klick(e, t, KLICK_A, CX + 30, BODEN - 170, ein)
    chat(e, 880, 905, chatzeilen([(KLICK_A + .8, "§dGeschwächt! §7Der Mob hat nur noch die Hälfte seiner Herzen.")]), t, 3, ein)


TOD = 2.4


def szene_fangen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN - 100, ein)
    boden = BODEN - 100
    if t < TOD:
        treffer = any(z <= t < z + .18 for z in (1.0, 1.6, 2.2))
        if treffer:
            bild = rot("enderman")
            skaliert(e, bild, CX, boden - bild.height * 15, bild.width * 30, bild.height * 30, ein)
        else:
            mob(e, "enderman", CX, boden, 30, ein)
        funken(e, CX, boden, 110, 320, t, ein)
    else:
        u = phase(t, TOD, TOD + .4)
        mob(e, "enderman", CX, boden, 30, ein * (1 - u), 1 - .4 * u)
        funkenkranz(e, CX, boden - 120, t, TOD, radius=120, n=8, farbe=(255, 190, 235))
        s = rueckschwung(phase(t, TOD + .1, TOD + .5))
        if s > 0:
            skaliert(e, jar("item/ender_pearl"), CX - 90, boden - 40 + 6 * math.sin(t * 3), 64 * s, alpha=ein)
            mct(e, CX - 90, boden - 110, "§7Beute", 3, ein * aus_kubisch(phase(t, TOD + 3.4, TOD + 3.8)), anker="m")
    x, y = zeigerweg(t, [(.3, 1720, 620), (.9, CX + 60, boden - 160), (TOD, CX + 60, boden - 160), (TOD + .8, 1720, 620)])
    if t < TOD + .8:
        hand(e, x, y, jar("item/iron_sword"), ein * (1 - phase(t, TOD + .4, TOD + .8)), 1.0 if any(z <= t < z + .12 for z in (1.0, 1.6, 2.2)) else 0)
    voll = plate("enderman")
    hotbar(e, {6: voll} if t >= TOD + 2.2 else {}, ein)
    flug(e, voll, (CX, boden - 120), hotbar_mitte(6), phase(t, TOD + 1.0, TOD + 2.2), ein, 96)
    if t >= TOD + 2.2:
        mx, my = hotbar_mitte(6)
        funkenkranz(e, mx, my, t, TOD + 2.2, radius=60, n=6, farbe=(255, 190, 235), groesse=14)
    chat(e, 880, 905, chatzeilen([(TOD + 2.4, "§dEingefangen! §7Die gefüllte Plate liegt in deinem Inventar. Mit Rechtsklick "
                                              "auf einen Block lässt du den Mob wieder frei.")]), t, 3, ein)


KLICK_F = 2.7
ZWEITE = dict(gras=(214, 190, 120), gras_h=(232, 208, 140))


def szene_freisetzen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN, ein, seed=44, **ZWEITE)
    s = rueckschwung(phase(t, KLICK_F + .05, KLICK_F + .5))
    if s > 0:
        mob(e, "enderman", CX, BODEN, 30, ein, s)
        funkenkranz(e, CX, BODEN - 130, t, KLICK_F, radius=130, n=8)
    x, y = zeigerweg(t, [(.3, 1720, 720), (KLICK_F, CX, BODEN + 10), (KLICK_F + 1.0, 1700, 720)])
    hand(e, x, y, plate("enderman") if t < KLICK_F else None, ein * (1 - phase(t, KLICK_F + .6, KLICK_F + 1.0)))
    klick(e, t, KLICK_F, CX, BODEN + 10, ein)
    for i, (t0, zeile) in enumerate(((4.6, "§7Truhen und Türen: nur beim §fSchleichen"),
                                     (6.0, "§7Freigesetzt: §ckein Mana§7, §ckeine Quests"))):
        mct(e, 900, 790 + i * 50, zeile, 4, ein * aus_kubisch(phase(t, t0, t0 + .4)))


KLICK_D = 3.3


def szene_dorf(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    xl, xr = 1090, 1590
    for x, seed in ((xl, 31), (xr, 37)):
        buehne(e, x, 470, ein, seed=seed)
    mob(e, "villager", xl, 470, 26, ein * (1 - phase(t, KLICK_D, KLICK_D + .25)))
    mob(e, "zombie_villager", xr, 470, 26, ein * aus_kubisch(phase(t, .3, .7)))
    x, y = zeigerweg(t, [(1.4, 1400, 720), (KLICK_D, xl + 20, 340), (KLICK_D + .8, 1400, 640)])
    hand(e, x, y, plate("leer") if t < KLICK_D else None, ein * (1 - phase(t, KLICK_D + .4, KLICK_D + .8)))
    klick(e, t, KLICK_D, xl + 20, 340, ein)
    voll = plate("villager")
    hotbar(e, {2: voll} if t >= KLICK_D + .9 else {}, ein)
    flug(e, voll, (xl, 340), hotbar_mitte(2), phase(t, KLICK_D + .1, KLICK_D + .9), ein, 96)
    mct(e, xl, 688, "§aErster Klick: drin", 4, ein * aus_kubisch(phase(t, KLICK_D + .9, KLICK_D + 1.3)), anker="m")
    mct(e, xr, 688, "§cErst besiegen", 4, ein * aus_kubisch(phase(t, 5.6, 6.0)), anker="m")
    chat(e, 880, 905, chatzeilen([(KLICK_D + 1.1, "§dEingefangen! §7Dorfbewohner kommen ohne Kampf in die Plate. Mit Rechtsklick "
                                                  "auf einen Block lässt du ihn wieder frei.")]), t, 3, ein)


KLICK_W, ABSETZEN = 2.3, 6.2
NETZ_ROT = (235, 70, 60)


def szene_warpett(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    wechsel = ein_aus(phase(t, 4.9, 5.3))
    voll = plate("warpett")
    a = ein * (1 - wechsel)
    if a > 0:
        boden = BODEN - 100
        buehne(e, CX, boden, a)
        s = 1 - .5 * phase(t, KLICK_W, KLICK_W + .3)
        sprite_boden(e, "warpett_poppy", t, CX, boden + 4, 300 * s, a * (1 - phase(t, KLICK_W, KLICK_W + .3)))
        if t >= KLICK_W:
            funkenkranz(e, CX, boden - 120, t, KLICK_W, radius=120, n=8, farbe=(255, 190, 235))
        x, y = zeigerweg(t, [(.3, 1720, 620), (KLICK_W, CX + 30, boden - 120), (KLICK_W + 1.0, 1700, 620)])
        hand(e, x, y, plate("leer") if t < KLICK_W else None, a * (1 - phase(t, KLICK_W + .6, KLICK_W + 1.0)))
        klick(e, t, KLICK_W, CX + 30, boden - 120, a)
        hotbar(e, {2: voll} if t >= KLICK_W + .9 else {}, a)
        flug(e, voll, (CX, boden - 120), hotbar_mitte(2), phase(t, KLICK_W + .1, KLICK_W + .9), a, 96)
        mx, my = hotbar_mitte(2)
        tooltip_bei(e, ("§dMobplate: Warpett", "§7Blume: §dMohn", "§7Rechtsklick auf einen Block: absetzen"),
                    mx, my, 3, a * aus_kubisch(phase(t, 3.6, 4.0)))
    b = ein * wechsel
    if b > 0:
        xl, xr, boden = 1090, 1590, 540
        buehne(e, xl, boden, b, seed=44, **ZWEITE)
        buehne(e, xr, boden, b, seed=47, **ZWEITE)
        for cx, tv in ((xr - 80, .4), (xr + 80, 0)):
            sprite_boden(e, "warpett_poppy", t + tv, cx, boden + 4, 210, b, spiegeln=True)
        s = rueckschwung(phase(t, ABSETZEN + .05, ABSETZEN + .5))
        if s > 0:
            sprite_boden(e, "warpett_poppy", t, xl, boden + 4, 210 * s, b)
            funkenkranz(e, xl, boden - 90, t, ABSETZEN, radius=110, n=8)
        x, y = zeigerweg(t, [(5.0, 1700, 720), (ABSETZEN, xl, boden + 10), (ABSETZEN + 1.0, 1700, 720)])
        hand(e, x, y, voll if t < ABSETZEN else None, b * (1 - phase(t, ABSETZEN + .6, ABSETZEN + 1.0)))
        klick(e, t, ABSETZEN, xl, boden + 10, b)
        n = 28
        u = ein_aus(phase(t, 6.7, 7.3))
        for i in range(n + 1):
            p = i / n
            if p <= u:
                g = 16 if (p - t * .6) % .25 < .05 else 10
                gx, gy = xl + (xr - xl) * p, boden - 170 - 90 * math.sin(math.pi * p)
                mc.einfuegen(e, Image.new("RGBA", (g, g), NETZ_ROT + (255,)), gx - g / 2, gy - g / 2, b)
        s = rueckschwung(phase(t, 7.0, 7.4))
        if s > 0:
            mitte = (xl + xr) / 2
            skaliert(e, jar("block/poppy"), mitte, boden - 310, 80 * s, alpha=b)
            mct(e, mitte, boden - 395, "§dNetz Mohn", 4, b * aus_kubisch(phase(t, 7.1, 7.5)), anker="m")
        mct(e, 900, 770, "§7Andere Insel: §fgleiche Blume§7, §fgleiches Netz", 4, b * aus_kubisch(phase(t, 7.5, 7.9)))
        chat(e, 880, 905, chatzeilen([(ABSETZEN + .7, "§dVerbunden! §7Das Warpett ist wieder im Netz §fMohn§7, dort warten §f2 §7weitere.")]),
             t, 3, b)


ENDE_S = 4.6


def szene_schief(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN - 100, ein)
    boden = BODEN - 100
    mob(e, "sheep", CX, boden, 24, ein)
    if t < ENDE_S:
        funken(e, CX, boden, 110, 240, t, ein)
    zeit_tafel(e, 4 * (1 - phase(t, .4, ENDE_S)), ein)
    leer = plate("leer")
    hotbar(e, {4: leer} if t >= ENDE_S + .8 else {}, ein)
    flug(e, leer, (CX, boden - 100), hotbar_mitte(4), phase(t, ENDE_S, ENDE_S + .8), ein, 96)
    if t >= ENDE_S + .8:
        mx, my = hotbar_mitte(4)
        funkenkranz(e, mx, my, t, ENDE_S + .8, radius=60, n=6, groesse=14)
    chat(e, 880, 905, chatzeilen([(ENDE_S + .4, "§7Deine Markierung ist abgelaufen. Du hast die §dleere Plate §7zurück.")]), t, 3, ein)
    u = aus_kubisch(phase(t, 1.2, 1.7))
    for i, zeile in enumerate(("§7Auch wenn er §fanders stirbt§7,", "§fsich verwandelt §7oder §fverschwindet")):
        mct(e, 900, 210 + i * 44, zeile, 3, ein * u)


def szene_vielfalt(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    namen = sorted(f[:-4] for f in os.listdir(PLATES) if f.endswith(".png") and f != "forestling.png")  # Forestling: eigener Film
    rnd = random.Random(9)
    start = [rnd.uniform(.2, 2.6) for _ in namen]
    sp, z = 16, 60
    for i, name in enumerate(namen):
        s = rueckschwung(phase(t, start[i], start[i] + .3))
        if s > 0:
            skaliert(e, plate(name), 900 + i % sp * z + z / 2, 110 + i // sp * z + z / 2, 56 * s, alpha=ein)
    for i, (t0, zeile) in enumerate(((3.0, "§f11 §7Katzen, §f9 §7Wölfe, §f7 §7Pferde und viele mehr"),
                                     (6.2, "§cKeine Plate: §7Bossmobs und ein paar Sonderfälle"))):
        mct(e, 900, 690 + i * 56, zeile, 4, ein * aus_kubisch(phase(t, t0, t0 + .4)))
    u = aus_kubisch(phase(t, 7.8, 8.2))
    mct(e, 900, 802, "§7Babys ergeben die normale Plate, heraus kommt ein Erwachsener", 3, ein * u)


def szene_regeln(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    u = aus_kubisch(phase(t, .3, .8))
    mc.einfuegen(e, tafel(960, 330, 18), 880, 170 + (1 - u) * 30, ein * u)
    mct(e, 920, 200 + (1 - u) * 30, "§fAuf fremden Inseln", 5, ein * u)
    for i, (t0, was, recht) in enumerate(((2.2, "§7Markieren, Fangen, Mana-Apfel", "§fTiere"), (4.2, "§7Freisetzen", "§fBauen"),
                                          (5.4, "§7Warpett umziehen", "§fWarpetts"))):
        a = aus_kubisch(phase(t, t0, t0 + .4))
        mct(e, 920, 290 + i * 70, was, 4, ein * a)
        mct(e, 1800, 290 + i * 70, "§7Recht " + recht, 4, ein * a, anker="r")
    u = aus_kubisch(phase(t, 6.1, 6.6))
    mc.einfuegen(e, tafel(960, 290, 18), 880, 530 + (1 - u) * 30, ein * u)
    mct(e, 920, 560 + (1 - u) * 30, "§fHandel im ChestShop", 5, ein * u)
    for i, (t0, bild, zeile) in enumerate(((6.6, plate("enderman"), "§aMobplates: §7leer und gefüllt"),
                                           (7.5, plate("scherbe"), "§aBlasse Scherben: §7auch"))):
        a = aus_kubisch(phase(t, t0, t0 + .4))
        skaliert(e, bild, 960, 670 + i * 76, 64, alpha=ein * a)
        mct(e, 1020, 654 + i * 76, zeile, 4, ein * a)


def szene_outro(e, t, d):
    titelkarte(e, t, "Viel Spaß beim Einfangen!", "Alles Weitere steht im Wiki unter Mobplates", y=150)
    u = rueckschwung(phase(t, .5, 1.0))
    if u > 0:
        skaliert(e, plate("enderman"), W / 2, 610 + 8 * math.sin(t * 2), 190 * u)
    mb_logo(e, W / 2, 830, 200, aus_kubisch(phase(t, 1.4, 2.0)))


SZENEN = [
    dict(dauer=8.4, zeichne=szene_intro, ton=[(.2, "sfx:chime"), (1.5, "sfx:funkeln", .7)] + erzaehlt(.8, "mobplates-intro")),
    dict(dauer=8.6, nr="01", kicker="Rezept", titel="Die Blasse Scherbe",
         text="Eine beliebige Töpferscherbe, rundum 8 Ziegel. An der Werkbank.",
         zeichne=szene_scherbe, ton=werkbank_ton(ZEITEN_SCHERBE) + erzaehlt(.4, "mobplates-scherbe")),
    dict(dauer=9.6, nr="02", kicker="Rezept", titel="Die leere Mobplate",
         text="Die Blasse Scherbe, rundum 8 Mana-Kugeln. Das ist alles, was du zum Fangen brauchst.",
         zeichne=szene_plate, ton=werkbank_ton(ZEITEN_PLATE) + erzaehlt(.4, "mobplates-plate")),
    dict(dauer=8.0, nr="03", kicker="Fangen", titel="Markieren",
         text="Rechtsklick mit der leeren Plate auf einen Mob. Die Plate ist verbraucht, du hast 10 Minuten.",
         zeichne=szene_markieren, ton=[(KLICK_M, "sfx:klick"), (KLICK_M + .05, "sfx:funkeln", .7)] + erzaehlt(.4, "mobplates-markieren")),
    dict(dauer=8.2, nr="04", kicker="Freiwillig", titel="Der Mana-Apfel",
         text="Er nimmt deinem markierten Mob die Hälfte seiner Herzen. Einmal je Mob.",
         zeichne=szene_apfel, ton=[(KLICK_A, "sfx:klick"), (KLICK_A + .7, "sfx:pop", .6)] + erzaehlt(.4, "mobplates-apfel")),
    dict(dauer=9.0, nr="05", kicker="Fangen", titel="Direkt ins Inventar",
         text="Töte den Mob. Die gefüllte Plate liegt sofort bei dir, nichts fällt ins Leere. Die Beute fällt wie immer.",
         zeichne=szene_fangen, ton=[(1.0, "sfx:klick"), (1.6, "sfx:klick"), (2.2, "sfx:klick"), (TOD, "sfx:pop"), (TOD + 2.2, "sfx:erfolg", .7)] + erzaehlt(.4, "mobplates-fangen")),
    dict(dauer=10.0, nr="06", kicker="Freisetzen", titel="Wieder frei",
         text="Rechtsklick mit der gefüllten Plate auf einen Block oder auf Wasser. Dein Inventar reist mit, also auch auf andere Inseln.",
         zeichne=szene_freisetzen, ton=[(KLICK_F, "sfx:klick"), (KLICK_F + .05, "sfx:funkeln", .8)] + erzaehlt(.4, "mobplates-freisetzen")),
    dict(dauer=9.2, nr="07", kicker="Dorfbewohner", titel="Ganz ohne Kampf",
         text="Dorfbewohner kommen beim ersten Klick in die Plate. Zombie-Dorfbewohner musst du besiegen.",
         zeichne=szene_dorf, ton=[(KLICK_D, "sfx:klick"), (KLICK_D + .9, "sfx:erfolg", .6)] + erzaehlt(.4, "mobplates-dorf")),
    dict(dauer=9.4, nr="08", kicker="Warpetts", titel="Die Blume reist mit",
         text="Klick mit der leeren Plate auf ein aufgestelltes Warpett. Abgesetzt gehört es sofort wieder zum Netz seiner Blume.",
         zeichne=szene_warpett, ton=[(KLICK_W, "sfx:klick"), (KLICK_W + .9, "sfx:erfolg", .6), (ABSETZEN, "sfx:klick"),
                                     (ABSETZEN + .05, "sfx:funkeln", .8), (7.0, "sfx:pop", .6)] + erzaehlt(.4, "mobplates-warpett")),
    dict(dauer=8.4, nr="09", kicker="Keine Sorge", titel="Die Plate kommt zurück",
         text="Zeit um, Mob anders gestorben, verwandelt oder verschwunden: Du bekommst die leere Plate zurück.",
         zeichne=szene_schief, ton=[(ENDE_S, "sfx:pop", .7), (ENDE_S + .8, "sfx:funkeln", .6)] + erzaehlt(.4, "mobplates-schief")),
    dict(dauer=10.4, nr="10", kicker="Vielfalt", titel="127 Plates",
         text="Eine eigene Plate gibt es nur, wo man den Unterschied dauerhaft sieht. Schafe kommen immer weiß heraus.",
         zeichne=szene_vielfalt, ton=[(.2, "sfx:funkeln", .7)] + erzaehlt(.4, "mobplates-vielfalt")),
    dict(dauer=11.2, nr="11", kicker="Regeln", titel="Fremde Inseln und Handel",
         text="Fremde gezähmte Tiere gehen nicht. Bewohner und die Crew passen in keine Plate.",
         zeichne=szene_regeln, ton=erzaehlt(.4, "mobplates-regeln")),
    dict(dauer=5.0, zeichne=szene_outro, ton=[(.3, "sfx:chime", .8)] + erzaehlt(.5, "mobplates-outro")),
]

FILM = Film("mobplates", SZENEN, musik=dict(tonart="A", tempo=88, stimmung="hell"))
FILM.poster = sum(s["dauer"] for s in SZENEN[:5]) + 4.5
