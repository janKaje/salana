import discord
from discord.ext import commands, tasks
import json
import os
import datetime as dt
from copy import deepcopy

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(questions(client))

class questions(commands.Cog, name='QUESTIONS'):

    '''A module for keeping track of questions.
       \nTo begin setup, use `,setup questions`. To remove this feature, use `,remove questions`.'''

    def __init__(self, client):
        self.client = client
        self.newquestions = dict()

    async def ifquestions(self, ctx):
        try:
            return config[str(ctx.guild.id)]['questions'] is not None
        except:
            return False

    async def add_question(self, question, ctx):
        q_info = {'question': question, 'authormention': ctx.author.mention, 'messageurl': ctx.message.jump_url, 'channelmention': ctx.channel.mention, 'messageutc': ctx.message.created_at.isoformat()}
        config[str(ctx.guild.id)]['questions'].append(q_info)
        await ctx.message.add_reaction('\u2705')
        #questions asked over 24 hours ago are deleted
        for i in deepcopy(config[str(ctx.guild.id)]['questions']):
            if dt.datetime.utcnow() - dt.datetime.fromisoformat(i['messageutc']) > dt.timedelta(days=1):
                config[str(ctx.guild.id)]['questions'].remove(i)
        #if the list is too long, deletes the least recent one
        if len(config[str(ctx.guild.id)]['questions']) > 10:
            del config[str(ctx.guild.id)]['questions'][0]

    @commands.command(aliases=['q'])
    async def question(self, ctx, *, question):
        '''A command to register questions. Use `,q <question>` to ask a question. `,q a` will mark your last question as answered. `,q list` will list the currently open questions.'''
        #lists open questions
        if not await self.ifquestions(ctx):
            return
        if question == 'list':
            if len(config[str(ctx.guild.id)]['questions']) == 0:
                await ctx.send('No currently open questions.')
                return
            emb = discord.Embed(color=discord.Color.dark_green(), title='List of open questions:')
            for i in deepcopy(config[str(ctx.guild.id)]['questions']):
                #if question was asked more than a day ago, deletes
                if dt.datetime.utcnow() - dt.datetime.fromisoformat(i['messageutc']) > dt.timedelta(days=1):
                    config[str(ctx.guild.id)]['questions'].remove(i)
                    continue
                #else, adds field
                emb.add_field(name=f'Question #{config[str(ctx.guild.id)]["questions"].index(i)+1}:',
                              value=f'By {i["authormention"]} in {i["channelmention"]}\n'
                                    f'{i["question"]}\n'
                                    f'[Jump URL]({i["messageurl"]})', inline=False)
            await ctx.send(embed=emb)
        elif question == 'a':
            #gets all the questions that the author asked in reverse order
            setwithauthor = list(reversed([i for i in config[str(ctx.guild.id)]['questions'] if i["authormention"] == ctx.author.mention]))
            if setwithauthor != []:
                lastq = setwithauthor[0]
                config[str(ctx.guild.id)]['questions'].remove(lastq)
                await ctx.message.add_reaction('\u2705')
                #deleted successfully
            else:
                await ctx.send('You have no open questions.')
        elif question.startswith('a '):
            try:
                index = int(question[2:])
            #if not followed by an integer, interprets it as a question
            except:
                await self.add_question(question, ctx)
                return
            #if author is not equal to the asker of specified question
            if config[str(ctx.guild.id)]['questions'][(index-1)]["authormention"] != ctx.author.mention:
                await ctx.send('You didn\'t send that question.')
                return
            #else, removes
            config[str(ctx.guild.id)]['questions'].remove(config[str(ctx.guild.id)]['questions'][index-1])
            await ctx.message.add_reaction('\u2705')
        elif question.startswith('delete '):
            try:
                index = int(question[7:])
            #if not followed by an integer, interprets as a question
            except:
                self.add_question(question, ctx)
                return
            #checks for the manage_messages permission in that channel
            if not ctx.channel.permissions_for(ctx.author).manage_messages:
                await ctx.send('You don\'t have the right permissions to delete other\'s questions.')
                return
            #else, removes
            config[str(ctx.guild.id)]['questions'].remove(config[str(ctx.guild.id)]['questions'][index-1])
            await ctx.send('Deleted successfully.')
        else:
            await self.add_question(question, ctx)
        self.newquestions[str(ctx.guild.id)] = config[str(ctx.guild.id)]['questions']