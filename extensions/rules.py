import nextcord
from nextcord import Embed, Interaction, slash_command, Message, SlashOption
from nextcord.ext import commands
# import json
from utils.file_load import get_rules
from difflib import get_close_matches


class RulesCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.colors = [0xF9CF95, 0x3EB489, 0xE5002D, 0xFF6EC7, 0xA1800B, 0x676D99]


  @slash_command(name="rules", description="Must be run in rules channel!")
  async def send_rules(
    self, 
    interaction: Interaction,
    rule_category: str = SlashOption(
      name="rule_category",
      description="The rule category",
      required=False
    ),
    rule_number: int = SlashOption(
      name="rule_number",
      description="The rule number to send",
      required=False
    )
  ):
    color_index = 0
    embeds = []
    extra_field_data = None
    
    rule_book = get_rules()

    if rule_category and rule_number:
      rules_dict = get_close_matches(rule_category, [key for key, _ in rule_book.items()])
      rule = rule_book[rules_dict[0]][str(rule_number)]

      warning = Embed(
        title="Looks like chat is getting a bit out of hand!",
        color=self.bot.default_color
      )
      warning.add_field(
        name=f"{rules_dict[0]} - #{rule_number}",
        value=f"```{rule_number}) {rule}```"
      )
      await interaction.channel.send(embed=warning)
      return

    chief_role = interaction.guild.get_role(989226771465535528)

    if chief_role not in interaction.user.roles:
      await interaction.send("You have screwed up G. Make sure you choose a rule category AND a rule number! Thanks :)", ephemeral=True)
      return
    
    for category, rules in rule_book.items():
      embed = Embed(title=category, color=self.colors[color_index])
      color_index += 1

      rules_message = "``` \n"
      for number, rule in rules.items():
        if type(rule) == str:
          rules_message += f"{number}) {rule} \n \n"
        else:
          extra_field_data = {number: rule}

      rules_message += "```"
      embed.description = rules_message

      if extra_field_data == None:
        embeds.append(embed)
        continue
        
      else:
        rules_message = "``` \n"
        for category, sub_rules in extra_field_data.items():
          for number, rule in sub_rules.items():
            rules_message += f"{number}) {rule} \n \n"
          rules_message += "```"
          embed.add_field(name=category, value=rules_message)
          embeds.append(embed)
          extra_field_data = None
          continue

    await interaction.channel.send(embeds=embeds)
    await interaction.channel.send("These Rules are not a comprehensive guide on how to act, and staff will moderate content \
that they believe to  violate the spirit of the rules at their own discretion. \n\n Not knowing the rules is not an excuse. In the event \
of a rule change, you will be notifid accordingly.")


  @slash_command(name="rules_update", description="Must be run in rules channel")
  async def update_rules(self, interaction: Interaction, rules_message_id: str):
    try:
      rules_message_id = int(rules_message_id)
    except:
      await interaction.send("You didn't give a Valid id! Message id must be a number", ephemeral=True)
      return
    
    color_index = 0
    embeds = []
    extra_field_data = None
    
    rule_book = get_rules()

    for category, rules in rule_book.items():
      embed = Embed(title=category, color=self.colors[color_index])
      color_index += 1

      rules_message = "``` \n"
      for number, rule in rules.items():
        if type(rule) == str:
          rules_message += f"{number}) {rule} \n \n"
        else:
          extra_field_data = {number: rule}

      rules_message += "```"
      embed.description = rules_message

      if extra_field_data == None:
        embeds.append(embed)
        continue
        
      else:
        rules_message = "``` \n"
        for category, sub_rules in extra_field_data.items():
          for number, rule in sub_rules.items():
            rules_message += f"{number}) {rule} \n \n"
          rules_message += "```"
          embed.add_field(name=category, value=rules_message)
          embeds.append(embed)
          extra_field_data = None
          continue

    rules = await interaction.channel.fetch_message(rules_message_id)
    await rules.edit(embeds=embeds)



def setup(bot):
  bot.add_cog(RulesCog(bot))