import discord
from discord.ext import commands
from config import *
from lexicon import * 
from storage import Storage

# NOTE: All developers must add an empty data/ directory at root
Storage.validate_data_dir(DATA_DIR)

#
# Get Discord bot token
#

auth_storage = Storage('auth.json', True)

try:
    # NOTE: add auth.json at root with the token as the only field
    # e.g. { "token": "some_random_token_value" }
    auth_token = auth_storage.read()['token']
except FileNotFoundError:
    print('Cannot start bot without auth token, aborting')
    raise

#
# Load words/phrases
#

# load default and user words
words_storage = Storage('words.txt')
default_words = {'sport', 'chief', 'bud', 'pal', 'champ', 'squirt', 'buster', 'big boy', 'big hoss', 'turbo', 'slugger', 'bucko'}
stored_words = words_storage.read() or []
words = default_words.union(stored_words)
# load default and user phrases
phrases_storage = Storage('phrases.txt')
stored_phrases = phrases_storage.read() or []
default_phrases = {
    'wow, look at you',
    'how ya doin there',
    'keep it up',
    "you'll get em next time",
    'keep your chin up',
    'thanks for that',
    'thanks for the update',
    'the important thing is you tried'
}
phrases = default_phrases.union(stored_phrases)
# define default welcome phrases
default_welcome_phrases = {
    'nice job finding us',
    'introduce yourself to the class',
    'how ya doin there',
    'wow, look at you'
}
# create structures for words/phrases
thesaurus = Thesaurus(words, words_storage)
phrasebook = Phrasebook(phrases, phrases_storage)
welcome_phrasebook = Phrasebook(default_welcome_phrases)

#
# Set basic parameters for Discord bot
#

description = "Treat others how you'd want them to be treated."
# use default Discord intents
intents = discord.Intents.default()
# but ensure the 'members' intent is allowed
intents.members = True
# create bot with parameters
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

#
# Implement common bot events
#

PATRONIZE_CMD = '!patronize'

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print('------')

@bot.event
async def on_member_join(member):
    print('member joined:', member)
    member_to_patronize = member
    soul_crushing_text = '{0.mention} {1}, {2}'.format(
        member_to_patronize,
        welcome_phrasebook.get_random(),
        thesaurus.get_random()
    )
    # assume first channel in list is 'main' channel (e.g. # general)
    FIRST_POS = 0
    main_channel = discord.utils.find(lambda c: c.position == FIRST_POS, member.guild.text_channels)
    await main_channel.send(soul_crushing_text)

@bot.event
async def on_message(message):
    print('message:', message.type, message.content)
    # do not process !patronize command here
    if PATRONIZE_CMD not in message.content:
        # if bot is being mentioned
        if bot.user.mentioned_in(message):
            raw_text_i = message.clean_content.index(bot.user.name) + len(bot.user.name) + 1
            raw_text = message.clean_content[raw_text_i:].strip()
            if raw_text:
                cmd = raw_text.split()[0]
                # basic health check
                if cmd == 'ping':
                    await message.channel.send(message.author.mention + ' pong')
                # print words list in channel
                elif cmd == 'words':
                    # found this gem when looking up embeds:
                    # https://stackoverflow.com/questions/62390411/discord-py-discord-embed-from-dict-not-creating-an-embed-properly
                    words_embed = discord.Embed.from_dict(thesaurus.to_embed_dict())
                    await message.channel.send(embed=words_embed)
                # print phrases list in channel
                elif cmd == 'phrases':
                    phrases_embed = discord.Embed.from_dict(phrasebook.to_embed_dict())
                    await message.channel.send(embed=phrases_embed)
                # add new word to thesaurus
                elif cmd == 'word':
                    new_word_i = raw_text.index(cmd) + len(cmd) + 1
                    new_word = raw_text[new_word_i:].strip()
                    thesaurus.add(new_word)
                    success_embed = discord.Embed.from_dict({
                        'description': f'Patronizor has added **{new_word}** to its thesaurus'
                    })
                    await message.channel.send(embed=success_embed)
                # add new phrase to phrasebook
                elif cmd == 'phrase':
                    new_phrase_i = raw_text.index(cmd) + len(cmd) + 1
                    new_phrase = raw_text[new_phrase_i:].strip()
                    phrasebook.add(new_phrase)
                    success_embed = discord.Embed.from_dict({
                        'description': f'Patronizor has added **{new_phrase}** to its phrasebook'
                    })
                    await message.channel.send(embed=success_embed)
        # remove default Discord new member message
        if message.type == discord.MessageType.new_member:
            await message.channel.delete_messages([message])
    # forward command to normal processing
    await bot.process_commands(message)

#
# Implement patronize command
#

@bot.command()
async def patronize(ctx, username: str):
    patronizing_word = thesaurus.get_random()
    patronizing_phrase = phrasebook.get_random()
    # get member to patronize
    mentions = ctx.message.mentions
    # first check for username, then for mention
    member_by_name = discord.utils.find(lambda m: m.name.lower() == username.lower(), ctx.guild.members)
    member_to_patronize = member_by_name or (mentions[0] if 0 < len(mentions) else None) or None
    if member_to_patronize == bot.user or username == bot.user.name:
        # patronize author for even trying to outsmart me
        await ctx.send(ctx.author.mention + ' nice try, ' + patronizing_word)
        return
    if member_to_patronize is None:
        # patronize author if he fails to do this correctly
        await ctx.send(ctx.author.mention + ' you gotta patronize someone, ' + patronizing_word)
        return
    # generate soul-crushing text and send to channel
    soul_crushing_text = '{0.mention} {1}, {2}'.format(member_to_patronize, patronizing_phrase, patronizing_word)
    await ctx.send(soul_crushing_text)

@patronize.error
async def patronize_error(ctx, error):
    if (isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send(ctx.author.mention + ' you gotta patronize someone, genius')

#
# Run bot
#

bot.run(auth_token)
