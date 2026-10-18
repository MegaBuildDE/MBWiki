#!/usr/bin/env python3
"""Dein Start auf MegaBuild Skyblock - von der Lobby bis zum ersten Bewohner.

Stand der Spielinhalte: Release vom 12.10.2026 (MBSkyConnector, MBSkyIntro,
MBSkyManager). Malas Stimme und Untertitel sind die echten Aufnahmen aus dem Pool
(assets/sounds/mala, Texte aus story/voice-lines.yml). Chatzeilen sind die
Sprachdateien des Spiels, gekuerzt wo noetig.

    python3 bauen.py start [--sprache en]
"""
import functools
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

FOTO_EINS = os.path.join(WIKI, ".gitbook", "assets", "mb-skyblock-one.jpg")
FOTO_DREI = os.path.join(WIKI, ".gitbook", "assets", "mb-skyblock-three.jpg")
PIP = "§fPip §b(KI)§7: §f"


def szene_intro(e, t, d):
    titelkarte(e, t, L("Dein Start", "Your start"), L("auf MegaBuild Skyblock", "on MegaBuild Skyblock"),
               L("Von der Lobby bis zur eigenen Insel", "From the lobby to your own island"), y=150)
    s = rueckschwung(phase(t, .8, 1.3))
    if s > 0:
        schatten(e, W / 2, 900, 220 * s, .8)
        if t < 1.3:
            sprite_boden(e, "mala_idle", t, W / 2, 900, 360 * s)
        else:
            sprite_boden(e, "mala_hello", t - 1.3, W / 2, 900, 360, schleife=False)
    funkenkranz(e, W / 2, 740, t, 1.0, radius=170)


