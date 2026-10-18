"""Ton der Wiki-Videos: Musikbett, Effekte, Malas Stimme und Spielgeraeusche.

Alles wird hier erzeugt oder aus dem Pool gelesen - keine fremden Aufnahmen.

- Musik: ruhiges Stueck aus Flaechen, Spieluhr-Arpeggio und Bass, je Film
  gleich gebaut, nur Tonart und Tempo wechseln (Film.musik). Unter Malas
  Stimme wird sie leiser.
- Effekte 'sfx:<name>': whoosh, pop, chime, klick, funkeln, tippen - synthetisch.
- Stimme 'mala:<name>': Malas Aufnahmen aus dem Pool (assets/sounds/mala/<sprache>/),
  Text und Wortzeiten aus MBSkyManager/src/main/resources/story/voice-lines.yml.
  Daraus entstehen auch die Untertitel im Bild (Film.untertitel).
- Spielgeraeusche 'pool:<pfad>': assets/sounds/<pfad>.ogg im Pool, z. B. 'pool:warpett/eat_1'.

Ergebnis sind zwei WAV-Dateien (Musik, Rest); bauen.py mischt sie mit ffmpeg.
"""
import array
import math
import os
import random
import re
import subprocess
import wave

import basis

SR = 44100
POOL = os.environ.get("MBSKY_POOLS", os.path.expanduser("~/Coding/pools"))
STIMMEN = os.path.join(os.environ.get("MBSKY_REPO", "/Users/kay/IdeaProjects/MBSkyManager"),
                       "src", "main", "resources", "story", "voice-lines.yml")


# ── Stimme ──────────────────────────────────────────────────────────────────

def stimmen(sprache):
    """{name: (ms, text, [wortzeiten ms])} aus voice-lines.yml (ohne PyYAML)."""
    out, schluessel, lang, feld = {}, None, None, {}
    for zeile in open(STIMMEN, encoding="utf-8"):
        m = re.match(r"^  intro\.mala\.([\w-]+):\s*$", zeile)
        if m:
            schluessel, lang = m.group(1), None
            continue
        m = re.match(r"^    (\w\w):\s*$", zeile)
        if m and schluessel:
            lang, feld = m.group(1), {}
            continue
        m = re.match(r'^      (ms|text|words): (.*)$', zeile)
        if m and schluessel and lang == sprache:
            feld[m.group(1)] = m.group(2).strip()
            if {"ms", "text", "words"} <= feld.keys():
                text = feld["text"][1:-1].replace('\\"', '"')
                woerter = [int(w) for w in feld["words"].strip("[]").split(",") if w.strip()]
                out[schluessel] = (int(feld["ms"]), text, woerter)
                feld = {}
    return out


def stuecke(text, woerter, ms, maxlen=58):
    """Untertitel-Stuecke wie im Spiel: an Satzenden und Gedankenstrichen trennen."""
    tokens = text.split()
    if len(woerter) != len(tokens):
        woerter = [int(i * ms / max(1, len(tokens))) for i in range(len(tokens))]
    teile, cur, start = [], [], 0
    for i, tok in enumerate(tokens):
        if tok in ("–", "-") and cur:
            cur.append(tok)
            teile.append((start, " ".join(cur)))
            cur = []
            continue
        if not cur:
            start = woerter[i]
        cur.append(tok)
        laenge = len(" ".join(cur))
        if re.search(r"[.!?…]$", tok) or (laenge > maxlen and re.search(r"[,;:]$", tok)):
            teile.append((start, " ".join(cur)))
            cur = []
    if cur:
        teile.append((start, " ".join(cur)))
    out = []
    for k, (s, t) in enumerate(teile):
        ende = teile[k + 1][0] if k + 1 < len(teile) else ms
        out.append((s / 1000, ende / 1000, t))
    return out


