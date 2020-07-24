import discord
from discord.ext import commands, tasks
import json
import os
import re

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(welcome(client))

class welcome(commands.Cog, name='WELCOME'):

    '''A module that regulates member entry. A certain message will be sent by the bot to a specific channel. It should be the only message in the channel. Then, if someone sends a message to that channel that is equal to a certain key and they do not have the join role, they are given the join role and all their previous messages in that channel are deleted.
       To begin setup, use `,setup welcome`. To remove this feature, use `,remove welcome`.

       There is also a separate module inside this one that will welcome these new members into a certain channel with a certain message.
       To set this up, use `,setup welcome2`. You must have already set up the main module.
       To remove this feature, use `,remove welcome2`.'''

    def __init__(self, client):
        self.client = client

    async def ifwelcome(self, ctx):
        try:
            return config[str(ctx.guild.id)]['welcome'] is not None
        except:
            return False

    async def ifwelcome2(self, ctx):
        try:
            if config[str(ctx.guild.id)]['welcome'] is None:
                return False
        except:
            return False
        return config[str(ctx.guild.id)]['welcome']['second'] is not None

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def reset(self, ctx):
        """Resets the welcome channel. You must have the manage messages permissions to use this command."""
        if not await self.ifwelcome(ctx):
            return
        if ctx.channel.id == config[str(ctx.guild.id)]['welcome']['channel']:
            await ctx.channel.purge()
            await ctx.send(config[str(ctx.guild.id)]['welcome']['message'])
        else:
            await ctx.send('Not in the right channel.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not await self.ifwelcome(message):
            return
        if message.channel.id == config[str(message.guild.id)]['welcome']['channel'] and not message.author.bot:
            #if the message they send is the key, deletes their message(s) and gives them the entry role.
            if re.sub(r'\W', '', message.content).lower() == config[str(message.guild.id)]['welcome']['key'].lower():
                join_role = message.guild.get_role(config[str(message.guild.id)]['welcome']['role'])
                if join_role not in message.author.roles:
                    await message.author.add_roles(join_role)
                    await message.delete()
                    async for i in message.channel.history():
                        if i.author == message.author:
                            await i.delete()
                    #if the second welcome feature is enabled, sends the second welcome.
                    if await self.ifwelcome2(message):
                        welcome2channel = self.client.get_channel(config[str(message.guild.id)]['welcome']['second']['channel'])
                        msg = re.sub('!MENTION', message.author.mention, config[str(message.guild.id)]['welcome']['second']['message'])
                        await welcome2channel.send(msg)