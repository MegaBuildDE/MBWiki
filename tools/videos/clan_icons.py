"""Entwuerfe der neuen Clan-Icons im Format von tools/gen_icons.py.

Jedes Icon ist ein 16x16-Raster mit den Farbbuchstaben aus gen_icons.FARBEN
(k Aussenlinie, Grossbuchstabe = helle obere Haelfte, Kleinbuchstabe = dunkle
untere Haelfte). Die Raster lassen sich spaeter unveraendert in gen_icons.py
uebernehmen.

Wappen: ein Schild in Clanfarbe (F hell, f dunkel) mit einem 8x8-Motiv
('#' weiss, '+' hellgrau). Dasselbe 8x8-Motiv ist der Entwurf fuer das
Schriftzeichen vor dem Kuerzel in Tablist und Chat.
"""

CLAN = [
    "................",
    "..kkkkkkkkkkkk..",
    "..kBBBBBBBBBBk..",
    "..kBBBBBBBBBBk..",
    "..kBBBBBBBBBBk..",
    "..kYYYYYYYYYYk..",
    "..kyyyyyyyyyyk..",
    "..kbbbbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "...kbbbbbbbbk...",
    "...kbbbbbbbbk...",
    "....kbbbbbbk....",
    ".....kbbbbk.....",
    "......kkkk......",
    "................",
    "................",
]

CLAN_CREATE = [
    "................",
    "..kkkkkkkkkkkk..",
    "..kBBBBBBBBBBk..",
    "..kBBBBWWBBBBk..",
    "..kBBBBWWBBBBk..",
    "..kBBWWWWWWBBk..",
    "..kbbWWWWWWbbk..",
    "..kbbbbWWbbbbk..",
    "..kbbbbWWbbbbk..",
    "...kbbbbbbbbk...",
    "...kbbbbbbbbk...",
    "....kbbbbbbk....",
    ".....kbbbbk.....",
    "......kkkk......",
    "................",
    "................",
]

CLAN_LIST = [
    "................",
    "................",
    "................",
    "................",
    "kkkkkkkkkkkkkkk.",
    "kRRRkkBBBkkGGGk.",
    "kRRRkkBBBkkGGGk.",
    "krrrkkbbbkkgggk.",
    "krrrkkbbbkkgggk.",
    ".krk..kbk..kgk..",
    "..k....k....k...",
    "................",
    "................",
    "................",
    "................",
    "................",
]

CROWN = [
    "................",
    "................",
    "................",
    "..k....kk....k..",
    ".kYk..kYYk..kYk.",
    ".kYYkkYYYYkkYYk.",
    ".kYYYYYYYYYYYYk.",
    ".kYYRYYYYYYRYYk.",
    ".kyyyyyyyyyyyyk.",
    ".kooooooooooook.",
    ".kkkkkkkkkkkkkk.",
    "................",
    "................",
    "................",
    "................",
    "................",
]

OFFICER = [
    "................",
    ".....kkkkkk.....",
    "...kkBBBBBBkk...",
    "..kBBBBYYBBBBk..",
    "..kBBBBYYBBBBk..",
    "..kBYYYYYYYYBk..",
    "..kbbYYYYYYbbk..",
    "..kbbbYYYYbbbk..",
    "..kbbYYbbYYbbk..",
    "...kkbbbbbbkk...",
    ".....kkkkkk.....",
    ".....krk.krk....",
    "....krrk.krrk...",
    "....kkk...kkk...",
    "................",
    "................",
]

RECRUIT = [
    "................",
    "................",
    "................",
    "...kkk....kkk...",
    "..kGGGk..kGGGk..",
    "..kGGGGkkGGGGk..",
    "...kgggkkgggk...",
    "....kkkggkkk....",
    "......kggk......",
    "......kggk......",
    ".....kkkkkk.....",
    "....kDDDDDDk....",
    "....kddddddk....",
    "....kkkkkkkk....",
    "................",
    "................",
]

