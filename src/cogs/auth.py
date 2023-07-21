from discord.ext import commands
from discord import app_commands
import discord
import aiohttp

import asyncio

import uuid


class GetAccessToken(discord.ui.View):

    def __init__(self, auth):
        self.auth = auth
        super().__init__()

    @discord.ui.button(label="次へ")
    async def next(
        self, interaction: discord.Interaction,
        button: discord.ui.Button) -> None:
        if interaction.user.id in self.auth.waiting_auth_users:
            user = self.auth.waiting_auth_users[interaction.user.id]
            async with aiohttp.ClientSession(skip_auto_headers=["Content-Type"]) as sess:
                async with sess.post(
                    f"https://{user['host']}/api/miauth/{user['session_id']}/check",
                    headers={
                        "User-Agent": "Discord bot"
                    }
                ) as r:
                    print(r.request_info.headers)
                    print(await r.json())


class Auth(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.waiting_auth_users = {}

    @app_commands.command(
        description="misskeyにログインするために必要なことです。"
    )
    @app_commands.describe(host="ログインする対象のmisskeyインスタンス")
    async def login(
        self, interaction: discord.Interaction,
        host: str | None = "misskey.io"
    ) -> None:
        session_id = uuid.uuid4()
        self.waiting_auth_users[interaction.user.id] = {
            "host": host,
            "session_id": str(session_id),
        }
        await interaction.response.send_message(
            embed=discord.Embed(
                title="こちらでログインしてください。",
                description="https://{}/miauth/{}?name=MIKY&permission=read:account,write:notes".format(host, session_id)
            ).set_footer(name="反映まで最大五秒かかります。"),
            ephemeral=True
        )
        for i in range(60):
            async with aiohttp.ClientSession(skip_auto_headers=["Content-Type"]) as session:
                async with session.post(
                    "https://{host}/api/miauth/{session}/check".format(host=host, session=session_id),
                    allow_redirects=False
                ) as r:
                    data = await r.json()
                    print(data)
                    if data["ok"]:
                        await interaction.edit_original_response(embed=discord.Embed(
                            title="こちらでログインしてください。",
                            description="ログイン確認できました。"
                        ))
                        break
                    await asyncio.sleep(5)


async def setup(bot: commands.Bot):
    await bot.add_cog(Auth(bot))