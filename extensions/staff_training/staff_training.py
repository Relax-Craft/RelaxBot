from nextcord.ext import commands
from nextcord import Embed, Interaction, slash_command, Webhook, PermissionOverwrite
import aiohttp

from main import RelaxSMP


class Test(commands.Cog):
    def __init__(self, bot: RelaxSMP) -> None:
        super().__init__()

        self.bot: RelaxSMP = bot

    def get_webhook(self):
        session = aiohttp.ClientSession()
        webhook = Webhook.from_url(
                'https://discord.com/api/webhooks/1104717611519971388/14mKTQGAsSJ4-716dwoH2RgOeLEbLilx53vfqOk5Vpyn481_n7P2Zv_9Y96or82l_AnW', 
                session=session
            )
        return session, webhook

    @commands.command(name="training")
    async def prefix_staff_training(self, ctx):
        overwrites = {
            ctx.guild.default_role: PermissionOverwrite(view_channel = False),
            ctx.auhor: PermissionOverwrite(view_channel=True, send_messages=False)
        }
        
        channel = await ctx.guild.create_text_channel(f"Training - {ctx.author.name}")
        
        session, webhook = self.get_webhook()
        
        await webhook.send("does this work?")
        await session.close()

    @slash_command(name="training")
    async def slash_staff_training(self, interaction: Interaction):
        session, webhook = self.get_webhook()
        
        await webhook.send("does this work?")
        await session.close()


def setup(bot: RelaxSMP):
    bot.add_cog(Test(bot))