from discord.ext import commands
from discord import app_commands

import uuid


class Auth(comamnds.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        description="misskeyにログインするために必要なことです。"
    )
    @app_commands.describe(url="ログインする対象のmisskeyインスタンス")
    async def login(
        self, interaction: discord.Interaction,
        host: str | None = "misskey.io"
    ) -> None:
        session_id = uuid.uuid4()
        await interaction.response.send_message(
            embed=discord.Embed(
                title="こちらでログインしてください。",
                description="https://{}/miauth/{}?name=MIKY&permission=read:account,write:notes".format(host, session_id)
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Auth(bot))