def szene_verbinden(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    for i, (ic, titel, port) in enumerate((("world", "§aJava Edition", L("§7Port: §fStandard", "§7Port: §fdefault")),
                                           ("connect", "§bBedrock Edition", "§7Port: §f19132"))):
        u = rueckschwung(phase(t, .2 + i * .25, .7 + i * .25))
        if u > 0:
            x = 880 + i * 480
            karte(e, x, 200, 450, 190, ic, titel, [L("§7Adresse: §fmegabuild.de", "§7Address: §fmegabuild.de"), port],
                  alpha=ein * min(1, u))
    eingabe = "§f" + tippen("/sky", t, 1.7, 2.5) + ("_" if int(t * 3) % 2 == 0 and t < 2.9 else "")
    if t < 2.9:
        chat(e, 880, 800, [], t, 3, ein, eingabe)
    if t >= 2.9:
        u = aus_kubisch(phase(t, 2.9, 3.25))
        slots = {11: "create_world", 13: "island", 15: "shared", 20: "settings", 22: "friends", 24: "stats"}
        tipps = {11: [L("§a§lSkyblock erstellen", "§a§lCreate Skyblock"), L("§7Startbiom wählen", "§7Pick a start biome"),
                      L("§7und losfliegen", "§7and take off")],
                 13: [L("§a§lInsel betreten", "§a§lJoin Island"), L("§7Zu deiner Insel reisen", "§7Travel to your island")]}
        menue_mit_zeiger(e, t - 2.9, "§b§lSkyblock", 3, slots, tipps, [(.5, 1.0, 13), (1.6, 2.0, 11)], 900, 450, 4, u)
        klick(e, t - 2.9, 2.4, *slot_mitte(11, 900, 450, 4), alpha=u)


BIOME = [  # Slot, Icon, Name, Startinsel, Text
    (10, "biome_plains_open", L("§aEbenen", "§aPlains"), L("Ebene", "Plains"),
     L("Weite Wiesen und Sonnenblumen.", "Wide meadows and sunflowers.")),
    (11, "biome_forests_temperate", L("§2Wälder", "§2Forests"), L("Wald", "Forest"),
     L("Dichte Laub- und Nadelwälder.", "Dense broadleaf and conifer woods.")),
    (12, "biome_snow_cold", L("§bSchnee & Eis", "§bSnow & Ice"), L("Verschneite Ebene", "Snowy Plains"),
     L("Frostige Ebenen und Gletscher.", "Frosty plains and glaciers.")),
    (13, "biome_hot_dry", L("§eWüste & Steppe", "§eDesert & Steppe"), L("Wüste", "Desert"),
     L("Sand, Hitze und Badlands.", "Sand, heat and badlands.")),
    (14, "biome_jungle_tropical", L("§aDschungel", "§aJungle"), L("Lichter Dschungel", "Sparse Jungle"),
     L("Tropisch, grün und voller Leben.", "Tropical, green and full of life.")),
    (15, "biome_mountains_rocky", L("§7Gebirge", "§7Mountains"), L("Windschliff-Hügel", "Windswept Hills"),
     L("Schroffe Gipfel und Geröll.", "Rugged peaks and scree.")),
    (16, "biome_swamp_rare", L("§5Sumpf & Selten", "§5Swamp & Rare"), L("Sumpf", "Swamp"),
     L("Moorige und ungewöhnliche Biome.", "Boggy and unusual biomes.")),
]


def szene_startbiom(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    slots = {s: ic for s, ic, *_ in BIOME}
    slots[22] = "biome_water"
    tipps = {s: [name, L("§7Startinsel: §f", "§7Start island: §f") + insel, "§7" + text]
             for s, ic, name, insel, text in BIOME}
    tipps[22] = [L("§9Gewässer", "§9Water"), L("§eBald verfügbar", "§eComing soon")]
    halte = [(.6, 1.1, 10), (1.9, 2.3, 11), (3.2, 3.6, 13), (4.5, 4.9, 22), (6.1, 6.5, 11)]
    menue_mit_zeiger(e, t, L("§d§lStartbiom wählen", "§d§lChoose start biome"), 3, slots, tipps, halte, 880, 330, 4, ein)
    klick(e, t, 7.0, *slot_mitte(11, 880, 330, 4), alpha=ein)
    if t >= 7.05:
        u = rueckschwung(phase(t, 7.05, 7.5))
        b = mc.text_bild(L("§a✔ Wälder gewählt", "§a✔ Forests chosen"), 5)
        skaliert(e, b, 880 + 352, 720, b.width * u, b.height * u, alpha=ein)
        funkenkranz(e, 880 + 352, 720, t, 7.05, radius=240, n=8)


def wolken_vorne(e, t, alpha=1.0):
    """Schnelle Wolkenfetzen fuer das Fluggefuehl."""
    for i, (y, tempo, z) in enumerate(((310, 260, 14), (700, 340, 18), (520, 210, 11))):
        b = WOLKEN_BILDER[i % len(WOLKEN_BILDER)]
        b2 = b.resize((b.width * z // 12, b.height * z // 12), Image.NEAREST)
        x = 1900 - (t * tempo + i * 420) % 1300
        mc.einfuegen(e, b2, x, y, .8 * alpha)


def szene_vorspann(e, t, d):
    ein = aus_kubisch(phase(t, 0, .5))
    schiff = luftschiff_bild(16, 8)
    wip = 10 * math.sin(t * 1.3)
    x0, y0 = CX - schiff.width / 2, 170 + wip
    mc.einfuegen(e, schiff, x0, y0, ein)
    deck = y0 + 19 * 16
    sprite_boden(e, "mala_idle", t, CX - 30, deck + 4, 230, ein)
    sprite_boden(e, "warpett_idle", t, CX + 150, deck + 4, 130, ein)
    wolken_vorne(e, t, ein)


def szene_insel(e, t, d):
    ein = aus_kubisch(phase(t, 0, .5))
    w, h = 900, 560
    ken_burns(e, FOTO_EINS, 900, 200, w, h, t, d, alpha=ein)
    if t > 5.4:
        u = aus_kubisch(phase(t, 5.4, 6.2))
        ken_burns(e, FOTO_DREI, 900, 200, w, h, t - 5.4, d - 5.4, alpha=ein * u)
    schiff = luftschiff_bild(6, 5)
    sx = 900 + w - 260 - 20 * phase(t, 0, d)
    mc.einfuegen(e, schiff, sx, 230 + 6 * math.sin(t * 1.4), ein * .95)


def szene_warpett(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    y_boden = 770
    mc.einfuegen(e, insel_bild(26, 6, 41, 18, baum=False), CX - 26 * 18 / 2, y_boden - 18, ein)
    if t < 5.3:
        sprite_boden(e, "warpett_idle", t, CX + 60, y_boden, 380, ein)
    elif t < 8.6:
        sprite_boden(e, "warpett_eat", t - 5.3, CX + 60, y_boden, 380, ein, schleife=False)
    else:
        sprite_boden(e, "warpett_idle", t, CX + 60, y_boden, 380, ein)
    # Loewenzahn: erscheint, schwebt, fliegt zum Maul
    if 1.0 <= t < 5.5:
        s = rueckschwung(phase(t, 1.0, 1.4))
        u = ein_aus(phase(t, 4.4, 5.3))
        x = 960 + (CX - 40 - 960) * u
        y = 420 + 8 * math.sin(t * 3) + (560 - 420) * u - 120 * math.sin(math.pi * u)
        skaliert(e, LOEWENZAHN, x, y, 13 * 10 * s * (1 - .5 * u), 13 * 10 * s * (1 - .5 * u), alpha=ein)
    # Verschluckt: kurz schwarz, dann Ankunft
    if 7.5 <= t < 9.3:
        r = 560 * ein_aus(phase(t, 7.5, 8.1)) if t < 8.6 else 560 * (1 - ein_aus(phase(t, 8.7, 9.3)))
        if r > 4:
            mc.einfuegen(e, _iris(int(r)), CX + 60 - r, 560 - r, ein)
    if t >= 8.9:
        u = aus_kubisch(phase(t, 8.9, 9.4))
        b = mc.text_bild(L("§aAngekommen auf deiner Startinsel", "§aArrived on your starting island"), 4)
        mc.einfuegen(e, b, CX - b.width / 2, 210, ein * u)
    for i, txt in enumerate((L("§7Java: §fRechts- oder Linksklick", "§7Java: §fright or left click"),
                             L("§7Bedrock: §fdaneben schleichen", "§7Bedrock: §fsneak next to it"))):
        u = aus_kubisch(phase(t, 1.6 + i * .3, 2.1 + i * .3)) * (1 - phase(t, 7.2, 7.6))
        mct(e, 900, 180 + i * 40, txt, 3, ein * u)


@functools.lru_cache(maxsize=64)
def _iris(r):
    """Schwarze Scheibe mit weichem Rand (das Warpett hat dich verschluckt)."""
    k = 2
    img = Image.new("L", (2 * r * k // 4 + 1, 2 * r * k // 4 + 1), 0)
    ImageDraw.Draw(img).ellipse((r * k * .05, r * k * .05, img.width - r * k * .05, img.height - r * k * .05), fill=255)
    img = img.filter(ImageFilter.GaussianBlur(max(1, r * k / 60))).resize((2 * r, 2 * r), Image.BILINEAR)
    out = Image.new("RGBA", (2 * r, 2 * r), (2, 2, 8, 0))
    out.putalpha(img)
    return out


def szene_sonderquest(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    meter = int(round(112 - 104 * ein_aus(phase(t, 1.0, 7.2))))
    hud_kasten(e, 1180, 150, "hud_icon_quest_pfeil_vorn", "§f" + str(meter) + " m", 6, ein)
    # Startinsel links, Nachbarinsel rechts, Rankentreppe dazwischen
    links = insel_bild(16, 6, 12, 14)
    rechts = insel_bild(12, 5, 77, 14)
    lx, ly = 900, 610 + 6 * math.sin(t * .8)
    rx, ry = 1440, 470 + 6 * math.sin(t * .8 + 1)
    mc.einfuegen(e, links, lx, ly - 6 * 14, ein)
    mc.einfuegen(e, rechts, rx, ry - 6 * 14, ein)
    blatt = Image.new("RGBA", (28, 14), (70, 140, 60, 255))
    for k in range(12):
        u = k / 11
        bx = lx + links.width - 30 + (rx - lx - links.width + 50) * u
        by = ly + (ry - ly) * u + 18 - 30 * math.sin(math.pi * u)
        mc.einfuegen(e, blatt, bx, by, ein * (1 if k % 2 else .85))
    leuchtfeuer(e, rx + rechts.width / 2, ry + 10, 330, t, ein)
    sprite_boden(e, "goblin_idle", t, rx + rechts.width / 2 + 40, ry + 4, 120, ein)
    # Hilfsgeist: ein blaues Licht fliegt den Weg voraus
    u = phase(t, 1.2, 7.2)
    gx = lx + 120 + (rx + 60 - lx - 120) * ein_aus(u)
    gy = ly - 70 + (ry - ly) * ein_aus(u) - 60 * math.sin(math.pi * u) + 10 * math.sin(t * 5)
    mc.einfuegen(e, glanz(46, (140, 220, 255), 200), gx - 46, gy - 46, ein)
    funkeln(e, gx, gy, 12, ein, (220, 245, 255))
    text = L("§bSonderquest: §7Auf einer Nachbarinsel ist jemand eingezogen – im §fNordosten§7. "
             "Folge dem Pfeil im Questkasten und dem Hilfsgeist – auf der Insel steht ein Leuchtfeuer.",
             "§bSpecial quest: §7Someone has moved onto a neighbouring island – to the §fnortheast§7. "
             "Follow the arrow in the quest box and the helper spirit – there's a beacon on the island.")
    chat(e, 880, 870, chatzeilen([(.5, text)]), t, 3, ein)


def szene_begegnung(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    y_boden = 640
    mc.einfuegen(e, insel_bild(36, 6, 5, 16, baum=False), CX - 36 * 8, y_boden - 16, ein)
    if t < 1.0:
        a = phase(t, .3, 1.0)
        funkenkranz(e, CX - 170, y_boden - 120, t, .3, radius=90, farbe=(255, 120, 255))
    else:
        a = 1
    if 1.0 <= t < 2.5:
        sprite_boden(e, "mala_hello", t - 1.0, CX - 170, y_boden, 300, ein * a, schleife=False)
    else:
        sprite_boden(e, "mala_idle", t, CX - 170, y_boden, 300, ein * a)
    if 4.6 <= t < 6.1:
        sprite_boden(e, "goblin_hello", t - 4.6, CX + 190, y_boden, 260, ein, schleife=False)
    elif t >= 9.4:
        sprite_boden(e, "goblin_talk", t - 9.4, CX + 190, y_boden, 260, ein)
    else:
        sprite_boden(e, "goblin_idle", t, CX + 190, y_boden, 260, ein)
    namensschild(e, CX + 190, y_boden - 250, "§fPip §b(KI)", 3, ein)
    namensschild(e, CX - 170, y_boden - 300, "§bMala", 3, ein)
    zeilen = [
        (9.5, PIP + L("Hallo! Ich bin Pip, ich wohne hier. Schön, dich zu sehen!",
                      "Hello! I'm Pip, I live here. Nice to see you!")),
        (10.9, PIP + L("Bist du neu hier oben? Bauen oder erkunden?", "Are you new up here? Building or exploring?")),
    ]
    chat(e, 880, 860, zeilen, t, 3, ein)


def szene_aufgaben(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    karten = [
        ("quests", "§e/quest", [L("§7Tages-, Wochen- und Bonusquests", "§7Daily, weekly and bonus quests"),
                                L("§7bringen das meiste Mana", "§7earn the most Mana")]),
        ("biome_forests_temperate", L("§aBiomquest", "§aBiome quest"),
         [L("§7Wald: §fFälle 48 Eichenstämme", "§7Forest: §fchop 48 oak logs"),
          L("§7danach ist das nächste Biom kaufbar", "§7then the next biome can be bought")]),
        ("biome", "§d/sky skills", [L("§7Skilltree mit 8 Kristall-Pfaden", "§7Skill tree with 8 crystal paths"),
                                    L("§7oder beim Golem auf dem Luftschiff", "§7or at the golem on the airship")]),
    ]
    for i, (ic, titel, zeilen) in enumerate(karten):
        u = aus_kubisch(phase(t, .3 + i * .35, .8 + i * .35))
        karte(e, 870 + (1 - u) * 40, 190 + i * 196, 720, 170, ic, titel, zeilen, alpha=ein * u)
    u = rueckschwung(phase(t, 1.5, 2.0))
    if u > 0:
        schatten(e, 1735, 760, 180 * u, .7 * ein)
        sprite_boden(e, "golem_idle", t, 1735, 760, 260 * u, ein)


def szene_outro(e, t, d):
    titelkarte(e, t, L("Viel Glück!", "Good luck!"), L("Die neue Welt beginnt mit dir.", "The new world begins with you."),
               "megabuild.de  ·  Java & Bedrock", y=120)
    u = rueckschwung(phase(t, .5, 1.0))
    if u > 0:
        sprite_boden(e, "mala_hello", max(0, t - 1.0), W / 2 - 220, 800, 300 * u, schleife=False)
        sprite_boden(e, "warpett_idle", t, W / 2 + 200, 800, 210 * u)
    a3 = aus_kubisch(phase(t, 1.4, 2.0))
    skaliert(e, WORTMARKE, W / 2, 862, WORTMARKE.width * 2, WORTMARKE.height * 2, alpha=a3)


TIPP = [(t, "sfx:tippen", .8) for t in (1.75, 1.95, 2.15, 2.35)]

SZENEN = [
    dict(dauer=5.0, zeichne=szene_intro, ton=[(.2, "sfx:chime"), (1.3, "sfx:funkeln", .7)]),
    dict(dauer=6.5, nr="01", kicker=L("Verbinden", "Connect"), titel=L("Ab auf den Server", "Join the server"),
         text=L("Java und Bedrock spielen zusammen. In der Lobby öffnet /sky das Skyblock-Menü.",
                "Java and Bedrock play together. In the lobby, /sky opens the Skyblock menu."),
         zeichne=szene_verbinden, ton=TIPP + [(2.8, "sfx:klick"), (2.95, "sfx:pop", .6), (5.3, "sfx:klick")]),
    dict(dauer=9.0, nr="02", kicker=L("Startbiom", "Start biome"), titel=L("Wähle deinen Kristall", "Pick your crystal"),
         text=L("Sieben Kristalle bestimmen, womit deine Insel beginnt. Weitere Biome schaltest du später frei – "
                "Gewässer kommt bald.",
                "Seven crystals decide how your island begins. You unlock more biomes later – Water is coming soon."),
         zeichne=szene_startbiom, ton=[(7.0, "sfx:klick"), (7.1, "sfx:chime", .7)]),
    dict(dauer=11.0, nr="03", kicker=L("Der Vorspann", "The intro"), titel=L("Mala nimmt dich mit", "Mala takes you along"),
         text=L("Während deine Insel entsteht, fliegst du mit Kapitänin Mala im Luftschiff los – mit Stimme und Untertiteln.",
                "While your island is being built, Captain Mala flies you there in her airship – with voice and subtitles."),
         zeichne=szene_vorspann, ton=[(.7, "mala:wake"), (5.3, "mala:name")]),
    dict(dauer=11.5, nr="04", kicker=L("Ankunft", "Arrival"), titel=L("Klein – aber nicht allein", "Small – but not alone"),
         text=L("Vorne taucht deine Startinsel auf, mitten zwischen ihren Nachbarn. Darüber ankert das Luftschiff.",
                "Your starting island appears ahead, right among its neighbours. The airship anchors above it."),
         zeichne=szene_insel, ton=[(.6, "mala:island"), (5.9, "mala:anchor")]),
    dict(dauer=12.0, nr="05", kicker="Warpett", titel=L("Löwenzahn pflücken, Warpett füttern",
                                                        "Pick the dandelion, feed the Warpett"),
         text=L("Halt dem Warpett den Löwenzahn hin: Es frisst ihn – und trägt dich gleich mit auf deine Insel.",
                "Hold the dandelion out to the Warpett: it eats it – and carries you straight down to your island."),
         zeichne=szene_warpett, ton=[(.5, "mala:dandelion"), (1.0, "sfx:pop", .5), (5.4, "pool:warpett/eat_1"),
                                     (7.5, "pool:warpett/gulp"), (6.3, "mala:twin"), (9.6, "pool:warpett/happy", .8)]),
    dict(dauer=9.5, nr="06", kicker=L("Sonderquest", "Special quest"), titel=L("Finde den ersten Bewohner",
                                                                             "Find the first resident"),
         text=L("Ein Pfeil im Questkasten, ein Leuchtfeuer und ein Hilfsgeist führen dich über eine Rankentreppe "
                "zur Nachbarinsel.",
                "An arrow in the quest box, a beacon and a helper spirit lead you across a vine staircase to the "
                "neighbouring island."),
         zeichne=szene_sonderquest, ton=[(.5, "sfx:pop", .5), (1.3, "sfx:funkeln", .6), (6.8, "sfx:funkeln", .6)]),
    dict(dauer=12.5, nr="07", kicker=L("Begegnung", "Meeting"), titel=L("Mala stellt dir die Bewohner vor",
                                                                      "Mala introduces the residents"),
         text=L("Auf der Nachbarinsel wartet sie mit deinem ersten Bewohner. Mit ihm schreibst du ganz normal im Chat.",
                "She's waiting on the neighbouring island with your first resident. You talk to them in the normal chat."),
         zeichne=szene_begegnung, ton=[(.3, "sfx:funkeln", .7), (.6, "mala:resident-hello"), (4.4, "mala:resident-meet"),
                                       (4.7, "pool:goblin/gruss_1", .6), (9.5, "pool:goblin/freude_1", .7),
                                       (10.9, "pool:goblin/frage_1", .7)]),
    dict(dauer=10.0, nr="08", kicker=L("Erste Aufgaben", "First tasks"), titel=L("Und dann geht's los", "And off you go"),
         text=L("Quests bringen Mana, die Biomquest deines Startbioms öffnet den nächsten Kauf – und der Golem kennt "
                "alle Pfade.",
                "Quests earn Mana, your start biome's quest unlocks the next purchase – and the golem knows every path."),
         zeichne=szene_aufgaben, ton=[(.8, "mala:golem"), (1.6, "pool:command_golem/greet_1", .6)]),
    dict(dauer=6.5, zeichne=szene_outro, ton=[(.3, "mala:farewell"), (.4, "sfx:chime", .6)]),
]

FILM = Film("start", SZENEN, musik=dict(tonart="D", tempo=80, stimmung="hell"))
FILM.poster = sum(s["dauer"] for s in SZENEN[:7]) + 8.5
