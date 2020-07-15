import discord
from discord.ext import commands
import re
from emoji import demojize
import time
import os
import datetime as dt
import requests

#some variables to help keep track of ids
mapona_id = 301377942062366741
waliwipamu_id = 654411781929959424
wali_welcomechannel_id = 719681821742465034
mapona_welcomechannel_id = 722087129559072788
wali_surveillance_id = 711341612030099546
mapona_surveillance_id = 596158180275519500
wali_logchannel_id = 654413820995043350

def setup(client):
    client.add_cog(utilities(client))

class utilities(commands.Cog):

    """UTILITIES"""

    def __init__(self, client):
        self.client = client
        self.questions = []
        self.headers = {'Accept': 'application/vnd.heroku+json; version=3', 'Content-Type': 'application/json'}
        self.url = 'https://api.heroku.com/apps/salana/config-vars'

    @commands.command(hidden=True)
    @commands.is_owner()
    async def test(self, ctx):
        """Don't worry about this one. Bot owner only."""
        pass

    @commands.command(hidden=True)
    @commands.is_owner()
    async def activityupdate(self, ctx, *, activity):
        """Changes the discord 'playing' status to the specified activity. You must be the bot owner to activate this command."""
        await self.client.change_presence(activity=discord.Game(activity))
        await ctx.send('Changed successfully.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def omoli(self, ctx):
        """Kills the bot. (supposedly. with heroku it just starts right back up again.) You must be the bot owner to activate this command."""
        await ctx.send('a! :dizzy_face::skull_crossbones:')
        quit()

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def reset(self, ctx):
        """Resets the welcome channel. You must have the manage messages permissions to use this command."""
        if ctx.channel.id == wali_welcomechannel_id:
            await ctx.channel.purge()
            await ctx.send(f'Welcome! This is wali wi pa mu, a discord server for the constructed language pa mu. Read the rules in {self.client.get_channel(654413439141150751).mention} and it\'ll tell you what you need to do to gain access to the server.\n\nIf you\'re having trouble, ping `@ju pala` and we\'ll be with you to help as soon as we can.')
        elif ctx.channel.id == mapona_welcomechannel_id:
            await ctx.channel.purge()
            await ctx.send(f':flag_gb: Welcome! This is ma pona pi toki pona, a discord server for the constructed language toki pona. Read the rules in {self.client.get_channel(589550572051628049).mention} and it\'ll tell you what you need to do to gain access to the server.\n\nIf you\'re still having trouble with gaining entry after reading the rules, that\'s totally fine! Just ping `@jan lawa` and `@jan pali` and we\'ll be with you to help as soon as we can.\n\n<:flag_tp:448287759266742272> kama pona a! ni li ma pona pi toki pona. kulupu ni la jan li toki pona li toki e ijo pi toki pona. o lukin e tomo {self.client.get_channel(589550572051628049).mention}. kama lon kulupu ale la o toki e nimi "toki" lon tomo ni.\n\nsina ken ala kama lon kulupu ale la o toki e `@jan lawa` e `@jan pali`.')
        else:
            await ctx.send('Not in the right channel.')

    #Custom Help command
    @commands.command(aliases=['h'])
    async def help(self, ctx, cmd=None):
        """Displays the help command. If <cmd> is given, displays the long help text for that command."""
        #displays all commands if cmd is not given
        if cmd == None:
            command_msg = discord.Embed(title='Commands', color=discord.Color.blue(), description='Type `,help [command]` or `,h [command]` for more information.')
            #iterates through cogs
            for x in self.client.cogs:
                cog_info = ''
                cog = self.client.get_cog(x)
                #iterates through commands of the cog, adding their names to cog_info
                for c in cog.walk_commands():
                    if not c.hidden:
                        cog_info += f'***{c.name}***  -  '
                cog_info = re.sub(r'  \-  \Z', '', cog_info) #trims end off, if there is one
                command_msg.add_field(name = f'__{cog.__doc__}__', value = cog_info, inline = False) #adds cog and commands to embed
        
            #message to explain features
            extra_msg = discord.Embed(title='Features', color=discord.Color.blue())
            if ctx.guild.id == waliwipamu_id:
                muwipamumi = self.client.get_channel(654422747090518036).mention
                hardcore_text = f'If you have the hardcore role, any message you send that is not in pa mu will be deleted. Exceptions are when you preface your message with an asterisk or put the non-pa mu text behind spoiler bars. In addition, any message in {muwipamumi} will be scanned and possibly deleted in the same way.'
            elif ctx.guild.id == mapona_id:
                mentions = f'{self.client.get_channel(301377942062366741).mention}, {self.client.get_channel(375591429608570881).mention}, {self.client.get_channel(340307145373253642).mention}, or {self.client.get_channel(545467374254555137).mention}'
                hardcore_text = f'If you have the hardcore role, any message you send in {mentions} that is not in toki pona will be deleted. Exceptions are when you preface your message with an asterisk. Checks for toki pona the same way that ,ctp does.'
            extra_msg.add_field(name='__HARDCORE__', value=hardcore_text, inline = False)
            extra_msg.add_field(name='__REPORTING MESSAGES__', value='Any message that two or more people react to with :triangular_flag_on_post: will have a copy sent to a certain channel. This allows people to flag messages they think are breaking the rules so that mods can easily notice and address the issue.', inline=False)
            extra_msg.add_field(name='__QUESTION LOGGING__', value='ilo Salana has a way to record and keep track of questions people ask. To log your question, simply type `,q <question>` and it\'ll add it to its log. Type `,q a` to mark your last question as answered.', inline = False)

            await ctx.send(embed=command_msg)
            await ctx.send(embed=extra_msg)
            return
        #if 'hidden' is specified, shows all the hidden ones and their info
        if cmd == 'hidden':
            command_msg = discord.Embed(title='Commands', color=discord.Color.blue())
            #iterates through cogs
            for x in self.client.cogs:
                cog_info = ''
                cog = self.client.get_cog(x)
                #iterates through commands, checking if they're hidden and adding them
                for c in cog.walk_commands():
                    if c.hidden:
                        cog_info += f'***{c.name}*** - {c.help}\n\n'
                #if nothing found, exit this cog and check the next one
                if cog_info == '':
                    continue
                command_msg.add_field(name = f'__{cog.__doc__}__', value = cog_info, inline = False) #add info to embed
            await ctx.send(embed=command_msg)
        #for when a certain command is specified
        else:
            comd = ''
            alia = 'Aliases: '
            #iterates through cogs
            for x in self.client.cogs:
                cog = self.client.get_cog(x)
                #iterates through cog's commands
                for c in cog.walk_commands():
                    if c.name == cmd or cmd in c.aliases: #if search term matches command or any of the aliases
                        if not c.hidden:
                            title = f'{c.name}' #adds name
                            comd = f'{c.help}' #adds help
                            #adds aliases
                            for a in c.aliases:
                                alia += f'{a}, '
                            #adds parameters
                            for b in c.clean_params:
                                title += f' <{b}>'
            #if the command wasn't found
            if comd == '':
                await ctx.send('That command was not found.')
                return
            helpmsg = discord.Embed(title=title, color=discord.Color.blue(), description=comd) #creates embed
            #if the command has aliases, add them to the footer
            if not alia == 'Aliases: ':
                alia = re.sub(r', \Z', '', alia)
                helpmsg.set_footer(text=alia)
            await ctx.send(embed=helpmsg)
    
    #Link to github
    @commands.command()
    async def github(self, ctx):
        '''Links to the github page for this bot.'''
        embed = discord.Embed(color=discord.Color.gold())
        embed.add_field(name='Link to my Github', value=f'[Click Here](https://github.com/janKaje/salana)')
        await ctx.send(embed=embed)

    async def add_question(self, question, ctx):
        q_info = {'question': question, 'author': ctx.author, 'message': ctx.message}
        self.questions.append(q_info)
        await ctx.message.add_reaction('\u2705')
        #questions asked over 24 hours ago are deleted
        for i in self.questions:
            if dt.datetime.utcnow() - i["message"].created_at > dt.timedelta(days=1):
                del i
        #if the list is too long, deletes the least recent one
        if len(self.questions) > 10:
            del self.questions[0]

    #question module
    @commands.command(aliases=['q'])
    async def question(self, ctx, *, question):
        '''A command to register questions. Use `,q <question>` to ask a question. `,q a` will mark your last question as answered. `,q list` will list the currently open questions.'''
        #lists open questions
        if question == 'list':
            if len(self.questions) == 0:
                await ctx.send('No currently open questions.')
                return
            emb = discord.Embed(color=discord.Color.dark_green(), title='List of open questions:')
            for i in self.questions:
                #if question was asked more than a day ago, deletes
                if dt.datetime.utcnow() - i["message"].created_at > dt.timedelta(days=1):
                    del i
                    continue
                #else, adds field
                emb.add_field(name=f'Question #{self.questions.index(i)+1}:',
                              value=f'By {i["author"].mention} in {i["message"].channel.mention}\n'
                                    f'{i["question"]}\n'
                                    f'[Jump URL]({i["message"].jump_url})', inline=False)
            await ctx.send(embed=emb)
        elif question == 'a':
            #gets all the questions that the author asked in reverse order
            setwithauthor = list(reversed([i for i in self.questions if i["author"] == ctx.author]))
            if setwithauthor != []:
                lastq = setwithauthor[0]
                self.questions.remove(lastq)
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
            if self.questions[(index-1)]["author"] != ctx.author:
                await ctx.send('You didn\'t send that question.')
                return
            #else, removes
            self.questions.remove(self.questions[index-1])
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
            self.questions.remove(self.questions[index-1])
            await ctx.send('Deleted successfully.')
        else:
            await self.add_question(question, ctx)

    #Reporting feature
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.custom_emoji: #only goes to the rest of the function if it's a unicode emoji
            if str(demojize(reaction.emoji)) == ':triangular_flag:' and reaction.count == 2: #checks for the right number and type of reactions
                if reaction.message.guild.id == waliwipamu_id:
                    mod_surveillance_channel = self.client.get_channel(wali_surveillance_id)
                elif reaction.message.guild.id == mapona_id:
                    mod_surveillance_channel = self.client.get_channel(mapona_surveillance_id)
                userlist = ''

                #embed creation
                msg_to_channel = discord.Embed(color = discord.Color.red())
                msg_to_channel.set_author(name = f'{reaction.message.author.display_name}, AKA {str(reaction.message.author)}', icon_url = reaction.message.author.avatar_url) #sets author to person who's message is being reported
                msg_to_channel.add_field(name = 'Message content:', value = reaction.message.content, inline=False) #adds copy of message content
                msg_to_channel.add_field(name = 'Original', value = f'[Jump]({reaction.message.jump_url})', inline=False) #adds url to jump to
                #iterates through reporters, adding their names to the embed
                async for reporter in reaction.users():
                    if reporter.display_name != reporter.name:
                        userlist += f'{reporter.display_name}, AKA {str(reporter)}\n'
                    else:
                        userlist += f'{str(reporter)}\n'
                msg_to_channel.add_field(name = 'People who originally reported it:', value = userlist, inline=False)

                #sends embed and tells channel it's been reported
                await mod_surveillance_channel.send(f':warning: New Flagged Message in {reaction.message.channel.mention} :warning:\n', embed=msg_to_channel)
                await reaction.message.channel.send('Message successfully reported.', delete_after=6)

    #Welcome
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == wali_welcomechannel_id and message.author.id != 712086611097157652: #if in the wali wi pa mu welcome channel and the message wasn't sent by the bot
            #if the message they send is the key, deletes their message(s), gives them the entry role, and introduces them.
            if re.sub(r'\W', '', message.content).startswith('mu'):
                await message.delete()
                join_role = message.guild.get_role(654416341775679518)
                main_chat = message.guild.get_channel(654413515301584896)
                help_channel = message.guild.get_channel(654414352354508800)
                if join_role not in message.author.roles:
                    await message.author.add_roles(join_role)
                    await main_chat.send(f'Welcome to the server, {message.author.mention}! This is the main chat. You can ask any questions about the language in {help_channel.mention}.')
                    async for i in message.channel.history():
                        if i.author == message.author:
                            await i.delete()
        elif message.channel.id == mapona_welcomechannel_id and message.author.id != 712086611097157652: #if in the ma pona welcome channel and the message wasn't sent by the bot
            #same as above
            if re.sub(r'\W', '', message.content).lower().startswith('toki'):
                await message.delete()
                join_role = message.guild.get_role(475389238494625812)
                main_chat = message.guild.get_channel(301377942062366741)
                help_channel = message.guild.get_channel(301378960468738050)
                if join_role not in message.author.roles:
                    await message.author.add_roles(join_role)
                    await main_chat.send(f'Welcome to the server, {message.author.mention}! This is the main chat. You can ask any questions about the language in {help_channel.mention}.\n\nkama pona, {message.author.mention} o! ni li tomo pi toki mute. sina wile sona e ijo la o toki e ona lon tomo {help_channel.mention}.')
                    async for i in message.channel.history():
                        if i.author == message.author:
                            await i.delete()

    #Join/leave logging for wali wi pa mu
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == waliwipamu_id:
            log_channel = self.client.get_channel(wali_logchannel_id)
            log_msg = discord.Embed(color = discord.Color.green())
            log_msg.set_author(name = str(member), icon_url = member.avatar_url)
            log_msg.add_field(name = 'Member joined', value = time.strftime('Joined on %A, %d %B %Y, %H:%M:%S UTC', time.gmtime()))
            await log_channel.send(embed=log_msg)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == waliwipamu_id:
            log_channel = self.client.get_channel(wali_logchannel_id)
            log_msg = discord.Embed(color = discord.Color.red())
            log_msg.set_author(name = str(member), icon_url = member.avatar_url)
            log_msg.add_field(name = 'Member left', value = time.strftime('Left on %A, %d %B %Y, %H:%M:%S UTC', time.gmtime()))
            await log_channel.send(embed=log_msg)