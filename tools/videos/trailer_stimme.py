#!/usr/bin/env python3
"""Malas Zeilen fuer den Trailer mit ElevenLabs aufnehmen - nur fuers Wiki.

Nutzt Stimme, Modell, Einstellungen und Schnitt aus MBSkyManager/tools/intro_stimmen.py,
schreibt aber nichts ins Spiel oder in den Pool:

- stimmen/<sprache>/<name>.ogg      die Aufnahme
- stimmen/manifest.json             Laenge, Text und Wortzeiten (fuer die Untertitel)

Die Texte stehen in stimmen/texte.json. Aufgenommen wird nur, was fehlt oder
sich geaendert hat (--alle: alles neu). Der API-Schluessel kommt wie dort aus
ELEVENLABS_API_KEY oder dem Schluesselbund (elevenlabs-api).

    python3 trailer_stimme.py [--alle] [--nur trailer-welt ...]
"""
import argparse
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
MBSKY = os.environ.get("MBSKY_REPO", "/Users/kay/IdeaProjects/MBSkyManager")
sys.path.insert(0, os.path.join(MBSKY, "tools"))
import intro_stimmen as werkzeug  # noqa: E402

ORDNER = os.path.join(HIER, "stimmen")
TEXTE = os.path.join(ORDNER, "texte.json")
MANIFEST = os.path.join(ORDNER, "manifest.json")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--alle", action="store_true")
    p.add_argument("--nur", nargs="*")
    a = p.parse_args()
    konfig = werkzeug.lade_konfig()
    zeilen = json.load(open(TEXTE, encoding="utf-8"))["zeilen"]
    manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.isfile(MANIFEST) else {}
    formatwahl = [konfig["format"], konfig["format_rueckfall"]]
    for name, z in zeilen.items():
        if a.nur and name not in a.nur:
            continue
        konfig.setdefault("regie", {})["intro.mala." + name] = z.get("regie", "")
        for sprache in konfig["sprachen"]:
            text = z[sprache]
            schluessel = "intro.mala." + name  # nur fuer Seed und Fingerabdruck
            abdruck = werkzeug.fingerabdruck(konfig, schluessel, sprache, text)
            datei = os.path.join(ORDNER, sprache, name + ".ogg")
            alt = manifest.get(name, {}).get(sprache, {})
            if not a.alle and os.path.isfile(datei) and alt.get("hash") == abdruck:
                continue
            ogg, eintrag, fmt, quelle = werkzeug.nimm_auf(konfig, schluessel, sprache, text, formatwahl)
            if fmt != formatwahl[0]:
                formatwahl = [fmt]
            os.makedirs(os.path.dirname(datei), exist_ok=True)
            open(datei, "wb").write(ogg)
            eintrag.pop("sound", None)
            manifest.setdefault(name, {})[sprache] = eintrag
            with open(MANIFEST, "w", encoding="utf-8") as fh:  # nach jeder bezahlten Aufnahme sichern
                json.dump(manifest, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
            print(f"  {sprache} {name}: {eintrag['ms'] / 1000:.2f} s ({quelle}, {fmt})")


if __name__ == "__main__":
    main()
