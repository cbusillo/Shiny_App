"""Sync cogs to discord to enable /commands"""
import asyncio
import os
import platform
import time
import discord
from discord import app_commands
from discord.ext import commands


BOT_CHANNEL = 1073943829192912936


class SetupCog(commands.Cog):
    """Add anything related to setting up bot here"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.enable_commands = True
        super().__init__()

    @commands.Cog.listener("on_message")
    async def enable_function(self, _: discord.Message):
        """If not enabled, delay one second so dev can answer"""
        if self.enable_commands is False:
            time.sleep(2)

    @commands.command(name="sync")
    async def sync_command(self, context: commands.Context) -> None:
        """Add slash commands to Discord guid"""
        if "imagingserver" in platform.node().lower():
            await context.defer()
            os.system("git fetch")
            return_code = os.system("git diff origin/main --quiet")
            if return_code:
                print("Restarting server!!!")
                await context.channel.send("Updating and restarting server!!!")
                os.system("ssh 127.0.0.1 ~/launch_api.sh")

            await asyncio.sleep(2)

        try:
            await context.message.delete()
            await self.check_server()
            self.enable_commands = True
        except discord.errors.NotFound:
            print("Not able to delete message")
            self.enable_commands = False
            return

    @app_commands.command(name="clear")  # type: ignore
    @app_commands.choices(
        scope=[
            app_commands.Choice(name="Bot", value="bot"),
            app_commands.Choice(name="All", value="all"),
        ]
    )
    async def clear_command(self, context: discord.Interaction, scope: str) -> None:
        """Clear all or bot messages in bot-config"""

        if not isinstance(context.channel, discord.TextChannel):
            return
        if context.channel.id != BOT_CHANNEL:
            await context.channel.send("Cannot use in this channel")
            return
        temp_message = await context.channel.send(f"Clearing messages from {scope}")
        await context.response.defer()
        if scope == "bot":
            async for message in context.channel.history():
                if message.author == context.client.user and message != temp_message:
                    await message.delete()
        elif scope == "all":
            async for message in context.channel.history():
                if message != temp_message:
                    await message.delete()
        await temp_message.delete()

    @commands.Cog.listener("on_ready")
    async def shiny_bot_connect(self):
        """Print console message that bot is connected"""
        if not isinstance(self.bot.user, discord.ClientUser):
            print("Bot is not connected to Discord")
            return
        print(f"{self.bot.user.display_name} has connected to Discord!")

    @commands.Cog.listener("on_ready")
    async def set_dev_rol(self):
        """Add dev role to activate bot if run from dev machine"""
        await self.check_server()

    async def check_server(self):
        """Set bot role and sync commands"""

        self.bot.tree.copy_global_to(guild=self.bot.guilds[0])
        synced = await self.bot.tree.sync(guild=self.bot.guilds[0])
        current_channel = self.bot.get_channel(BOT_CHANNEL)
        if isinstance(current_channel, discord.TextChannel):
            await current_channel.send(f"Synced {len(synced)} commands from {platform.node()}.")

        role = discord.utils.get(self.bot.guilds[0].roles, name="Dev")
        bot_member = discord.utils.get(self.bot.get_all_members(), name="Doug Bot")
        if bot_member is None or role is None:
            return

        if "imagingserver" in platform.node().lower():
            print("Switching to Prod")
            await bot_member.remove_roles(role)
        else:
            print("Switching to Dev")
            await bot_member.add_roles(role)


async def setup(client: commands.Bot):
    """Run the Setup cog"""
    await client.add_cog(SetupCog(client))