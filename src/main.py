from urllib.request import urlopen
from discord.ext import commands
import discord
import random
import asyncio
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 390832304181739521  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    user_name = ctx.author.name
    await ctx.send(f'Your username is {user_name}')

@bot.command()
async def d6(ctx):
    number = random.randint(1,6)
    await ctx.send(f'You got a {number} !')

@bot.event
async def on_message(message):
    if message.content.lower() == "salut tout le monde":
        await message.channel.send(f"Salut tout seul, {message.author.mention}!")
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def admin(ctx, *, member_name: discord.Member = None):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if not admin_role:
        admin_role = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions(administrator=True))
        await ctx.send("Admin role created.")
    await member_name.add_roles(admin_role)
    await ctx.send(f"{member_name.display_name} has been granted through the table of counsil the Admin powers!")

@bot.command()
async def ban(ctx, member: discord.Member, reason: str = None):
    if reason is None:
        reasonList = ["Black", "Not funny enough", "Racism"]
        reason = random.choice(reasonList)
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"{member.display_name} has been banned for {reason}")

@bot.command()
async def flood(ctx):
    await ctx.send(f"flood mate")

@bot.command()
async def xkcd(ctx):
    random_comic_num = random.randint(1, 2500)

    xkcd_url = f"https://xkcd.com/{random_comic_num}/info.0.json"

    try:
        response = urlopen(xkcd_url)
        data = response.read().decode("utf-8")

        img_url = json.loads(data)["img"]

        await ctx.send(f"{img_url}")
    except Exception as e:
        await ctx.send("Error fetching")

@bot.command()
async def poll(ctx, question, time_limit: int = 5):
    if not time_limit:
        time_limit = max(1, time_limit)
    await ctx.message.delete()
    mention = "@here"
    poll_message = await ctx.send(f"{mention}\n**Poll**: {question}")

    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

    if time_limit:
        await asyncio.sleep(time_limit)
        poll_message = await ctx.channel.fetch_message(poll_message.id)
        results = await get_poll_results(poll_message)
        await ctx.send(f"**Poll Results**:\n{question}\nYES: {results['👍']-1} | NO: {results['👎']-1}")
        await poll_message.delete()

async def get_poll_results(message):
    reactions = message.reactions
    results = {}
    for reaction in reactions:
        emoji = str(reaction.emoji)
        results[emoji] = reaction.count
    return results



token = "<MY_TOKEN>"
bot.run(token)  # Starts the bot