from nextcord import Intents
from nextcord.ext import commands

from utils.cog_load import load_cogs
from  extensions.applications.application_ui.buttons import ApplicationButton, DecideButtons
from extensions.utils.utils_ui.views import InfoReactionRoles

import os
from dotenv import load_dotenv
import tomli


class RelaxSMP(commands.Bot):
    def __init__(self, config):
        self._channel_ids = config["channels"]
        self._role_ids = config["roles"]
        self._config = config

        intent = Intents.default()
        intent.message_content = True
        # intent.members = True
        
        super().__init__(
            command_prefix = "rc!",
            intents = intent 
        )

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
    def game_chat_id(self):
        return self._channel_ids["game_chat_id"]
    
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

    async def on_ready(self):
        self.add_view(ApplicationButton(self))
        self.add_view(DecideButtons(self))
        self.add_view(InfoReactionRoles(self))

        print("ready")


if __name__ == "__main__":
    with open("./config.toml", mode="rb") as fp:
        config = tomli.load(fp)

    relax_smp: RelaxSMP = RelaxSMP(config["bot"])
    load_dotenv(".env")
    token = os.getenv("BotToken")

    relax_smp.run(token)