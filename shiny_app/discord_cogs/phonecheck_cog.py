"""Allow PhoneCheck lookup from discord cog"""
import discord
from discord import app_commands
from discord.ext import commands
import shiny_app.classes.phonecheck as pc


class PhoneCheckCog(commands.Cog):
    """PhoneCheck functions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="pc")  # type: ignore
    @app_commands.checks.has_role("Shiny")
    async def pc_lookup_command(self, context: discord.Interaction, serial_number: str):
        """Look up serial number in PhoneCheck"""
        device = pc.Device(serial_number=serial_number)
        await context.response.send_message(device)


async def setup(bot: commands.Bot):
    """Add cog"""
    await bot.add_cog(PhoneCheckCog(bot))
