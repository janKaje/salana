import discord
from discord.ext import commands, tasks
import os
import time
import math
from datetime import datetime as dt
import json
import requests

#Initialize
client = commands.Bot(command_prefix = ',')
client.remove_command('help')
dir_path = os.path.dirname(os.path.abspath(__file__))

try:
    open(dir_path+'/config.json', mode='x')
except:
    pass

config = dict()

for i in os.environ:
    try:
        int(i)
        config[i] = json.loads(os.environ[i])
    except:
        pass

print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))

TOKEN = os.environ['TOKEN']

#On_ready command
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('type ,help for help'))

#function to handle updating of config
async def updateconfig():
    #gets new additions to cog-specific config elements
    questions = client.get_cog('QUESTIONS')
    tokipona = client.get_cog('TOKI PONA')
    fun = client.get_cog('FUN')
    newquestions = questions.newquestions
    newudspcs = tokipona.newudspcs
    newglyphs = tokipona.newdefaultglyphs
    newguildhighscores = fun.newguildhighscores
    newpersonalhighscores = fun.newpersonalhighscores

    #updates the main config with all the new stuff
    for i in config:
        if isinstance(config[i], dict):
            if i in newguildhighscores:
                config[i]['hsu'] = newguildhighscores[i][0]
                config[i]['hsv'] = newguildhighscores[i][1]
            if i in newquestions:
                config[i]['questions'] = newquestions[i]
            if i in newudspcs:
                for j in newudspcs[i]:
                    config[i]['tp']['udspc'][j] = newudspcs[i][j]
            if i in newglyphs:
                for j in newglyphs[i]:
                    config[i]['tp']['defaultglyphs'][j] = newglyphs[i][j]
    for i in newpersonalhighscores:
        config[i] = newpersonalhighscores[i]
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))

    #adds everything that's changed to the data to be readded
    data = dict()
    for i in config:
        if i not in os.environ or config[i] != json.loads(os.environ[i]):
            data[i] = json.dumps(config[i])
    data = json.dumps(data)

    #makes the request
    headers = {"Content-Type": "application/json", "Accept": "application/vnd.heroku+json; version=3"}
    auth = (os.environ['usern'], os.environ['apitoken'])
    url = 'https://api.heroku.com/apps/salana/config-vars'
    requests.patch(url, data=data, headers=headers, auth=auth)

#resets heroku config keys when disconnects
@client.event
async def on_disconnect():
    await updateconfig()

#Load, unload, reload cog commands
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    """Loads a specified extension."""
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Loaded successfully.")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Unloads a specified extension."""
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Unloaded successfully.")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Reloads a specified extension, or all of them."""
    #if input is not 'all', reloads a specified extention
    if str(extension) != 'all':
        try:
            client.reload_extension(f"cogs.{extension}")
            await ctx.send("Reloaded successfully.")
        #if extension is already loaded
        except Exception as e:
            try:
                client.load_extension(f'cogs.{extension}')
                await ctx.send("Reloaded successfully.")
            except:
                #something else happened
                await ctx.send(f'There was an error reloading the extention: {e}')
    #if input is 'all', reloads all extensions.
    else:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.{filename[:-3]}")
        await ctx.send("All extensions reloaded.")

#Automatically loads all cogs in ./cogs on startup
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
    
