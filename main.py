import asyncio
import logging
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from gtts import gTTS

from configs import (
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


async def connect_to_voice() -> Optional[discord.VoiceClient]:
    global voice_client

    try:
        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        if not voice_channel:
            logger.error(f"Canal de voz {VOICE_CHANNEL_ID} não encontrado!")
            return None

        existing_client = voice_channel.guild.voice_client

        if existing_client:
            if (
                existing_client.channel
                and existing_client.channel.id == VOICE_CHANNEL_ID
            ):
                if existing_client.is_connected():
                    logger.info("✅ Já conectado no canal correto")
                    voice_client = existing_client
                    return voice_client

                logger.warning("🔄 Conexão existente mas não ativa, limpando...")
                try:
                    await existing_client.disconnect(force=True)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Erro ao desconectar cliente existente: {e}")
            else:
                logger.info("🔄 Movendo para canal correto...")
                try:
                    await existing_client.move_to(voice_channel)
                    voice_client = existing_client
                    logger.info(f"✅ Movido para {voice_channel.name}")
                    return voice_client
                except Exception as e:
                    logger.warning(f"Erro ao mover canal: {e}, tentando desconectar...")
                    await existing_client.disconnect(force=True)
                    await asyncio.sleep(0.5)

        logger.info(f"🔌 Conectando ao canal {voice_channel.name}...")
        voice_client = await voice_channel.connect(timeout=10.0, reconnect=True)
        logger.info("✅ Conectado com sucesso!")
        return voice_client

    except discord.ClientException as e:
        if "Already connected" in str(e):
            logger.warning("⚠️ Discord detectou conexão existente")

            voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
            if voice_channel and voice_channel.guild.voice_client:
                existing_client = voice_channel.guild.voice_client
                if existing_client.is_connected():
                    voice_client = existing_client
                    logger.info("✅ Usando conexão existente")
                    return voice_client

            logger.info("🔄 Forçando nova conexão...")
            try:
                if voice_channel and voice_channel.guild.voice_client:
                    await voice_channel.guild.voice_client.disconnect(force=True)
                    await asyncio.sleep(1)

                voice_client = await voice_channel.connect(timeout=10.0, reconnect=True)
                logger.info("✅ Nova conexão estabelecida!")
                return voice_client

            except Exception as retry_error:
                logger.exception(f"Falha na reconexão: {retry_error}")
                return None
        else:
            logger.exception(f"Erro de conexão: {e}")
            return None

    except Exception as e:
        logger.exception(f"Erro inesperado: {e}")
        return None


async def play_audio(message: str) -> bool:
    try:
        global voice_client

        voice_client = await connect_to_voice()
        if not voice_client:
            logger.exception("Não foi possível conectar ao canal de voz")
            return False

        if not voice_client.is_connected():
            logger.exception("Cliente não está conectado, tentando reconectar...")
            voice_client = await connect_to_voice()
            if not voice_client or not voice_client.is_connected():
                logger.error("Falha na reconexão")
                return False

        if voice_client.is_playing():
            logger.info("Parando áudio atual...")
            voice_client.stop()
            await asyncio.sleep(0.5)

        logger.info("Gerando áudio em memória...")

        tts = gTTS(text=message, lang="pt", tld="com.br")
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        finished = asyncio.Event()
        playback_error = None

        def after_play(err):
            nonlocal playback_error
            if err:
                playback_error = err
                logger.error(f"Erro na reprodução: {err}")
            finished.set()

        audio_source = discord.FFmpegPCMAudio(
            audio_buffer,
            executable=FFMPEG_PATH,
            options="-vn -ar 44100 -ac 2 -b:a 192k -loglevel error",
            pipe=True,
        )

        logger.info("▶️ Iniciando reprodução do áudio...")
        voice_client.play(audio_source, after=after_play)

        try:
            await asyncio.wait_for(finished.wait(), timeout=30.0)
        except asyncio.TimeoutError:
            logger.exception("Timeout na reprodução")
            if voice_client.is_playing():
                voice_client.stop()
            return False

        if playback_error:
            logger.exception(f"Erro durante reprodução: {playback_error}")
            return False

        logger.info("✅ Áudio reproduzido com sucesso usando memória!")
        return True

    except Exception as e:
        logger.exception(f"Erro no play_audio: {e}")
        return False


@bot.command(name="reconectar", aliases=["reconnect", "volta"])
async def force_reconnect(ctx):
    global voice_client

    logger.info(f"Reconexão forçada solicitada por {ctx.author}")

    try:
        await ctx.send("Iniciando reconexão forçada...")

        if voice_client:
            try:
                if voice_client.is_connected():
                    await voice_client.disconnect(force=True)
                    logger.info("Voice client global desconectado")
            except Exception as e:
                logger.warning(f"Erro ao desconectar voice_client global: {e}")
            finally:
                voice_client = None

        for guild in bot.guilds:
            if guild.voice_client:
                try:
                    await guild.voice_client.disconnect(force=True)
                    logger.info(f"Desconectado do guild: {guild.name}")
                except Exception as e:
                    logger.warning(f"Erro ao desconectar do guild {guild.name}: {e}")

        await asyncio.sleep(2)
        await ctx.send("Conexões antigas limpas...")

        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        if not voice_channel:
            await ctx.send(f"Canal de voz {VOICE_CHANNEL_ID} não encontrado!")
            return

        await ctx.send(f"🔌 Conectando ao canal {voice_channel.name}...")

        voice_client = await voice_channel.connect(timeout=15.0, reconnect=True)

        if voice_client and voice_client.is_connected():
            await ctx.send(
                f"Reconectado com sucesso! 🎉\n🔊 Canal: {voice_channel.name}",
            )
            logger.info(
                f"Reconexão forçada bem-sucedida no canal {voice_channel.name}",
            )

        else:
            await ctx.send(
                "Falha na reconexão. Verifique permissões e tente novamente.",
            )
            logger.exception("Falha na reconexão forçada")

    except discord.ClientException as e:
        error_msg = str(e)
        if "Already connected" in error_msg:
            await ctx.send(
                "⚠️ Discord detectou conexão existente. Tentando usar a conexão atual...",
            )

            voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
            if voice_channel and voice_channel.guild.voice_client:
                voice_client = voice_channel.guild.voice_client
                await ctx.send("✅ Usando conexão existente!")
            else:
                await ctx.send("Não foi possível resolver o conflito de conexão")
        else:
            await ctx.send(f"Erro Discord: {error_msg[:100]}")
            logger.exception(f"Erro ClientException na reconexão: {e}")

    except Exception as e:
        await ctx.send(f"Erro inesperado: {str(e)[:100]}")
        logger.exception(f"Erro inesperado na reconexão forçada: {e}")


@bot.command(name="status")
async def voice_status(ctx):
    global voice_client

    embed = discord.Embed(title="Status da Conexão de Voz", color=0x00FF00)

    if voice_client:
        embed.add_field(
            name="Voice Client Global",
            value=f"Conectado: {voice_client.is_connected()}\n"
            f"Canal: {voice_client.channel.name if voice_client.channel else 'Nenhum'}\n"
            f"Tocando: {voice_client.is_playing()}",
            inline=False,
        )
    else:
        embed.add_field(name="Voice Client Global", value="Nenhum", inline=False)

    guild_status = []
    for guild in bot.guilds:
        if guild.voice_client:
            status = (
                f"{guild.name}: {guild.voice_client.channel.name if guild.voice_client.channel else 'Canal desconhecido'}",
            )
        else:
            status = f"{guild.name}: Desconectado"
        guild_status.append(status)

    if guild_status:
        embed.add_field(
            name="Status por Servidor",
            value="\n".join(guild_status),
            inline=False,
        )

    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        embed.add_field(
            name="Canal Configurado",
            value=f"{voice_channel.name} ({voice_channel.guild.name})",
            inline=False,
        )
    else:
        embed.add_field(
            name="Canal Configurado",
            value="Canal não encontrado",
            inline=False,
        )

    await ctx.send(embed=embed)


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
    load_dotenv()
    max_retries = 5
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa de conexão {attempt + 1}/{max_retries}")
            bot.run(BOT_TOKEN)
            break
        except Exception as e:
            logger.critical(f"Erro na tentativa {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Aguardando {retry_delay}s para tentar novamente...")
                asyncio.sleep(retry_delay)
            else:
                logger.critical("Todas as tentativas falharam")
