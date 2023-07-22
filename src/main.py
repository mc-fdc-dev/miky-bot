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

try:
    import uvloop
except ImportError:
    pass
else:
    uvloop.install()


class MikyBot(commands.Bot):
    pool: Pool | None
    logined_users: dict[discord.User, str] = {}

    async def setup_hook(self) -> None:
        self.pool = await create_pool(
            host=getenv("DB_HOST"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            db=getenv("DB_NAME"),
            autocommit=True
        )
        await self.load_extension("cogs.auth")
        await self.load_extension("cogs.user")
        await self.load_extension("jishaku")
        await self.tree.sync()


bot = MikyBot(command_prefix="d!", intents=discord.Intents.all())


bot.run(getenv("DISCORD_TOKEN"))
