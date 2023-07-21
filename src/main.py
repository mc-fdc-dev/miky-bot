from discord.ext import commands
import discord

from os import getenv


class MikyBot(commands.Bot):

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.auth")


bot = MikyBot(command_prefix="debug!", intents=discord.Intents.all())


bot.run(getenv("DISCORD_TOKEN"))