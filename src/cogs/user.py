from discord.ext import commands
from discord import app_commands
import discord

import aiohttp

from .utils import get_user


class Note(discord.ui.Modal, title="ノート"):
    content = discord.ui.TextInput(label="内容")

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as sess:
            async with sess.post() as r:
                pass


class User(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool

    @app_commands.command(description="ノートします")
    async def note(self, interaction) -> None:
        token = await get_user(interaction.user.id)
        if token is None:
            await interaction.response.send_message("利用するためにはログインしてください。")
        await interaction.response.send_modal()


async def setup(bot) -> None:
    await bot.add_cog(User(bot))
