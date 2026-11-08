---
description: >-
  ChestShops on MegaBuild.de – trade for Ruby with a sign and a chest, search
  offers across the network, travel there and open a market of your own.
icon: store
---

# ChestShops

A **ChestShop** lets you trade with other players: a sign on a chest names the item, amount and price, and one click on the sign buys or sells. Payment is **Ruby only** – see [Mana & Ruby](economy.md#ruby). If you open an area of your island as a **market**, players from all over the network find it in the shop search and travel straight to you.

{% hint style="info" %}
Shops only exist on islands, not in the lobby. Every shop belongs to a player – there are no admin shops.
{% endhint %}

## Buying and selling

| You want to | Java | Bedrock |
| ----------- | ---- | ------- |
| **Buy** | Right-click the sign | Tap the sign |
| **Sell** | Left-click the sign | Hold the sign |
| **Open the trade menu** | Sneak + right-click | Sneak and tap |

The **trade menu** shows the item and stock and has one button each for buying and selling. It's mainly meant for touchscreens and only works while you're within 8 blocks of the sign.

### Reading a sign

| Line | Example | Meaning |
| ---- | ------- | ------- |
| 1 | `Tom` | Who owns the shop |
| 2 | `16` | Amount per trade |
| 3 | `B 16 : 10 S` | Prices in Ruby for the whole amount: **B** you buy here, **S** you sell here |
| 4 | `Eichenstamm` | The item |

If the sign only has `B` or only `S`, that's all you can do there. A `*` after the item means it differs from the plain item – enchanted, renamed or worn, for example.

Signs show item names in the server's default language, German. The search also understands English names.

### When a trade goes through

A trade is always for the full amount on the sign.

* **When buying**, the shop needs enough stock, and you need enough Ruby and room in your inventory.
* **When selling**, you need exactly this item in your inventory or off-hand, the shop needs room and its owner enough Ruby. Armour you're wearing doesn't count.
* You can't trade at your own shop.
* If a trade doesn't go through, the chat tells you why, and nothing is booked. Only if it reports an “unclear” booking should you check your balance with `/bal`.
* There's no fee. The Ruby go straight from one account to the other.

{% hint style="info" %}
**New accounts** can only spend Ruby **24 hours after their first login** and after **20 minutes of playtime**. Until then you can sell but not buy. The chat tells you how long is left. A shop owner with a new account can't buy from customers yet either.
{% endhint %}

## Finding shops

`/shop` opens the shop menu. You also find it in your island's `/sky` menu under **Shops**.

| Button | What it does |
| ------ | ------------ |
| **Search** | Type an item name in chat, at least 2 characters. English and German both work, and so do parts of words: “iron” finds iron ingots, iron ore … |
| **Search the item in your hand** | Shows who trades the item in your main hand |
| **All offers** | Every open offer in the network |
| **Markets** | The open shop areas of all islands. One click travels there |
| **My shops** | Your own shops on all islands, with stock and space |
| **Shop areas** | This island's areas, if you may manage them |
| **Back to your own island** | Only while you're out as a customer |

The offer lists only show shops you can trade at right now. You can filter by **Buy** and **Sell** and sort by **Cheap** or **New** – when selling, whoever pays the most comes first.

Custom items are listed under their German names, even on an English client, and the search only finds them under those names.

## Travelling there

One click on an offer opens **Travel there?** – one more click on **Travel there** and you're on your way. You land right in front of the sign or at the market's arrival point.

* **Your whole inventory travels with you.** Ender chest and levels stay on each island.
* **Cooldown:** 20 seconds between two trips.
* **You can't set off** if you took damage in the last 5 seconds, or while falling or gliding.
* **Sleeping islands** aren't woken up. You'll read “This island is asleep right now” and try again later.
* **If a trip is cancelled,** you stay where you are and nothing is missing.

**To get back**, use `/shop home` – no cooldown. If your island is asleep or you don't have one, you go to the lobby.

## As a customer on other islands

If you have no access to the island, you arrive as a **customer**. With access – as a member, through your clan or friends – you're not a customer and have your usual [rights](members.md#the-rights) there.

| As a customer you may | As a customer you may not |
| --------------------- | ------------------------- |
| Buy and sell at shop signs | Break or place blocks, edit signs, harvest |
| Eat and drink – except the ominous bottle | Open containers, including shop chests and the ender chest |
| Chat | Use animals, residents, Warpetts, frames or vehicles |
| `/shop`, `/bal`, `/msg`, `/r`, `/friend`, `/mail` and `/lobby` | Attack, throw projectiles, fish |
| Pick up your own items | Drop items or pick up other people's items |
| | Fly, glide, use portals, leave the market by ender pearl or chorus fruit |

* **You stay in the market.** At the edge of the area you're sent back (“The market ends here”). If you fall out at the bottom, you land at the arrival point again.
* **You're safe.** You take no damage, and mobs don't attack you. If you do die, you keep your inventory and levels.
* **There's no Mana here,** and residents don't talk to you.
* **If the market closes,** you travel home automatically.
* An island takes at most **10 customers** at once. The last 4 player slots are kept for the owner and members.

## Opening a shop

The **island owner** and members with the **Skill tree** right can do this – the **Manager** template includes it. See [Members & rights](members.md#the-rights).

{% stepper %}
{% step %}
#### Create a shop area

Shops only stand in a [shop area](#shop-areas). Sign and container must be in the same area, open or closed.
{% endstep %}

{% step %}
#### Place a container

A **chest**, **trapped chest**, **barrel** or **copper chest**, waxed ones too. Put the item in it. A double chest counts with both halves.
{% endstep %}

{% step %}
#### Attach a sign

A **wall or standing sign** on the container, on top of it or below it. Hanging signs don't work.
{% endstep %}

{% step %}
#### Write on the sign

**Line 1** doesn't matter, the server puts your name there. **Line 2** is the amount, **line 3** the price, **line 4** the item. The chat confirms “Shop opened”.
{% endstep %}
{% endstepper %}

The sign is waxed afterwards. To change anything, break it and put up a new one.

### Line 3: the price

| You write | It means |
| --------- | -------- |
| `B 10` | Customers buy for 10 Ruby |
| `S 5` | Customers sell for 5 Ruby – you're buying |
| `B 10 : 5 S` | Both |
| `B free` or `B 0` | You give the item away |

Upper and lower case and spaces don't matter, and the letter may come before or after the number. **Two prices are always separated by a colon** – `B 10 S 5` stays an ordinary sign.

### Line 4: the item

* **Empty or `?`:** The first item in the container, exactly as it is there – with name, enchantments and durability. This is how you sell special items.
* **A name:** `Diamant`, `diamond` or `minecraft:diamond`. This trades the plain item without enchantments.

If several items share a name, such as “nether bricks” or “music disc”, the chat gives you the exact names.

### Examples

| Line 2 | Line 3 | Line 4 | It means |
| ------ | ------ | ------ | -------- |
| `16` | `b16` | `oak log` | Customers buy 16 oak logs for 16 Ruby |
| `1` | `S 40 : B 60` | empty, enchanted sword in the chest | Customers buy the sword for 60 Ruby and sell one exactly like it for 40 |
| `64` | `5 s` | `?`, cobblestone in the chest | You buy 64 cobblestone for 5 Ruby |

### Limits

* **Amount:** 1 to 2,304 per trade. It must fit into the empty container and into an inventory once.
* **Price:** 0 to 1,000,000 Ruby.
* **Number:** 50 shops per player across the network, 200 per island.
* **Blocked items:** [Mana orbs](economy.md#mana-orbs), Mana Charges, [Mana Blocks and Mana Shards](furnace-golem.md#trading), bedrock, command blocks, spawners and other technical blocks – also inside a shulker box or bundle. Mana Apples and plates are fine, see [Mobplates](mobplates.md#rules).
* **No shop is possible:** on a container where another player already has a shop, in a residents' settlement, close to the world spawn and on a clan's project chest. Open loot chests once first.

## Running your shop

| You want to | How |
| ----------- | --- |
| See stock and space | Right-click your sign, or `/shop mine` |
| Close the shop | Left-click your sign |
| Restock or collect items | Open the container |

* **Opening the container** is only for the shop owner, the island owner and the team – not for other members.
* **The island owner** can remove someone else's shop on their island with sneak + left-click.
* **Breaking the container** closes all shops on it, and their signs turn back into ordinary signs. This only works if all the shops on it are yours or the island is yours.
* **Earnings:** If you're on the same island, you see every trade in chat right away. Otherwise a line appears the next time you enter an island: “Since your last visit: 12 sales, +192 Ruby.”
* **Buying from customers** is paid from your own account. If you're short of Ruby, the sale doesn't go through and the customer keeps the items.

Shop blocks are protected: explosions, fire, pistons and mobs can't harm them, and a sign stays up even if whatever holds it disappears. **Hoppers** may fill and empty your container. Only someone who may open a shop container can put a hopper under it or attach a chest to it.

## Shop areas

A shop area is a box on your island: shops only stand inside it, and customers only move inside it. Creating one is **free**. The island owner and members with the **Skill tree** right can manage it.

{% stepper %}
{% step %}
#### Create the area

`/shop areas` → **New area**, then type the name in chat, 24 characters at most. The area starts as 3 × 3 around you and is **closed** at first.
{% endstep %}

{% step %}
#### Set the corners

Stand on two opposite corners and click **Corner 1 here** and **Corner 2 here**. The height grows by itself: 4 blocks below the lower corner, 24 above the higher one.
{% endstep %}

{% step %}
#### Set the arrival point

Stand on solid, harmless ground inside the area and click **Arrival point here**. This is where customers arrive. The direction you're facing is kept – so look at your market.
{% endstep %}

{% step %}
#### Open it

Click the **Closed** switch in the menu so it reads **Open**. This needs an arrival point first. Your market now appears in the shop search.
{% endstep %}
{% endstepper %}

**Show borders** makes the edges light up for 10 seconds, only for you: green for open, orange for closed, plus a light blue column at the arrival point.

### Open and closed

| | Open | Closed |
| --- | --- | --- |
| **In the shop search and markets** | Yes | No |
| **Customers travel there** | Yes | No |
| **Who may trade** | Everyone | Island owner, members, team and anyone who has a shop on the island |

A friend who's only visiting can't trade in a closed area. **If you close a market,** all customers in it travel home right away.

### Rules for areas

* **Size:** 3 to 48 blocks wide and long.
* **Number:** at most 3 areas per island. They may not overlap.
* **Place:** only in the island world and without any blocks of your airship.
* **Shrinking:** An area with shops may grow, but only shrink as far as all shop signs and containers stay inside.
* **Deleting** only works once no shops are left in it.

## Commands

| Command | What it does |
| ------- | ------------ |
| `/shop` | Shop menu. Also `/shops`, `/sky shop` |
| `/shop search [term]` | Search offers on all islands. Also `/shop find` |
| `/shop hand` | Who trades the item in your main hand? |
| `/shop list` | All offers |
| `/shop markets` | Open markets of all islands |
| `/shop mine` | Your shops with stock and space. Also `/shop my` |
| `/shop areas` | This island's shop areas |
| `/shop home` | Back to your own island |
| `/shop help` | Help in chat |

## Related pages

* [Mana & Ruby](economy.md)
* [Members & rights](members.md)
* [Your island](island.md)
* [Mobplates](mobplates.md)
* [Commands](commands.md)