@client.event
async def on_guild_join(guild):
    #sets basic guild variables
    config[str(guild.id)] = {'hsu': 'nobody', 'hsv': -1, 'tp': {'udspc': dict(), 'tasochannelids': [], 'spchannel': None, 'defaultglyphs': dict()}, 'hardcore': None, 'welcome': None, 'questions': None, 'reporting': None, 'logging': None}
    
    #sends first message and asks if it should use pa mu or tp
    embed = discord.Embed(title='Hello!', description="I'm salana, a discord bot developed to add toki pona or pa mu features to your server. To begin, select whether this guild is\n\n1️⃣ a toki pona server, or\n2️⃣ a pa mu server.\n\nThis can be changed later with the `,switchlanguage` command.", color=discord.Color.blue())
    for channel in guild.text_channels:
        try:
            msg = await channel.send(embed=embed)
            await msg.add_reaction('1️⃣')
            await msg.add_reaction('2️⃣')
            break
        except:
            try:
                await msg.delete
            except:
                pass
    else:
        await guild.me.edit(nick="couldn't send setup msg", reason="If you're reading this, I tried to send a message to initialize my features. I wasn't able to, and as a result, the pa mu features are enabled by default. If you want to use the toki pona features, you need to use \",switchlanguage\"")
        return

    #all this is to see the reaction and parse it
    def check(reaction, user):
        nonlocal channel, msg
        return channel.permissions_for(user).manage_guild and reaction.message.id == msg.id and str(reaction.emoji) in '1️⃣2️⃣'

    reaction, _ = await client.wait_for('reaction_add', check=check)
    
    if str(reaction.emoji) == '1️⃣':
        await channel.send("Congrats! Give me a few seconds to save the data. Once I'm done, you'll be able to use all of the base toki pona features.\n\nI have many more modules than this. If you'd like to see them, use `,server`. To see more information about a module, or to learn how to enable it, use `,help <module>`. To set channels in which I will try to only speak in toki pona, use the command `,settaso` in those channels.")
    elif str(reaction.emoji) == '2️⃣':
        config[str(guild.id)]['tp'] = None
        await channel.send("Congrats! Give me a few seconds to save the data. Once I'm done, you'll be able to use all of the pa mu features.\n\nI have many more modules than this. If you'd like to see them, use `,server`. To see more information about a module, or to learn how to enable it, use `,help <module>`.")
    
    await updateconfig()

@client.event
async def on_guild_remove(guild):
    del config[str(guild.id)]
    data = {str(guild.id): None}
    headers = {"Content-Type": "application/json", "Accept": "application/vnd.heroku+json; version=3"}
    auth = (os.environ['usern'], os.environ['apitoken'])
    url = 'https://api.heroku.com/apps/salana/config-vars'
    requests.patch(url, data=data, headers=headers, auth=auth)

@client.command()
@commands.has_permissions(manage_roles=True)
async def blacklist(ctx, userid:int):
    '''Blacklists a user from automatically joining in the welcome channel. Requires manage roles permissions.'''
    if not await client.get_cog('WELCOME').ifwelcome(ctx):
        return
    if userid in config[str(ctx.guild.id)]['welcome']['blacklist']:
        await ctx.send('Already blacklisted.')
        return
    config[str(ctx.guild.id)]['welcome']['blacklist'].append(userid)
    await ctx.send('Successfully blacklisted.')

@client.command()
@commands.has_permissions(manage_roles=True)
async def unblacklist(ctx, userid:int):
    '''Removes a blacklist entry for the welcome channel. Requires manage roles permissions.'''
    if not await client.get_cog('WELCOME').ifwelcome(ctx):
        return
    if userid not in config[str(ctx.guild.id)]['welcome']['blacklist']:
        await ctx.send('Not in blacklist.')
        return
    config[str(ctx.guild.id)]['welcome']['blacklist'].remove(userid)
    await ctx.send('Removed from blacklist.')

@client.command()
@commands.has_permissions(manage_roles=True)
async def blacklistshow(ctx):
    '''Shows blacklisted users. Requires manage roles permissions.'''
    if not await client.get_cog('WELCOME').ifwelcome(ctx):
        return
    if len(config[str(ctx.guild.id)]['welcome']['blacklist']) == 0:
        await ctx.send('No blacklisted users.')
        return
    emb = discord.Embed(title='Blacklisted users', color=discord.Color.blue())
    for user in config[str(ctx.guild.id)]['welcome']['blacklist']:
        emb.add_field(name=str(user), value=f'<@{user}>')
    await ctx.send(embed=emb)

@client.command()
@commands.is_owner()
async def test(ctx):
    """Don't worry about this one. Bot owner only."""
    await ctx.send('test')

