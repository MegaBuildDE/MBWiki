---
description: >-
  ChestShops auf MegaBuild.de – mit Schild und Kiste gegen Ruby handeln, Angebote
  im ganzen Netzwerk suchen, hinreisen und einen eigenen Markt eröffnen.
icon: store
---

# ChestShops

Mit einem **ChestShop** handelst du mit anderen Spielern: Ein Schild an einer Kiste nennt Ware, Menge und Preis, ein Klick aufs Schild kauft oder verkauft. Bezahlt wird **nur mit [Ruby](eco.md#ruby)**. Öffnest du einen Bereich deiner Insel als **Markt**, finden ihn Spieler aus dem ganzen Netzwerk in der Shopsuche und reisen direkt zu dir.

{% hint style="info" %}
Shops gibt es nur auf den Inseln, nicht in der Lobby. Alle Shops gehören Spielern – es gibt keine Admin-Shops.
{% endhint %}

## Kaufen und verkaufen

| Du willst | Java | Bedrock |
| --------- | ---- | ------- |
| **Kaufen** | Rechtsklick aufs Schild | Schild antippen |
| **Verkaufen** | Linksklick aufs Schild | Schild gedrückt halten |
| **Handelsmenü** | Schleichen + Rechtsklick | Schleichen und antippen |

Das **Handelsmenü** zeigt Ware und Vorrat und hat je einen Knopf zum Kaufen und Verkaufen. Es ist vor allem für Touchscreens gedacht und geht nur, solange du höchstens 8 Blöcke vom Schild entfernt stehst.

### So liest du ein Schild

| Zeile | Beispiel | Bedeutung |
| ----- | -------- | --------- |
| 1 | `Tom` | Wem der Shop gehört |
| 2 | `16` | Menge je Handel |
| 3 | `B 16 : 10 S` | Preise in Ruby für die ganze Menge: **B** kaufst du hier, **S** verkaufst du hier |
| 4 | `Eichenstamm` | Die Ware |

Steht nur `B` oder nur `S` auf dem Schild, geht auch nur das. Ein `*` hinter der Ware heißt, dass sie vom schlichten Item abweicht – etwa verzaubert, umbenannt oder abgenutzt.

### Wann ein Handel durchgeht

Gehandelt wird immer die ganze Menge vom Schild.

* **Beim Kauf** braucht der Shop genug Ware, du genug Ruby und Platz im Inventar.
* **Beim Verkauf** brauchst du genau diese Ware im Inventar oder in der Zweithand, der Shop Platz und sein Besitzer genug Ruby. Angelegte Rüstung zählt nicht.
* An deinem eigenen Shop kannst du nicht handeln.
* Geht ein Handel nicht durch, sagt dir der Chat, warum, und es wird nichts gebucht. Nur wenn er eine „unklare“ Buchung meldet, prüfst du mit `/bal` deinen Stand.
* Eine Gebühr gibt es nicht. Die Ruby gehen direkt von Konto zu Konto.

{% hint style="info" %}
**Neue Konten** geben Ruby erst **24 Stunden nach dem ersten Login** und nach **20 Minuten Spielzeit** aus. Bis dahin kannst du verkaufen, aber nichts kaufen. Wie lange es noch dauert, sagt dir der Chat. Auch ein Shop-Besitzer mit neuem Konto kann noch nichts ankaufen.
{% endhint %}

## Shops finden

`/shop` öffnet das Shop-Menü. Du findest es auch im `/sky`-Menü deiner Insel unter **Shops**.

| Knopf | Was er macht |
| ----- | ------------ |
| **Suchen** | Item-Namen in den Chat tippen, mindestens 2 Zeichen. Deutsch und Englisch gehen, auch Teilwörter: „Eisen“ findet Eisenbarren, Eisenerz … |
| **Item in der Hand suchen** | Zeigt, wer das Item in deiner Haupthand handelt |
| **Alle Angebote** | Jedes offene Angebot im Netzwerk |
| **Märkte** | Die offenen Shop-Bereiche aller Inseln. Ein Klick reist hin |
| **Meine Shops** | Deine eigenen Shops auf allen Inseln mit Vorrat und Platz |
| **Shop-Bereiche** | Die Bereiche dieser Insel, wenn du sie verwalten darfst |
| **Zurück zur eigenen Insel** | Nur, wenn du gerade als Kunde unterwegs bist |

In den Angebotslisten stehen nur Shops, an denen du gerade handeln kannst. Du kannst nach **Kaufen** und **Verkaufen** filtern und nach **Günstig** oder **Neu** sortieren – beim Verkaufen steht dann vorn, wer am meisten zahlt.

## Hinreisen

Ein Klick auf ein Angebot öffnet **Hinreisen?** – mit einem weiteren Klick auf **Hinreisen** bist du unterwegs. Du landest direkt vor dem Schild oder am Ankunftspunkt des Marktes.

* **Dein ganzes Inventar reist mit.** Endertruhe und Level bleiben auf jeder Insel für sich.
* **Abklingzeit:** Zwischen zwei Reisen liegen 20 Sekunden.
* **Nicht losreisen** kannst du, wenn du in den letzten 5 Sekunden Schaden bekommen hast, gerade fällst oder gleitest.
* **Schlafende Inseln** werden nicht geweckt. Dann heißt es „Diese Insel schläft gerade“, und du versuchst es später noch einmal.
* **Fällt eine Reise aus,** bleibst du, wo du bist, und dir fehlt nichts.

**Zurück** kommst du mit `/shop home`, ohne Abklingzeit. Schläft deine Insel oder hast du keine, geht es in die Lobby.

## Als Kunde auf fremden Inseln

Hast du auf der Insel keinen Zugang, kommst du als **Kunde** – auch wenn du dort sonst [zuschauen](reisen.md) dürftest. Mit Zugang – als Mitglied, über Clan oder Freunde – bist du kein Kunde und hast dort deine normalen [Rechte](mitglieder.md#die-rechte).

| Als Kunde darfst du | Als Kunde darfst du nicht |
| ------------------- | ------------------------- |
| An Shop-Schildern kaufen und verkaufen | Blöcke abbauen oder setzen, Schilder bearbeiten, ernten |
| Essen und trinken – außer der unheilvollen Flasche | Behälter öffnen, auch Shop-Kisten und die Endertruhe |
| Chatten | Tiere, Bewohner, Warpetts, Rahmen oder Fahrzeuge benutzen |
| `/shop`, `/bal`, `/msg`, `/r`, `/friend`, `/mail` und `/lobby` | Angreifen, Geschosse werfen, angeln |
| Deine eigenen Items aufheben | Items wegwerfen und fremde Items aufheben |
| | Fliegen, gleiten, Portale benutzen, per Enderperle oder Chorusfrucht den Markt verlassen |

* **Du bleibst im Markt.** An der Grenze des Bereichs geht es zurück („Hier endet der Markt“). Fällst du unten hinaus, landest du wieder am Ankunftspunkt.
* **Dir passiert nichts.** Du bekommst keinen Schaden, und Mobs greifen dich nicht an. Stirbst du doch, behältst du Inventar und Level.
* **Mana gibt es hier nicht,** und Bewohner sprechen dich nicht an.
* **Schließt der Markt,** reist du automatisch nach Hause.
* Eine Insel nimmt höchstens **10 Kunden** zugleich. Die letzten 4 Plätze bleiben dem Besitzer und den Mitgliedern.

## Einen Shop eröffnen

Das dürfen der **Inselbesitzer** und Mitglieder mit dem Recht **Skilltree** – die Vorlage **Verwalter** hat es. Mehr dazu unter [Mitglieder & Rechte](mitglieder.md#die-rechte).

{% stepper %}
{% step %}
#### Shop-Bereich anlegen

Shops stehen nur in einem [Shop-Bereich](#shop-bereiche). Schild und Behälter müssen im selben Bereich liegen, offen oder zu.
{% endstep %}

{% step %}
#### Behälter aufstellen

Eine **Truhe**, **Falltruhe**, ein **Fass** oder eine **Kupfertruhe**, auch gewachst. Leg die Ware hinein. Eine Doppeltruhe zählt mit beiden Hälften.
{% endstep %}

{% step %}
#### Schild anbringen

Ein **Wand- oder Standschild** an den Behälter, darauf oder darunter. Hängeschilder gehen nicht.
{% endstep %}

{% step %}
#### Schild beschriften

**Zeile 1** ist egal, dort trägt der Server deinen Namen ein. **Zeile 2** ist die Menge, **Zeile 3** der Preis, **Zeile 4** die Ware. Der Chat meldet „Shop eröffnet“.
{% endstep %}
{% endstepper %}

Danach ist das Schild gewachst. Willst du etwas ändern, baust du es ab und stellst es neu auf.

### Zeile 3: der Preis

| Du schreibst | Das bedeutet |
| ------------ | ------------ |
| `B 10` | Kunden kaufen für 10 Ruby |
| `S 5` | Kunden verkaufen für 5 Ruby – du kaufst an |
| `B 10 : 5 S` | Beides |
| `B frei` oder `B 0` | Du verschenkst die Ware |

Groß- und Kleinschreibung und Leerzeichen sind egal, der Buchstabe darf vor oder hinter der Zahl stehen. **Zwei Preise trennt immer ein Doppelpunkt** – `B 10 S 5` bleibt ein gewöhnliches Schild.

### Zeile 4: die Ware

* **Leer oder `?`:** Das erste Item im Behälter, genau so, wie es dort liegt – mit Name, Verzauberungen und Haltbarkeit. So verkaufst du besondere Items.
* **Ein Name:** `Diamant`, `diamond` oder `minecraft:diamond`. Umlaute gehen auch als `ae`, `oe`, `ue`. Damit handelst du das schlichte Item ohne Verzauberung.

Tragen mehrere Items denselben Namen, etwa „Netherziegel“ oder „Schallplatte“, nennt dir der Chat die genauen Namen.

### Beispiele

| Zeile 2 | Zeile 3 | Zeile 4 | Das bedeutet |
| ------- | ------- | ------- | ------------ |
| `16` | `b16` | `Eichenstamm` | Kunden kaufen 16 Eichenstämme für 16 Ruby |
| `1` | `S 40 : B 60` | leer, verzaubertes Schwert in der Kiste | Kunden kaufen das Schwert für 60 Ruby und verkaufen genau so eines für 40 |
| `64` | `5 s` | `?`, Kopfsteinpflaster in der Kiste | Du kaufst 64 Kopfsteinpflaster für 5 Ruby an |

### Grenzen

* **Menge:** 1 bis 2.304 je Handel. Sie muss einmal in den leeren Behälter und in ein Inventar passen.
* **Preis:** 0 bis 1.000.000 Ruby.
* **Anzahl:** 50 Shops je Spieler im ganzen Netzwerk, 200 je Insel.
* **Gesperrte Ware:** [Mana-Kugeln](eco.md#mana-kugeln), Mana-Ladungen, [Mana-Blöcke und Mana-Scherben](furnace-golem.md#handel), Bedrock, Befehlsblöcke, Spawner und andere technische Blöcke – auch in einer Shulkerkiste oder einem Bündel. Mana-Äpfel und Plates gehen, siehe [Mobplates](mobplates.md#regeln).
* **Kein Shop geht:** an einem Behälter, an dem ein anderer Spieler schon einen Shop hat, in einer Siedlung der Bewohner, nah am Weltspawn und an der Projektkiste eines Clans. Beutekisten öffnest du vorher einmal.

## Deinen Shop führen

| Du willst | So geht's |
| --------- | --------- |
| Vorrat und Platz sehen | Rechtsklick auf dein Schild, oder `/shop mine` |
| Den Shop auflösen | Linksklick auf dein Schild |
| Ware nachlegen oder abholen | Den Behälter öffnen |

* **Den Behälter öffnen** dürfen nur der Shop-Besitzer, der Inselbesitzer und das Team – andere Mitglieder nicht.
* **Der Inselbesitzer** baut einen fremden Shop auf seiner Insel mit Schleichen + Linksklick ab.
* **Baust du den Behälter ab,** werden alle Shops daran aufgelöst und ihre Schilder wieder gewöhnliche Schilder. Das geht nur, wenn dir alle Shops daran gehören oder die Insel dir gehört.
* **Einnahmen:** Bist du auf derselben Insel, siehst du jeden Handel sofort im Chat. Sonst kommt beim nächsten Betreten einer Insel eine Zeile: „Seit deinem letzten Besuch: 12 Verkäufe, +192 Ruby.“
* **Ankaufen** zahlst du von deinem eigenen Konto. Hast du zu wenig Ruby, geht der Verkauf nicht durch und der Kunde behält seine Ware.

Shop-Blöcke sind geschützt: Explosionen, Feuer, Kolben und Mobs können ihnen nichts anhaben, und ein Schild bleibt hängen, auch wenn sein Halt verschwindet. **Trichter** dürfen deinen Behälter füllen und leeren. Unter einen fremden Shop-Behälter setzen oder eine Truhe daran anbauen darf nur, wer ihn öffnen darf.

## Shop-Bereiche

Ein Shop-Bereich ist ein Quader auf deiner Insel: Nur darin stehen Shops, und nur darin bewegen sich Kunden. Das Anlegen ist **kostenlos**. Verwalten dürfen ihn der Inselbesitzer und Mitglieder mit dem Recht **Skilltree**.

{% stepper %}
{% step %}
#### Bereich anlegen

`/shop areas` → **Neuer Bereich** und den Namen in den Chat tippen, höchstens 24 Zeichen. Der Bereich beginnt als 3 × 3 um dich herum und ist zunächst **zu**.
{% endstep %}

{% step %}
#### Ecken setzen

Stell dich an zwei gegenüberliegende Ecken und klicke **Ecke 1 hierher** und **Ecke 2 hierher**. Die Höhe wächst von selbst: 4 Blöcke unter die tiefere Ecke, 24 über die höhere.
{% endstep %}

{% step %}
#### Ankunftspunkt setzen

Stell dich auf festen, harmlosen Boden im Bereich und klicke **Ankunftspunkt hierher**. Hier kommen Kunden an. Deine Blickrichtung bleibt erhalten – schau also auf deinen Markt.
{% endstep %}

{% step %}
#### Öffnen

Klicke im Menü auf den Schalter **Zu**, dann steht er auf **Offen**. Das geht erst mit einem Ankunftspunkt. Dein Markt erscheint jetzt in der Shopsuche.
{% endstep %}
{% endstepper %}

**Grenzen zeigen** lässt die Kanten 10 Sekunden lang leuchten, nur für dich: grün für offen, orange für zu, dazu eine hellblaue Säule am Ankunftspunkt.

### Offen und zu

| | Offen | Zu |
| --- | --- | --- |
| **In Shopsuche und Märkten** | Ja | Nein |
| **Kunden reisen hin** | Ja | Nein |
| **Wer handeln darf** | Alle | Inselbesitzer, Mitglieder, Team und wer auf der Insel selbst einen Shop hat |

Ein Freund, der nur zu Besuch ist, oder ein [Zuschauer](reisen.md) handelt in einem geschlossenen Bereich also nicht. **Schließt du einen Markt,** reisen alle Kunden darin sofort nach Hause.

### Regeln für Bereiche

* **Größe:** 3 bis 48 Blöcke breit und lang.
* **Anzahl:** höchstens 3 Bereiche je Insel. Sie dürfen sich nicht überschneiden.
* **Ort:** nur in der Inselwelt und ohne Blöcke deines Luftschiffs.
* **Schrumpfen:** Ein Bereich mit Shops darf wachsen, aber nur so weit schrumpfen, dass alle Shop-Schilder und Behälter drin bleiben.
* **Löschen** geht erst, wenn keine Shops mehr darin stehen.

## Befehle

| Befehl | Was er macht |
| ------ | ------------ |
| `/shop` | Shop-Menü. Auch `/shops`, `/sky shop` |
| `/shop search [Begriff]` | Angebote aller Inseln suchen. Auch `/shop suche` |
| `/shop hand` | Wer handelt das Item in deiner Haupthand? |
| `/shop list` | Alle Angebote |
| `/shop markets` | Offene Märkte aller Inseln. Auch `/shop märkte` |
| `/shop mine` | Deine Shops mit Vorrat und Platz. Auch `/shop meine` |
| `/shop areas` | Shop-Bereiche dieser Insel. Auch `/shop bereiche` |
| `/shop home` | Zurück auf deine eigene Insel. Auch `/shop heim` |
| `/shop help` | Hilfe im Chat |

## Verwandte Seiten

* [Mana & Ruby](eco.md)
* [Mitglieder & Rechte](mitglieder.md)
* [Deine Insel](insel.md)
* [Mobplates](mobplates.md)
* [Befehle](../ag/befehle.md)
