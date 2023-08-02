from nextcord.ext import commands
from nextcord import slash_command, Interaction

from .staff_ui.views import RoleSelectView
from main import RelaxSMP


class GetAnnouncementRole(commands.Cog):
  def __init__(self, bot: RelaxSMP):
    self.bot: RelaxSMP = bot

  @slash_command(name="roles", guild_ids=[988160173870841957])
  async def roles(self, interaction: Interaction):
    await interaction.send("Choose a role!",
                           view=RoleSelectView(interaction.user),
                           ephemeral=True)


def setup(bot: RelaxSMP):
  bot.add_cog(GetAnnouncementRole(bot))