#!/usr/bin/env python3
"""Bilder fuer sb/mobplates.md und en/mobplates.md: alle Plates und die zwei Rezepte.

Die Plates kommen frisch aus dem Pool (MBSKY_POOLS, assets/items/mobplates), Ziegel und
Toepferscherbe aus dem neuesten Client-Jar. Ein neues Bild im Pool heisst: dieses Skript
noch einmal laufen lassen.

    python3 tools/mobplate_bilder.py
"""
import glob
import io
import os
import zipfile

from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
AUS = os.path.join(os.path.dirname(HIER), ".gitbook", "assets", "mobplates")
POOL = os.path.join(os.environ.get("MBSKY_POOLS", os.path.expanduser("~/Coding/pools")), "assets", "items")
PLATES = os.path.join(POOL, "mobplates")
JARS = os.path.expanduser("~/Library/Application Support/minecraft/versions/*/*.jar")

SLOT = 72  # Platz im Raster
ITEM = 56
FLAECHE = (198, 198, 198, 255)
HELL, DUNKEL, INNEN = (255, 255, 255, 255), (55, 55, 55, 255), (139, 139, 139, 255)


def pool_bild(pfad, px=ITEM):
    return Image.open(os.path.join(POOL, pfad)).convert("RGBA").resize((px, px), Image.NEAREST)


def jar_bild(name, px=ITEM):
    jar = max(glob.glob(JARS), key=os.path.getmtime)
    with zipfile.ZipFile(jar) as z:
        roh = z.read("assets/minecraft/textures/item/" + name + ".png")
    return Image.open(io.BytesIO(roh)).convert("RGBA").resize((px, px), Image.NEAREST)


def slot(ziel, x, y, item=None, groesse=SLOT):
    z = ImageDraw.Draw(ziel)
    z.rectangle((x, y, x + groesse - 1, y + groesse - 1), fill=INNEN)
    z.rectangle((x, y, x + groesse - 1, y + 3), fill=DUNKEL)
    z.rectangle((x, y, x + 3, y + groesse - 1), fill=DUNKEL)
    z.rectangle((x, y + groesse - 4, x + groesse - 1, y + groesse - 1), fill=HELL)
    z.rectangle((x + groesse - 4, y, x + groesse - 1, y + groesse - 1), fill=HELL)
    if item is not None:
        ziel.alpha_composite(item, (x + (groesse - item.width) // 2, y + (groesse - item.height) // 2))


def pfeil(ziel, x, y):
    z = ImageDraw.Draw(ziel)
    z.rectangle((x, y - 8, x + 44, y + 7), fill=INNEN)
    z.polygon([(x + 44, y - 24), (x + 76, y), (x + 44, y + 23)], fill=INNEN)


def rezept(mitte, rund, ergebnis, name):
    rand = 24
    breite = rand * 2 + 3 * SLOT + 24 + 76 + 24 + 96
    hoehe = rand * 2 + 3 * SLOT
    b = Image.new("RGBA", (breite, hoehe), FLAECHE)
    for i in range(9):
        slot(b, rand + i % 3 * SLOT, rand + i // 3 * SLOT, mitte if i == 4 else rund)
    pfeil(b, rand + 3 * SLOT + 24, hoehe // 2)
    slot(b, breite - rand - 96, (hoehe - 96) // 2, ergebnis.resize((72, 72), Image.NEAREST), 96)
    b.save(os.path.join(AUS, name))


def alle():
    namen = sorted(f for f in os.listdir(PLATES) if f.endswith(".png"))
    spalten, zelle = 12, 72
    zeilen = (len(namen) + spalten - 1) // spalten
    b = Image.new("RGBA", (spalten * zelle + 16, zeilen * zelle + 16), (22, 30, 58, 255))
    for i, f in enumerate(namen):
        im = Image.open(os.path.join(PLATES, f)).convert("RGBA").resize((64, 64), Image.NEAREST)
        b.alpha_composite(im, (12 + i % spalten * zelle, 12 + i // spalten * zelle))
    b.save(os.path.join(AUS, "alle.png"))
    return len(namen)


def main():
    os.makedirs(AUS, exist_ok=True)
    blass = pool_bild("mobplates/vorlagen/mob_pre_template.png")
    leer = pool_bild("mobplates/vorlagen/mob_template.png")
    rezept(jar_bild("angler_pottery_sherd"), jar_bild("brick"), blass, "rezept-scherbe.png")
    rezept(blass, pool_bild("mana/mana.png"), leer, "rezept-plate.png")
    print(alle(), "Plates")


if __name__ == "__main__":
    main()
