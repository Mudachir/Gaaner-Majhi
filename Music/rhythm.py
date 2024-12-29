import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    @client.event
    async def on_ready():
        print(f'{client.user} is now online!')

    @client.event
    async def on_message(message):
        if message.content.startswith("/play"):
            try:
                if message.author.voice:
                    channel = message.author.voice.channel
                    if message.guild.id not in voice_clients:
                        voice_client = await channel.connect()
                        voice_clients[message.guild.id] = voice_client
                    else:
                        voice_client = voice_clients[message.guild.id]

                    url = message.content.split()[1]
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                    song = data['url']
                    print(f"Playing song: {song}")
                    voice_client.play(discord.FFmpegPCMAudio(song, **ffmpeg_options))
                else:
                    await message.channel.send("You need to be in a voice channel to use this command.")
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send(f"An error occurred: {e} because queue system is't available right now")

    client.run(TOKEN)
