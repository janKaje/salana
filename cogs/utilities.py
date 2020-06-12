import discord
from discord.ext import commands
import re
from emoji import demojize
import time
from datetime import datetime

mapona_id = 301377942062366741
waliwipamu_id = 654411781929959424
wali_welcomechannel_id = 719681821742465034
mapona_welcomechannel_id = 475392923031044098
wali_surveillance_id = 711341612030099546
mapona_surveillance_id = 596158180275519500
wali_logchannel_id = 654413820995043350
jankaje_id = 474349369274007552

def setup(client):
    client.add_cog(utilities(client))

class utilities(commands.Cog):

    """UTILITIES"""

    def __init__(self, client):
        self.client = client
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def activityupdate(self, ctx, *, activity):
        """Changes the discord 'playing' status to the specified activity"""
        await self.client.change_presence(activity=discord.Game(activity))
        await ctx.send('Changed successfully.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def omoli(self, ctx):
        """Kills the bot. (supposedly, with heroku it just starts right back up again)"""
        await ctx.send('a! :dizzy_face::skull_crossbones:')
        quit()

    @commands.command(aliases=['hc_info'])
    async def hcinfo(self, ctx):
        """Displays the specifics on how toki pona is detected."""
        await ctx.send('Anything behind spoiler bars won\'t count towards the detection process. In addition, any word that is capitalized that still contains only the 14 toki pona letters will pass. Every other word will be examined, and if it doesn\'t match a word in a certain list, it won\'t pass. For more information, or to request a change in the program, please contact me (jan Kaje#3293).')

    #Reporting feature
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.custom_emoji:
            if str(demojize(reaction.emoji)) == ':triangular_flag:' and reaction.count == 2:
                if reaction.message.guild.id == waliwipamu_id:
                    mod_surveillance_channel = self.client.get_channel(wali_surveillance_id)
                elif reaction.message.guild.id == mapona_id:
                    mod_surveillance_channel = self.client.get_channel(mapona_surveillance_id)
                userlist = f''

                msg_to_channel = discord.Embed(color = discord.Color.red())
                msg_to_channel.set_author(name = f'{reaction.message.author.display_name}, AKA {str(reaction.message.author)}', icon_url = reaction.message.author.avatar_url)
                msg_to_channel.add_field(name = 'Message content:', value = reaction.message.content, inline=False)
                msg_to_channel.add_field(name = 'Original', value = f'[Jump]({reaction.message.jump_url})', inline=False)
                async for reporter in reaction.users():
                    if reporter.display_name != reporter.name:
                        userlist += f'{reporter.display_name}, AKA {str(reporter)}\n'
                    else:
                        userlist += f'{str(reporter)}\n'
                msg_to_channel.add_field(name = 'People who originally reported it:', value = userlist, inline=False)

                await mod_surveillance_channel.send(f':warning: New Flagged Message in {reaction.message.channel.mention} :warning:\n', embed=msg_to_channel)
                await reaction.message.channel.send('Message successfully reported.', delete_after=2)

    #Welcome
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == wali_welcomechannel_id and message.author.id != 712086611097157652:
            if re.sub(r'\W', '', message.content) == 'mu':
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

        #elif message.channel.id == mapona_welcomechannel_id and message.author.id != 712086611097157652:
        #    if re.sub(r'\W', '', message.content) == 'toki':
        #        await message.delete()
        #        join_role = message.guild.get_role(475389238494625812)
        #        main_chat = message.guild.get_channel(301377942062366741)
        #        help_channel = message.guild.get_channel(301378960468738050)
        #        if join_role not in message.author.roles:
        #            await message.author.add_roles(join_role)
        #            await main_chat.send(f'Welcome to the server, {message.author.mention}! This is the main chat. You can ask any questions about the language in {help_channel.mention}.')

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def reset(self, ctx):
        """Resets the welcome channel."""
        if ctx.channel.id == wali_welcomechannel_id:
            await ctx.channel.purge()
            await ctx.send(f'Welcome! This is wali wi pa mu, a discord server for the constructed language pa mu. Read the rules in {self.client.get_channel(654413439141150751).mention} and it\'ll tell you what you need to do to gain access to the server.\n\nIf you\'re having trouble, ping `@ju pala` and we\'ll be with you to help as soon as we can.')
        #elif ctx.channel.id == mapona_welcomechannel_id:
        #    await ctx.channel.purge(after=datetime(2020, 6, 12, hour=, minute=))
        #    await ctx.send(f'Welcome! This is ma pona pi toki pona, a discord server for the constructed language toki pona. Read the rules in {self.client.get_channel(589550572051628049).mention} and it\'ll tell you what you need to do to gain access to the server.\n\nIf you\'re having trouble or don\'t know that yet, that\'s totally fine! Just ping `@jan lawa` and `@jan pali` and we\'ll be with you to help as soon as we can.')
        else:
            await ctx.send('Not in the right channel.')

    #Join/leave logging
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

    #Custom Help command
    @commands.command()
    async def help(self, ctx, cmd=None):
        """Displays the help command. If [cmd] is given, displays the long help text for that command."""
        if cmd == None:
            command_msg = discord.Embed(title='Commands', color=discord.Color.blue(), description='Type `,help [command]` for more information.')
            for x in self.client.cogs:
                cog_info = ''
                cog = self.client.get_cog(x)
                for c in cog.walk_commands():
                    if not c.hidden:
                        cog_info += f'***{c.name}***  -  '
                cog_info = re.sub(r'  \-  \Z', '', cog_info)
                command_msg.add_field(name = f'__{cog.__doc__}__', value = cog_info, inline = False)
        
            extra_msg = discord.Embed(title='Features', color=discord.Color.blue())
            if ctx.guild.id == waliwipamu_id:
                muwipamumi = self.client.get_channel(654422747090518036).mention
                hardcore_text = f'If you have the hardcore role, any message you send that is not in pa mu will be deleted. Exceptions are when you preface your message with an asterisk or put the non-pa mu text behind spoiler bars. In addition, any message in {muwipamumi} will be scanned and possibly deleted in the same way.'
            elif ctx.guild.id == mapona_id:
                hardcore_text = f'If you have the hardcore role, any message you send that is not in toki pona will be deleted. Exceptions are when you preface your message with an asterisk or put the non-toki pona text behind spoiler bars.'
            extra_msg.add_field(name='__HARDCORE__', value=hardcore_text, inline = False)
            extra_msg.add_field(name='__REPORTING MESSAGES__', value='Any message that two or more people react to with :triangular_flag_on_post: will have a copy sent to a certain channel. This allows people to flag messages they think are breaking the rules so that mods can easily notice and address the issue.', inline=False)
        
            await ctx.send(embed=command_msg)
            await ctx.send(embed=extra_msg)
            return
        if cmd == 'hidden' and ctx.author.id == jankaje_id:
            command_msg = discord.Embed(title='Commands', color=discord.Color.blue())
            for x in self.client.cogs:
                cog_info = ''
                cog = self.client.get_cog(x)
                for c in cog.walk_commands():
                    if c.hidden:
                        cog_info += f'***{c.name}*** - {c.help}\n'
                if cog_info == '':
                    continue
                command_msg.add_field(name = f'__{cog.__doc__}__', value = cog_info, inline = False)
            await ctx.send(embed=command_msg)
        else:
            comd = ''
            alia = 'Aliases: '
            for x in self.client.cogs:
                cog = self.client.get_cog(x)
                for c in cog.walk_commands():
                    if c.name == cmd or cmd in c.aliases:
                        if not c.hidden:
                            title = f'{c.name}'
                            comd = f'{c.help}'
                            for a in c.aliases:
                                alia += f'{a}, '
                            for b in c.clean_params:
                                title += f' <{b}>'
            if comd == '':
                await ctx.send('That command was not found.')
                return
            helpmsg = discord.Embed(title=title, color=discord.Color.blue(), description=comd)
            if not alia == 'Aliases: ':
                alia = re.sub(r', \Z', '', alia)
                helpmsg.set_footer(text=alia)
            await ctx.send(embed=helpmsg)