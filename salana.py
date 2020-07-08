import discord
from discord.ext import commands, tasks
import os
import time
import math

#Initialize
client = commands.Bot(command_prefix = ',')
client.remove_command('help')
TOKEN = NzEyMDg2NjExMDk3MTU3NjUy.XwUT3g.Y_ChxDIMCe9KN3YYuF7nXm7BLLg

#On_ready command
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('type ,help for help'))

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
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
            await ctx.send("Reloaded successfully.")
        #if extension is already loaded
        except:
            try:
                client.load_extension(f'cogs.{extension}')
                await ctx.send("Reloaded successfully.")
            except:
                #something else happened
                pass
    #if input is 'all', reloads all extensions.
    else:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.unload_extension(f"cogs.{filename[:-3]}")
                client.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send("All extensions reloaded.")

#Automatically loads all cogs in ./cogs on startup
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

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
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('The bot is missing the required permissions to invoke this command: '+str(error.missing_perms))
    elif isinstance(error, commands.ExtensionError):
        await ctx.send(f'The extension {str(error.name)} raised an exception.')
    else:
        await ctx.send(f'ERROR! {error}')

@client.event
async def on_error(event, *args, **kwargs):
    await client.get_user(client.owner_id).send(f'There was an error on {event} in {event.cog}:\n{args}\n{kwargs}')

#runs bot
client.run(TOKEN)