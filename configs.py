import os
from datetime import timedelta, timezone

from dotenv import load_dotenv

from custom_types import BossRotation

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "0"))
AUDIO_PATH = os.path.join("audios", "audio.mp3")
GMT_MINUS_3 = timezone(timedelta(hours=-3))
FFMPEG_PATH = "ffmpeg"


ROTATION_MINUTES = os.getenv("ROTATION_MINUTES", "25;28")
FURY_MINUTES = os.getenv("FURY_MINUTES", "55;58")
DEIUS_MINUTES = os.getenv("DEIUS_MINUTES", "55;58")


BOSS_ROTATION: dict[int, BossRotation] = {
    0: {
        "rotation": [
            "Valento",
            "Kelvezu",
            "Gorgoniac",
            "Draxos",
            "Eadric/Vault",
        ],
        "special_bosses": {},
    },
    1: {
        "rotation": [
            "Chaos Queen",
            "Blood Prince",
            "Devil Shy",
            "Primal Golem",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
        },
    },
    2: {
        "rotation": [
            "Valento",
            "Mokova",
            "Tulla",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
        },
    },
    3: {
        "rotation": [
            "Chaos Queen",
            "Kelvezu",
            "Gorgoniac",
            "Greedy",
            "Aragonian",
            "Eadric/Vault",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
        },
    },
    4: {
        "rotation": [
            "Valento",
            "Blood Prince",
            "Draxos",
            "Yagditha",
        ],
        "special_bosses": {},
    },
    5: {
        "rotation": [
            "Chaos Queen",
            "Mokova",
            "Devil Shy",
            "Ignis",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
            "Furia": FURY_MINUTES,
        },
    },
    6: {
        "rotation": [
            "Valento",
            "Kelvezu",
            "Gorgoniac",
            "Tulla",
            "Eadric/Vault",
        ],
        "special_bosses": {},
    },
    7: {
        "rotation": [
            "Chaos Queen",
            "Blood Prince",
            "Eadric/Vault",
            "Primal Golem (H)",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
        },
    },
    8: {
        "rotation": [
            "Valento",
            "Mokova",
            "Draxos",
        ],
        "special_bosses": {
            "Furia": FURY_MINUTES,
        },
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
        "special_bosses": {},
    },
    11: {
        "rotation": [
            "Chaos Queen",
            "Mokova",
            "Ignis",
        ],
        "special_bosses": {
            "Deius": DEIUS_MINUTES,
            "Furia": FURY_MINUTES,
        },
    },
}

VG_MAPPER: dict[str, str] = {
    "00h00": "CBA",
    "00h20": "Forgoten Land",
    "00h40": "Iron 1",
    "01h00": "CN H",
    "01h20": "Ruinem",
    "01h40": "Dungeon 1",
    "02h00": "E.T. 2",
    "02h40": "LAB",
    "03h20": "CT 1",
    "03h40": "CBA",
    "04h00": "CT 1",
    "04h20": "Abiss",
    "04h40": "Ruinem",
    "05h00": "Iron 1",
    "05h20": "Forgoten Land",
    "05h40": "CN H",
    "06h00": "DS",
    "06h20": "Ruinem",
    "06h40": "Dungeon 1",
    "07h00": "E.T. 2",
    "07h20": "CT 1",
    "07h40": "CBA",
    "08h00": "Forgoten Land",
    "08h20": "DS 1",
    "08h40": "LAB 1",
    "09h00": "Iron 1",
    "09h20": "Forgoten Land",
    "09h40": "CBA",
    "10h00": "CBA",
    "10h20": "ICE 2",
    "10h40": "Abiss",
    "11h00": "Dungeon 1",
    "11h20": "CT1 ",
    "11h40": "Iron 1",
    "12h00": "BC",
    "12h40": "Ruinem",
    "13h00": "Dungeon 1",
    "13h20": "Forgoten Land",
    "13h40": "CBA",
    "14h00": "E.T. 2",
    "14h20": "DS ",
    "14h40": "Iron 1",
    "15h00": "Ruinem",
    "15h20": "LAB",
    "15h40": "Forgoten Land",
    "16h00": "Dungeon 1",
    "16h20": "CBA",
    "16h40": "DS",
    "17h00": "Iron 1",
    "17h20": "Abiss",
    "17h40": "CT1",
    "18h00": "Ruinem",
    "18h20": "CBA",
    "18h40": "Forgoten Land ",
    "19h00": "DS 3",
    "19h20": "CN H",
    "19h40": "Dungeon 1",
    "20h00": "Iron 1",
    "20h20": "CT1",
    "20h40": "Ruinem",
    "21h00": "DS",
    "21h20": "Ruinem",
    "21h40": "E.T. 2",
    "22h00": "Dungeon 1",
    "22h20": "Forgoten Land",
    "22h40": "LAB",
    "23h00": "Iron 1",
}
