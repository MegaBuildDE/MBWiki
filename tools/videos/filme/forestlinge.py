#!/usr/bin/env python3
"""Forestlinge auf MegaBuild Skyblock: finden, Segen mit dem Mana-Apfel, mitnehmen mit der Mobplate.

Inhalt nach MBSkyManager/docs/FORESTLINGE.md (Stand 08.11.2026: Mana-Apfel statt „ja“, Apfel in
der Hand, Einfangen mit der Mobplate). Saetze der Forestlinge aus lang/de.yml (forestling.*).
Die Modelle kommen aus modelle.py (forest_*), der Apfel in der Hand ist der im Modell verborgene
Knochen apple (ZEIGEN in modelle.py). Mala erklaert jede Szene (nur Deutsch).

    python3 modelle.py forest_oak_apfel forest_oak_apfel_happy forest_spruce forest_jungle \\
        forest_acacia forest_darkoak forest_paleoak forest_bamboo
    python3 bauen.py forestlinge
"""
import functools
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403
from mobplates import Z, flug, hand, hotbar, hotbar_mitte, jar, plate, slot_bild  # noqa: E402

GRUEN = (160, 255, 160)
PINK = (255, 105, 200)
NAME = "§aEichen-Waldelf§7: §f"


@functools.lru_cache(maxsize=None)
def plate_forestling():
    return Image.open(os.path.join(mc.POOL, "assets", "items", "mobplates", "forestling.png")).convert("RGBA")


@functools.lru_cache(maxsize=None)
def insel(seed, gras=(88, 160, 64), gras_h=(118, 190, 82), breite=13):
    return insel_bild(breite, 4, seed, 30, gras=gras, gras_h=gras_h, baum=False)


def buehne(e, cx, boden, alpha, seed=31, **farben):
    bild = insel(seed, **farben)
    mc.einfuegen(e, bild, cx - bild.width / 2, boden, alpha)


def apfel():
    return mc.icon16("mana_apple")


# ── Szenen ──────────────────────────────────────────────────────────────────

RUNDE = ["forest_oak", "forest_spruce", "forest_birch", "forest_jungle", "forest_acacia", "forest_mangrove",
         "forest_cherry", "forest_paleoak", "forest_bamboo", "forest_darkoak"]


def szene_intro(e, t, d):
    titelkarte(e, t, "Forestlinge", "Kleine Waldelfen mit einem Segen", y=110)
    n = len(RUNDE)
    for i, name in enumerate(RUNDE):
        s = rueckschwung(phase(t, .9 + i * .14, 1.4 + i * .14))
        if s <= 0:
            continue
        x = 250 + i * (W - 500) / (n - 1)
        boden = 820 + 30 * math.sin(i * 1.3) + 6 * math.sin(t * 2 + i)
        sprite_boden(e, name, t + i * .3, x, boden, 230 * s, spiegeln=i % 2 == 1)


ARTEN = [("forest_oak", "§aEiche", "§7Wald, Ebene", 31, {}),
         ("forest_cherry", "§dKirsche", "§7Kirschhain", 36, dict(gras=(222, 150, 190), gras_h=(240, 180, 210))),
         ("forest_spruce", "§aFichte", "§7Taiga", 41, dict(gras=(70, 120, 80), gras_h=(96, 146, 104)))]