def lade_ogg(pfad):
    roh = subprocess.run(["ffmpeg", "-v", "error", "-i", pfad, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    a = array.array("f")
    a.frombytes(roh)
    return a


# ── Synthese ────────────────────────────────────────────────────────────────

def midi_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def addiere(ziel, quelle, start_s, gain=1.0, pan=0.0):
    """Mono-Quelle in Stereo-Ziel (zwei Listen) addieren; pan -1 links … 1 rechts."""
    links, rechts = ziel
    i0 = int(start_s * SR)
    gl = gain * math.cos((pan + 1) * math.pi / 4) * math.sqrt(2)
    gr = gain * math.sin((pan + 1) * math.pi / 4) * math.sqrt(2)
    n = min(len(quelle), len(links) - i0)
    if n <= 0 or i0 < 0:
        return
    for k in range(n):
        v = quelle[k]
        links[i0 + k] += v * gl
        rechts[i0 + k] += v * gr


def flaeche(hz, dauer, anschlag=1.2, ausklang=1.8):
    n = int((dauer + ausklang) * SR)
    out = [0.0] * n
    w1, w2, w3 = 2 * math.pi * hz / SR, 2 * math.pi * hz * 1.0035 / SR, 2 * math.pi * hz * 2 / SR
    for k in range(n):
        t = k / SR
        if t < anschlag:
            e = math.sin(.5 * math.pi * t / anschlag) ** 2
        elif t < dauer:
            e = 1.0
        else:
            e = max(0.0, 1 - (t - dauer) / ausklang) ** 2
        out[k] = e * (math.sin(w1 * k) + .7 * math.sin(w2 * k) + .22 * math.sin(w3 * k)) * .5
    return out


def spieluhr(hz, dauer=1.4):
    n = int(dauer * SR)
    w = 2 * math.pi * hz / SR
    out = [0.0] * n
    for k in range(n):
        t = k / SR
        a = min(1.0, t / .004)
        out[k] = a * (math.sin(w * k) * math.exp(-t / .42) + .28 * math.sin(3 * w * k) * math.exp(-t / .1)
                      + .12 * math.sin(4.02 * w * k) * math.exp(-t / .06))
    return out


def bass(hz, dauer):
    n = int((dauer + .4) * SR)
    w = 2 * math.pi * hz / SR
    out = [0.0] * n
    for k in range(n):
        t = k / SR
        e = min(1.0, t / .03) * (0.55 + .45 * math.exp(-t / .5))
        if t > dauer:
            e *= max(0.0, 1 - (t - dauer) / .4)
        out[k] = e * (math.sin(w * k) + .25 * math.sin(2 * w * k))
    return out


TONARTEN = {"D": 50, "C": 48, "E": 52, "F": 53, "G": 43, "A": 45}
# Stufen relativ zum Grundton: I maj9, vi m7, IV maj7, V sus2 - darunter der Bass
FOLGE = [
    (0, [0, 7, 11, 14, 16]),
    (-3, [-3, 4, 7, 12, 14]),
    (-7, [-7, 0, 4, 11, 12]),
    (-5, [-5, 2, 7, 9, 14]),
]
MUSTER = [0, 1, 2, 3, 2, 1, 4, 2]  # Arpeggio-Reihenfolge durch die Akkordtoene (Achtel)


def musik(dauer, tonart="D", tempo=84, stimmung="hell"):
    n = int((dauer + 3) * SR)
    stereo = ([0.0] * n, [0.0] * n)
    grund = TONARTEN.get(tonart, 50)
    schlag = 60 / tempo
    takt = 4 * schlag
    rnd = random.Random(7)
    t, i = 0.0, 0
    while t < dauer + 1:
        bass_off, toene = FOLGE[i % len(FOLGE)]
        # Flaeche: drei obere Akkordtoene, leicht verteilt
        for j, ton in enumerate(toene[1:4]):
            addiere(stereo, flaeche(midi_hz(grund + ton), takt), t, .055, pan=(-.5, .1, .5)[j])
        # Bass auf 1 und 3
        for b in (0, 2):
            addiere(stereo, bass(midi_hz(grund + bass_off - 12), 2 * schlag * .95), t + b * schlag, .16)
        # Spieluhr ab dem zweiten Takt
        if t >= takt:
            for k, m in enumerate(MUSTER):
                ton = toene[m] + 12 + (12 if stimmung == "hell" and k == 6 else 0)
                laut = .07 if k % 2 == 0 else .05
                addiere(stereo, spieluhr(midi_hz(grund + ton)), t + k * schlag / 2 + rnd.uniform(0, .008), laut,
                        pan=rnd.uniform(-.35, .35))
        t += takt
        i += 1
    return stereo


def rauschen(dauer, seed=1):
    rnd = random.Random(seed)
    return [rnd.uniform(-1, 1) for _ in range(int(dauer * SR))]


def sfx(name, seed=0):
    """Kurze synthetische Effekte als Mono-Liste."""
    rnd = random.Random(seed)
    if name == "whoosh":
        d = .9
        r = rauschen(d, seed + 3)
        out, y1, y2 = [], 0.0, 0.0
        for k, v in enumerate(r):
            t = k / SR
            fc = 180 + 1100 * math.sin(math.pi * t / d) ** 2
            a = 1 - math.exp(-2 * math.pi * fc / SR)
            y1 += a * (v - y1)
            y2 += a * (y1 - y2)
            out.append(y2 * math.sin(math.pi * t / d) ** 2 * 1.4)
        return out
    if name == "pop":
        d = .16
        out, ph = [], 0.0
        for k in range(int(d * SR)):
            t = k / SR
            hz = 520 + 520 * math.exp(-t / .03)
            ph += 2 * math.pi * hz / SR
            out.append(math.sin(ph) * math.exp(-t / .045) * min(1, t / .002))
        return out
    if name == "klick":
        r = rauschen(.03, seed + 5)
        return [v * math.exp(-k / SR / .006) * .7 for k, v in enumerate(r)]
    if name == "tippen":
        r = rauschen(.025, seed + 9)
        return [v * math.exp(-k / SR / .004) * .35 for k, v in enumerate(r)]
    if name == "chime":
        d = 2.2
        out = [0.0] * int(d * SR)
        for ton, start in ((88, 0.0), (95, .09)):
            hz = midi_hz(ton)
            for p, (mult, tau, g) in enumerate(((1, .9, 1), (2.76, .3, .35), (5.4, .12, .2))):
                w = 2 * math.pi * hz * mult / SR
                i0 = int(start * SR)
                for k in range(len(out) - i0):
                    t = k / SR
                    out[i0 + k] += g * math.sin(w * k) * math.exp(-t / tau) * min(1, t / .002) * .25
        return out
    if name == "funkeln":
        d = .9
        out = [0.0] * int(d * SR)
        for j in range(6):
            hz = rnd.uniform(2200, 4200)
            i0 = int(rnd.uniform(0, .5) * SR)
            w = 2 * math.pi * hz / SR
            for k in range(min(int(.25 * SR), len(out) - i0)):
                t = k / SR
                out[i0 + k] += math.sin(w * k) * math.exp(-t / .05) * .35
        return out
    if name == "erfolg":
        d = 1.6
        out = [0.0] * int(d * SR)
        for j, ton in enumerate((74, 78, 81, 86)):
            w = 2 * math.pi * midi_hz(ton) / SR
            i0 = int(j * .09 * SR)
            for k in range(len(out) - i0):
                t = k / SR
                out[i0 + k] += (math.sin(w * k) + .2 * math.sin(2 * w * k)) * math.exp(-t / .5) * min(1, t / .003) * .3
        return out
    raise KeyError("unbekannter Effekt: " + name)


# ── Mischen ─────────────────────────────────────────────────────────────────

def schreibe_wav(pfad, stereo, gain=1.0):
    links, rechts = stereo
    a = array.array("h")
    for l, r in zip(links, rechts):
        l, r = l * gain, r * gain
        a.append(int(32767 * math.tanh(l)))
        a.append(int(32767 * math.tanh(r)))
    with wave.open(pfad, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(a.tobytes())


def untertitel(film, sprache="de"):
    """Fuellt film.untertitel aus den Mala-Cues und gibt die Sprechzeiten zurueck."""
    texte = stimmen(sprache) if any(q.startswith("mala:") for _, q, _ in film.cues()) else {}
    film.untertitel, sprechen = [], []
    for t, quelle, _ in film.cues():
        if quelle.startswith("mala:"):
            ms, text, woerter = texte[quelle[5:]]
            sprechen.append((t, t + ms / 1000))
            for a, b, stueck in stuecke(text, woerter, ms):
                film.untertitel.append((t + a, t + b, stueck))
    return sprechen


def baue(film, ordner, sprache="de", szenen_whoosh=True):
    """Schreibt musik.wav und rest.wav nach ordner und fuellt film.untertitel."""
    os.makedirs(ordner, exist_ok=True)
    dauer = film.gesamt
    n = int((dauer + 1) * SR)
    rest = ([0.0] * n, [0.0] * n)
    sprechen = untertitel(film, sprache)
    for t, quelle, laut in film.cues():
        art, name = quelle.split(":", 1)
        if art == "mala":
            pfad = os.path.join(POOL, "assets", "sounds", "mala", sprache, name + ".ogg")
            addiere(rest, lade_ogg(pfad), t, 1.1 * laut)
        elif art == "pool":
            addiere(rest, lade_ogg(os.path.join(POOL, "assets", "sounds", name + ".ogg")), t, .7 * laut)
        elif art == "sfx":
            addiere(rest, sfx(name, seed=int(t * 100)), t, .5 * laut)
        else:
            raise KeyError(quelle)
    if szenen_whoosh:
        for i, t0 in enumerate(film.starts[1:], 1):
            addiere(rest, sfx("whoosh", seed=i), t0 - .45, .07, pan=(-.4 if i % 2 else .4))
    m = musik(dauer, **film.musik)
    # Musik unter der Stimme absenken, am Anfang ein- und am Ende ausblenden
    links, rechts = m
    hulle = [1.0] * len(links)
    for t0, t1 in sprechen:
        for k in range(max(0, int((t0 - .35) * SR)), min(len(hulle), int((t1 + .6) * SR))):
            t = k / SR
            u = min(1.0, (t - (t0 - .35)) / .35, ((t1 + .6) - t) / .6)
            hulle[k] = min(hulle[k], 1 - .55 * max(0.0, min(1.0, u)))
    for k in range(len(links)):
        t = k / SR
        g = hulle[k] * min(1.0, t / 1.5) * max(0.0, min(1.0, (dauer - t) / 3.0))
        links[k] *= g
        rechts[k] *= g
    schreibe_wav(os.path.join(ordner, "musik.wav"), (links[:n], rechts[:n]), .9)
    schreibe_wav(os.path.join(ordner, "rest.wav"), rest, 1.0)
    return sprechen
