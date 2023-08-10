from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption, Member, Permissions, Embed, User

from main import RelaxSMP


class StaffCommands(commands.Cog):

  def __init__(self, bot: RelaxSMP):
    self.bot: RelaxSMP = bot

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

  @slash_command(name="whitelist",
                 default_member_permissions=Permissions(manage_messages=True))
  async def whitelist_command(self,
                              interaction: Interaction,
                              action=SlashOption(required=True,
                                                 choices=["add", "remove"]),
                              ign: str = SlashOption(required=True),
                              user: Member = SlashOption(required=False,
                                                         default=None)):
    await interaction.response.defer(ephemeral=True, with_message=False)
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
        f"""Welcome to the server! You have just been accepted and should be whitelisted! :)
`Server ip: {self.bot.server_ip}`""")
    except:
      pass

  @slash_command(name="kick",
                 default_member_permissions=Permissions(kick_members=True))
  async def slash_kick(
    self,
    interaction: Interaction,
    member: Member = SlashOption(name="kick",
                                 description="Kick a member",
                                 required=True),
    reason: str = SlashOption(name="reason",
                              description="The reason for kicking this member",
                              required=True,
                              min_length=5,
                              max_length=150)):
    user_check = self.check_user(interaction, member)

    if user_check:
      await interaction.send(user_check, ephemeral=True)
      return

    await member.kick()

    log = Embed(title=f"{member.name} Kicked",
                color=self.bot.log_color)
    if interaction.user.avatar.url:
      log.set_author(
        name=interaction.user.name,
        icon_url=interaction.user.avatar.url
      )
    else:
      log.set_author(
        name=interaction.user.name
      )
    if member.avatar.url:
      log.set_thumbnail(member.avatar.url)
  
    log.set_footer(text=member.id)

    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)
    await log_channel.send(embed=log)
    await interaction.send("User has been Kicked, and it has been logged",
                           ephemeral=True)

  @slash_command(name="ban",
                 default_member_permissions=Permissions(ban_members=True))
  async def slash_ban(self,
                      interaction: Interaction,
                      member: Member,
                      reason: str = SlashOption(
                        name="reason",
                        description="Reason for the ban",
                        required=True,
                        min_length=5,
                        max_length=150)):
    user_check = self.check_user(interaction, member)

    if user_check:
      await interaction.send(user_check)
      return

    await member.ban()

    log = Embed(title=f"{member.name} Unbanned",
                color=self.bot.log_color)
    
    if interaction.user.avatar.url:
      log.set_author(
        name=interaction.user.name,
        icon_url=interaction.user.avatar.url
      )
    else:
      log.set_author(name=interaction.user.name)
    if member.avatar.url:
      log.set_thumbnail(member.avatar.url)
    log.set_footer(text=member.id)

    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)
    await log_channel.send(embed=log)
    await interaction.send("User has been banned, and it has been logged",
                           ephemeral=True)

  @slash_command(name="unban",
                 default_member_permissions=Permissions(ban_members=True))
  async def slash_unban(self, interaction: Interaction, member: User):
    try:
      await interaction.guild.unban(member)
    except:
      await interaction.send("User isn't banned.", ephemeral=True)
      return

    log = Embed(title=f"{member.name} Unbanned",
                color=self.bot.log_color)
    
    if interaction.user.avatar.url:
      log.set_author(
        name=interaction.user.name,
        icon_url=interaction.user.avatar.url
      )
    else:
      log.set_author(
        name=interaction.user.name
      )
    if member.avatar.url:
      log.set_thumbnail(member.avatar.url)
    log.set_footer(text=member.id)

    log_channel = interaction.guild.get_channel(self.bot.log_channel_id)
    await log_channel.send(embed=log)
    await interaction.send("User has been unbanned, and it has been logged",
                           ephemeral=True)

  @slash_command(name="warn",
                 default_member_permissions=Permissions(manage_messages=True))
  async def slash_warn(self, interaction: Interaction, user: Member,
                       reason: str):
    staff_role = interaction.guild.get_role(self.bot.staff_role_id)

    if staff_role not in interaction.user.roles:
      await interaction.response.send(
        "You aren't allowed to use this command, nor should you see it xD'",
        ephemeral=True)
      return

    warning = Embed(description=f"**Reason:** {reason}", color=0x2f3136)
    
    if user.avatar.url:
      warning.set_author(
        name=f"{user.name} has been warned",
        icon_url=user.avatar.url
        )
    else:
      warning.set_author(
        name=f"{user.name} has been warned"
      )

    await interaction.send(embed=warning)

  @slash_command(name="clear",
                 default_member_permissions=Permissions(manage_messages=True))
  async def slash_clear(self, interaction: Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Cleared {amount} messages!")

  @slash_command(name="log", default_member_permissions=Permissions(manage_messages=True))
  async def slash_log(self, interaction: Interaction, log: str):
    log_channel = self.bot.get_channel(self.bot.log_channel_id)

    log_embed = Embed(
      title="New Log",
      description=log,
      color=self.bot.log_color
    )

    if interaction.user.avatar.url:
      log_embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    else:
      log_embed.set_author(
        name=interaction.user.name
      )

    await log_channel.send(embed=log_embed)
    await interaction.send("Log posted!", ephemeral=True)



def setup(bot: RelaxSMP):
  bot.add_cog(StaffCommands(bot))
