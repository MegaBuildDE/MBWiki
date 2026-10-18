#!/usr/bin/env python3
"""Deine Insel lebt - KI-Bewohner und Forestlinge auf MegaBuild Skyblock.

Stand: Release vom 12.10.2026 (MBSkyManager: ai/, forestling/). Zahlen sind
Standardwerte aus ai.yml und config.yml. Malas Zeilen sind die echten Aufnahmen
von der Begegnungsinsel, Chatzeilen stammen aus lang/de.yml und ai/dialoge.
Wichtig (KI_SPIELER.md): Siedlungen nie als Kaufanreiz fuer Biome zeigen.

    python3 bauen.py bewohner [--sprache en]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

PIP = "§fPip §b(KI)§7: §f"
MOSS = "§fMoss §b(KI)§7: §f"


def szene_intro(e, t, d):
    titelkarte(e, t, L("Deine Insel lebt", "Your island is alive"),
               L("Bewohner und Forestlinge auf MegaBuild Skyblock", "Residents and Forestlings on MegaBuild Skyblock"),
               y=150)
    y = 860
    figuren = [("goblin_idle", W / 2 - 420, 300, False), ("shroom_idle", W / 2 - 140, 230, False),
               ("forest_oak", W / 2 + 140, 230, True), ("schmied", W / 2 + 420, 300, True)]
    for i, (name, x, g, sp) in enumerate(figuren):
        s = rueckschwung(phase(t, .7 + i * .15, 1.15 + i * .15))
        if s > 0:
            schatten(e, x, y, g * .6 * s, .7)
            sprite_boden(e, name, t, x, y, g * s, spiegeln=sp)


def szene_nachbarn(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    y = 560
    mc.einfuegen(e, insel_bild(38, 6, 9, 16, baum=False), CX - 38 * 8, y - 16, ein)
    figuren = [("goblin_idle", CX - 300, 280, "§fPip §b(KI)", False), ("shroom_idle", CX - 20, 210, "§fMoss §b(KI)", False),
               ("schmied", CX + 260, 280, "§fBruno §b(KI)", True)]
    for i, (name, x, g, schild, sp) in enumerate(figuren):
        u = rueckschwung(phase(t, .3 + i * .25, .8 + i * .25))
        if u > 0:
            sprite_boden(e, name, t + i, x, y, g * u, ein, spiegeln=sp)
            namensschild(e, x, y - g * .92, schild, 3, ein * min(1, u))
    zeilen = [(L("Einsiedler", "Hermits"), L("wohnen allein auf Inseln, die du erkundest", "live alone on islands you explore")),
              (L("Siedlungen", "Settlements"), L("1–5 Bewohner, aus Zelten wird ein Dorf", "1–5 residents, tents grow into a village")),
              (L("Begegnungsinsel", "Meeting island"), L("dein erster Bewohner, gleich am Start", "your first resident, right at the start"))]
    for i, (kopf, text) in enumerate(zeilen):
        u = aus_kubisch(phase(t, 2.0 + i * .5, 2.5 + i * .5))
        mct(e, 900, 650 + i * 50, "§b" + kopf + "§7  " + text, 3, ein * u)


def szene_reden(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    y = 520
    mc.einfuegen(e, insel_bild(20, 5, 3, 14, baum=False), CX - 10 * 14 - 260, y - 14, ein)
    sprite_boden(e, "goblin_talk" if t > 4.2 else "goblin_idle", t, CX - 260, y, 300, ein)
    namensschild(e, CX - 260, y - 290, "§fPip §b(KI)", 3, ein)
    hinweis = L("§7Du bist bei §fPip (KI)§7. Was du jetzt in den Chat schreibst, hört nur, wer hier wohnt. "
                "Mit §f! §7vorn schreibst du an alle.",
                "§7You're with §fPip (KI)§7. What you type in chat now is only heard by those who live here. "
                "Start with §f! §7to write to everyone.")
    eingabe_text = L("was machst du hier?", "what are you doing here?")
    getippt = tippen(eingabe_text, t, 2.0, 3.4)
    zeilen = chatzeilen([
        (.6, hinweis),
        (3.6, L("§7Du → Pip: §f", "§7You → Pip: §f") + eingabe_text),
        (4.5, PIP + L("Ich wohne hier und baue an meiner Hütte. Hier oben gibt es für jeden etwas zu tun.",
                      "I live here and I'm building my hut. There's something to do for everyone up here.")),
        (6.6, L("§7Du → Pip: §f", "§7You → Pip: §f") + L("handeln", "trade")),
        (7.4, PIP + L("Gern! Schau dir mein Lager an.", "Sure! Take a look at my stock.")),
    ])
    eingabe = "§f" + (getippt if t < 3.6 else "") + ("_" if int(t * 3) % 2 == 0 else "")
    chat(e, 880, 830, zeilen, t, 3, ein, eingabe)


def szene_alltag(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    figuren = [("goblin_hacken", L("§fHacken", "§fChopping")), ("goblin_ernten", L("§fErnten", "§fHarvesting")),
               ("schmied", L("§fSchmieden", "§fForging")), ("shroom_graben", L("§fGraben", "§fDigging")),
               ("goblin_sit", L("§fPause", "§fBreak")), ("goblin_sleep", L("§fSchlafen", "§fSleeping"))]
    for i, (name, label) in enumerate(figuren):
        x = 980 + (i % 3) * 300
        y = 470 + (i // 3) * 320
        u = rueckschwung(phase(t, .2 + i * .18, .65 + i * .18))
        if u <= 0:
            continue
        mc.einfuegen(e, tafel(260, 290, 18, (10, 16, 36, 160), (255, 255, 255, 26)), x - 130, y - 250, ein * min(1, u))
        schatten(e, x, y, 140 * u, .6 * ein)
        sprite_boden(e, name, t, x, y, 230 * u, ein)
        mct(e, x, y + 2, label, 3, ein * min(1, u), anker="m")


STUFEN = [("member", L("Fremd", "Stranger"), L("spricht dich an", "talks to you")),
          ("friends", L("Bekannt", "Acquainted"), L("reden, Lager ansehen", "chat, see the stock")),
          ("coin", L("Handelspartner", "Trade partner"), L("kaufen und verkaufen", "buy and sell")),
          ("shared", L("Offen", "Open"), L("Tausch, Aufgaben, Aufträge", "barter, tasks, orders")),
          ("star", L("Vertraut", "Trusted"), L("persönliche Angebote", "personal offers"))]


def szene_vertrauen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    x0, y0, rh = 900, 200, 112
    stand = 4.0 * ein_aus(phase(t, 1.0, 7.0))
    linie_x = x0 + 40
    mc.einfuegen(e, Image.new("RGBA", (6, 4 * rh), (40, 46, 80, 230)), linie_x - 3, y0 + 40, ein)
    voll = stand * rh
    if voll > 0:
        mc.einfuegen(e, Image.new("RGBA", (6, int(voll)), (85, 255, 255, 255)), linie_x - 3, y0 + 40, ein)
    for i, (ic, name, frei) in enumerate(STUFEN):
        y = y0 + i * rh
        u = aus_kubisch(phase(t, .1 + i * .08, .5 + i * .08))
        erreicht = stand >= i - .02
        t_hit = 1.0 + 6.0 * umkehr_ein_aus(i / 4) if i else 0
        s = 1 + .25 * math.sin(math.pi * phase(t, t_hit, t_hit + .3)) if erreicht and i else 1
        box = tafel(80, 80, 14, (85, 255, 255, 255) if erreicht else (34, 40, 72, 255), (20, 16, 30, 255))
        skaliert(e, box, linie_x, y + 40, 80 * s, alpha=ein * u, glatt=True)
        icon_bei(e, ic, linie_x - 28, y + 12, 56, ein * u * (1 if erreicht else .5))
        mct(e, x0 + 110, y + 14, ("§b§l" if erreicht else "§7§l") + name, 4, ein * u)
        mct(e, x0 + 110, y + 58, ("§f" if erreicht else "§8") + frei, 3, ein * u)
    sprite_boden(e, "goblin_hello" if t > 6.6 else "goblin_idle", max(0, t - 6.6) if t > 6.6 else t, 1700, 720, 280, ein,
                 schleife=t <= 6.6, spiegeln=True)


def szene_handel(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    slots = {10: "mining", 11: "harvest", 12: "building", 13: "quest_fishing", 14: "potion_icon", 16: "coin",
             19: "craft_button", 21: "quest_trading", 23: "quests", 27: "back", 35: "close"}
    tipps = {
        10: [L("§fEisenbarren §7×64", "§fIron ingots §7×64"), L("§7Preis: §d45 Mana", "§7Price: §d45 Mana"),
             L("§7Vorrat: §fviel", "§7Stock: §fplenty"), L("§8Klick zum Kaufen", "§8Click to buy")],
        11: [L("§fBrot §7×16", "§fBread §7×16"), L("§7Preis: §d14 Mana", "§7Price: §d14 Mana"),
             L("§8Klick zum Kaufen", "§8Click to buy")],
        16: [L("§eVerkaufen", "§eSell"), L("§7Bis zu §d30–40 Mana §7am Tag", "§7Up to §d30–40 Mana §7a day"),
             L("§7je Bewohner", "§7per resident")],
        21: [L("§aTauschen", "§aBarter"), L("§7Ware gegen Ware –", "§7Goods for goods –"),
             L("§7auch nach dem Tageslimit", "§7even past the daily limit")],
    }
    halte = [(.5, 1.0, 10), (2.0, 2.4, 11), (3.5, 3.9, 16), (5.0, 5.4, 21)]
    menue_mit_zeiger(e, t, L("§6§lPips Lager", "§6§lPip's stock"), 4, slots, tipps, halte, 880, 300, 4, ein)
    u = aus_kubisch(phase(t, 6.4, 6.9))
    mct(e, 880, 760, L("§aMana §7oder §aWare §7– §cnie Ruby oder Echtgeld", "§aMana §7or §agoods §7– §cnever Ruby or real money"),
        4, ein * u)


SEGEN = [("forest_oak", L("Himmelsprung", "Sky Leap"), 20), ("forest_birch", L("Luftsprung", "Air Jump"), 25),
         ("forest_cherry", L("Kirschblütensprung", "Blossom Leap"), 30), ("forest_mangrove", L("Wurzelbrücke", "Root Bridge"), 30)]


def szene_forestlinge(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    # oben: vier Forestlinge mit ihrem Segen
    for i, (name, segen, preis) in enumerate(SEGEN):
        x = 970 + i * 230
        u = rueckschwung(phase(t, .3 + i * .2, .8 + i * .2))
        if u <= 0:
            continue
        wip = 8 * math.sin(t * 2.2 + i)
        sprite(e, name, t + i * .3, x, 330 + wip, 220 * u, ein)
        mct(e, x, 466, "§a" + segen, 2, ein * min(1, u), anker="m")
        mct(e, x, 496, "§d" + str(preis) + " Mana", 2, ein * min(1, u), anker="m")
    zeilen = chatzeilen([
        (7.2, "§2Forestling§7: §f" + L("Mein Segen heißt Himmelsprung. Sehr hohe Sprungkraft – damit springst du "
                                       "über Lücken zwischen Inseln.",
                                       "My blessing is called Sky Leap. A huge jump boost – so you can jump the gaps "
                                       "between islands.")),
        (8.6, "§2Forestling§7: §f" + L("Er kostet 20 Mana, du hast 57. Magst du ihn? Dann sag einfach „ja“.",
                                       "It costs 20 Mana, you have 57. Want it? Then just say “yes”.")),
        (10.4, L("§7Du → Forestling: §fja", "§7You → Forestling: §fyes")),
        (11.0, "§a" + L("Himmelsprung! §7Für 120 s springst du so hoch wie nie.", "Sky Leap! §7For 120 s you jump higher than ever.")),
    ])
    chat(e, 880, 830, zeilen, t, 3, ein)
    if t >= 11.0:
        funkenkranz(e, 970, 330, t, 11.0, radius=120, farbe=(160, 255, 160))


def szene_ki(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    sprite_boden(e, "goblin_idle", t, 1080, 520, 260, ein)
    s = 1 + .08 * math.sin(math.pi * phase(t, .6, 1.2))
    b = mc.text_bild("§fPip §b(KI)", 6)
    mc.einfuegen(e, Image.new("RGBA", (int(b.width * s), int(70 * s)), (0, 0, 0, 110)), 1080 - b.width * s / 2, 200, ein)
    skaliert(e, b, 1080, 236, b.width * s, b.height * s, alpha=ein)
    u = aus_kubisch(phase(t, 1.0, 1.4))
    eintraege = [L("§7Spieler", "§7Players"), "§fLena", "§fTom", "", "§#5CE1E6Bewohner (KI)",
                 L("§fPip §7– Wald, 212 / -88", "§fPip §7– Forest, 212 / -88"),
                 L("§fMoss §7– Sumpf, -340 / 410", "§fMoss §7– Swamp, -340 / 410")]
    eintraege[4] = L("§bBewohner (KI)", "§bResidents (KI)")
    tablist(e, 1330, 220, eintraege, 4, ein * u)
    befehle = [("/bewohner", L("alle Bewohner, die du kennst", "all residents you know")),
               ("/ki", L("was Bewohner bei dir dürfen", "what residents may do with you")),
               ("/auftraege", L("Aufträge und Lieferungen", "orders and deliveries"))]
    if SPRACHE == "en":
        befehle[0] = ("/residents", befehle[0][1])
        befehle[2] = ("/orders", befehle[2][1])
    for i, (cmd, text) in enumerate(befehle):
        uu = aus_kubisch(phase(t, 2.2 + i * .35, 2.7 + i * .35))
        mc.einfuegen(e, tafel(900, 64, 14), 900, 610 + i * 80, ein * uu)
        mct(e, 924, 628 + i * 80, "§e" + cmd + "  §7" + text, 4, ein * uu)


def szene_outro(e, t, d):
    titelkarte(e, t, L("Bis bald!", "See you soon!"), L("Deine Nachbarn warten schon.", "Your neighbours are waiting."),
               L("megabuild.de  ·  /bewohner  ·  /ki", "megabuild.de  ·  /residents  ·  /ki"), y=120)
    u = rueckschwung(phase(t, .4, .9))
    if u > 0:
        sprite_boden(e, "mala_hello", max(0, t - .9), W / 2 - 240, 800, 300 * u, schleife=False)
        sprite_boden(e, "goblin_hello", max(0, t - 1.2), W / 2 + 220, 800, 260 * u, schleife=False, spiegeln=True)
    a3 = aus_kubisch(phase(t, 1.4, 2.0))
    skaliert(e, WORTMARKE, W / 2, 862, WORTMARKE.width * 2, WORTMARKE.height * 2, alpha=a3)


SZENEN = [
    dict(dauer=5.0, zeichne=szene_intro, ton=[(.2, "sfx:chime"), (.8, "pool:goblin/gruss_2", .6),
                                              (1.1, "pool:shroomling/freude_1", .6), (1.4, "pool:forestling/oak/happy", .6)]),
    dict(dauer=10.0, nr="01", kicker=L("KI-Bewohner", "AI residents"), titel=L("Nachbarn auf den Inseln", "Neighbours on the islands"),
         text=L("Goblins und Shroomlinge wohnen auf den Inseln um dich herum – als Einsiedler oder in kleinen Siedlungen.",
                "Goblins and Shroomlings live on the islands around you – as hermits or in small settlements."),
         zeichne=szene_nachbarn, ton=[(1.0, "mala:resident-more")]),
    dict(dauer=11.0, nr="02", kicker=L("Reden", "Talking"), titel=L("Schreib einfach in den Chat", "Just type in chat"),
         text=L("Auf ihrer Insel geht dein Chat nur an die Bewohner, die du kennst. Mit ! vorn schreibst du an alle.",
                "On their island your chat only goes to residents you know. Start with ! to write to everyone."),
         zeichne=szene_reden, ton=[(.5, "mala:resident-chat")] + [(2.0 + k * .2, "sfx:tippen", .8) for k in range(7)]
         + [(3.6, "sfx:klick"), (4.5, "pool:goblin/ja_1", .6), (7.4, "pool:goblin/freude_2", .6)]),
    dict(dauer=10.0, nr="03", kicker=L("Alltag", "Daily life"), titel=L("Sie arbeiten, ruhen und schlafen",
                                                                  "They work, rest and sleep"),
         text=L("Bewohner hacken, ernten und schmieden an ihrem Posten, machen Pause und schlafen nachts.",
                "Residents chop, harvest and forge at their posts, take breaks and sleep at night."),
         zeichne=szene_alltag, ton=[(.8, "mala:resident-grow")]),
    dict(dauer=9.0, nr="04", kicker=L("Vertrauen", "Trust"), titel=L("Je öfter, desto mehr", "The more you visit"),
         text=L("Mit jedem Besuch kennen sie dich besser: erst reden, dann handeln, später Aufgaben und Aufträge.",
                "With every visit they know you better: first chatting, then trading, later tasks and orders."),
         zeichne=szene_vertrauen, ton=[(2.5, "sfx:pop", .5), (4.0, "sfx:pop", .5), (5.4, "sfx:pop", .5),
                                       (6.6, "pool:goblin/lachen_1", .6)]),
    dict(dauer=8.5, nr="05", kicker=L("Handel", "Trading"), titel=L("Bezahlt wird mit Mana oder Ware",
                                                                  "Pay with Mana or goods"),
         text=L("In der Lagerkiste am Haus oder mit „handeln“ im Chat. Verkaufen bringt Mana bis zu einem Tageslimit.",
                "Use the storage chest by the house or type “trade” in chat. Selling earns Mana up to a daily limit."),
         zeichne=szene_handel, ton=[(.3, "sfx:pop", .5), (6.4, "sfx:klick")]),
    dict(dauer=14.0, nr="06", kicker="Forestlinge", titel=L("Kleine Waldelfen mit Segen", "Little forest elves with blessings"),
         text=L("Forestlinge ziehen von Insel zu Insel. Für etwas Mana schenken sie dir einen Segen – sag einfach „ja“.",
                "Forestlings move from island to island. For a little Mana they grant you a blessing – just say “yes”."),
         zeichne=szene_forestlinge, ton=[(.3, "mala:forest-look"), (3.7, "mala:forest-bless"),
                                         (7.2, "pool:forestling/oak/ambient_1", .6), (11.0, "pool:forestling/oak/bless", .8),
                                         (11.1, "sfx:funkeln", .7)]),
    dict(dauer=8.5, nr="07", kicker=L("Ehrlich", "Honest"), titel=L("„(KI)“ steht dran", "“(KI)” says it all"),
         text=L("Bewohner sind keine Spieler und sagen das auch. Mit /ki stellst du ein, was sie bei dir dürfen.",
                "Residents are not players and say so. Use /ki to set what they may do with you."),
         zeichne=szene_ki, ton=[(.6, "sfx:pop", .5)]),
    dict(dauer=6.0, zeichne=szene_outro, ton=[(.3, "mala:resident-bye"), (1.2, "pool:goblin/tschuess_1", .6)]),
]

FILM = Film("bewohner", SZENEN, musik=dict(tonart="F", tempo=88, stimmung="hell"))
FILM.poster = 5.0 + 10.0 + 11.0 + 6.0
