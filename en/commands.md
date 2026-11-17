---
description: All the commands you can use as a player on MegaBuild.de.
icon: terminal
---

# Commands

You reach most features through menus. These commands take you there directly. Square brackets `[ ]` mark what you can leave out, angle brackets `< >` what you have to fill in.

## Skyblock

| Command | What it does |
| ------- | ------------ |
| `/sky` | **In the lobby:** create, join and manage your island. **On an island:** the island menu. Also `/skyblock` |
| `/quest` | Your quests. Also `/quests`, `/sky quests`, `/sky q` |
| `/sky skills` | Skill tree – unlock new biomes |
| `/sky friends` | Members of your island |
| `/sky island` | Info about your island |
| `/sky stats` | Your statistics |
| `/sky global` | Statistics for the whole server |
| `/sky visit <player>` | To a player's island – with access as a fellow player, otherwise as a [spectator](travel.md) if the island allows it. From the lobby too |
| `/sky visit` | The travel menu: open islands and your friends' islands |

The `/sky …` commands and `/quest` only exist **on the islands**, except `/sky visit <player>`. Otherwise, in the lobby `/sky` always opens the Skyblock menu. On other players' islands, `/sky stats` and `/sky global` require the **Statistics** right.

## Clans

| Command | What it does |
| ------- | ------------ |
| `/clan` | Your clan – or find and found one. Also `/clans` |
| `/c <text>` | One line to the clan chat. `/c` on its own switches clan chat on and off. Also `#` in front of a message |
| `/clan visit <player>` | To a clan member's island |
| `/clan home` | Back to your own island |
| `/clan meet` | Invite your clan to your island |
| `/clan help` | All clan commands |

All commands are listed under [Clans](clans.md#all-commands).

## AI residents

| Command | What it does |
| ------- | ------------ |
| `/residents` | All residents you know – with biome, coordinates and trust. Also `/bewohner` |
| `/residents liste` | The same as a list in chat |
| `/ki` | Set what residents may do around you |
| `/ki off` · `/ki on` | Turn residents talking to you, scenes and chat off or on |
| `/ki report` | Report what you typed to residents in the last 30 minutes to the team for review |
| `/orders` | Orders, swap requests and deliveries. Also `/auftraege` |

Only on the islands. More under [AI residents](residents.md).

## Mana & Ruby

| Command | What it does |
| ------- | ------------ |
| `/bal [player]` | Balance – yours or another player's. Also `/balance`, `/money` |
| `/baltop [mana\|ruby] [page]` | Richest players. Also `/balancetop` |
| `/pay <player> <amount>` | Send Ruby to a player |

Mana can't be sent – only Ruby.

## ChestShops

| Command | What it does |
| ------- | ------------ |
| `/shop` | Shop menu: search, markets, your shops. Also `/shops`, `/sky shop` |
| `/shop search [term]` | Search offers on all islands |
| `/shop hand` | Who trades the item in your main hand? |
| `/shop markets` | Open markets of all islands |
| `/shop mine` | Your shops with stock and space |
| `/shop areas` | This island's shop areas |
| `/shop home` | Back to your own island |

Only on the islands. All commands are listed under [ChestShops](chestshop.md#commands).

## Rank commands

| Command | Rank | What it does |
| ------- | ---- | ------------ |
| `/craft` | Gold | A crafting table without a block. Also `/workbench`, `/wb` |
| `/stonecutter` · `/loom` · `/cartography` | Platin | Stonecutter, loom or cartography table without a block |
| `/trash` | Gold | The trash – only what you confirm is gone |
| `/trash undo` | Gold | Gets back what you threw away last, for 5 minutes |
| `/ec` | Gold | Your [ender chest](ranks.md#ender-chest) from anywhere. Also `/enderchest` |
| `/ptime morning` · `noon` · `evening` · `night` | Platin | Your own time of day – only you see it |
| `/ptime <time>` | Titan | Any time, for example `/ptime 21:30` |
| `/ptime freeze` | Titan | Stop your time or let it run again |
| `/ptime reset` | Platin | Back to the island's time |
| `/hat` | Gold | The item in your hand as a hat – only for show. `/hat off` takes it off |
| `/sit` · `/lay` · `/crawl` | Gold | Sit, lie down, crawl. Type it again or sneak to get up |
| `/rename [name]` | Gold | Rename the item in your hand – with colours from Platin, also RGB and gradients with Titan. `/rename clear` removes the name |
| `/head <player>` | Gold | Get a player's head, bound to you. Gold 1 a month, Platin 1 a week, Titan 1 a day |
| `/nick <name>` | Platin | Another name in chat and the tab list, with `~` in front. `/nick clear` removes it |
| `/status <text>` | Platin | A text behind your name in the tab list. `/status clear` removes it |

`/nick` and `/status` work across the whole network. All other rank commands work on all Sky islands, as a visitor too – not for 10 seconds after a hit and not as a customer on someone else's market. A higher rank has everything from the rank below. More under [Ranks](ranks.md#perks-across-the-network).

## Friends & messages

| Command | What it does |
| ------- | ------------ |
| `/friend` | Your friends list. Also `/friends`, `/friend list` |
| `/friend <player>` | Send a friend request – or accept theirs |
| `/friend add` | Players you can ask |
| `/friend requests` | Pending requests |
| `/g <text>` | One line to the [global chat](messages.md#global-chat) – to everyone on the network, also with a Forestling. It doesn't work on a residents' island. A normal chat line goes to the network too; with `!` in front it stays on your server |
| `/msg <player> <text>` | Private message – if the player isn't online, it goes to their mailbox. Also `/tell`, `/w` |
| `/r <text>` | Reply to the last private message. Also `/reply` |
| `/mail` | Your mailbox. Also `/post` |
| `/mail <player> <text>` | Quickly send a message to someone's mailbox |

## Network

| Command | What it does |
| ------- | ------------ |
| `/hub` | Back to the lobby. Also `/lobby` |
| `/ot [player]` | Playtime and first join. Also `/onlinetime`, `/playertime`, `/otime`, `/pt` – but not `/ptime`, that's the rank command for your [own time of day](ranks.md#your-own-time-of-day) |
| `/vote` | Vote link, your reward and how often you've already voted today. Also `/votes` |
| `/connect` | Link your Minecraft and Discord accounts. `/connect status` shows the current state, `/connect disconnect` removes the link |
| `/linkaccount` | Link your Java and Bedrock accounts |
| `/discord` | Link to the Discord. Also `/dc` |
| `/wiki` | Link to this wiki. Also `/help` |

{% hint style="info" %}
**On the intro server** – during the intro with Mala – only the network commands work.
{% endhint %}

## Related pages

* [Friends](friends.md)
* [Messages & Mail](messages.md)
* [Mana & Ruby](economy.md)
* [ChestShops](chestshop.md)
* [Ranks](ranks.md)
* [Discord](discord.md)
