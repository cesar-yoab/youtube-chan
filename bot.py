import os
import argparse
import discord
from discord.ext import commands
import youtube_dl

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best'}


class YTChan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel before calling the bot.")

    @commands.command()
    async def play(self, ctx, url):
        # Make sure the voice channel is not empty
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel before playing any song.")

        # Join the voice channel or move to the correct voice channel
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)

            if 'entries' in info.keys():
                # This is a list
                pass
            else:
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused :play_pause:")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Player resumed :play_pause:")


def setup_client(client):
    """Adds cog to client with class YTChan.

    Args:
        client (discord.ext.commands.Bot): Discord client.
    """
    client.add_cog(YTChan(client))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process runs the YouTube Chan discord bot.")

    parser.add_argument(
        "--token", help="Discord bot token", required=True, metavar="[T]")
    parser.add_argument(
        "--prefix", help="Set the command prefix to be used by the bot, defaults to '?'", default="?", metavar="[prefix]")

    args = parser.parse_args()
    # Start client
    client = commands.Bot(command_prefix=args.prefix,
                          intents=discord.Intents.all())

    setup_client(client)
    try:
        client.run(args.token)
    except Exception as e:
        print(f"Could not start client: {e}")
