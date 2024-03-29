"""Allow label printing from discord cog"""
import discord
from discord import app_commands
from discord.ext import commands
from shiny_app.modules.label_print import print_text


class LabelCog(commands.Cog):
    """Print to label printer in config"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="label")  # type: ignore
    @app_commands.checks.has_role("Shiny")
    async def label_command(
        self, context: discord.Interaction, text: str, quantity: int = 1, date: bool = True, barcode: str | None = None
    ):
        """Print label"""
        await context.response.send_message(f"Printing {quantity} label with {text=} and {date=}")
        lines = text.strip().splitlines()

        print_text(lines, quantity=quantity, print_date=date, barcode=barcode)


async def setup(bot: commands.Bot):
    """Add cog"""

    await bot.add_cog(LabelCog(bot))
