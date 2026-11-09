#!/usr/bin/env python3
"""Furnace Golem auf MegaBuild Skyblock: Mana-Block, Golem bauen, ein- und abheben, Mana-Geode,
Scherben verbacken, Tageslimit, Abbauen.

Inhalt nach MBSkyManager/docs/MANA.md (Stand 09.11.2026, Commit 54ab82ec: Kapitel Mana-Block,
Mana-Geode und Der Furnace Golem) und config.yml mana.golem / mana.budding: 1 Mana je Scherbe
in 120 s, 20 Scherben je Erbauer und Tag, Block = 17 Mana ohne Rueckrezept, Kristall in vier
Stufen zu je rund 10 Minuten. Seit 09.11.: Arme ueber dem Kopf (Pool 75f3f3c5), nur rosa
Effekte (nichts Brennendes), Abheben nur als Kugeln, Plaketten statt Items im Menue. Menue und Chat aus lang/de.yml (menu.furnace-golem.*,
furnace-golem.*), Tageswechsel aus quests.reset (4 Uhr). Die Figur kommt aus modelle.py
(fgolem_*), die Bloecke als eigene Iso-Wuerfel aus den Texturen des Manager-Packs und des
Client-Jars. Mala erklaert jede Szene (nur Deutsch).

    python3 modelle.py fgolem_idle fgolem_play fgolem_start fgolem_work fgolem_take fgolem_done \\
        fgolem_wait fgolem_rest fgolem_greet fgolem_happy
    python3 bauen.py furnace_golem
"""
import functools
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageEnhance, ImageOps  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403
from mobplates import Z, flug, hand, hotbar, hotbar_mitte, jar, werkbank, werkbank_ton, zeit_tafel  # noqa: E402,F401

PINK = (255, 105, 200)
ROSA = (255, 190, 235)
ERBAUER = "Alex"
TITEL = "§d§lFurnace Golem"


# ── Bloecke als Iso-Wuerfel ─────────────────────────────────────────────────

def _flaeche(tex, O, U, V, groesse, hell):
    """Textur affin auf das Parallelogramm O, O+U, O+U+V, O+V legen."""
    a, b, c, d = U[0] / tex.width, V[0] / tex.height, U[1] / tex.width, V[1] / tex.height
    det = a * d - b * c
    ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    daten = (ia, ib, -(ia * O[0] + ib * O[1]), ic, id_, -(ic * O[0] + id_ * O[1]))
    if hell < 1:
        hell_bild = ImageEnhance.Brightness(tex.convert("RGB")).enhance(hell).convert("RGBA")
        hell_bild.putalpha(tex.getchannel("A"))
        tex = hell_bild
    bild = tex.transform(groesse, Image.AFFINE, daten, resample=Image.NEAREST)
    maske = Image.new("L", groesse, 0)
    ImageDraw.Draw(maske).polygon([O, (O[0] + U[0], O[1] + U[1]), (O[0] + U[0] + V[0], O[1] + U[1] + V[1]),
                                   (O[0] + V[0], O[1] + V[1])], fill=255)
    alpha = Image.new("L", groesse, 0)
    alpha.paste(bild.getchannel("A"), mask=maske)
    bild.putalpha(alpha)
    return bild


def _wuerfel(oben, links, rechts, kante):
    """Wuerfel von schraeg oben: links die Vorderseite (0.8 hell), rechts die Seite (0.62)."""
    w, h = kante * math.cos(math.radians(30)), kante / 2
    groesse = (math.ceil(2 * w) + 1, math.ceil(2 * h + kante) + 1)
    bild = Image.new("RGBA", groesse, (0, 0, 0, 0))
    for tex, O, U, V, hell in ((oben, (0, h), (w, -h), (w, h), 1.0),
                               (links, (0, h), (w, h), (0, kante), .8),
                               (rechts, (w, 2 * h), (w, -h), (0, kante), .62)):
        bild.alpha_composite(_flaeche(tex, O, U, V, groesse, hell))
    return bild


@functools.lru_cache(maxsize=None)
def manager_block(name):
    return Image.open(os.path.join(mc.MANAGER, "block", name + ".png")).convert("RGBA")


@functools.lru_cache(maxsize=None)
def _kiste_flaechen():
    """Truhe aus entity/chest/normal (seit 1.15 kopfstehend): Deckel, Vorderseite mit Schloss, Seite."""
    c = jar("entity/chest/normal")
    vorne = Image.new("RGBA", (14, 14))
    vorne.paste(ImageOps.flip(c.crop((14, 14, 28, 19))), (0, 0))
    vorne.paste(ImageOps.flip(c.crop((14, 33, 28, 43))).crop((0, 1, 14, 10)), (0, 5))
    vorne.paste(ImageOps.flip(c.crop((1, 1, 3, 5))), (6, 3))
    seite = Image.new("RGBA", (14, 14))
    seite.paste(ImageOps.flip(c.crop((0, 14, 14, 19))), (0, 0))
    seite.paste(ImageOps.flip(c.crop((0, 34, 14, 43))), (0, 5))
    return ImageOps.flip(c.crop((28, 0, 42, 14))), vorne, seite


