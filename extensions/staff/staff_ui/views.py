from nextcord import Interaction, SelectOption
from nextcord.ui import StringSelect, View

class RoleSelect(StringSelect["RolesView"]):
  def __init__(self, user):
    self.user = user

    def has_role(user, role_id):
      for role in user.roles:
        if role.id == role_id:
          return True
      return False

    self.roles = {
      "announce": 1079431372109787147,
      "news": 1089604637822291988,
      "event": 1108164048148770937,
      "bump": 997189428835524728
    }

    options = [
      SelectOption(label="Announcements Role",
                   value="announce",
                   default=has_role(user, self.roles["announce"])),
      SelectOption(label="News Role",
                   value="news",
                   default=has_role(user, self.roles["news"])),
      SelectOption(label="Event Role",
                   value="event",
                   default=has_role(user, self.roles["event"])),
      SelectOption(label="Bump Role",
                   value="bump",
                   default=has_role(user, self.roles["bump"]))
    ]
    super().__init__(placeholder="Get/Remove a role!",
                     options=options,
                     min_values=0,
                     max_values=len(self.roles))

  async def callback(self, interaction: Interaction):
    guild = interaction.client.get_guild(interaction.guild_id)
    added_roles = []
    removed_roles = []

    # create a collection of possible roles to select from, with active Role objects instead of IDs
    roles = {}
    for key, role_id in self.roles.items():
      roles[key] = guild.get_role(role_id)

    # iterate through items in roles dict
    for key, role in roles.items():
      # Run this if the key isn't in the Selected values
      if key not in self.values:

        # remove role if user has role but its deselected
        if role in interaction.user.roles:
          await interaction.user.remove_roles(role)
          removed_roles.append(role)

      elif key in self.values:
        if role not in interaction.user.roles:
          await interaction.user.add_roles(role)
          added_roles.append(role)

    if len(added_roles) > 0 and len(removed_roles) > 0:
      message = f"Added {str(added_roles)}, removed {str(removed_roles)}"
    elif len(added_roles) > 0:
      message = f"Added {str([str(role) for role in added_roles])}"
    else:
      message = f"Removed {str([str(role) for role in removed_roles])}"

    await interaction.edit(content=message, view=RoleSelectView(self.user))


class RoleSelectView(View):
  def __init__(self, user):
    super().__init__()
    self.add_item(RoleSelect(user))