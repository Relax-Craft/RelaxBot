from nextcord.ext import commands
from nextcord import (
    Interaction, 
    slash_command, 
    SlashOption, 
    Member, 
    Permissions, 
    Embed, 
    User
)


class StaffCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def check_user(self, interaction, victim):
    staff_role = interaction.guild.get_role(self.bot.staff_role_id)
    
    if interaction.user == victim:
      return "You cannot kick yourself!"
      
    elif isinstance(victim, User):
       return "User is not in the server!"
    
    elif staff_role in victim.roles:
      return "You cannot kick another staff member!"

    else:
      return None

  
  @slash_command(name="whitelist", default_member_permissions=Permissions(manage_messages=True))
  async def whitelist_command(
    self,
    interaction: Interaction,
    action = SlashOption(
      required=True,
      choices=["add", "remove"]
    ),
    ign: str = SlashOption(
      required=True
    ),
    user: Member = SlashOption(
      required=False,
      default=None
    )
  ):
    console = interaction.guild.get_channel(self.bot.console)
    await console.send(f"whitelist {action} {ign}")
    await interaction.send("Done!", ephemeral=True)

    if user == None:
      return

    await user.edit(nick=ign)
    member_role = interaction.guild.get_role(self.bot.member_role_id)
    await user.add_roles(member_role)
    
    try:  
      await user.send(
        """Welcome to the server! You have just been accepted and should be whitelisted! :)
`Server ip: 51.68.21.111:25588`""")
    except:  
      pass

  @slash_command(name="kick", default_member_permissions=Permissions(kick_members=True))
  async def slash_kick(
    self, 
    interaction: Interaction, 
    member: Member = SlashOption(
      name="kick",
      description="Kick a member",
      required=True
    ),
    reason: str = SlashOption(
      name="reason",
      description="The reason for kicking this member",
      required=True,
      min_length=5,
      max_length = 150
    ) 
  ):
    user_check = self.check_user(interaction, member)
    
    if user_check:
      await interaction.send(user_check, ephemeral=True)
      return    

    await member.kick()
    
    log = Embed(title=f"{member.name} Kicked by {interaction.user.name}", color=self.bot.log_color)
    log.add_field(name="Reason", value=reason)
    log.set_thumbnail(interaction.user.avatar.url)
    log.set_footer(text=member.id)

    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)
    await log_channel.send(embed=log)
    await interaction.send("User has been Kicked, and it has been logged", ephemeral=True)


  @slash_command(name="ban", default_member_permissions=Permissions(ban_members=True))
  async def slash_ban(
    self, 
    interaction: Interaction,
    member: Member,
    reason: str = SlashOption(
      name="reason",
      description="Reason for the ban",
      required=True,
      min_length=5,
      max_length=150
    )
  ):
    user_check = self.check_user(interaction, member)

    if user_check:
      await interaction.send(user_check)
      return

    await member.ban()

    log = Embed(title=f"{member.name} kicked by {interaction.user.name}", color=self.bot.log_color)
    log.add_field(name="Reason", value=reason)
    log.set_thumbnail(interaction.user.avatar.url)
    log.set_footer(text=member.id)

    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)
    await log_channel.send(embed=log)
    await interaction.send("User has been kicked, and it has been logged", ephemeral=True)

  @slash_command(name="unban", default_member_permissions=Permissions(ban_members=True))
  async def slash_unban(self, interaction: Interaction, member: User):
    try:
      await interaction.guild.unban(member)
    except:
      await interaction.send("User isn't banned.", ephemeral=True)
      return
    
    log = Embed(title=f"{member.name} Unbanned by {interaction.user.name}", color=self.bot.log_color)
    log.set_thumbnail(interaction.user.avatar.url)
    log.set_footer(text=member.id)

    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)
    await log_channel.send(embed=log)
    await interaction.send("User has been unbanned, and it has been logged", ephemeral=True)

  @slash_command(name="warn", default_member_permissions=Permissions(manage_messages=True))
  async def slash_warn(
    self,
    interaction: Interaction,
    user: Member,
    reason: str
  ):
    staff_role = interaction.guild.get_role(self.bot.staff_role_id)

    if staff_role not in interaction.user.roles:
      await interaction.response.send("You aren't allowed to use this command, nor should you see it xD'", ephemeral=True)
      return

    warning = Embed(
      description=f"**Reason:** {reason}",
      color=0x2f3136
    )
    warning.set_author(name=f"{user.name} has been warned", icon_url=user.avatar.url)

    await interaction.send(embed=warning)
    

  @slash_command(name="nuke", default_member_permissions=Permissions(administrator=True))
  async def slash_nuke(
    self,
    interaction: Interaction,
  ):
    not_applied_role = interaction.guild.get_role(1101286162557050972)
    users = [member for member in interaction.guild.members if not_applied_role in member.roles]
    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)

    for user in users:
      await user.kick()

      log = Embed(title=f"{user.name} Kicked by {interaction.user.name}", color=self.bot.log_color)
      log.add_field(name="Reason", value="Nuke")
      log.set_thumbnail(interaction.user.avatar.url)
      log.set_footer(text=user.id)
      
      await log_channel.send(embed=log)


  @slash_command(name="clear", default_member_permissions=Permissions(manage_messages=True))
  async def slash_clear(self, interaction: Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Cleared {amount} messages!")
    

def setup(bot):
  bot.add_cog(StaffCommands(bot))