CHAT = [
    "................",
    "................",
    "..kkkkkkkkkkkk..",
    ".kWWWWWWWWWWWWk.",
    ".kWWWWWWWWWWWWk.",
    ".kWWkkWkkWkkWWk.",
    ".kWWkkWkkWkkWWk.",
    ".kwwwwwwwwwwwwk.",
    ".kwwwwwwwwwwwwk.",
    "..kwwkkkkkkkkk..",
    "..kwk...........",
    "..kk............",
    "................",
    "................",
    "................",
    "................",
]

INVITE = [
    "...kkkkkk.......",
    "..kddddddk......",
    "..kDDDDDDk......",
    "..kDkDDkDk......",
    "..kDDDDDDk......",
    "...kkkkkk.......",
    ".kkkkkkkkkk.....",
    "kBBBBBBBBBBk....",
    "kbbbbbbbbbbkkk..",
    "kbbbbbbbbbbkGk..",
    "kkkkkkkkkkkkGkkk",
    ".........kGGGGGk",
    ".........kkkGkkk",
    "...........kGk..",
    "...........kkk..",
    "................",
]

KICK = [
    "...kkkkkk.......",
    "..kddddddk......",
    "..kDDDDDDk......",
    "..kDkDDkDk......",
    "..kDDDDDDk......",
    "...kkkkkk.......",
    ".kkkkkkkkkk.....",
    "kBBBBBBBBBBk....",
    "kbbbbbbbbbbk....",
    "kbbbbbbbbbbk....",
    "kkkkkkkkkkkkkkkk",
    ".........kRRRRRk",
    ".........kkkkkkk",
    "................",
    "................",
    "................",
]

APPLY = [
    "................",
    "................",
    ".kkkkkkkkkkkkkk.",
    ".kDkWWWWWWWWkDk.",
    ".kDkWkkkkkkWkDk.",
    ".kdkWWWWWWWWkdk.",
    ".kdkWkkkkWWWkdk.",
    ".kDkWWWWWWRRkDk.",
    ".kdkWkkkkWRrkdk.",
    ".kdkwwwwwwwwkdk.",
    ".kkkkkkkkkkkkkk.",
    "................",
    "................",
    "................",
    "................",
    "................",
]

LEAVE = [
    "................",
    ".kkkkkkkk.......",
    ".kDDDDDDk.......",
    ".kDkkkkDk.......",
    ".kDkDDkDk.......",
    ".kDkkkkDk...kk..",
    ".kDDDDDYk...kGk.",
    ".kddddddkkkkkGGk",
    ".kdkkkkdkkGGGGGk",
    ".kdkddkdkkkkkggk",
    ".kdkkkkdk...kgk.",
    ".kddddddk...kk..",
    ".kkkkkkkk.......",
    "................",
    "................",
    "................",
]

VISIT = [
    "................",
    "....kkkkkkkk....",
    "...kTTTTTTTTk...",
    "..kTTkkkkkkTTk..",
    "..kTkPPPPPPkTk..",
    "..kTkPPWPPPkTk..",
    "..kTkPPPPPPkTk..",
    "..ktkppppppktk..",
    "..ktkpppPppktk..",
    "..ktkppppppktk..",
    "..ktkppppppktk..",
    "..kkkkkkkkkkkk..",
    "................",
    "................",
    "................",
    "................",
]

HOME = [
    "................",
    ".......kk.......",
    "......kRRk......",
    ".....kRRRRk.....",
    "....kkkkkkkk....",
    ".....kDkkDk.....",
    ".kkkkkDkkDkkkk..",
    "kGGGGGGGGGGGGGk.",
    "kdddddddddddddk.",
    ".kwwwwwwwwwwwk..",
    "..kwwwwwwwwwk...",
    "...kwwwwwwwk....",
    "....kwwwwwk.....",
    ".....kwwwk......",
    "......kwk.......",
    ".......k........",
]

TROPHY = [
    "................",
    "...kkkkkkkkkk...",
    ".kkYYYYYYYYYYkk.",
    "kYkYYWYYYYYYkYk.",
    "kYkYYYYYYYYYkYk.",
    ".kkyyyyyyyyyykk.",
    "...kyyyyyyyyk...",
    "....kyyyyyyk....",
    ".....kkyykk.....",
    "......kyyk......",
    "......kyyk......",
    "....kkkkkkkk....",
    "....kooooook....",
    "....kkkkkkkk....",
    "................",
    "................",
]

