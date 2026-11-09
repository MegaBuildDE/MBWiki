---
description: >-
  Spieler auf deine Insel einladen, festlegen, was sie dort dürfen, deinem Clan
  und deinen Freunden Zugang geben und bestimmen, wer zuschauen darf.
icon: users-gear
---

# Mitglieder & Rechte

Du kannst bis zu **25 Mitglieder** auf deine Insel einladen und für jedes einzeln festlegen, was es darf. Deinem [Clan](clans.md) und deinen Freunden gibst du Zugang auch ohne Einladung – siehe [Clan und Freunde](#clan-und-freunde). Wer sich deine Insel nur ansehen darf, legst du unter [Zuschauen](#zuschauen) fest.

## Mitglied einladen

{% stepper %}
{% step %}
#### Menü öffnen

**In der Lobby:** `/sky` → **Mitglieder** → **Mitglied hinzufügen**

**Auf der Insel:** `/sky friends` → **Mitglied hinzufügen**
{% endstep %}

{% step %}
#### Spieler auswählen

Zuerst siehst du deine Freundesliste. Über die Suche findest du alle Spieler im Netzwerk, auch offline – gib dafür mindestens **3 Zeichen** des Namens ein.
{% endstep %}

{% step %}
#### Bestätigen

Klicke auf **Einladen**. Der Spieler bekommt eine Nachricht und eine Post und darf deine Insel ab sofort betreten – als **Mitbauer**.
{% endstep %}
{% endstepper %}

Einladen dürfen der Besitzer und Mitglieder mit dem Recht **Mitglieder**.

## Die Rechte

| Recht | Was es erlaubt |
| ----- | -------------- |
| **Bauen** | Blöcke setzen und abbauen, Eimer, Feuer, Rüstungsständer, Rahmen, Schilder |
| **Behälter** | Kisten, Fässer, Öfen, Trichter, Braustände, Lesepulte, das Menü des [Furnace Golem](furnace-golem.md) |
| **Schalter** | Türen, Falltüren, Zauntore, Knöpfe, Hebel, Druckplatten |
| **Tiere** | Tiere schlagen, füttern, züchten, anleinen, scheren, melken, reiten |
| **Ernten** | Reife Pflanzen ernten und neu pflanzen |
| **Warpetts** | [Warpett](warpetts.md)-Blumen und -Eier nutzen und setzen, Warpetts mit einer [Mobplate](mobplates.md) einsammeln und absetzen |
| **Skilltree** | Biome kaufen, Lieblinge setzen, den Clan um Hilfe bitten, [Shops](chestshop.md) eröffnen, [Shop-Bereiche](chestshop.md#shop-bereiche) verwalten |
| **Mitglieder** | Mitglieder, Rechte und Zugang verwalten |
| **Statistik** | Die Statistik der Insel ansehen |

Dazu kommt der Schalter **Betreten**: Ist er aus, kommt das Mitglied nur noch über den Clan- oder Freunde-Zugang auf die Insel – oder als [Zuschauer](reisen.md) ohne Rechte, wenn du das [Zuschauen](#zuschauen) erlaubst.

**Ohne besonderes Recht** darf jeder, der auf der Insel mitspielt, Monster bekämpfen, Gegenstände aufheben, angeln, mit Bewohnern und Forestlingen sprechen und handeln, Schilder anklicken, die Endertruhe und Werkbänke ohne Speicher benutzen – Werkbank, Steinsäge, Webstuhl, Kartentisch, Schmiedetisch, Schleifstein, Zaubertisch und Amboss. Für [Zuschauer](reisen.md) gelten engere Regeln.

* Fehlt dir ein Recht, sagt dir die Anzeige über der Hotbar, welches – zum Beispiel „Hier darfst du nicht bauen.“
* Eine Kiste, einen Ofen oder einen anderen Block mit Inhalt abbauen braucht **Bauen und Behälter**.
* Einen [Furnace Golem](furnace-golem.md) bauen oder abbauen braucht **Bauen**, sein Menü öffnen **Behälter**.
* **Shop-Behälter** öffnen nur der Shop-Besitzer, der Inselbesitzer und das Team – das Recht Behälter reicht dafür nicht.
* **Fliegen** mit dem `/fly` deines Rangs geht nur, wo du das Recht **Bauen** hast.
* Als Besitzer hast du immer alle Rechte. Deine Insel **löschen** kannst nur du, in der Lobby.

## Vorlagen

Damit du nicht jedes Recht einzeln setzen musst, gibt es vier Vorlagen. Jede enthält alles aus der davor:

| Vorlage | Rechte |
| ------- | ------ |
| **Besucher** | Schalter |
| **Helfer** | dazu Ernten und Tiere |
| **Mitbauer** | dazu Bauen, Behälter und Warpetts |
| **Verwalter** | dazu Skilltree, Mitglieder und Statistik |

Stellst du ein einzelnes Recht um, zeigt das Menü **Eigen**.

* **Neue Mitglieder** kommen als **Mitbauer**. Biome kaufen und Shops eröffnen dürfen sie erst, wenn du ihnen das Recht **Skilltree** gibst.
* **Mitglieder von früher** haben weiter alle Handlungsrechte. Nur wer früher als **Besucher** eingetragen war, darf jetzt nur noch Türen und Schalter benutzen.

## Mitglieder bearbeiten

**Auf der Insel** (`/sky friends`) siehst du die Köpfe deiner Mitglieder:

* **Linksklick** öffnet die Rechte. Oben schaltest du mit **Vorlage** durch Besucher → Helfer → Mitbauer → Verwalter, darunter jedes Recht einzeln und **Betreten**.
* **Rechtsklick** entzieht dem Spieler den Zugriff.

**In der Lobby** (`/sky` → **Mitglieder**) wechselst du nur die Vorlage. Einzelne Rechte stellst du auf der Insel ein.

{% hint style="warning" %}
**Biome kauft, wer klickt.** Kauft ein Mitglied mit dem Recht Skilltree ein Biom, wird das Mana **von seinem Konto** abgebucht – nicht von deinem.
{% endhint %}

## Clan und Freunde

Ganz oben in den Mitgliedern auf der Insel stehen drei Karten: **Zuschauen** (siehe [unten](#zuschauen)), **Clan-Zugang** für deinen [Clan](clans.md) und **Freunde-Zugang** für deine [Freunde](../ag/freunde.md). Mit den beiden Zugängen kommen sie auf deine Insel, ohne dass du sie einzeln einlädst.

| Stufe | Was sie dürfen |
| ----- | -------------- |
| **Niemand** | Herein nur mit eigener Einladung |
| **Besucher** | Herein, sich umsehen und Schalter benutzen |
| **Helfer** | Dazu ernten und Tiere versorgen |
| **Mitbauer** | Dazu bauen, Behälter öffnen und Warpetts nutzen |

* **Von Anfang an** steht der Clan-Zugang auf **Besucher** und der Freunde-Zugang auf **Niemand**.
* Umstellen darf, wer das Recht **Mitglieder** hat. Den Freunde-Zugang deiner eigenen Insel stellst du auch in den Freunden unter **Einstellungen** ein.
* Ist jemand Mitglied und zugleich im Clan oder ein Freund, gilt die höhere Stufe.
* **Neulinge im Clan** (die ersten 72 Stunden) kommen höchstens als Besucher.
* Verlässt jemand deinen Clan oder stellst du den Zugang auf Niemand, verliert er seine Rechte sofort. Darf er auf deiner Insel zuschauen, bleibt er als Zuschauer, sonst wechselt er in die Lobby.

**Besuchen** geht mit `/sky visit <Name>` – auch aus der Lobby –, über das [Reisemenü](reisen.md), aus der Mitgliederliste des Clans oder aus der Freundesliste. Das Inventar reist mit.

## Zuschauen

Wer auf deiner Insel weder Mitglied ist noch über Clan oder Freunde Zugang hat, darf sie sich als **Zuschauer** ansehen – herein und umsehen, aber nichts verändern. Was Zuschauer dürfen, steht unter [Reisen & Zuschauen](reisen.md).

Wer zuschauen darf, stellst du auf der Insel unter `/sky` → **Mitglieder** → **Zuschauen** ein. Die gewählte Stufe glänzt.

| Stufe | Wer zuschauen darf |
| ----- | ------------------ |
| **Alle** | Jeder |
| **Nur Freunde** | Nur deine [Freunde](../ag/freunde.md) – auch wenn der Freunde-Zugang auf Niemand steht |
| **Nur Mitglieder** | Niemand. Herein kommt nur, wer Zugang zur Insel hat |

* **Von Anfang an** steht Zuschauen auf **Alle**. Solange deine Insel läuft, steht sie dann im [Reisemenü](reisen.md) unter **Offene Inseln**.
* Umstellen darf, wer das Recht **Mitglieder** hat.
* Stellst du strenger, wechseln Zuschauer, die nicht mehr zuschauen dürfen, sofort in die Lobby.
* Wer als Mitglied mit **Betreten**, über Clan-Zugang, Hilferuf oder Freunde-Zugang kommt, spielt wie bisher mit seinen Rechten mit. Zuschauer ist nur, wer allein über diese Stufe hereinkommt.
* Zuschauer wecken deine Insel nicht: Schläft sie, kann niemand zuschauen.
* **Clan-Inseln** sind nie zum Zuschauen offen.

## Was Mitglieder davon haben

* Mitglieder helfen bei den [Biomquests](skilltree.md#biomquests) mit und bekommen beim Abschluss **25 Mana** – genau wie du. Clanmitglieder bekommen dasselbe über den [Hilferuf](clans.md#hilferuf).
* Ihre [Quests](quests.md) zählen auch auf deiner Insel.
* Ihre Spielzeit auf deiner Insel steht in der Mitgliederliste.

## Inseln, auf denen du Mitglied bist

In der Lobby öffnest du mit `/sky` → **Geteilte Server** eine Liste aller Inseln, auf denen du Mitglied bist. Ein Klick bringt dich hin, auch wenn die Insel gerade nicht läuft.

Welche Rechte du auf einer Insel hast, siehst du dort unter `/sky` → **Insel** → **Deine Rechte**.

## Verwandte Seiten

* [Clans](clans.md)
* [Freunde](../ag/freunde.md)
* [Reisen & Zuschauen](reisen.md)
* [Deine Insel](insel.md)
* [Skilltree & Biome](skilltree.md)