@client.command()
@commands.is_owner()
async def activityupdate(ctx, *, activity):
    """Changes the discord 'playing' status to the specified activity. You must be the bot owner to activate this command."""
    await client.change_presence(activity=discord.Game(activity))
    await ctx.send('Changed successfully.')

@client.command()
@commands.is_owner()
async def omoli(ctx):
    """Kills the bot. (supposedly. with heroku it just starts right back up again.) You must be the bot owner to activate this command."""
    await updateconfig()
    await ctx.send('a! :dizzy_face::skull_crossbones:')
    quit()

@client.command()
@commands.is_owner()
async def guildinfo(ctx, *, guild=None):
    '''Shows which guilds salana is a part of, and which language they are. Also can display info about specific guilds.'''
    if guild == None:
        info = ''
        for i in client.guilds:
            if config[str(i.id)]['tp'] is None:
                info += f'{i.name} - pa mu\n'
            else:
                info += f'{i.name} - toki pona\n'
        await ctx.send(info)
    else:
        g = ''
        info = ''
        for i in client.guilds:
            if i.name == guild:
                g = str(i.id)
                info = f'__{i.name}__\n'
                break
        else:
            await ctx.send('Unknown guild')
            return
        if config[g]['tp'] is None:
            info += 'Language is pa mu\n'
        else:
            info += 'Language is toki pona\n'
            if config[g]['tp']['spchannel'] is not None:
                info += 'sitelen pona channel is active\n'
        if config[g]['hardcore'] is not None:
            info += 'Hardcore is active\n'
        if config[g]['welcome'] is not None:
            info += f'Welcome is active, key is {config[g]["welcome"]["key"]}\n'
            if config[g]['welcome']['second'] is not None:
                info += 'Second welcome is active\n'
        if config[g]['questions'] is not None:
            info += 'Questions are active\n'
        if config[g]['reporting'] is not None:
            info += 'Reporting is active\n'
        if config[g]['logging'] is not None:
            info += 'Logging is active\n'
        await ctx.send(info)

@client.command()
@commands.is_owner()
async def save(ctx):
    """Saves the current config."""
    await updateconfig()
    await ctx.send('Successfully saved data.')

