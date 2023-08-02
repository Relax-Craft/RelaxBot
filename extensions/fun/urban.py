from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed, slash_command
from nextcord.ui import View, Button
from main import RelaxSMP


class UrbanDictionary(commands.Cog):
    def __init__(self, bot: RelaxSMP):
        self.bot: RelaxSMP = bot

    @slash_command("urban")
    async def dectionary_slash(
        self, 
        interaction: Interaction, 
        query: str =SlashOption(description="What word or expression do you want to look for?")
      ):
        url = "https://www.urbandictionary.com/define.php?term="
        url_query = query.replace(" ", "%20")
        url += url_query

        embed = Embed(
          title="Enlgisch Gud 👍",
          color=self.bot.default_color,
          description="Let's learn with Urban dictionary xD"
        )
        embed.add_field(
          name="Query",
          value=f"```{query}```"
        )

        view = View(timeout=None)
        url_button = Button(label="Explanation", url=url)
        view.add_item(url_button)

        await interaction.send(embed=embed, view=view)


def setup(bot: RelaxSMP):
    bot.add_cog(bot)