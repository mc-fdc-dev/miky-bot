from discord.ext import commands
import discord

from os import getenv
from aiomysql import create_pool, Pool

try:
    import dotenv
except ImportError:
    pass
else:
    dotenv.load_dotenv()


class MikyBot(commands.Bot):
    pool: Pool | None

    async def setup_hook(self) -> None:
        self.pool = await create_pool(
            host=getenv("DB_HOST"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            db=getenv("DB_NAME")
        )
        await self.load_extension("cogs.auth")
        await self.load_extension("jishaku")


bot = MikyBot(command_prefix="d!", intents=discord.Intents.all())


bot.run(getenv("DISCORD_TOKEN"))