@functools.lru_cache(maxsize=None)
def block(name, kante):
    if name == "mana_block":
        t = manager_block("mana_block")
        return _wuerfel(t, t, t, kante)
    if name == "budding":
        b = manager_block("mana_budding")
        oben = b.crop((0, 0, 16, 16))
        oben.alpha_composite(manager_block("mana_budding_glow").crop((0, 0, 16, 16)))
        seite = b.crop((16, 0, 32, 16))
        return _wuerfel(oben, seite, seite, kante)
    if name == "ofen":
        return _wuerfel(jar("block/furnace_top"), jar("block/furnace_front"), jar("block/furnace_side"), kante)
    if name == "kuerbis":
        return _wuerfel(jar("block/pumpkin_top"), jar("block/carved_pumpkin"), jar("block/pumpkin_side"), kante)
    if name == "kiste":
        oben, vorne, seite = _kiste_flaechen()
        return _wuerfel(oben, vorne, seite, round(kante * 14 / 16))
    raise KeyError(name)


def setze_block(e, name, kante, cx, unten, alpha=1.0, s=1.0):
    """Wuerfel mit der vorderen unteren Ecke bei (cx, unten); s skaliert fuers Erscheinen."""
    if s <= .02 or alpha <= .003:
        return
    bild = block(name, kante)
    if s != 1.0:
        bild = bild.resize((max(1, round(bild.width * s)), max(1, round(bild.height * s))), Image.LANCZOS)
    mc.einfuegen(e, bild, cx - bild.width / 2, unten - bild.height, alpha)


def oben_mitte(kante, unten):
    """Mitte der Oberseite eines Wuerfels, dessen vordere untere Ecke auf unten steht."""
    return unten - 1.5 * kante


# ── Golem ───────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=None)
def _unten():
    return sprite_unten("fgolem_idle")


def golem_mitte(boden, g):
    return boden - (_unten() - .5) * g


def golem(e, name, t, cx, boden, g, alpha=1.0, schleife=True):
    """Furnace Golem mit festem Fusspunkt (alle Animationen auf derselben Grundlinie)."""
    schatten(e, cx, boden + 4, g * .55, .55 * alpha)
    sprite(e, name, t, cx, golem_mitte(boden, g), g, alpha, schleife=schleife)


def maul(cx, boden, g):
    """Ofenmaul im Sprite (512er Bild: um 220/305)."""
    return cx + (220 - 256) / 512 * g, golem_mitte(boden, g) + (305 - 256) / 512 * g


def ofen(cx, boden, g):
    """Ofenoeffnung im Sprite (512er Bild: um 205/378) - dort glimmt das Mana."""
    return cx + (205 - 256) / 512 * g, golem_mitte(boden, g) + (378 - 256) / 512 * g


def kopf(cx, boden, g):
    """Ueber dem Kopf zwischen den erhobenen Armen (512er Bild: um 262/140)."""
    return cx + (262 - 256) / 512 * g, golem_mitte(boden, g) + (140 - 256) / 512 * g


# Die drei Rosatoene der Partikel im Spiel (FurnaceGolemService MANA_DUST, MANA_GLOW, MANA_DIM)
MANA_DUST, MANA_GLOW, MANA_DIM = (253, 68, 190), (255, 165, 225), (196, 116, 170)


def glimmen(e, x, y, t, alpha, n=7, breite=60, seed=3, farben=(MANA_DUST, MANA_GLOW)):
    """Rosa Glimmen an der Ofenoeffnung: Koernchen leuchten auf und steigen ein Stueck.
    Seit 09.11.2026 statt Flammen und Lavafunken (Kay: nichts Brennendes mehr)."""
    rnd = random.Random(seed)
    for i in range(n):
        tempo, versatz = rnd.uniform(.8, 1.3), rnd.random()
        dx, dy = rnd.uniform(-breite / 2, breite / 2), rnd.uniform(-10, 10)
        farbe, g = rnd.choice(farben), rnd.choice((8, 10, 12))
        u = (t * tempo + versatz) % 1
        mc.einfuegen(e, Image.new("RGBA", (g, g), farbe + (255,)), x + dx - g / 2, y + dy - u * 34 - g / 2,
                     alpha * math.sin(math.pi * u))


def faden(e, x, y, t, alpha, n=6, hoehe=150):
    """Heller Mana-Faden, der zwischen den erhobenen Armen aufsteigt (statt Rauch aus dem Schornstein)."""
    for i in range(n):
        u = (t * .5 + i / n) % 1
        g = 10 if u < .5 else 8
        mc.einfuegen(e, Image.new("RGBA", (g, g), MANA_GLOW + (255,)), x + 8 * math.sin(u * 5 + t * 1.5) - g / 2,
                     y - u * hoehe - g / 2, alpha * .9 * (1 - u))


def staub(e, cx, unten, t, alpha, n=10, radius=120, hoehe=240, seed=5):
    """Rosa Mana-Staub, der um ihn aufsteigt."""
    rnd = random.Random(seed)
    for i in range(n):
        versatz, tempo, g = rnd.random(), rnd.uniform(.35, .55), rnd.choice((8, 10, 14))
        u = (t * tempo + versatz) % 1
        w = versatz * 2 * math.pi + t * 1.8
        x = cx + math.cos(w) * radius * (1 - .35 * u)
        mc.einfuegen(e, Image.new("RGBA", (g, g), PINK + (255,)), x - g / 2, unten - u * hoehe,
                     alpha * math.sin(math.pi * u))


def regen(e, cx, oben, t, t0, alpha, n=14, breite=150, seed=9):
    """Staubregen beim Fertigwerden."""
    rnd = random.Random(seed)
    for i in range(n):
        u = phase(t, t0 + rnd.uniform(0, .5), t0 + rnd.uniform(1.0, 1.6))
        if 0 < u < 1:
            g = rnd.choice((8, 12))
            mc.einfuegen(e, Image.new("RGBA", (g, g), ROSA + (255,)), cx + rnd.uniform(-breite, breite),
                         oben + u * 200, alpha * (1 - u))


