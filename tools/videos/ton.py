"""Ton der Wiki-Videos: Musikbett, Effekte, Malas Stimme und Spielgeraeusche.

Alles wird hier erzeugt oder aus dem Pool gelesen - keine fremden Aufnahmen.

- Musik: ruhiges Stueck aus Flaechen, Spieluhr-Arpeggio und Bass, je Film
  gleich gebaut, nur Tonart und Tempo wechseln (Film.musik). Unter Malas
  Stimme wird sie leiser.
- Effekte 'sfx:<name>': whoosh, pop, chime, klick, funkeln, tippen, erfolg, boom, swell, herz - synthetisch.
- Stimme 'mala:<name>': Malas Aufnahmen aus dem Pool (assets/sounds/mala/<sprache>/),
  Text und Wortzeiten aus MBSkyManager/src/main/resources/story/voice-lines.yml.
  Daraus entstehen auch die Untertitel im Bild (Film.untertitel).
- Spielgeraeusche 'pool:<pfad>': assets/sounds/<pfad>.ogg im Pool, z. B. 'pool:warpett/eat_1'.
- Fertige Geraeusche 'datei:<pfad>': Audiodatei relativ zu tools/videos, z. B. 'datei:musik/trailer-leere.mp3'.

Ergebnis sind zwei WAV-Dateien (Musik, Rest); bauen.py mischt sie mit ffmpeg.
"""
import array
import functools
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
    # Zeilen nur fuer Wiki-Filme (z. B. den Trailer), aufgenommen mit trailer_stimme.py
    for name, sprachen in _wiki_stimmen().items():
        if sprache in sprachen:
            e = sprachen[sprache]
            out[name] = (int(e["ms"]), e["text"], [int(w) for w in e["words"]])
    return out


WIKI_STIMMEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stimmen")


def _wiki_stimmen():
    import json
    pfad = os.path.join(WIKI_STIMMEN, "manifest.json")
    return json.load(open(pfad, encoding="utf-8")) if os.path.isfile(pfad) else {}


def stimm_pfad(sprache, name):
    """OGG einer Mala-Zeile: erst die Wiki-eigenen Aufnahmen, sonst der Pool."""
    eigen = os.path.join(WIKI_STIMMEN, sprache, name + ".ogg")
    return eigen if os.path.isfile(eigen) else os.path.join(POOL, "assets", "sounds", "mala", sprache, name + ".ogg")


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


def kick():
    """Tonaler Kick: kurzer, schnell fallender Sinus (kein Rauschen)."""
    d = .45
    out, ph = [], 0.0
    for k in range(int(d * SR)):
        t = k / SR
        ph += 2 * math.pi * (46 + 110 * math.exp(-t / .035)) / SR
        out.append(math.sin(ph) * math.exp(-t / .16) * min(1, t / .002))
    return out


# ── Feurig (Trailer) ────────────────────────────────────────────────────────
# d-Moll, i - VI - III - VII (Dm, Bb, F, C), ein Akkord je Takt. Alles tonal,
# kein Rauschen: Taiko und Toms sind fallende Sinus, Streicher und Blaeser
# additive Saegezaehne.
FOLGE_FEURIG = [(0, (0, 3, 7)), (-4, (0, 4, 7)), (3, (0, 4, 7)), (-2, (0, 4, 7))]
# Ostinato in Sechzehnteln: Stufen relativ zum Akkordgrundton (12 = Oktave, 7 = Quinte)
OSTINATO = [0, 0, 12, 0, 7, 0, 12, 0, 0, 0, 12, 0, 7, 12, 7, 0]
# Taiko je Takt in Sechzehnteln (Position, Lautstaerke) - der typische Trailer-Galopp
TAIKO = [(0, 1.0), (3, .55), (6, .7), (8, .9), (11, .55), (12, .75), (14, .6)]


@functools.lru_cache(maxsize=None)
def saege(midi, dauer, anschlag, abklang, obertoene=9, verstimmt=0.0):
    """Saegezahn aus Obertoenen mit Huellkurve (Anschlag, exponentieller Abklang)."""
    hz = midi_hz(midi)
    n = int(dauer * SR)
    ws = [2 * math.pi * hz * h / SR for h in range(1, obertoene + 1) if hz * h < 9000]
    w2 = 2 * math.pi * hz * (1 + verstimmt) / SR
    out = [0.0] * n
    for k in range(n):
        t = k / SR
        e = min(1.0, t / anschlag) * math.exp(-t / abklang) * min(1.0, (dauer - t) / .01)
        v = 0.0
        for h, w in enumerate(ws, 1):
            v += math.sin(w * k) / h
        if verstimmt:
            v = .65 * v + .35 * math.sin(w2 * k)
        out[k] = e * v * .5
    return tuple(out)


