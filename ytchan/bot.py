import discord
from discord.ext import commands
from voice_state import VoiceState
from song import Song, YTDError

# You should change this.
# OUTPUT_EMOJIS = {'now_playing': ':ASgaztonrainbow:', 'not_in_vc': ':ASRemHmph:', 'error': ':Asevil:'}
OUTPUT_EMOJIS = {'now_playing': ':musical_note:',
                 'not_in_vc': ':warning:', 'error': ':bangbang:',
                 'warning': ':warning:'}


class YTChan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_state = None

    def get_voice_state(self, ctx: commands.Context):
        if not self.voice_state:
            self.voice_state = VoiceState(self.bot, ctx)

        return self.voice_state

    async def cog_before_invoke(self, ctx: commands.Context):
        """Embeds the current voice state into the context"""
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Error handling"""
        self.voice_state.stop()
        await ctx.send(f"> {OUTPUT_EMOJIS['error']} **An error occurred: {OUTPUT_EMOJIS['error']}**\n{str(error)}")

    @commands.command(invoke_without_subcommand=True)
    async def join(self, ctx: commands.Context):
        """Join voice channel"""
        channel = ctx.author.voice.channel

        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(channel)
            return

        ctx.voice_state.voice = await channel.connect()

    @commands.command()
    async def pause(self, ctx: commands.Context):
        """Pauses the player"""
        print("Player paused.")
        if ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.send("> **Player paused**")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        """Resumes the player if it was paused"""
        print("Player resumed")
        if ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.send("> **Resumed**")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stops the player"""
        print("Player stopped")
        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            await ctx.voice_state.stop()
            await ctx.send("> **Player stopped and queue cleared**")

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skips the current playing video"""
        if not ctx.voice_state.is_playing:
            return await ctx.send("> **There are no videos playing...**")

        ctx.voice_state.skip()
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def shuffle(self, ctx: commands.Context):
        """Shuffles the queue"""
        if not ctx.voice_state.is_playing:
            return await ctx.send(f"> {OUTPUT_EMOJIS['error']} **There are no videos playing...**")

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send(f"> {OUTPUT_EMOJIS['error']} **The queue is empty...**")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def remove(self, ctx: commands.Context, index: int):
        """Removes video from queue at index"""
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("> **Queue is empty...**")
        elif index >= len(ctx.voice_state.songs):
            return await ctx.send(f"> {OUTPUT_EMOJIS['error']} Invalid index **{index}** for queue of size **{len(ctx.voice_state.songs)}**")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def queue(self, ctx: commands.Context, page: int = 1):
        """Shows all the videos in the queue"""
        import math
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send(f"> {OUTPUT_EMOJIS['warning']} **The queue is empty**")

        vids_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs)/vids_per_page)
        start = (page - 1) * vids_per_page
        end = start + vids_per_page
        msg = ""

        for i, video in enumerate(ctx.voice_state.songs[start:end], start=start):
            msg += f"**{i+1}** [{video.title}]({video.url})\n"

        embed = discord.Embed(
            description=f"**{len(ctx.voice_state.songs)} videos:**\n\n{msg}")
        embed.set_footer(text=f"Viewing page {page}/{pages}")
        await ctx.send(embed=embed)

    @commands.command()
    async def show_commands(self, ctx: commands.Context):
        """Sends message with all the commands"""
        embed = discord.Embed(
            title="**Youtube Chan Commands**", color=discord.Color.blue())
        embed.add_field(
            name="`?play [URL]`", value="Plays the video or adds it to queue if there is a video currently playing. The URL can be a single video or a playlist", inline=False)
        embed.add_field(name="`?pause`",
                        value="Pauses the player.", inline=False)
        embed.add_field(name="`?resume`",
                        value="Resumes the player.", inline=False)
        embed.add_field(
            name='`?stop`', value="Stops the player clears the queue and Youtube Chan leaves the voice channel.", inline=False)
        embed.add_field(
            name="`?join`", value="Youtube Chan joins the voice channel (You need to be in one).", inline=False)
        embed.add_field(
            name="`?skip`", value="Skips the current video and starts the next one if there is one.", inline=False)
        embed.add_field(name="`?shuffle`",
                        value="Shuffles the queue.", inline=False)
        embed.add_field(
            name="`?remove [SONG NUMBER]`", value="Removes video at index.", inline=False)
        embed.add_field(
            name="`?commands`", value="Shows all commands.", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
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
        """Ensures there is someone in the voice channel before starting the player"""
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                "You are not connected to any voice channel.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError(
                    "Youtube Chan is already in a voice channel.")
