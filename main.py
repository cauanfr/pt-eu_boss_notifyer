import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from gtts import gTTS

from configs import (
    AUDIO_PATH,
    BOSS_ROTATION,
    BOT_TOKEN,
    FFMPEG_PATH,
    GMT_MINUS_3,
    ROTATION_MINUTES,
    VG_MAPPER,
    VOICE_CHANNEL_ID,
)
from custom_types import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("boss-rotator")


intents = discord.Intents.all()
bot = commands.Bot("~", intents=intents)
voice_client: Optional[discord.VoiceClient] = None


def get_seconds_until(hour: int, minute: int) -> int:
    now = datetime.now(GMT_MINUS_3)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


def format_event_message(boss_list: str, ev_type: str, is_first: bool = True) -> str:
    def _rotation_message(bosses: str, is_first: bool) -> str:
        minutes = "5" if is_first else "2"
        return f"{minutes} minutos para a próxima rotação: {bosses}"

    if ev_type == "default":
        return _rotation_message(boss_list, is_first)

    elif ev_type == "special":
        return _rotation_message(boss_list, is_first)

    elif ev_type == "vg":
        return f"Atenção! Próxima rotação: VG {boss_list}"

    return "Evento desconhecido."


def get_next_event() -> EventType:
    events: list[EventType] = []

    for hour in range(24):
        mapped_hour = hour % 12
        data = BOSS_ROTATION[mapped_hour]

        rotation_minutes = ROTATION_MINUTES.split(";")
        for i, minute in enumerate(rotation_minutes):
            boss_list = ", ".join(data["rotation"])
            events.append(
                {
                    "hour": hour,
                    "minute": int(minute),
                    "type": "default",
                    "message": format_event_message(
                        boss_list=boss_list,
                        ev_type="default",
                        is_first=i == 0,
                    ),
                    "seconds": get_seconds_until(hour, int(minute)),
                    "rotation_minutes": rotation_minutes,
                },
            )

        special_by_minute = {}
        for boss, minutes in data["special_bosses"].items():
            for i, minute in enumerate(minutes.split(";")):
                minute = int(minute)
                if minute not in special_by_minute:
                    special_by_minute[minute] = {"bosses": [], "is_first": i == 0}
                special_by_minute[minute]["bosses"].append(boss)
                if i == 0:
                    special_by_minute[minute]["is_first"] = True

        for minute, info in special_by_minute.items():
            boss_list = ", ".join(info["bosses"])
            events.append(
                {
                    "hour": hour,
                    "minute": minute,
                    "type": "special",
                    "message": format_event_message(
                        boss_list=boss_list,
                        ev_type="special",
                        is_first=info["is_first"],
                    ),
                    "seconds": get_seconds_until(hour, minute),
                },
            )

        for key, value in VG_MAPPER.items():
            hour, minute = key.split("h")
            hour = int(hour)
            minute = int(minute)

            events.append(
                {
                    "hour": hour,
                    "minute": minute,
                    "type": "vg",
                    "boss_list": value,
                    "is_first": True,
                    "message": format_event_message(
                        boss_list=value,
                        ev_type="vg",
                    ),
                    "seconds": get_seconds_until(hour, minute),
                    "rotation_minutes": [minute],
                },
            )

    return min(events, key=lambda x: x["seconds"])


async def connect_to_voice() -> discord.VoiceClient:
    global voice_client

    if voice_client is None or not voice_client.is_connected():
        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        voice_client = await voice_channel.connect(reconnect=True)
        return voice_client

    return voice_client


async def play_audio(message: str) -> None:
    try:
        global voice_client
        os.makedirs("audios", exist_ok=True)
        tts = gTTS(text=message, lang="pt")
        tts.save(AUDIO_PATH)

        voice_client = await connect_to_voice()

        finished = asyncio.Event()

        def after_play(err):
            if err:
                logger.error(f"Erro no áudio (after_play): {err}")
            finished.set()

        audio = discord.FFmpegPCMAudio(
            AUDIO_PATH,
            executable=FFMPEG_PATH,
            options="-vn -ar 44100 -ac 2 -b:a 192k",
        )
        voice_client.play(audio, after=after_play)

        await finished.wait()

    except Exception as e:
        logger.exception(f"Erro no áudio: {e}")


@bot.event
async def on_ready():
    global voice_client
    voice_client = await connect_to_voice()

    logger.info(f"Bot conectado como {bot.user}")
    scheduler.start()


@tasks.loop(count=1)
async def scheduler():
    event = get_next_event()
    ev_type = event["type"]
    ev_seconds = event["seconds"]
    ev_hour = f"{event['hour']:2d}"
    ev_minute = f"{event['minute']:2d}"
    ev_message = event["message"]

    logger.info(f"Próximo: {ev_type} em {ev_seconds}s às {ev_hour}:{ev_minute}")
    logger.info(ev_message)

    await asyncio.sleep(event["seconds"])

    await play_audio(ev_message)

    scheduler.restart()


if __name__ == "__main__":
    try:
        load_dotenv()
        bot.run(BOT_TOKEN)
    except Exception as e:
        logger.critical(f"Erro: {e}")
