import discord
import asyncio
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

    @commands.command(name="skip")
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send("> **There are no videos playing...**")

        ctx.voice_state.skip()
        await ctx.message.add_reaction("✅")

    @commands.command(name="suffle")
    async def shuffle(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send("> **There are no videos playing...**")

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("> **The queue is empty...**")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name="skipto")
    async def skipto(self, ctx: commands.Context, index: int):
        pass

    @commands.command(name="remove")
    async def remove(self, ctx: commands.Context, index:int):
        pass

    @commands.command(name="queue")
    async def queue(self, ctx: command.Context):
        pass

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
