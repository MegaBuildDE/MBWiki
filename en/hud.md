---
description: >-
  What the displays on your screen mean – on Java and Bedrock – and where to
  find your statistics.
icon: gauge
---

# HUD & Statistics

Each box in the HUD shows only an **icon and a number**. The icon tells you what's being counted – a pickaxe for a mining quest, a sword for combat.

## Top: three boxes

| Box | Icon | Example | What it shows |
| --- | ---- | ------- | ------------- |
| **1** | Globe | `12/40` | Biomes your island owns. All fellow players see the island's progress. It's 40 as long as the Water crystal is locked |
| **2** | Icon of the quest's theme | `7/12` | The quest you're currently tracking |
| **3** | changes every 5 seconds | | Completed quests · your playtime **on this island** · animals and monsters defeated · players on this island |

**Which quest box 2 shows:**

1. the quest you **pinned** in the quest menu,
2. otherwise the quest you made progress on in the last 10 minutes,
3. otherwise the first open quest.

This also applies to your island's [biome quest](skilltree.md#biome-quests) – then you see the progress of the whole island. After you complete a quest, a checkmark shows briefly. If you have no open quest, the box counts the blocks you've mined since joining the server.

{% hint style="info" %}
**Special quest:** While you're looking for your first resident, box 2 shows an **arrow** that turns as you look around, along with the distance in meters.
{% endhint %}

## Bottom right: Mana & Ruby

Right above your hunger bar you see your **Mana** (pink orb), and above that your **Ruby** (red gem).

{% content-ref url="economy.md" %}
[economy.md](economy.md)
{% endcontent-ref %}

## In the lobby

In the lobby, the boxes show the **time**, the **server** you're on and how many **players** are online in the network.

## On Bedrock

Bedrock shows the same numbers, with a few differences:

* **No bars** behind the numbers – the number tells you the same thing.
* The quest box **always shows the scroll** instead of the theme icon, even after you complete a quest.
* For very large targets, such as long walking quests, you see the percentage instead of `4321/9000`: `48%`.
* The tab list doesn't show the **Residents (KI)** section – use `/residents` instead.

## Statistics

{% tabs %}
{% tab title="In the lobby" %}
`/sky` → **Statistics** has three pages:

| Page | Contents |
| ---- | -------- |
| **Personal dashboard** | Activity, mining & building, progress, farming, combat, generation and your playtime on your islands |
| **Top lists** | The top players in mining, building, harvesting, planting and monsters defeated |
| **World & network** | The most common biomes and island types across the whole network |
{% endtab %}

{% tab title="On the island" %}
| Command | Contents |
| ------- | -------- |
| `/sky` → **Statistics** | Mining, building, harvesting, combat, quests, skill tree, playtime, biomes and islands |
| `/sky stats` | Your stats in chat |
| `/sky global` | The whole server's stats in chat |

On other players' islands you need the **Statistics** right for this. Your fellow players' playtime on your island is shown in the member list.
{% endtab %}
{% endtabs %}

## Playtime

```
/ot [player]
```

Shows your total playtime in the network and your first join – or another player's. `/onlinetime` and `/pt` work too.

## Language

Menus, chat and Mala's voice follow the **language of your Minecraft client**: German for a German client, English otherwise.

## Related pages

* [Quests](quests.md)
* [Skill tree & biomes](skilltree.md)
* [Achievements](achievements.md)
