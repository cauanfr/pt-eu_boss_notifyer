import os
from datetime import timedelta, timezone

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
