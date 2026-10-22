#!/usr/bin/env python3
"""Mana, Skilltree & Biome - wie die Inselwelt auf MegaBuild Skyblock waechst.

Zahlen: Standardwerte aus MBSkyManager/src/main/resources/config.yml und
skilltree/SKILLTREE.yml, MBEconomy (Startguthaben) und MBPM (Votes), Stand der
Release vom 12.10.2026. Preis = 100 x 1,05^Kaeufe x (1 + 0,25 x (Stelle - 1)),
auf 5 gerundet. Mana-Erz gibt Kugeln; den Ofen-Golem zum Einzahlen gibt es noch nicht.

    python3 bauen.py skilltree [--sprache en]
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

KRISTALLE = ["biome_snow_cold", "biome_mountains_rocky", "biome_forests_temperate", "biome_plains_open",
             "biome_swamp_rare", "biome_jungle_tropical", "biome_hot_dry", "biome_water"]


def szene_intro(e, t, d):
    titelkarte(e, t, L("Mana & Biome", "Mana & biomes"), L("So wächst deine Inselwelt", "How your island world grows"), y=150)
    n = len(KRISTALLE)
    for i, ic in enumerate(KRISTALLE):
        w = math.pi * (1.1 + .8 * i / (n - 1))
        s = rueckschwung(phase(t, .7 + i * .09, 1.1 + i * .09))
        if s <= 0:
            continue
        x = W / 2 + math.cos(w) * 520
        y = 900 + math.sin(w) * 260 + 8 * math.sin(t * 2 + i)
        icon_bei(e, ic, x - 48 * s, y - 48 * s, int(96 * s), 1.0 if ic != "biome_water" else .45)
    s = rueckschwung(phase(t, 1.4, 1.9))
    if s > 0:
        mc.einfuegen(e, glanz(150, (255, 120, 255), 150), W / 2 - 150, 640 - 150)
        skaliert(e, mc.icon16("mana_orb"), W / 2, 640 + 8 * math.sin(t * 2), 180 * s)


EREIGNISSE = [(1.4, "quests", L("Tagesquest", "Daily quest"), 60), (2.6, "coin", "Vote", 50),
              (3.6, "mining", L("Erz abbauen", "Mining ore"), 2), (4.6, "biome", "Biomquest", 25),
              (5.6, "combat", L("Monster", "Monster"), 1), (6.4, "quest_weekly", L("Wochenquest", "Weekly quest"), 310)]


def szene_mana(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    stand = 1000 + sum(wert * aus_kubisch(phase(t, t0 + .5, t0 + 1.0)) for t0, _, _, wert in EREIGNISSE)
    ruby = 0 + aus_kubisch(phase(t, 3.1, 3.6))
    mc.einfuegen(e, tafel(620, 260, 22), 1030, 560, ein)
    mana_ruby(e, 1610, 610, stand, ruby, 8, ein)
    mct(e, 1060, 600, L("§7unten rechts", "§7bottom right"), 3, ein)
    mct(e, 1060, 640, L("§7im Spiel", "§7in game"), 3, ein)
    for i, (t0, ic, name, wert) in enumerate(EREIGNISSE):
        u = phase(t, t0, t0 + 1.0)
        if 0 < u < 1:
            a = ein * min(1, u * 5) * (1 - phase(u, .75, 1))
            x = 960 + (i % 3) * 300
            y = 470 - 140 * aus_kubisch(u)
            icon_bei(e, ic, x, y, 56, a)
            mct(e, x + 70, y + 6, "§d+" + str(wert) + " Mana", 4, a)
            mct(e, x + 70, y + 46, "§7" + name, 3, a)


QUELLEN = [("quests", L("Tagesquests", "Daily quests"), L("leicht, mittel, schwer", "easy, medium, hard"), "15–90 Mana"),
           ("quest_weekly", L("Wochenquest", "Weekly quest"), L("Montag bis Montag", "Monday to Monday"), "250–400 Mana"),
           ("quest_bonus", L("Bonusquest", "Bonus quest"), L("Woche in 3 Tagen geschafft", "week done within 3 days"),
            "120–180 Mana"),
           ("coin", "Votes", L("jeder Vote zählt", "every vote counts"), "50 Mana + 5 Ruby"),
           ("biome", "Biomquest", L("je Helfer, der Mitglied ist", "per helper who is a member"), "25 Mana"),
           ("mining", L("Aktionen", "Actions"), L("Erz, Kampf, Angeln, Zähmen …", "ore, combat, fishing, taming …"),
            L("bis 150 Mana/Tag", "up to 150 Mana/day"))]


def szene_verdienen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    x0, y0, rh = 880, 190, 104
    for i, (ic, name, unter, wert) in enumerate(QUELLEN):
        u = aus_kubisch(phase(t, .2 + i * .3, .7 + i * .3))
        y = y0 + i * rh
        dx = (1 - u) * 40
        mc.einfuegen(e, tafel(960, 92, 16), x0 + dx, y, ein * u)
        icon_bei(e, ic, x0 + 22 + dx, y + 14, 64, ein * u)
        mct(e, x0 + 110 + dx, y + 16, "§f" + name, 4, ein * u)
        mct(e, x0 + 110 + dx, y + 58, "§7" + unter, 3, ein * u)
        mct(e, x0 + 930 + dx, y + 30, "§d" + wert, 4, ein * u, anker="r")


def szene_erz(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    cx, cy = 1180, 470
    zerbrochen = t >= 4.0
    if not zerbrochen:
        wackel = 10 * math.sin(t * 40) * (phase(t, 2.8, 3.0) - phase(t, 3.8, 4.0))
        mc.einfuegen(e, glanz(260, (255, 90, 230), 110 + int(40 * math.sin(t * 3))), cx - 260, cy - 260, ein)
        sprite(e, "mana_erz", t * .6, cx + wackel, cy, 420, ein)
    else:
        u = phase(t, 4.0, 4.4)
        mc.einfuegen(e, glanz(260, (255, 90, 230), int(150 * (1 - u))), cx - 260, cy - 260, ein)
        rnd = random.Random(4)
        for k in range(5):
            w = rnd.uniform(-math.pi, 0)
            v = rnd.uniform(260, 420)
            tt = t - 4.0
            x = cx + math.cos(w) * v * min(tt, 1.0) * .8
            y = cy + math.sin(w) * v * min(tt, 1.0) + 420 * max(0, min(tt, 1.0)) ** 2
            y = min(y, cy + 150)
            skaliert(e, mc.icon16("mana_orb"), x, y + 6 * math.sin(t * 4 + k), 80, alpha=ein)
        mct(e, cx, cy - 250, "§d+5 " + L("Mana-Kugeln", "Mana orbs"), 5, ein * aus_kubisch(phase(t, 4.3, 4.7)), anker="m")
    for i, txt in enumerate((L("§7Nur mit §fSpitzhacke §7– jede ist gleich schnell", "§7Pickaxe only §7– every pickaxe is equally fast"),
                             L("§7Mit §fGlück §7mehr Kugeln, bis §f200 §7am Tag", "§7More orbs with §fFortune§7, up to §f200 §7a day"),
                             L("§7Einzahlen beim §fOfen-Golem §7– folgt noch", "§7Deposit at the §fFurnace Golem §7– coming later"))):
        u = aus_kubisch(phase(t, 1.0 + i * .5, 1.5 + i * .5))
        mct(e, 900, 700 + i * 46, txt, 4, ein * u)
    icon_bei(e, "mining", 1460, 300, 96, ein * (phase(t, 2.5, 2.8) - phase(t, 3.9, 4.1)))


PFAD = [(10, "biome_forests_temperate"), (11, "quests"), (12, "locked"), (13, "locked"), (14, "locked"), (15, "locked")]


def szene_baum(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    slots = dict(PFAD)
    slots.update({27: "back", 30: "page_prev", 31: "biome_forests_temperate", 32: "page_next", 35: "close"})
    tipps = {
        10: [L("§aWald §2✔", "§aForest §2✔"), L("§7Startbiom deiner Insel", "§7Your island's start biome")],
        11: [L("§fBewaldete Hügel", "§fWooded Hills"), L("§7Erst die Biomquest von §fWald§7:", "§7First Forest's biome quest:"),
             L("§fFälle 48 Eichenstämme §7(12/48)", "§fChop 48 oak logs §7(12/48)"), L("§7Danach: §d125 Mana", "§7Then: §d125 Mana")],
        12: [L("§fTaiga", "§fTaiga"), L("§7Erst §fBewaldete Hügel §7kaufen", "§7Buy §fWooded Hills §7first")],
        31: [L("§aKristall Wälder", "§aForests crystal"), L("§7◀ ▶ blättert durch die 8 Pfade", "§7◀ ▶ flip through the 8 paths")],
    }
    halte = [(.6, 1.0, 10), (2.0, 2.4, 11), (4.6, 5.0, 12), (6.4, 6.8, 31)]
    menue_mit_zeiger(e, t, L("§2§lSkilltree · Wälder", "§2§lSkill tree · Forests"), 4, slots, tipps, halte, 880, 240, 4, ein)
    u = rueckschwung(phase(t, .8, 1.3))
    if u > 0:
        schatten(e, 1100, 860, 160 * u, .6 * ein)
        sprite_boden(e, "golem_idle", t, 1100, 860, 220 * u, ein)
        mct(e, 1240, 760, L("§7Auch beim §fGolem", "§7Also at the §fgolem"), 3, ein * min(1, u))
        mct(e, 1240, 800, L("§7auf dem Luftschiff", "§7on the airship"), 3, ein * min(1, u))


HELFER = [("head_1", "Lena", 20), ("head_2", "Tom", 16), ("head_3", "Mia", 12)]


def szene_biomquest(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    p = ein_aus(phase(t, .8, 5.0))
    n = int(round(12 + 36 * p))
    text = L("§fEichenstämme ", "§fOak logs ") + ("§a" if n >= 48 else "§f") + str(n) + "§7/§f48"
    hud_kasten(e, 1020, 160, "hud_icon_quest_mining", text, 5, ein, balken=n / 48)
    if n >= 48:
        skaliert(e, mc.hud_bild("hud_icon_quest_done"), 1020 + 9 * 5, 160 + 8 * 5, 45, alpha=ein)
        funkenkranz(e, 1330, 210, t, 5.0, radius=230, n=8)
    for i, (kopf, name, anteil) in enumerate(HELFER):
        x = 1030 + i * 260
        u = aus_kubisch(phase(t, .4 + i * .15, .9 + i * .15))
        icon_bei(e, kopf, x, 330, 96, ein * u)
        mct(e, x + 48, 440, "§f" + name, 3, ein * u, anker="m")
        mct(e, x + 48, 478, "§e" + str(int(round(anteil * p))) + L(" §7Stämme", " §7logs"), 3, ein * u, anker="m")
    zeilen = chatzeilen([
        (5.2, L("§aBiomquest geschafft: §fFälle 48 Eichenstämme§a. §fBewaldete Hügel §aist jetzt kaufbar.",
                "§aBiome quest done: §fChop 48 oak logs§a. §fWooded Hills §acan now be bought.")),
        (5.21, L("§7Dabei: §fLena, Tom, Mia", "§7Helpers: §fLena, Tom, Mia")),
        (6.2, "§d+25 Mana §7" + L("für jeden Helfer, der Mitglied der Insel ist", "for every helper who is an island member")),
    ])
    chat(e, 880, 800, zeilen, t, 3, ein)


BIOMFARBEN = {
    "wald": ((70, 140, 50), (90, 165, 62)), "huegel": ((60, 120, 45), (80, 140, 55)),
    "ebene": ((110, 180, 70), (130, 200, 80)), "schnee": ((235, 240, 245), (215, 225, 235)),
    "wueste": ((220, 200, 130), (235, 215, 150)),
}


def szene_gegenden(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    raster = [("wald", 0), ("wald", 1), ("ebene", 2), ("wald", 3), ("wald", 4), ("huegel", 5), ("wald", 6), ("ebene", 7)]
    for i, (biom, seed) in enumerate(raster):
        x = 920 + (i % 4) * 230
        y = 300 + (i // 4) * 240
        u = rueckschwung(phase(t, .3 + i * .35, .75 + i * .35))
        if u <= 0:
            continue
        gras, hell = BIOMFARBEN[biom]
        bild = insel_bild(11, 4, 30 + seed, 14, gras=gras, gras_h=hell, baum=biom != "ebene")
        neu = biom == "huegel"
        if neu:
            mc.einfuegen(e, glanz(130, (140, 255, 160), 120), x + bild.width / 2 - 130, y + 40 - 130, ein)
        skaliert(e, bild, x + bild.width / 2, y + 50, bild.width * u, bild.height * u, alpha=ein)
        if neu and t > 2.5:
            uu = aus_kubisch(phase(t, 2.5, 2.9))
            mct(e, x + bild.width / 2, y - 60, L("§aNeu: Bewaldete Hügel", "§aNew: Wooded Hills"), 3, ein * uu, anker="m")
            funkenkranz(e, x + bild.width / 2, y + 40, t, 2.3, radius=110, n=6, farbe=(160, 255, 170))
    if t > 4.8:
        for k, i in enumerate((0, 6)):
            x = 920 + (i % 4) * 230 + 77
            y = 300 + (i // 4) * 240 - 30
            s = rueckschwung(phase(t, 4.8 + k * .3, 5.2 + k * .3))
            if s > 0:
                skaliert(e, mc.icon16("star"), x, y, 56 * s, alpha=ein)
        u = aus_kubisch(phase(t, 5.4, 5.9))
        mct(e, 920, 800, L("§e★ Lieblinge: §fbis zu 3 Biome erscheinen 3× so oft", "§e★ Favourites: §fup to 3 biomes appear 3× as often"),
            4, ein * u)


PREISE = [(1, 100), (5, 120), (10, 155), (20, 255), (30, 410), (39, 640)]


def szene_preise(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    x0, y0, hmax = 940, 700, 420
    mc.einfuegen(e, Image.new("RGBA", (860, 3), (255, 255, 255, 60)), x0 - 20, y0 + 2, ein)
    for i, (kauf, preis) in enumerate(PREISE):
        u = ein_aus(phase(t, .3 + i * .25, 1.1 + i * .25))
        h = hmax * preis / 640 * u
        x = x0 + i * 140
        if h > 1:
            mc.einfuegen(e, tafel(84, max(20, int(h)), 10, (201, 133, 255, 230), (255, 255, 255, 40)), x, y0 - h, ein)
        mct(e, x + 42, y0 - h - 44, "§d" + str(preis), 4, ein * min(1, u * 2), anker="m")
        mct(e, x + 42, y0 + 20, "§7" + L("Kauf ", "buy ") + str(kauf), 3, ein, anker="m")
    u = aus_kubisch(phase(t, 2.6, 3.1))
    mct(e, 920, 200, L("§fPreis an Stelle 1 eines Pfads, in Mana", "§fPrice at step 1 of a path, in Mana"), 4, ein * u)
    mct(e, 920, 790, L("§7+25 % je Stelle im Pfad · gerundet auf 5", "§7+25 % per step in the path · rounded to 5"), 3, ein * u)
    mct(e, 920, 832, L("§7Alle 39 Käufe zusammen: §drund 20 900 Mana", "§7All 39 purchases together: §daround 20,900 Mana"),
        3, ein * aus_kubisch(phase(t, 3.6, 4.1)))


def szene_outro(e, t, d):
    titelkarte(e, t, L("Viel Spaß beim Wachsen!", "Have fun growing!"), "/sky skills  ·  /quest",
               L("47 Biome in 8 Pfaden – Gewässer kommt bald", "47 biomes in 8 paths – Water is coming soon"), y=150)
    u = rueckschwung(phase(t, .5, 1.0))
    if u > 0:
        sprite_boden(e, "golem_idle", t, W / 2 - 200, 820, 240 * u)
        skaliert(e, mc.icon16("mana_orb"), W / 2 + 200, 720 + 8 * math.sin(t * 2), 140 * u)
    a3 = aus_kubisch(phase(t, 1.4, 2.0))
    skaliert(e, WORTMARKE, W / 2, 900, WORTMARKE.width * 2, WORTMARKE.height * 2, alpha=a3)


SZENEN = [
    dict(dauer=5.0, zeichne=szene_intro, ton=[(.2, "sfx:chime"), (1.4, "sfx:funkeln", .7)]),
    dict(dauer=9.0, nr="01", kicker="Mana", titel=L("Mana ist deine Magie", "Mana is your magic"),
         text=L("Damit schaltest du neue Biome frei. Du startest mit 1 000 Mana – unten rechts siehst du deinen Stand.",
                "It unlocks new biomes. You start with 1,000 Mana – your balance sits at the bottom right."),
         zeichne=szene_mana, ton=[(t0 + .5, "sfx:pop", .45) for t0, *_ in EREIGNISSE]),
    dict(dauer=10.0, nr="02", kicker=L("Mana verdienen", "Earning Mana"), titel=L("Quests, Votes und Abenteuer",
                                                                                "Quests, votes and adventures"),
         text=L("Quests bringen am meisten. Dazu kommen Votes, Biomquests und viele kleine Aktionen – aus Aktionen bis 150 "
                "Mana am Tag.",
                "Quests earn the most. Add votes, biome quests and lots of small actions – up to 150 Mana a day from actions."),
         zeichne=szene_verdienen, ton=[(.2 + i * .3, "sfx:klick", .6) for i in range(6)]),
    dict(dauer=8.5, nr="03", kicker=L("Mana-Erz", "Mana ore"), titel=L("Leuchtende Adern", "Glowing veins"),
         text=L("Tief in den Höhlen der Hauptinseln: Mana-Erz lässt Mana-Kugeln fallen. Die Startinsel hat keins.",
                "Deep in the caves of main islands: Mana ore drops Mana orbs. Your starting island has none."),
         zeichne=szene_erz, ton=[(2.9, "sfx:klick"), (3.3, "sfx:klick"), (3.7, "sfx:klick"), (4.0, "sfx:funkeln"),
                                 (4.05, "sfx:pop", .6)]),
    dict(dauer=11.0, nr="04", kicker="Skilltree", titel=L("Acht Kristalle, acht Pfade", "Eight crystals, eight paths"),
         text=L("Jeder Pfad führt von links nach rechts durch seine Biome. Öffne ihn mit /sky skills auf deiner Insel.",
                "Each path leads left to right through its biomes. Open it with /sky skills on your island."),
         zeichne=szene_baum, ton=[(.6, "mala:golem"), (1.0, "pool:command_golem/beep_1", .6)]),
    dict(dauer=10.0, nr="05", kicker="Biomquest", titel=L("Erst die Quest, dann das Biom", "First the quest, then the biome"),
         text=L("Alle auf der Insel helfen mit. Ist die Biomquest geschafft, wird das nächste Biom des Pfads kaufbar.",
                "Everyone on the island helps. Once the biome quest is done, the next biome of the path can be bought."),
         zeichne=szene_biomquest, ton=[(5.0, "sfx:erfolg"), (6.2, "sfx:pop", .5)]),
    dict(dauer=9.0, nr="06", kicker=L("Neue Gegenden", "New regions"), titel=L("Dein Biom taucht auf", "Your biome appears"),
         text=L("Ein frisch gekauftes Biom erscheint sicher in der nächsten neuen Gegend, die du erkundest.",
                "A freshly bought biome is sure to appear in the next new region you explore."),
         zeichne=szene_gegenden, ton=[(2.3, "sfx:funkeln"), (4.8, "sfx:pop", .5), (5.1, "sfx:pop", .5)]),
    dict(dauer=8.0, nr="07", kicker=L("Preise", "Prices"), titel=L("Fair gestaffelt", "Fairly staged"),
         text=L("Das erste Biom kostet 100 Mana. Jeder Kauf macht die nächsten ein wenig teurer.",
                "Your first biome costs 100 Mana. Each purchase makes the next ones a little pricier."),
         zeichne=szene_preise),
    dict(dauer=5.5, zeichne=szene_outro, ton=[(.3, "sfx:chime", .8)]),
]

FILM = Film("skilltree", SZENEN, musik=dict(tonart="G", tempo=92, stimmung="hell"))
FILM.poster = 5.0 + 9.0 + 10.0 + 8.5 + 6.5
