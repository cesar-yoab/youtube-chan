import discord
import asyncio
import threading
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from ytqueue import YTQueue

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# You should change this.
# OUTPUT_EMOJIS = {'now_playing': ':ASgaztonrainbow:', 'not_in_vc': ':ASRemHmph:', 'error': ':Asevil:'}
OUTPUT_EMOJIS = {'now_playing': ':musical_note:',
                 'not_in_vc': ':warning:', 'error': ':bangbang:'}


class YTChan(commands.Cog):
    def __init__(self, client, max_q_size=30):
        self.client = client
        self.Q = YTQueue(max_q_size)
        self.now_playing = None
        self.vc = None
        self.current_ctx = None

    @commands.command()
    async def play(self, ctx, url):
        if not url:
            await ctx.send(f"> {OUTPUT_EMOJIS['error']} **Usage:** ?play VIDEO_URL")
            return

        # Make sure the voice channel is not empty
        if ctx.author.voice is None:
            await ctx.send(f"> {OUTPUT_EMOJIS['not_in_vc']} **You need to be in a voice channel before playing any song.**")
            return

        # Join the voice channel or move to the correct voice channel
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        self.vc = ctx.voice_client
        await ctx.send("> :mag_right: **Searching...**")
        err, msg = self.Q.add(
            url, ctx.author.display_name, ctx.author.avatar_url)

        if err:
            await ctx.send(f"> {OUTPUT_EMOJIS['error']} Could not download video")
            return

        self.current_ctx = ctx
        if ctx.voice_client.is_playing():
            await ctx.send(f"> {msg}")
            return

        if self.now_playing is None:
            await self._play_next()

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
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        self.Q.clear()
        await ctx.send("> **Player stopped and queued has been cleared**")

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        self._play_next()

    @commands.command()
    async def skipto(self, ctx, song_index):
        ctx.voice_client.stop()
        song = self.Q.next_to(song_index)
        if not song:
            await ctx.send(f"> {OUTPUT_EMOJIS['error']} **Invalid index**")

    async def _play_next(self, e=None):
        if e is not None:
            print(e)

        if self.Q.is_empty():
            self.now_playing = None
            return

        song = self.Q.next()
        self.now_playing = song
        source = await discord.FFmpegOpusAudio.from_probe(song['source'], **FFMPEG_OPTIONS)
        self.vc.play(source, after=self._play_next)
        await self._now_playing()

    async def _now_playing(self):
        video_name = self.now_playing['title']
        embed = discord.Embed(title=f"{OUTPUT_EMOJIS['now_playing']} == Now playing == {OUTPUT_EMOJIS['now_playing']}\n{video_name}",
                              url="https://google.com",
                              color=discord.Color.blue())

        embed.set_author(
            name=self.now_playing['requestedBy'], icon_url=self.now_playing['requestedByAvatar'])
        embed.set_thumbnail(url=self.now_playing['thumbnail'])
        await self.current_ctx.sed(embed=embed)
