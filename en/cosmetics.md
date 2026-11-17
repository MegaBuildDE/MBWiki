---
description: >-
  Cosmetics for ranks on MegaBuild.de – trails, prefix styles, name colours,
  chat emojis, island greeting and your airship.
icon: wand-magic-sparkles
---

# Cosmetics

Cosmetics only change how you, your name or your island look. They give you no advantage in the game: no Mana, no Ruby, nothing in combat. You get them with a [rank](ranks.md), and each higher rank has everything from the rank below.

| What | Gold | Platin | Titan |
| --- | --- | --- | --- |
| [Trails](#trails) | 2 | 6 | all 16 |
| [Prefix style](#prefix-styles) – your rank badge | single colour | 4 gradients | plus 3 animated |
| [Name colour](#name-colour) | – | 12 colours | plus 6 gradients |
| [Chat emojis](#chat-emojis) | 24 | 24 | 24 |
| [Island greeting](#island-greeting) | 3 sounds | 3 sounds | 7 sounds |
| [Airship](#airship) | Gold pennant | Platin pennant, 2 paints | Titan sail, all 8 paints |

If you lose the rank later, your choice stays saved. It just isn't shown, and it comes back with the rank.

## The cosmetics menu

```
/cosmetics
```

`/cosmetics` – `/cos` for short – opens the cosmetics menu. It works on the **Sky islands**. Each tile leads to a page: trails, prefix, name colour, emojis, airship and greeting. Tiles that are grey and say “soon” aren't there yet.

What you don't have yet is grey in the list, with the rank that includes it. You can't buy anything in the menu.

### What I see

Under **What I see** you hide what others wear – only for you. Every switch is on by default:

* **Trails** – other players' trails,
* **Greetings** – the greetings of other islands.

The other switches belong to cosmetics that are still to come. `/cosmetics view` opens the page directly.

## Trails

```
/trail [trail]
/trail off
```

A trail follows behind you. There are two kinds:

* **Particle trail** – at your feet when you walk or run. Not when you stand still or sneak.
* **Elytra trail** – behind you when you glide with the elytra.

You always wear **one** trail. `/trail` opens the list, a click puts a trail on. `/trail <trail>` chooses directly, for example `/trail cherry`, and `/trail off` takes it off.

**Preview:** If you click a trail you don't have yet, you see it on yourself for **10 seconds** – only you. `/cosmetics preview <trail>` does the same.

| Trail | `/trail` | Kind | Rank |
| ----- | -------- | ---- | ---- |
| Cherry Blossoms | `cherry` | Particle | Gold |
| Contrail | `contrail` | Elytra | Gold |
| Note Trail | `notes` | Particle | Platin |
| Fireflies | `fireflies` | Particle | Platin |
| Comet Tail | `comet` | Elytra | Platin |
| Wings of Flame | `wingfire` | Elytra | Platin |
| Soul Flames | `soulfire` | Particle | Titan |
| Runes | `runes` | Particle | Titan |
| Spore Bloom | `spores` | Particle | Titan |
| Sparks | `sparks` | Particle | Titan |
| Pale Leaves | `paleleaves` | Particle | Titan |
| Portal Vortex | `vortex` | Elytra | Titan |
| Soul Stream | `souls` | Elytra | Titan |
| Totem Shine | `totem` | Elytra | Titan |
| Glow Band | `glow` | Elytra | Titan |
| Gold Sparks | `goldsparks` | Elytra | Titan |

* **Where:** on all Sky islands, as a visitor too. Not for 10 seconds after a hit and not while you are invisible.
* **Clan flight trail:** An elytra trail covers your [clan's flight trail](clans.md#everyday-perks). Take it off and you fly with the clan flight trail again. It is also in the trail list – a click on it takes your elytra trail off.
* **On Bedrock** the particles look similar, size and path differ a little.

## Prefix styles

```
/prefix
```

Your rank is shown as a **badge** in front of your name, in chat and in the tab list. With `/prefix` you choose how it looks:

| Rank | Styles |
| ---- | ------ |
| Gold | the Gold badge, single colour |
| Platin | **gradients:** Ice, Sunset, Emerald, MegaBuild |
| Titan | the four gradients and also **animated:** Shine, Pulse, Sparkle |

* **Animated styles** move in the tab list. Chat shows their first frame – a chat line doesn't change after it is sent.
* **Standard** brings your badge back the way it is.
* **On Bedrock** the badge is only in chat. The tab list there only shows names.

## Name colour

```
/namecolor
/namecolor reset
```

From **Platin**, `/namecolor` colours your name, in chat and in the tab list.

* **Platin – 12 colours:** Dark blue, Dark green, Dark aqua, Purple, Gold, Grey, Blue, Green, Aqua, Pink, Yellow, White.
* **Titan – plus 6 gradients:** Sun, Ocean, Forest, Aurora, Ice, MegaBuild.
* If you have a [nick](ranks.md#nick), it gets the same colour.
* **In clan chat**, in `/msg` and in the mail your name has no colour.
* `/namecolor reset` takes the colour away again.
* **On Bedrock** the colours look the same in chat, gradients in steps. In the tab list your name has no colour there.

## Chat emojis

```
/emojis
```

From **Gold**, `:name:` turns into a picture, for example `:herz:`, `:feuer:` or `:gg:`. At most **5 per message**, upper and lower case don't matter.

* **Where:** in global chat, in your server's chat, in clan chat, in `/msg` and in the [mail](messages.md#the-mailbox).
* **Without a rank**, `:herz:` simply stays text.
* `/emojis` shows all 24. A click writes the name into your chat line.

The names are German – they are the same for everyone. The 24 emojis: `:lachen:` (laughing) `:grinsen:` (grinning) `:zwinkern:` (winking) `:cool:` `:traurig:` (sad) `:weinen:` (crying) `:wuetend:` (angry) `:staunen:` (amazed) `:verliebt:` (in love) `:denken:` (thinking) `:herz:` (heart) `:daumen:` (thumbs up) `:feuer:` (fire) `:stern:` (star) `:pokal:` (trophy) `:mana:` `:ruby:` `:luftschiff:` (airship) `:insel:` (island) `:krone:` (crown) `:geschenk:` (gift) `:party:` `:gg:` `:schlafen:` (sleeping) – instead of `:wuetend:` you can also write `:wütend:`.

## Island greeting

```
/sky greeting
```

From **Gold**, your island greets its visitors: with a **title**, a **subtitle** and a **sound**. Only the **island owner** can set it. `/sky greeting` opens the menu with preview, title, subtitle, sound and the on/off switch.

1. **Title and subtitle** you type into chat after a click. Together at most **48 characters**, no links. Colours work with `&` codes, RGB and gradients from Platin. With `cancel` everything stays as it was.
2. **The sound** you choose from a list. A click plays it so you can listen – the ones you don't have yet too.

| Rank | Sounds |
| ---- | ------ |
| Gold, Platin | Bell, Harp, Seagulls |
| Titan | plus Goat horn, Wind chimes, Amethyst chime, Drum |

* **Who sees it:** visitors when they arrive on your island – each one at most every **10 minutes**. Not your island members, and there is no greeting on the clan island.
* **Hiding:** visitors can hide other islands' greetings under [What I see](#what-i-see).
* **The rules:** The chat filter applies, and the greeting must not sound as if it came from the team. The team can reset it.
* **Without a rank**, colours and Titan sounds are dropped. If you haven't been on any Sky island for **35 days**, the greeting rests until you come back.

## Airship

```
/sky ship
```

The airship in front of your island shows your rank:

* **Gold** – a yellow pennant at the bow,
* **Platin** – a light blue pennant,
* **Titan** – a sail of its own in blue and white.

Only the sign of your highest rank is shown. You can also switch it off.

From **Platin** you give the ship a new paint:

| Rank | Paints |
| ---- | ------ |
| Platin | Emerald, Night Sky |
| Titan | all eight: Standard, Emerald, Night Sky, Cherry Wood, Ice, Copper, Nether, Sunset |

**How it works:** `/sky ship` opens the menu – so do the **Airship** card in the island menu and the tile in the cosmetics menu.

* **Left-click** chooses a paint. Only the island owner can do that.
* **Right-click** shows you for **20 seconds** how the ship looks with it – only you, within sight of the ship. Anyone can do that, guests too.
* **If someone is on board** or a landing is running, the ship remembers your choice and is painted afterwards.
* **The clan island** keeps its ship as it is.
* **Without a rank** the ship goes back to Standard and the highest sign you still have.

| Command | What it does |
| ------- | ------------ |
| `/sky ship` | The airship menu. Also `/sky ship paint`, `/sky schiff` |
| `/sky ship paint <paint>` | Choose a paint directly: `standard`, `emerald`, `nightsky`, `cherry`, `ice`, `copper`, `nether`, `sunset` |
| `/sky ship preview <paint>` | 20 seconds preview, only for you. With `gold`, `platin` or `titan` you see the pennant or sail |
| `/sky ship badge on` · `off` | Switch the pennant or sail on or off |

## Related pages

* [Ranks](ranks.md)
* [Pets](pets.md)
* [Commands](commands.md#cosmetics)
* [Messages & Mail](messages.md)
* [Clans](clans.md)