@client.command()
@commands.is_owner()
async def saveandshow(ctx):
    '''Saves the current config and sends it to the channel (USE WITH CAUTION)'''
    try:
        #gets new additions to cog-specific config elements
        questions = client.get_cog('QUESTIONS')
        tokipona = client.get_cog('TOKI PONA')
        fun = client.get_cog('FUN')
        newquestions = questions.newquestions
        newudspcs = tokipona.newudspcs
        newguildhighscores = fun.newguildhighscores
        newpersonalhighscores = fun.newpersonalhighscores

        #updates the main config with all the new stuff
        for i in config:
            if isinstance(config[i], dict):
                if i in newguildhighscores:
                    config[i]['hsu'] = newguildhighscores[i][0]
                    config[i]['hsv'] = newguildhighscores[i][1]
                if i in newquestions:
                    config[i]['questions'] = newquestions[i]
                if i in newudspcs:
                    for j in newudspcs[i]:
                        config[i]['tp']['udspc'][j] = newudspcs[i][j]
        for i in newpersonalhighscores:
            config[i] = newpersonalhighscores[i]
        print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))

        #adds everything that's changed to the data to be readded
        
        data = dict()
        for i in config:
            if i not in os.environ or config[i] != json.loads(os.environ[i]):
                data[i] = json.dumps(config[i])
                await ctx.send(f'{i} updated\n')
        data = json.dumps(data)
        await ctx.send(f'DATA: {data}\n')

        #makes the request
        headers = {"Content-Type": "application/json", "Accept": "application/vnd.heroku+json; version=3"}
        auth = (os.environ['usern'], os.environ['apitoken'])
        url = 'https://api.heroku.com/apps/salana/config-vars'
        requests.patch(url, data=data, headers=headers, auth=auth)
    except Exception as e:
        await ctx.send(e)

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def settaso(ctx):
    '''Adds or removes a toki pona taso channel to the bot's internal library. This means that the bot will try to only speak in toki pona in these channels. Requires manage server permissions.'''
    if config[str(ctx.guild.id)]['tp'] is None:
        await ctx.send('This is only available on a toki pona server.')
        return
    channelid = ctx.channel.id
    if channelid in config[str(ctx.guild.id)]['tp']['tasochannelids']:
        config[str(ctx.guild.id)]['tp']['tasochannelids'].remove(channelid)
        await ctx.send('✅ This channel is no longer a toki pona taso channel.')
    else:
        config[str(ctx.guild.id)]['tp']['tasochannelids'].append(channelid)
        await ctx.send('✅ tomo ni li kama tomo pi toki pona taso.')
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    client.reload_extension('cogs.tokipona')

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def switchlanguage(ctx, confirm=None):
    '''Switches the server's language. Deletes any data regarding toki pona, including tpt channels, sitelen pona channel, default sp colors, etc. Requires manage server permissions.'''
    if confirm == None:
        if config[str(ctx.guild.id)]['tp'] is None:
            await ctx.send('This will switch this server from a pa mu one to a toki pona one. Type `,switchlanguage confirm` to confirm that you want to do this.')
        else:
            await ctx.send('This will switch this server from a toki pona one to a pa mu one. It will delete all data regarding toki pona, including tpt channels, sitelen pona channel, default sp colors, etc. Type `,switchlanguage confirm` to confirm that you want to do this.')
        return
    if confirm != 'confirm':
        await ctx.send('Please type `,switchlanguage confirm` to confirm this.')
        return
    if config[str(ctx.guild.id)]['tp'] is None:
        config[str(ctx.guild.id)]['tp'] = {'udspc': dict(), 'tasochannelids': [], 'spchannel': None}
        await ctx.send('Done! Give me a few seconds to save the data. Once I\'m done, you\'ll be able to use all of the base toki pona features.')
    else:
        config[str(ctx.guild.id)]['tp'] = None
        await ctx.send('Done! Give me a few seconds to save the data. Once I\'m done, you\'ll be able to use all of the pa mu features.')
    await updateconfig()

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def ignore(ctx, ar='add'):
    '''Adds a channel to the bot's list to ignore the hardcore feature in. You can specify to add or remove a channel. Defaults to add. Requires manage server permissions.'''
    hardcore = client.get_cog('HARDCORE')
    if not await hardcore.ifhardcore(ctx):
        await ctx.send('Not in the right context.')
        return
    if ar == 'add':
        config[str(ctx.guild.id)]['hardcore']['channels'].append(ctx.channel.id)
        print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
        await ctx.send('Hardcore will now ignore this channel. Changes should be available shortly.')
    elif ar == 'remove':
        config[str(ctx.guild.id)]['hardcore']['channels'].remove(ctx.channel.id)
        print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
        await ctx.send('Hardcore will no longer ignore this channel. Changes should be available shortly.')
    else:
        await ctx.send('Unknown parameter. Please enter either "add" or "remove".')
        return
    client.reload_extension('cogs.hardcore')
    client.reload_extension('cogs.utilities')

