import discord
from discord.ext import commands, tasks
import json
import os
import re

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(hardcore(client))

class hardcore(commands.Cog, name='HARDCORE'):

    '''A module for the hardcore feature. This will detect if people with a certain role are not speaking in toki pona or pa mu. It will then delete their message, unless they're in one of a specified list of channels to ignore.
       \nTo begin setup, please use `,setup hardcore`. To remove this feature, use `,remove hardcore`.'''

    def __init__(self, client):
        self.client = client

    async def ifhardcore(self, ctx):
        try:
            return config[str(ctx.guild.id)]['hardcore'] is not None
        except:
            return False

    @commands.command()
    async def hc(self, ctx):
        """Gives/takes the hardcore role. See `,help modules` for more info."""
        if not await self.ifhardcore(ctx):
            return
        role = ctx.guild.get_role(config[str(ctx.guild.id)]['hardcore']['role'])
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send("Hardcore role removed.")
        else:
            await ctx.author.add_roles(role)
            await ctx.send("Hardcore role given.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not await self.ifhardcore(msg.channel):
            return
        if msg.author.bot:
            return
        if msg.channel.id not in config[str(msg.guild.id)]['hardcore']['channels']:
            if msg.guild.get_role(config[str(msg.guild.id)]['hardcore']['role']) in msg.author.roles:
                if config[str(msg.guild.id)]['tp'] is not None:
                    tokipona = self.client.get_cog('TOKI PONA')
                    delete = any(msg.content.startswith(i) for i in ['*', ',', 't!', 'x/', '=', ';;', 'pk;', '.', '-']) or await tokipona.tp_check(msg.content)
                else:
                    pamu = self.client.get_cog('PA MU')
                    delete = any(msg.content.startswith(i) for i in ['*', ',', 't!', 'x/', '=', ';;', 'pk;', '.', '-']) or await pamu.pamu_check(msg.content)
                if not delete:
                    if len(msg.content) > 15:
                        try:
                            await msg.author.send('I may have deleted a message of yours that was long:')
                            await msg.author.send(msg.content)
                        except discord.HTTPException:
                            pass
                    await msg.delete()
