import discord
from discord.ext import commands
import re
from emoji import demojize
import time
import os
import datetime as dt
import json
import asyncio
from math import ceil

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(utilities(client))

class utilities(commands.Cog, name="UTILITIES"):

    """A general utility module. Always on."""

    def __init__(self, client):
        self.client = client

    #Custom Help command
    @commands.command(aliases=['h'])
    async def help(self, ctx, *, cmd=None):
        """Displays the help command. `<cmd>` can be the name of a command or category, and if given, displays the long help text for that command or category. If `<cmd>` is 'commands' or not specified, lists the commands. If `<cmd>` is 'modules', lists the modules available on the current server and info about them."""
        #displays all commands if cmd is not given
        if cmd == None or cmd == 'commands':
            command_msg = discord.Embed(title='Commands', color=discord.Color.blue(), description='Type `,help [command]` or `,help [category]` for more information. Also available is `,help modules`, which lists the modules available for this server and details about them.')

            cmds = []
            async def addcommands(cog, add=[]):
                nonlocal command_msg, cmds
                cog_info = ''
                for i in cog.walk_commands():
                    checks = True
                    for j in i.checks:
                        try:
                            try:
                                await j(ctx)
                            except commands.CheckFailure:
                                checks = False
                        except:
                            try:
                                j(ctx)
                            except commands.CheckFailure:
                                checks = False
                    if checks:
                        cog_info += f'***{i.name}***  -  '
                        cmds.append(i.name)
                for cmd in add:
                    i = self.client.get_command(cmd)
                    checks = True
                    for j in i.checks:
                        try:
                            try:
                                await j(ctx)
                            except commands.CheckFailure:
                                checks = False
                        except:
                            try:
                                j(ctx)
                            except commands.CheckFailure:
                                checks = False
                    if checks:
                        cog_info += f'***{i.name}***  -  '
                        cmds.append(i.name)
                if cog_info != '':
                    command_msg.add_field(name = f'__{cog.qualified_name}__', value = re.sub(r'  \-  \Z', '', cog_info), inline = False)

            await addcommands(self.client.get_cog('UTILITIES'), add=['setup', 'remove', 'switchlanguage'])
            await addcommands(self.client.get_cog('FUN'))

            tp = self.client.get_cog('TOKI PONA')
            if await tp.iftokipona(ctx):
                await addcommands(tp, add=['settaso'])

            pamu = self.client.get_cog('PA MU')
            if await pamu.ifpamu(ctx):
                await addcommands(pamu)

            hc = self.client.get_cog('HARDCORE')
            if await hc.ifhardcore(ctx):
                await addcommands(hc, add=['ignore'])

            w = self.client.get_cog('WELCOME')
            if await w.ifwelcome(ctx):
                await addcommands(w, add=['blacklist', 'unblacklist', 'blacklistshow'])

            q = self.client.get_cog('QUESTIONS')
            if await q.ifquestions(ctx):
                await addcommands(q)

            if await self.client.is_owner(ctx.author):
                info = ''
                for command in self.client.commands:
                    if command.name not in cmds:
                        checks = True
                        for j in command.checks:
                            try:
                                try:
                                    await j(ctx)
                                except commands.CheckFailure:
                                    checks = False
                            except:
                                try:
                                    j(ctx)
                                except commands.CheckFailure:
                                    checks = False
                        if checks:
                            info += f'***{command.name}***  -  '
                            cmds.append(command.name)
                if info != '':
                    command_msg.add_field(name = '__OWNER ONLY__', value = re.sub(r'  \-  \Z', '', info), inline = False)

            await ctx.send(embed=command_msg)

        elif cmd == 'modules':
            #message to explain features
            extra_msg = discord.Embed(title='Modules', color=discord.Color.blue())

            spchannel = self.client.get_cog('SITELEN PONA CHANNEL')
            if await spchannel.ifspchannel(ctx):
                channelmention = self.client.get_channel(config[str(ctx.guild.id)]['tp']['spchannel']['channelid']).mention
                extra_msg.add_field(name='__SITELEN PONA CHANNEL__', value=f'Any message you send in {channelmention} will be turned into sitelen pona. For those of you who use Pluralkit, you can insert `u=` into your message and whatever comes after will be the display name used when the bot replaces your message. If you\'d like to delete your message, react to it with 🗑️.')

            hardcore = self.client.get_cog('HARDCORE')
            if await hardcore.ifhardcore(ctx):
                if config[str(ctx.guild.id)]['tp'] is None:
                    pamu_or_tp = 'pa mu'
                else:
                    pamu_or_tp = 'toki pona'
                role = ctx.guild.get_role(config[str(ctx.guild.id)]['hardcore']['role']).name
                if len(config[str(ctx.guild.id)]['hardcore']['channels']) == 1:
                    mentions = self.client.get_channel(config[str(ctx.guild.id)]['hardcore']['channels'][0]).mention
                elif len(config[str(ctx.guild.id)]['hardcore']['channels']) == 2:
                    mentions = f"{self.client.get_channel(config[str(ctx.guild.id)]['hardcore']['channels'][0]).mention} or "
                    mentions += self.client.get_channel(config[str(ctx.guild.id)]['hardcore']['channels'][1]).mention
                else:
                    mentions = ''
                    for i in config[str(ctx.guild.id)]['hardcore']['channels']:
                        channel = self.client.get_channel(i).mention
                        if config[str(ctx.guild.id)]['hardcore']['channels'].index(i) == len(config[str(ctx.guild.id)]['hardcore']['channels'])-1:
                            mentions += f'or {channel}'
                        else:
                            mentions += f'{channel}, '
                hardcore_text = f'If you have the `{role}` role, any message that you send (unless it\'s in in {mentions}) that is not in {pamu_or_tp} will be deleted. The bot checks for {pamu_or_tp} using the same method as the check command.'
                extra_msg.add_field(name='__HARDCORE__', value=hardcore_text, inline = False)

            welcome = self.client.get_cog('WELCOME')
            if await welcome.ifwelcome(ctx):
                value = 'When someone joins the server, they will be asked to type a certain key before they get in. The moderators decide what the key is.'
                if await welcome.ifwelcome2(ctx):
                    value += '\n\nOnce someone joins by using the key, the bot will send an automated message to a certain channel, welcoming them into the server.'
                extra_msg.add_field(name='__WELCOME__', value=value, inline=False)

            questions = self.client.get_cog('QUESTIONS')
            if await questions.ifquestions(ctx):
                extra_msg.add_field(name='__QUESTIONS__', value='The bot has a way to record and keep track of questions people ask. To log your question, simply type `,q <question>` and it\'ll add it to its log. Type `,q a` to mark your last question as answered. For more info, use `,help q`.', inline=False)

            reporting = self.client.get_cog('REPORTING')
            if await reporting.ifreporting(ctx):
                count = config[str(ctx.guild.id)]['reporting']['count']
                extra_msg.add_field(name='__REPORTING MESSAGES__', value=f'Any message that {count} or more people react to with :triangular_flag_on_post: will have a copy sent to a certain channel. This allows people to flag messages they think are breaking the rules so that mods can easily notice and address the issue.', inline=False)

            logging = self.client.get_cog('LOGGING')
            if await logging.iflogging(ctx):
                extra_msg.add_field(name='__LOGGING__', value='Basic join/leave logging.', inline=False)

            await ctx.send(embed=extra_msg)
        #for when a certain command or cog is specified
        else:
            for i in self.client.cogs:
                if cmd.upper() == i:
                    embed = discord.Embed(title=i, color=discord.Color.blue(), description=self.client.get_cog(i).__doc__)
                    await ctx.send(embed=embed)
                    return
            comd = ''
            alia = 'Aliases: '
            #iterates through commands
            for c in self.client.walk_commands():
                if c.name == cmd or cmd in c.aliases: #if search term matches command or any of the aliases
                    title = c.name #adds name
                    comd = c.help #adds help
                    #adds aliases
                    for a in c.aliases:
                        alia += f'{a}, '
                    #adds parameters
                    for b in c.clean_params:
                        title += f' <{b}>'
                    break
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
        '''Links to the github repository for this bot.'''
        embed = discord.Embed(color=discord.Color.gold())
        embed.add_field(name='Link to my Github', value=f'[Click Here](https://github.com/janKaje/salana)')
        await ctx.send(embed=embed)

    @commands.command(aliases=['d', 'dict', 'define'])
    async def dictionary(self, ctx, *words):
        '''Finds the definition of a certain word.'''
        tokipona = self.client.get_cog('TOKI PONA')
        pamu = self.client.get_cog('PA MU')
        if len(words) == 0:
            await tokipona.safesend(ctx, 'You need to input at least one word.', 'o toki e nimi a.')
            return
        if len(words) > 10:
            await tokipona.safesend(ctx, 'You input too many words.', 'mute nimi pi toki sina li ike.')
            return
        if await pamu.ifpamu(ctx):
            for i in words:
                try:
                    await ctx.send(pamu.pamu_dict[i])
                except KeyError:
                    await ctx.send(f'{i} is not a word in my dictionary.')
        elif await tokipona.iftokipona(ctx):
            if ctx.channel.id in config[str(ctx.guild.id)]['tp']['tasochannelids']:
                for i in words:
                    if i in tokipona.tpt_dict:
                        await ctx.send(tokipona.tpt_dict[i])
                    elif i in tokipona.tp_dict:
                        await ctx.send(f'toki pona la mi sona ala e kon pi nimi ni. ni li kon ona pi toki Inli:\n||{tokipona.tp_dict[i]}||')
                    else:
                        await ctx.send(f'mi sona ala e nimi "{i}".')
                return
            for i in words:
                try:
                    await ctx.send(tokipona.tp_dict[i])
                except KeyError:
                    await ctx.send(f'{i} is not a word in my dictionary.')

    @commands.command(aliases=['find', 'f'])
    async def search(self, ctx, *, term):
        '''Searches through the dictionary for the given term.'''
        tokipona = self.client.get_cog('TOKI PONA')
        pamu = self.client.get_cog('PA MU')
        if await tokipona.iftokipona(ctx):
            searchdict = tokipona.tp_dict
        elif await pamu.ifpamu(ctx):
            searchdict = pamu.pamu_dict
        else:
            await ctx.send("You can't use that here.")
            return
        found = dict() #new dictionary for found items
        #searches for matches and adds them to found
        for k, v in searchdict.items():
            if re.search(term, v, flags=re.I):
                found[k] = v
        if len(found) == 0:
            await tokipona.safesend(ctx, 'No results found.', 'mi ken ala lukin e nimi ni.')
            return
        #if it's short enough, does it in one message
        if len(found) < 6:
            embed = discord.Embed(title=f'{len(found)} result(s) found', color=discord.Color.teal())
            for i in found:
                if await tokipona.iftokipona(ctx):
                    embed.add_field(name=i, value=found[i][(len(i)+9):], inline=False)
                else:
                    value = re.sub(f'{i}: ?\n?', '', found[i])
                    embed.add_field(name=i, value=value, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{len(found)} result(s) found', description='Displaying results 1-5', color=discord.Color.teal())
            foundtouse = dict(list(found.items())[:5])
            for i in foundtouse:
                if await tokipona.iftokipona(ctx):
                    embed.add_field(name=i, value=found[i][(len(i)+9):], inline=False)
                else:
                    value = re.sub(f'{i}: ?\n?', '', found[i])
                    embed.add_field(name=i, value=value, inline=False)
            page = 1

            messagesent = await ctx.send(embed=embed)
            await messagesent.add_reaction('⬅')
            await messagesent.add_reaction('➡')

            def checkright(reaction, user):
                nonlocal messagesent, ctx
                return str(reaction.emoji) == '➡' and user.id == ctx.author.id and reaction.message.id == messagesent.id

            def checkleft(reaction, user):
                nonlocal messagesent, ctx
                return str(reaction.emoji) == '⬅' and user.id == ctx.author.id and reaction.message.id == messagesent.id
            
            async def update(fb):
                nonlocal page, messagesent, found, tokipona
                page += fb
                #if reached the end or beginning, end the function
                if page == 0:
                    page = 1
                    return
                if page > ceil(len(found)/5):
                    page -= 1
                    return
                #sets range for embed to display
                front = page*5-4
                back = page*5 if page*5 <= len(found) else len(found)
                embed = discord.Embed(title=f'{len(found)} result(s) found', description=f'Displaying results {front}-{back}', color=discord.Color.teal())
                #makes dictionary just for range to use in embed
                foundtouse = dict(list(found.items())[(front-1):back])
                #adds appropriate message to embed
                for i in foundtouse:
                    if await tokipona.iftokipona(ctx):
                        embed.add_field(name=i, value=found[i][(len(i)+9):], inline=False)
                    else:
                        value = re.sub(f'{i}: ?\n?', '', found[i])
                        embed.add_field(name=i, value=value, inline=False)
                await messagesent.edit(embed=embed)

            asyncio.sleep(0.5)
            while True:
                right_add = asyncio.create_task(self.client.wait_for('reaction_add', check=checkright))
                left_add = asyncio.create_task(self.client.wait_for('reaction_add', check=checkleft))
                right_remove = asyncio.create_task(self.client.wait_for('reaction_remove', check=checkright))
                left_remove = asyncio.create_task(self.client.wait_for('reaction_remove', check=checkleft))

                done, pending = await asyncio.wait([right_add, left_add, right_remove, left_remove], timeout=60.0, return_when=asyncio.FIRST_COMPLETED)
                
                for i in pending:
                    i.cancel()

                if right_add in done or right_remove in done:
                    await update(1)
                elif left_add in done or left_remove in done:
                    await update(-1)
                else:
                    break

            await messagesent.clear_reactions()