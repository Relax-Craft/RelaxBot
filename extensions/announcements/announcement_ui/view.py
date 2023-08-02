from nextcord.ui import View, RoleSelect, button, Button
from nextcord import Interaction, ButtonStyle

from .modal import AnnouncementData

class PingRoleSelect(View):
  def __init__(self, role):
    super().__init__()

    self.role_select = RoleSelect(
      placeholder = role.name,
      max_values = 1
    )
    self.role_select.callback = self.select_callback
    self.add_item(self.role_select)


  async def select_callback(self, interaction: Interaction):
    self.stop()


class AnnouncementButtons(View):
  def __init__(self, role):
    super().__init__(timeout=180)

    self.title = None
    self.content = None
    self.send = False
    self.cancle = False
    self.role = role

  
  @button(label="Send", style=ButtonStyle.blurple)
  async def send_announcement(self, button: Button, interaction: Interaction):
    # for child in self.children:
    #   child.disabled = True

    # await interaction.message.edit(view=self)
    self.send=True
    self.stop()

  
  @button(label="Add Topic", style=ButtonStyle.green)
  async def add_topic(self, button: Button, interaction: Interaction):
    modal = AnnouncementData()
    await interaction.response.send_modal(modal)
    await modal.wait()

    self.title = modal.info_title.value
    self.content = modal.info_content.value
    self.stop()

  
  @button(label="Change Ping", style=ButtonStyle.green)
  async def change_ping(self, button: Button, interaction: Interaction):
    select = PingRoleSelect(self.role)
    await interaction.send("Which Role should I ping?", ephemeral=True, view=select)
    await select.wait()

    if select.role_select.values[0].id != self.role.id:
      self.role = select.role_select.values[0]
    self.stop()
  

  @button(label="Cancel", style=ButtonStyle.danger)
  async def stop_announcement(self, button: Button, interaction: Interaction):
    self.cancle = True
    await interaction.send("Announcement canceled!", ephemeral=True)
    self.stop()