@functools.lru_cache(maxsize=None)
def trommel(hz_hoch, hz_tief, abklang, dauer=.9):
    """Taiko/Tom: schnell fallender Sinus mit etwas Oberton fuer den Anschlag."""
    out, ph = [], 0.0
    for k in range(int(dauer * SR)):
        t = k / SR
        ph += 2 * math.pi * (hz_tief + (hz_hoch - hz_tief) * math.exp(-t / .025)) / SR
        out.append((math.sin(ph) + .3 * math.sin(2.01 * ph) * math.exp(-t / .03))
                   * math.exp(-t / abklang) * min(1, t / .002))
    return tuple(out)


def musik_feurig(dauer, tonart="D", tempo=120, ab=0.0, ende=None):
    """Treibendes Trailer-Stueck: Taiko-Galopp, Streicher-Ostinato, Blaeser-Stoesse, Bass.

    Steigerung: erste zwei Takte Trommeln und Streicher, dann Blaeser dazu,
    in den letzten zwei Takten vor ende ein Tom-Wirbel."""
    n = int((dauer + 3) * SR)
    stereo = ([0.0] * n, [0.0] * n)
    grund = TONARTEN.get(tonart, 50)
    sech = 60 / tempo / 4
    takt = 16 * sech
    ende = dauer + 1 if ende is None else ende
    takte = int(round((ende - ab) / takt))
    for i in range(takte):
        t0 = ab + i * takt
        wurzel, drei = FOLGE_FEURIG[i % len(FOLGE_FEURIG)]
        g = grund + wurzel
        rest = takte - i
        # Taiko-Galopp, im Wirbel zum Schluss alle Sechzehntel
        if rest <= 2:
            for k in range(16):
                laut = .45 + .55 * (k / 15) if rest == 1 else .5
                addiere(stereo, trommel(150, 70, .18), t0 + k * sech, .5 * laut, pan=(-.3 if k % 2 else .3))
        for pos, laut in TAIKO:
            addiere(stereo, trommel(110, 42, .32), t0 + pos * sech, .75 * laut)
        addiere(stereo, trommel(170, 85, .16), t0 + 13 * sech, .35, pan=.4)
        addiere(stereo, trommel(170, 85, .16), t0 + 15 * sech, .35, pan=-.4)
        # Streicher-Ostinato, zwei Lagen links/rechts
        for k, stufe in enumerate(OSTINATO):
            akzent = 1.0 if k % 4 == 0 else .7
            ton = g + stufe
            addiere(stereo, saege(ton, sech * .95, .004, .09), t0 + k * sech, .11 * akzent, pan=-.45)
            addiere(stereo, saege(ton + 12, sech * .95, .004, .07, 6), t0 + k * sech, .05 * akzent, pan=.45)
        # Bass: Achtel, Grundton tief
        for k in range(8):
            addiere(stereo, saege(g - 12, 2 * sech * .9, .006, .2, 6), t0 + k * 2 * sech, .16)
        # Blaeser-Stoesse ab dem dritten Takt: Akkord auf 1 und kurzer Nachschlag auf 3 und
        if i >= 2:
            for st in drei:
                for pos, d, laut in ((0, 1.1, 1.0), (10, .35, .6)):
                    addiere(stereo, saege(g + 12 + st, d, .03, .45, 9, .006), t0 + pos * sech, .07 * laut,
                            pan=(st - 3) / 10)
    # Auf den Pegel des ruhigen Musikbetts bringen (ca. -18 dB im Mittel), sonst geht die Stimme unter
    for kanal in stereo:
        for k in range(len(kanal)):
            kanal[k] *= .56
    return stereo


