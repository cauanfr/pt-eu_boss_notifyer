import asyncio
import logging
import os
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("boss-rotator")

BOT_TOKEN = os.getenv("BOT_TOKEN")
VOICE_CHANNEL_ID = os.getenv("VOICE_CHANNEL_ID")
AUDIO_PATH = os.path.join("audios", "audio.mp3")
FFMPEG_PATH = "ffmpeg"


intents = discord.Intents.all()
bot = commands.Bot("~", intents=intents)

BOSS_ROTATION = {
    0: ["Valento", "Kelvezu", "Gorgoniac", "Draxos", "Eadric/Vault"],
    1: ["Chaos Queen", "Blood Prince", "Devil Shy", "Primal Golem"],
    2: ["Valento", "Mokova", "Tulla"],
    3: [
        "Chaos Queen",
        "Kelvezu",
        "Gorgoniac",
        "Deius",
        "Greedy",
        "Aragonian",
        "Eadric/Vault",
    ],
    4: ["Valento", "Blood Prince", "Draxos", "Yagditha"],
    5: ["Chaos Queen", "Mokova", "Devil Shy", "Ignis"],
    6: ["Valento", "Kelvezu", "Gorgoniac", "Tulla", "Eadric/Vault"],
    7: ["Chaos Queen", "Blood Prince", "Eadric/Vault", "Primal Golem (H)"],
    8: ["Valento", "Mokova", "Draxos"],
    9: [
        "Chaos Queen",
        "Kelvezu",
        "Gorgoniac",
        "Devil Shy",
        "Greedy",
        "Aragonian",
        "Eadric/Vault",
    ],
    10: ["Valento", "Blood Prince", "Yagditha", "Tulla"],
    11: ["Chaos Queen", "Mokova", "Ignis"],
}


def get_seconds_until_minute(minute: int) -> int:
    now = datetime.now()
    target = now.replace(minute=minute, second=0, microsecond=0)

    if now >= target:
        target += timedelta(hours=1)

    return int((target - now).total_seconds())


def format_time(seconds: int) -> str:
    minutes, secs = divmod(seconds, 60)
    return f"{minutes}m {secs}s" if minutes else f"{secs}s"


def generate_tts_audio(message: str):
    logger.info("Gerando áudio para a mensagem.")
    message = message.replace(" -> ", ", ")
    os.makedirs("audios", exist_ok=True)
    tts = gTTS(text=message, lang="pt")
    tts.save(AUDIO_PATH)
    logger.info("Áudio salvo com sucesso em 'audios/audio.mp3'")


def delete_tts_audio():
    if os.path.exists(AUDIO_PATH):
        os.remove(AUDIO_PATH)
        logger.info("Áudio antigo deletado.")


async def play_audio(voice_channel: discord.VoiceChannel, message: str):
    try:
        generate_tts_audio(message)
        await asyncio.sleep(1)

        if voice_channel:
            logger.info("Conectando ao canal de voz.")
            vc = await voice_channel.connect()

            if os.path.isfile(AUDIO_PATH):
                logger.info("Tocando áudio no canal de voz.")
                vc.play(discord.FFmpegPCMAudio(AUDIO_PATH, executable=FFMPEG_PATH))

                while not vc.is_playing():
                    await asyncio.sleep(0.1)
                while vc.is_playing():
                    await asyncio.sleep(1)

            await vc.disconnect()
            logger.info("Desconectado do canal de voz.")

    except Exception as e:
        logger.exception(
            f"Erro durante envio ou reprodução de áudio: {e}.",
        )


@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")
    boss_rotation_scheduler.start()


@tasks.loop(count=1)
async def boss_rotation_scheduler():
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)

    logger.info("Esperando até o minuto 25.")
    await asyncio.sleep(get_seconds_until_minute(25))

    current_hour = datetime.now().hour
    next_hour = current_hour % 24
    mapped_hour = next_hour % 12
    boss_list = BOSS_ROTATION.get(mapped_hour, [])
    message = f"5 minutos para à próxima rotação de BOSS: {' -> '.join(boss_list)}."

    logger.info("Executando ação no minuto 25.")
    await play_audio(voice_channel, message)

    logger.info("Esperando até o minuto 28.")
    await asyncio.sleep(get_seconds_until_minute(28))

    logger.info("Executando ação no minuto 28.")
    message = f"2 minutos para à próxima rotação de BOSS: {' -> '.join(boss_list)}."
    await play_audio(voice_channel, message)

    next_wait = get_seconds_until_minute(25)
    formatted = format_time(next_wait)

    logger.info(f"Próxima execução em: {formatted}.")

    boss_rotation_scheduler.restart()


if __name__ == "__main__":
    try:
        logger.info("Iniciando o bot...")
        bot.run(BOT_TOKEN)
    except Exception as e:
        logger.critical(f"Erro crítico ao iniciar o bot: {e}")
