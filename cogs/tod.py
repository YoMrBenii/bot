import random
import discord
from discord.ext import commands

class TruthOrDareView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Truth", style=discord.ButtonStyle.success, custom_id="tod_truth")
    async def truth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        question = self.cog.get_random_truth()
        if not question:
            await interaction.response.send_message(
                embed=discord.Embed(description="No truth questions available.", color=discord.Color.red()), ephemeral=True
            )
            return
        embed = discord.Embed(title=question, color=discord.Color.green(), )
        embed.set_footer(text=f"Sent by {user.display_name}")
        await interaction.response.send_message(embed=embed, view=TruthOrDareView(self.cog))

    @discord.ui.button(label="Dare", style=discord.ButtonStyle.danger, custom_id="tod_dare")
    async def dare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        dare = self.cog.get_random_dare()
        if not dare:
            await interaction.response.send_message(
                embed=discord.Embed(description="No dares available.", color=discord.Color.red()), ephemeral=True
            )
            return
        embed = discord.Embed(title=dare, color=discord.Color.red())
        embed.set_footer(text=f"Sent by {user.display_name}")
        await interaction.response.send_message(embed=embed, view=TruthOrDareView(self.cog))

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_truths = ["Have you ever watched gay porn?", "At what age did you start masturbating?", "Have you ever comitted a crime, if so which?", "Whats your least favourite race?", "Whats the weirdest place where you masturbated?", "Would you ever let yourself get pegged/Peg somebody?", "What was your longest relationship?", "How tall are you?", "Have you ever been caught gooning?", "If you could molest one person in this chat, who would you?", "Would you rather date an indian or a nigger?", "How long is your dick?", "Would you rather kill a baby or 100 very old ladies?", "Would you ever go skydiving?", "Ass or titties?", "Would you suck a dick for 1,000 dollars?", "Whats the longest time you went without sleep?", "Whats your record for the most times you gooned in a day?", "How long was your longest gooning session?", "Do you think 9/11 was an inside job?", "How many languages do you know and which?", "Whos the most retarded person in the chat rn?", "How much do you weigh?", "How tall are you?", "Which country has the hottest people in your opinion?", "Have you cheated on somebody in the past?", "Do u hate period cramps?", "Have you ever thought about killing yourself?", "Do you wear glasses or contacts?", "How many romantic partners did you have in total?", "Do you think its morally okay to goon infront of a dog?", "Have you ever taken a shit in the wilderness?", "Summer or winter?", "Which celebrity would you smash with no hesitation?", "Would you ever smash a granny?", "When do you go to sleep on weekends normally?", "Have you ever fallen down the stairs?", "What's your favorite roblox game?", "Whats the most inappropriate time youve laughed?", "Are you scared of insects?","Whats the most recent thing you cried over?", "What do you wanna do when your older?", "Have you ever beaten minecraft without cheats?", "Have you ever had sexual fantasies about your classmates?", "Would you be open to getting a tattoo?", "Do you work out?, If not why are you not working out yet fatass?", "Would you rather be skinny or be fat?", "Why do you believe in god/Or dont?", "How often do you eat mcdonalds per month?", "Have you ever been kissed by a non family member?", "If you could instantly acquire any skill, which one would you wanna have?", "Do bikinis look better high waisted or low waisted?", "How did you come up with your nickname?", "Have you ever gooned to feet?", "Can you swim?", "Have you ever heard your parents having sex?", "Do you have a j*b?", "Whats your dream j*b?", "Whats your favourite phrase?", "Whats your favourite car brand?", "Whats the most expensive car youve ever been in?", "How many close friends do you have?", "Whats your opinion on bald people?", "Have you ever been on a speedboat?", "Have you ever gotten drunk?", "Do you smoke/vape?", "Whats your favourite energy drink?", "Whats your favourite soda?", "Die a virgin or be homosexual?", "Have you ever donated to a charity?","Would you rather eat a cat or a dog?", "Do you think iphone is better than android?", "Whats your opinion on donald trump?", "Would you rather get molested by diddy or by epstein?", "Would you rather be jewish or gay?", "Is your family rich or poor?", "Have you ever had a close death encounter?", "How old is too old to be a virgin?", "Do you prefer mornings or evenings?", "Whats the most amount of money you spent at once?", "Whats the longest you went without a shower?", "Have you ever considered visiting india?", "Whens your birthday?", "Have you ever seen a naked person in public?", "Have you ever cheated on an exam?", "How long is too long (dick size)", "Have you ever said nigga in public?", "If you had to live as an animal, which animal would you wanna live as?", "Which insect do you hate the most?", "What would you do first if you switched genders?", "What do you do when your bored?", "Have you ever destroyed someone elses relationship?", "If you could make one person on the world disappear forever, who would that be?","Whats the longest time youve been without your parents and why?", "Have you ever gotten rejected?", "Do you have any mental disorders?", "Have you ever skipped school?", "Have you ever visited an abandoned building?", "Have you tried starting a yt channel in the past?", "What app do you spend the most time on?", "Whats your favourite porn category?", "Do you do sports in your free time, if so which sports?", "Which hair color do you find the most attractive?", "Would you fuck a homosexual jew?", "Whos your favourite staff member right now?", "Who do you hate the most in pvp?", "Are your teeth white or yellow?", "How much battery does your phone have rn?", "How long do you sleep most of the time?", "Have you had a nightmare this year yet?", "Do you still watch tv in 2025?", "How long could you run continuously?", "What was your longest hike?", "Do you live in an apartment or in a house?", "Whats your favourite singer?", "Messi or ronaldo?", "Whats the most expensive thing youve lost?", "Has a non family member seen you naked before?", "Whats your opinion on goth mommies?", "Have you been at a concert before, if so which?", "What phone model do you have?", "Have you ever catfished somebody?", "Whats your favourite type of meat?", "Would you go vegan for 100,000$?", "Have you ever gotten detention and if so, for what?", "Whats your least favourite school subject?", "Do you have any chores?", "Whos your favourite influencer?", "What was the longest car ride youve been on?", "Have you ever touched a spider?", "Whos the oldest person you know in pvp?", "Who do you suspect being underage in pvp?", "Is lebron smash?", "How much robux do you have?", "How much money is in your bank account?", "Whats your most expensive subscription?", "If you had to choose between anal or oral, what are you choosing?", "Do you plan on buying a sex toy when your older?", "How young is too young for you?", "Are you able to crack your finger joints?", "Have you ever gotten into a physical fight in public?", "Do you know how to ride a bike?", "Have you ever been to a circus?", "Have you shat in a public bathroom this year?", "Whats your favourite shoe brand?", "Have you ever pissed yourself in your sleep when you were smaller?", "Have you ever broken a bone?", "Did you ever have a surgery?", "Have any of your accounts ever gotten banned?", "Whats your longest friendship?", "How did you find out about pvp clan?", "Have you ever gotten scammed?", "Is it football or soccer?", "Whats your favourite film?", "Do you like going on planes?", "Do you like saunas?", "Where do you come from?", "Have you ever visited a cave?", "Do you have grand grandparents?", "What role in pvp do you think looks the best?", "When did you start playing bedwars?", "Have you ever considered joining the military?", "Is your diet healthy or unhealthy?", "Which country would you love to live in?", "If you had to live in any country from africa, which one would you live in?", "How many children do you want?", "Have you ever put a pill up your fat juicy ass?", "Have you ever put your hand inside your asshole?", "Whats your least favourite country?", "What made you racist?", "If you won the lottery, what you buying?", "Can you do a handstand?", "How many pushups can you do in one go?", "Have you ever tried doing a backflip?", "Whats the best month of the year?", "Would you rather be able to go invisible on command or stop time for 5 mins daily on command?", "Whats your favourite anime?", "Whats the most exciting thing you did today?", "Are you circumcised?", "Whats your favourite dish?", "Have you ever left the country on your own?", "Whats your favourite day of the week?", "Watermelon or fried chicken?", "Whats your favourite sex position?", "Would you sacrifice yourself for your family?", "Do you prefer your mom or your dad?", "If you could revive anybody, who would it be?", "Have you ever trained material arts?", "Whats your most used website?", "Have you ever learnt a lesson from your old relationships?", "If you could eradicate any group of people, who would they be?", "Has the opposite gender hugged you before?", "Whats the longest you slept for?", "Do you prefer google or chatGPT?", "How much storage does your phone have?", "Do you have a morning routine?", "Whats your longest friendship?", "Are you introverted or extroverted?", "Whats the longest you can hold your breath for?", "Do you use your phone on the toilet?", "Have you ever been grounded?", "Would you suck a dick for your best friends life?"]
        self.all_dares = ["Tell us the city you live in.", "Send a voice message of you barking.", "Dm a member from pvp with the opposite gender saying I love you.", "Go in vc and livestream porn", "Insult someone in the chat who you think is a victim", "Show a picture of your feet", "Set your pfp to whatever picture gets sent first for 10 mins", "Act like your homosexual for 10 mins", "Show us your latest photo in your gallery", "Raid a random server (not pvp)", "Type with your feet for 1 minute", "Donate 10k bot money to someone in the chat", "Write a short essay about how stupid you are", "Livestream your search history", "Imitate somebody from pvp for a minute", "Tell us your email", "Go in vc and moan for us", "Ragebait someone in pvp till they insult you.", "Impersonate an active pvp member for a day.", "Spam ping someones dms till they get mad", "Send a picture of your hand oiled up in peanut butter", "Send the oldest photo on your phone", "Type a sentence with your eyes closed", "Chat in a different language for a minute", "Reveal a random secret someone from pvp told you", "Get together with a random person for a day", "Text your best friend *Thanks for everything* and dont respond for a day", "Say the n word in vc", "Scream in vc whatever the chat tells you to say", "Show your screentime.", "You have permission to mute someone for one minute, mute whoever you want"]
        self.available_truths = self.all_truths.copy()
        self.available_dares = self.all_dares.copy()

    def get_random_truth(self):
        if not self.available_truths:
            if not self.all_truths:
                return None
            self.available_truths = self.all_truths.copy()
        question = random.choice(self.available_truths)
        self.available_truths.remove(question)
        return question

    def get_random_dare(self):
        if not self.available_dares:
            if not self.all_dares:
                return None
            self.available_dares = self.all_dares.copy()
        dare = random.choice(self.available_dares)
        self.available_dares.remove(dare)
        return dare

    @commands.command(name="tod")
    async def tod(self, ctx):
        embed = discord.Embed(title="Truth or Dare?", description="Pick one by pressing a button below.", color=discord.Color.blurple())
        view = TruthOrDareView(self)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(TruthOrDare(bot))
