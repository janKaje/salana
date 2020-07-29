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
    except Exception as e:
        print(f'An error: {e}')

print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
'''
print(os.environ['config'], file=open(dir_path+'/config.json', mode='w'))
config = json.loads(open(dir_path+'/config.json').read())'''

TOKEN = os.environ['TOKEN']
config2 = config

#On_ready command
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('type ,help for help'))
    await client.get_user(474349369274007552).send(f'Ready on {dt.utcnow()}')

#function to handle updating of config
async def updateconfig():
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
    global config2
    data = dict()
    for i in config:
        if i not in config2 or config[i] != config2[i]:
            data[i] = config[i]
    data = json.dumps(data)

    #makes the request
    headers = {"Content-Type": "application/json", "Accept": "application/vnd.heroku+json; version=3"}
    auth = (os.environ['usern'], os.environ['apitoken'])
    url = 'https://api.heroku.com/apps/salana/config-vars'
    requests.patch(url, data=data, headers=headers, auth=auth)

    #updates the config2 that keeps track of what's changed
    config2 = config

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
    config[str(guild.id)] = {'hsu': 'nobody', 'hsv': -1, 'tp': None, 'hardcore': None, 'welcome': None, 'questions': None, 'reporting': None, 'logging': None}
    
    #sends first message and asks if it should use pa mu or tp
    channel = guild.text_channels[0]
    embed = discord.Embed(title='Hello!', description="I'm salana, a discord bot developed to add toki pona or pa mu features to your server. To begin, select whether this guild is\n1️⃣ a toki pona server, or\n2️⃣ a pa mu server.\nThis is irreversible, so please choose wisely. If you enter the wrong one, kick the bot and invite it again.", color=discord.Color.blue())
    msg = await channel.send(embed=embed)
    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')

    #all this is to see the reaction and parse it
    def check(reaction, user):
        nonlocal channel, msg
        return channel.permissions_for(user).manage_guild and reaction.message.id == msg.id and str(reaction.emoji) in '1️⃣2️⃣'

    reaction, _ = await client.wait_for('reaction_add', check=check)
    
    if str(reaction.emoji) == '1️⃣':
        config[str(guild.id)]['tp'] = {'udspc': dict(), 'tasochannelids': [], 'spchannel': None}
        await channel.send("Congrats! You can now use all of the base toki pona features. I have many more modules than this. If you'd like to see them, use `,server`. To see more information about a module, or to learn how to enable it, use `,help <module>`. To set channels in which I will try to only speak in toki pona, use the command `,settaso` in those channels.")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.{filename[:-3]}")
    elif str(reaction.emoji) == '2️⃣':
        await channel.send("Congrats! You can now use all of the pa mu features. I have many more modules than this. If you'd like to see them, use `,server`. To see more information about a module, or to learn how to enable it, use `,help <module>`.")

@client.event
async def on_guild_remove(guild):
    del config[str(guild.id)]
    data = {str(guild.id): None}
    headers = {"Content-Type": "application/json", "Accept": "application/vnd.heroku+json; version=3"}
    auth = (os.environ['usern'], os.environ['apitoken'])
    url = 'https://api.heroku.com/apps/salana/config-vars'
    requests.patch(url, data=data, headers=headers, auth=auth)

@client.command()
@commands.is_owner()
async def test(ctx):
    """Don't worry about this one. Bot owner only."""
    await ctx.send(config[str(ctx.guild.id)])

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
        await ctx.send(newpersonalhighscores)

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
        global config2
        data = dict()
        for i in config:
            if i not in config2 or config[i] != config2[i]:
                data[i] = config[i]
        data = json.dumps(data)
        await ctx.send(data)

        #makes the request
        headers = {"Content-Type": "application/json", "Accept": "application/vnd.heroku+json; version=3"}
        auth = (os.environ['usern'], os.environ['apitoken'])
        url = 'https://api.heroku.com/apps/salana/config-vars'
        requests.patch(url, data=data, headers=headers, auth=auth)

        #updates the config2 that keeps track of what's changed
        config2 = config
        await ctx.send(json.dumps(config))
    except Exception as e:
        await ctx.send(e)

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def settaso(ctx):
    '''Adds a toki pona taso channel to the bot's internal library.'''
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

@client.group(name='setup', invoke_without_command=True)
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def setup_command(ctx):
    '''General command to set up or edit different modules. For more information, see `,server` or `,help <module>`.'''
    await ctx.send('You entered an unknown subcommand or didn\'t enter one at all. Please try again.')

@setup_command.command(name='hardcore')
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def hardcore_setup(ctx, *, param=None):
    '''Command to setup or edit the hardcore module'''
    if ctx.guild is None:
        return
    if config[str(ctx.guild.id)]['hardcore'] is None and param is None:
        config[str(ctx.guild.id)]['hardcore'] = {'role': None, 'channels': []}
        await ctx.send('Initial setup complete. Please repeat the command followed by the role that will be the hardcore role.')
    elif param is not None:
        rolementions = ctx.message.raw_role_mentions
        if len(rolementions) > 0:
            config[str(ctx.guild.id)]['hardcore']['role'] = rolementions[0]
            await ctx.send('Successfully added. Now type `,setup hardcore` in any channel that you would like to add to the list of channels in which this will be enforced.')
        else:
            await ctx.send('That role was not recognized. Please try again.')
    else:
        config[str(ctx.guild.id)]['hardcore']['channels'].append(ctx.channel.id)
        print(json.dumps(config), file=open(dir_path+'/config.json', mode='w'))
        await ctx.send('Hardcore channel added. Changes should be available shortly.')
        client.reload_extension('cogs.hardcore')
        client.reload_extension('cogs.utilities')

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
    await ctx.send('Successfully configured. Changes should be available shortly.')
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
    '''General command to remove modules.'''
    await ctx.send("You either didn't enter a subcommand or entered an invalid one. Please try again.")

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
        await ctx.send('The bot is missing the required permissions to invoke this command: '+str(error.missing_perms))
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