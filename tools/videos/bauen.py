#!/usr/bin/env python3
"""Baut ein Wiki-Video: Bilder (parallel), Ton, MP4 und Vorschaubild.

    python3 bauen.py <film> [--sprache de|en] [--teile 8] [--crf 23]
    python3 bauen.py <film> --standbild 3.0 12.5 …     PNGs nach test/
    python3 bauen.py <film> --kontakt [zeiten …]        Kontaktbogen nach test/

<film> ist eine Datei in filme/ ohne .py (clans, start, bewohner, skilltree).
Ergebnis: ../../.gitbook/assets/videos/<film>[-en].mp4 und .jpg (Vorschaubild).
Braucht ffmpeg (Homebrew), Pillow und die Quellen aus MBSkyManager, MBSkyConnector,
Datapacks/MBDefault und dem Pool (~/Coding/pools) - siehe README.md.
"""
import argparse
import importlib
import os
import shutil
import subprocess
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(os.path.dirname(os.path.dirname(HIER)), ".gitbook", "assets", "videos")


def lade_film(name, sprache):
    os.environ["SPRACHE"] = sprache
    sys.path.insert(0, HIER)
    sys.path.insert(0, os.path.join(HIER, "filme"))
    modul = importlib.import_module(name)
    return modul.FILM


def worker(name, sprache, von, bis, ausgabe):
    import ton
    film = lade_film(name, sprache)
    ton.untertitel(film, sprache)
    from basis import W, H, FPS
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10",
                           "-pix_fmt", "yuv420p", ausgabe], stdin=subprocess.PIPE)
    for i in range(von, bis):
        ff.stdin.write(film.bild(i / FPS).tobytes("raw", "BGRA"))
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg (Teil) fehlgeschlagen")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("film")
    p.add_argument("--sprache", default="de")
    p.add_argument("--teile", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    p.add_argument("--crf", type=int, default=23)
    p.add_argument("--standbild", nargs="*", type=float)
    p.add_argument("--kontakt", nargs="*", type=float)
    p.add_argument("--worker", nargs=3)
    a = p.parse_args()

    if a.worker:
        worker(a.film, a.sprache, int(a.worker[0]), int(a.worker[1]), a.worker[2])
        return

    import ton
    film = lade_film(a.film, a.sprache)
    from basis import W, H, FPS
    from PIL import Image
    test = os.path.join(HIER, "test")

    if a.standbild is not None or a.kontakt is not None:
        ton.untertitel(film, a.sprache)
        os.makedirs(test, exist_ok=True)
        if a.standbild:
            for t in a.standbild:
                film.bild(t).convert("RGB").save(os.path.join(test, f"{a.film}_{a.sprache}_{t:06.2f}.png"))
            return
        zeiten = a.kontakt
        if not zeiten:
            zeiten = [t0 + sz["dauer"] * .7 for sz, t0 in zip(film.szenen, film.starts)]
        spalten = 3
        bw, bh = W // 3, H // 3
        bogen = Image.new("RGB", (spalten * bw, ((len(zeiten) + spalten - 1) // spalten) * bh), (0, 0, 0))
        for i, t in enumerate(zeiten):
            b = film.bild(t).convert("RGB").resize((bw, bh), Image.LANCZOS)
            bogen.paste(b, ((i % spalten) * bw, (i // spalten) * bh))
        bogen.save(os.path.join(test, f"kontakt_{a.film}_{a.sprache}.jpg"), quality=88)
        return

    start = time.time()
    arbeit = os.path.join(HIER, "build", f"{a.film}-{a.sprache}")
    shutil.rmtree(arbeit, ignore_errors=True)
    os.makedirs(arbeit)
    print(f"Ton für {a.film} ({a.sprache}) …", flush=True)
    ton.baue(film, arbeit, a.sprache)
    n = int(round(film.gesamt * FPS))
    grenzen = [round(i * n / a.teile) for i in range(a.teile + 1)]
    print(f"{n} Bilder in {a.teile} Teilen …", flush=True)
    prozesse, teile = [], []
    for k in range(a.teile):
        aus = os.path.join(arbeit, f"teil{k:02d}.mp4")
        teile.append(aus)
        prozesse.append(subprocess.Popen([sys.executable, __file__, a.film, "--sprache", a.sprache,
                                          "--worker", str(grenzen[k]), str(grenzen[k + 1]), aus]))
    for pr in prozesse:
        if pr.wait() != 0:
            raise SystemExit("Ein Teil ist fehlgeschlagen.")
    liste = os.path.join(arbeit, "teile.txt")
    with open(liste, "w") as f:
        for t in teile:
            f.write(f"file '{t}'\n")
    os.makedirs(ZIEL, exist_ok=True)
    name = a.film + ("" if a.sprache == "de" else "-" + a.sprache)
    mp4 = os.path.join(ZIEL, name + ".mp4")
    filter_ton = ("[1:a]aecho=0.8:0.5:110|230:0.2|0.1,highpass=f=35[m];"
                  "[m][2:a]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste,
                    "-i", os.path.join(arbeit, "musik.wav"), "-i", os.path.join(arbeit, "rest.wav"),
                    "-filter_complex", filter_ton, "-map", "0:v", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", str(a.crf),
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", f"{film.gesamt:.3f}",
                    "-movflags", "+faststart", mp4], check=True)
    poster_t = getattr(film, "poster", None) or film.gesamt * .3
    film.bild(poster_t).convert("RGB").save(os.path.join(ZIEL, name + ".jpg"), quality=86)
    groesse = os.path.getsize(mp4) / 1e6
    print(f"fertig: {mp4} ({groesse:.1f} MB, {film.gesamt:.1f} s) in {time.time() - start:.0f} s")


if __name__ == "__main__":
    main()
