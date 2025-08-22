import os
from datetime import timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "0"))
AUDIO_PATH = os.path.join("audios", "audio.mp3")
GMT_MINUS_3 = timezone(timedelta(hours=-3))
FFMPEG_PATH = "ffmpeg"


ROTATION_MINUTES = os.getenv("ROTATION_MINUTES", "25;28")
FURY_MINUTES = os.getenv("FURY_MINUTES", "55;58")
DEIUS_MINUTES = os.getenv("DEIUS_MINUTES", "55;58")


BOSS_ROTATION = {
    0: {
        "rotation": [
            "Valento",
            "Kelvezu",
            "Gorgoniac",
            "Draxos",
            "Eadric/Vault",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
        },
    },
    1: {
        "rotation": [
            "Chaos Queen",
            "Blood Prince",
            "Devil Shy",
            "Primal Golem",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
        },
    },
    2: {
        "rotation": [
            "Valento",
            "Mokova",
            "Tulla",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
        },
    },
    3: {
        "rotation": [
            "Chaos Queen",
            "Kelvezu",
            "Gorgoniac",
            "Deius",
            "Greedy",
            "Aragonian",
            "Eadric/Vault",
        ],
        "special_bosses": {},
    },
    4: {
        "rotation": [
            "Valento",
            "Blood Prince",
            "Draxos",
            "Yagditha",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
            "Deius": DEIUS_MINUTES,
        },
    },
    5: {
        "rotation": [
            "Chaos Queen",
            "Mokova",
            "Devil Shy",
            "Ignis",
        ],
        "special_bosses": {},
    },
    6: {
        "rotation": [
            "Valento",
            "Kelvezu",
            "Gorgoniac",
            "Tulla",
            "Eadric/Vault",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
            "Deius": DEIUS_MINUTES,
        },
    },
    7: {
        "rotation": [
            "Chaos Queen",
            "Blood Prince",
            "Eadric/Vault",
            "Primal Golem (H)",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
        },
    },
    8: {
        "rotation": [
            "Valento",
            "Mokova",
            "Draxos",
        ],
        "special_bosses": {},
    },
    9: {
        "rotation": [
            "Chaos Queen",
            "Kelvezu",
            "Gorgoniac",
            "Devil Shy",
            "Greedy",
            "Aragonian",
            "Eadric/Vault",
        ],
        "special_bosses": {},
    },
    10: {
        "rotation": [
            "Valento",
            "Blood Prince",
            "Yagditha",
            "Tulla",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
            "Deius": DEIUS_MINUTES,
        },
    },
    11: {
        "rotation": [
            "Chaos Queen",
            "Mokova",
            "Ignis",
        ],
        "special_bosses": {},
    },
}

VG_MAPPER = {
    "00h00": "VG CBA",
    "00h20": "VG FORGOTEN LAND",
    "00h40": "VG IRON 1",
    "01h00": "VG CN H",
    "01h20": "VG RUINEM",
    "01h40": "VG DUNGEON 1",
    "02h00": "VG ET2",
    "02h40": "VG LAB",
    "03h20": "VG CT 1",
    "03h40": "VG CBA",
    "04h00": "VG CT 1",
    "04h20": "VG ABISS",
    "04h40": "VG RUINEM",
    "05h00": "VG IRON 1",
    "05h20": "VG FORGOTEN LAND",
    "05h40": "VG CN H",
    "06h00": "VG DS",
    "06h20": "VG RUINEM",
    "06h40": "VG DUNGEON 1",
    "07h00": "VG ET 2",
    "07h20": "VG CT 1",
    "07h40": "VG CBA",
    "08h00": "VG FORGOTEN LAND",
    "08h20": "VG DS 1",
    "08h40": "VG LAB 1",
    "09h00": "VG IRON 1",
    "09h20": "VG FORGOTEN LAND",
    "09h40": "VG CBA",
    "10h00": "VG CBA",
    "10h20": "VG ICE 2",
    "10h40": "VG ABISS",
    "11h00": "VG DUNGEON 1",
    "11h20": "VG CT1 ",
    "11h40": "VG IRON 1",
    "12h00": "VG BC",
    "12h40": "VG RUINEM",
    "13h00": "VG DUNGEON 1",
    "13h20": "VG FORGOTEN LAND",
    "13h40": "VG CBA",
    "14h00": "VG ET 2",
    "14h20": "VG DS ",
    "14h40": "VG IRON 1",
    "15h00": "VG RUINEM",
    "15h20": "VG LAB",
    "15h40": "VG FORGOTEN LAND",
    "16h00": "VG DUNGEON 1",
    "16h20": "VG CBA",
    "16h40": "VG DS",
    "17h00": "VG IRON 1",
    "17h20": "VG ABISS",
    "17h40": "VG CT1",
    "18h00": "VG RUINEM ",
    "18h20": "VG CBA",
    "18h40": "VG FORGOTEN LAND ",
    "19h00": "VG DS 3",
    "19h20": "VG CN H",
    "19h40": "VG DUNGEON 1",
    "20h00": "VG IRON 1",
    "20h20": "VG FORGOTEN LAND",
    "20h40": "VG RUINEM",
    "21h00": "VG DS",
    "21h20": "VG RUINEM",
    "21h40": "VG ET 2",
    "22h00": "VG DUNGEON 1",
    "22h20": "VG FORGOTEN LAND",
    "22h40": "VG LAB",
    "23h00": "VG IRON 1",
}
