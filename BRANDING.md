# MegaBuild.de Wiki – Design & Branding

Diese Datei ist **interne Doku** und steht bewusst nicht in `SUMMARY.md` – sie wird von GitBook nicht veröffentlicht.

Sie hält fest, wie das Wiki an den Style von [megabuild.de](https://megabuild.de/) angeglichen wird.

---

## Wichtig: Was geht aus dem Repo, was nicht

GitBook trennt **Inhalt** (Git) von **Aussehen** (GitBook-UI):

| Bereich | Wo einstellbar |
| --- | --- |
| Seitenstruktur, Texte, Blöcke, Seiten-Icons, Cover | ✅ Repo (dieses Git-Repo) |
| Theme-Farben, Schriftart, Logo, Favicon, Footer | ❌ Nur GitBook-UI |
| Eigenes CSS / JS | ❌ Von GitBook nicht unterstützt |

Der Repo-Teil ist bereits umgesetzt. Die folgenden Werte müssen **einmalig in der GitBook-UI** gesetzt werden.

---

## Design-Tokens von megabuild.de

Ausgelesen aus `https://megabuild.de/css/global.css` (`:root`):

### Farben

| Token | Hex / Wert | Verwendung |
| --- | --- | --- |
| `--mb-color-primary` | `#C985FF` | Primärfarbe (hell, für Dark Mode) |
| `--mb-color-primary-strong` | `#A958FF` | Primärfarbe kräftig (für Light Mode) |
| `--mb-color-bg` | `#170D29` | Seitenhintergrund |
| `--mb-color-bg-soft` | `#22153A` | Hintergrund abgesetzt |
| `--mb-color-surface` | `rgba(66, 43, 108, 0.78)` | Karten / Flächen |
| `--mb-color-surface-strong` | `rgba(81, 55, 132, 0.92)` | Karten hervorgehoben |
| `--mb-color-text` | `#FFFAFF` | Fließtext |
| `--mb-color-text-soft` | `#DDD2EE` | Text abgeschwächt |
| `--mb-color-text-muted` | `#AB9DC0` | Hilfstext |
| `--mb-color-border` | `rgba(211, 176, 255, 0.18)` | Rahmen |
| `--mb-color-success` | `#8CFFB8` | Erfolg / positiv |
| `--mb-color-danger` | `#FF9292` | Warnung / negativ |

Der Shop nutzt zusätzlich `theme-color = #C985FF` – dieselbe Primärfarbe.

### Typografie

* **Headings & Body:** `Geist`
* **Monospace / Code:** `Geist Mono`

Beides sind lokal eingebundene Webfonts der Website (`/css/fonts/local/geist-regular.woff2`, `geist-mono.woff2`). Geist ist eine freie Schrift von Vercel.

---

## Einstellungen in der GitBook-UI

Zu finden unter **Site settings → Customization**.

### 1. Theme

* **Mode:** Dark als Standard – megabuild.de ist durchgehend dunkel
* **Header / Background:** `Gradient` oder `Bold` kommt dem violetten Verlauf der Website am nächsten

### 2. Farben

* **Primary color (Dark mode):** `#C985FF`
* **Primary color (Light mode):** `#A958FF`

Falls semantische Farben verfügbar sind (Premium/Ultimate):

* **Success:** `#8CFFB8`
* **Danger / Warning:** `#FF9292`

### 3. Schrift

* **Primary font:** `Geist`
* **Monospace font:** `Geist Mono`

> Custom Fonts erfordern einen Premium- oder Ultimate-Plan. Ist das nicht verfügbar, ist **Inter** der nächstbeste Ersatz aus der GitBook-Standardauswahl.

### 4. Logo & Favicon

Die Assets liegen bereits im Repo unter `.gitbook/assets/`:

| Datei | Größe | Verwendung |
| --- | --- | --- |
| `mb-logo.png` | 64×64 | Favicon |
| `mb-logo-round.png` | 512×512 | Logo im Header |

Quelle: `megabuild.de/images/mblogo.png` bzw. `mblogo-normal-rund.png`.

> Ein eigenes Logo erfordert ebenfalls Premium/Ultimate. Ohne diesen Plan bleibt es beim Titel-Text.

### 5. Footer

Falls verfügbar, passend zur Website verlinken:

* Regeln – `https://megabuild.de/rules/`
* AGB – `https://megabuild.de/terms/`
* Impressum – `https://megabuild.de/imprint/`
* Datenschutz – `https://megabuild.de/privacy/`

Copyright-Text: `© 2026 MegaBuild.de – nicht verbunden mit Mojang oder Microsoft.`

---

## Was im Repo bereits umgesetzt ist

* **Cover-Bilder** auf den Einstiegsseiten – echte Skyblock-Screenshots von megabuild.de
* **Seiten-Icons** über `icon:` im Frontmatter (Font Awesome), passend zum Thema jeder Seite
* **Zwei-Spalten-Layouts** (`{% columns %}`) analog zu den Feature-Karten der Website
* **Stepper-Blöcke** für alle Anleitungen
* **Hint-Blöcke** in der Farblogik der Website (Warnung für den Wartungsmodus, Erfolg für Tipps)
* **Tabs** für Java-/Bedrock-Anleitungen
* **Emoji-Gruppen** in `SUMMARY.md`, angelehnt an die Navigation der Website

## Assets

| Datei | Herkunft |
| --- | --- |
| `.gitbook/assets/mb-logo.png` | `megabuild.de/images/mblogo.png` |
| `.gitbook/assets/mb-logo-round.png` | `megabuild.de/images/mblogo-normal-rund.png` |
| `.gitbook/assets/mb-skyblock-one.jpg` | `megabuild.de/images/about-img-one.jpg` |
| `.gitbook/assets/mb-skyblock-two.jpg` | `megabuild.de/images/about-img-two.jpg` |
| `.gitbook/assets/mb-skyblock-three.jpg` | `megabuild.de/images/about-img-three.jpg` |

---

## Mehrsprachigkeit

Aktuell liegen DE und EN als **zwei Gruppen in einer SUMMARY** (`## 🇬🇧 English`). Das funktioniert ohne Zusatzkonfiguration.

Sauberer wäre GitBooks **Variants**-Feature (echter Sprachumschalter wie der DE/EN-Toggle auf megabuild.de). Das erfordert allerdings mehrere GitBook-Sections mit je eigenem Git-Sync-Verzeichnis – ein bewusster Umbau, kein Repo-Change.

---

## Offene Inhalte

Das Wiki dokumentiert bewusst **keine geschätzten Skyblock-Werte**. Sobald der Server startet, sind zu ergänzen:

* Befehlsübersicht
* Inselgrößen und Upgrade-Stufen
* Generator-Typen und Farm-Mechaniken
* Währung, Spielershops, Handelssysteme
* Vote-Belohnungen
* Rang-Perks für Skyblock
* Event-Ablauf und Belohnungen

Die entsprechenden Stellen sind in den Seiten mit einem `hint style="warning"` markiert.
