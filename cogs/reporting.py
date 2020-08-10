import discord
from discord.ext import commands, tasks
import json
import os
from emoji import demojize

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(reporting(client))

class reporting(commands.Cog, name='REPORTING'):

    '''A module for the report feature. This will detect if a message has a certain number of the triangular flag emoji in its reactions, and will automatically send a copy of that message to a certain channel. It's designed to assist with moderation.
       \nTo begin setup, use `,setup reporting`. To remove this feature, use `,remove reporting`.'''

    def __init__(self, client):
        self.client = client

    async def ifreporting(self, ctx):
        try:
            return config[str(ctx.guild.id)]['reporting'] is not None
        except:
            return False

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not await self.ifreporting(reaction.message):
            return
        if not reaction.custom_emoji: #only goes to the rest of the function if it's a unicode emoji
            if str(reaction.emoji) == '🚩' and reaction.count == config[str(reaction.message.guild.id)]['reporting']['count']: #checks for the right number and type of reactions
                mod_surveillance_channel = self.client.get_channel(config[str(reaction.message.guild.id)]['reporting']['channelid'])
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