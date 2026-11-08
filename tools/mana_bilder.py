#!/usr/bin/env python3
"""Bilder fuer sb/mana-items.md und en/mana-items.md: die Mana-Items und ihre Rezepte.

Die Texturen kommen frisch aus dem Pool (MBSKY_POOLS, assets/items/mana), der Apfel aus dem
neuesten Client-Jar. Ein neues Bild im Pool heisst: dieses Skript noch einmal laufen lassen.

    python3 tools/mana_bilder.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mobplate_bilder import FLAECHE, SLOT, jar_bild, pfeil, pool_bild, slot  # noqa: E402

AUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".gitbook", "assets", "mana")


def anzahl(ziel, x, y, n, groesse):
    """Stapelzahl unten rechts im Platz, wie im Spiel."""
    if n <= 1:
        return
    z = ImageDraw.Draw(ziel)
    try:
        schrift = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", groesse // 3)
    except OSError:
        schrift = ImageFont.load_default()
    text = str(n)
    box = z.textbbox((0, 0), text, font=schrift)
    tx = x + groesse - 8 - (box[2] - box[0])
    ty = y + groesse - 10 - (box[3] - box[1]) - box[1]
    z.text((tx + 3, ty + 3), text, font=schrift, fill=(63, 63, 63, 255))
    z.text((tx, ty), text, font=schrift, fill=(255, 255, 255, 255))


def rezept(raster, ergebnis, name, menge=1):
    """raster: neun Items (oder None) zeilenweise."""
    rand = 24
    breite = rand * 2 + 3 * SLOT + 24 + 76 + 24 + 96
    hoehe = rand * 2 + 3 * SLOT
    b = Image.new("RGBA", (breite, hoehe), FLAECHE)
    for i, item in enumerate(raster):
        slot(b, rand + i % 3 * SLOT, rand + i // 3 * SLOT, item)
    pfeil(b, rand + 3 * SLOT + 24, hoehe // 2)
    ex, ey = breite - rand - 96, (hoehe - 96) // 2
    slot(b, ex, ey, ergebnis.resize((72, 72), Image.NEAREST), 96)
    anzahl(b, ex, ey, menge, 96)
    b.save(os.path.join(AUS, name))


def reihe():
    """Die drei Items nebeneinander, fuer den Kopf der Seite."""
    namen = ["mana.png", "mana_charge.png", "mana_apple.png"]
    zelle = 112
    b = Image.new("RGBA", (len(namen) * zelle + 16, zelle + 16), (22, 30, 58, 255))
    for i, f in enumerate(namen):
        b.alpha_composite(pool_bild("mana/" + f, 96), (16 + i * zelle, 16))
    b.save(os.path.join(AUS, "items.png"))


def main():
    os.makedirs(AUS, exist_ok=True)
    kugel = pool_bild("mana/mana.png")
    ladung = pool_bild("mana/mana_charge.png")
    apfel_mana = pool_bild("mana/mana_apple.png")
    apfel = jar_bild("apple")
    rezept([kugel] * 9, ladung, "rezept-ladung.png")
    rezept([None, None, None, None, ladung, None, None, None, None], kugel, "rezept-zerlegen.png", 9)
    rezept([None, kugel, None, kugel, apfel, kugel, None, kugel, None], apfel_mana, "rezept-apfel.png")
    reihe()
    print("Bilder in", AUS)


if __name__ == "__main__":
    main()
