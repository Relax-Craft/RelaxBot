import nextcord
from nextcord.ui import Modal, TextInput
from nextcord import Interaction, Embed, TextInputStyle

class User_Related_Input(Modal):
    def __init__(self, bot, questions, platform):
        self.bot = bot
        self.q_n_a = {}
        self.ign = None
        self.questions = questions
        self.embed = None
        self.platform = platform

        super().__init__(title="Application for RelaxSMP", timeout=12*60)

        for question_number, question in self.questions.items():
            text_input = TextInput(
                    label=question[0],
                    placeholder=question[2],
                    style=TextInputStyle.short if question[1] == "short" else TextInputStyle.paragraph,
                    max_length=1000,
                    # default_value="GangstaMuffin",
                    required=True
                )
            
            if self.ign == None:
                self.ign = text_input

            self.q_n_a[question[0]] = text_input
            self.add_item(text_input)


    async def callback(self, interaction: Interaction):
        user_related_embed = Embed(title=f"{self.platform} | {interaction.user.display_name}", color=self.bot.default_color)
        user_related_embed.set_thumbnail(url=interaction.user.avatar.url)
        user_related_embed.set_footer(text=f"id: {interaction.user.id}")
        
        for question, answer in self.q_n_a.items():
            user_related_embed.add_field(name=question, value=f"```{answer.value}```", inline=False)

        self.embed = user_related_embed
        self.stop()


class CommunityRelated(Modal):
    def __init__(self, questions, embed):
        self.q_n_a = {}
        self.ign = None
        self.questions = questions
        self.embed = embed
        super().__init__(title="Application for RelaxSMP", timeout=12*60)

        self.time_expired = False

        for question_number, question in self.questions.items():
            text_input = TextInput(
                    label=question[0],
                    placeholder=question[2],
                    style=TextInputStyle.short if question[1] == "short" else TextInputStyle.paragraph,
                    max_length=1000,
                    # default_value="GangstaMuffin",
                    required=True 
                )
            
            if self.ign == None:
                self.ign = text_input

            self.q_n_a[question[0]] = text_input
            self.add_item(text_input)


    async def callback(self, interaction: Interaction):
        for question, answer in self.q_n_a.items():
            self.embed.add_field(name=question, value=f"```{answer.value}```", inline=False)
        self.stop()


class DecisionReason(Modal):
    def __init__(self):
        super().__init__("Decision Reason", timeout=5*60)

        self.reason = TextInput(
            label="Reason for your decision?",
            required=False,
            style=TextInputStyle.paragraph,
            max_length=1000
        )

        self.add_item(self.reason)


    async def callback(self, interaction: Interaction):
        self.stop()