---
description: >-
  Was die Anzeigen auf deinem Bildschirm bedeuten – auf Java und Bedrock – und
  wo du deine Statistiken findest.
icon: gauge
---

# HUD & Statistiken

Jeder Kasten im HUD zeigt nur **Symbol und Zahl**. Das Symbol sagt, was gezählt wird – eine Spitzhacke für eine Abbau-Quest, ein Schwert für Kämpfe.

## Oben: drei Kästen

| Kasten | Symbol | Beispiel | Was er zeigt |
| ------ | ------ | -------- | ------------ |
| **1** | Weltkugel | `12/40` | Biome, die deiner Insel gehören. Alle Mitspieler sehen den Stand der Insel. 40 sind es, solange der Kristall Gewässer gesperrt ist |
| **2** | Symbol des Quest-Themas | `7/12` | Die Quest, die du gerade verfolgst |
| **3** | wechselt alle 5 Sekunden | | Erledigte Quests · deine Spielzeit **auf dieser Insel** · besiegte Tiere und Monster · Spieler auf dieser Insel |

**Welche Quest in Kasten 2 steht:**

1. die Quest, die du im Questmenü **angeheftet** hast,
2. sonst die Quest, bei der du in den letzten 10 Minuten vorangekommen bist,
3. sonst die erste offene Quest.

Das gilt auch für die [Biomquest](skilltree.md#biomquests) deiner Insel – dann siehst du den Stand der ganzen Insel. Nach einem Abschluss steht kurz ein Haken da. Hast du keine offene Quest, zählt der Kasten die Blöcke, die du seit dem Betreten des Servers abgebaut hast.

{% hint style="info" %}
**Sonderquest:** Solange du deinen ersten Bewohner suchst, zeigt Kasten 2 einen **Pfeil**, der sich mit deinem Blick dreht, und die Entfernung in Metern.
{% endhint %}

## Unten rechts: Mana & Ruby

Direkt über deiner Hungerleiste steht dein **Mana** (rosa Kugel), darüber dein **Ruby** (roter Edelstein).

{% content-ref url="eco.md" %}
[eco.md](eco.md)
{% endcontent-ref %}

## In der Lobby

In der Lobby zeigen die Kästen die **Uhrzeit**, den **Server**, auf dem du bist, und wie viele **Spieler** im Netzwerk online sind.

## Auf Bedrock

Bedrock zeigt dieselben Zahlen, mit ein paar Unterschieden:

* **Keine Balken** hinter den Zahlen – die Zahl sagt dasselbe.
* Im Quest-Kasten steht **immer die Schriftrolle** statt des Themen-Symbols, auch nach einem Abschluss.
* Bei sehr großen Zielen, etwa langen Laufquests, steht statt `4321/9000` der Anteil in Prozent: `48%`.
* Die Tablist zeigt den Abschnitt **Bewohner (KI)** nicht – nutze dort `/bewohner`.

## Statistiken

{% tabs %}
{% tab title="In der Lobby" %}
`/sky` → **Statistiken** hat drei Seiten:

| Seite | Inhalt |
| ----- | ------ |
| **Persönliches Dashboard** | Aktivität, Abbau & Bau, Fortschritt, Farmen, Kampf, Generierung und deine Spielzeit auf deinen Inseln |
| **Toplisten** | Die besten Spieler bei Abbau, Bau, Ernte, Pflanzen und besiegten Monstern |
| **Welt & Netzwerk** | Die häufigsten Biome und Inseltypen im ganzen Netzwerk |
{% endtab %}

{% tab title="Auf der Insel" %}
| Befehl | Inhalt |
| ------ | ------ |
| `/sky` → **Statistiken** | Abbau, Bau, Ernte, Kampf, Quests, Skilltree, Spielzeit, Biome und Inseln |
| `/sky stats` | Deine Werte im Chat |
| `/sky global` | Die Werte des ganzen Servers im Chat |

Auf fremden Inseln brauchst du dafür das Recht **Statistiken**. Die Spielzeit deiner Mitspieler auf deiner Insel steht in der Mitgliederliste.
{% endtab %}
{% endtabs %}

## Spielzeit

```
/ot [Spieler]
```

Zeigt deine gesamte Spielzeit im Netzwerk und deinen ersten Join – oder die eines anderen Spielers. Auch `/onlinetime` und `/pt` funktionieren.

## Sprache

Menüs, Chat und Malas Stimme richten sich nach der **Sprache deines Minecraft-Clients**: Deutsch bei deutschem Client, sonst Englisch.

## Verwandte Seiten

* [Quests](quests.md)
* [Skilltree & Biome](skilltree.md)
* [Erfolge](erfolge.md)