@client.group(name='setup', invoke_without_command=True)
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def setup_command(ctx):
    '''General command to set up or edit different modules. Requires manage server permissions.'''
    info = discord.Embed(title='Setup help', description='Use `,setup <module>` to begin setup for a specified module.\nModules that you can enable:')

    tp = client.get_cog('TOKI PONA')
    spchannel = client.get_cog('SITELEN PONA CHANNEL')
    if not await spchannel.ifspchannel(ctx) and await tp.iftokipona(ctx):
        info.add_field(name='spchannel', value='This will take a channel and automatically convert everything that is sent to it to sitelen pona. Messages can be deleted by the author by reacting to it with 🗑️. Only works in toki pona servers.')
    
    hardcore = client.get_cog('HARDCORE')
    if not await hardcore.ifhardcore(ctx):
        info.add_field(name='hardcore', value='This will detect if people with a certain role are not speaking in toki pona or pa mu. It will then delete their message, unless they\'re in one of a specified list of channels to ignore.')

    welcome = client.get_cog('WELCOME')
    if not await welcome.ifwelcome(ctx):
        info.add_field(name='welcome', value='A module that regulates member entry. A certain message will be sent by the bot to a specific channel. It should be the only message in the channel. Then, if someone sends a message to that channel that is equal to a certain key and they do not have the join role, they are given the join role and all their previous messages in that channel are deleted. An optional feature that can be added is a second welcome, where the newcomer is greeted with a welcome message in a channel of your choice.')

    questions = client.get_cog('QUESTIONS')
    if not await questions.ifquestions(ctx):
        info.add_field(name='questions', value='A module for keeping track of questions that people might have. Useful for busy language servers.')

    reporting = client.get_cog('REPORTING')
    if not await reporting.ifreporting(ctx):
        info.add_field(name='reporting', value='This will detect if a message has a certain number of the triangular flag emoji in its reactions, and will automatically send a copy of that message to a certain channel. It\'s designed to assist with moderation.')

    logging = client.get_cog('LOGGING')
    if not await logging.iflogging(ctx):
        info.add_field(name='logging', value='A simple module for join/leave logging.')

    await ctx.send(embed=info)

@setup_command.command(name='hardcore')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def hardcore_setup(ctx, *, param=None):
    '''Command to setup or edit the hardcore module'''
    if config[str(ctx.guild.id)]['hardcore'] is None:
        config[str(ctx.guild.id)]['hardcore'] = {'role': None, 'channels': []}
        await ctx.send('Initial setup complete. Please repeat the command followed by a mention of the role that will be the hardcore role.')
    elif param is not None and config[str(ctx.guild.id)]['hardcore'] is not None:
        rolementions = ctx.message.raw_role_mentions
        if len(rolementions) > 0:
            config[str(ctx.guild.id)]['hardcore']['role'] = rolementions[0]
            await ctx.send('Successfully added. Changes should be available shortly. You can choose to ignore the hardcore role in certain channels with `,ignore`.')
            print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
            client.reload_extension('cogs.hardcore')
            client.reload_extension('cogs.utilities')
        else:
            await ctx.send('That role was not recognized. Please try again.')
    else:
        await ctx.send('Please enter a role to be the hardcore role.')

@setup_command.command(name='spchannel')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def spchannel_setup(ctx, confirm=None):
    '''Command to setup or edit the sitelen pona channel module'''
    if config[str(ctx.guild.id)]['tp'] is None:
        await ctx.send('This is only available on a toki pona server.')
        return
    if confirm == None:
        await ctx.send('This will turn the current channel into the sitelen pona channel for this server. Make sure you\'re in the right channel and type `,setup spchannel confirm` to confirm.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    webhook = await ctx.channel.create_webhook(name='sitelen pona webhook')
    config[str(ctx.guild.id)]['tp']['spchannel'] = {'webhook_id': webhook.id, 'webhook_token': webhook.token, 'channelid': ctx.channel.id}
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Complete. Changes should be available shortly.')
    client.reload_extension('cogs.spchannel')
    client.reload_extension('cogs.utilities')

@setup_command.command(name='welcome')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def welcome_setup(ctx, key=None, role=None, *, message=None):
    '''Command to setup or edit the primary welcome module'''
    if key is None:
        await ctx.send('This command is used to setup the welcome channel. To use it, first navigate to the channel you wish to set as the welcome channel. Then, follow the command with the single-word entry key, a mention of the join role, and finally the message you want me to send to this channel.')
        return
    if message is None:
        await ctx.send('You\'re missing some of the required arguments. Please try again.')
        return
    rolementions = ctx.message.raw_role_mentions
    if len(rolementions) == 0:
        await ctx.send('Please mention the join role.')
    config[str(ctx.guild.id)]['welcome'] = {'key': key, 'role': rolementions[0], 'channel': ctx.channel.id, 'message': message, 'second': None}
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Successfully configured. Changes should be available shortly. If you\'d also like to set up the optional portion of the welcome module, use `,setup welcome2`')
    client.reload_extension('cogs.welcome')
    client.reload_extension('cogs.utilities')

