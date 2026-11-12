# MegaBuild.de Wiki – selbst gehostet (Astro Starlight)

Dieser Ordner baut das Wiki als statische Seite im MegaBuild-Design. Die Inhalte bleiben
die GitBook-Markdown-Dateien im Repo-Root (`SUMMARY.md`, `README.md`, `ag/`, `sb/`, `en/` …).
GitBook und die neue Seite laufen so während der Umstellung parallel, ohne dass eine Seite
doppelt gepflegt wird.

## Lokal ansehen

```bash
npm --prefix site install
npm --prefix site run dev        # http://localhost:4321, lädt bei Änderungen neu
npm --prefix site run build      # fertige Seite nach site/dist
npm --prefix site run preview    # site/dist ansehen
```

Nötig ist Node 22.23 oder neuer.

## Wie es funktioniert

`scripts/convert.mjs` läuft vor jedem `dev`/`build` und erzeugt aus den GitBook-Dateien:

- `src/content/docs/` – die Seiten mit Starlight-Frontmatter
- `src/generated/` – Seitenleiste (aus `SUMMARY.md`) und Weiterleitungen
- `public/assets/` – Kopie von `.gitbook/assets`

Alle drei sind gitignored. GitBook-Blöcke werden dabei umgewandelt:

| GitBook | Neue Seite |
| --- | --- |
| `{% hint %}` | farbiger Hinweis-Kasten |
| `{% stepper %}` | nummerierte Schritte |
| `{% tabs %}` | Tabs (Wahl wird gemerkt, z. B. Java/Bedrock) |
| `{% content-ref %}` | Karte mit Titel und Beschreibung der Zielseite |
| `{% embed %}` / `{% file %}` | Video-Player oder Link-Karte |
| `{% columns %}` | Spalten |

Bleibt ein `{%`-Block übrig, meldet der Build das als Hinweis.

### Items, Rezepte und Skilltree

Rezepte, Item-Symbole, die Mobplate-Galerie und der klickbare Skilltree-Baum brauchen
Texturen und Daten aus dem Pool, dem Minecraft-Client-Jar und MBSkyManager. Der Server hat
die nicht, darum erzeugen zwei Skripte die Ergebnisse lokal, und sie liegen eingecheckt
in `site/`:

| Skript | Liest | Schreibt |
| --- | --- | --- |
| `tools/site_items.py` | `data/items.json` | `public/items/`, `data/items.generated.json` |
| `tools/site_skilltree.py` | `data/skilltree.json`, `SKILLTREE.yml`, `config.yml`, `lang/*.yml` | `public/skilltree/`, `data/skilltree.generated.json` |

Ändert sich ein Item, eine Textur oder der Skilltree im Plugin, das passende Skript noch
einmal laufen lassen und die Ergebnisse mit committen:

```bash
python3 tools/site_items.py
python3 tools/site_skilltree.py
```

Den Baum baut `convert.mjs` aus den Tabs der Skilltree-Seite (`sb/skilltree.md`,
`en/skilltree.md`): Pfade, Biome, Quests und Preise kommen aus den erzeugten Daten, die
Bilder aus den Tabs. Gesperrte Pfade (`skilltree.locked-groups`) fehlen wie im Spiel.

## Adressen: kurz und englisch

Jede Seite hat eine kurze englische Adresse:

- Deutsch unter `/<name>/`, Englisch unter `/en/<name>/`, z. B. `/island/` und `/en/island/`.
- `<name>` ist der Dateiname der englischen Seite (`en/island.md`).
- Die Paare stehen in `locale-map.json` → `pages`.
- Deutsche Seiten ohne englisches Gegenstück, zum Beispiel das Archiv, bekommen ihre Adresse über `locale-map.json` → `slugs`.
- Alle alten GitBook-Adressen (`/sb/insel`, `/ag/befehle`, `/en/welcome`, …) leiten automatisch weiter. Dasselbe gilt für die Weiterleitungen aus `.gitbook.yaml`.

**Neue Seite im Wiki:** wie bisher in `SUMMARY.md` eintragen, dazu in `site/locale-map.json`
das Paar (`"en/neu.md": "sb/neu.md"`) oder für eine rein deutsche Seite einen Slug ergänzen.
Fehlt der Eintrag, sagt der Build das als Hinweis und nimmt den Dateipfad als Adresse.

