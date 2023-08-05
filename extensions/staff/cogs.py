from nextcord import Interaction, slash_command, Permissions
from nextcord.ext import commands

from difflib import get_close_matches
import os

from main import RelaxSMP


class CogHandeling(commands.Cog):
    def __init__(self, bot: RelaxSMP) -> None:
        self.bot: RelaxSMP = bot

    def cog_recognition(self, cog: str):
        options = [key.qualified_name for key, _ in self.bot.cog_files.items()]
        match = get_close_matches(cog, options)

        return match if match else options
        
    @slash_command(
		name="cog", 
		default_member_permissions=Permissions(administrator=True)
    )
    async def slash_cog(self, interaction: Interaction):
        return

    @slash_cog.subcommand(name="unload")
    async def slash_cog_unload(self, interaction: Interaction, cog: str):
        matches = self.cog_recognition(cog)

        if not matches:
            await interaction.send("Cog not recognized!", ephemeral=True)
    
        # Make it easier to access cogs: file with qualified name
        for cog, file in self.bot.cog_files.items():
            if cog.qualified_name == matches[0]:
                cog_file = file

        self.bot.unload_extension(cog_file)
        await interaction.send(f"{matches[0]} Unloaded!", ephemeral=True)

    @slash_cog_unload.on_autocomplete("cog")
    async def autocomplate_cog_unload(self, interaction: Interaction, cog: str):
        await interaction.response.send_autocomplete(
            self.cog_recognition(cog)
        )

    @slash_cog.subcommand(name="reload")
    async def slash_cog_reload(self, interaction: Interaction, cog: str):
        options = [key.qualified_name for key, _ in self.bot.cog_files.items()]
        if cog not in options:
            await interaction.send("Cog not recognized!", ephemeral=True)
    
        # Make it easier to access cogs: file with qualified name
        for loaded_cog, file in self.bot.cog_files.items():
            if loaded_cog.qualified_name == cog:
                cog_file = file
                # break

        self.bot.reload_extension(cog_file)
        await interaction.send(f"{cog} Reloaded!", ephemeral=True)
    
    @slash_cog_reload.on_autocomplete("cog")
    async def autocomplate_cog_reload(self, interaction: Interaction, cog: str):
        await interaction.response.send_autocomplete(
            self.cog_recognition(cog)
        )

    @slash_cog.subcommand(name="load")
    async def slash_cog_load(self, interaction: Interaction, path: str):
        if path.endswith(".py"):
            path = path.removesuffix(".py")
        if path.startswith("./"):
            path = path.removeprefix("./")
        if not path.startswith("extensions."):
            path = "extensions."+path
        if "/" in path:
            path = path.replace("/", ".")
        
        try:
            self.bot.load_extension(path)
            await interaction.send(f"loading {path}", ephemeral=True)
        except ModuleNotFoundError:
            await interaction.send("Module Not Found!", ephemeral=True)
    
    @slash_cog_load.on_autocomplete("path")
    async def autocomplate_cog_load(self, interaction: Interaction, path: str):
        path: list = path.split(".")
        path.remove("extensions") if "extensions" in path else None
        nav = "./extensions"

        # Folder in extensions
        dirs = [file for file in os.listdir(nav)]
        close_matches = get_close_matches(path[0], dirs)

        if not close_matches:
            return

        if len(path) == 1:
            matches = [f"extensions.{x}" for x in close_matches]
            await interaction.response.send_autocomplete(matches)
            return
        
        nav += f"/{close_matches[0]}"

        if nav.endswith(".py"):
            await interaction.response.send_autocomplete(nav)
            return

        # subfolder/file in extensions folder
        # If we are here, user wants to go a level deeper, best match wasn't a file
        dirs = [file for file in os.listdir(nav)]
        close_matches = get_close_matches(path[1], dirs)

        if len(path) == 2:
            nav = nav.removeprefix("./")
            nav = nav.replace("/", ".")
            matches = [f"{nav}.{x}" for x in close_matches]
            await interaction.response.send_autocomplete(matches)
            return
        
        nav += f"/{close_matches[0]}"

        if nav.endswith(".py"):
            await interaction.response.send_autocomplete(nav)
            return

        # If we are here, file might be another level lower
        # If wer are here, same criteria from before applies
        dirs = [file for file in os.listdir(nav)]
        close_matches = get_close_matches(path[2], dirs)

        matches = [f"{nav}.{x}" for x in close_matches]
        await interaction.response.send_autocomplete(matches)


def setup(bot: RelaxSMP):
    bot.add_cog(CogHandeling(bot))