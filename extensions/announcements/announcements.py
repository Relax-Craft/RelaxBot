from nextcord import slash_command, Embed, Interaction, Permissions, TextInputStyle, ButtonStyle
from nextcord.ext import commands

from .modal.modal import AnnouncementData
from .view.view import AnnouncementButtons

class Announcements(commands.Cog):
  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @slash_command(name="announcement", default_member_permissions=Permissions(administrator=True))
  async def announcement(self, interaction: Interaction):
    modal = AnnouncementData()    
    await interaction.response.send_modal(modal)
    await modal.wait()

    announcement = Embed(
      title="New Announcement!",
      color=self.bot.default_color
    )
    announcement.add_field(
      name=modal.info_title.value,
      value=modal.info_content.value,
      inline=False
    )

    announcement_role = interaction.guild.get_role(1079431372109787147)
    view = AnnouncementButtons(announcement_role)

    while view.send == False and view.cancle == False:
      await interaction.send(announcement_role.name, embed=announcement, ephemeral=True, view=view)
      timeout = await view.wait()

      if timeout:
        return

      if view.title != None and view.content != None:
        announcement.add_field(
          name=view.title,
          value=view.content,
          inline=False
        )

      if view.role.id != announcement_role.id:
        announcement_role = view.role

      if view.send == False and view.cancle == False:
        view = AnnouncementButtons(announcement_role)

    announcement.set_footer(
      text="Use /roles to never miss out on an announcement!"
    )
    
    if view.send:
      announcement_channel = self.bot.get_channel(self.bot.announcement_channel_id)
      await announcement_channel.send(announcement_role.mention, embed=announcement)

      console = self.bot.get_channel(self.bot.console)
      await console.send("broadcast New Announcement just released! Go check it out :)")


def setup(bot):
  bot.add_cog(Announcements(bot))