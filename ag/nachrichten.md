---
description: >-
  Der Globalchat, private Nachrichten, das Postfach und der Chatfilter auf
  MegaBuild.de.
icon: envelope
---

# Nachrichten & Post

## Globalchat

```
<Text>
/g <Text>
!<Text>
```

Schreibst du einfach in den Chat, geht deine Zeile an **alle Spieler im Netzwerk**, egal auf welchem Server sie gerade sind – ebenso mit `/g <Text>`. Vor der Zeile steht `[Global]`, dein [Rang](rang.md), dein [Clan-Kürzel](../sb/clans.md) und dein Name; ein Klick auf den Namen schlägt dir `/msg` vor.

| So schreibst du | Wer liest mit |
| --------------- | ------------- |
| Normal in den Chat | Alle im Netzwerk |
| `/g <Text>` | Alle im Netzwerk – auch dort, wo der normale Chat nicht hinausgeht |
| **`!`** vorn, etwa `!Hallo zusammen` | Nur die Spieler auf **deinem** Server, das `!` fällt weg |
| **`#`** vorn oder `/c` | Dein [Clan](../sb/clans.md) |

* Nach dem `!` muss ein Buchstabe oder eine Ziffer kommen – ein einzelnes „!“ oder „!!!“ ist eine normale Zeile.
* Höchstens **eine Zeile je Sekunde** und **256 Zeichen** je Zeile. Warst du zu schnell, kommt die Zeile nicht an – der Chat zeigt sie dir mit ihrem Text zurück, damit du sie noch einmal schicken kannst.
* Chatfilter und Stummschaltung gelten wie im normalen Chat (siehe unten).
* **Im Vorspann** auf dem Intro-Server bleibt deine Zeile dort, und vom Globalchat kommt nichts an – sonst liefe der Chat des ganzen Netzwerks durch Malas Erzählung. Mit `/g` erreichst du trotzdem alle.

{% hint style="info" %}
**Bei den Bewohnern und Forestlingen** geht deine Zeile nur an sie – im Gespräch mit [KI-Bewohnern](../sb/bewohner.md), im Inselchat und bei den [Forestlingen](../sb/forestlinge.md). Mit **`!`** vorn schreibst du dort an alle auf dem Server, mit `/g` ins ganze Netzwerk.
{% endhint %}

## Private Nachrichten

```
/msg <Spieler> <Text>
/r <Text>
```

Mit `/msg` schreibst du einem Spieler privat, mit `/r` antwortest du auf die letzte private Nachricht. Beim Ausloggen vergisst `/r`, mit wem du zuletzt geschrieben hast.

{% hint style="info" %}
**Ist der Spieler nicht online, geht nichts verloren:** Die Nachricht landet automatisch in seinem Postfach und du bekommst eine Bestätigung.
{% endhint %}

## Das Postfach

Öffne es mit `/mail`. Auch `/post` funktioniert. Das Postfach gilt im ganzen Netzwerk. Nachrichten bleiben dort, bis du sie löschst – räum ab und zu auf.

Ungelesene Nachrichten erkennst du am fett geschriebenen Namen. Wenn du eine Nachricht öffnest, kannst du:

* **Antworten**
* den **Absender blockieren**
* die Nachricht **löschen**

Beim Einloggen siehst du, ob neue Post auf dich wartet. Auch Nachrichten vom Server landen hier – etwa die Belohnung für einen [Vote](vote.md), während du offline warst, oder ein Danke für eine [Bug-Meldung](discord.md#bug-bounty-und-clipcoin).

### Nachricht schreiben

{% stepper %}
{% step %}
#### Empfänger wählen

Klicke in `/mail` auf **Neue Nachricht** und wähle einen Freund aus oder suche nach einem Namen.
{% endstep %}

{% step %}
#### Im Buch schreiben

Du bekommst ein Buch mit Feder. Schreib deine Nachricht hinein. Absätze sind erlaubt, höchstens **256 Zeichen**.

Dafür brauchst du einen **freien Platz in deiner Schnellleiste**.
{% endstep %}

{% step %}
#### Signieren = Abschicken

Signiere das Buch, um die Nachricht zu senden. Wirfst du das Buch weg, wird nichts gesendet.
{% endstep %}
{% endstepper %}

Schneller geht es mit einem einzigen Befehl:

```
/mail <Spieler> <Text>
```

Wurde deine Nachricht nicht gesendet, etwa wegen des Chatfilters, bekommst du den Text im Buch zurück und kannst ihn anpassen.

### Blockieren

Blockierst du einen Absender, bekommst du von ihm keine Post mehr. Er selbst merkt davon nichts. Die Blockierung hebst du in `/mail` unter **Blockierte Spieler** wieder auf.

## Chatfilter

Der Chat, private Nachrichten und die Post werden automatisch geprüft. Folgendes führt zu einem **Kick**:

| Verstoß | Beispiel |
| ------- | -------- |
| Unangemessene Wörter | Beleidigungen, Beschimpfungen |
| Werbung | IP-Adressen und Domains anderer Server |
| Betteln | Fragen nach OP, Rang, Admin oder Gamemode |

Umschreibungen wie Zahlen statt Buchstaben oder langgezogene Wörter werden ebenfalls erkannt.

{% hint style="warning" %}
Bist du **stummgeschaltet**, kannst du weder im Chat schreiben noch private Nachrichten oder Post verschicken. Den Grund und die verbleibende Zeit siehst du beim Versuch zu schreiben.
{% endhint %}

## Verwandte Seiten

* [Freunde](freunde.md)
* [Befehle](befehle.md)
* [Support & Kontakt](support.md)
