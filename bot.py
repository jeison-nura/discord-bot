import discord
import yt_dlp
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

 
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Buenas hijos de su puta madre {bot.user}!')

async def get_audio_stream(url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)
                if 'url' in info_dict:
                    return info_dict['url'], info_dict.get('title', 'Canción desconocida')
                elif 'formats' in info_dict:
                    # Try to find a format with audio
                    for fmt in info_dict['formats']:
                        if fmt.get('acodec') != 'none' and fmt.get('acodec') is not None:
                            return fmt['url'], info_dict.get('title', 'Canción desconocida')
                    # If no specific audio format found, use the best available
                    if len(info_dict['formats']) > 0:
                        return info_dict['formats'][-1]['url'], info_dict.get('title', 'Canción desconocida')
                return None, None
            except Exception as e:
                print(f"Error al obtener el audio: {e}")
                return None, None
            
# Comando para reproducir música
@bot.command()
async def play(ctx, *, url: str):  # Añadido * para permitir espacios en la URL
    # Asegúrate de que el usuario esté en un canal de voz
    voice_channel = ctx.author.voice
    if not voice_channel:
        await ctx.send("Debes estar en un canal de voz para usar este comando.")
        return
    
    # Obtener el canal de voz
    vc = ctx.guild.voice_client
    if not vc:
        # Unirse al canal de voz
        try:
            vc = await voice_channel.channel.connect()
        except discord.errors.ClientException as e:
            await ctx.send(f"Error al unirse al canal de voz: {e}")
            return
    
    # Mostrar mensaje de carga
    loading_msg = await ctx.send("Cargando audio, por favor espera...")
    
    # Obtener el audio de YouTube
    audio_url, title = await get_audio_stream(url)
    if not audio_url:
        await loading_msg.edit(content="No se pudo obtener el audio de la URL proporcionada.")
        return
    
    # Reproducir el audio
    try:
        # Mejores opciones para FFmpeg para evitar interrupciones
        ffmpeg_options = {
            'executable': 'C:/Users/jeison/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe',
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10M -analyzeduration 10M',
            'options': '-vn -bufsize 8192k'
        }
        
        # Detener cualquier reproducción actual antes de iniciar una nueva
        if vc.is_playing():
            vc.stop()
        
        # Definir una función para manejar cuando la canción termina
        def after_playing(error):
            if error:
                print(f"Error en la reproducción: {error}")
                asyncio.run_coroutine_threadsafe(
                    ctx.send(f"Error durante la reproducción: {error}"),
                    bot.loop
                )
            else:
                # Enviar mensaje y desconectar el bot cuando termine la canción
                asyncio.run_coroutine_threadsafe(
                    ctx.send("🎵 La canción ha terminado. ¡Desconectando!"),
                    bot.loop
                )
                coro = vc.disconnect()
                fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                try:
                    fut.result()
                except Exception as e:
                    print(f"Error al desconectar: {e}")
        
        vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=after_playing)
        await loading_msg.edit(content=f"🎵 Reproduciendo: **{title}**")
    except Exception as e:
        await loading_msg.edit(content=f"Error al reproducir la música: {e}")
        

@bot.command()
async def stop(ctx):
    vc = ctx.guild.voice_client
    if vc:
        vc.stop()
        await vc.disconnect()
        await ctx.send("Reproducción detenida y bot desconectado.")
    else:
        await ctx.send("El bot no está conectado a un canal de voz.")

# Añadir comandos de pausa y reanudar
@bot.command()
async def pause(ctx):
    vc = ctx.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("⏸️ Reproducción pausada.")
    else:
        await ctx.send("No hay nada reproduciéndose actualmente.")

@bot.command()
async def resume(ctx):
    vc = ctx.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Reproducción reanudada.")
    else:
        await ctx.send("No hay nada pausado actualmente.")

bot.run(os.getenv('DCTOKEN'))