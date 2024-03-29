"""Allow Sickw lookup from discord cog"""
import discord
from discord import app_commands
from discord.ext import commands
from shiny_app.classes.sickw import Sickw


class SickwCog(commands.Cog):
    """Sickw functions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sick")  # type: ignore
    @app_commands.checks.has_role("Shiny")
    async def sickw_lookup_command(self, context: discord.Interaction, serial_number: str):
        """Look up serial number in Sickw"""
        device = Sickw(imei=serial_number)
        await context.response.send_message(device)


async def setup(bot: commands.Bot):
    """Add cog"""
    await bot.add_cog(SickwCog(bot))
