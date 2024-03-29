"""Homeasssistant discord cog"""
from typing import Type
import discord
from discord import app_commands
from discord.ext import commands
import shiny_app.classes.homeassistant as ha
from .setup_cog import SetupCog


class HomeAssistantCog(commands.Cog):
    """Homeassistant API plugin"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def get_functions(function_name: Type[ha.HomeAssistant] | ha.TaylorSwiftly):
        """Get all functions from a class"""
        return [
            app_commands.Choice(name=function_choice, value=function_choice) for function_choice in function_name.get_functions()
        ]

    @app_commands.command(name="vacuum")  # type: ignore
    @app_commands.choices(choices=get_functions(ha.Vacuum))
    @SetupCog.has_role("Shiny")
    async def vacuum(self, context: discord.Interaction, choices: str):
        """Vacuum commands"""
        roomba = ha.Vacuum()
        status = getattr(roomba, choices)()
        await context.response.send_message(f"Vacuum is {status or choices}")

    @app_commands.command(name="alarm")  # type: ignore
    @app_commands.choices(choices=get_functions(ha.Alarm))
    @SetupCog.has_role("Shiny")
    async def alarm(self, context: discord.Interaction, choices: str):
        """Alarm commands"""
        alarm = ha.Alarm()
        status = getattr(alarm, choices)()
        await context.response.send_message(f"Alarm is {status or choices}")

    @app_commands.command(name="taylor_swiftly")  # type: ignore
    @app_commands.choices(choices=get_functions(ha.TaylorSwiftly()))
    @SetupCog.has_role("Shiny")
    async def tesla(self, context: discord.Interaction, choices: str):
        """Tesla commands"""
        taylor = ha.TaylorSwiftly()
        status = taylor.get_functions()[choices]()
        await context.response.send_message(f"Taylor Swiftly {choices.split()[1]} is {status or choices}")


async def setup(bot: commands.Bot):
    """Add cog"""
    await bot.add_cog(HomeAssistantCog(bot))
