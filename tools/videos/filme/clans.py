#!/usr/bin/env python3
"""Clans auf MegaBuild Skyblock - Vorschau des geplanten Clansystems.

Inhalt nach MBSkyManager/docs/CLANS.md (Stand 12.10.2026). Alles daran ist
Konzept, deshalb steht durchgehend "Vorschau · noch in Planung" im Bild.
Menues, Icons, Schrift und Wappen sind dieselben wie auf der Entscheidungsseite
(echte Pack-Grafiken, clan_icons.py). Erste Fassung: 13.10.2026 fuer die
Beta-Tester; fuers Wiki mit oeffentlichem Untertitel und Discord-Hinweis.

    python3 bauen.py clans
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

import mc  # noqa: E402
from basis import *  # noqa: E402,F401,F403

GRUEN = "#55FF55"
NBW = "§f" + mc.wappen_char(GRUEN, "pilz") + "§aNBW"
MX, MY, MS = 880, 340, 4


INTRO_WAPPEN = [
    ("#55FF55", "pilz"), ("#FF5555", "flamme"), ("#5555FF", "anker"), ("#FFFF55", "sonne"),
    ("#FFAA00", "fuchs"), ("#55FFFF", "welle"), ("#FF55FF", "kristall"), ("#00AA00", "baum"),
    ("#AAAAAA", "wolf"), ("#AA00AA", "mond"), ("#00AAAA", "luftschiff"), ("#FFFFFF", "stern"),
]


def szene_intro(e, t, d):
    S = 22
    titel = "§b§lCLANS"
    p = aus_kubisch(phase(t, 0, .9))
    mct(e, W / 2, 196 - (1 - p) * 26, titel, S, anker="m")
    a2 = aus_kubisch(phase(t, .2, .8))
    av(e, "auf MegaBuild Skyblock", W / 2, 455 + (1 - a2) * 22, 66, "heavy", (255, 255, 255), a2, anker="m")
    a3 = aus_kubisch(phase(t, .5, 1.1))
    av(e, "Ein erster Blick auf das, was kommt", W / 2, 552 + (1 - a3) * 16, 36, "medium",
       (196, 220, 248), a3, anker="m", schatten=.4)
    n, g, gap = len(INTRO_WAPPEN), 104, 22
    x0 = (W - (n * g + (n - 1) * gap)) / 2
    for i, (farbe, motiv) in enumerate(INTRO_WAPPEN):
        t0 = .9 + i * .07
        s = rueckschwung(phase(t, t0, t0 + .42))
        if s <= 0:
            continue
        wip = 6 * math.sin(2 * math.pi * (t * .42 + i * .11))
        wappen_bei(e, farbe, motiv, x0 + i * (g + gap) + g / 2, 770 + wip, g * s)


MOTIV_FOLGE = ["anker", "flamme", "kristall", "wolf", "sonne", "welle", "fuchs", "luftschiff",
               "baum", "stern", "biene", "schwert", "pilz"]
FARB_FOLGE = ["#5555FF", "#FF5555", "#FF55FF", "#AAAAAA", "#FFFF55", "#55FFFF", "#FFAA00", "#00AAAA",
              "#00AA00", "#FFFFFF", "#FFAA00", "#AA0000", GRUEN]
ALLE_MOTIVE = list(mc.clan_icons.MOTIVE)
ALLE_FARBEN = ["#00AA00", "#00AAAA", "#AA0000", "#AA00AA", "#FFAA00", "#AAAAAA", "#555555", "#5555FF",
               "#55FF55", "#55FFFF", "#FF5555", "#FF55FF", "#FFFF55", "#FFFFFF"]
MC_CODE = {"#00AA00": "2", "#00AAAA": "3", "#AA0000": "4", "#AA00AA": "5", "#FFAA00": "6", "#AAAAAA": "7",
           "#555555": "8", "#5555FF": "9", "#55FF55": "a", "#55FFFF": "b", "#FF5555": "c", "#FF55FF": "d",
           "#FFFF55": "e", "#FFFFFF": "f"}


def tippen(text, t, t0, t1):
    n = int(round(len(text) * phase(t, t0, t1)))
    return text[:n]


def szene_gruenden(e, t, d):
    schritt, start = .42, .45
    k = max(0, min(len(MOTIV_FOLGE) - 1, int((t - start) // schritt)))
    motiv, farbe = MOTIV_FOLGE[k], FARB_FOLGE[k]
    fertig = start + (len(MOTIV_FOLGE) - 1) * schritt
    lokal = (t - start) - k * schritt
    puls = 1 + .07 * (1 - aus_kubisch(phase(lokal, 0, .2))) if t >= start else 1
    if t >= fertig:
        puls = 1 + .16 * math.sin(math.pi * phase(t, fertig, fertig + .35))
    ein = aus_kubisch(phase(t, .05, .45))
    wappen_bei(e, farbe, motiv, 1110, 400, 320 * puls * (0.85 + .15 * ein), alpha=ein)
    if t >= fertig:
        for i in range(6):
            w = i / 6 * 2 * math.pi + .4
            u = phase(t, fertig + .05 * i, fertig + .05 * i + .6)
            funkeln(e, 1110 + math.cos(w) * (190 + 40 * u), 400 + math.sin(w) * (190 + 40 * u),
                    18 * math.sin(math.pi * u), math.sin(math.pi * u))
    code = MC_CODE[farbe]
    blink = "§7_" if int(t * 3) % 2 == 0 else ""
    kuerzel = tippen("NBW", t, .5, 1.1)
    name = tippen("Nebelwald", t, 1.25, 2.35)
    a = ein
    mct(e, 1330, 268, "§7Kürzel", 3, a)
    mct(e, 1330, 300, "§" + code + "§l" + kuerzel + (blink if t < 1.15 else ""), 9, a)
    mct(e, 1330, 400, "§7Name", 3, a)
    mct(e, 1330, 432, "§f" + name + (blink if 1.15 <= t < 2.45 else ""), 5, a)
    # Vorschau Tablist
    if t > 2.5:
        u = aus_kubisch(phase(t, 2.5, 2.9))
        zeile = "§f" + mc.wappen_char(farbe, motiv) + "§" + code + "NBW §fLena"
        bw = (mc.breite(zeile) + 4) * 4
        mct(e, 1330, 506, "§7In Tabliste und Chat", 3, u)
        mc.einfuegen(e, Image.new("RGBA", (bw, 40), (0, 0, 0, 120)), 1330, 538, u)
        mct(e, 1338, 542, zeile, 4, u)
    # Wappen-Raster (24) und Farben (14)
    gr, gap = 52, 12
    x0 = CX - (12 * gr + 11 * gap) / 2
    u = aus_kubisch(phase(t, .3, .8))
    mct(e, x0, 628, "§724 Wappen", 3, u)
    for i, m in enumerate(ALLE_MOTIVE):
        x = x0 + (i % 12) * (gr + gap)
        y = 664 + (i // 12) * (gr + gap)
        if m == motiv:
            mc.einfuegen(e, tafel(gr + 14, gr + 14, 8, (255, 255, 255, 60), (255, 255, 255, 230)), x - 7, y - 7, u)
        wappen_bei(e, farbe, m, x + gr / 2, y + gr / 2, gr, alpha=u * (1 if m == motiv else .78))
    mct(e, x0, 812, "§714 Farben", 3, u)
    sw, sg = 44, 10
    for i, fhex in enumerate(ALLE_FARBEN):
        x = x0 + i * (sw + sg)
        rgb = mc.hex_rgb(fhex)
        if fhex == farbe:
            mc.einfuegen(e, tafel(sw + 12, sw + 12, 7, (255, 255, 255, 60), (255, 255, 255, 230)), x - 6, 842, u)
        mc.einfuegen(e, tafel(sw, sw, 6, rgb + (255,), (20, 16, 30, 255)), x, 848, u)


# Clan-Menue (Kap. 4.3); Stufe 5, damit Clan-Insel und Hain schon dazugehoeren
MENUE_CLAN = {4: "wappen:#55FF55:pilz", 10: "member", 12: "clan_quest", 14: "clan_island", 16: "chat",
              19: "clan_level", 21: "trophy", 23: "treasury", 25: "settings", 27: "back", 35: "close"}
TIPPS_CLAN = {
    4: ["§a§lNebelwald", "§7Kürzel §aNBW §7· Stufe §f5", "§7Erfahrung: §f2 610 §7/ §f3 500", "§7Online: §f5 §7von §f12"],
    10: ["§dMitglieder", "§7Anführer, Offiziere, Mitglieder", "§7und Neulinge, jeder mit Rechten", "§7Plätze: §f12 §7von §f20",
         "§8Klick zum Öffnen"],
    12: ["§6Clan-Quests", "§7Wochenauftrag: §fSilber geschafft", "§7Hilferufe offen: §f1", "§7Projekt Hain: §f62 %",
         "§8Klick zum Öffnen"],
    14: ["§aClan-Insel", "§7Eure gemeinsame Insel", "§7Projekte: §f2 §7fertig, §f1 §7läuft", "§8Klick zum Hinreisen"],
    16: ["§bClan-Chat", "§7Schreib §f#Text §7in den Chat", "§7oder schalte mit §f/c §7um", "§8Klick zum Umschalten"],
}
MX, MY, MS = 880, 340, 4


def szene_menue(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    halte = [(.55, 1.0, 4), (2.55, 2.9, 10), (4.55, 4.9, 12), (6.55, 6.9, 14)]
    menue_mit_zeiger(e, t, "§b§lClan Nebelwald", 4, MENUE_CLAN, TIPPS_CLAN, halte, MX, MY, MS, ein)


def szene_chat(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    S = 5
    eintraege = [
        NBW + " §fLena", NBW + " §fTom", "§f" + mc.wappen_char("#FF5555", "flamme") + "§cFLM §fNoah",
        "§fJonas", "§f" + mc.wappen_char("#5555FF", "anker") + "§9ANK §fEmma", NBW + " §fMia",
    ]
    bw = (max(mc.breite(z) for z in eintraege) + 4) * S
    mct(e, CX, 170, "§7Tabliste", 3, ein, anker="m")
    tablist(e, CX - bw / 2, 206, eintraege, S, ein)
    S = 3
    nachricht = "#Wer kommt mit in die Wüste?"
    getippt = tippen(nachricht, t, .7, 2.0)
    gesendet = t >= 2.3
    blink = "_" if int(t * 3) % 2 == 0 else ""
    zeilen = [
        (-1, "§fJonas§7: §fHat jemand Kakteen übrig?"),
        (-1, "§fEmma§7: §fGleich Event am Spawn!"),
        (2.3, NBW + " §fLena§7: §bWer kommt mit in die Wüste?"),
        (3.3, NBW + " §fTom§7: §bBin dabei, komme aus dem Citybuild!"),
        (4.2, NBW + " §fMia§7: §bIch bringe Fackeln mit."),
        (5.3, "§f" + mc.ALARM["blau"] + " §bLena lädt ein: §fAuf der Insel von Lena §a[Hinreisen]"),
    ]
    eingabe = ("§f" + getippt + blink) if not gesendet else ("§f" + blink)
    chat(e, 880, 860, zeilen, t, S, ein, eingabe)
    # Hinweis auf das #
    if .7 <= t < 2.3:
        u = aus_kubisch(phase(t, .75, 1.0))
        av(e, "# vorne = Clan-Chat", 880 + 2 * S, 860 + 18 * S, 26, "demi", (255, 230, 120), u * ein, schatten=.6)


AUFGABEN = [("quest_fishing", "Fische fangen", 140, (85, 255, 255)),
            ("mining", "Erze abbauen", 480, (230, 230, 240)),
            ("combat", "Monster besiegen", 360, (255, 110, 110))]
SCHWELLEN = [(800, "medal_bronze", "Bronze"), (1600, "medal_silver", "Silber"), (2400, "medal_gold", "Gold")]


def szene_auftrag(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    px, py, pw, ph = 890, 186, 880, 714
    mc.einfuegen(e, tafel(pw, ph), px, py, ein)
    icon_bei(e, "clan_quest", px + 30, py + 22, 64, ein)
    mct(e, px + 112, py + 38, "§6§lWochenauftrag", 5, ein)
    mct(e, px + pw - 32, py + 46, "§7noch 4 Tage", 3, ein, anker="r")
    trenner = Image.new("RGBA", (pw - 60, 2), (255, 255, 255, 40))
    mc.einfuegen(e, trenner, px + 30, py + 104, ein)
    p = ein_aus(phase(t, .7, 6.7))
    punkte = 2400 * p
    bx0, bx1, by = px + 50, px + pw - 50, py + 470
    for i, (ic, name, ende, farbe) in enumerate(AUFGABEN):
        y = py + 118 + i * 72
        u = aus_kubisch(phase(t, .2 + i * .12, .6 + i * .12))
        icon_bei(e, ic, px + 34, y, 60, ein * u)
        mct(e, px + 112, y + 16, "§f" + name, 4, ein * u)
        mct(e, px + pw - 40, y + 16, "§e" + str(int(round(ende * p))), 4, ein * u, anker="r")
    mct(e, px + 50, py + 340, "§7Gemeinsamer Topf", 3, ein)
    mct(e, px + pw - 50, py + 340, "§f" + tausender(int(round(punkte))) + " §7/ §f2 400 §7Punkte", 3, ein, anker="r")
    # Teilchen: jeder Beitrag fliegt in den gemeinsamen Topf
    fuell_x = bx0 + (bx1 - bx0) * p
    for i in range(3):
        y_start = py + 118 + i * 72 + 30
        k = 0
        while True:
            t0 = .75 + i * .11 + k * .3
            k += 1
            if t0 > 6.3:
                break
            u = phase(t, t0, t0 + .55)
            if 0 < u < 1:
                sx, sy = px + pw - 130, y_start
                ex, ey = fuell_x, by + 12
                kx, ky = (sx + ex) / 2 + 80, (sy + ey) / 2 - 30
                q = ein_aus(u)
                x = (1 - q) ** 2 * sx + 2 * (1 - q) * q * kx + q * q * ex
                yy = (1 - q) ** 2 * sy + 2 * (1 - q) * q * ky + q * q * ey
                g = 12
                mc.einfuegen(e, Image.new("RGBA", (g, g), AUFGABEN[i][3] + (235,)), x - g / 2, yy - g / 2, ein * (1 - u * .3))
    # Medaillen ueber dem Balken, Namen darunter
    for wert, ic, name in SCHWELLEN:
        mx = bx0 + (bx1 - bx0) * wert / 2400
        erreicht = punkte >= wert - .5
        t_hit = .7 + 6.0 * umkehr_ein_aus(wert / 2400)
        if erreicht:
            s = 1 + .35 * math.sin(math.pi * phase(t, t_hit, t_hit + .35))
            skaliert(e, mc.icon16(ic), mx, by - 50, 88 * s, alpha=ein)
            u = phase(t, t_hit, t_hit + 1.1)
            if 0 < u < 1:
                rechts = wert < 2400
                mct(e, mx + (54 if rechts else -54), by - 66 - 24 * u, "§d+Mana", 3, ein * (1 - u ** 2),
                    anker="l" if rechts else "r")
            mct(e, mx, by + 40, "§f" + name, 3, ein, anker="m")
        else:
            grau = mc.icon16(ic).convert("LA").convert("RGBA")
            skaliert(e, grau, mx, by - 50, 80, alpha=ein * .45)
            mct(e, mx, by + 40, "§8" + name, 3, ein, anker="m")
    breite_gui = int((bx1 - bx0) / 4)
    balken = mc.balken_bild(breite_gui, p, 4, mc.gefaerbt("bar_fill64", (255, 196, 64)))
    mc.einfuegen(e, balken, bx0, by, ein)
    for wert, _, _ in SCHWELLEN[:-1]:
        mx = bx0 + (bx1 - bx0) * wert / 2400
        mc.einfuegen(e, Image.new("RGBA", (4, 24), (20, 16, 30, 200)), mx - 2, by, ein)
    mc.einfuegen(e, trenner, px + 30, py + 572, ein)
    u = aus_kubisch(phase(t, 4.4, 4.9))
    icon_bei(e, "together", px + 34, py + 600, 60, ein * u)
    mct(e, px + 112, py + 606, "§aZusammen-Bonus §f×1,5", 4, ein * u)
    mct(e, px + 112, py + 650, "§7wenn ihr auf derselben Insel spielt", 3, ein * u)


def szene_hilferuf(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    S = 3
    ruf = "§f" + mc.ALARM["gelb"] + " §eLena bittet um Hilfe: §fWüste – 128 Sand §7(40/128) "
    knopf = "§a[Besuchen]"
    zeilen = [
        (-1, "§fEmma§7: §fGleich Event am Spawn!"),
        (.3, ruf + knopf),
        (1.95, "§f" + mc.ALARM["gruen"] + " §7Du reist zur Insel von §fLena§7 …"),
        (5.75, "§f" + mc.ALARM["gruen"] + " §aBiomquest Wüste geschafft!"),
        (6.15, "§f" + mc.ALARM["magenta"] + " §dMana §7für deine Hilfe bei §fLena§7!"),
    ]
    cx0, cy_unten = 880, 800
    chat(e, cx0, cy_unten, zeilen, t, S, ein)
    # Zeiger klickt auf [Besuchen]
    if .8 <= t < 2.3:
        # Zeile des Rufs: zuerst die unterste, ab 1.95 eine hoeher
        hoch = 9 * S
        zeile_y = cy_unten - hoch if t < 1.95 else cy_unten - 2 * hoch
        kx = cx0 + S + (mc.breite(ruf) + mc.breite(knopf) / 2) * S
        ky = zeile_y + 5 * S
        zx, zy = zeigerweg(t, [(.8, kx + 300, ky + 160), (1.45, kx, ky)])
        druck = math.sin(math.pi * phase(t, 1.55, 1.75))
        a = ein * (1 - phase(t, 2.0, 2.3))
        if 1.55 <= t < 2.1:
            ring(e, kx, ky, 10 + 40 * phase(t, 1.55, 2.0), (1 - phase(t, 1.55, 2.0)) * a)
        zeiger(e, zx, zy, a, druck)
    # HUD: Pille mit Biomquest und Balken
    u = aus_kubisch(phase(t, 2.1, 2.5))
    if u > 0:
        fortschritt = 40 + 88 * ein_aus(phase(t, 2.6, 5.6))
        text = "§eWüste §7· §fSand " + str(int(round(fortschritt))) + "§7/§f128"
        S4 = 4
        inhalt = 14 + mc.breite("§eWüste §7· §fSand 128§7/§f128") + 6
        pille = mc.pille_bild(inhalt, S4)
        x = CX - pille.width / 2
        mc.einfuegen(e, pille, x, 170, ein * u)
        icon_bei(e, "biome_hot_dry", x + 4 * S4, 170 + 2 * S4, 12 * S4, ein * u)
        mct(e, x + 18 * S4, 170 + 4 * S4, text, S4, ein * u)
        bal = mc.balken_bild(160, fortschritt / 128, S4)
        mc.einfuegen(e, bal, CX - bal.width / 2, 248, ein * u)
        helfer = [("head_1", "Lena", 40, 58), ("head_2", "Tom", 0, 42), ("head_3", "Mia", 0, 28)]
        for i, (kopf, name, von, bis) in enumerate(helfer):
            hx = CX - 220 + i * 220
            uu = aus_kubisch(phase(t, 2.3 + i * .12, 2.7 + i * .12))
            icon_bei(e, kopf, hx - 36, 300, 72, ein * uu)
            mct(e, hx, 378, "§f" + name, 3, ein * uu, anker="m")
            wert = von + (bis - von) * ein_aus(phase(t, 2.6, 5.6))
            mct(e, hx, 412, "§e" + str(int(round(wert))) + " §7Sand", 3, ein * uu, anker="m")
        if t >= 5.6:
            s = math.sin(math.pi * phase(t, 5.6, 6.0))
            for i in range(5):
                w = i / 5 * 2 * math.pi
                funkeln(e, CX + math.cos(w) * 300, 258 + math.sin(w) * 40, 14 * s, s)


STUFEN = [
    (0, "chat", "Clan-Chat, Kürzel, 12 Wappen"),
    (300, "mail_broadcast", "Clan-Nachricht und Rundbrief"),
    (800, "banner", "15 Plätze und Clan-Banner"),
    (1500, "clan_island", "Clan-Insel"),
    (2400, "tag", "20 Plätze, Wappen in der Tabliste"),
    (3500, "mana_orb", "Clan-Segen am Wochenende"),
    (5000, "member", "25 Plätze, 8 Wappen mehr"),
    (7000, "star", "Flugspur in Clanfarbe"),
    (9500, "wappen:#FFAA00:krone", "Rahmen um das Wappen"),
    (12500, "trophy", "Titel „Legendär“"),
]


def szene_stufen(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    xp = 3500 * ein_aus(phase(t, .5, 5.2))
    y0, rh = 196, 66
    bx = 900
    # Verbindungslinie
    linie_x = bx + 26
    oben, unten = y0 + 26, y0 + 9 * rh + 26
    mc.einfuegen(e, Image.new("RGBA", (6, unten - oben), (40, 46, 80, 230)), linie_x - 3, oben, ein)
    stufe = 1
    for i, (schwelle, _, _) in enumerate(STUFEN):
        if xp >= schwelle:
            stufe = i + 1
    if stufe < 10:
        a, b = STUFEN[stufe - 1][0], STUFEN[stufe][0]
        anteil = (stufe - 1) + (xp - a) / (b - a)
    else:
        anteil = 9
    voll = min(unten - oben, anteil * rh)
    if voll > 0:
        mc.einfuegen(e, Image.new("RGBA", (6, int(voll)), (255, 200, 60, 255)), linie_x - 3, oben, ein)
    for i, (schwelle, ic, text) in enumerate(STUFEN):
        y = y0 + i * rh
        u = aus_kubisch(phase(t, .1 + i * .05, .5 + i * .05))
        erreicht = xp >= schwelle
        t_hit = .5 + 4.7 * umkehr_ein_aus(schwelle / 3500) if schwelle <= 3500 else 99
        s = 1 + .28 * math.sin(math.pi * phase(t, t_hit, t_hit + .3)) if erreicht else 1
        if erreicht:
            mc.einfuegen(e, tafel(820, 58, 12, (255, 255, 255, 22), (255, 255, 255, 30)), bx - 8, y - 3, ein * u)
        farbe_box = (255, 200, 60, 255) if erreicht else (34, 40, 72, 255)
        box = tafel(52, 52, 10, farbe_box, (20, 16, 30, 255))
        skaliert(e, box, bx + 26, y + 26, 52 * s, alpha=ein * u, glatt=True)
        mct(e, bx + 26, y + 14, ("§0" if erreicht else "§7") + "§l" + str(i + 1), 3, ein * u, anker="m", schatten=not erreicht)
        icon_bei(e, ic, bx + 74, y + 2, 48, ein * u * (1 if erreicht else .45))
        mct(e, bx + 140, y + 15, ("§f" if erreicht else "§7") + text, 3, ein * u * (1 if erreicht else .6))
    mct(e, bx + 812, 140, "§7Erfahrung §f" + tausender(int(round(xp))), 3, ein, anker="r")
    mct(e, bx, 140, "§6Clan-Stufe §f§l" + str(stufe), 3, ein)


PROJEKTE = [
    ("location", "Ankunftsplatz", 4), ("biome_forests_temperate", "Hain", 5), ("clan_hall", "Clanhaus", 6),
    ("warpett_egg", "Blumentor", 7), ("home", "Herberge", 8), ("trophy", "Ehrenhalle", 9),
]


def szene_insel(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    icon_bei(e, "clan_island", 900, 196, 80, ein)
    mct(e, 1000, 208, "§a§lClan-Projekte", 5, ein)
    mct(e, 1000, 260, "§7Baustoffe und Mana zusammentragen", 3, ein)
    kw, kh, gap = 274, 214, 22
    x0, y0 = 900, 318
    for i, (ic, name, stufe) in enumerate(PROJEKTE):
        x = x0 + (i % 3) * (kw + gap)
        y = y0 + (i // 3) * (kh + gap)
        u = rueckschwung(phase(t, .3 + i * .14, .75 + i * .14))
        if u <= 0:
            continue
        hain = i == 1
        if hain and t > 2.4:
            g = aus_kubisch(phase(t, 2.4, 2.8))
            mc.einfuegen(e, tafel(kw + 12, kh + 12, 22, (85, 255, 255, 40), (85, 255, 255, int(220 * g))), x - 6, y - 6, ein)
        karte = tafel(kw, kh, 16)
        skaliert(e, karte, x + kw / 2, y + kh / 2, kw * u, kh * u, alpha=ein, glatt=True)
        if u < .9:
            continue
        icon_bei(e, ic, x + kw / 2 - 40, y + 20, 80, ein)
        mct(e, x + kw / 2, y + 116, "§f" + name, 3, ein, anker="m")
        if hain and t > 2.6:
            q = ein_aus(phase(t, 2.8, 5.2))
            mana = 620 + 380 * q
            if t < 5.3:
                mct(e, x + kw / 2, y + 152, "§d" + tausender(int(round(mana))) + "§7/§f1 000 §7Mana", 3, ein, anker="m")
            else:
                s = 1 + .3 * math.sin(math.pi * phase(t, 5.3, 5.6))
                b = mc.text_bild("§a§lFertig!", 4)
                skaliert(e, b, x + kw / 2 + 2, y + 158 + 12, b.width * s, b.height * s, alpha=ein)
            bal = mc.balken_bild(54, .62 + .38 * q, 4)
            mc.einfuegen(e, bal, x + kw / 2 - bal.width / 2, y + 186, ein)
        else:
            mct(e, x + kw / 2, y + 152, "§7ab Stufe §f" + str(stufe), 3, ein, anker="m")


GUT = ["Gemeinsame Quests", "Wappen, Banner, Titel", "Hilfe bei Biomquests", "Treffpunkt, Rundbrief"]
NICHT = ["Keine Rabatte", "Kein Mana-Handel", "Nichts davon im Shop", "Keine Gratis-Items"]


def szene_fair(e, t, d):
    ein = aus_kubisch(phase(t, 0, .4))
    pw, ph, gap = 470, 470, 24
    x0, y0 = CX - pw - gap / 2, 300
    for spalte, (kopf, liste, zeichen, start) in enumerate((("§a§lDas bringt euer Clan", GUT, "§a✔", .4),
                                                             ("§c§lDas gibt es nicht", NICHT, "§c✘", 2.0))):
        x = x0 + spalte * (pw + gap)
        u = aus_kubisch(phase(t, start - .3, start + .1))
        mc.einfuegen(e, tafel(pw, ph), x, y0, ein * u)
        mct(e, x + 30, y0 + 34, kopf, 3, ein * u)
        mc.einfuegen(e, Image.new("RGBA", (pw - 60, 2), (255, 255, 255, 40)), x + 30, y0 + 84, ein * u)
        for i, eintrag in enumerate(liste):
            uu = rueckschwung(phase(t, start + .2 + i * .3, start + .55 + i * .3))
            if uu <= 0:
                continue
            yy = y0 + 112 + i * 84
            mct(e, x + 30 + (1 - uu) * -20, yy, zeichen + " §f" + eintrag, 3, ein * min(1, uu))


def szene_outro(e, t, d):
    a1 = aus_kubisch(phase(t, .1, .6))
    av(e, "Was meint ihr?", W / 2, 250 + (1 - a1) * 30, 112, "heavy", (255, 255, 255), a1, anker="m")
    a2 = aus_kubisch(phase(t, .45, .95))
    av(e, "Das Clansystem ist noch in Planung.", W / 2, 420, 40, "medium", (214, 228, 248), a2, anker="m", schatten=.4)
    av(e, "Sagt uns im Discord, was ihr davon haltet.", W / 2, 474, 40, "medium", (140, 236, 255), a2,
       anker="m", schatten=.4)
    n, g, gap = 8, 84, 24
    xs = (W - (n * g + (n - 1) * gap)) / 2
    for i, (farbe, motiv) in enumerate(INTRO_WAPPEN[:n]):
        t0 = .8 + i * .06
        s = rueckschwung(phase(t, t0, t0 + .4))
        if s > 0:
            wip = 5 * math.sin(2 * math.pi * (t * .42 + i * .11))
            wappen_bei(e, farbe, motiv, xs + i * (g + gap) + g / 2, 640 + wip, g * s)
    a3 = aus_kubisch(phase(t, 1.3, 1.9))
    skaliert(e, WORTMARKE, W / 2, 820, WORTMARKE.width * 2, WORTMARKE.height * 2, alpha=a3)


SZENEN = [
    dict(dauer=5.0, zeichne=szene_intro),
    dict(dauer=7.0, nr="01", kicker="Clan gründen", titel="Dein Clan, dein Wappen",
         text="Name, Kürzel, Farbe und Wappen suchst du selbst aus. Mit /clan geht es los.", zeichne=szene_gruenden),
    dict(dauer=9.0, nr="02", kicker="Das Clan-Menü", titel="Alles an einem Ort",
         text="Mitglieder, Clan-Quests, Clan-Insel, Chat und Einstellungen – übersichtlich in einem Menü.",
         zeichne=szene_menue),
    dict(dauer=7.5, nr="03", kicker="Clan-Chat", titel="Schreib mit # an deinen Clan",
         text="Der Clan-Chat erreicht euch auf jedem Server: in der Lobby, auf den Inseln und im Citybuild.",
         zeichne=szene_chat),
    dict(dauer=8.5, nr="04", kicker="Clan-Quests", titel="Der Wochenauftrag",
         text="Jede Woche drei Aufgaben und ein gemeinsamer Punkte-Topf. Jeder hilft dort, wo er gerade spielt.",
         zeichne=szene_auftrag),
    dict(dauer=7.5, nr="05", kicker="Clan-Quests", titel="Hilferuf",
         text="Hängst du an einer Biomquest fest? Ruf deinen Clan. Wer mit anpackt, bekommt Mana wie ein Inselmitglied.",
         zeichne=szene_hilferuf),
    dict(dauer=7.0, nr="06", kicker="Clan-Stufen", titel="Zusammen aufsteigen",
         text="Jeder Wochenauftrag bringt Erfahrung. Zehn Stufen schalten Plätze, Wappen, das Clan-Banner und mehr frei.",
         zeichne=szene_stufen),
    dict(dauer=7.5, nr="07", kicker="Clan-Insel · geplant", titel="Eine Insel für euren Clan",
         text="Ab Stufe 4 baut ihr gemeinsam an eurer Clan-Insel – Projekt für Projekt, ganz ohne Zeitdruck.",
         zeichne=szene_insel),
    dict(dauer=6.5, nr="08", kicker="Fair für alle", titel="Gemeinschaft statt Vorsprung",
         text="Clans bringen gemeinsame Ziele, Kosmetik und Komfort – aber keine Rabatte und nichts zu kaufen.",
         zeichne=szene_fair),
    dict(dauer=5.5, zeichne=szene_outro),
]
FILM = Film("clans", SZENEN, abzeichen_text="VORSCHAU  ·  noch in Planung",
            musik=dict(tonart="D", tempo=84, stimmung="hell"))
