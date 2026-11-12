---
description: >-
  The two currencies on MegaBuild.de – how to earn Mana and Ruby, what you need
  them for and what happens when you die.
icon: coins
---

# Mana & Ruby

MegaBuild.de has two currencies. Both work on all servers and are shown at the bottom right above your hunger bar – **Ruby** (red gem) above **Mana** (pink orb).

| | Mana | Ruby |
| --- | --- | --- |
| **Used for** | Biomes in the skill tree, skipping quests, Forestling blessings | Trading between players and with AI residents |
| **Starting balance** | 1,000 | 500 |
| **Sending** | Not from your account – you can pass on [Mana orbs](#mana-orbs) | With `/pay` |

{% content-ref url="skilltree.md" %}
[skilltree.md](skilltree.md)
{% endcontent-ref %}

## Earning Mana

| Source | Mana | Limit |
| ------ | ---: | ----- |
| [Daily quests](quests.md) | 15–90 | three quests at a time |
| Weekly quest | 250–400 | one per week |
| Bonus quest | 120–180 | one per week |
| [Biome quest](skilltree.md#biome-quests) | 25 per helper | owner and members of the island |
| [Voting](vote.md) | 50 + 5 Ruby | none – every vote counts |
| Actions (see below) | mostly 1–8 | **150 a day** |
| [Mana ore](#mana-ore) | 3–5 Mana orbs | **200 a day** |
| [Mana Shards](furnace-golem.md#turning-shards-into-mana) at the Furnace Golem | 1 per shard | **20 shards a day** |

### From actions

Many activities have a chance to give Mana:

| Action | Chance | Mana |
| ------ | -----: | ---: |
| Mining ore | 8 % | 1–2 |
| Diamond, emerald or gold ore | 35 % | 2–4 |
| Defeating monsters | 15 % | 1–2 |
| Fishing | 10 % | 1–3 |
| Trading with villagers | 12 % | 1–2 |
| Taming an animal | 60 % | 4–8 |
| Breeding animals | 10 % | 1–2 |
| Shearing sheep | 12 % | 1 |
| Harvesting | 4 % | 1 |
| Enchanting | 35 % | 2–5 |
| Every 5 levels gained | 50 % | 1–3 |
| Defending against a raid | 100 % | 20–40 |
| Earning an advancement or [achievement](achievements.md) | 100 % | 3–8 |
| Wearing out a tool (200+ durability) | 25 % | 2–4 |
| Taking items out of a furnace | 5 % | 1 |

{% hint style="info" %}
**Daily limit: 150 Mana from actions.** Quests, biome quests and votes don't count towards it. The limit resets every day at **04:00**.
{% endhint %}

Advancements and achievements only give Mana the first time – no matter which island you're on.

### What doesn't give Mana

* Anything outside **Survival mode**, and anything during the intro
* Blocks you **placed yourself** – such as ores, logs, melons or pumpkins
* Ore you mine **without a pickaxe**
* Monsters from **spawners** – including [spawners from Mobplates](feather.md#mobs-from-the-spawner) –, spawn eggs, [Mobplates](mobplates.md) or commands, even after they transform
* **AFK fishing** or fishing outside of open water
* Taming animals you bred yourself
* Levels you pick up again after dying
* Harvesting sugar cane, bamboo and cacti

## Mana ore

Mana ore is a block of its own with **glowing pink veins** in stone. You find it in the caves of main islands – 4 to 14 per main island. The starting island has none.

| Property | Value |
| -------- | ----- |
| Mining | Only with a **pickaxe** – every pickaxe takes about the same time |
| Yield | **3–5 Mana orbs**, up to 20 with Fortune III, plus some XP |
| Daily limit | 200 Mana from Mana ore, separate from the limit for actions |

Mana ore survives explosions and can be pushed with pistons.

### Mana orbs

Mana ore gives you Mana as **orbs** in your inventory; one orb is one Mana. They go into your account once you deposit them at a [Furnace Golem](furnace-golem.md) – you build one yourself from a Mana Block, a furnace and a carved pumpkin. Orbs you mined yourself always go in completely, orbs from other players up to 100 a day.

You can also craft with orbs:

* **Mana Charge** from 9 orbs – can be broken back down
* **Mana Block** from 8 orbs around a Mana Charge – 17 Mana, the base of the [Furnace Golem](furnace-golem.md); it can't be crafted back
* **Mana Apple** from 4 orbs around an apple – it confirms buying a blessing from the [Forestlings](forestlings.md#getting-a-blessing) and takes half the hearts of a mob you marked with a [Mobplate](mobplates.md)
* **Empty Mobplate** from 8 orbs around a Pale Sherd – see [Mobplates](mobplates.md)

Recipes and all the details are under [Mana Items](mana-items.md).

## Spending Mana

* **Biomes** in the [skill tree](skilltree.md) – from 100 Mana; the next biome on your starting path costs 125
* **Skipping quests** – see [Quests](quests.md#skipping), also as *Swap a quest* with trusted [AI residents](residents.md)
* **Forestling blessings** – 20 to 40 Mana, see [Forestlings](forestlings.md)

## Dying

If you die in Survival mode, **you keep your inventory and levels**. In return you lose **5–15 Mana**, but never more than 10 % of your balance. Below 10 Mana you lose nothing.

Below height 0 you die instantly. You wake up in your bed – or on the deck of your airship if you don't have one.

## Ruby

Ruby is the currency for **trading** – between players and with the [AI residents](residents.md#trading). Every new account starts with **500 Ruby** – they're there from your very first login.

* **Earning more:** 5 Ruby per [vote](vote.md), selling goods to [AI residents](residents.md#the-market-fund) (usually up to 10 Ruby a day) and rewards for [bug reports and clips](discord.md#bug-bounty-and-clipcoin).
* **Spending:** At other players' [ChestShops](chestshop.md), directly with `/pay` – for example as payment for goods you trade among yourselves – and with AI residents for goods, orders and tasks (up to 40 Ruby a day).
* **Market fund:** What you spend with residents goes into one shared fund for the whole network, and that fund pays for what residents buy from you. So no Ruby is created out of thin air – [more on this](residents.md#the-market-fund).
* [Forestlings](forestlings.md) **never** take Ruby; their blessings still cost Mana.
* Ruby can't be bought with real money, and Mana and Ruby can't be exchanged for each other.

## Commands

| Command | What it does |
| ------- | ------------ |
| `/bal [player]` | Show your balance (also `/balance`, `/money`) |
| `/baltop [mana\|ruby] [page]` | The richest players, 10 per page |
| `/pay <player> <amount>` | Send Ruby |

### Sending Ruby

* There's **no fee** and no confirmation prompt – double-check the name first.
* You can also send to players who are currently offline.
* Amounts may use thousands separators: `1000`, `1.000` and `1,000` all work. Decimals don't.
* Mana can't be sent – `/pay … mana` is rejected.
* **New accounts** can only pass on Ruby **24 hours after their first login** and after **20 minutes of playtime**. Receiving always works, and the message tells you how long is left. This also applies to purchases in a [ChestShop](chestshop.md). With [AI residents](residents.md#prices-and-lots), you can buy for up to 20 Ruby more than you've sold to them during that time.

## Deleting your island

Your **Mana and Ruby stay**, and so do your quest progress, streak and achievements. Bought biomes, biome quests and favourites belong to the island, though, and are gone afterwards. You don't get spent Mana back.

## Related pages

* [Skill tree & biomes](skilltree.md)
* [Mana Items](mana-items.md)
* [Furnace Golem & Mana Geode](furnace-golem.md)
* [Quests](quests.md)
* [Voting](vote.md)
* [ChestShops](chestshop.md)
* [AI residents](residents.md)
