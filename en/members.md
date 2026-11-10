---
description: >-
  Invite players to your island, decide what they're allowed to do there, give
  your clan and your friends access and choose who may watch.
icon: users-gear
---

# Members & Rights

You can invite up to **25 members** to your island and decide for each of them what they're allowed to do. Your [clan](clans.md) and your friends can get access without an invitation too – see [Clan and friends](#clan-and-friends). You decide who may only look around your island under [Watching](#watching).

## Inviting a member

{% stepper %}
{% step %}
#### Open the menu

**In the lobby:** `/sky` → **Members** → **Add a member**

**On the island:** `/sky friends` → **Add a member**
{% endstep %}

{% step %}
#### Choose a player

First you see your friends list. The search finds every player in the network, even offline ones – enter at least **3 characters** of the name.
{% endstep %}

{% step %}
#### Confirm

Click **Invite**. The player gets a message and a mail and can enter your island right away – as a **Builder**.
{% endstep %}
{% endstepper %}

The owner and members with the **Members** right can invite.

## The rights

| Right | What it allows |
| ----- | -------------- |
| **Build** | Place and break blocks, buckets, fire, armour stands, frames, signs |
| **Containers** | Chests, barrels, furnaces, hoppers, brewing stands, lecterns, the [Furnace Golem](furnace-golem.md) menu and the chest on its head |
| **Switches** | Doors, trapdoors, fence gates, buttons, levers, pressure plates |
| **Animals** | Hit, feed, breed, leash, shear, milk and ride animals, put [Forestlings](forestlings.md#on-a-lead) on a lead and untie them |
| **Harvest** | Harvest ripe crops and replant |
| **Warpetts** | Use and place [Warpett](warpetts.md) flowers and eggs, collect and set down Warpetts with a [Mobplate](mobplates.md) |
| **Skill tree** | Buy biomes, set favourites, ask the clan for help, open [shops](chestshop.md), manage [shop areas](chestshop.md#shop-areas) |
| **Members** | Manage members, rights and access |
| **Statistics** | View the island statistics |

On top of that there's the **Join** switch: if it's off, the member only gets onto the island through clan or friend access – or as a [spectator](travel.md) without rights, if you allow [watching](#watching).

**Without any special right**, everyone playing on the island may fight monsters, pick up items, fish, talk and trade with residents and Forestlings, click signs, use the ender chest and workstations without storage – crafting table, stonecutter, loom, cartography table, smithing table, grindstone, enchanting table and anvil. Stricter rules apply to [spectators](travel.md).

* If you're missing a right, the display above the hotbar tells you which one – for example “You may not build here.”
* Breaking a chest, furnace or any other block with contents needs **Build and Containers**.
* Building or dismantling a [Furnace Golem](furnace-golem.md) needs **Build**, opening its menu or its chest needs **Containers**.
* **Shop containers** can only be opened by the shop owner, the island owner and the team – the Containers right isn't enough.
* **Flying** with your rank's `/fly` only works where you have the **Build** right.
* As the owner you always have all rights. Only you can **delete** your island, in the lobby.

## Templates

So you don't have to set every right individually, there are four templates. Each one includes everything from the one before:

| Template | Rights |
| -------- | ------ |
| **Visitor** | Switches |
| **Helper** | plus Harvest and Animals |
| **Builder** | plus Build, Containers and Warpetts |
| **Manager** | plus Skill tree, Members and Statistics |

If you change a single right, the menu shows **Custom**.

* **New members** come in as **Builders**. They can only buy biomes and open shops once you give them the **Skill tree** right.
* **Members from before** keep all action rights. Only those who were set as **Visitor** before can now just use doors and switches.

## Editing members

**On the island** (`/sky friends`) you see your members' heads:

* **Left-click** opens their rights. At the top, **Template** cycles through Visitor → Helper → Builder → Manager; below that you switch every right individually, and **Join**.
* **Right-click** revokes the player's access.

**In the lobby** (`/sky` → **Members**) you only change the template. You set individual rights on the island.

{% hint style="warning" %}
**Whoever clicks, pays for the biome.** If a member with the Skill tree right buys a biome, the Mana is taken **from their account** – not from yours.
{% endhint %}

## Clan and friends

At the very top of the members menu on the island there are three cards: **Watching** (see [below](#watching)), **Clan access** for your [clan](clans.md) and **Friend access** for your [friends](friends.md). With the two access cards, they can come onto your island without you inviting each of them.

| Level | What they may do |
| ----- | ---------------- |
| **Nobody** | Only with their own invitation |
| **Visitor** | Come in, look around and use switches |
| **Helper** | Also harvest and tend animals |
| **Builder** | Also build, open containers and use Warpetts |

* **At the start**, clan access is set to **Visitor** and friend access to **Nobody**.
* Anyone with the **Members** right may change it. You can also set the friend access of your own island in your friends under **Settings**.
* If someone is a member and also in the clan or a friend, the higher level applies.
* **Clan recruits** (the first 72 hours) come in as visitors at most.
* If someone leaves your clan or you set the access to Nobody, they lose their rights immediately. If they may watch on your island, they stay as a spectator; otherwise they switch to the lobby.

**Visiting** works with `/sky visit <name>` – from the lobby too –, through the [travel menu](travel.md), from the clan's member list or from the friends list. Your inventory travels with you.

## Watching

Anyone who is neither a member of your island nor gets in through clan or friend access may look around it as a **spectator** – come in and look around, but not change anything. What spectators may do is under [Travel & Watching](travel.md).

You set who may watch on the island under `/sky` → **Members** → **Watching**. The selected level has a glint.

| Level | Who may watch |
| ----- | ------------- |
| **Everyone** | Anyone |
| **Friends only** | Only your [friends](friends.md) – even if friend access is set to Nobody |
| **Members only** | Nobody. Only those with access to the island come in |

* **At the start**, watching is set to **Everyone**. As long as your island is running, it then appears in the [travel menu](travel.md) under **Open islands**.
* Anyone with the **Members** right may change it.
* If you make it stricter, spectators who may no longer watch switch to the lobby right away.
* Anyone who comes in as a member with **Join**, through clan access, a call for help or friend access plays with their rights as before. Only those who get in through this level alone are spectators.
* Spectators don't wake your island: if it's asleep, nobody can watch.
* **Clan islands** are never open for watching.

## What members get out of it

* Members help with the [biome quests](skilltree.md#biome-quests) and get **25 Mana** when one is completed – just like you. Clan members get the same through a [call for help](clans.md#calls-for-help).
* Their [quests](quests.md) count on your island too.
* Their playtime on your island is shown in the member list.

## Islands you're a member of

In the lobby, `/sky` → **Shared servers** opens a list of all islands you're a member of. One click takes you there, even if the island isn't running.

To see which rights you have on an island, go to `/sky` → **Island** → **Your rights** there.

## Related pages

* [Clans](clans.md)
* [Friends](friends.md)
* [Travel & watching](travel.md)
* [Your island](island.md)
* [Skill tree & biomes](skilltree.md)