def szene_finden(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    for i, (name, art, biom, seed, farben) in enumerate(ARTEN):
        u = aus_kubisch(phase(t, .3 + i * .5, .8 + i * .5))
        x, boden = 1060 + i * 330, 470 + (i % 2) * 90
        mc.einfuegen(e, insel(seed, breite=9, **farben), x - 135, boden + (1 - u) * 40, ein * u)
        s = rueckschwung(phase(t, 1.0 + i * .5, 1.5 + i * .5))
        if s > 0:
            sprite_boden(e, name, t + i * .4, x, boden + 4, 190 * s, ein)
            mct(e, x, boden - 230, art, 4, ein * min(1, s), anker="m")
            mct(e, x, boden - 190, biom, 3, ein * min(1, s), anker="m")
    for i, (t0, zeile) in enumerate(((3.6, "§fHöchstens einer §7je Insel"),
                                     (4.6, "§7Nie auf deiner §fStartinsel"))):
        mct(e, 900, 780 + i * 50, zeile, 4, ein * aus_kubisch(phase(t, t0, t0 + .4)))


CX, BODEN = 1330, 600
KLICK_G = 1.4


def gespraech_zeilen(t0):
    return [(t0, NAME + "Eichen wachsen langsam – aber sie springen hoch, wenn man sie lässt."),
            (t0 + 1.6, NAME + "Mein Segen heißt Himmelsprung. 120 Sekunden lang wird jeder Sprung mit Anlauf "
                              "zum Riesensprung: rund 60 Blöcke weit, bis zur nächsten Insel."),
            (t0 + 3.6, NAME + "Er kostet 20 Mana, du hast 57. Magst du ihn? Dann gib mir einen §dMana-Apfel§f.")]


def szene_ansprechen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN, ein)
    sprite_boden(e, "forest_oak_happy" if KLICK_G <= t < KLICK_G + 2 else "forest_oak", t, CX, BODEN + 4, 300, ein)
    x, y = zeigerweg(t, [(.2, 1720, 720), (KLICK_G, CX + 20, BODEN - 140), (KLICK_G + 1.0, 1700, 700)])
    hand(e, x, y, None, ein * (1 - phase(t, KLICK_G + .6, KLICK_G + 1.0)))
    klick(e, t, KLICK_G, CX + 20, BODEN - 140, ein)
    chat(e, 880, 905, chatzeilen(gespraech_zeilen(KLICK_G + .5)), t, 3, ein)


ZEITEN_APFEL = (2.2, 3.4, 5.0)
KREUZ = [1, 3, 5, 7]


