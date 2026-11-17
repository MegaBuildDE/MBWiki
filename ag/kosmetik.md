---
description: >-
  Kosmetik für Ränge auf MegaBuild.de – Spuren, Präfix-Stile, Namensfarben,
  Chat-Emojis, Insel-Begrüßung und dein Luftschiff.
icon: wand-magic-sparkles
---

# Kosmetik

Kosmetik ändert nur, wie du, dein Name oder deine Insel aussehen. Einen Vorteil im Spiel gibt sie nicht: kein Mana, kein Ruby, nichts im Kampf. Du bekommst sie mit einem [Rang](rang.md), und jeder höhere Rang hat alles vom Rang darunter.

| Was | Gold | Platin | Titan |
| --- | --- | --- | --- |
| [Spuren](#spuren) | 2 | 6 | alle 16 |
| [Präfix-Stil](#präfix-stile) – dein Rang-Abzeichen | einfarbig | 4 Farbverläufe | dazu 3 animierte |
| [Namensfarbe](#namensfarbe) | – | 12 Farben | dazu 6 Verläufe |
| [Chat-Emojis](#chat-emojis) | 24 | 24 | 24 |
| [Insel-Begrüßung](#insel-begrüßung) | 3 Laute | 3 Laute | 7 Laute |
| [Luftschiff](#luftschiff) | Gold-Wimpel | Platin-Wimpel, 2 Anstriche | Titan-Segel, alle 8 Anstriche |

Fehlt dir der Rang später, bleibt deine Wahl gespeichert. Sie ist nur nicht zu sehen und kommt mit dem Rang zurück.

## Das Kosmetik-Menü

```
/cosmetics
```

`/cosmetics` – kurz `/cos` – öffnet das Kosmetik-Menü. Es geht auf den **Sky-Inseln**. Jede Kachel führt zu einer Seite: Spuren, Präfix, Namensfarbe, Emojis, Luftschiff und Begrüßung. Kacheln, die grau sind und „bald“ zeigen, gibt es noch nicht.

Was dir fehlt, steht grau in der Liste, mit dem Rang, in dem es enthalten ist. Kaufen kannst du im Menü nichts.

### Was ich sehe

Unter **Was ich sehe** blendest du aus, was andere tragen – nur für dich. Jeder Schalter ist von Haus aus an:

* **Spuren** – die Spuren anderer Spieler,
* **Begrüßungen** – die Begrüßungen fremder Inseln.

Die übrigen Schalter gehören zu Kosmetik, die noch kommt. `/cosmetics view` öffnet die Seite direkt.

## Spuren

```
/trail [Spur]
/trail off
```

Eine Spur zieht hinter dir her. Es gibt zwei Sorten:

* **Partikelspur** – an deinen Füßen, wenn du gehst oder läufst. Im Stehen und beim Schleichen nicht.
* **Elytra-Spur** – hinter dir, wenn du mit der Elytra gleitest.

Du trägst immer **eine** Spur. `/trail` öffnet die Liste, ein Klick legt eine Spur an. `/trail <Spur>` wählt direkt, etwa `/trail cherry`, und `/trail off` legt sie ab.

**Vorschau:** Klickst du eine Spur an, die du noch nicht hast, siehst du sie **10 Sekunden** lang an dir – nur du. `/cosmetics preview <Spur>` macht dasselbe.

| Spur | `/trail` | Sorte | Rang |
| ---- | -------- | ----- | ---- |
| Kirschblüten | `cherry` | Partikel | Gold |
| Kondensstreifen | `contrail` | Elytra | Gold |
| Notenspur | `notes` | Partikel | Platin |
| Glühwürmchen | `fireflies` | Partikel | Platin |
| Kometenschweif | `comet` | Elytra | Platin |
| Flammenflügel | `wingfire` | Elytra | Platin |
| Seelenflämmchen | `soulfire` | Partikel | Titan |
| Runen | `runes` | Partikel | Titan |
| Sporenblüte | `spores` | Partikel | Titan |
| Funkenschlag | `sparks` | Partikel | Titan |
| Blasses Laub | `paleleaves` | Partikel | Titan |
| Portalwirbel | `vortex` | Elytra | Titan |
| Seelenzug | `souls` | Elytra | Titan |
| Totemglanz | `totem` | Elytra | Titan |
| Leuchtband | `glow` | Elytra | Titan |
| Goldfunken | `goldsparks` | Elytra | Titan |

* **Wo:** auf allen Sky-Inseln, auch als Besucher. Nicht in den 10 Sekunden nach einem Treffer und nicht, wenn du unsichtbar bist.
* **Clan-Flugspur:** Eine Elytra-Spur verdeckt die [Flugspur deines Clans](../sb/clans.md#vorteile-im-alltag). Legst du sie ab, fliegst du wieder mit der Clan-Flugspur. Sie steht auch in der Spurenliste – ein Klick darauf legt deine Elytra-Spur ab.
* **Auf Bedrock** sehen die Partikel ähnlich aus, Größe und Flugbahn weichen etwas ab.

## Präfix-Stile

```
/prefix
```

Dein Rang steht als **Abzeichen** vor deinem Namen, im Chat und in der Tablist. Mit `/prefix` wählst du, wie es aussieht:

| Rang | Stile |
| ---- | ----- |
| Gold | das Gold-Abzeichen, einfarbig |
| Platin | **Farbverläufe:** Eis, Abendrot, Smaragd, MegaBuild |
| Titan | die vier Verläufe und dazu **animiert:** Glanz, Puls, Funkeln |

* **Animierte Stile** bewegen sich in der Tablist. Im Chat steht ihr erstes Bild – eine Chatzeile ändert sich nach dem Senden nicht mehr.
* **Standard** bringt dein Abzeichen zurück, wie es ist.
* **Auf Bedrock** steht das Abzeichen nur im Chat. Die Tablist zeigt dort nur die Namen.

## Namensfarbe

```
/namecolor
/namecolor reset
```

Ab **Platin** färbst du mit `/namecolor` deinen Namen, im Chat und in der Tablist.

* **Platin – 12 Farben:** Dunkelblau, Dunkelgrün, Dunkeltürkis, Lila, Gold, Grau, Blau, Grün, Türkis, Rosa, Gelb, Weiß.
* **Titan – dazu 6 Verläufe:** Sonne, Ozean, Wald, Polarlicht, Eis, MegaBuild.
* Hast du einen [Nick](rang.md#nick), bekommt er dieselbe Farbe.
* **Im Clan-Chat**, bei `/msg` und in der Post steht dein Name ohne Farbe.
* `/namecolor reset` nimmt die Farbe wieder weg.
* **Auf Bedrock** stehen die Farben im Chat genauso da, Verläufe in Stufen. In der Tablist bleibt dein Name dort ohne Farbe.

## Chat-Emojis

```
/emojis
```

Ab **Gold** wird `:name:` zu einem Bild, etwa `:herz:`, `:feuer:` oder `:gg:`. Höchstens **5 je Nachricht**, Groß- und Kleinschreibung ist egal.

* **Wo:** im Globalchat, im Chat deines Servers, im Clan-Chat, bei `/msg` und in der [Post](nachrichten.md#das-postfach).
* **Ohne Rang** bleibt `:herz:` einfach Text.
* `/emojis` zeigt alle 24. Ein Klick schreibt den Namen in deine Chatzeile.

Die 24 Emojis: `:lachen:` `:grinsen:` `:zwinkern:` `:cool:` `:traurig:` `:weinen:` `:wuetend:` `:staunen:` `:verliebt:` `:denken:` `:herz:` `:daumen:` `:feuer:` `:stern:` `:pokal:` `:mana:` `:ruby:` `:luftschiff:` `:insel:` `:krone:` `:geschenk:` `:party:` `:gg:` `:schlafen:` – statt `:wuetend:` geht auch `:wütend:`.

## Insel-Begrüßung

```
/sky greeting
```

Ab **Gold** begrüßt deine Insel ihre Besucher: mit einem **Titel**, einem **Untertitel** und einem **Laut**. Einstellen kann das nur der **Inselbesitzer**. `/sky greeting` öffnet das Menü mit Vorschau, Titel, Untertitel, Laut und dem Schalter an oder aus.

1. **Titel und Untertitel** schreibst du nach einem Klick in den Chat. Zusammen höchstens **48 Zeichen**, ohne Links. Farben gehen mit `&`-Codes, RGB und Verläufe ab Platin. Mit `abbrechen` bleibt alles, wie es war.
2. **Den Laut** wählst du aus einer Liste. Ein Klick spielt ihn zum Probehören – auch die, die du noch nicht hast.

| Rang | Laute |
| ---- | ----- |
| Gold, Platin | Glocke, Harfe, Möwen |
| Titan | dazu Ziegenhorn, Windspiel, Amethyst-Klang, Trommel |

* **Wer sie sieht:** Besucher, wenn sie auf deiner Insel ankommen – jeder höchstens alle **10 Minuten**. Deine Inselmitglieder nicht, und auf der Clan-Insel gibt es keine Begrüßung.
* **Ausblenden** können Besucher fremde Begrüßungen unter [Was ich sehe](#was-ich-sehe).
* **Die Regeln:** Der Chatfilter gilt, und die Begrüßung darf nicht so klingen, als käme sie vom Team. Das Team kann sie zurücksetzen.
* **Ohne Rang** fallen Farben und Titan-Laute weg. Warst du **35 Tage** auf keiner Sky-Insel, ruht die Begrüßung, bis du wiederkommst.

## Luftschiff

```
/sky ship
```

Das Luftschiff vor deiner Insel zeigt deinen Rang:

* **Gold** – ein gelber Wimpel am Bug,
* **Platin** – ein hellblauer Wimpel,
* **Titan** – ein eigenes Segel in Blau und Weiß.

Es hängt immer nur das Zeichen deines höchsten Rangs. Du kannst es auch abschalten.

Ab **Platin** streichst du das Schiff neu an:

| Rang | Anstriche |
| ---- | --------- |
| Platin | Smaragd, Nachthimmel |
| Titan | alle acht: Standard, Smaragd, Nachthimmel, Kirschholz, Eis, Kupfer, Nether, Sonnenuntergang |

**So geht's:** `/sky ship` öffnet das Menü – auch die Karte **Luftschiff** im Inselmenü und die Kachel im Kosmetik-Menü.

* **Linksklick** wählt einen Anstrich. Das darf nur der Inselbesitzer.
* **Rechtsklick** zeigt dir **20 Sekunden** lang, wie das Schiff damit aussieht – nur dir, in Sichtweite des Schiffs. Das geht für jeden, auch für Gäste.
* **Ist jemand an Bord** oder landet gerade jemand, merkt sich das Schiff deine Wahl und wird danach gestrichen.
* **Die Clan-Insel** behält ihr Schiff, wie es ist.
* **Ohne Rang** trägt das Schiff wieder Standard und das höchste Zeichen, das dir noch zusteht.

| Befehl | Was er macht |
| ------ | ------------ |
| `/sky ship` | Das Luftschiff-Menü. Auch `/sky ship paint`, `/sky schiff` |
| `/sky ship paint <Anstrich>` | Einen Anstrich direkt wählen: `standard`, `emerald`, `nightsky`, `cherry`, `ice`, `copper`, `nether`, `sunset` |
| `/sky ship preview <Anstrich>` | 20 Sekunden Vorschau, nur für dich. Mit `gold`, `platin` oder `titan` siehst du Wimpel oder Segel |
| `/sky ship badge on` · `off` | Wimpel oder Segel an- oder abschalten |

## Verwandte Seiten

* [Ränge](rang.md)
* [Pets](pets.md)
* [Befehle](befehle.md#kosmetik)
* [Nachrichten & Post](nachrichten.md)
* [Clans](../sb/clans.md)
