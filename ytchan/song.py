import youtube_dl
import asyncio
import discord
import functools
from discord.ext import commands


class YTDError(Exception):
    pass


class Song:
    YTDL_OPTIONS = {
        'format': 'bestaudio/best'
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data
        self.source = source

        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')
        self.url = data.get('url')

    def create_embed(self):
        embed = discord.Embed(title='Now playing',
                              description=f"```css\n{self.title}\n```",
                              color=discord.Color.blurple())

        embed.add_field(name='Duration', value=self.duration)
        embed.add_field(name='Requested by', value=self.requester.mention)
        embed.add_field(name='URL', value=f"[Click]({self.url})")
        embed.set_thumbnail(url=self.thumbnail)

        return embed

    @classmethod
    async def create_source_yt(cls, ctx: commands.Context, url: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, url, download=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDError(f"Couldn't find anything that matches: {url}")

        if 'entries' in data:
            # This is a playlist
            sources = list()
            for entry in data.get('entries'):
                source = entry['formats'][0]['url']
                inst = cls(ctx, discord.FFmpegPCMAudio(
                    source, **cls.FFMPEG_OPTIONS), data=entry)
                sources.append(inst)

            return sources

        else:
            source = data['formats'][0]['url']
            return [cls(ctx, discord.FFmpegPCMAudio(source, **cls.FFMPEG_OPTIONS), data=data)]