@setup_command.command(name='welcome2')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def welcome2_setup(ctx, *, message=None):
    '''Command to remove the secondary welcome module'''
    if config[str(ctx.guild.id)]['welcome'] is None:
        await ctx.send('You must set up the main module first.')
        return
    if message == None:
        await ctx.send('This command will set up the current channel as the secondary welcome channel. Please make sure you\'re in the correct channel and follow it with the desired welcome message. If you\'d like to mention the newcomer in this message, insert !MENTION where you would like to mention them.')
        return
    config[str(ctx.guild.id)]['welcome']['second'] = {'channel': ctx.channel.id, 'message': message}
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Successfully configured. Changes should be available shortly.')
    client.reload_extension('cogs.welcome')
    client.reload_extension('cogs.utilities')

@setup_command.command(name='questions')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def questions_setup(ctx):
    '''Command to setup the questions module'''
    if config[str(ctx.guild.id)]['questions'] is not None:
        await ctx.send('This server already uses the question module. To remove it, use `,remove questions`.')
        return
    config[str(ctx.guild.id)]['questions'] = []
    newquestions = client.get_cog('QUESTIONS').newquestions
    for i in config:
        if isinstance(config[i], dict):
            if i in newquestions:
                config[i]['questions'] = newquestions[i]
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Successfully enabled. Changes should be available shortly.')
    client.reload_extension('cogs.questions')
    client.reload_extension('cogs.utilities')

@setup_command.command(name='reporting')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def reporting_setup(ctx, count:int=0):
    '''Command to setup the reporting module'''
    if count == 0:
        await ctx.send('This will set up the reporting feature. The current channel will be used as the channel to which report messages will go, so make sure you\'re in the right channel, repeat the command, and follow it with the number of reactions that are necessary to report a message.')
        return
    if count < 1:
        await ctx.send('Please enter a positive integer.')
        return
    config[str(ctx.guild.id)]['reporting'] = {'channelid': ctx.channel.id, 'count': count}
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Successfully configured. Changes should be available shortly.')
    client.reload_extension('cogs.reporting')
    client.reload_extension('cogs.utilities')

