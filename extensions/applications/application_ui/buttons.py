from nextcord import Interaction, ButtonStyle, Member, MessageType
from nextcord.ui import button, Button, View
# import json
from utils.file_load import application_questions

from .modals import *


class ApplicationButton(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot


    @button(label="Java", style=ButtonStyle.blurple, custom_id="persistent_view:java")
    async def application_button(self, button: Button, interaction: Interaction):
        await self.application_process(interaction, "Java")


    @button(label="Bedrock", style=ButtonStyle.blurple, custom_id="persistent_view:bedrock")
    async def bedrock_application(self, button: Button, interaction: Interaction):
        await self.application_process(interaction, "Bedrock")
        

    async def application_process(self, interaction: Interaction, platform):
        application_archive_channel = self.bot.get_channel(self.bot.application_archive_channel_id)
        
        for role in interaction.user.roles:
            if role.id == self.bot.member_role_id:
                await interaction.send("You've already been accepted to the server!", ephemeral=True)
                return
            if role.id == self.bot.applicant_role_id:
                await interaction.send("You already have an ongoing application!", ephemeral=True)
                return
        
        questions = application_questions()
        applicant_role = interaction.guild.get_role(self.bot.applicant_role_id)
        await interaction.user.add_roles(applicant_role)

        user_related_input = User_Related_Input(self.bot, questions["user_related"], platform)
        await interaction.response.send_modal(user_related_input)
        timeout = await user_related_input.wait()

        if timeout:
            await interaction.followup.send("Time expired!", ephemeral=True)
            await application_archive_channel.send(f"`{interaction.user.display_name}'s Application timed out!` ||id: {interaction.user.id}||")
            await interaction.user.remove_roles(applicant_role)
            return
        
        application_message = await interaction.followup.send(embed=user_related_input.embed, ephemeral=True)
        proceed = ContinueApplicationButtons(interaction.user, application_message, user_related_input.embed, questions["community_related"])
        await application_message.edit(view=proceed)
        timeout = await proceed.wait()

        if proceed.canceled:
            await interaction.user.remove_roles(applicant_role)
            return
        elif proceed.timed_out or timeout:
            await interaction.followup.send("`Application Error: Timeout`", ephemeral=True)
            await application_archive_channel.send(f"`{interaction.user.display_name}'s Application timed out!` ||id: {interaction.user.id}||")
            await interaction.user.remove_roles(applicant_role)
            return

        await application_message.edit(embed=proceed.embed)
        application = await application_archive_channel.send(embed=proceed.embed, view=DecideButtons(self.bot, user_related_input.ign.value, interaction.user))
        await application.pin(reason="New Application")
        
        async for message in interaction.client.get_channel(self.bot.application_archive_channel_id).history(limit=4):
            if message.type == MessageType.pins_add:
                await message.delete()


class ContinueApplicationButtons(View):
    def __init__(self, user, application, embed, questions):
        super().__init__(timeout=10*60)
        self.user = user
        self.application = application
        self.embed = embed
        self.questions = questions
        self.canceled = False
        self.timed_out = False


    @button(label="Continue", style=ButtonStyle.success)
    async def next_questions(self, button: Button, interaction: Interaction):
        community_related_input = CommunityRelated(self.questions, self.embed)
        await interaction.response.send_modal(community_related_input)

        for button in self.children:
            button.disabled = True
        await self.application.edit(view=self)

        self.timed_out = await community_related_input.wait()

        self.embed = community_related_input.embed
        self.stop()


    @button(label="Cancel", style=ButtonStyle.danger)
    async def cancel_application(self, button: Button, interaction: Interaction):
        if interaction.user.id != self.user.id:
            await interaction.send("This isn't for you!", ephemeral=True)
            return
        
        await self.application.edit(view=None, embed=None, content="`Application Terminated`")
        self.canceled = True
        self.stop()


class DecideButtons(View):
    def __init__(self, bot, in_game_name=None, applicant=None):
        self.bot = bot
        
        self.ign = in_game_name
        self.applicant: Member = applicant
        super().__init__(timeout=None)


    @button(label="Accept", style=ButtonStyle.success, custom_id="persistent_view:accept")
    async def accept_applicant(self, button: Button, interaction: Interaction):
        for role in interaction.user.roles:
            if role.id == self.bot.staff_role_id:
                break
            
        else:
            error = Embed(title="__Error__", description="You don't have permission to use that!", color=self.bot.default_color)
            await interaction.send(embed=error, ephemeral=True)
            return

        modal = DecisionReason()
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        await interaction.message.unpin(reason="Application Handled")

        if self.ign == None:
            self.ign = interaction.message.embeds[0].fields[0].value.replace("```", "")

        if self.applicant == None:
            self.applicant = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text.replace("id: ", "")))

        for button in self.children:
            button.disabled = True
        
        accepted_info = Embed(title=f"Application Accepted by {interaction.user.display_name}", color=0x08E500)
        reason = modal.reason.value
        accepted_info.add_field(name="Reason", value=f"```{reason if len(reason)>0 else 'None'}```", inline=False)

        await interaction.edit(view=self, embeds=[interaction.message.embeds[0], accepted_info])

        applicant_role = interaction.guild.get_role(self.bot.applicant_role_id)
        member_role = interaction.guild.get_role(self.bot.member_role_id)
        await self.applicant.edit(nick=self.ign)
        await self.applicant.add_roles(member_role)
        await self.applicant.remove_roles(applicant_role)

        application = interaction.message.embeds[0]
        app_title = application.title

        if app_title.startswith("Bedrock"):
            self.ign = "."+self.ign

        console_channel = interaction.client.get_channel(self.bot.console)
        await console_channel.send(f"whitelist add {self.ign}")


    @button(label="Decline", style=ButtonStyle.danger, custom_id="persistent_view:deny")
    async def deny_application(self, button: Button, interaction: Interaction):
        for role in interaction.user.roles:
            if role.id == self.bot.staff_role_id:
                break
        else:
            error = Embed(title="__Error__", description="You don't have permission to use that!", color=self.bot.default_color)
            await interaction.send(embed=error, ephemeral=True)
            return

        modal = DecisionReason()
        await interaction.response.send_modal(modal)
        await modal.wait()

        await interaction.message.unpin(reason="Application Handled")

        if self.applicant == None:
            print(interaction.message.embeds[0].footer.text)
            self.applicant = interaction.client.get_user(int(interaction.message.embeds[0].footer.text.replace("id: ", "")))
        
        applicant_role = interaction.guild.get_role(self.bot.applicant_role_id)
        await self.applicant.remove_roles(applicant_role)

        for button in self.children:
            button.disabled = True

        declined_info = Embed(title=f"Application Declined by {interaction.user.display_name}", color=self.bot.default_color)
        reason = modal.reason.value
        declined_info.add_field(name="Reason", value=f"```{reason if len(reason)>0 else 'None'}```", inline=False)

        await interaction.edit(view=self, embeds=[interaction.message.embeds[0], declined_info])

            


# User dm channel - doesn't accept dms from mutual guilds