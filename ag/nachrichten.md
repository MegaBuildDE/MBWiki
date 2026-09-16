---
description: Private Nachrichten, das Postfach und der Chatfilter auf MegaBuild.de.
icon: envelope
---

# Nachrichten & Post

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

Öffne es mit `/mail`. Das Postfach gilt im ganzen Netzwerk und fasst bis zu **200 Nachrichten**. Nachrichten bleiben dort, bis du sie löschst.

Ungelesene Nachrichten erkennst du am fett geschriebenen Namen. Wenn du eine Nachricht öffnest, kannst du:

* **Antworten**
* den **Absender blockieren**
* die Nachricht **löschen**

Beim Einloggen siehst du, ob neue Post auf dich wartet.

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
