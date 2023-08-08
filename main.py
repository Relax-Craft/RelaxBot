from nextcord import Intents
from nextcord.ext import commands, tasks

from utils.cog_load import load_cogs
from extensions.applications.application_ui.view import ApplicationButton, DecideButtons
from extensions.utils.utils_ui.views import InfoReactionRoles
from utils.error_handler.error_handler import ErrorHandler

import os
from dotenv import load_dotenv
import tomli


class RelaxSMP(commands.Bot):
    def __init__(self, config):
        self._channel_ids = config["channels"]
        self._role_ids = config["roles"]
        self._config = config

        self._cog_link = None
        self.cog_files = {}
        self._is_live = False

        intent = Intents.default()
        intent.message_content = True
        # intent.members = True
        
        super().__init__(
            command_prefix = "rc!",
            intents = intent 
        )

        ErrorHandler(self)
        load_cogs(self)

    @property
    def default_color(self):
        return self._config["default_color"]
    
    @property
    def log_color(self):
        return self._config["log_color"]

    @property
    def server_ip(self):
        return self._config["server_ip"]

    @property
    def home_guild_id(self):
        return self._channel_ids["home_guild_id"]

    @property
    def application_channel_id(self):
        return self._channel_ids["application_channel_id"]

    @property
    def log_channel_id(self):
        return self._channel_ids["log_channel_id"]

    @property
    def console(self):
        return self._channel_ids["console_id"]

    @property
    def application_archive_channel_id(self):
        return self._channel_ids["application_archive_channel_id"]

    @property
    def game_chat_id(self):
        return self._channel_ids["game_chat_id"]

    @property
    def announcement_channel_id(self):
        return self._channel_ids["announcement_channel_id"]
    
    @property
    def info_channel_id(self):
        return self._channel_ids["info_channel_id"]

    @property
    def staff_role_id(self):
        return self._role_ids["staff_role_id"]

    @property
    def member_role_id(self):
        return self._role_ids["member_role_id"]

    @property
    def applicant_role_id(self):
        return self._role_ids["applicant_role_id"]
    
    @property
    def bump_role_id(self):
        return self._role_ids["bump_role_id"]
    
    @property
    def announcement_role_id(self):
        return self._role_ids["announcement_role_id"]

    @property
    def news_role_id(self):
        return self._role_ids["news_role_id"]

    @property
    def event_role_id(self):
        return self._role_ids["event_role_id"]

    def add_cog(self, cog: commands.Cog, *, override: bool = False) -> None:
        self.cog_files[cog] = self._cog_link
        super().add_cog(cog, override=override)

    def load_extension(self, name, *, package=None, extras=None):
        self._cog_link = name
        super().load_extension(name, package=package)

        if self._is_live:
            self.task_sync_all_application_commands.start()

    def unload_extension(self, name, *, package=None, reloading=False):
        super().unload_extension(name, package=package)
        deleted_cogs = []

        for cog, link in self.cog_files.items():
            if link == name:
                deleted_cogs.append(cog)
        
        for cog in deleted_cogs:
            del self.cog_files[cog]

        if not reloading:
            self.task_sync_all_application_commands.start()

    def reload_extension(self, name, *, package=None):
        self.unload_extension(name, package=package, reloading=True)
        self.load_extension(name, package=package)
        
    @tasks.loop()
    async def task_sync_all_application_commands(self):
        await self.sync_all_application_commands()
        self.task_sync_all_application_commands.stop()

    async def on_ready(self):
        self.add_view(ApplicationButton(self))
        self.add_view(DecideButtons(self))
        self.add_view(InfoReactionRoles(self))

        self._is_live = True
        print("ready")

    async def on_close(self):
        self._is_live = False


if __name__ == "__main__":
    with open("./config.toml", mode="rb") as fp:
        config = tomli.load(fp)

    relax_smp: RelaxSMP = RelaxSMP(config["bot"])
    load_dotenv(".env")
    token = os.getenv("BotToken")

    relax_smp.run(token)