def lade_audio_stereo(pfad):
    """Beliebige Audiodatei (mp3, ogg, wav) -> Stereo-Floatlisten mit SR, ueber ffmpeg."""
    roh = subprocess.run(["ffmpeg", "-v", "error", "-i", pfad, "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h")
    a.frombytes(roh)
    return [v / 32768 for v in a[0::2]], [v / 32768 for v in a[1::2]]


@functools.lru_cache(maxsize=8)
def _audio(pfad):
    return lade_audio_stereo(pfad)


def musik_dateien(dauer, stuecke, pegel=1.0):
    """Fertige Musikstuecke ins Bett legen: [(start_s, pfad, lautstaerkekurve[, (von_s, bis_s)])].

    Die Kurve ist [(t relativ zum Stueck, gain), ...], linear dazwischen; None = durchgehend 1.
    Mit Ausschnitt wird nur dieser Teil gelegt (an den Kanten 40 ms weich) - so laesst sich ein
    Stueck taktgenau verlaengern, indem ein Ausschnitt ein zweites Mal kommt."""
    n = int((dauer + 3) * SR)
    links, rechts = [0.0] * n, [0.0] * n
    for eintrag in stuecke:
        start, pfad, kurve = eintrag[:3]
        if not os.path.isabs(pfad):
            pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), pfad)
        l, r = _audio(pfad)
        if len(eintrag) > 3:
            von, bis = int(eintrag[3][0] * SR), int(eintrag[3][1] * SR)
            rand = int(.04 * SR)
            l, r = list(l[von:bis]), list(r[von:bis])
            for k in range(min(rand, len(l))):
                f = k / rand
                if von > 0:
                    l[k] *= f
                    r[k] *= f
                l[-1 - k] *= f
                r[-1 - k] *= f
        i0 = int(start * SR)
        for k in range(min(len(l), n - i0)):
            g = pegel
            if kurve:
                t = k / SR
                g *= kurve[-1][1]
                for (ta, ga), (tb, gb) in zip(kurve, kurve[1:]):
                    if ta <= t < tb:
                        g = pegel * (ga + (gb - ga) * (t - ta) / (tb - ta))
                        break
                else:
                    if t < kurve[0][0]:
                        g = pegel * kurve[0][1]
            links[i0 + k] += l[k] * g
            rechts[i0 + k] += r[k] * g
    return links, rechts


def musik(dauer, tonart="D", tempo=84, stimmung="hell", ab=0.0, ende=None, beat=False, beat_ab=None, beat_bis=None,
          art="ruhig", stuecke=None, pegel=1.0):
    """Musikbett. ab/ende: wann die Musik einsetzt und aufhoert (Sekunden, auf Taktgrenzen legen).
    beat=True legt Kick auf jede Zaehlzeit und pumpenden Achtel-Bass darunter (zwischen beat_ab und beat_bis).
    art="feurig" nimmt stattdessen musik_feurig(), art="dateien" fertige Stuecke (siehe musik_dateien)."""
    if art == "feurig":
        return musik_feurig(dauer, tonart, tempo, ab, ende)
    if art == "dateien":
        return musik_dateien(dauer, stuecke, pegel)
    n = int((dauer + 3) * SR)
    stereo = ([0.0] * n, [0.0] * n)
    grund = TONARTEN.get(tonart, 50)
    schlag = 60 / tempo
    takt = 4 * schlag
    rnd = random.Random(7)
    ende = dauer + 1 if ende is None else ende
    beat_ab = ab if beat_ab is None else beat_ab
    beat_bis = ende if beat_bis is None else beat_bis
    k_kick = kick() if beat else None
    t, i = ab, 0
    while t < ende - 1e-6:
        if beat and beat_ab - 1e-6 <= t < beat_bis - 1e-6:
            bass_off = FOLGE[i % len(FOLGE)][0]
            for b in range(4):
                addiere(stereo, k_kick, t + b * schlag, .42)
                addiere(stereo, bass(midi_hz(grund + bass_off - 12), schlag * .3), t + (b + .5) * schlag, .1)
        bass_off, toene = FOLGE[i % len(FOLGE)]
        # Flaeche: drei obere Akkordtoene, leicht verteilt
        for j, ton in enumerate(toene[1:4]):
            addiere(stereo, flaeche(midi_hz(grund + ton), takt), t, .055, pan=(-.5, .1, .5)[j])
        # Bass auf 1 und 3
        for b in (0, 2):
            addiere(stereo, bass(midi_hz(grund + bass_off - 12), 2 * schlag * .95), t + b * schlag, .16)
        # Spieluhr ab dem zweiten Takt
        if t >= ab + takt:
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
    if name == "boom":
        # Trailer-Schlag: tiefer, fallender Sinus mit Obertoenen und langem Ausklang (kein Rauschen)
        d = 3.2
        out, ph = [], 0.0
        for k in range(int(d * SR)):
            t = k / SR
            hz = 41 + 60 * math.exp(-t / .1)
            ph += 2 * math.pi * hz / SR
            ton = math.sin(ph) + .3 * math.sin(2 * ph) + .12 * math.sin(3 * ph)
            out.append(ton * .9 * math.exp(-t / 1.0) * min(1, t / .006))
        return out
    if name == "herz":
        # Herzschlag: zwei tiefe, weiche Schlaege (lub-dub), rein tonal
        d = .7
        out = [0.0] * int(d * SR)
        for start, hz0, g in ((0.0, 62, 1.0), (.2, 55, .7)):
            ph, i0 = 0.0, int(start * SR)
            for k in range(len(out) - i0):
                t = k / SR
                ph += 2 * math.pi * (hz0 + 30 * math.exp(-t / .03)) / SR
                out[i0 + k] += g * math.sin(ph) * math.exp(-t / .09) * min(1, t / .004)
        return out
    if name == "swell":
        # Anschwellender Akkord (Grundton, Quinte, Oktave), steigt leicht an und reisst vor dem Schnitt ab
        d = 2.0
        out = [0.0] * int(d * SR)
        for j, (ton, g) in enumerate(((50, .5), (57, .35), (62, .3), (69, .15))):
            ph = 0.0
            for k in range(len(out)):
                t = k / SR
                u = t / d
                ph += 2 * math.pi * midi_hz(ton + 1.5 * u) / SR
                out[k] += g * math.sin(ph + .6 * math.sin(ph * .5)) * u ** 2.5 * min(1, (d - t) / .015)
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


