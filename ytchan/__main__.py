import argparse
import discord
import asyncio
from discord.ext import commands
from bot import YTChan


def run_ytchan(args):
    """Starts the YouTube Chan bot

    Args:
        args: Should contain token and prefix.
    """
    intents = discord.Intents.all()
    intents.message_content = True
    client = commands.Bot(command_prefix=args.prefix,
                          intents=intents)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(client.add_cog(YTChan(client)))

    @client.event
    async def on_ready():
        print("="*10)
        print("Logged in as:\n{0.user.name}\n{0.user.id}".format(client))
        print("="*10)

    try:
        client.run(args.token)
    except Exception as e:
        print(f"Could not start client: {e}")


parser = argparse.ArgumentParser(
    description="Process runs the YouTube Chan discord bot.")
parser.add_argument(
    "--token", help="Discord bot token", required=True, metavar="[T]")
parser.add_argument(
    "--prefix", help="Set the command prefix to be used by the bot, defaults to '?'", default=">", metavar="[prefix]")

args = parser.parse_args()

run_ytchan(args)