CLAN_QUEST = [
    "................",
    "................",
    ".kkkkkkkkkkkkkk.",
    ".kDkWWWWWWWWkDk.",
    ".kDkWWkkkkWWkDk.",
    ".kdkWWkBBkWWkdk.",
    ".kdkWWkbbkWWkdk.",
    ".kDkWWWkkWWWkDk.",
    ".kdkWkkkkkkWkdk.",
    ".kdkwwwwwwwwkdk.",
    ".kkkkkkkkkkkkkk.",
    "................",
    "................",
    "................",
    "................",
    "................",
]

MEDAILLE = [
    "................",
    "...kk......kk...",
    "...krk....kbk...",
    "....krk..kbk....",
    ".....krkkbk.....",
    ".....kkkkkk.....",
    "....kMMMMMMk....",
    "...kMMMMMMMMk...",
    "...kMMWMMMMMk...",
    "...kmmmmmmmmk...",
    "...kmmmmmmmmk...",
    "....kmmmmmmk....",
    ".....kkkkkk.....",
    "................",
    "................",
    "................",
]


def _medaille(hell: str, dunkel: str) -> list:
    return [z.replace("M", hell).replace("m", dunkel) for z in MEDAILLE]


MEDAL_GOLD = _medaille("Y", "y")
MEDAL_SILVER = _medaille("W", "w")
MEDAL_BRONZE = _medaille("o", "d")

CLAN_LEVEL = [
    "................",
    ".kkkkkkkkkkkkkk.",
    ".kddddddddddddk.",
    ".kkkkkkkkkkkkkk.",
    "..kBBBBBBBBBBk..",
    "..kBBBBYYBBBBk..",
    "..kBBBBYYBBBBk..",
    "..kBYYYYYYYYBk..",
    "..kbbYYYYYYbbk..",
    "..kbbbYYYYbbbk..",
    "..kbbYYbbYYbbk..",
    "..kbbbbbbbbbbk..",
    "..kbbbbkkbbbbk..",
    "..kbbbk..kbbbk..",
    "..kkkk....kkkk..",
    "................",
]

CLAN_ISLAND = [
    "......kkkkkkk...",
    "......kBBBBBk...",
    "......kBYBBBk...",
    "......kbbbbbk...",
    "......kkkkkkk...",
    "......k.........",
    ".kkkkkkkkkkkkk..",
    "kGGGGGGGGGGGGGk.",
    "kdddddddddddddk.",
    ".kwwwwwwwwwwwk..",
    "..kwwwwwwwwwk...",
    "...kwwwwwwwk....",
    "....kwwwwwk.....",
    ".....kwwwk......",
    "......kwk.......",
    ".......k........",
]

CLAN_HALL = [
    ".......kkkk.....",
    ".......kYYk.....",
    ".......kkkk.....",
    ".......kk.......",
    "......kBBk......",
    ".....kBBBBk.....",
    "....kBBBBBBk....",
    "...kBBBBBBBBk...",
    "..kBBBBBBBBBBk..",
    "..kkkDDDDDkkkk..",
    "....kDDDDDk.....",
    "....kDkkkDk.....",
    "....kDkWkDk.....",
    "....kDkkkDk.....",
    "....kkkkkkk.....",
    "................",
]

TREASURY = [
    ".....kkkkkk.....",
    "....kRRRRRRk....",
    ".....krrrrk.....",
    "......kkkk......",
    "..kkkkkkkkkkkk..",
    "..kDDDDDDDDDDk..",
    "..kDDDDDDDDDDk..",
    "..kkkkkRRkkkkk..",
    "..kddddkkddddk..",
    "..kddddRRddddk..",
    "..kddddkkddddk..",
    "..kddddddddddk..",
    "..kkkkkkkkkkkk..",
    "................",
    "................",
    "................",
]

RUBY = [
    "................",
    "................",
    "....kkkkkkkk....",
    "...kRRRRRRRRk...",
    "..kRRWRRRRRRRk..",
    ".kRRRRRRRRRRRRk.",
    ".keeeeeeeeeeeek.",
    "..krrrrrrrrrrk..",
    "...krrrrrrrrk...",
    "....krrrrrrk....",
    ".....krrrrk.....",
    "......krrk......",
    ".......kk.......",
    "................",
    "................",
    "................",
]

