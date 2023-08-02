from nextcord import slash_command, Interaction, SlashOption, Permissions
from nextcord.ext import commands
from main import RelaxSMP

from ...utils.file_load import get_char_table, get_chars


class Encryption(commands.Cog):
  def __init__(self, bot: RelaxSMP):
    self.bot: RelaxSMP = bot

  @slash_command(name="encrypt", guild_ids=[1104791361665892485], default_member_permissions=Permissions(administrator=True))
  async def slash_encrypt(
    self, 
    interaction: Interaction, 
    to_encrypt: str = SlashOption(
        description="Provide an input for me to encrypt",
        name="input"
   )
  ):
    await interaction.response.defer(ephemeral=True, with_message=True)
    
    encrypted = ""
    table = get_chars()

    for letter in to_encrypt:
        encrypted += table[letter]

    i = 0
    even = ""
    odd = ""

    while i < len(encrypted):
        odd += encrypted[i]
        even += encrypted[i+1]

        i += 2

    encrypted = even+odd

    await interaction.followup.send(
      f"""```ini
[INPUT]
{to_encrypt}

[ENCRYPTED]
{encrypted}```
"""
    )

  @slash_command(name="decrypt", guild_ids=[1104791361665892485], default_member_permissions=Permissions(administrator=True))
  async def slash_decrypt(
    self, 
    interaction: Interaction, 
    encrypted = SlashOption(
        description="Provide an input for me to encrypt",
        name="input"
   )
  ):
    try:
      encrypted = int(encrypted)
    except:
      await interaction.send("input wasn't a raw number - Maybe you included spaces on accident?", ephemeral=True)
      return
      
    await interaction.response.defer(ephemeral=True, with_message=True)

    encrypted = str(encrypted)
    decrypted = ""

    i = 0
    even = ""
    odd = ""

    while len(encrypted) > 0:
        odd += encrypted[i]
        encrypted = encrypted[1:]

        if len(encrypted) > 0:
            even += encrypted[i-1]
            encrypted = encrypted[:-1]


    even = even[::-1]

    encrypted = ""
    for x in range(0, len(odd)):
        encrypted += even[x]
        encrypted += odd[x]


    x = 0
    split_id = []
    
    while x < len(encrypted):
        split_id.append(encrypted[x:x+2])
        x += 2

    table = get_char_table()
    
    for char in split_id:
        decrypted += table[char[0]][char[1]]

    await interaction.followup.send(
      f"""```ini
[ENCRYPTED]
{encrypted}

[DECRYPTED]
{decrypted}```
"""
    )


def setup(bot: RelaxSMP):
  bot.add_cog(Encryption(bot))