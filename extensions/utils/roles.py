from nextcord.ext import commands
from nextcord import slash_command, Interaction, Embed

from .utils_ui.views import RoleSelectView, InfoReactionRoles
from main import RelaxSMP


class RoleSelection(commands.Cog):
	def __init__(self, bot: RelaxSMP):
		self.bot: RelaxSMP = bot

	@slash_command(name="roles", guild_ids=[988160173870841957])
	async def roles(self, interaction: Interaction):
		await interaction.send(
    		"Choose a role!",
    		view=RoleSelectView(interaction.user, self.bot),
    		ephemeral=True
    	)

	@commands.command(name="reactionroles")
	async def reactionroles_message(self, ctx: commands.Context):
		await ctx.message.delete()
		embed = Embed(color=self.bot.default_color)
		embed.title = """—\nTake control of your pings\n—"""
		embed.description="""<:Apple:1002823039240634368> - To get notified to /bump the server which helps promote it for more members to join it.
📣 - To get notified for server announcements, includes server changes, updates, events and etc.
📰 - To get notified about server wide news, which are written in a short and an entertaining form of a news article.
🎁 - To get notified about new and upcoming server events! (Events may give rewards)"""

		embed.set_footer(text="For manual role equipment \nand removal use /roles")
		embed.set_author(name="For manual role equipment \nand removal use /roles")		
		
		await ctx.send(embed=embed, view=InfoReactionRoles(self.bot))


def setup(bot: RelaxSMP):
  bot.add_cog(RoleSelection(bot))