PALETTE = [
    "................",
    "................",
    "....kkkkkkk.....",
    "..kkDDDDDDDkk...",
    ".kDDRRDDDBBDDk..",
    ".kDDRRDDDBBDDDk.",
    ".kDDDDDDDDDkkkk.",
    ".kdYYdddddk.....",
    ".kdYYddGGdk.....",
    "..kddddGGddk....",
    "...kkdddddddk...",
    ".....kkkkkkk....",
    "................",
    "................",
    "................",
    "................",
]

TAG = [
    "................",
    "................",
    "................",
    "....kkkkkkkkkkk.",
    "...kWWWWWWWWWWk.",
    "..kWWkWWWWWWWWk.",
    "..kWWWWkkkkkkWk.",
    "..kwwwwwwwwwwwk.",
    "...kwwwkkkkwwwk.",
    "....kkkkkkkkkkk.",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

QUILL = [
    "................",
    "............kkk.",
    "..........kkWWk.",
    ".........kWWWWk.",
    "........kWWWWk..",
    ".......kWWWWk...",
    "......kWWwwk....",
    ".....kWwwwk.....",
    "....kwwwkk......",
    "...kwwk.........",
    "..ktk...........",
    ".kk.............",
    "................",
    "................",
    "................",
    "................",
]

BELL_ON = [
    "................",
    ".......kk.......",
    "......kYYk......",
    ".....kYYYYk.....",
    "....kYYYYYYk....",
    "....kYWYYYYk....",
    "....kyyyyyyk....",
    "...kyyyyyyyyk...",
    "..kyyyyyyyyyyk..",
    "..kkkkkkkkkkkk..",
    "......kyyk......",
    ".......kk.......",
    "................",
    "................",
    "................",
    "................",
]

EYE = [
    "................",
    "................",
    "................",
    "................",
    "....kkkkkkkk....",
    "..kkWWWWWWWWkk..",
    ".kWWWkkkkkkWWWk.",
    "kWWWWkBBBBkWWWWk",
    "kWWWWkbkkbkWWWWk",
    ".kwwwkkkkkkwwwk.",
    "..kkwwwwwwwwkk..",
    "....kkkkkkkk....",
    "................",
    "................",
    "................",
    "................",
]

RIGHTS = [
    "................",
    "..kkkkkkkkkkkk..",
    "..kGGGGGGGGGGk..",
    "..kGGGGGGGGWGk..",
    "..kGGGGGGGWWGk..",
    "..kGWGGGGWWGGk..",
    "..kgWWggWWgggk..",
    "..kggWWWWggggk..",
    "..kgggWWgggggk..",
    "...kggggggggk...",
    "...kggggggggk...",
    "....kggggggk....",
    ".....kggggk.....",
    "......kkkk......",
    "................",
    "................",
]

DOOR = [
    "................",
    "....kkkkkkkk....",
    "....kDDDDDDk....",
    "....kDkkkkDk....",
    "....kDkDDkDk....",
    "....kDkkkkDk....",
    "....kDDDDDYk....",
    "....kddddddk....",
    "....kdkkkkdk....",
    "....kdkddkdk....",
    "....kdkkkkdk....",
    "....kddddddk....",
    "....kkkkkkkk....",
    "................",
    "................",
    "................",
]

ANIMALS = [
    "................",
    "................",
    ".....kkkkkkkkk..",
    ".kkkkWWWWWWWWWk.",
    "kTTTkWWWWWWWWWk.",
    "kTkTkWWWWWWWWWk.",
    "ktttkWWWWWWWWWk.",
    ".kkkkwwwwwwwwwk.",
    ".....kwwwwwwwwk.",
    ".....kkkkkkkkkk.",
    "......ktk..ktk..",
    "......kkk..kkk..",
    "................",
    "................",
    "................",
    "................",
]

REQUEST_OUT = [
    "................",
    ".............k..",
    "............kGk.",
    "...........kGGGk",
    "...........kkGkk",
    "............kGk.",
    "............kGk.",
    "kkkkkkkkkkkkkkk.",
    "kkWWWWWWWWkk....",
    "kWkkWWWWkkWk....",
    "kWWWkkkkWWWk....",
    "kwwwwwwwwwwk....",
    "kwwwwwwwwwwk....",
    "kkkkkkkkkkkk....",
    "................",
    "................",
]


def _durchgestrichen(raster: list) -> list:
    """Legt einen roten Schraegstrich von links oben nach rechts unten darueber."""
    zeilen = [list(z) for z in raster]
    for i in range(13):
        x, y = 2 + i, 1 + i
        if 0 <= y < 16:
            for dx, farbe in ((-1, "k"), (0, "R"), (1, "e"), (2, "k")):
                xx = x + dx
                if 0 <= xx < 16:
                    zeilen[y][xx] = farbe
    return ["".join(z) for z in zeilen]


BELL_OFF = _durchgestrichen(BELL_ON)
EYE_OFF = _durchgestrichen(EYE)

# Spielerkoepfe fuer die Menue-Entwuerfe (Java zeigt Koepfe, Bedrock nicht).
KOPF_VORLAGE = [
    "................",
    "..kkkkkkkkkkkk..",
    "..kHHHHHHHHHHk..",
    "..kHHHHHHHHHHk..",
    "..kHDDDDDDDDHk..",
    "..kDDDDDDDDDDk..",
    "..kDWbDDDDbWDk..",
    "..kDDDDDDDDDDk..",
    "..kDDDddddDDDk..",
    "..kdddddddddDk..",
    "..kkkkkkkkkkkk..",
    "................",
    "................",
    "................",
    "................",
    "................",
]


def _kopf(haar: str) -> list:
    return [z.replace("H", haar) for z in KOPF_VORLAGE]


KOEPFE = {
    "head_1": _kopf("d"),
    "head_2": _kopf("y"),
    "head_3": _kopf("t"),
    "head_4": _kopf("e"),
    "head_5": _kopf("o"),
    "head_6": _kopf("k"),
}

# Neu am 12.10.2026: Hilferuf, Projekte, Meilensteine, Chronik, Banner, Zusammen-Bonus
HELP_CALL = [
    "................",
    "................",
    "...........kk...",
    "..........kYYk..",
    ".........kYYYk.k",
    "........kYYYYk..",
    "..kkk..kYYYYYk.k",
    ".kdDDkkYYYYYYk..",
    ".kddddyyyyyyyk.k",
    "..kkk..kyyyyyk..",
    "........kyyyyk.k",
    ".........kyyyk..",
    "..........kyyk..",
    "...........kk...",
    "................",
    "................",
]

PROJECT = [
    "................",
    "..kkkkkkkkkkk...",
    "..kBBBBBBBBBk...",
    "..kBWWWWBBBBk...",
    "..kBWBBWBWWBk...",
    "..kBWWWWBBBBk.kk",
    "..kbbbbbbbbbkkTk",
    "..kbWWbbWWWbkTTk",
    "..kbbbbbbbkkTTk.",
    "..kbWWWWbkTTkk..",
    "..kbbbbbkTTkk...",
    "..kkkkkkdkk.....",
    "......kdk.......",
    ".....kdk........",
    "....kdk.........",
    "....kk..........",
]

MILESTONE = [
    "................",
    "......kkkkkkk...",
    "......kdRRRRk...",
    "......kdRRRk....",
    "......kdrrrrk...",
    "......kdkkkkk...",
    "......kdk.......",
    "....kkkdkkk.....",
    "...kTTTTTTTk....",
    "...kTTWTTTTk....",
    "...kTTTTTTTk....",
    "...kttttwttk....",
    "..kttttttttk....",
    "..kttttttttttk..",
    "..kkkkkkkkkkkk..",
    "................",
]

CHRONICLE = [
    "................",
    "..kkkkkkkkkkk...",
    "..kDdDDDDDDDDk..",
    "..kDdDDkkkkDDk..",
    "..kDdDkYYYYkDk..",
    "..kDdDkYooYkDk..",
    "..kDdDkYooYkDk..",
    "..kddddkyykddk..",
    "..kdddddkkdddk..",
    "..kddddddddddk..",
    "..kddddddddddk..",
    "..kdWWWWWWWWWk..",
    "..kdwwwwwwwwwk..",
    "..kkkkkkkkkkkk..",
    "................",
    "................",
]

BANNER = [
    "................",
    ".kkkkkkkkkkkkkk.",
    ".kDDDDDDDDDDDDk.",
    ".kkkkkkkkkkkkkk.",
    "...kBBBBBBBBk...",
    "...kBBBBBBBBk...",
    "...kBBBWWBBBk...",
    "...kBBWWWWBBk...",
    "...kbbWWWWbbk...",
    "...kbbbWWbbbk...",
    "...kbbbbbbbbk...",
    "...kbbbbbbbbk...",
    "...kbbbkkbbbk...",
    "...kbbk..kbbk...",
    "...kbk....kbk...",
    "...kk......kk...",
]

TOGETHER = [
    "................",
    "................",
    "...kkkk..kkkk...",
    "..kDDDDk.kDDDDk.",
    "..kDDDDk.kDDDDk.",
    "..kDDDDk.kDDDDk.",
    "..kddddk.kddddk.",
    "...kkkk...kkkk..",
    "..kkkkkk.kkkkkk.",
    ".kBBBBBBkGGGGGGk",
    ".kBBBBBBkGGGGGGk",
    ".kbbbbbbkggggggk",
    ".kbbbbbbkggggggk",
    ".kkkkkkkkkkkkkkk",
    "................",
    "................",
]

NEU = {
    "clan": CLAN,
    "clan_create": CLAN_CREATE,
    "clan_list": CLAN_LIST,
    "crown": CROWN,
    "officer": OFFICER,
    "recruit": RECRUIT,
    "chat": CHAT,
    "invite": INVITE,
    "kick": KICK,
    "apply": APPLY,
    "leave": LEAVE,
    "visit": VISIT,
    "home": HOME,
    "trophy": TROPHY,
    "clan_quest": CLAN_QUEST,
    "medal_bronze": MEDAL_BRONZE,
    "medal_silver": MEDAL_SILVER,
    "medal_gold": MEDAL_GOLD,
    "clan_level": CLAN_LEVEL,
    "clan_island": CLAN_ISLAND,
    "clan_hall": CLAN_HALL,
    "treasury": TREASURY,
    "ruby": RUBY,
    "palette": PALETTE,
    "tag": TAG,
    "quill": QUILL,
    "bell_on": BELL_ON,
    "bell_off": BELL_OFF,
    "eye": EYE,
    "eye_off": EYE_OFF,
    "rights": RIGHTS,
    "door": DOOR,
    "animals": ANIMALS,
    "request_out": REQUEST_OUT,
    "help_call": HELP_CALL,
    "project": PROJECT,
    "milestone": MILESTONE,
    "chronicle": CHRONICLE,
    "banner": BANNER,
    "together": TOGETHER,
}

# ── Wappen ───────────────────────────────────────────────────────────────────

# Wappen, zweite Fassung (12.10.2026): Schild 13 breit, innen 11 (x 2..12, Mitte 7),
# damit symmetrische Motive mit Mittelspalte genau mittig sitzen.
SCHILD = [
    "................",
    ".kkkkkkkkkkkkk..",
    ".kFFFFFFFFFFFk..",
    ".kFFFFFFFFFFFk..",
    ".kFFFFFFFFFFFk..",
    ".kFFFFFFFFFFFk..",
    ".kFFFFFFFFFFFk..",
    ".kfffffffffffk..",
    ".kfffffffffffk..",
    ".kfffffffffffk..",
    "..kfffffffffk...",
    "...kfffffffk....",
    "....kfffffk.....",
    ".....kfffk......",
    "......kkk.......",
    "................",
]
# Rueckfall-Ecke; gesetzt wird nach MOTIV_POS.
MOTIV_X, MOTIV_Y = 3, 3

# Motive im Schild, bis 9x9, ungerade breit. '#' weiss, '+' hellgrau.
MOTIVE = {
    "kristall": ["..#####..", ".#+#+#+#.", "#########", ".#######.", "..#####..", "...###...", "....#...."],
    "blatt": ["....####.", "..#######", ".####+###", ".###+####", ".##+####.", ".#+####..", ".+.##....", "+........"],
    "pilz": ["..#####..", ".##.####.", "######.##", "#########", "...+++...", "...+++...", "..+++++.."],
    "fisch": ["....###..", "#..#####.", "######.##", "#########", "#..#####.", "....###.."],
    "welle": [".##..##..", "#..##..##", ".........", ".##..##..", "#..##..##", ".........", ".##..##..", "#..##..##"],
    "berg": ["....#....", "...###...", "..#####..", "..#+#+#..", ".#+++++#.", ".+++++++.", "+++++++++"],
    "schneeflocke": ["....#....", ".#..#..#.", "..#.#.#..", "...###...", "#########", "...###...", "..#.#.#..", ".#..#..#.", "....#...."],
    "sonne": ["....#....", ".#.....#.", "...###...", "..#####..", "#.#####.#", "..#####..", "...###...", ".#.....#.", "....#...."],
    "mond": ["..####.", ".###...", "###....", "###....", "###....", "###....", ".###...", "..####."],
    "stern": ["....#....", "....#....", "...###...", "#########", ".#######.", "..#####..", "..##.##..", ".##...##.", ".#.....#."],
    "flamme": ["...#...", "...##..", "..###..", ".####.#", ".##+###", "##+++##", "#+++++#", ".#+++#.", "..###.."],
    "feder": [".......##", "......###", ".....##+#", "....##+##", "...##+##.", "..##+##..", "..#+##...", ".+.......", "+........"],
    "fuchs": ["#.......#", "##.....##", "###...###", "#########", "##.###.##", ".#######.", "..++#++..", "...+#+...", "....#...."],
    "wolf": ["....#.#..", "....####.", "...##.##.", "..######.", "########.", ".....###.", "....####.", "...#####.", "..#.#.##."],
    "biene": ["...###...", "##.###.##", "###+++###", ".##+++##.", "...###...", "...+++...", "...###...", "....#...."],
    "axt": ["##..+..##", "###.+.###", "#########", "###.+.###", "##..+..##", "....+....", "....+....", "....+...."],
    "spitzhacke": ["..#####..", ".##.+.##.", "##..+..##", "#...+...#", "....+....", "....+....", "....+....", "....+...."],
    "schwert": ["....#....", "...#+#...", "...#+#...", "...#+#...", "...#+#...", ".#######.", "....+....", "....+....", "...+++..."],
    "anker": ["...###...", "...#.#...", "...###...", ".#######.", "....#....", "#...#...#", "##..#..##", ".##.#.##.", "..#####.."],
    "luftschiff": [".#####..#", "#######.#", "#########", "#######.#", ".#####..#", "..+..+...", "..####..."],
    "warpett": ["..#.#.#..", "..#####..", "..#####..", "...###...", "....+....", "++..+..++", ".++.+.++.", "..+++++..", "....+...."],
    "baum": ["....#....", "...###...", "..#####..", "...###...", "..#####..", ".#######.", "#########", "....+....", "...+++..."],
    "krone": ["#...#...#", "##.###.##", "#########", "#+#+#+#+#", "#########"],
    "kaktus": ["....#....", "...###...", "#..###...", "#..###..#", "##.###..#", ".#####.##", "...#####.", "...###...", "...###..."],
}

# Dieselben Motive als Schriftzeichen fuer Tablist und Chat: hoechstens 7x8,
# die 8. Spalte ist der Abstand (Schriftzeichen im Pack sind 8 hoch).
GLYPHE = {
    "kristall": [".#####.", "#+#+#+#", "#######", ".#####.", "..###..", "...#..."],
    "blatt": ["...####", ".######", ".###+##", ".##+##.", ".#+##..", ".+.....", "+......"],
    "pilz": [".#####.", "##.####", "####.##", "#######", "..+++..", "..+++..", ".+++++."],
    "fisch": ["...##..", "#.####.", "####.##", "#######", "#.####.", "...##.."],
    "welle": [".##..##", "#..##..", ".......", ".##..##", "#..##..", ".......", ".##..##", "#..##.."],
    "berg": ["...#...", "..###..", ".##+##.", ".#+++#.", "#+++++#", "+++++++"],
    "schneeflocke": ["...#...", ".#.#.#.", "..###..", "#######", "..###..", ".#.#.#.", "...#..."],
    "sonne": ["...#...", ".#...#.", "..###..", "#.###.#", "..###..", ".#...#.", "...#..."],
    "mond": ["..####.", ".###...", "###....", "###....", "###....", "###....", ".###...", "..####."],
    "stern": ["...#...", "...#...", "#######", ".#####.", "..###..", ".##.##.", ".#...#."],
    "flamme": ["...##..", "..###..", ".####.#", ".##+###", "##+++##", "#+++++#", ".#+++#.", "..###.."],
    "feder": [".....##", "....###", "...##+#", "..##+##", ".##+##.", ".#+##..", ".+.....", "+......"],
    "fuchs": ["#.....#", "##...##", "#######", "#.###.#", ".#####.", "..+#+..", "...#..."],
    "wolf": ["...#.#.", "...####", "..##.##", ".######", "######.", "...###.", "..####.", ".#####."],
    "biene": ["..###..", "#.###.#", "##+++##", ".#+++#.", "..###..", "..+++..", "..###..", "...#..."],
    "axt": ["#..+..#", "##.+.##", "#######", "##.+.##", "#..+..#", "...+...", "...+...", "...+..."],
    "spitzhacke": [".#####.", "##.+.##", "#..+..#", "...+...", "...+...", "...+...", "...+..."],
    "schwert": ["...#...", "..#+#..", "..#+#..", "..#+#..", "#######", "...+...", "...+...", "..+++.."],
    "anker": ["..###..", "..#.#..", "..###..", "#######", "...#...", "#..#..#", "##.#.##", ".#####."],
    "luftschiff": [".####.#", "######.", "#######", "######.", ".####.#", "..+.+..", "..###.."],
    "warpett": [".#.#.#.", ".#####.", ".#####.", "..###..", "...+...", "++.+.++", ".+++++.", "...+..."],
    "baum": ["...#...", "..###..", ".#####.", "..###..", ".#####.", "#######", "...+...", "..+++.."],
    "krone": ["#..#..#", "##.#.##", "#######", "#+#+#+#", "#######"],
    "kaktus": ["...#...", "..###..", "#.###..", "#.###.#", "#####.#", "..#####", "..###..", "..###.."],
}

MOTIV_NAMEN = {
    "kristall": "Kristall", "blatt": "Blatt", "pilz": "Pilz", "fisch": "Fisch", "welle": "Welle",
    "berg": "Berg", "schneeflocke": "Schneeflocke", "sonne": "Sonne", "mond": "Mond", "stern": "Stern",
    "flamme": "Flamme", "feder": "Feder", "fuchs": "Fuchs", "wolf": "Wolf", "biene": "Biene",
    "axt": "Axt", "spitzhacke": "Spitzhacke", "schwert": "Schwert", "anker": "Anker",
    "luftschiff": "Luftschiff", "warpett": "Warpett", "baum": "Baum", "krone": "Krone", "kaktus": "Kaktus",
}


# Optischer Ausgleich (dx, dy): Der Mond hat seine Masse links, er rueckt einen Pixel nach rechts.
AUSGLEICH = {"mond": (1, 0)}


def motiv_pos(name):
    """Ecke (x, y), an der ein Motiv mittig im Schild sitzt.

    Gemittelt wird die belegte Flaeche: waagerecht auf x 7 (Schild innen x 2..12),
    senkrecht auf y 6,5, etwas ueber der halben Hoehe, wo der Schild noch breit
    ist. Dazu kommt der optische Ausgleich.
    """
    raster = MOTIVE[name]
    xs = [x for z in raster for x, ch in enumerate(z) if ch != "."]
    ys = [y for y, z in enumerate(raster) for ch in z if ch != "."]
    breite, hoehe = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    links = int(7 - (breite - 1) / 2 + 0.5 - 1e-9)
    oben = int(6.5 - (hoehe - 1) / 2)
    dx, dy = AUSGLEICH.get(name, (0, 0))
    return links - min(xs) + dx, oben - min(ys) + dy


MOTIV_POS = {name: motiv_pos(name) for name in MOTIVE}
