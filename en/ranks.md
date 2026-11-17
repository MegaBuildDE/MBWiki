---
description: >-
  The ranks on MegaBuild.de – Gold, Platin and Titan – and where to get them.
icon: crown
---

# Ranks

You can get a rank on MegaBuild.de and support the server at the same time.

{% hint style="info" %}
**The first rank perks are here:**

* **across the whole network** chat colours, nick, status and a bigger mailbox – see [Perks across the network](#perks-across-the-network),
* **on the Sky islands** crafting table, trash, ender chest, your own time of day, hat, poses, renaming and player heads – see [Perks on the Sky islands](#perks-on-the-sky-islands).

More perks will follow. They will be listed here as soon as they are unlocked.
{% endhint %}

## Available ranks

Currently available in the [MegaBuild.de shop](https://shop.megabuild.de/):

<table><thead><tr><th width="200">Rank</th><th width="160">Price</th><th>Shop</th></tr></thead><tbody><tr><td><strong>Gold</strong></td><td>€9.99</td><td><a href="https://shop.megabuild.de/">shop.megabuild.de</a></td></tr><tr><td><strong>Platin</strong></td><td>€19.99</td><td><a href="https://shop.megabuild.de/">shop.megabuild.de</a></td></tr><tr><td><strong>Titan</strong></td><td>€34.99</td><td><a href="https://shop.megabuild.de/">shop.megabuild.de</a></td></tr></tbody></table>

{% hint style="info" %}
**As of November 2026.** Every rank is permanent. Prices can change – the [shop](https://shop.megabuild.de/) is always authoritative.

Buying a rank directly for another player isn't possible in the shop at the moment.
{% endhint %}

## Perks across the network

Each higher rank has everything from the rank below: Platin has everything from Gold, Titan everything from Platin.

| What | no rank | Gold | Platin | Titan |
| --- | --- | --- | --- | --- |
| Your rank in front of your name in chat and the tab list | – | yes | yes | yes |
| [Colours in chat](#chat-colours) | – | `&` colour codes | plus RGB | plus RGB |
| [`/nick`](#nick) – another name in chat and the tab list | – | – | yes | yes |
| [`/status`](#status) – text behind your name in the tab list | – | – | yes | yes |
| [Mailbox](#bigger-mailbox) | 200 messages | 300 | 400 | 500 |

In the [tab list](hud.md#tab-list), players with a rank are at the top, the highest rank first.

### Chat colours

From **Gold**, you colour your chat lines with `&` codes:

* `&0` to `&f` for the 16 colours, for example `&a` green or `&6` gold,
* `&l` bold, `&o` italic, `&n` underlined, `&m` struck through,
* `&r` resets.

From **Platin**, any RGB colour works too with `&#RRGGBB`, for example `&#ff8800` for orange.

There's no `&k` (scrambled text), and lines in the clan chat stay without colours. The [chat filter](messages.md#chat-filter) checks the text without the codes too.

### Nick

From **Platin**, `/nick <name>` gives you another name. It shows in the global chat and the tab list, always with `~` in front – so everyone can see it's a nick.

* **3 to 16 characters:** letters, digits and `_`.
* **Not allowed:** another player's name, a nick someone already has, and rank or team names. The chat filter applies.
* `/nick` shows your nick, `/nick clear` removes it again.
* **With `/msg`, in your clan and in lines with `!`**, your real name always shows.
* **The team** sees your real name and can reset your nick.

### Status

From **Platin**, `/status <text>` puts a short text in grey behind your name in the [tab list](hud.md#tab-list), for example "Building".

* At most **24 characters**. The chat filter applies, and invisible special characters don't work.
* `/status` shows your status, `/status clear` removes it again.
* The team can reset your status.

### Bigger mailbox

Your mailbox keeps the newest messages: 200 without a rank, 300 with Gold, 400 with Platin and 500 with Titan. Anything beyond that which you have already read gets tidied away – how, is explained under [Messages & Mail](messages.md#the-mailbox).

## Perks on the Sky islands

Here too, each higher rank has everything from the rank below.

| What | no rank | Gold | Platin | Titan |
| --- | --- | --- | --- | --- |
| `/craft` – crafting table anywhere | – | yes | yes | yes |
| `/stonecutter`, `/loom`, `/cartography` | – | – | yes | yes |
| `/trash` – trash can | – | yes | yes | yes |
| `/ec` – open your ender chest anywhere | – | yes | yes | yes |
| Size of the [ender chest](#ender-chest) | 3 rows | 4 rows | 5 rows | 6 rows |
| `/ptime` – your own time of day | – | – | morning, noon, evening, night | any time, freeze |
| [`/hat`](#hat) – an item as a hat | – | yes | yes | yes |
| [`/sit`, `/lay`, `/crawl`](#sit-lie-down-crawl) | – | yes | yes | yes |
| [`/rename`](#renaming-items) – rename an item | – | text only | with colours | with RGB and gradients |
| [`/head`](#player-heads) – a player head | – | 1 a month | 1 a week | 1 a day |

### Where the commands work

* **On all Sky islands** – on your own and as a visitor on other islands too.
* **Not in combat:** For 10 seconds after a mob or player hit you – with a projectile too – or after you hit a living creature yourself, they don't work. The chat tells you how many seconds are left. Fall damage, fire and drowning don't count.
* **Not as a customer** on someone else's market – there you only have the [customer commands](chestshop.md#as-a-customer-on-other-islands).

Without the rank, the command tells you: "That is part of a rank you don't have." Taking off your hat and getting up from a pose always works.

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

### Hat

From **Gold**, `/hat` puts the item in your hand on your head as a hat.

* **It's only for show:** the item stays in your inventory and doesn't protect you like a helmet. If you wear a helmet, the hat sits on top of it.
* **`/hat off`** takes it off – that always works.
* **You don't see your own hat,** not even in the view from behind (F5). While swimming, crawling, gliding, sleeping and lying down it's gone, and also while you're invisible.
* **Each island remembers your hat** on its own and puts it back on when you return.
* **On Bedrock** hats can't be seen. Java players do see a Bedrock player's hat, though.

### Sit, lie down, crawl

From **Gold**:

| Command | What it does |
| --- | --- |
| `/sit` | You sit down |
| `/lay` | You lie flat on the ground |
| `/crawl` | You crawl and can move while doing so |

* You need **solid ground** for this – not in water and not in the air.
* **To get up,** sneak or type the command again. Lying down also ends when you take damage.
* **On Bedrock** only `/sit` works – lying down and crawling aren't available there yet.

### Renaming items

From **Gold**, `/rename [name]` gives the item in your hand a new name – without an anvil.

| Rank | What the name can contain |
| --- | --- |
| Gold | Text only |
| Platin | Colours as in chat: `&0` to `&f`, plus `&l` bold, `&o` italic, `&n` underlined, `&m` struck through |
| Titan | Plus RGB with `&#ff8800`, gradients with `<gradient:#ff0000:#0000ff>Name` and `<rainbow>Name` |

* **At most 50 visible characters** – colour codes don't count. Only the name changes, not the description.
* **Not allowed:** names of ranks, of the team and of the server's items – such as Ruby, Mana, Mana Apple, Plate or Warpett. The chat filter applies.
* **`/rename clear`** removes the name again.
* Player heads from `/head` can't be renamed.

### Player heads

From **Gold**, `/head <player>` gets you a player's head, with their skin. How often depends on your rank:

| Rank | Heads | The next one comes |
| --- | --- | --- |
| Gold | 1 a month | on the first of the next month |
| Platin | 1 a week | from Monday |
| Titan | 1 a day | the next day |

It counts across the whole network, not per island. If your inventory is full, the head lands at your feet.

**The head is bound to you:**

* **No trading** – neither in a [ChestShop](chestshop.md) nor with [residents](residents.md).
* **Only you can pick it up** – no other player, no mob, no hopper. Only you can take it off an armor stand, too.
* **Placed as a block,** it stays bound. If you mine it, it drops as your head again. Explosions leave it standing.

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
* [Messages & Mail](messages.md)
* [Travel & Watching](travel.md)
* [Voting](vote.md)
* [Support & Contact](support.md)
* [Mana & Ruby](economy.md)
* [FAQ](faq.md)
