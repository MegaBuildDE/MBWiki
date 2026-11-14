#!/usr/bin/env python3
"""Texturen und Item-Daten fuer die eigenen Bausteine der neuen Wiki-Seite (site/).

Liest site/data/items.json und schreibt:

  site/public/items/<id>.png             16x16, wie im Spiel (die Seite skaliert pixelgenau)
  site/public/items/<id>/<name>.png      bei tex mit * (z. B. alle Toepferscherben)
  site/public/items/mobplates/<mob>.png  alle gefuellten Mobplates aus dem Pool
  site/data/items.generated.json         Texturpfade, Mobplate-Namen (DE/EN) und welche
                                         Plates einen Spawner ergeben

Quellen: der Pool (MBSKY_POOLS, assets/items), das neueste Client-Jar fuer Vanilla-Texturen,
fuer eigene Bloecke ihr Blockbench-Projekt (tex block:<name>, assets/custom_blocks, gezeichnet
wie im Java-Inventar von tools/mana_bilder.py, 64x64 - das Item-Bild im Pool ist dort nur das
Bedrock-Icon und hinkt hinterher, wenn der Modeler den Block aendert) und MBSkyManager (MBSKY_MANAGER) fuer die Mobplate-Namen (SkyItem.java) und die
Spawner-Plates (config.yml: feather.spawner.plates). Der Server baut nur aus dem Repo,
darum liegen die Ergebnisse eingecheckt in site/. Neues Bild im Pool oder neues Item in
items.json heisst: dieses Skript noch einmal laufen lassen.

    python3 tools/site_items.py
"""
import fnmatch
import glob
import io
import json
import os
import re
import sys
import zipfile

import yaml
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HIER), "site")
DATEN = os.path.join(SITE, "data", "items.json")
AUS = os.path.join(SITE, "public", "items")
ERZEUGT = os.path.join(SITE, "data", "items.generated.json")

POOL = os.path.join(os.environ.get("MBSKY_POOLS", os.path.expanduser("~/Coding/pools")), "assets", "items")
MANAGER = os.environ.get("MBSKY_MANAGER", os.path.expanduser("~/IdeaProjects/MBSkyManager"))
SKYITEM = os.path.join(MANAGER, "src/main/java/de/kay313/mbsm/item/SkyItem.java")
CONFIG = os.path.join(MANAGER, "src/main/resources/config.yml")
JARS = os.path.expanduser("~/Library/Application Support/minecraft/versions/*/*.jar")


def erstes_bild(roh_oder_pfad):
    """16x16 als RGBA; bei animierten Streifen (hoeher als breit) nur das erste Bild."""
    bild = Image.open(roh_oder_pfad).convert("RGBA")
    if bild.height > bild.width:
        bild = bild.crop((0, 0, bild.width, bild.width))
    return bild


def speichern(bild, pfad):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    bild.save(pfad, optimize=True)
    return "/" + os.path.relpath(pfad, os.path.join(SITE, "public")).replace(os.sep, "/")


def texturen(item_id, spec, jar):
    """Exportiert die Textur(en) eines Items, gibt die URLs zurueck."""
    quelle, _, pfad = spec.partition(":")
    if quelle == "pool":
        treffer = sorted(glob.glob(os.path.join(POOL, pfad)))
        laden = lambda t: erstes_bild(t)  # noqa: E731
        name = lambda t: os.path.splitext(os.path.basename(t))[0]  # noqa: E731
    elif quelle == "jar":
        alle = [n for n in jar.namelist() if n.startswith("assets/minecraft/textures/") and n.endswith(".png")]
        muster = "assets/minecraft/textures/" + pfad + ".png"
        treffer = sorted(n for n in alle if fnmatch.fnmatch(n, muster))
        laden = lambda t: erstes_bild(io.BytesIO(jar.read(t)))  # noqa: E731
        name = lambda t: os.path.splitext(os.path.basename(t))[0]  # noqa: E731
    elif quelle == "block":
        from mana_bilder import block_bild
        treffer = [pfad]
        laden = lambda t: block_bild(t, 64)  # noqa: E731
        name = lambda t: t  # noqa: E731
    else:
        sys.exit(f"{item_id}: unbekannte Quelle in tex '{spec}' (pool:, jar: oder block:)")
    if not treffer:
        sys.exit(f"{item_id}: keine Textur für '{spec}' gefunden")
    if "*" not in pfad:
        return [speichern(laden(treffer[0]), os.path.join(AUS, item_id + ".png"))]
    return [speichern(laden(t), os.path.join(AUS, item_id, name(t) + ".png")) for t in treffer]


def mobplate_namen():
    """mobplate_<mob> -> (deutsch, englisch) ohne das 'Mobplate: ' davor, aus SkyItem.java."""
    namen = {}
    zeile = re.compile(r'^\s+MOBPLATE_\w+\("(mobplate_\w+)",[^"]*"([^"]+)"(?:,\s*"([^"]+)")?\)')
    with open(SKYITEM, encoding="utf-8") as f:
        for z in f:
            m = zeile.match(z)
            if m:
                de, en = m.group(2), m.group(3) or m.group(2)
                namen[m.group(1)] = (de.removeprefix("Mobplate: "), en.removeprefix("Mobplate: "))
    return namen


def spawner_plates():
    with open(CONFIG, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return list(config["feather"]["spawner"]["plates"])


def main():
    with open(DATEN, encoding="utf-8") as f:
        daten = json.load(f)
    jar_pfad = max(glob.glob(JARS), key=os.path.getmtime)
    if os.path.isdir(AUS):
        for alt in glob.glob(os.path.join(AUS, "**", "*.png"), recursive=True):
            os.remove(alt)

    erzeugt = {
        "$hinweis": "Erzeugt von tools/site_items.py - nicht von Hand ändern.",
        "jar": os.path.basename(jar_pfad),
        "textures": {},
        "mobplates": {},
    }
    with zipfile.ZipFile(jar_pfad) as jar:
        for item_id, item in daten["items"].items():
            erzeugt["textures"][item_id] = texturen(item_id, item["tex"], jar)

    namen = mobplate_namen()
    spawner = set(spawner_plates())
    for datei in sorted(glob.glob(os.path.join(POOL, "mobplates", "*.png"))):
        mob = os.path.splitext(os.path.basename(datei))[0]
        plate_id = "mobplate_" + mob
        if plate_id not in namen:
            print(f"Hinweis: {plate_id} hat keinen Eintrag in SkyItem.java - nicht in der Galerie")
            continue
        de, en = namen[plate_id]
        erzeugt["mobplates"][plate_id] = {
            "de": de,
            "en": en,
            "tex": speichern(erstes_bild(datei), os.path.join(AUS, "mobplates", mob + ".png")),
            **({"spawner": True} if plate_id in spawner else {}),
        }
    fehlt = spawner - erzeugt["mobplates"].keys()
    if fehlt:
        print("Hinweis: Spawner-Plates ohne Textur:", ", ".join(sorted(fehlt)))

    with open(ERZEUGT, "w", encoding="utf-8") as f:
        json.dump(erzeugt, f, ensure_ascii=False, indent="\t")
        f.write("\n")
    n_tex = sum(len(v) for v in erzeugt["textures"].values())
    print(f"{n_tex} Item-Texturen, {len(erzeugt['mobplates'])} Mobplates ({len(spawner)} mit Spawner) aus {erzeugt['jar']}")


if __name__ == "__main__":
    main()
