from nextcord.ui import Modal, TextInput
from nextcord import Interaction, TextInputStyle


class AnnouncementData(Modal):
  def __init__(self):
    super().__init__("Announcement")
    
    self.info_title = TextInput(
      label = "Title",
      min_length = 1,
      placeholder = "Title for the Announcement",
      required = True
    )
    self.add_item(self.info_title)

    self.info_content = TextInput(
      label = "Announcement",
      style = TextInputStyle.paragraph,
      min_length = 1,
      placeholder = "Announcement Content",
      required=True
    )
    self.add_item(self.info_content)

  async def callback(self, interaction: Interaction):
    self.stop()