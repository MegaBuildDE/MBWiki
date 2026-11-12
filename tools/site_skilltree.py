#!/usr/bin/env python3
"""Daten und Symbole fuer den Skilltree-Baum der neuen Wiki-Seite (site/).

Liest aus MBSkyManager (MBSKY_MANAGER):

  src/main/resources/skilltree/SKILLTREE.yml   Pfade, Biome mit Menue-Symbol, Biom- und Kristallquests
  src/main/resources/config.yml                skilltree.price, skilltree.locked-groups, skilltree.quests
  src/main/resources/lang/de.yml, en.yml       menu.skilltree: Pfad- und Biomnamen, Quest-Saetze

und site/data/skilltree.json (von Hand: Seiten, Kristallbilder, Symbol-Ausnahmen). Schreibt:

  site/public/skilltree/<material>.png         Biom-Symbole, 16x16 aus dem neuesten Client-Jar
  site/public/skilltree/crystal-<pfad>.png     Kristalle aus dem Pool
  site/data/skilltree.generated.json           alles, was scripts/convert.mjs fuer den Baum braucht

Gesperrte Pfade (locked-groups) fehlen im Baum, wie im Spiel. Aendert sich der Skilltree im
Plugin, dieses Skript noch einmal laufen lassen:

    python3 tools/site_skilltree.py
"""
import glob
import io
import json
import os
import re
import sys
import zipfile

import yaml
from PIL import Image

from site_items import JARS, MANAGER, POOL, SITE, erstes_bild, speichern

DATEN = os.path.join(SITE, "data", "skilltree.json")
AUS = os.path.join(SITE, "public", "skilltree")
ERZEUGT = os.path.join(SITE, "data", "skilltree.generated.json")
RES = os.path.join(MANAGER, "src/main/resources")
SPRACHEN = ("de", "en")


def lade_yaml(pfad):
    with open(pfad, encoding="utf-8") as f:
        return yaml.safe_load(f)


def textur(spec, jar):
    """'jar:block/snow' oder 'pool:biome/Plains.png' -> RGBA-Bild oder None."""
    quelle, _, pfad = spec.partition(":")
    if quelle == "pool":
        datei = os.path.join(POOL, pfad)
        return erstes_bild(datei) if os.path.isfile(datei) else None
    name = "assets/minecraft/textures/" + pfad + ".png"
    try:
        return erstes_bild(io.BytesIO(jar.read(name)))
    except KeyError:
        return None