def baue(film, ordner, sprache="de", szenen_whoosh=None):
    """Schreibt musik.wav und rest.wav nach ordner und fuellt film.untertitel."""
    os.makedirs(ordner, exist_ok=True)
    dauer = film.gesamt
    n = int((dauer + 1) * SR)
    rest = ([0.0] * n, [0.0] * n)
    sprechen = untertitel(film, sprache)
    for t, quelle, laut in film.cues():
        art, name = quelle.split(":", 1)
        if art == "mala":
            addiere(rest, lade_ogg(stimm_pfad(sprache, name)), t, 1.1 * laut)
        elif art == "pool":
            addiere(rest, lade_ogg(os.path.join(POOL, "assets", "sounds", name + ".ogg")), t, .7 * laut)
        elif art == "datei":  # fertiges Geraeusch, Pfad relativ zu tools/videos
            pfad = name if os.path.isabs(name) else os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
            l, r = lade_audio_stereo(pfad)
            addiere(rest, [(x + y) / 2 for x, y in zip(l, r)], t, laut)
        elif art == "sfx":
            addiere(rest, sfx(name, seed=int(t * 100)), t, .5 * laut)
        else:
            raise KeyError(quelle)
    if szenen_whoosh is None:
        szenen_whoosh = getattr(film, "whoosh", True)
    if szenen_whoosh:
        for i, t0 in enumerate(film.starts[1:], 1):
            addiere(rest, sfx("whoosh", seed=i), t0 - .45, .07, pan=(-.4 if i % 2 else .4))
    m = musik(dauer, **film.musik)
    # Musik unter der Stimme absenken, am Anfang ein- und am Ende ausblenden
    links, rechts = m
    hulle = [1.0] * len(links)
    ducken = getattr(film, "ducken", .55)  # wie stark die Musik unter der Stimme leiser wird (0..1)
    for t0, t1 in sprechen:
        for k in range(max(0, int((t0 - .35) * SR)), min(len(hulle), int((t1 + .6) * SR))):
            t = k / SR
            u = min(1.0, (t - (t0 - .35)) / .35, ((t1 + .6) - t) / .6)
            hulle[k] = min(hulle[k], 1 - ducken * max(0.0, min(1.0, u)))
    for k in range(len(links)):
        t = k / SR
        g = hulle[k] * (1.0 if film.musik.get("art") == "dateien" else min(1.0, t / 1.5)) \
            * max(0.0, min(1.0, (dauer - t) / 3.0))
        links[k] *= g
        rechts[k] *= g
    schreibe_wav(os.path.join(ordner, "musik.wav"), (links[:n], rechts[:n]), .9)
    schreibe_wav(os.path.join(ordner, "rest.wav"), rest, 1.0)
    return sprechen
