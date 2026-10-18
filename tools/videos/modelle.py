#!/usr/bin/env python3
"""Rendert die 3D-Modelle aus dem Pool als freigestellte Einzelbilder fuer die Filme.

    python3 modelle.py            alle Auftraege (fehlende)
    python3 modelle.py --neu      alle neu
    python3 modelle.py mala_hello goblin_talk …

Startet einen kleinen Server (modelle.html, Pool-Modelle, Speichern) und ein
kopfloses Chrome, das modelle.html abarbeitet. Ergebnis: .cache/sprites/<auftrag>/NNN.png
(512 x 512, durchsichtig). basis.sprite() liest sie.
"""
import argparse
import base64
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import threading

HIER = os.path.dirname(os.path.abspath(__file__))
POOL = os.environ.get("MBSKY_POOLS", os.path.expanduser("~/Coding/pools"))
MODELLE = os.path.join(POOL, "assets", "bettermodels")
BLOECKE = os.path.join(POOL, "assets", "custom_blocks")
AUS = os.path.join(HIER, ".cache", "sprites")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS = 30

# name: (modell relativ zu assets/bettermodels, animation, blick-yaw, zoom[, tempo])
# tempo 2 = doppelt so schnell wie in Blockbench (wie das Fressen im Spiel seit 07.10.)
AUFTRAEGE = {
    "mala_idle": ("crew/mala_mage.bbmodel", "Idle.model.new", -28, 1.0),
    "mala_hello": ("crew/mala_mage.bbmodel", "hello.model.new", -28, 1.0),
    "golem_idle": ("command_golem/command_golem_1.bbmodel", None, -30, 1.0),
    "goblin_idle": ("goblins/goblin-standart-1.bbmodel", "idle", -25, 1.0),
    "goblin_hello": ("goblins/goblin-standart-1.bbmodel", "hello", -25, 1.0),
    "goblin_talk": ("goblins/goblin-standart-1.bbmodel", "talk", -25, 1.0),
    "goblin_hacken": ("goblins/goblin-standart-1.bbmodel", "hacken", 35, 1.0),
    "goblin_ernten": ("goblins/goblin-standart-2.bbmodel", "ernten", -35, 1.0),
    "goblin_sit": ("goblins/goblin-standart-1.bbmodel", "sit", -25, 1.0),
    "goblin_sleep": ("goblins/goblin-standart-2.bbmodel", "sleep", -40, 1.0),
    "schmied": ("goblins/goblin-schmiede.bbmodel", "schmieden", 30, 1.0),
    "shroom_hello": ("shroomling/Shroomling_red.bbmodel", "hello", -25, 1.0),
    "shroom_graben": ("shroomling/Shroomling_blue_dots.bbmodel", "graben", 30, 1.0),
    "shroom_idle": ("shroomling/Shroomling_brown.bbmodel", "idle", -25, 1.0),
    "forest_oak": ("forestlinge/forestling_oak.bbmodel", "idle", -25, 1.0),
    "forest_oak_happy": ("forestlinge/forestling_oak.bbmodel", "happy2", -25, 1.0),
    "forest_cherry": ("forestlinge/forestling_cherry.bbmodel", "idle", -25, 1.0),
    "forest_birch": ("forestlinge/forestling_birch.bbmodel", "idle", 25, 1.0),
    "forest_mangrove": ("forestlinge/forestling_mangrove.bbmodel", "idle", -25, 1.0),
    "warpett_idle": ("warper/Warpett_dandelion.bbmodel", "idle", -30, 1.0),
    "warpett_eat": ("warper/Warpett_dandelion.bbmodel", "eat", -30, 0.5, 2.0),
    "warpett_poppy": ("warper/Warpett_poppy.bbmodel", "idle", 30, 1.0),
    "warpett_blau": ("warper/Warpett_cornflower.bbmodel", "idle", -30, 1.0),
    # Bloecke (assets/custom_blocks): langsam gedreht, 'drehen' Bilder fuer eine Umdrehung
    "mana_erz": ("blocks:mana_ore/mana_ore.bbmodel", None, 35, 0.8, 1.0, 120),
    "warpett_ei": ("blocks:warpett_egg/warpett_egg.bbmodel", None, -30, 0.9),
}


class Server(http.server.SimpleHTTPRequestHandler):
    auftraege = []
    ergebnis = None
    fertig = threading.Event()

    def log_message(self, *a):
        pass

    def translate_path(self, path):
        sauber = path.split("?", 1)[0]
        if sauber.startswith("/pool/"):
            return os.path.join(MODELLE, sauber[len("/pool/"):])
        if sauber.startswith("/blocks/"):
            return os.path.join(BLOECKE, sauber[len("/blocks/"):])
        return os.path.join(HIER, sauber.lstrip("/") or "modelle.html")

    def do_GET(self):
        if self.path.startswith("/auftraege.json"):
            daten = json.dumps(self.auftraege).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(daten)))
            self.end_headers()
            self.wfile.write(daten)
            return
        super().do_GET()

    def do_POST(self):
        laenge = int(self.headers["Content-Length"])
        daten = self.rfile.read(laenge).decode()
        m = re.match(r"^/save/([\w-]+)/(\d+)\.png$", self.path)
        if m:
            ordner = os.path.join(AUS, m.group(1))
            os.makedirs(ordner, exist_ok=True)
            with open(os.path.join(ordner, m.group(2) + ".png"), "wb") as f:
                f.write(base64.b64decode(daten.split(",", 1)[-1]))
        elif self.path == "/fertig":
            Server.ergebnis = daten
            Server.fertig.set()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("namen", nargs="*")
    p.add_argument("--neu", action="store_true")
    a = p.parse_args()
    namen = a.namen or list(AUFTRAEGE)
    jobs = []
    for name in namen:
        if not a.neu and not a.namen and os.path.isdir(os.path.join(AUS, name)):
            continue
        shutil.rmtree(os.path.join(AUS, name), ignore_errors=True)
        modell, anim, yaw, zoom, *rest = AUFTRAEGE[name]
        url = "/blocks/" + modell[7:] if modell.startswith("blocks:") else "/pool/" + modell
        jobs.append(dict(name=name, url=url, anim=anim, yaw=yaw, zoom=zoom, fps=FPS,
                         tempo=rest[0] if rest else 1.0, drehen=rest[1] if len(rest) > 1 else 0))
    if not jobs:
        print("Alle Sprites vorhanden (--neu baut sie neu).")
        return
    Server.auftraege = jobs
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Server)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/modelle.html"
    profil = os.path.join(HIER, ".cache", "chrome")
    chrome = subprocess.Popen([CHROME, "--headless=new", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                               "--ignore-gpu-blocklist", f"--user-data-dir={profil}", "--no-first-run",
                               "--window-size=600,600", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not Server.fertig.wait(timeout=900):
            raise SystemExit("Zeitueberschreitung beim Rendern der Modelle")
    finally:
        chrome.terminate()
        srv.shutdown()
    print(Server.ergebnis)
    if Server.ergebnis.startswith("FEHLER"):
        sys.exit(1)


if __name__ == "__main__":
    main()