@setup_command.command(name='logging')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def logging_setup(ctx, confirm=None):
    '''Command to set up the join/leave logging module'''
    if config[str(ctx.guild.id)]['logging'] is not None:
        await ctx.send('This server already uses the logging module. To remove it, use `,remove logging`.')
        return
    if confirm == None:
        await ctx.send('This will mark the current channel as the logging channel for this server. Make sure you\'re in the right channel and type `,setup spchannel confirm` to confirm.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['logging'] = ctx.channel.id
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Successfully enabled and set to this channel. Changes should be available shortly.')
    client.reload_extension('cogs.logging')
    client.reload_extension('cogs.utilities')

@client.group(name='remove', invoke_without_command=True)
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def remove_command(ctx):
    '''General command to remove modules. Requires manage server permissions.'''
    info = discord.Embed(title='Remove help', description='Use `,remove <module>` to begin removal for a specified module.\nModules that you have enabled:')

    tp = client.get_cog('TOKI PONA')
    spchannel = client.get_cog('SITELEN PONA CHANNEL')
    if await spchannel.ifspchannel(ctx) and await tp.iftokipona(ctx):
        info.add_field(name='spchannel', value='\u200b')
    
    hardcore = client.get_cog('HARDCORE')
    if await hardcore.ifhardcore(ctx):
        info.add_field(name='hardcore', value='\u200b')

    welcome = client.get_cog('WELCOME')
    if await welcome.ifwelcome(ctx):
        info.add_field(name='welcome', value='\u200b')

    questions = client.get_cog('QUESTIONS')
    if await questions.ifquestions(ctx):
        info.add_field(name='questions', value='\u200b')

    reporting = client.get_cog('REPORTING')
    if await reporting.ifreporting(ctx):
        info.add_field(name='reporting', value='\u200b')

    logging = client.get_cog('LOGGING')
    if await logging.iflogging(ctx):
        info.add_field(name='logging', value='\u200b')

    await ctx.send(embed=info)

@remove_command.command(name='hardcore')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def hardcore_remove(ctx, confirm=None):
    '''Command to remove the hardcore module'''
    if config[str(ctx.guild.id)]['hardcore'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the hardcore module from your server. Please confirm by typing `,remove hardcore confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['hardcore'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.hardcore')
    client.reload_extension('cogs.utilities')

@remove_command.command(name='spchannel')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def spchannel_remove(ctx, confirm=None):
    '''Command to remove the sitelen pona channel module'''
    if config[str(ctx.guild.id)]['tp'] is None or config[str(ctx.guild.id)]['tp']['spchannel'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the sitelen pona channel module from your server. Please confirm by typing `,remove spchannel confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['tp']['spchannel'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.spchannel')
    client.reload_extension('cogs.utilities')

@remove_command.command(name='welcome')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def welcome_remove(ctx, confirm=None):
    '''Command to remove the welcome module'''
    if config[str(ctx.guild.id)]['welcome'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the welcome module from your server. Please confirm by typing `,remove welcome confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['welcome'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.welcome')
    client.reload_extension('cogs.utilities')

@remove_command.command(name='welcome2')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def welcome2_remove(ctx, confirm=None):
    '''Command to remove the secondary hardcore module'''
    if config[str(ctx.guild.id)]['welcome'] is None or config[str(ctx.guild.id)]['welcome']['second'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the secondary welcome module from your server. Please confirm by typing `,remove welcome2 confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['welcome']['second'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.welcome')
    client.reload_extension('cogs.utilities')

@remove_command.command(name='questions')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def questions_remove(ctx, confirm=None):
    '''Command to remove the questions module'''
    if config[str(ctx.guild.id)]['questions'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the questions module from your server. Please confirm by typing `,remove questions confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['questions'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.questions')
    client.reload_extension('cogs.utilities')

@remove_command.command(name='reporting')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def reporting_remove(ctx, confirm=None):
    '''Command to remove the reporting module'''
    if config[str(ctx.guild.id)]['reporting'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the reporting module from your server. Please confirm by typing `,remove reporting confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['reporting'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.reporting')
    client.reload_extension('cogs.utilities')

@remove_command.command(name='logging')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def logging_remove(ctx, confirm=None):
    '''Command to remove the logging module'''
    if config[str(ctx.guild.id)]['logging'] is None:
        await ctx.send('This module is not enabled on this server.')
        return
    if confirm == None:
        await ctx.send('This will remove the logging module from your server. Please confirm by typing `,remove logging confirm`.')
        return
    if confirm != 'confirm':
        await ctx.send('Please use "confirm" to confirm this.')
        return
    config[str(ctx.guild.id)]['logging'] = None
    print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
    await ctx.send('Removed successfully. Changes should be available shortly.')
    client.reload_extension('cogs.logging')
    client.reload_extension('cogs.utilities')

#Error messages
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You\'re missing a required argument: '+str(error.param))
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send('You input too many arguments.')
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.NotOwner):
        await ctx.send('You have to be the owner to excute this command.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the right permissions to execute that command.")
    elif isinstance(error, commands.BotMissingPermissions):
        try:
            await ctx.send('The bot is missing the required permissions to invoke this command: '+str(error.missing_perms))
        except commands.CommandInvokeError:
            await ctx.author.send("An error occurred and I wasn't able to handle it normally. I can't send messages to the channel you entered that command in. Other permissions I'm missing are "+str(error.missing_perms))
    elif isinstance(error, commands.ExtensionError):
        await ctx.send(f'The extension {str(error.name)} raised an exception.')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'That command is on cooldown. Try again in {math.ceil(error.retry_after)} second(s).')
    else:
        await ctx.send(f'An unknown error occurred:\n{error}')

@client.event
async def on_error(event, *args, **kwargs):
    await client.get_user(474349369274007552).send(f'There was an error on {event}:\n{args}\n{kwargs}')

#runs bot
client.run(TOKEN)