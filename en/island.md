---
description: >-
  Your island on MegaBuild.de – your own server, menus, management, dying and
  what happens when you delete it.
icon: tree
cover: ../.gitbook/assets/screenshots/mbsky-wuestenhaus.webp
coverY: 0
---

# Your Island

Every island is **its own server** with its own world. Only you, your [members](members.md) and – if you allow it – your [clan](clans.md) and your friends can play on it. Everyone else may look around your island as a [spectator](travel.md), unless you restrict [watching](members.md#watching). You can own an island yourself and also be a member on other players' islands.

As you explore, a whole island world grows around your starting island:

{% content-ref url="world.md" %}
[world.md](world.md)
{% endcontent-ref %}

## The Skyblock menu

`/sky` opens the Skyblock menu. What's in it depends on where you are.

{% tabs %}
{% tab title="In the lobby" %}
| Menu item | What you do there |
| --------- | ----------------- |
| **Join Island** | Travel to your island. If it's asleep, it gets woken up |
| **Management** | Rename your island (3–20 characters), server info, statistics, **Delete the server** |
| **Members** | Invite players and assign rights |
| **Statistics** | Your stats, leaderboards and the whole network |
| **Shared Servers** | Islands you're a member of |
| **Friends & Clan** | Friends, [clan](clans.md) and mail |

If you don't have an island yet, you'll find **Create Skyblock** here instead – see [Getting started](start.md).
{% endtab %}

{% tab title="On the island" %}
| Menu item | Command | What you do there |
| --------- | ------- | ----------------- |
| **Skill tree** | `/sky skills` | Buy biomes, biome quests, favourites |
| **Quests** | `/quest` | Daily, weekly and bonus quests |
| **Members** | `/sky friends` | Members and rights |
| **Statistics** | `/sky stats` | Your stats on this island |
| **Island** | `/sky island` | Server, starting biome and **Your rights** – what you're allowed to do on this island |
| **Friends & Clan** | `/friend` | Friends, [clan](clans.md) and mail |
| **Travel** | `/sky visit` | Visit open islands and your friends' islands – see [Travel & Watching](travel.md) |
| **Shops** | `/shop` | Search [ChestShops](chestshop.md), markets and your own shops |
| **To your own island** | `/clan home` | Back to your island when you're somewhere else |

Clicking the **Golem** on your airship also opens the skill tree.
{% endtab %}
{% endtabs %}

## Getting around

* **To your island:** In the lobby, `/sky` → **Join Island**. To islands you're a member of: `/sky` → **Shared Servers**.
* **Visiting:** With `/sky visit <name>` to another player's island, on an island also through `/sky` → **Travel**. If you have no access there, you watch if the island allows it – see [Travel & Watching](travel.md). **Your inventory travels with you** – ender chest and levels stay on each island.
* **Back to the lobby:** `/hub` (or `/lobby`).
* **Coming back:** If your island is running, you land straight on it when you log in. Otherwise you arrive in the lobby, and the lobby [wakes your island](#waking-up-your-island) right away.
* **Getting around on the island:** With the [Warpetts](warpetts.md) – your first pair connects your starting island and the airship.

## Waking up your island

If nobody has been on your island for a while, it falls asleep. When you then arrive in the lobby, the lobby wakes it right away – you don't have to do anything.

* **While it wakes up,** your action bar shows “Waking up your island”, followed by changing lines like “Mala wakes the crew” or “Wind fills the sails”. You can move around the lobby freely.
* **Once it's ready,** the chat says “Your island is ready – **[To your island]**”. Click **[To your island]** to go there – the button works for 15 minutes. **Bedrock** has no button – type `/sky` and choose **Join Island** instead.
* **Back by itself:** If you were on your own island last time and haven't chosen anything else in the lobby since – no menu opened, no command typed, no character clicked – the lobby sends you back as soon as your island is ready.
* **Clicking yourself works too:** If you choose `/sky` → **Join Island** in the meantime, that takes you there as soon as your island is ready.
* **All places taken?** Then you'll read “All places are taken right now. Please try again in a minute.”

Only your **own** island is woken up. To islands you're a member of, you go as before via `/sky` → **Shared Servers**. Archived clan islands and islands whose last build failed aren't woken up by the lobby on its own.

## Dying

If you die on your island in Survival mode:

* **You keep your inventory and levels.**
* You lose **5–15 Mana**, but never more than 10 % of your balance. Below 10 Mana you lose nothing.
* You wake up in your **bed** – or on the deck of your **airship** if you don't have one.

Below height 0 you die instantly.

## Deleting your island

In the lobby under `/sky` → **Management** → **Delete the server**. The menu asks you to confirm first.

| Stays | Gone |
| ----- | ---- |
| Your **Mana and Ruby** | The island and everything on it |
| Quest progress and streak | Bought **biomes**, biome quests and favourites |
| Your **achievements** | Warpetts, residents and their trust on this island |

You don't get spent Mana back. Afterwards you can create a new island and choose a new crystal.

{% hint style="danger" %}
**Deleting the server is permanent.** Your island and everything on it will be gone.
{% endhint %}

## Good to know

* **One island of your own per player.** If you already have one, "Create Skyblock" opens the management menu directly.
* **The crystal stays.** Your starting biome is set when you create the island and can't be changed – only with a new island.
* **Your island, your world.** On your island you only see other players you let in – as members, through clan or friend access or as [spectators](travel.md). The lobby is where everyone meets – or on an island with `/clan meet`.

## Related pages

* [The island world](world.md)
* [Members & rights](members.md)
* [Travel & watching](travel.md)
* [Skill tree & biomes](skilltree.md)
* [Warpetts](warpetts.md)
