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

    # if bot is being mentioned
    if bot.user.mentioned_in(message):
        # basic health check
        if message.content.endswith('ping'):
            await message.channel.send(message.author.mention + ' pong')

    if message.type == discord.MessageType.new_member:
        await message.channel.delete_messages([message])

    await bot.process_commands(message)

@bot.command()
async def patronize(ctx, username: str):
    # get randomized index of word and phrase
    patronizing_phrases = ['wow, look at you', 'how ya doin there', 'keep it up', "you'll get em next time", 'keep your chin up', 'thanks for that', 'thanks for the update']
    patronizing_words = ['sport', 'chief', 'bud', 'pal', 'champ', 'squirt', 'buster', 'big boy', 'big hoss', 'turbo', 'slugger']
    phrase_index = randrange(0, len(patronizing_phrases))
    word_index = randrange(0, len(patronizing_words))

    # get member to patronize
    mentions = ctx.message.mentions
    # first check for username, then for mention
    member_to_patronize = ctx.guild.get_member_named(username) or (mentions[0] if 0 < len(mentions) else None) or None
    if member_to_patronize is None:
        # patronize author if he fails to do this correctly
        await ctx.send(ctx.author.mention + ' you gotta patronize someone, ' + patronizing_words[word_index])
        return

    # generate soul-crushing text and send to channel
    soul_crushing_text = '{0.mention}, {1} {2}'.format(member_to_patronize, patronizing_phrases[phrase_index], patronizing_words[word_index])
    await ctx.send(soul_crushing_text)

@patronize.error
async def patronize_error(ctx, error):
    if (isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send(ctx.author.mention + ' you gotta patronize someone, genius')

bot.run(auth_token)
