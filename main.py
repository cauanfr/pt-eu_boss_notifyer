import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()
from configs import (
    AUDIO_PATH,
    BOSS_ROTATION,
    BOT_TOKEN,
    DEIUS_MINUTES,
    FURY_MINUTES,
    VOICE_CHANNEL_ID,
    FFMPEG_PATH,
    GMT_MINUS_3,
    ROTATION_MINUTES,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("boss-rotator")


intents = discord.Intents.all()
bot = commands.Bot("~", intents=intents)


def get_seconds_until(hour: int, minute: int) -> int:
    now = datetime.now(GMT_MINUS_3)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


def get_next_event():
    events = []

    for hour in range(24):
        mapped_hour = hour % 12
        data = BOSS_ROTATION[mapped_hour]

        rotation_minutes = ROTATION_MINUTES.split(";")
        for i, minute in enumerate(rotation_minutes):
            events.append(
                {
                    "hour": hour,
                    "minute": int(minute),
                    "type": "rotation",
                    "boss_list": data["rotation"],
                    "seconds": get_seconds_until(hour, int(minute)),
                    "is_first": i == 0,
                    "rotation_minutes": rotation_minutes,
                }
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
            events.append(
                {
                    "hour": hour,
                    "minute": minute,
                    "type": "special",
                    "boss_list": data["rotation"],
                    "seconds": get_seconds_until(hour, minute),
                    "special_bosses": info["bosses"],
                    "is_first": info["is_first"],
                }
            )

    return min(events, key=lambda x: x["seconds"])


async def play_audio(message: str):
    try:
        os.makedirs("audios", exist_ok=True)
        tts = gTTS(text=message, lang="pt")
        tts.save(AUDIO_PATH)

        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        if voice_channel:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(AUDIO_PATH, executable=FFMPEG_PATH))

            while vc.is_playing():
                await asyncio.sleep(1)

            await vc.disconnect()
    except Exception as e:
        logger.exception(f"Erro no áudio: {e}")


@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")
    scheduler.start()


@tasks.loop(count=1)
async def scheduler():
    event = get_next_event()
    logger.info(
        f"Próximo: {event['type']} em {event['seconds']}s às {event['hour']:02d}:{event['minute']:02d}"
    )

    await asyncio.sleep(event["seconds"])

    boss_list = ", ".join(event["boss_list"])

    if event["type"] == "rotation":
        if event["is_first"]:
            message = f"5 minutos para a próxima rotação: {boss_list}"
        else:
            message = f"2 minutos para a próxima rotação: {boss_list}"

    elif event["type"] == "special":
        bosses = event["special_bosses"]
        if event["is_first"]:
            if len(bosses) == 1:
                message = f"5 minutos para o spawn do boss: {bosses[0]}."
            else:
                boss_names = " e ".join(bosses)
                message = f"5 minutos para o spawn dos bosses: {boss_names}."
        else:
            minutes_until = int(FURY_MINUTES.split(";")[1]) - 60
            if len(bosses) == 1:
                message = f"2 minutos para o spawn do boss {bosses[0]}."
            else:
                boss_names = " e ".join(bosses)
                message = f"2 minutos para o spawn dos bosses: {boss_names}."

    logger.info(message)
    await play_audio(message)

    scheduler.restart()


if __name__ == "__main__":
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        logger.critical(f"Erro: {e}")
