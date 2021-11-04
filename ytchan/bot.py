import discord
import asyncio
import threading
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from voice_state import VoiceState
from song import Song, YTDError

# You should change this.
# OUTPUT_EMOJIS = {'now_playing': ':ASgaztonrainbow:', 'not_in_vc': ':ASRemHmph:', 'error': ':Asevil:'}
OUTPUT_EMOJIS = {'now_playing': ':musical_note:',
                 'not_in_vc': ':warning:', 'error': ':bangbang:'}


class YTChan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_state = None

    def get_voice_state(self, ctx: commands.Context):
        if not self.voice_state:
            self.voice_state = VoiceState(self.bot, ctx)

        return self.voice_state

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f"> {OUTPUT_EMOJIS['error']} **An error occurred:**\n{str(error)}")

    @commands.command(name="join", invoke_without_subcommand=True)
    async def join(self, ctx: commands.Context):
        """Join voice channel"""
        channel = ctx.author.voice.channel

        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(channel)
            return

        ctx.voice_state.voice = await channel.connect()

    @commands.command(name="pause")
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.send("> **Player paused**")

    @commands.command(name="resume")
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.send("> **Resumed**")

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            await ctx.voice_state.stop()
            await ctx.send("> **Player stopped and queue cleared**")

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, url: str):
        """Plays a song
        if there are songs in the queue the song will be queued.
        """
        if not ctx.voice_state.voice:
            await ctx.invoke(self.join)

        async with ctx.typing():
            try:
                songs = await Song.create_source_yt(ctx, url)
            except YTDError:
                await ctx.send(f"> {OUTPUT_EMOJIS['error']} **An error ocurred while searching for: {url}")
            else:
                for song in songs:
                    await ctx.voice_state.songs.put(song)

                if len(songs) == 1:
                    await ctx.send(f"> **{songs[0].title}** added to queue.")
                else:
                    await ctx.send(f"> **{len(songs)} songs added to queue**.")

    @play.before_invoke
    async def check_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                "You are not connected to any voice channel.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    "Youtube Chan is already in a voice channel.")

# class YTChan(commands.Cog):
#     def __init__(self, client, max_q_size=30):
#         self.client = client
#         self.Q = YTQueue(max_q_size)
#         self.now_playing = None
#         self.vc = None
#         self.current_ctx = None

#     @commands.command()
#     async def play(self, ctx, url):
#         if not url:
#             await ctx.send(f"> {OUTPUT_EMOJIS['error']} **Usage:** ?play VIDEO_URL")
#             return

#         # Make sure the voice channel is not empty
#         if ctx.author.voice is None:
#             await ctx.send(f"> {OUTPUT_EMOJIS['not_in_vc']} **You need to be in a voice channel before playing any song.**")
#             return

#         # Join the voice channel or move to the correct voice channel
#         voice_channel = ctx.author.voice.channel
#         if ctx.voice_client is None:
#             await voice_channel.connect()
#         else:
#             await ctx.voice_client.move_to(voice_channel)

#         self.vc = ctx.voice_client
#         await ctx.send("> :mag_right: **Searching...**")
#         err, msg = self.Q.add(
#             url, ctx.author.display_name, ctx.author.avatar_url)

#         if err:
#             await ctx.send(f"> {OUTPUT_EMOJIS['error']} Could not download video")
#             return

#         self.current_ctx = ctx
#         if ctx.voice_client.is_playing():
#             await ctx.send(f"> {msg}")
#             return

#         if self.now_playing is None:
#             await self._play_next()

#     @commands.command()
#     async def pause(self, ctx):
#         ctx.voice_client.pause()
#         await ctx.send("> **Paused** :play_pause:")

#     @commands.command()
#     async def resume(self, ctx):
#         ctx.voice_client.resume()
#         await ctx.send("> **Player resumed** :play_pause:")

#     @commands.command()
#     async def stop(self, ctx):
#         ctx.voice_client.stop()
#         await ctx.voice_client.disconnect()
#         self.Q.clear()
#         await ctx.send("> **Player stopped and queued has been cleared**")

#     @commands.command()
#     async def skip(self, ctx):
#         ctx.voice_client.stop()
#         await self._play_next()

#     @commands.command()
#     async def skipto(self, ctx, song_index):
#         ctx.voice_client.stop()
#         song = self.Q.next_to(song_index)
#         if not song:
#             await ctx.send(f"> {OUTPUT_EMOJIS['error']} **Invalid index**")

#     async def _play_next(self, e=None):
#         if e is not None:
#             print(e)

#         if self.Q.is_empty():
#             self.now_playing = None
#             return

#         song = self.Q.next()
#         self.now_playing = song
#         source = await discord.FFmpegOpusAudio.from_probe(song['source'], **FFMPEG_OPTIONS)
#         self.vc.play(source, after=self._play_next)
#         await self._now_playing()

#     async def _now_playing(self):
#         video_name = self.now_playing['title']
#         embed = discord.Embed(title=f"{OUTPUT_EMOJIS['now_playing']} == Now playing == {OUTPUT_EMOJIS['now_playing']}\n{video_name}",
#                               url="https://google.com",
#                               color=discord.Color.blue())

#         embed.set_author(
#             name=self.now_playing['requestedBy'], icon_url=self.now_playing['requestedByAvatar'])
#         embed.set_thumbnail(url=self.now_playing['thumbnail'])
#         await self.current_ctx.send(embed=embed)
