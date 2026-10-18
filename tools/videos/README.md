# Wiki-Videos

Kurze Feature-Filme fürs Wiki, gebaut aus echten Spielinhalten: Minecraft-Schrift und -Menüs, die 3D-Modelle aus dem Pool, Malas aufgenommene Stimme mit Untertiteln und selbst erzeugte Musik.

| Film | Datei | Seite |
| ---- | ----- | ----- |
| Dein Start | `filme/start.py` | `sb/start.md`, `en/start.md` |
| Deine Insel lebt | `filme/bewohner.py` | `sb/bewohner.md`, `en/residents.md` |
| Mana & Biome | `filme/skilltree.py` | `sb/skilltree.md`, `en/skilltree.md` |
| Clans – ein erster Blick | `filme/clans.py` | `sb/clans.md`, `en/clans.md` (nur DE) |

Ergebnis liegt in `.gitbook/assets/videos/<film>.mp4` (DE) bzw. `<film>-en.mp4`, daneben das Standbild `<film>.jpg` für die Seite.

## Bauen

```bash
python3 bauen.py start                  # deutscher Film
python3 bauen.py start --sprache en     # englischer Film
python3 bauen.py start --standbild 3 12.5   # einzelne Bilder nach test/
python3 bauen.py start --kontakt        # Kontaktbogen aller Szenen nach test/
python3 bauen.py start --poster         # nur das Standbild für die Wiki-Seite
```

Ein Film braucht auf einem M-Mac rund eine Minute (`--teile` Worker parallel, Vorgabe: Kerne minus eins).

## Was gebraucht wird

* Python 3 mit **Pillow**, dazu **ffmpeg** (Homebrew).
* **Google Chrome** für `modelle.py`.
* Die Quellen neben dem Wiki:
  * `~/IdeaProjects/MBSkyManager` (`MBSKY_REPO`) – Sprachdateien, Stimmen (`story/voice-lines.yml`), Icons, Manager-Pack
  * `~/IdeaProjects/MBSkyConnector` (`MBSC_TEXTUREN`) – HUD- und Item-Texturen
  * `~/IdeaProjects/Datapacks/MBDefault` – Hinweis-Symbole
  * `~/Coding/pools` (`MBSKY_POOLS`) – 3D-Modelle (`assets/bettermodels`) und eigene Blöcke

## Cache (nicht im Repo)

`.cache/` ist in `.gitignore`:

* `.cache/mcfont/` – die Minecraft-Schrift. Sie gehört Mojang und wird deshalb nicht eingecheckt, sondern von `mc.hole_schrift()` einmal aus dem neuesten Client-Jar im Minecraft-Ordner entpackt.
* `.cache/sprites/<auftrag>/NNN.png` – die gerenderten 3D-Modelle. Neu erzeugen mit:

```bash
python3 modelle.py            # fehlende Aufträge
python3 modelle.py --neu      # alle neu
python3 modelle.py mala_hello goblin_talk
```

`modelle.py` startet einen kleinen lokalen Server und ein kopfloses Chrome, das `modelle.html` (three.js) abarbeitet: jedes Modell mit seiner Animation, freigestellt in 512 × 512. Welche Modelle, Animationen, Zoom und Tempo, steht in `AUFTRAEGE`.

## Aufbau

| Datei | Was |
| ----- | --- |
| `basis.py` | Gerüst: `Film` aus Szenen, Überblendungen, Untertitel, Sprites, Schatten, Glanz, Tooltips, Chatzeilen. 1920 × 1080, 30 fps |
| `mc.py` | Minecraft-Optik: Schrift, Menüs, Tooltips, Chat, Tablist, HUD, Icons |
| `ton.py` | Musik (Flächen, Spieluhr, Bass), Geräusche, Malas Stimme aus den Aufnahmen, Absenken der Musik unter der Stimme, Lautheit −16 LUFS |
| `bauen.py` | Bilder parallel rendern, Ton mischen, mit ffmpeg zu MP4 (x264, crf 23) und Standbild |
| `modelle.py`, `modelle.html` | 3D-Modelle als Sprites |
| `clan_icons.py` | Entwürfe der Clan-Icons für den Clan-Film |
| `filme/*.py` | Ein Film je Datei: Szenen mit Länge und Zeichenfunktion, Texte über `L(de, en)` |

## Einen Film ändern

1. Szene in `filme/<film>.py` anpassen. Texte immer als `L("deutsch", "english")`.
2. Mit `--standbild` die betroffenen Stellen ansehen.
3. Ganz bauen, Film ansehen, beide Sprachen.
4. Ändert sich die Länge, die Angabe auf der Wiki-Seite nachziehen (DE und EN).

Fakten in den Filmen kommen aus den Docs der Plugins (`MBSkyManager/docs/`). Ändert sich dort etwas – etwa ein Preis oder eine Dauer –, den Film neu bauen.