def faerben(bild, farbe):
    """Graue Gras-/Laub-Texturen wie im Inventar einfaerben."""
    r, g, b = (int(farbe[i:i + 2], 16) for i in (1, 3, 5))
    px = bild.load()
    for y in range(bild.height):
        for x in range(bild.width):
            pr, pg, pb, pa = px[x, y]
            px[x, y] = (pr * r // 255, pg * g // 255, pb * b // 255, pa)
    return bild


def farbe(bild):
    """Leuchtende Mittelfarbe der deckenden Pixel - der Akzent des Pfads im Baum."""
    roh = bild.tobytes()
    px = [roh[i:i + 4] for i in range(0, len(roh), 4) if roh[i + 3] > 200]
    if not px:
        return "#a958ff"
    r, g, b = (sum(p[i] for p in px) / len(px) for i in range(3))
    hoch = max(r, g, b) or 1
    r, g, b = (min(255, int(c * 230 / hoch)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def symbol(material, ausnahmen, jar):
    """Menue-Symbol eines Bioms: Ausnahme aus skilltree.json, sonst item/, block/, block/*_top."""
    eintrag = ausnahmen.get(material)
    if isinstance(eintrag, str):
        eintrag = {"tex": eintrag}
    if eintrag:
        bild = textur(eintrag["tex"], jar)
        if bild and eintrag.get("tint"):
            bild = faerben(bild, eintrag["tint"])
        return bild
    m = material.lower()
    for spec in (f"jar:item/{m}", f"jar:block/{m}", f"jar:block/{m}_top", f"jar:block/{m}_front"):
        bild = textur(spec, jar)
        if bild:
            return bild
    return None


def satz(text, menge=None):
    """Quest-Satz aus der Sprachdatei: <amount> einsetzen, MiniMessage-Tags weg."""
    if menge is not None:
        text = text.replace("<amount>", f"{menge:,}".replace(",", "."))
    return re.sub(r"<[^>]+>", "", text).strip()


def main():
    with open(DATEN, encoding="utf-8") as f:
        hand = json.load(f)
    baum = lade_yaml(os.path.join(RES, "skilltree", "SKILLTREE.yml"))
    st_conf = lade_yaml(os.path.join(RES, "config.yml"))["skilltree"]
    lang = {l: lade_yaml(os.path.join(RES, "lang", f"{l}.yml"))["menu"]["skilltree"] for l in SPRACHEN}
    gesperrt = set(st_conf.get("locked-groups") or [])
    jar_pfad = max(glob.glob(JARS), key=os.path.getmtime)

    os.makedirs(AUS, exist_ok=True)
    for alt in glob.glob(os.path.join(AUS, "*.png")):
        os.remove(alt)

    fehler = []
    pfade = []
    with zipfile.ZipFile(jar_pfad) as jar:
        for pfad_id, pfad in baum["paths"].items():
            if pfad_id in gesperrt or pfad.get("dimension"):
                continue
            kristall = textur(hand["crystals"].get(pfad_id, ""), jar) if pfad_id in hand["crystals"] else None
            if not kristall:
                fehler.append(f"{pfad_id}: kein Kristallbild (site/data/skilltree.json: crystals)")
            kq = baum.get("crystal-quests", {}).get(pfad_id)
            eintrag = {
                "id": pfad_id,
                "crystal": speichern(kristall, os.path.join(AUS, f"crystal-{pfad_id}.png")) if kristall else "",
                "color": farbe(kristall) if kristall else "#a958ff",
                "name": {l: lang[l]["groups"][pfad_id]["name"] for l in SPRACHEN},
                "description": {l: lang[l]["groups"][pfad_id].get("description", "") for l in SPRACHEN},
                "crystalQuest": {l: satz(lang[l]["quest"]["objective"]["crystal"][pfad_id], kq["amount"]) for l in SPRACHEN} if kq else None,
                "biomes": [],
            }
            for zeile in pfad["biomes"]:
                ((biom, material),) = zeile.items()
                bild = symbol(material, hand.get("icons", {}), jar)
                if not bild:
                    fehler.append(f"{biom}: keine Textur für {material} (site/data/skilltree.json: icons)")
                q = baum.get("quests", {}).get(biom)
                eintrag["biomes"].append({
                    "id": biom,
                    "icon": speichern(bild, os.path.join(AUS, material.lower() + ".png")) if bild else "",
                    "name": {l: lang[l]["biomes"][biom] for l in SPRACHEN},
                    "quest": {l: satz(lang[l]["quest"]["objective"][biom], q["amount"]) for l in SPRACHEN} if q else None,
                })
            pfade.append(eintrag)

    preis = st_conf.get("price", {})
    quests = st_conf.get("quests", {})
    erzeugt = {
        "$hinweis": "Erzeugt von tools/site_skilltree.py - nicht von Hand ändern.",
        "jar": os.path.basename(jar_pfad),
        "price": {
            "base": preis.get("base", 100),
            "growth": preis.get("growth", 0.05),
            "perStep": preis.get("per-step", 0.25),
            "roundTo": preis.get("round-to", 5),
        },
        "reward": quests.get("reward", 0),
        "locked": sorted(gesperrt),
        "paths": pfade,
    }
    with open(ERZEUGT, "w", encoding="utf-8") as f:
        json.dump(erzeugt, f, ensure_ascii=False, indent="\t")
        f.write("\n")
    if fehler:
        print("\n".join(fehler))
    n = sum(len(p["biomes"]) for p in pfade)
    print(f"{len(pfade)} Pfade, {n} Biome (gesperrt: {', '.join(sorted(gesperrt)) or '-'}) aus {erzeugt['jar']}")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