def szene_apfel(e, t, d):
    """Werkbank: Apfel in der Mitte, vier Mana-Kugeln darum (SkyRecipes: " M ", "MAM", " M ")."""
    ein = aus_kubisch(phase(t, 0, .4))
    t_mitte, t_rund, fertig = ZEITEN_APFEL
    x0, y0 = 930, 250
    mc.einfuegen(e, tafel(880, 400, 20), x0 - 50, y0 - 50, ein)
    for i in range(9):
        mc.einfuegen(e, slot_bild(Z), x0 + i % 3 * Z, y0 + i // 3 * Z, ein)
    s = rueckschwung(phase(t, t_mitte, t_mitte + .3))
    if s > 0:
        skaliert(e, jar("item/apple"), x0 + 1.5 * Z, y0 + 1.5 * Z, 72 * s, alpha=ein)
    for k, i in enumerate(KREUZ):
        s = rueckschwung(phase(t, t_rund + k * .25, t_rund + k * .25 + .3))
        if s > 0:
            skaliert(e, mc.icon16("mana_orb"), x0 + i % 3 * Z + Z / 2, y0 + i // 3 * Z + Z / 2, 72 * s, alpha=ein)
    pfeil = Image.new("RGBA", (116, 60), (0, 0, 0, 0))
    dr = ImageDraw.Draw(pfeil)
    dr.rectangle((0, 22, 76, 37), fill=(190, 190, 190, 255))
    dr.polygon([(76, 0), (115, 30), (76, 59)], fill=(190, 190, 190, 255))
    mc.einfuegen(e, pfeil, x0 + 3 * Z + 30, y0 + 1.5 * Z - 30, ein)
    ex, ey = x0 + 3 * Z + 190, y0 + Z / 2 - 12
    mc.einfuegen(e, slot_bild(Z + 24), ex, ey, ein)
    s = rueckschwung(phase(t, fertig, fertig + .4))
    if s > 0:
        mitte = ex + (Z + 24) / 2, ey + (Z + 24) / 2
        mc.einfuegen(e, glanz(150, PINK, 150), mitte[0] - 150, mitte[1] - 150, ein)
        skaliert(e, apfel(), mitte[0], mitte[1], 92 * s, alpha=ein)
        funkenkranz(e, mitte[0], mitte[1], t, fertig, radius=110, n=7, farbe=(255, 190, 235))
        mct(e, mitte[0], ey + Z + 56, "§dMana-Apfel", 4, ein * aus_kubisch(phase(t, fertig + .2, fertig + .6)), anker="m")
    mct(e, 930, 690, "§fApfel §7in die Mitte, §d4 Mana-Kugeln §7darum", 4, ein * aus_kubisch(phase(t, 1.4, 1.9)))
    mct(e, 930, 750, "§7Dazu der §dMana-Preis §7des Segens", 4, ein * aus_kubisch(phase(t, 5.8, 6.3)))


KLICK_A = 3.3


def szene_geben(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    BODEN = 540
    buehne(e, CX, BODEN, ein)
    name = "forest_oak_apfel_happy" if t >= KLICK_A else "forest_oak"
    sprite_boden(e, name, t - KLICK_A if t >= KLICK_A else t, CX, BODEN + 4, 300, ein)
    if t >= KLICK_A + .6:
        funkenkranz(e, CX, BODEN - 150, t, KLICK_A + .6, radius=150, n=8, farbe=GRUEN)
    x, y = zeigerweg(t, [(.6, 1720, 720), (KLICK_A, CX + 20, BODEN - 140), (KLICK_A + 1.0, 1700, 700)])
    hand(e, x, y, apfel() if t < KLICK_A else None, ein * (1 - phase(t, KLICK_A + .6, KLICK_A + 1.0)))
    klick(e, t, KLICK_A, CX + 20, BODEN - 140, ein)
    zeilen = [(.6, NAME + "Eichen wachsen langsam – aber sie springen hoch, wenn man sie lässt."),
              (2.2, NAME + "Mein Segen heißt Himmelsprung …"),
              (KLICK_A + .3, NAME + "Oh, ein Mana-Apfel! Danke dir."),
              (KLICK_A + .6, "§aHimmelsprung! §7Renn los und spring: rund §f60 Blöcke §7weit, dorthin, wohin du schaust. §f120 s§7."),
              (KLICK_A + 1.4, "§7Mana: §d57 §7→ §d37")]
    chat(e, 880, 905, chatzeilen(zeilen), t, 3, ein)
    mct(e, 900, 170, "§7Auch §fmitten im Gespräch", 4, ein * aus_kubisch(phase(t, 1.8, 2.3)))


def szene_hand(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    mc.einfuegen(e, glanz(260, PINK, 90), CX - 260, 400 - 260, ein)
    buehne(e, CX, 630, ein)
    sprite_boden(e, "forest_oak_apfel_happy", t, CX, 634, 500, ein)
    u = aus_kubisch(phase(t, 2.6, 3.0))
    mct(e, 900, 840, "§7Er hält den Apfel bis zum Kauf", 4, ein * u)
    mct(e, 900, 890, "§7und noch §feine Minute §7danach", 4, ein * u)


SPRUENGE = [("forest_oak", "§aHimmelsprung", "§760 Blöcke", 20),
            ("forest_spruce", "§aWindlauf", "§775 Blöcke", 20),
            ("forest_birch", "§fLuftsprung", "§73 × 20 Blöcke", 25),
            ("forest_jungle", "§aRankenschwinger", "§74 Ranken", 25),
            ("forest_acacia", "§6Wüstenwind", "§745 Blöcke", 25),
            ("forest_mangrove", "§cWurzelbrücke", "§760 s gehen", 30),
            ("forest_paleoak", "§7Geisterschritt", "§78 s fliegen", 30),
            ("forest_bamboo", "§eBambuskatapult", "§795 Blöcke", 30)]


def szene_spruenge(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    for i, (name, segen, was, preis) in enumerate(SPRUENGE):
        s = rueckschwung(phase(t, .3 + i * .22, .8 + i * .22))
        if s <= 0:
            continue
        x, y = 1000 + i % 4 * 230, 250 + i // 4 * 330
        sprite(e, name, t + i * .3, x, y + 6 * math.sin(t * 2.2 + i), 190 * s, ein)
        a = ein * min(1, s)
        mct(e, x, y + 100, segen, 3, a, anker="m")
        mct(e, x, y + 130, was, 3, a, anker="m")
        mct(e, x, y + 160, f"§d{preis} Mana", 3, a, anker="m")


SPRUENGE_INSEL = [("forest_cherry", "§dKirschblütensprung", "§7meist §f100–300 §7Blöcke", 30, 1110),
                  ("forest_darkoak", "§dSchattenportal", "§7meist §f300–500 §7Blöcke", 40, 1580)]


def szene_inselsprung(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    for i, (name, segen, weite, preis, x) in enumerate(SPRUENGE_INSEL):
        s = rueckschwung(phase(t, .3 + i * .6, .8 + i * .6))
        if s <= 0:
            continue
        sprite(e, name, t + i * .4, x, 380 + 8 * math.sin(t * 2 + i), 300 * s, ein, spiegeln=i == 1)
        a = ein * min(1, s)
        mct(e, x, 560, segen, 4, a, anker="m")
        mct(e, x, 606, weite, 3, a, anker="m")
        mct(e, x, 644, f"§d{preis} Mana §7· sofort", 3, a, anker="m")
        if t >= 1.4 + i * .6:
            funkenkranz(e, x, 380, t, 1.4 + i * .6, radius=170, n=8, farbe=(255, 190, 235) if i == 0 else (190, 140, 255))
    mct(e, 900, 760, "§7Nur auf Inseln, §fdie es schon gibt", 4, ein * aus_kubisch(phase(t, 3.6, 4.0)))
    mct(e, 900, 810, "§7Keine passende? §fNichts wird abgebucht", 4, ein * aus_kubisch(phase(t, 4.6, 5.0)))


def szene_regeln(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    u = aus_kubisch(phase(t, .3, .8))
    mc.einfuegen(e, tafel(960, 560, 18), 880, 170 + (1 - u) * 30, ein * u)
    zeilen = [(.9, "§fImmer nur ein Segen", "§7ein neuer ersetzt den alten"),
              (2.4, "§fApfel bleibt bei dir", "§7wenn der Kauf nicht klappt"),
              (3.9, "§fKein Rettungsschirm", "§7Luftsprung & Co. fangen nicht jeden Sturz"),
              (5.0, "§f„ja“ allein kauft nicht", "§7er bittet dann um den Apfel")]
    for i, (t0, oben, unten) in enumerate(zeilen):
        a = ein * aus_kubisch(phase(t, t0, t0 + .4))
        mct(e, 930, 210 + i * 125, oben, 5, a)
        mct(e, 930, 262 + i * 125, unten, 3, a)


KLICK_P = 2.4


def plate_tooltip():
    return ("§dMobplate: Forestling", "§7Art: §aEichen-Waldelf", "§7Rechtsklick auf einen Block: absetzen")


def szene_mobplate(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    boden = BODEN - 100
    buehne(e, CX, boden, ein)
    s = 1 - .5 * phase(t, KLICK_P, KLICK_P + .3)
    sprite_boden(e, "forest_oak", t, CX, boden + 4, 300 * s, ein * (1 - phase(t, KLICK_P, KLICK_P + .3)))
    if t >= KLICK_P:
        funkenkranz(e, CX, boden - 130, t, KLICK_P, radius=130, n=8, farbe=(255, 190, 235))
    x, y = zeigerweg(t, [(.3, 1720, 620), (KLICK_P, CX + 20, boden - 130), (KLICK_P + 1.0, 1700, 620)])
    hand(e, x, y, plate("leer") if t < KLICK_P else None, ein * (1 - phase(t, KLICK_P + .6, KLICK_P + 1.0)))
    klick(e, t, KLICK_P, CX + 20, boden - 130, ein)
    voll = plate_forestling()
    hotbar(e, {2: voll} if t >= KLICK_P + .9 else {}, ein)
    flug(e, voll, (CX, boden - 130), hotbar_mitte(2), phase(t, KLICK_P + .1, KLICK_P + .9), ein, 96)
    mx, my = hotbar_mitte(2)
    tooltip_bei(e, plate_tooltip(), mx, my, 3, ein * aus_kubisch(phase(t, 4.0, 4.4)))
    mct(e, 900, 170, "§fKein Kampf, §7kein Markieren", 4, ein * aus_kubisch(phase(t, 3.0, 3.4)))


KLICK_S = 2.0
ZWEITE = dict(gras=(214, 190, 120), gras_h=(232, 208, 140))


def szene_absetzen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    buehne(e, CX, BODEN, ein, seed=44, **ZWEITE)
    s = rueckschwung(phase(t, KLICK_S + .05, KLICK_S + .5))
    if s > 0:
        sprite_boden(e, "forest_oak_happy", t - KLICK_S, CX, BODEN + 4, 300 * s, ein)
        funkenkranz(e, CX, BODEN - 140, t, KLICK_S, radius=140, n=8, farbe=GRUEN)
    x, y = zeigerweg(t, [(.3, 1720, 720), (KLICK_S, CX, BODEN + 10), (KLICK_S + 1.0, 1700, 720)])
    hand(e, x, y, plate_forestling() if t < KLICK_S else None, ein * (1 - phase(t, KLICK_S + .6, KLICK_S + 1.0)))
    klick(e, t, KLICK_S, CX, BODEN + 10, ein)
    chat(e, 880, 905, chatzeilen([(KLICK_S + .6, NAME + "Hier ist guter Boden. Hier bleib ich.")]), t, 3, ein)
    for i, (t0, zeile) in enumerate(((3.4, "§7Fester Boden, §fzwei Blöcke §7frei"),
                                     (4.4, "§7Höchstens §f6 §7im Umkreis von §f32 §7Blöcken"),
                                     (5.4, "§7Dazu das Inselrecht §fTiere"))):
        mct(e, 900, 150 + i * 48, zeile, 4, ein * aus_kubisch(phase(t, t0, t0 + .4)))


def szene_outro(e, t, d):
    titelkarte(e, t, "Halt die Augen offen!", "Alles Weitere steht im Wiki unter Forestlinge", y=150)
    u = rueckschwung(phase(t, .5, 1.0))
    if u > 0:
        sprite_boden(e, "forest_oak_apfel_happy", t, W / 2, 720, 300 * u)
    mb_logo(e, W / 2, 860, 180, aus_kubisch(phase(t, 1.4, 2.0)))


SZENEN = [
    dict(dauer=10.0, zeichne=szene_intro, ton=[(.2, "sfx:chime"), (1.0, "pool:forestling/oak/happy", .6)]
         + erzaehlt(1.2, "forestlinge-intro")),
    dict(dauer=7.4, nr="01", kicker="Finden", titel="Auf vielen Inseln",
         text="Welche Art dort wohnt, hängt vom Biom ab. Nach einem Erscheinen dauert es eine Weile bis zum nächsten.",
         zeichne=szene_finden, ton=[(1.0, "sfx:pop", .5), (1.5, "sfx:pop", .5), (2.0, "sfx:pop", .5)]
         + erzaehlt(.4, "forestlinge-finden")),
    dict(dauer=8.6, nr="02", kicker="Ansprechen", titel="Klick ihn an",
         text="Rechtsklick oder Schlag, auf Bedrock antippen. Er stellt sich vor, nennt seinen Segen und den Preis.",
         zeichne=szene_ansprechen, ton=[(KLICK_G, "sfx:klick"), (KLICK_G + .1, "pool:forestling/oak/happy", .6)]
         + erzaehlt(.4, "forestlinge-ansprechen")),
    dict(dauer=8.6, nr="03", kicker="Rezept", titel="Der Mana-Apfel",
         text="Ein Apfel in der Mitte der Werkbank, vier Mana-Kugeln darum. Er bestätigt den Kauf, das Mana zahlst du dazu.",
         zeichne=szene_apfel, ton=[(ZEITEN_APFEL[0], "sfx:klick", .5)]
         + [(ZEITEN_APFEL[1] + k * .25, "sfx:klick", .5) for k in range(4)] + [(ZEITEN_APFEL[2], "sfx:funkeln")]
         + erzaehlt(.4, "forestlinge-apfel")),
    dict(dauer=8.4, nr="04", kicker="Segen", titel="Apfel in die Hand, anklicken",
         text="Jederzeit, auch während er noch redet. Ein „ja“ im Chat kauft nicht mehr.",
         zeichne=szene_geben, ton=[(KLICK_A, "sfx:klick"), (KLICK_A + .3, "pool:forestling/oak/happy", .6),
                                   (KLICK_A + .6, "pool:forestling/oak/bless", .8), (KLICK_A + .6, "sfx:funkeln", .7)]
         + erzaehlt(.4, "forestlinge-geben")),
    dict(dauer=7.0, nr="05", kicker="Danke!", titel="Dein Apfel in seiner Hand",
         text="Der Segen wirkt sofort. Der Forestling hält deinen Apfel noch eine Weile fest.",
         zeichne=szene_hand, ton=[(.3, "pool:forestling/oak/happy", .6)] + erzaehlt(.4, "forestlinge-hand")),
    dict(dauer=8.0, nr="06", kicker="Sprünge", titel="Über die Lücke",
         text="Acht Segen bringen dich von Insel zu Insel – springen, gleiten, klettern oder auf Wurzeln gehen.",
         zeichne=szene_spruenge, ton=[(.3 + i * .22, "sfx:pop", .4) for i in range(8)] + erzaehlt(.4, "forestlinge-spruenge")),
    dict(dauer=7.0, nr="07", kicker="Inselsprünge", titel="Direkt zu einer fernen Insel",
         text="Kirsche und Schwarzeiche bringen dich sofort zu einer zufälligen Insel.",
         zeichne=szene_inselsprung, ton=[(1.4, "sfx:funkeln", .7), (2.0, "sfx:funkeln", .7)]
         + erzaehlt(.4, "forestlinge-inselsprung")),
    dict(dauer=7.4, nr="08", kicker="Regeln", titel="Gut zu wissen",
         text="Denselben Segen erneuerst du erst in seinen letzten 10 Sekunden.",
         zeichne=szene_regeln, ton=erzaehlt(.4, "forestlinge-regeln")),
    dict(dauer=8.0, nr="09", kicker="Mobplate", titel="Ein Klick, und er ist drin",
         text="Mit einer leeren Mobplate in der Hand anklicken. Die Art steht auf der Plate.",
         zeichne=szene_mobplate, ton=[(KLICK_P, "sfx:klick"), (KLICK_P + .9, "sfx:erfolg", .6)]
         + erzaehlt(.4, "forestlinge-mobplate")),
    dict(dauer=7.6, nr="10", kicker="Absetzen", titel="Sein neues Zuhause",
         text="Rechtsklick mit der gefüllten Plate auf einen Block. Die Plate kannst du auch im ChestShop handeln.",
         zeichne=szene_absetzen, ton=[(KLICK_S, "sfx:klick"), (KLICK_S + .05, "sfx:funkeln", .8),
                                      (KLICK_S + .6, "pool:forestling/oak/happy", .6)] + erzaehlt(.4, "forestlinge-absetzen")),
    dict(dauer=5.4, zeichne=szene_outro, ton=[(.3, "sfx:chime", .8)] + erzaehlt(.5, "forestlinge-outro")),
]

FILM = Film("forestlinge", SZENEN, musik=dict(tonart="D", tempo=88, stimmung="hell"))
FILM.poster = sum(s["dauer"] for s in SZENEN[:5]) + 5.0
