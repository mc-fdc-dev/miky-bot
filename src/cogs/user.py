from discord.ext import commands
from discord import app_commands
import discord

import aiohttp

from .utils import get_userdata


class Note(discord.ui.Modal, title="ノート"):
    content = discord.ui.TextInput(label="内容", style=discord.TextStyle.paragraph)

    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as sess:
            async with sess.post(
                f"https://{self.host}/api/notes/create",
                json={
                    "i": self.token,
                    "text": self.content.value
                }
            ) as r:
                await interaction.response.send_message("送信しました。")


class MisskeyUser(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool

    @app_commands.command(description="ノートします")
    async def note(self, interaction):
        data = await get_userdata(interaction.user.id, self.pool)
        if data is None:
            await interaction.response.send_message("利用するためにはログインしてください。")
        await interaction.response.send_modal(Note(data[0], data[1]))


async def setup(bot):
    await bot.add_cog(MisskeyUser(bot))
