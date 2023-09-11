from nextcord.ext import commands
from nextcord import Interaction, Embed, Interaction, SlashOption
from main import RelaxSMP
import nextcord
from .application_ui.view import ApplicationButton



class Application(commands.Cog):
    guild_id = 988160173870841957
    
    def __init__(self, bot: RelaxSMP):
        self.bot: RelaxSMP = bot
        Application.guild_id = self.bot.home_guild_id

    @commands.command(name="appbutton")
    async def application_button(self, ctx: commands.Context):
        await ctx.message.delete()
        
        application_channel = self.bot.get_channel(self.bot.application_channel_id)
        msg = Embed(
            title="Welcome to RelaxSMP!",
            description="Looking to join our server? Press the button below to apply!",
            color=self.bot.default_color
        )

        start = Embed(
          title="Disclaimer",
          description="```Before you apply, make sure that you are on an official Java version \
of the game. We do not currently support Cracked, or Bedrock versions!```",
          color=self.bot.default_color
        )
    
        start.add_field(
          name="How it works",
          value="```We have had several cases of people not understanding how this \
application system works. This message is supposed to help you with that. \n\n\
Once you press the start button, you will be given 5 text fields, which you must fill out. \
Please only give us your in game name when answering the 'in game name' question (question 1) \
as this will be the input the bot uses to whitelist you. Once you have answered the first 5 questions \
you will be shown a preview of your application, along side 2 buttons. To continue your application, you must \
press the 'Continue' button. This will prompt you with the remaining 5 questions. Once you submit your answers \
you are done :). \n\n\
Once your application has been reviewed, you will be notified on the decision. Please note that the 'Bot must have \
access to your DM' to be able to do this.```",
      inline=False
        )
        start.add_field(
          name="Timing out - What happens when you mess up your application?",
          value="```The answer to this question is simple. \
For each set of questions, you are given 15 minutes time. If you mess something up, fear not for you will \
be able to re apply when the timer ends. Please note, that the bot sometimes fails to remove the applicant role, \
ultimately blocking people from re applying. If this is the case, feel free to let us know in the support channel.```",
          inline=False
        )
        start.set_footer(text="If you prefer to apply using a copy paste message you can do so in the support channel. \
Application format is in the pins :)")
        
        app_buttons = ApplicationButton(self.bot)
        await application_channel.send(embeds=[msg, start], view=app_buttons)

    
    @nextcord.slash_command(name="find_application", description="get a Link to a user's application", guild_ids=[guild_id])
    async def find_application(self, interaction: Interaction, applicant: nextcord.Member=SlashOption(
        name="user",
        description="User whomst application to look for",
        required=True,
        )
    ):
        application_archive_channel = self.bot.get_channel(self.bot.application_archive_channel_id)
        
        async for message in application_archive_channel.history(limit=100):
            if len(message.embeds) > 0 and message.author.bot:
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