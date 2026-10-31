#!/usr/bin/env python3
"""Musik fuer den Trailer mit ElevenLabs Music komponieren lassen - nur fuers Wiki.

Zwei Stuecke mit Kompositionsplan, Abschnittslaengen passend zum Schnitt in
filme/trailer.py (Drop bei 6 s, Abbruch bei 34 s, Logo-Schlag bei 38 s):

- musik/trailer-haupt.mp3   0-34 s
- musik/trailer-logo.mp3    8 s ab dem Logo

Die Plaene stehen in PLAENE. Neu komponiert wird nur, was fehlt (--neu: alles,
--nur haupt|logo: nur dieses Stueck). Der API-Schluessel kommt wie bei
trailer_stimme.py aus ELEVENLABS_API_KEY oder dem Schluesselbund. Die Music-API
gibt es nur in bezahlten ElevenLabs-Plaenen.

    python3 trailer_musik.py [--neu] [--nur haupt]
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.environ.get("MBSKY_REPO", "/Users/kay/IdeaProjects/MBSkyManager"), "tools"))
import intro_stimmen as werkzeug  # noqa: E402  (Schluessel und TLS)

ORDNER = os.path.join(HIER, "musik")
MODELL = "music_v2_5"  # haelt die Abschnittslaengen exakt ein (music_v1 hat den Drop 2,5 s zu spaet gesetzt)

STIL = ["hybrid cinematic trailer music", "epic orchestral strings and brass with modern electronic sound design",
        "pulsing analog synth arpeggios", "huge hybrid drums and taiko", "ethereal female choir chops",
        "fantasy adventure in the sky", "D minor", "120 BPM", "instrumental", "high energy", "modern, fresh, bold"]
NICHT = ["vocals", "lyrics", "corporate", "stock music", "ukulele", "lo-fi", "jazz", "acoustic guitar strumming",
         "happy pop", "elevator music"]

PLAENE = {
    "haupt": {
        "positive_global_styles": STIL,
        "negative_global_styles": NICHT,
        "sections": [
            {"section_name": "Cold open", "duration_ms": 6000, "lines": [],
             "positive_local_styles": ["dark tense drone", "deep sub pulse like a heartbeat", "sparse and quiet",
                                       "reversed swell rising into a hit at the end"],
             "negative_local_styles": ["drums", "melody", "loud"]},
            {"section_name": "Drop", "duration_ms": 8000, "lines": [],
             "positive_local_styles": ["massive impact on the first beat", "driving synth bass",
                                       "fast string ostinato", "punchy hybrid drums", "full energy immediately"],
             "negative_local_styles": ["slow intro", "fade in"]},
            {"section_name": "Build", "duration_ms": 12000, "lines": [],
             "positive_local_styles": ["brass stabs", "choir enters", "rising intensity", "syncopated percussion",
                                       "soaring melody"],
             "negative_local_styles": ["breakdown", "quiet"]},
            {"section_name": "Climax", "duration_ms": 8000, "lines": [],
             "positive_local_styles": ["biggest and loudest part", "drum fills and rolls", "riser",
                                       "ends with an abrupt hard stop on the last beat"],
             "negative_local_styles": ["fade out", "ritardando", "reverb tail"]},
        ],
    },
    "logo": {
        "positive_global_styles": STIL,
        "negative_global_styles": NICHT,
        "sections": [
            {"section_name": "Logo hit", "duration_ms": 8000, "lines": [],
             "positive_local_styles": ["one enormous cinematic impact with sub drop at the very start",
                                       "then a sustained shimmering choir and string chord", "slow fade out",
                                       "majestic, hopeful ending"],
             "negative_local_styles": ["drums after the first hit", "melody", "build up"]},
        ],
    },
}


def als_chunks(plan):
    """MusicPrompt (v1) -> CompositionPlan (v2.5): je Abschnitt ein Chunk, Laengen werden dort exakt eingehalten."""
    return {"chunks": [{"text": f"[{a['section_name']}]", "duration_ms": a["duration_ms"],
                        "positive_styles": plan["positive_global_styles"] + a["positive_local_styles"],
                        "negative_styles": plan["negative_global_styles"] + a["negative_local_styles"],
                        "context_adherence": "high"} for a in plan["sections"]]}


def komponiere(name):
    koerper = {"composition_plan": als_chunks(PLAENE[name]), "model_id": MODELL}
    anfrage = urllib.request.Request(
        werkzeug.API + "/v1/music?output_format=mp3_44100_192", method="POST",
        data=json.dumps(koerper).encode("utf-8"),
        headers={"xi-api-key": werkzeug.api_schluessel(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(anfrage, context=werkzeug.tls(), timeout=600) as antwort:
            return antwort.read()
    except urllib.error.HTTPError as fehler:
        raise SystemExit(f"FEHLER {fehler.code} bei {name}: {fehler.read().decode('utf-8', 'replace')[:600]}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--neu", action="store_true")
    p.add_argument("--nur", nargs="*")
    a = p.parse_args()
    os.makedirs(ORDNER, exist_ok=True)
    for name in PLAENE:
        if a.nur and name not in a.nur:
            continue
        datei = os.path.join(ORDNER, f"trailer-{name}.mp3")
        if os.path.isfile(datei) and not a.neu:
            continue
        print(f"komponiere {name} …", flush=True)
        daten = komponiere(name)
        open(datei, "wb").write(daten)
        print(f"  {datei}: {len(daten) // 1024} KB")


if __name__ == "__main__":
    main()
