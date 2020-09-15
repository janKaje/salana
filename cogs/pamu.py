import discord
from discord.ext import commands, tasks
import json
import os
import re
from emoji import demojize, emojize
import random
from math import ceil
import asyncio

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(pamu(client))

class pamu(commands.Cog, name='PA MU'):

    '''A module for pa mu servers.'''

    def __init__(self, client):
        self.client = client
        self.pamu_dict = json.loads(open(f'{dir_path}/data/pamu_dict.json').read())

    async def ifpamu(self, ctx):
        if ctx.guild is None:
            return False
        return config[str(ctx.guild.id)]['tp'] is None

    async def pamu_check(self, msg):
        msg= str(msg)
        step1 = re.sub(r'\|\|[^\|]+\|\||\s', '', msg) #removes between spoiler tags and whitespace characters
        step2 = demojize(step1) #textifies emojis
        step3 = re.sub(r':[^ ]+:', '', step2) #deletes emojis
        step4 = re.sub('([mnptksljw][uia])', '', step3) #deletes all possible syllables
        if step4 == '':
            return True
        else:
            return False

    @commands.command(aliases=['check_for_pamu', 'cfpm'])
    async def pamucheck(self, ctx, *, text):
        """Checks if the input text is valid in pa mu or not. It does so by first removing anything behind spoiler bars and any whitespace characters, then removing emojis, and then it runs the text through all possible syllables in pa mu."""
        if not await self.ifpamu(ctx):
            return
        if await self.pamu_check(text):
            await ctx.send("pa mu confirmed. :sleepy:")
        else:
            await ctx.send(":rotating_light: Not pa mu! :rotating_light:")