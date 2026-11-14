#!/usr/bin/env python3
"""Bilder fuer sb/mana-items.md, sb/furnace-golem.md und ihre en/-Seiten: die Mana-Items und ihre Rezepte.

Die Texturen kommen frisch aus dem Pool (MBSKY_POOLS, assets/items/mana), der Apfel aus dem
neuesten Client-Jar. Ein neues Bild im Pool heisst: dieses Skript noch einmal laufen lassen.

Mana-Block und Knospender Mana-Amethyst sind Bloecke. Die zeichnet das Skript aus ihren
Blockbench-Projekten im Pool (assets/custom_blocks), in der Inventar-Ansicht, wie Java sie zeigt.
Das Item-Bild in assets/items/mana ist nur das Bedrock-Icon und hinkt hinterher, wenn der Modeler
den Block in Blockbench aendert (so beim Budding am 11.11.2026). Den Zeichner liefert
MBSkyManager (MBSKY_REPO, tools/gen_mana_geode.py).

    python3 tools/mana_bilder.py
"""
import base64
import glob
import io
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mobplate_bilder import FLAECHE, SLOT, jar_bild, pfeil, pool_bild, slot  # noqa: E402

AUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".gitbook", "assets", "mana")
BLOECKE = os.path.join(os.environ.get("MBSKY_POOLS", os.path.expanduser("~/Coding/pools")), "assets", "custom_blocks")
MANAGER_TOOLS = os.path.join(os.environ.get("MBSKY_REPO") or "/Users/kay/IdeaProjects/MBSkyManager", "tools")


def block_bild(name, px):
    """Der Block aus custom_blocks/**/<name>.bbmodel in der Inventar-Ansicht, px x px.

    Gezeichnet werden die Flaechen der ersten Textur; die Leucht-Ebene des Budding liegt
    deckungsgleich darueber und steht schon in der Grundtextur.
    """
    treffer = glob.glob(os.path.join(BLOECKE, "**", name + ".bbmodel"), recursive=True)
    if len(treffer) != 1:
        raise SystemExit(f"FEHLER: {name}.bbmodel {len(treffer)}-mal unter {BLOECKE}")
    sys.path.insert(0, MANAGER_TOOLS)
    from gen_mana_geode import BLOCK_GUI  # noqa: E402
    from gen_rucksack_modell import rendere  # noqa: E402

    projekt = json.load(open(treffer[0], encoding="utf-8"))
    aufloesung = projekt["resolution"]["width"]
    texturen = projekt["textures"]
    textur = Image.open(io.BytesIO(base64.b64decode(texturen[0]["source"].split(",", 1)[1]))).convert("RGBA")
    erste = {0, "0", texturen[0].get("id")}
    elemente = []
    for e in projekt["elements"]:
        flaechen = {s: {"uv": [v * 16 / aufloesung for v in f["uv"]], "texture": 0}
                    for s, f in e["faces"].items() if f.get("texture") in erste}
        if any(e.get("rotation") or [0]):
            raise SystemExit(f"FEHLER: {name}: gedrehte Wuerfel kann dieses Skript nicht zeichnen")
        if flaechen:
            elemente.append({"from": e["from"], "to": e["to"], "faces": flaechen})
    return rendere({"elements": elemente}, textur, BLOCK_GUI, px)


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
    """Items nebeneinander, fuer den Kopf der Seite. Ein Name ohne .png ist ein Block (block_bild)."""
    zelle = 112
    b = Image.new("RGBA", (len(namen) * zelle + 16, zelle + 16), (22, 30, 58, 255))
    for i, f in enumerate(namen):
        bild = pool_bild("mana/" + f, 96) if f.endswith(".png") else block_bild(f, 96)
        b.alpha_composite(bild, (16 + i * zelle, 16))
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
    rezept([kugel] * 4 + [ladung] + [kugel] * 4, block_bild("mana_block", 64), "rezept-block.png", px=64)
    reihe()
    reihe(("mana_block", "mana_budding", "mana_shard.png"), "items-golem.png")
    bauplan()
    print("Bilder in", AUS)


if __name__ == "__main__":
    main()
