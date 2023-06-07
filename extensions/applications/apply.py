from nextcord.ext import commands
from nextcord import Interaction, Embed, Interaction, SlashOption
from main import RelaxSMP
import nextcord
from .application_ui.buttons import ApplicationButton


class Application(commands.Cog):
    guild_id = None
    
    def __init__(self, bot: RelaxSMP):
        self.bot: RelaxSMP = bot
        Application.guild_id = self.bot.home_guild_id

    @commands.command(name="appbutton")
    async def application_button(self, ctx: commands.Context):
        await ctx.message.delete()
        
        application_channel = self.bot.get_channel(self.bot.application_channel_id)
        msg = Embed(
            title="[Welcome to RelaxSMP!](www.youtube.com)",
            description="Looking to join our server? Press the button below to apply!",
            color=self.bot.default_color
        )
        
        await application_channel.send(embed=msg, view=ApplicationButton(self.bot))

    
    @nextcord.slash_command(name="find_application", description="get a Link to a user's application", guild_ids=[guild_id])
    async def find_application(self, interaction: Interaction, applicant: nextcord.Member=SlashOption(
        name="user",
        description="User whomst application to look for",
        required=True,
        )
    ):
        application_archive_channel = self.bot.get_channel(self.bot.application_archive_channel_id)
        
        async for message in application_archive_channel.history(limit=100):
            if len(message.embeds) > 0:
                if str(applicant.id) in message.embeds[0].footer.text:
                    view = nextcord.ui.View()
                    view.add_item(nextcord.ui.Button(label="Application", url=message.jump_url))

                    await interaction.send("`Successful Application`", view=view)
                    return
            
            elif str(applicant.id) in message.content:
                view = nextcord.ui.View()
                view.add_item(nextcord.ui.Button(label="Application", url=message.jump_url))

                await interaction.send("`Application error: Timeout`", view=view)
                return

        await interaction.send(f"No Applciations from this user in the last 100 Applications! Search for the application using this id: {applicant.id}")


def setup(bot):
    bot.add_cog(Application(bot))