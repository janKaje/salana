import discord
from discord.ext import commands
import re
from emoji import demojize

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
        """Kills the bot."""
        await ctx.send('a! :dizzy_face::skull_crossbones:')
        quit()

    @commands.command(aliases=['hc_info'])
    async def hcinfo(self, ctx):
        """Displays the specifics on how toki pona is detected."""
        await ctx.send('Anything behind spoiler bars won\'t count towards the detection process. In addition, any word that is capitalized that still contains only the 14 toki pona letters will pass. Every other word will be examined, and if it doesn\'t match a word in a certain list, it won\'t pass. For more information, or to request a change in the program, please contact me (jan Kaje#3293).')

    #Reporting feature and welcome feature
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.custom_emoji:
            if str(demojize(reaction.emoji)) == ':triangular_flag:' and reaction.count == 2:
                if reaction.message.guild.id == 654411781929959424:
                    mod_surveillance_channel = self.client.get_channel(711341612030099546)
                elif reaction.message.guild.id == 301377942062366741:
                    mod_surveillance_channel = self.client.get_channel(596158180275519500)
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
            if str(demojize(reaction.emoji)) == ':upside-down_face:' and reaction.message.author.id == 712086611097157652:
                if reaction.message.channel.id == 719681821742465034:
                    join_role = reaction.message.guild.get_role(654416341775679518)
                    main_chat = reaction.message.guild.get_channel(654413515301584896)
                    help_channel = reaction.message.guild.get_channel(654414352354508800)
                    if join_role not in user.roles:
                        member = reaction.message.guild.get_member(user.id)
                        try:
                            await member.add_roles(join_role)
                        except Exception as e:
                            await self.client.get_channel(705223622981320706).send(e)
                            return
                        await main_chat.send(f'Welcome to the server, {user.mention}! This is the main chat. You can ask any questions in {help_channel.mention}.')
                        await reaction.message.delete()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 654411781929959424:
            join_channel = self.client.get_channel(719681821742465034)
            rules_channel = self.client.get_channel(654413439141150751)
            await join_channel.send(f'Welcome, {member.mention}! Please read {rules_channel.mention} and react to this message with the emoji at the end to join!\n\nPlease note that if you take too long to react, the bot won\'t recognize the reaction and you\'ll have to ping the ju pala in order to join.')
    
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
            if ctx.guild.id == 654411781929959424:
                muwipamumi = self.client.get_channel(654422747090518036).mention
                hardcore_text = f'If you have the hardcore role, any message you send that is not in pa mu will be deleted. Exceptions are when you preface your message with an asterisk or put the non-pa mu text behind spoiler bars. In addition, any message in {muwipamumi} will be scanned and possibly deleted in the same way.'
            elif ctx.guild.id == 301377942062366741:
                hardcore_text = f'If you have the hardcore role, any message you send that is not in toki pona will be deleted. Exceptions are when you preface your message with an asterisk or put the non-toki pona text behind spoiler bars.'
            extra_msg.add_field(name='__HARDCORE__', value=hardcore_text, inline = False)
            extra_msg.add_field(name='__REPORTING MESSAGES__', value='Any message that two or more people react to with :round_pushpin: will have a copy sent to a certain channel. This allows people to flag messages they think are breaking the rules so that mods can easily notice and address the issue.', inline=False)
        
            cautionmsg = discord.Embed(title='***NOTICE:***', color=discord.Color.red())
            cautionmsg.add_field(name='This bot is still in development.', value='I\'m still developing this bot and have yet to find a permanent home for it. The bot won\'t be active all the time. As such, you shouldn\'t rely on its features until development has slowed considerably and I have a permanent host for it. (If you would like to help me find a host, I would be more than happy.)')

            await ctx.send(embed=command_msg)
            await ctx.send(embed=extra_msg)
            #await ctx.send(embed=cautionmsg)
            return
        if cmd == 'hidden' and ctx.author.id == 474349369274007552:
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