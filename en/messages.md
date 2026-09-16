---
description: Private messages, the mailbox and the chat filter on MegaBuild.de.
icon: envelope
---

# Messages & Mail

## Private messages

```
/msg <player> <text>
/r <text>
```

Use `/msg` to write to a player privately and `/r` to reply to the last private message. When you log out, `/r` forgets who you last wrote with.

{% hint style="info" %}
**If the player isn't online, nothing gets lost:** the message automatically goes to their mailbox and you get a confirmation.
{% endhint %}

## The mailbox

Open it with `/mail`. The mailbox works across the whole network and holds up to **200 messages**. Messages stay there until you delete them.

Unread messages are shown with the name in bold. When you open a message, you can:

* **Antworten** (Reply)
* **Absender blockieren** (Block sender)
* **Löschen** (Delete) the message

When you log in, you'll see whether new mail is waiting for you.

### Writing a message

{% stepper %}
{% step %}
#### Choose a recipient

In `/mail`, click **Neue Nachricht** (New message) and pick a friend or search for a name.
{% endstep %}

{% step %}
#### Write in the book

You get a book and quill. Write your message in it. Paragraphs are allowed, up to **256 characters**.

You need a **free slot in your hotbar** for this.
{% endstep %}

{% step %}
#### Signing = sending

Sign the book to send the message. If you throw the book away, nothing is sent.
{% endstep %}
{% endstepper %}

It's faster with a single command:

```
/mail <player> <text>
```

If your message wasn't sent, for example because of the chat filter, you get the text back in the book and can adjust it.

### Blocking

If you block a sender, you won't get any more mail from them. They won't notice. You can lift the block again in `/mail` under **Blockierte Spieler** (Blocked players).

## Chat filter

Chat, private messages and mail are checked automatically. The following leads to a **kick**:

| Violation | Example |
| --------- | ------- |
| Inappropriate words | Insults, abuse |
| Advertising | IP addresses and domains of other servers |
| Begging | Asking for OP, a rank, admin or gamemode |

Workarounds such as numbers instead of letters or stretched-out words are detected as well.

{% hint style="warning" %}
If you're **muted**, you can't write in chat or send private messages or mail. You'll see the reason and the remaining time when you try to write.
{% endhint %}

## Related pages

* [Friends](friends.md)
* [Commands](commands.md)
* [Support & Contact](support.md)
