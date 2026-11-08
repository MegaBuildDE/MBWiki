#!/usr/bin/env python3
"""Bilder fuer sb/feder.md und en/feather.md: die Items und das Spawner-Rezept.

Feder und Spawner-Fragment kommen frisch aus dem Pool (MBSKY_POOLS, assets/items/sonstige),
die Mobplate aus assets/items/mobplates, der Spawner aus dem neuesten Client-Jar. Das Raster
zeichnet tools/mobplate_bilder.py. Ein neues Bild im Pool heisst: dieses Skript noch einmal
laufen lassen.

Die Feder bekommt bewusst kein Rezeptbild, solange Kay sie nicht freigibt.

    python3 tools/feder_bilder.py
"""
import glob
import io
import os
import zipfile

from PIL import Image

import mobplate_bilder as mb

AUS = os.path.join(os.path.dirname(mb.HIER), ".gitbook", "assets", "feder")


def spawner(px=mb.ITEM):
    jar = max(glob.glob(mb.JARS), key=os.path.getmtime)
    with zipfile.ZipFile(jar) as z:
        roh = z.read("assets/minecraft/textures/block/spawner.png")
    return Image.open(io.BytesIO(roh)).convert("RGBA").resize((px, px), Image.NEAREST)


def reihe(bilder):
    """Feder, Fragment und Spawner nebeneinander, fuer den Kopf der Seite. Heller Grund wie im
    Inventar, weil Fragment und Spawner auf dem dunklen der Mana-Items verschwinden."""
    zelle, rand = 120, 24
    b = Image.new("RGBA", (len(bilder) * zelle + 2 * rand - 24, zelle - 24 + 2 * rand), mb.FLAECHE)
    for i, bild in enumerate(bilder):
        mb.slot(b, rand + i * zelle, rand, bild, 96)
    b.save(os.path.join(AUS, "items.png"))


def main():
    os.makedirs(AUS, exist_ok=True)
    mb.AUS = AUS
    fragment = mb.pool_bild("sonstige/spawner_fragment.png")
    kuh = mb.pool_bild("mobplates/cow.png")
    mb.rezept(kuh, fragment, spawner(), "rezept-spawner.png")
    reihe([mb.pool_bild("sonstige/feather_of_softness.png", 80),
           mb.pool_bild("sonstige/spawner_fragment.png", 80),
           spawner(80)])
    print("Bilder in", AUS)


if __name__ == "__main__":
    main()
