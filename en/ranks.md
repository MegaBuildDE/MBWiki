---
description: >-
  The ranks on MegaBuild.de – Gold, Platin and Titan – and where to get them.
icon: crown
---

# Ranks

You can get a rank on MegaBuild.de and support the server at the same time.

{% hint style="info" %}
**Since 17 November 2026 the first rank perks are live on the Sky islands:** crafting table, trash, ender chest and your own time of day – see [Perks on the Sky islands](#perks-on-the-sky-islands).

More perks will follow. They will be listed here as soon as they are unlocked.
{% endhint %}

## Available ranks

Currently available in the [MegaBuild.de shop](https://shop.megabuild.de/):

<table><thead><tr><th width="200">Rank</th><th width="160">Price</th><th>Shop</th></tr></thead><tbody><tr><td><strong>Gold</strong></td><td>€9.99</td><td><a href="https://shop.megabuild.de/">shop.megabuild.de</a></td></tr><tr><td><strong>Platin</strong></td><td>€19.99</td><td><a href="https://shop.megabuild.de/">shop.megabuild.de</a></td></tr><tr><td><strong>Titan</strong></td><td>€49.99 – currently on sale for €34.99</td><td><a href="https://shop.megabuild.de/">shop.megabuild.de</a></td></tr></tbody></table>

{% hint style="info" %}
**As of October 2026.** Prices and promotions can change – the [shop](https://shop.megabuild.de/) is always authoritative.

Buying a rank directly for another player isn't possible in the shop at the moment.
{% endhint %}

## Perks on the Sky islands

Each higher rank has everything from the rank below: Platin has everything from Gold, Titan everything from Platin.

| What | no rank | Gold | Platin | Titan |
| --- | --- | --- | --- | --- |
| `/craft` – crafting table anywhere | – | yes | yes | yes |
| `/stonecutter`, `/loom`, `/cartography` | – | – | yes | yes |
| `/trash` – trash can | – | yes | yes | yes |
| `/ec` – open your ender chest anywhere | – | yes | yes | yes |
| Size of the [ender chest](#ender-chest) | 3 rows | 4 rows | 5 rows | 6 rows |
| `/ptime` – your own time of day | – | – | morning, noon, evening, night | any time, freeze |

### Where the commands work

* **On all Sky islands** – on your own and as a visitor on other islands too.
* **Not in combat:** For 10 seconds after a mob or player hit you – with a projectile too – or after you hit a living creature yourself, they don't work. The chat tells you how many seconds are left. Fall damage, fire and drowning don't count.
* **Not as a customer** on someone else's market – there you only have the [customer commands](chestshop.md#as-a-customer-on-other-islands).

Without the rank, the command tells you: "That is part of a rank you don't have."

### Crafting table and stations

From **Gold**, `/craft` opens a crafting table – without a block nearby. `/workbench` and `/wb` work too.

From **Platin**, `/stonecutter`, `/loom` and `/cartography` open a stonecutter, a loom and a cartography table.

They are the normal Minecraft windows, on Bedrock too. Whatever is still in the slots when you close the window goes back into your inventory.

### Trash

From **Gold**, `/trash` opens the **trash** with 4 rows: three rows at the top for what you want gone, the buttons at the bottom. This is how you throw something away:

1. Put in what you want gone.
2. Click **Throw away**.
3. Click **Confirm throwing away**. If you change the content before that, it starts over.

For special items the trash asks a third time: **Really throw away?** That applies to server items like the Mana Apple, plates or crystals, and to shulker boxes or bundles with something inside – their content is gone too.

* **If you close the trash before that,** you get everything back – also when you log out or change islands. Whatever doesn't fit into your inventory lands at your feet.
* **`/trash undo`** gets back what you threw away last, for 5 minutes – or the **Get back** button in the trash. This only works on the island where you threw it away. If not everything fits into your inventory, make room and type `/trash undo` again.

### Ender chest

**Everyone** has their own ender chest – without a rank too:

* **It's the same on all Sky islands** and travels with you like your inventory.
* **Every ender chest block opens it**, on your island and on others. From **Gold** you open it from anywhere with `/ec`, also `/enderchest`.
* **Size:** 3 rows without a rank, 4 with Gold, 5 with Platin, 6 with Titan.
* **Anything that travels with your inventory may go in,** shulker boxes too. If the chest would become too big for the trip between islands, it takes nothing more.
* **If something lies in rows above your rank,** you still see those rows and can only take things out there. Empty slots there show a lock.

**Your old ender chest:** Until now every island had its own ender chest. The first time you open your ender chest on an island, that island's old content moves in – into the same slot, otherwise the first free one. What isn't allowed in the ender chest goes into your inventory. If there's no room for it there or in the ender chest, the rest stays in the old chest: make room and open the ender chest again.

### Your own time of day

From **Platin**, `/ptime` sets your own time of day. Only you see it – mobs, plants and sleeping still follow the island.

| Command | Rank | What it does |
| --- | --- | --- |
| `/ptime morning` | Platin | 6:00 |
| `/ptime noon` | Platin | 12:00 |
| `/ptime evening` | Platin | 18:00 |
| `/ptime night` | Platin | 0:00 |
| `/ptime <time>` | Titan | Any time, for example `/ptime 21:30` or in ticks `/ptime 15500` (0 to 23999) |
| `/ptime freeze` | Titan | Stops your time. Once more, and it runs again |
| `/ptime reset` | Platin | Back to the island's time |
| `/ptime` | Platin | Shows which time you see right now |

* Your time **keeps running normally**, just shifted – unless you freeze it.
* It lasts **until you log out** or type `/ptime reset`. If you travel to another island, it comes along if you were gone for 2 minutes at most.

## Other shop offers

{% columns %}
{% column %}
### 🎁 Gift cards

Gift cards start at €5.99 – handy if you want to give someone a present.
{% endcolumn %}

{% column %}
### 🐾 Pets

Pets are planned. They have nothing to do with the [Warpetts](warpetts.md).
{% endcolumn %}
{% endcolumns %}

{% embed url="https://shop.megabuild.de/" %}

## Common questions

<details>

<summary>Do I keep my old rank after the relaunch?</summary>

How ranks from before the relaunch will be handled has not been announced publicly yet. It's best to ask directly on [Discord](https://megabuild.de/dc/) or via a [ticket](https://megabuild.de/ticket/).

</details>

<details>

<summary>Does my rank apply to my Bedrock account too?</summary>

If you have linked your Java and Bedrock accounts, both share the same save.

{% content-ref url="connect-account.md" %}
[connect-account.md](connect-account.md)
{% endcontent-ref %}

</details>

<details>

<summary>My order hasn't arrived</summary>

Contact [ticket support](https://megabuild.de/ticket/) or email [support@megabuild.de](mailto:support@megabuild.de). Have your order or transaction number ready.

</details>

<details>

<summary>Can I buy ranks in-game?</summary>

No. Ranks are only available in the [shop](https://shop.megabuild.de/) – not for Mana or Ruby.

</details>

## Related pages

* [Commands](commands.md#rank-commands)
* [Travel & Watching](travel.md)
* [Voting](vote.md)
* [Support & Contact](support.md)
* [Mana & Ruby](economy.md)
* [FAQ](faq.md)
