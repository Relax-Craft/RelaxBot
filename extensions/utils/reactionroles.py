from nextcord import Embed
from nextcord.ext import commands
from .utils_ui.views import InfoReactionRoles
from main import RelaxSMP

class ReactionRoles(commands.Cog):
    def __init__(self, bot: RelaxSMP) -> None:
        super().__init__()
        self.bot: RelaxSMP = bot

    @commands.command(name="reactionroles")
    async def reactionroles_message(self, ctx: commands.Context):
        await ctx.message.delete()
        embed = Embed(color=self.bot.log_color)
        embed.title = """—\nTake control of your pings\n—"""
        embed.description="""<:Apple:1002823039240634368> - To get notified to /bump the server which helps promote it for more members to join it.
📣 - To get notified for server announcements, includes server changes, updates, events and etc.
📰 - To get notified about server wide news, which are written in a short and an entertaining form of a news article.
🎁 - To get notified about new and upcoming server events! (Events may give rewards)"""

        embed.set_footer(text="For manual role equipment \nand removal use /roles")
        embed.set_author(name="For manual role equipment \nand removal use /roles")

        await ctx.send(embed=embed, view=InfoReactionRoles(self.bot))

def setup(bot):
    bot.add_cog(ReactionRoles(bot))