from nextcord import Interaction, Embed
from nextcord.ext import commands

import difflib
from traceback import format_exception, print_exception, print_exc, format_tb
from sys import exc_info, stderr
from cooldowns import CallableOnCooldown

from .exceptions import *


class ErrorHandler:
    def __init__(self, bot):
        bot.on_error = self.on_error
        bot.on_command_error = self.on_command_error
        bot.on_application_command_error = self.on_application_command_error

        self.bot = bot

    def embed(self, error):
        cls = str(error.__repr__())
        parenthesis = cls.index("(")
        return Embed(title=f"__{cls[:parenthesis]}__", color=self.bot.log_color)

    def traceback_maker(self, exception) -> str:
        """ A way to debug your code anywhere """
        tb = "```py\n"
        tb += ("".join(format_exception(exception))).replace("```", "\`\`\`")
        tb += "```"
        return tb
    
    async def on_error(self, method, *args, **kwargs):
        print(f"Ignoring exception in {method}", file=stderr)
        print_exc()
        
        exception = exc_info()

        log = self.bot.get_channel(self.bot.log_channel_id)
        log_embed = Embed(title="__Error__", color=self.bot.log_color)
        log_embed.add_field(
            name="Traceback", 
            value=self.traceback_maker(exception[1])
        )
        await log.send(embed=log_embed)

        ctx = [x for x in args if isinstance(x, Interaction) or isinstance(x, commands.Context)]

        if ctx:
            await ctx[0].send("An error occured! Please contact an admin for Help")


    async def on_command_error(self, ctx: commands.Context, error):
        embed = self.embed(error)

        if isinstance(error, commands.errors.CommandNotFound):
            embed.description = "That command does not exist!"
            prefix_commands = [command.name for command in self.bot.commands]
            matches = difflib.get_close_matches(error.command_name, prefix_commands)

            if not matches:
                embed.description = "No matching commands found"
                await ctx.send(embed=embed)
                return

            for prefix_command in self.bot.commands:
                if prefix_command.name == matches[0]:
                    command = prefix_command
                    break

            prefix = self.bot.command_prefix
            embed.add_field(name="Did you mean?", value=f"```{prefix}{command.name}```")
            await ctx.send(embed=embed)
            return

        print(f"Ignoring exception in command {ctx.command}:", file=stderr)
        print_exception(
            type(error), error, error.__traceback__, file=stderr
        )

        log = self.bot.get_channel(self.bot.log_channel_id)
        log_embed = self.embed(error)
        log_embed.add_field(
            name="Traceback", 
            value=self.traceback_maker(error)
        )
        await log.send(embed=log_embed)


        if isinstance(error, commands.errors.CommandOnCooldown):
            # round time into the nearest full second
            time=round(error.retry_after)

            # Convert seconds to Days (If amout of days >= 1)
            if int(time/86400) > 0:
                time = round(time/86400)
                time = f"{time} Day{'s' if time > 1 else ''}"

            # Convert seconds to Hours (if amount of hours >= 1)
            elif int(time/3600) > 0:
                time = round(time/3600)

                # Convert back to day if hours round up to 24
                if time == 24:
                    time = "1 Day"
                else:
                    time = f"{time} Hour{'s' if time > 1 else ''}"
            
            # Convert seconds to minutes (if minutes >= 1)
            elif int(time/60) > 0:
                time = round(time/60)

                # Convert back to hour if minutes round up to 60
                if time == 60:
                    time == "1 Hour"
                else:
                    time = f"{time} Minute{'s' if time > 1 else ''}"
            else:
                time = f"{time} Second{'s' if time > 1 else ''}"

            embed.description = f"You are on Cooldown! Please try again in {time}."
            await ctx.send(embed=embed)
            return

        if isinstance(error, NotOwner) or isinstance(error, NotAdmin):
            embed.description = "This command is not available to you!"
            await ctx.send(embed=embed)
            return
        
        if isinstance(error, commands.errors.MissingPermissions):
            embed.description = "You do not have the required Permissions for this command!"
            embed.add_field(name="Missing Permission:", value=f"```{error.missing_permissions[0]}```")
            await ctx.send(embed=embed)
            return

        if isinstance(error, NoProfile):
            embed.description = "You are no in the Casino!"
            await ctx.send(embed=embed)
            return

        await ctx.send("An error occured! Please contact an admin for support!")
        

    async def on_application_command_error(self, interaction: Interaction, error):
        log = self.bot.get_channel(self.bot.log_channel_id)
        log_embed = self.embed(error)
        log_embed.add_field(
            name="Traceback", 
            value=self.traceback_maker(error)
        )
        await log.send(embed=log_embed)
        
        error = getattr(error, "original", error)  # Used for CallableOnCooldown - doesn't affect the rest
        embed = self.embed(error)

        if isinstance(error, CallableOnCooldown):
            time=round(error.retry_after)

            if int(time/86400) > 0:
                time = round(time/86400)
                time = f"{time} Day{'s' if time > 1 else ''}"
            elif int(time/3600) > 0:
                time=round(error.retry_after)

                # Convert seconds to Days (If amout of days >= 1)
                if int(time/86400) > 0:
                    time = round(time/86400)
                    time = f"{time} Day{'s' if time > 1 else ''}"
    
                # Convert seconds to Hours (if amount of hours >= 1)
                elif int(time/3600) > 0:
                    time = round(time/3600)
    
                    # Convert back to day if hours round up to 24
                    if time == 24:
                        time = "1 Day"
                    else:
                        time = f"{time} Hour{'s' if time > 1 else ''}"
                
                # Convert seconds to minutes (if minutes >= 1)
                elif int(time/60) > 0:
                    time = round(time/60)
    
                    # Convert back to hour if minutes round up to 60
                    if time == 60:
                        time == "1 Hour"
                    else:
                        time = f"{time} Minute{'s' if time > 1 else ''}"
                else:
                    time = f"{time} Second{'s' if time > 1 else ''}"

            embed.description = f"You are on Cooldown! Please try again in {time}."
            await interaction.send(embed=embed, ephemeral=True)
            return
        
        if isinstance(error, NotOwner) or isinstance(error, NotAdmin):
            embed.description = "This command is not available to you!"
            await interaction.send(embed=embed, ephemeral=True)
            return
    
        if isinstance(error, NoProfile):
            embed.description = "You are no in the Casino!"
            await interaction.send(embed=embed)
            return

        await interaction.send("An error occured! Please contact an admin for further Help!")

        print(f"Ignoring exception in command {interaction.application_command}:", file=stderr)
        print_exception(
            type(error), error, error.__traceback__, file=stderr
        )