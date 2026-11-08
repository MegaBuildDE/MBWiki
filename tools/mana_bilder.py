#!/usr/bin/env python3
"""Bilder fuer sb/mana-items.md, sb/furnace-golem.md und ihre en/-Seiten: die Mana-Items und ihre Rezepte.

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


def rezept(raster, ergebnis, name, menge=1, px=72):
    """raster: neun Items (oder None) zeilenweise. px: Groesse des Ergebnisses (Bloecke 64, pixelgenau)."""
    rand = 24
    breite = rand * 2 + 3 * SLOT + 24 + 76 + 24 + 96
    hoehe = rand * 2 + 3 * SLOT
    b = Image.new("RGBA", (breite, hoehe), FLAECHE)
    for i, item in enumerate(raster):
        slot(b, rand + i % 3 * SLOT, rand + i // 3 * SLOT, item)
    pfeil(b, rand + 3 * SLOT + 24, hoehe // 2)
    ex, ey = breite - rand - 96, (hoehe - 96) // 2
    slot(b, ex, ey, ergebnis.resize((px, px), Image.NEAREST), 96)
    anzahl(b, ex, ey, menge, 96)
    b.save(os.path.join(AUS, name))


def reihe(namen=("mana.png", "mana_charge.png", "mana_apple.png"), datei="items.png"):
    """Items nebeneinander, fuer den Kopf der Seite."""
    zelle = 112
    b = Image.new("RGBA", (len(namen) * zelle + 16, zelle + 16), (22, 30, 58, 255))
    for i, f in enumerate(namen):
        b.alpha_composite(pool_bild("mana/" + f, 96), (16 + i * zelle, 16))
    b.save(os.path.join(AUS, datei))


def bauplan():
    """Kuerbis, Ofen, Mana-Block uebereinander und daneben der fertige Furnace Golem.

    Die Wuerfel zeichnet der Wiki-Film (tools/videos/filme/furnace_golem.py), die Figur kommt aus
    tools/videos/.cache/sprites/fgolem_idle (python3 tools/videos/modelle.py fgolem_idle).
    """
    videos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
    sys.path.insert(0, videos)
    sys.path.insert(0, os.path.join(videos, "filme"))
    from furnace_golem import block  # noqa: E402

    kante = 64
    turm = [block(n, kante) for n in ("mana_block", "ofen", "kuerbis")]
    figur = Image.open(os.path.join(videos, ".cache", "sprites", "fgolem_idle", "000.png")).convert("RGBA")
    figur = figur.crop(figur.getbbox())
    rand, luecke = 32, 40
    w, h = turm[0].size
    turm_h = h + 2 * kante
    hoehe = round(h + kante)  # die Figur steht in zwei Zellen, Fuss und Ofen
    figur = figur.resize((round(figur.width * hoehe / figur.height), hoehe), Image.LANCZOS)
    breite = rand + w + luecke + 76 + luecke + figur.width + rand
    gesamt = rand * 2 + max(turm_h, hoehe)
    b = Image.new("RGBA", (breite, gesamt), (22, 30, 58, 255))
    unten = gesamt - rand
    for i, wuerfel in enumerate(turm):
        b.alpha_composite(wuerfel, (rand, unten - h - i * kante))
    pfeil_x = rand + w + luecke
    z = ImageDraw.Draw(b)
    farbe = (200, 200, 220, 255)
    y = gesamt // 2
    z.rectangle((pfeil_x, y - 8, pfeil_x + 44, y + 7), fill=farbe)
    z.polygon([(pfeil_x + 44, y - 24), (pfeil_x + 76, y), (pfeil_x + 44, y + 23)], fill=farbe)
    b.alpha_composite(figur, (pfeil_x + 76 + luecke, unten - hoehe))
    b.save(os.path.join(AUS, "bauplan-golem.png"))


def main():
    os.makedirs(AUS, exist_ok=True)
    kugel = pool_bild("mana/mana.png")
    ladung = pool_bild("mana/mana_charge.png")
    apfel_mana = pool_bild("mana/mana_apple.png")
    apfel = jar_bild("apple")
    rezept([kugel] * 9, ladung, "rezept-ladung.png")
    rezept([None, None, None, None, ladung, None, None, None, None], kugel, "rezept-zerlegen.png", 9)
    rezept([None, kugel, None, kugel, apfel, kugel, None, kugel, None], apfel_mana, "rezept-apfel.png")
    # Mana-Block: nur das Rezept hin. Ein Rueckrezept gibt es seit dem 08.11.2026 nicht mehr.
    rezept([kugel] * 4 + [ladung] + [kugel] * 4, pool_bild("mana/mana_block.png", 64), "rezept-block.png", px=64)
    reihe()
    reihe(("mana_block.png", "mana_budding.png", "mana_shard.png"), "items-golem.png")
    bauplan()
    print("Bilder in", AUS)


if __name__ == "__main__":
    main()
