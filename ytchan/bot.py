import discord
from discord.ext import commands
import youtube_dl

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YDL_OPTIONS = {'format': 'bestaudio'}

# You should change this.
# OUTPUT_EMOJIS = {'now_playing': ':ASgaztonrainbow:', 'not_in_vc': ':ASRemHmph:', 'error': ':Asevil:'}
OUTPUT_EMOJIS = {'now_playing': ':musical_note:',
                 'not_in_vc': ':warning:', 'error': ':bangbang:'}


class YTChan(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Q = None
        self.now_playing = None
        self.vc = None

    def _get_video(self, url):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                is_playlist = False
                if entries in info.keys():
                    source = info['entries']
                    is_playlist = True
                else:
                    source = info['formats'][0]['url']

                return source, is_playlist, False

            except Exception as e:
                print(f"Could not retrieve youtube video(s) correctly: {url}")
                return None, False, True

    @commands.command()
    async def play(self, ctx, url):
        # Make sure the voice channel is not empty
        if ctx.author.voice is None:
            await ctx.send(f"> {OUTPUT_EMOJIS['not_in_vc']} **You need to be in a voice channel before playing any song.**")

        # Join the voice channel or move to the correct voice channel
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        self.vc = ctx.voice_client

        if 'entries' in info.keys():
            # This is a list
            await ctx.send(f"> {OUTPUT_EMOJIS['error']} **Operation not supported**")
        else:
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("> **Paused** :play_pause:")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("> **Player resumed** :play_pause:")

    @commands.command()
    async def stop(self, ctx):
        pass

    @commands.command()
    async def skip(self, ctx):
        pass

    @commands.command()
    async def skipto(self, ctx, song_index):
        pass
