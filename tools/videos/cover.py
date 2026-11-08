#!/usr/bin/env python3
"""Cover (Vorschaubilder) zu den Wiki-Filmen: links Titel und worum es geht, rechts gross
eine Figur aus dem Film, am unteren Bildrand angeschnitten. 1920 x 1080, z. B. fuer Discord.

Die Figuren kommen gross gerendert aus modelle.py:

    python3 modelle.py --groesse 1536 goblin_cover shroom_cover golem_cover mala_cover warpett_cover forest_cover
    python3 cover.py [film ...]          -> build/cover/<film>.jpg
    python3 cover.py --vorne ORDNER      Cover als erste Sekunde vor ORDNER/<film>.mp4 setzen
                                         (Discord zeigt das erste Bild als Vorschau)
"""
import os
import subprocess
import sys

from PIL import Image

import mc
from basis import (SPRITES, BLENDE, WORTMARKE, av, funkeln, glanz,
                   skaliert, wappen_bei)

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HIER, "build", "cover")
TEXT_X = 110


def figur(f, name, bild, cx, oben, hoehe, spiegeln=False):
    """Sprite-Bild auf den sichtbaren Teil beschnitten, Oberkante bei oben, hoehe in Pixeln."""
    im = Image.open(os.path.join(SPRITES, name, f"{bild:03d}.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    if spiegeln:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    breite = hoehe * im.width / im.height
    im = im.resize((round(breite), round(hoehe)), Image.LANCZOS)
    mc.einfuegen(f, im, cx - breite / 2, oben)


def licht(f, cx, cy, radius, farbe, staerke=150):
    g = glanz(radius, farbe, staerke)
    mc.einfuegen(f, g, cx - radius, cy - radius)


def text(f, kicker, titel, unter, punkte):
    y = 330
    av(f, kicker, TEXT_X, y, 30, "demi", (85, 255, 255), sperrung=4)
    y += 62
    for zeile in titel:
        av(f, zeile, TEXT_X, y, 132, "heavy", (255, 255, 255), schatten=.6)
        y += 140
    y += 20
    av(f, unter, TEXT_X, y, 44, "medium", (214, 228, 248), schatten=.5)
    y += 86
    for p in punkte:
        av(f, "•  " + p, TEXT_X + 4, y, 34, "medium", (196, 214, 240), schatten=.5)
        y += 52


def rahmen():
    from basis import hintergrund
    f = hintergrund(0).convert("RGBA")
    mc.einfuegen(f, BLENDE, 0, 0, 1.0)
    return f


def abschluss(f):
    mc.einfuegen(f, WORTMARKE, 40, 22, .95)
    # Hinweis unten links: Mala erklaert, also mit Ton
    av(f, "Mala erklärt  ·  Ton an", TEXT_X, 960, 32, "demi", (255, 222, 130), schatten=.5)
    return f


def bewohner():
    f = rahmen()
    licht(f, 1420, 560, 620, (120, 255, 160), 120)
    figur(f, "shroom_cover", 15, 1790, 500, 500, spiegeln=True)
    figur(f, "goblin_cover", 10, 1430, 200, 1050)
    text(f, "KI-BEWOHNER", ["Deine Insel", "lebt"], "Nachbarn, die mit dir reden",
         ["Goblins und Shroomlinge im Chat", "Vertrauen aufbauen und handeln", "Forestlinge und ihr Segen"])
    return abschluss(f)


def skilltree():
    f = rahmen()
    licht(f, 1400, 520, 640, (230, 110, 255), 140)
    figur(f, "golem_cover", 0, 1400, 150, 1080)
    orb = mc.icon16("mana_orb")
    for cx, cy, g in ((1010, 360, 120), (1800, 300, 96), (1760, 760, 140), (1050, 820, 84)):
        skaliert(f, orb, cx, cy, g)
    for cx, cy, g in ((960, 250, 26), (1850, 520, 22), (1690, 140, 30), (1110, 600, 18)):
        funkeln(f, cx, cy, g, 1.0)
    text(f, "SKILLTREE", ["Mana &", "Biome"], "So wächst deine Inselwelt",
         ["Mana verdienen: Quests, Votes, Erz", "Acht Kristall-Pfade im Skilltree", "Biomquest, dann neues Biom"])
    return abschluss(f)


def clans():
    f = rahmen()
    licht(f, 1400, 560, 640, (85, 200, 255), 130)
    wappen_bei(f, "#FF5555", "flamme", 1080, 700, 300)
    wappen_bei(f, "#5555FF", "anker", 1750, 690, 300)
    wappen_bei(f, "#55FF55", "pilz", 1415, 560, 560)
    for cx, cy, g in ((1180, 300, 28), (1690, 330, 24), (1880, 900, 22), (1010, 950, 20)):
        funkeln(f, cx, cy, g, 1.0)
    av(f, "NBW", 1415, 870, 96, "heavy", (85, 255, 85), schatten=.6, anker="m")
    text(f, "CLANSYSTEM", ["Clans"], "Gemeinsam mehr erreichen",
         ["Kürzel, Farbe und Wappen", "Clan-Chat über alle Server", "Wochenauftrag und Clan-Stufen"])
    return abschluss(f)


def start():
    f = rahmen()
    licht(f, 1400, 560, 640, (255, 160, 240), 130)
    figur(f, "warpett_cover", 0, 1800, 600, 440)
    figur(f, "mala_cover", 20, 1460, 170, 1100)
    text(f, "DEIN START", ["Dein Start"], "Von der Lobby bis zur Insel",
         ["Startbiom wählen", "Mit Mala im Luftschiff", "Der erste Bewohner"])
    return abschluss(f)


def plate(name):
    return Image.open(os.path.join(mc.POOL, "assets", "items", "mobplates", name + ".png")).convert("RGBA")


def mobplates():
    f = rahmen()
    licht(f, 1400, 540, 640, (255, 105, 200), 140)
    skaliert(f, plate("enderman"), 1400, 520, 544)
    for name, cx, cy, g in (("sheep", 1040, 300, 160), ("cat", 1780, 280, 176), ("villager", 1790, 800, 160),
                            ("creeper", 1040, 800, 176)):
        skaliert(f, plate(name), cx, cy, g)
    for cx, cy, g in ((1180, 170, 28), (1640, 150, 24), (1880, 540, 22), (960, 560, 20)):
        funkeln(f, cx, cy, g, 1.0)
    text(f, "MOBPLATES", ["Mobs", "einfangen"], "Und woanders wieder freisetzen",
         ["Leere Plate craften", "Mob markieren und besiegen", "127 Plates, vom Huhn bis zum Enderman"])
    return abschluss(f)


def forestlinge():
    f = rahmen()
    licht(f, 1400, 560, 640, (140, 230, 120), 130)
    figur(f, "forest_cover", 20, 1420, 200, 850)
    apfel = mc.icon16("mana_apple")
    for cx, cy, g in ((1010, 330, 120), (1820, 300, 96), (1800, 780, 120)):
        skaliert(f, apfel, cx, cy, g)
    for cx, cy, g in ((960, 230, 26), (1860, 520, 22), (1690, 140, 30), (1080, 620, 18)):
        funkeln(f, cx, cy, g, 1.0)
    text(f, "FORESTLINGE", ["Forestlinge"], "Kleine Waldelfen mit einem Segen",
         ["Segen gegen Mana und einen Mana-Apfel", "Sprünge von Insel zu Insel", "Mit der Mobplate mitnehmen"])
    return abschluss(f)


COVER = {"bewohner": bewohner, "skilltree": skilltree, "clans": clans, "start": start, "mobplates": mobplates,
         "forestlinge": forestlinge}


VORNE_S = 1.2  # so lange steht das Cover vor dem Film, dann geht er mit einer kurzen Blende los


def vorne(ordner, name):
    """Cover vor die fertige MP4 setzen (scharfe Fassung, crf 16). Laeuft auf derselben Datei
    zweimal nicht doppelt: das Original wird als <film>.ohne-cover.mp4 daneben gehalten."""
    mp4 = os.path.join(ordner, name + ".mp4")
    roh = os.path.join(ordner, name + ".ohne-cover.mp4")
    if not os.path.isfile(roh):
        os.replace(mp4, roh)
    bild = os.path.join(ZIEL, name + ".jpg")
    filter_ = (f"[0:v]scale=1920:1080,fps=30,format=yuv420p,setsar=1,settb=1/30[c];[1:v]fps=30,setsar=1,settb=1/30[f];"
               f"[c][f]xfade=transition=fade:duration=0.4:offset={VORNE_S - .4:.2f}[v];"
               f"[1:a]adelay={int((VORNE_S - .4) * 1000)}:all=1[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(VORNE_S), "-i", bild, "-i", roh,
                    "-filter_complex", filter_, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow",
                    "-tune", "animation", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", mp4], check=True)
    print(mp4)


def main():
    if sys.argv[1:2] == ["--vorne"]:
        ordner = sys.argv[2]
        for name in sys.argv[3:] or list(COVER):
            if any(os.path.isfile(os.path.join(ordner, name + e)) for e in (".mp4", ".ohne-cover.mp4")):
                vorne(ordner, name)
        return
    namen = sys.argv[1:] or list(COVER)
    os.makedirs(ZIEL, exist_ok=True)
    for name in namen:
        pfad = os.path.join(ZIEL, name + ".jpg")
        COVER[name]().convert("RGB").save(pfad, quality=92)
        print(pfad)


if __name__ == "__main__":
    main()
