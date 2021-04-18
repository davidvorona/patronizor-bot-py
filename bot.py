import json
import discord
from discord.ext import commands
from random import randrange

# add auth.json at root with the token as the only field
# e.g. { "token": "some_random_token_value" }
with open('auth.json', 'r') as file:
    auth_token = json.loads(file.read())['token']

description = "Treat others how you'd want them to be treated."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print('------')

@bot.event
async def on_member_join(member):
    print('member joined:', member)

    patronizing_phrases = ['nice job finding us', 'introduce yourself to the class', 'how ya doin there', 'wow, look at you']
    patronizing_words = ['sport', 'chief', 'bud', 'pal', 'champ', 'squirt', 'buster', 'big boy', 'big hoss', 'turbo', 'slugger']
    phraseIndex = randrange(0, len(patronizing_phrases))
    wordIndex = randrange(0, len(patronizing_words))
    member_to_patronize = member
    soul_crushing_text = '{0.mention}, {1} {2}'.format(member_to_patronize, patronizing_phrases[phraseIndex], patronizing_words[wordIndex])

    FIRST_POS = 0
    main_channel = discord.utils.find(lambda c: c.position == FIRST_POS, member.guild.text_channels)

    await main_channel.send(soul_crushing_text)

@bot.event
async def on_message(message):
    print('message:', message.type, message.content)

    if message.type == discord.MessageType.new_member:
        await message.channel.delete_messages([message])
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def patronize(ctx, username: str):
    patronizing_phrases = ['wow, look at you', 'how ya doin there', 'keep it up', "you'll get em next time", 'keep your chin up', 'thanks for that', 'thanks for the update']
    patronizing_words = ['sport', 'chief', 'bud', 'pal', 'champ', 'squirt', 'buster', 'big boy', 'big hoss', 'turbo', 'slugger']
    phraseIndex = randrange(0, len(patronizing_phrases))
    wordIndex = randrange(0, len(patronizing_words))
    member_to_patronize = ctx.guild.get_member_named(username)
    soul_crushing_text = '{0.mention}, {1} {2}'.format(member_to_patronize, patronizing_phrases[phraseIndex], patronizing_words[wordIndex])

    await ctx.send(soul_crushing_text)

bot.run(auth_token)