def zzz(e, x, y, t, alpha):
    for i in range(3):
        u = (t * .45 + i / 3) % 1
        mct(e, x + 30 * u + 14 * i, y - 110 * u, "§fz", 4 + i, alpha * math.sin(math.pi * u), anker="m")


@functools.lru_cache(maxsize=None)
def insel(seed, breite=13, gras=(88, 160, 64), gras_h=(118, 190, 82)):
    return insel_bild(breite, 4, seed, 30, gras=gras, gras_h=gras_h, baum=False)


def buehne(e, cx, boden, alpha, seed=31, breite=13, **farben):
    bild = insel(seed, breite, **farben)
    mc.einfuegen(e, bild, cx - bild.width / 2, boden, alpha)


# ── Hoehle ──────────────────────────────────────────────────────────────────

HX, HY, HW, HH = 880, 140, 960, 560
BODEN_H = 560  # Oberkante des Hoehlenbodens (Bildschirm)
KRISTALL = ["mana_bud_small", "mana_bud_medium", "mana_bud_large", "mana_cluster"]


@functools.lru_cache(maxsize=None)
def hoehle_bild():
    """Hoehle von vorn: dunkle Rueckwand, Boden aus Geodenschichten, abgerundet."""
    k = 64
    bild = Image.new("RGBA", (HW, HH), (0, 0, 0, 255))
    rnd = random.Random(12)
    wand = [jar("block/deepslate"), jar("block/tuff"), jar("block/deepslate"), jar("block/smooth_basalt")]
    boden_y = BODEN_H - HY
    for y in range(0, HH, k):
        for x in range(0, HW, k):
            if y >= boden_y:
                tiefe = (y - boden_y) // k
                tex = [jar("block/amethyst_block"), jar("block/calcite"), jar("block/smooth_basalt")][min(2, tiefe)]
                hell = .78
            else:
                tex, hell = rnd.choice(wand), .34 + .1 * rnd.random()
            kachel = ImageEnhance.Brightness(tex.convert("RGB").resize((k, k), Image.NEAREST)).enhance(hell)
            bild.paste(kachel, (x, y))
    licht = glanz(330, PINK, 70)
    bild.alpha_composite(licht, (HW // 2 - 330, boden_y - 330))
    maske = Image.new("L", (HW, HH), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, HW - 1, HH - 1), 22, fill=255)
    bild.putalpha(maske)
    return bild


def hoehle(e, alpha):
    mc.einfuegen(e, tafel(HW + 12, HH + 12, 26, (0, 0, 0, 0), (255, 255, 255, 60)), HX - 6, HY - 6, alpha)
    mc.einfuegen(e, hoehle_bild(), HX, HY, alpha)


KB = 120          # Kante des Budding-Blocks
BX = HX + HW // 2  # Mitte des Blocks
BU = BODEN_H + KB // 2 + 4  # vordere untere Ecke: halb im Boden


def kristall(e, stufe, s, alpha, riss=-1):
    """Kristall der Stufe 0-3 auf dem Budding-Block, Unterkante auf der Oberseitenmitte."""
    if s <= .02:
        return
    bild = manager_block(KRISTALL[stufe])
    g = KB * 1.15 * s
    oy = oben_mitte(KB, BU) + 8
    if riss >= 0:
        bild = bild.copy()
        risse = jar("block/destroy_stage_%d" % min(9, riss))
        bild.alpha_composite(Image.composite(risse, Image.new("RGBA", bild.size, (0, 0, 0, 0)), bild.getchannel("A")))
    skaliert(e, bild, BX, oy - g / 2, g, alpha=alpha)


# ── Menue ───────────────────────────────────────────────────────────────────

MX, MY, MS = 870, 250, 4
def menue(kugeln, bloecke):
    """Slots wie im Spiel seit 09.11.2026: gruene Plaketten zum Einzahlen, goldene zum Abheben, die
    Menge als Stapelzahl (hoechstens 64, ohne Items 1). Abheben nur noch als Kugeln."""
    def n(x):
        return max(1, min(64, x))
    return {4: "mana", 10: "golem_deposit", 11: "golem_in_one", 12: ("golem_in_stack", n(kugeln)),
            13: ("golem_in_all", n(kugeln)), 15: "golem_in_block", 16: ("golem_in_blocks", n(bloecke)),
            19: "golem_withdraw", 20: "golem_out_one", 21: ("golem_out_some", 16), 22: ("golem_out_stack", 64),
            29: "mana_shard", 31: "golem_work", 33: "golem_daily", 40: "golem_dismantle", 44: "close"}


def konto(stand, kugeln, bloecke):
    return ("§dDein Mana", f"§7Konto: §d{stand} Mana", f"§7Mana-Kugeln dabei: §f{kugeln}",
            f"§7Mana-Blöcke dabei: §f{bloecke}", "§8Kugel = 1 Mana, Block = 17 Mana")


def slot_klick(e, t, t0, slot, alpha):
    x, y = slot_mitte(slot, MX, MY, MS)
    klick(e, t, t0, x, y, alpha)


# ── Szenen ──────────────────────────────────────────────────────────────────

def szene_intro(e, t, d):
    titelkarte(e, t, "Furnace Golem", "Mana einzahlen – und aus Scherben neues backen", y=110)
    s = rueckschwung(phase(t, .6, 1.2))
    a = aus_kubisch(phase(t, .4, 1.0))
    buehne(e, W / 2, 790, a, breite=17)
    setze_block(e, "kiste", 96, W / 2 + 250, 812, a, s)
    if s > 0:
        g = 500 * s
        golem(e, "fgolem_work", t, W / 2 - 50, 790, g, a)
        if t > 1.2:
            glimmen(e, *ofen(W / 2 - 50, 790, g), t, a, n=9, breite=90)
            faden(e, *kopf(W / 2 - 50, 790, g), t, a)
            staub(e, W / 2 - 50, 790, t, a * aus_kubisch(phase(t, 1.4, 2.4)), radius=170, hoehe=300)


ZEITEN_BLOCK = (5.2, 3.3, 6.0)


def szene_block(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    werkbank(e, t, lambda _t: mc.icon16("mana_charge"), mc.icon16("mana_orb"), mc.icon16("mana_block"),
             "§dMana-Block", ein, ZEITEN_BLOCK)
    mct(e, 930, 690, "§d8 Mana-Kugeln §7um eine §dMana-Ladung", 4, ein * aus_kubisch(phase(t, 3.3, 3.8)))
    mct(e, 930, 750, "§7Ein Block = §d17 Mana §7· kein Rückrezept", 4, ein * aus_kubisch(phase(t, 6.4, 6.9)))


KB2 = 84        # Kante beim Bauen
BAU_X, BAU_B = 1330, 640
BAU = [(1.1, "mana_block"), (2.8, "ofen"), (4.8, "kuerbis")]
FERTIG = 5.4


def szene_bauen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, BAU_X, BAU_B, ein)
    weg = 1 - phase(t, FERTIG, FERTIG + .3)
    unten = BAU_B + 26
    for i, (t0, name) in enumerate(BAU):
        s = rueckschwung(phase(t, t0, t0 + .3))
        setze_block(e, name, KB2, BAU_X, unten - i * KB2, ein * weg, s)
    if t >= FERTIG:
        for i in range(3):
            funkenkranz(e, BAU_X, unten - KB2 - i * KB2, t, FERTIG + i * .05, radius=70, n=6, farbe=(255, 255, 255))
        s = rueckschwung(phase(t, FERTIG + .1, FERTIG + .5))
        golem(e, "fgolem_start", t - FERTIG, BAU_X, BAU_B + 6, 380 * s, ein, schleife=False) \
            if t < FERTIG + 1.3 else golem(e, "fgolem_idle", t, BAU_X, BAU_B + 6, 380, ein)
    punkte = [(.2, 1720, 760)]
    for i, (t0, _) in enumerate(BAU):
        ziel = (BAU_X + 10, unten - i * KB2 - KB2 * .9)
        punkte += [(t0 - .5, *ziel), (t0, *ziel)]
    punkte.append((FERTIG + .4, 1720, 760))
    x, y = zeigerweg(t, punkte)
    item = None
    for t0, name in BAU:
        if t < t0:
            item = block(name, 44)
            break
    hand(e, x, y, item, ein * (1 - phase(t, FERTIG, FERTIG + .4)))
    for i, (t0, _) in enumerate(BAU):
        klick(e, t, t0, BAU_X + 10, unten - i * KB2 - KB2 * .9, ein)
    chat(e, 880, 880, chatzeilen([(FERTIG + .5, "§aDein Furnace Golem steht! Stell eine Truhe oder ein Fass mit "
                                                "Mana-Scherben direkt neben ihn – er macht daraus Mana für dich.")]),
         t, 3, ein)
    mct(e, 900, 170, "§7Der Kopf §fzuletzt§7, auch eine Kürbislaterne", 4, ein * aus_kubisch(phase(t, 4.4, 4.8)))
    mct(e, 900, 220, "§7Nur im §fÜberlebensmodus §7und mit dem Recht §fBauen", 4,
        ein * aus_kubisch(phase(t, 7.0, 7.4)))


EIN_1, EIN_2 = 3.7, 5.6
GX, GB, GG = 1810, 850, 250  # Golem unten rechts, unter den Tooltips


def szene_einzahlen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    if t < EIN_1:
        stand, kugeln, bloecke = 57, 87, 3
    elif t < EIN_2:
        stand, kugeln, bloecke = 144, 0, 3
    else:
        stand, kugeln, bloecke = 195, 0, 0
    tipps = {4: konto(stand, kugeln, bloecke),
             13: ("§aAlle Kugeln einzahlen", "§7Alle Kugeln aus deinem Inventar", "§7+§f87§7 Mana aufs Konto",
                  "§8Klick zum Einzahlen") if t < EIN_1 else
             ("§aAlle Kugeln einzahlen", "§7Du hast keine Mana-Kugeln dabei.", "§8Mana-Erz lässt sie fallen."),
             16: ("§aAlle Mana-Blöcke einzahlen", "§7Alle Blöcke aus deinem Inventar", "§7+§f51§7 Mana aufs Konto",
                  "§8Klick zum Einzahlen") if t < EIN_2 else
             ("§aAlle Mana-Blöcke einzahlen", "§7Du hast keine Mana-Blöcke dabei.", "§88 Kugeln um eine Mana-Ladung",
              "§8ergeben einen Block.")}
    halte = [(.3, 1.0, 4), (2.5, 3.1, 13), (4.5, 5.0, 16)]
    buehne(e, GX, GB, ein, seed=33, breite=7)
    if t < 1.3:
        golem(e, "fgolem_greet", t, GX, GB, GG, ein, schleife=False)
    elif EIN_1 <= t < EIN_1 + 1.0:
        golem(e, "fgolem_happy", t - EIN_1, GX, GB, GG, ein, schleife=False)
    elif EIN_2 <= t < EIN_2 + 1.0:
        golem(e, "fgolem_happy", t - EIN_2, GX, GB, GG, ein, schleife=False)
    else:
        golem(e, "fgolem_idle", t, GX, GB, GG, ein)
    for t0 in (EIN_1, EIN_2):
        if t >= t0:
            funkenkranz(e, *maul(GX, GB, GG), t, t0 + .1, radius=40, n=6, farbe=ROSA, groesse=14)
    menue_mit_zeiger(e, t, TITEL, 5, menue(kugeln, bloecke), tipps, halte, MX, MY, MS, ein)
    slot_klick(e, t, EIN_1, 13, ein)
    slot_klick(e, t, EIN_2, 16, ein)
    chat(e, 110, 905, chatzeilen([(EIN_1 + .1, "§d87 Mana §7eingezahlt. Konto: §d144 Mana"),
                                  (EIN_2 + .1, "§d51 Mana §7eingezahlt. Konto: §d195 Mana")]), t, 3, ein)


AB_1, AB_2 = 3.6, 5.4


def szene_abheben(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    stand = 195 if t < AB_1 else 131 if t < AB_2 else 115
    tipps = {19: ("§6Abheben", "§7Mana vom Konto zurück", "§7als Mana-Kugeln", "§8Nur so viel, wie ins Inventar passt"),
             22: ("§664 Kugeln abheben", "§7Du bekommst §f64× Mana-Kugel", "§7-§f64§7 Mana vom Konto", "§8Klick zum Abheben"),
             21: ("§616 Kugeln abheben", "§7Du bekommst §f16× Mana-Kugel", "§7-§f16§7 Mana vom Konto",
                  "§8Klick zum Abheben"),
             4: konto(stand, 0, 0)}
    halte = [(.3, .9, 19), (2.4, 3.0, 22), (4.4, 4.9, 21)]
    buehne(e, GX, GB, ein, seed=33, breite=7)
    golem(e, "fgolem_idle", t, GX, GB, GG, ein)
    hotbar(e, ({1: mc.icon16("mana_orb")} if t >= AB_1 + .2 else {}) |
           ({2: mc.icon16("mana_orb")} if t >= AB_2 + .2 else {}), ein * aus_kubisch(phase(t, .6, 1.0)))
    menue_mit_zeiger(e, t, TITEL, 5, menue(0, 0), tipps, halte, MX, MY, MS, ein)
    slot_klick(e, t, AB_1, 22, ein)
    slot_klick(e, t, AB_2, 21, ein)
    chat(e, 110, 905, chatzeilen([(AB_1 + .1, "§f64× Mana-Kugel §7abgehoben (§d-64 Mana§7). Konto: §d131 Mana"),
                                  (AB_2 + .1, "§f16× Mana-Kugel §7abgehoben (§d-16 Mana§7). Konto: §d115 Mana")]),
         t, 3, ein)


STUFEN = (5.0, 5.9, 6.8, 7.7)
NAMEN = ("klein", "mittel", "groß", "Cluster")


def stufe_bei(t, zeiten):
    stufe = -1
    for i, t0 in enumerate(zeiten):
        if t >= t0:
            stufe = i
    return stufe


def szene_geode(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    hoehle(e, ein)
    setze_block(e, "budding", KB, BX, BU, ein)
    if t >= 3.0:
        funkenkranz(e, BX, oben_mitte(KB, BU), t, 3.0, radius=90, n=6, farbe=ROSA, groesse=16)
    mct(e, BX, HY + 96, "§dKnospender Mana-Amethyst", 4,
        ein * aus_kubisch(phase(t, 3.0, 3.4)) * (1 - phase(t, 4.6, 5.0)), anker="m")
    stufe = stufe_bei(t, STUFEN)
    if stufe >= 0:
        s = rueckschwung(phase(t, STUFEN[stufe], STUFEN[stufe] + .35))
        kristall(e, stufe, s, ein)
        if t - STUFEN[stufe] < .9:
            funkenkranz(e, BX, oben_mitte(KB, BU) - 60, t, STUFEN[stufe], radius=80, n=6, farbe=ROSA, groesse=16)
    for i, name in enumerate(NAMEN):
        x = HX + 150 + i * 220
        aktiv = stufe == i
        farbe = "§d" if aktiv else "§f" if stufe > i else "§8"
        a = ein * aus_kubisch(phase(t, STUFEN[i] - .3, STUFEN[i]))
        mct(e, x, HY + 22, farbe + name, 4, max(a, ein * .5), anker="m")
        if i < 3:
            mct(e, x + 110, HY + 22, "§8→", 4, ein * .7, anker="m")
    mct(e, HX + HW / 2, HY + HH + 24, "§7Nie auf deiner §fStartinsel", 4, ein * aus_kubisch(phase(t, 1.8, 2.2)), anker="m")
    mct(e, HX + HW / 2, HY + HH + 76, "§7Je Stufe §frund 10 Minuten", 4, ein * aus_kubisch(phase(t, 5.2, 5.6)), anker="m")
    mct(e, HX + HW / 2, HY + HH + 128, "§7Nur, §fsolange die Insel geladen ist", 4, ein * aus_kubisch(phase(t, 6.6, 7.0)),
        anker="m")


SCHLAG, BRUCH = 2.2, 3.2


def szene_scherbe(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    hoehle(e, ein)
    setze_block(e, "budding", KB, BX, BU, ein)
    ky = oben_mitte(KB, BU) - 60
    if t < BRUCH:
        riss = int(10 * phase(t, SCHLAG, BRUCH)) - 1 if t >= SCHLAG else -1
        kristall(e, 3, 1.0, ein, riss)
    else:
        rnd = random.Random(4)
        u = phase(t, BRUCH, BRUCH + .7)
        if u < 1:
            for i in range(14):
                w = rnd.uniform(0, 2 * math.pi)
                r = rnd.uniform(40, 140) * aus_kubisch(u)
                g = rnd.choice((10, 14, 18))
                mc.einfuegen(e, Image.new("RGBA", (g, g), PINK + (255,)), BX + math.cos(w) * r,
                             ky + math.sin(w) * r + 80 * u * u, ein * (1 - u))
    scherbe = mc.icon16("mana_shard")
    zu = hotbar_mitte(2)
    flug(e, scherbe, (BX, ky), zu, phase(t, BRUCH + .1, BRUCH + .9), ein, 80)
    hotbar(e, {2: scherbe} if t >= BRUCH + .9 else {}, ein)
    x, y = zeigerweg(t, [(.3, 1700, 760), (SCHLAG - .1, BX + 30, ky + 20), (BRUCH + .3, BX + 30, ky + 20),
                         (BRUCH + 1.1, 1700, 760)])
    druck = .6 if SCHLAG <= t < BRUCH else 0.0
    hand(e, x + 6 * math.sin(t * 40) * (SCHLAG <= t < BRUCH), y, None, ein * (1 - phase(t, BRUCH + .8, BRUCH + 1.2)),
         druck)
    tooltip_bei(e, ("§dMana-Scherbe",), *zu, 3, ein * aus_kubisch(phase(t, 4.4, 4.8)))
    mct(e, 900, HY + HH + 140, "§7Eine Knospe gibt §fnichts §7– lass sie wachsen", 4, ein * aus_kubisch(phase(t, 5.4, 5.8)))


TRUHE_X, TRUHE_U = 1470, 666
GOL_X, GOL_B, GOL_G = 1255, 640, 330
REIN, NIMMT = 2.0, 3.9


def szene_truhe(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, 1340, GOL_B, ein, breite=15)
    setze_block(e, "kiste", 80, TRUHE_X, TRUHE_U, ein)
    if t < NIMMT:
        golem(e, "fgolem_wait", t + 1.0, GOL_X, GOL_B, GOL_G, ein)
    elif t < NIMMT + 1.0:
        golem(e, "fgolem_take", t - NIMMT, GOL_X, GOL_B, GOL_G, ein, schleife=False)
    else:
        golem(e, "fgolem_work", t, GOL_X, GOL_B, GOL_G, ein)
        glimmen(e, *ofen(GOL_X, GOL_B, GOL_G), t, ein * aus_kubisch(phase(t, NIMMT + 1.0, NIMMT + 1.4)))
    scherbe = mc.icon16("mana_shard")
    deckel = (TRUHE_X, TRUHE_U - 100)
    x, y = zeigerweg(t, [(.3, 1720, 760), (REIN - .1, deckel[0] + 10, deckel[1]), (REIN + .8, 1720, 760)])
    hand(e, x, y, scherbe if t < REIN else None, ein * (1 - phase(t, REIN + .5, REIN + .9)))
    klick(e, t, REIN, deckel[0] + 10, deckel[1], ein)
    flug(e, scherbe, deckel, maul(GOL_X, GOL_B, GOL_G), phase(t, NIMMT, NIMMT + .7), ein, 60)
    if t >= NIMMT:
        staub(e, TRUHE_X, TRUHE_U - 60, t, ein * (1 - phase(t, NIMMT + .6, NIMMT + 1.4)), n=6, radius=40, hoehe=120)
    mct(e, 900, 170, "§7Keine Scherbe? §fEr wartet §7und schaut sich um", 4,
        ein * aus_kubisch(phase(t, .5, .9)) * (1 - phase(t, NIMMT - .2, NIMMT + .2)))
    mct(e, 900, 170, "§7Er nimmt sich §fje eine Scherbe", 4, ein * aus_kubisch(phase(t, NIMMT + .4, NIMMT + .8)))
    mct(e, 900, 820, "§7Truhe, Redstone-Truhe oder Fass", 4, ein * aus_kubisch(phase(t, 2.6, 3.0)))
    mct(e, 900, 870, "§7waagerecht §fdirekt neben §7ihm", 4, ein * aus_kubisch(phase(t, 2.6, 3.0)))


FERTIG_B = 4.1


def szene_backen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, 1340, GOL_B, ein, breite=15)
    setze_block(e, "kiste", 80, TRUHE_X, TRUHE_U, ein)
    fortschritt = phase(t, .4, FERTIG_B - .3)
    if t < FERTIG_B:
        golem(e, "fgolem_work", t, GOL_X, GOL_B, GOL_G, ein)
        glimmen(e, *ofen(GOL_X, GOL_B, GOL_G), t, ein)
        faden(e, *kopf(GOL_X, GOL_B, GOL_G), t, ein)
        staub(e, GOL_X, GOL_B, t, ein * (.3 + .7 * fortschritt), n=int(5 + 9 * fortschritt))
    else:
        golem(e, "fgolem_done", t - FERTIG_B, GOL_X, GOL_B, GOL_G, ein, schleife=False) if t < FERTIG_B + .9 \
            else golem(e, "fgolem_idle", t, GOL_X, GOL_B, GOL_G, ein)
        funkenkranz(e, GOL_X, golem_mitte(GOL_B, GOL_G) - 20, t, FERTIG_B, radius=120, n=8, farbe=(255, 255, 255))
        regen(e, GOL_X, golem_mitte(GOL_B, GOL_G) - 160, t, FERTIG_B, ein)
    zeit_tafel(e, 120 * (1 - fortschritt), ein * aus_kubisch(phase(t, .3, .7)), x=1580, y=170)
    mana_ruby(e, 1860, 800, 115 if t < FERTIG_B + .1 else 116, 500, 4, ein)
    u = phase(t, FERTIG_B + .1, FERTIG_B + 1.6)
    if 0 < u < 1:
        mct(e, 1700, 846 - 60 * u, "§d+1 Mana", 5, ein * math.sin(math.pi * min(1, u * 1.4)), anker="r")
    mct(e, 900, 820, "§d1 Mana §7je Scherbe, §fauch offline", 4, ein * aus_kubisch(phase(t, FERTIG_B + .8, FERTIG_B + 1.2)))


LIMIT_ZEITEN = (2.6, 3.6)
RUHE = 5.2
LIMIT_GOLEMS = ((1110, 600, 3.6), (1560, 600, 2.6))


def szene_limit(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    heute = 18 + sum(1 for t0 in LIMIT_ZEITEN if t >= t0)
    for i, (cx, boden, t0) in enumerate(LIMIT_GOLEMS):
        buehne(e, cx, boden, ein, seed=35 + i, breite=10)
        if t < t0:
            golem(e, "fgolem_work", t, cx, boden, 280, ein)
            glimmen(e, *ofen(cx, boden, 280), t, ein, n=5, breite=40, seed=3 + i)
        elif t < RUHE:
            golem(e, "fgolem_done", t - t0, cx, boden, 280, ein, schleife=False)
            funkenkranz(e, cx, golem_mitte(boden, 280) - 20, t, t0, radius=100, n=7, farbe=(255, 255, 255))
        else:
            golem(e, "fgolem_rest", t - RUHE, cx, boden, 280, ein)
            if t < RUHE + 1.4:  # der rosa Seufzer am Limit, matter als beim Backen
                glimmen(e, *ofen(cx, boden, 280), t - RUHE, ein * (1 - phase(t, RUHE + .8, RUHE + 1.4)), n=5,
                        breite=40, seed=7 + i, farben=(MANA_DIM,))
            sx, sy = kopf(cx, boden, 280)
            zzz(e, sx + 50, sy + 7, t, ein * aus_kubisch(phase(t, RUHE + .6, RUHE + 1.0)))
    tip = ("§bTageslimit", f"§7Heute: §f{heute}§7/§f20 §7Scherben", f"§8Gilt für alle Golems von {ERBAUER}.",
           "§8Neues Limit um 04:00 Uhr.")
    mc.einfuegen(e, mc.tooltip_bild(tip, 3), 1120, 160, ein * aus_kubisch(phase(t, .3, .7)))
    mct(e, 900, 870, "§7Ruhe bis zum §fTageswechsel", 4, ein * aus_kubisch(phase(t, RUHE + 1.6, RUHE + 2.0)))


BESTAETIGT = 2.9
WEG = 4.3  # Golem verschwindet, die drei Bloecke fallen heraus
CONFIRM = {11: "golem_confirm", 13: "golem_dismantle", 15: "close"}
AB_X, AB_B, AB_G = 1330, 560, 340


def szene_abbauen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    tipps = {13: (f"§dFurnace Golem von {ERBAUER}", "§7Kürbis, Ofen, Mana-Block und", "§7eine gehaltene Scherbe fallen.",
                  "§7Dein Konto bleibt, wie es ist."),
             11: ("§aJa, abbauen", "§7Der Golem verschwindet.", "§8Klick zum Abbauen")}
    zu = 1 - phase(t, BESTAETIGT + .2, BESTAETIGT + .5)
    if zu > 0:
        menue_mit_zeiger(e, t, "§c§lGolem abbauen?", 3, CONFIRM, tipps, [(.3, .9, 13), (2.0, 2.5, 11)],
                         900, 300, MS, ein * zu)
        x, y = slot_mitte(11, 900, 300, MS)
        klick(e, t, BESTAETIGT, x, y, ein)
    da = ein * aus_kubisch(phase(t, BESTAETIGT + .3, BESTAETIGT + .7))
    buehne(e, AB_X, AB_B, da)
    if t < WEG:
        golem(e, "fgolem_start", t - (WEG - 1.2), AB_X, AB_B, AB_G, da * (1 - phase(t, WEG - .15, WEG)),
              schleife=False) if t >= WEG - 1.2 else golem(e, "fgolem_idle", t, AB_X, AB_B, AB_G, da)
    else:
        funkenkranz(e, AB_X, golem_mitte(AB_B, AB_G), t, WEG, radius=110, n=8, farbe=(255, 255, 255))
    items = [block("kuerbis", 44), block("ofen", 44), mc.icon16("mana_block")]
    for i, item in enumerate(items):
        von = (AB_X - 70 + i * 70, golem_mitte(AB_B, AB_G) - 30 * (i == 1))
        u = phase(t, WEG + .3 + i * .15, WEG + 1.1 + i * .15)
        if t >= WEG and u <= 0:
            s = rueckschwung(phase(t, WEG, WEG + .3))
            skaliert(e, item, von[0], von[1], 64 * s, alpha=ein)
        flug(e, item, von, hotbar_mitte(i), u, ein, 64)
    hotbar(e, {i: item for i, item in enumerate(items) if t >= WEG + 1.1 + i * .15},
           ein * aus_kubisch(phase(t, BESTAETIGT + .3, BESTAETIGT + .7)))
    chat(e, 110, 905, chatzeilen([(WEG + .1, "§aDer Furnace Golem ist abgebaut.")]), t, 3, ein)


def szene_outro(e, t, d):
    titelkarte(e, t, "Frohes Backen!", "Alles Weitere steht im Wiki unter Furnace Golem", y=150)
    u = rueckschwung(phase(t, .5, 1.0))
    if u > 0:
        golem(e, "fgolem_play", t, W / 2, 740, 420 * u)
    mb_logo(e, W / 2, 860, 140, aus_kubisch(phase(t, 1.4, 2.0)))


SZENEN = [
    dict(dauer=9.6, zeichne=szene_intro, ton=[(.2, "sfx:chime"), (.7, "sfx:pop", .6)] + erzaehlt(1.2, "furnace_golem-intro")),
    dict(dauer=8.8, nr="01", kicker="Rezept", titel="Der Mana-Block",
         text="Acht Mana-Kugeln um eine Mana-Ladung. Ein Block ist 17 Mana wert, in Kugeln zurück craften lässt er sich nicht.",
         zeichne=szene_block, ton=werkbank_ton(ZEITEN_BLOCK) + erzaehlt(.4, "furnace_golem-block")),
    dict(dauer=9.6, nr="02", kicker="Bauen", titel="Drei Blöcke, ein Golem",
         text="Unten der Mana-Block, darauf ein Ofen, zuletzt ein geschnitzter Kürbis. Du kannst so viele bauen, wie du willst.",
         zeichne=szene_bauen, ton=[(t0, "sfx:pop", .8) for t0, _ in BAU] + [(FERTIG, "sfx:funkeln"), (FERTIG + .5, "sfx:erfolg", .6)]
         + erzaehlt(.4, "furnace_golem-bauen")),
    dict(dauer=8.6, nr="03", kicker="Menü", titel="Mana aufs Konto",
         text="Rechtsklick öffnet sein Menü. Kugeln und Mana-Blöcke zahlst du dort ein, ein Block zählt 17 Mana.",
         zeichne=szene_einzahlen, ton=[(EIN_1, "sfx:klick"), (EIN_1 + .1, "sfx:funkeln", .6), (EIN_2, "sfx:klick"),
                                       (EIN_2 + .1, "sfx:funkeln", .6)] + erzaehlt(.4, "furnace_golem-einzahlen")),
    dict(dauer=7.6, nr="04", kicker="Abheben", titel="Mana zurück in die Hand",
         text="Nur als Mana-Kugeln, so viel ins Inventar passt. Abheben ist nicht begrenzt.",
         zeichne=szene_abheben, ton=[(AB_1, "sfx:klick"), (AB_1 + .2, "sfx:pop", .5), (AB_2, "sfx:klick"),
                                     (AB_2 + .2, "sfx:pop", .5)] + erzaehlt(.4, "furnace_golem-abheben")),
    dict(dauer=9.8, nr="05", kicker="Mana-Geode", titel="Ein Kristall in der Höhle",
         text="Auf dem Höhlenboden vieler Inseln liegt Knospender Mana-Amethyst. Der Kristall darauf wächst in vier Stufen.",
         zeichne=szene_geode, ton=[(t0, "sfx:funkeln", .5) for t0 in STUFEN] + erzaehlt(.4, "furnace_golem-geode")),
    dict(dauer=8.0, nr="06", kicker="Abbauen", titel="Die Mana-Scherbe",
         text="Nur der ausgewachsene Kristall gibt eine Mana-Scherbe. Danach wächst eine neue Knospe.",
         zeichne=szene_scherbe, ton=[(SCHLAG + i * .2, "sfx:klick", .3) for i in range(4)]
         + [(BRUCH, "sfx:funkeln"), (BRUCH + .9, "sfx:pop", .6)] + erzaehlt(.4, "furnace_golem-scherbe")),
    dict(dauer=8.0, nr="07", kicker="Truhe", titel="Scherben neben den Golem",
         text="Leg die Scherben in eine Truhe oder ein Fass direkt neben ihm. Er holt sie sich selbst.",
         zeichne=szene_truhe, ton=[(REIN, "sfx:klick"), (NIMMT, "sfx:funkeln", .7)] + erzaehlt(.4, "furnace_golem-truhe")),
    dict(dauer=8.8, nr="08", kicker="Backen", titel="Aus einer Scherbe wird Mana",
         text="Jede Scherbe backt er 120 Sekunden lang. Das Mana bekommt, wer ihn gebaut hat, auch wenn er gerade offline ist.",
         zeichne=szene_backen, ton=[(FERTIG_B, "sfx:funkeln"), (FERTIG_B + .1, "sfx:erfolg", .6)]
         + erzaehlt(.4, "furnace_golem-backen")),
    dict(dauer=8.8, nr="09", kicker="Tageslimit", titel="20 Scherben am Tag",
         text="Das Limit gilt für alle deine Golems zusammen. Danach döst er bis zum Tageswechsel um 4 Uhr.",
         zeichne=szene_limit, ton=[(t0, "sfx:funkeln", .6) for t0 in LIMIT_ZEITEN] + erzaehlt(.4, "furnace_golem-limit")),
    dict(dauer=7.4, nr="10", kicker="Umziehen", titel="Über das Menü abbauen",
         text="Kürbis, Ofen und Mana-Block bekommst du zurück. Dein Konto bleibt, wie es ist.",
         zeichne=szene_abbauen, ton=[(BESTAETIGT, "sfx:klick"), (WEG, "sfx:whoosh", .6)]
         + [(WEG + 1.1 + i * .15, "sfx:pop", .5) for i in range(3)]
         + erzaehlt(.4, "furnace_golem-abbauen")),
    dict(dauer=5.0, zeichne=szene_outro, ton=[(.3, "sfx:chime", .8)] + erzaehlt(.5, "furnace_golem-outro")),
]

FILM = Film("furnace_golem", SZENEN, musik=dict(tonart="F", tempo=88, stimmung="hell"))
FILM.poster = sum(s["dauer"] for s in SZENEN[:8]) + 5.0