## Auf dem Server (mbs)

Das Wiki läuft als statische Seite neben Website und Shop. `deploy/` enthält:

| Datei | Zweck |
| --- | --- |
| `build-wiki.sh` | holt neue Commits, baut in Docker (Node 24), schaltet atomar um |
| `mbwiki-build.service` / `.timer` | prüft jede Minute auf neue Commits |
| `nginx-wiki.conf.example` | nginx-Vorlage (anonymisiert) |

Ablauf eines Builds:

1. Das Skript macht `git fetch` und vergleicht den Stand mit `/var/www/wiki/.built-commit`.
2. Gibt es einen neuen Commit, baut es in einem Docker-Container.
3. Das Ergebnis kommt nach `/var/www/wiki/releases/<zeit>-<commit>`, und der Link `current` wird darauf umgestellt.
4. Die letzten 5 Stände bleiben liegen.

Bei einem fehlgeschlagenen Build bleibt der alte Stand live, und derselbe Commit wird nicht jede Minute neu versucht.

### Einrichten (einmalig, als root)

```bash
git clone https://github.com/MegaBuildDE/MBWiki.git /opt/mbwiki/repo
# solange die Seite noch nicht auf main ist (dort fehlt site/ noch):
git -C /opt/mbwiki/repo checkout feat/starlight-wiki
install -m 755 /opt/mbwiki/repo/site/deploy/build-wiki.sh /usr/local/bin/mbwiki-build
install -m 644 /opt/mbwiki/repo/site/deploy/mbwiki-build.{service,timer} /etc/systemd/system/
```

Solange die Seite noch nicht auf `main` ist, den Branch und die Test-Adresse festlegen
(`SITE_URL` landet in Sitemap, `canonical` und Vorschaubildern):

```bash
printf 'BRANCH=feat/starlight-wiki\nSITE_URL=https://wiki-neu.megabuild.de\n' > /etc/default/mbwiki-build
```

Das Skript liest die Datei selbst, sie gilt also auch beim Aufruf von Hand.

Erster Build (dauert beim ersten Mal wegen `docker pull` und `npm ci` etwas länger):

```bash
mbwiki-build && mbwiki-build --status
```

nginx: Vorlage nach `sites-available` kopieren (bzw. dorthin, wo die anderen Seiten auf mbs
liegen) und `server_name` zuerst auf eine **Test-Subdomain** setzen, z. B. `wiki-neu.megabuild.de`.
Der `location = /robots.txt`-Block darin sperrt die Test-Subdomain für Suchmaschinen, damit das Wiki
nicht doppelt bei Google steht. Für die Subdomain einen DNS-Eintrag auf den Server anlegen, dann:

```bash
nginx -t && systemctl reload nginx
certbot --nginx -d wiki-neu.megabuild.de
systemctl daemon-reload && systemctl enable --now mbwiki-build.timer
```

### Umzug von GitBook

1. Auf der Test-Subdomain alles prüfen.
2. Den Branch nach `main` mergen und `/etc/default/mbwiki-build` löschen (dann gelten `main` und
   `https://wiki.megabuild.de`), danach `mbwiki-build --force`.
3. In nginx `server_name wiki.megabuild.de` eintragen und den `robots.txt`-Block löschen.
4. Den DNS-Eintrag `wiki.megabuild.de` vom GitBook-CNAME auf den Server umstellen, dann `certbot --nginx -d wiki.megabuild.de`.
5. In GitBook die eigene Domain lösen.

Die nginx-Datei gehört anonymisiert auch ins MBWeb-Repo.

### Im Betrieb

```bash
mbwiki-build --status                   # was ist live, was ist fehlgeschlagen
mbwiki-build --force                    # aktuellen Stand neu bauen
journalctl -u mbwiki-build -n 50        # Log der letzten Builds
ln -sfn releases/<ordner> /var/www/wiki/current   # auf einen älteren Stand zurück
```

Ändert sich `deploy/build-wiki.sh` im Repo, die Kopie in `/usr/local/bin` neu installieren.
Einstellungen (Branch, Adresse, Pfade, Docker-Grenzen `--cpus=4 --memory=2g`) stehen oben im Skript
und lassen sich in `/etc/default/mbwiki-build` überschreiben.
