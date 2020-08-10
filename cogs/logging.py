import discord
from discord.ext import commands, tasks
import json
import os
import time

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(logging(client))

class logging(commands.Cog, name='LOGGING'):

    '''A module for join/leave logging.
       \nTo begin setup, use `,setup logging`. To remove this feature, use `,remove logging`.'''

    def __init__(self, client):
        self.client = client

    async def iflogging(self, ctx):
        if config[str(ctx.guild.id)]['logging'] is None:
            return False
        else:
            return True

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not await self.iflogging(member):
            return
        log_channel = self.client.get_channel(config[str(member.guild.id)]['logging'])
        log_msg = discord.Embed(color = discord.Color.green())
        log_msg.set_author(name = str(member), icon_url = member.avatar_url)
        log_msg.add_field(name = 'Member joined', value = time.strftime('Joined on %A, %d %B %Y, %H:%M:%S UTC', time.gmtime()))
        await log_channel.send(embed=log_msg)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not await self.iflogging(member):
            return
        log_channel = self.client.get_channel(config[str(member.guild.id)]['logging'])
        log_msg = discord.Embed(color = discord.Color.red())
        log_msg.set_author(name = str(member), icon_url = member.avatar_url)
        log_msg.add_field(name = 'Member left', value = time.strftime('Left on %A, %d %B %Y, %H:%M:%S UTC', time.gmtime()))
        await log_channel.send(embed=log_msg)