import discord
from discord.ext import commands, tasks
import json
import os
from PIL import Image, ImageDraw, ImageFont
import re

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())

def setup(client):
    client.add_cog(spchannel(client))

class spchannel(commands.Cog, name='SITELEN PONA CHANNEL'):

    '''A module to implement a sitelen pona only channel. This will take a channel and automatically convert everything that is sent to it to sitelen pona. Messages can be deleted by the author by reacting to it with 🗑️. Only works in toki pona servers.
       \nTo begin setup, use `,setup spchannel`. To remove this feature, use `,remove spchannel`.'''

    def __init__(self, client):
        self.client = client

    async def ifspchannel(self, ctx):
        try:
            if config[str(ctx.guild.id)]['tp'] is None:
                return False
        except:
            return False
        return config[str(ctx.guild.id)]['tp']['spchannel'] is not None

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not await self.ifspchannel(msg):
            return
        if msg.channel.id == config[str(msg.guild.id)]['tp']['spchannel']['channelid']:
            if msg.webhook_id == config[str(msg.guild.id)]['tp']['spchannel']['webhook_id']:
                return
            elif msg.author.bot:
                await msg.delete()
                return
            files = []
            for i in msg.attachments:
                r = await i.to_file()
                files.append(r)
            if len(files) > 9:
                try:
                    await msg.author.send('You added too many files to your message. Please try again.')
                except discord.HTTPException:
                    await msg.channel.send(f'{msg.author.mention} o, sina pana e ijo ante pi mute ike lon toki sina. o lili e ona. (mi alasa toki e ni tawa sina taso, taso mi ken ala.)', delete_after=5)
                return
            try:
                await msg.delete()
                text = msg.content
                u_search = re.search('(u=.+)', text, flags=re.DOTALL)
                if u_search:
                    username = f'{u_search.group(0)[2:]} ({msg.author.display_name})'
                    text = re.sub('u=.+', '', text, flags=re.DOTALL)
                else:
                    username = msg.author.display_name
                tokipona = self.client.get_cog('TOKI PONA')
                text, fg, bg, border, fontsize = await tokipona.sitelen_replacements(text, msg.author.id, msg.guild.id)
                #loads font
                font = ImageFont.truetype(font=str(os.path.dirname(os.path.abspath(__file__)))[:-4]+'linja_pona_modified.otf', size=fontsize)
                if re.search(r'[a-zA-Z]', text):
                    try:
                        await msg.author.send('The message you sent could not be converted into sitelen pona. Please try again. Here is the message, in case it was long:')
                        await msg.author.send(msg.content)
                    except discord.HTTPException:
                        await msg.channel.send(f'{msg.author.mention} o, mi ken ala sitelen pona e toki sina. o toki pona taso. (mi alasa toki e ni tawa sina taso, taso mi ken ala.)', delete_after=5)
                    return
                if text != '':
                    size = font.getsize_multiline(text) #calculates size
                    finalsize = (size[0]+2*border, int((size[1]+2*border)*1.1)) #adds border to size
                    if finalsize[0]*finalsize[1] > 1000000:
                        try:
                            await msg.author.send('The message you sent was too big. Please try again. Here is the message, in case it was long:')
                            await msg.author.send(msg.content)
                        except discord.HTTPException:
                            await msg.channel.send(f'{msg.author.mention} o, toki sina li suli ike. o toki lili. (mi alasa toki e ni tawa sina taso, taso mi ken ala.)', delete_after=5)
                        return
                    img = Image.new('RGB', finalsize, color=bg) #new image
                    draw = ImageDraw.Draw(img)
                    draw.text((border, border), text, fill=fg, font=font) #draws text
                    img.save(str(msg.author.id)+'.png') #saves image
                    files.insert(0, discord.File(open(str(msg.author.id)+'.png', 'rb')))
                avatar = msg.author.avatar_url
                webhook = discord.Webhook.partial(str(config[str(msg.guild.id)]['tp']['spchannel']['webhook_id']), config[str(msg.guild.id)]['tp']['spchannel']['webhook_token'], adapter=discord.RequestsWebhookAdapter())
                webhook.send(files=files, avatar_url=avatar, username=username)
                if text != '':
                    os.remove(str(msg.author.id)+'.png') #deletes image
            except Exception as e:
                try:
                    await msg.author.send(f'There was an error with the message I tried to convert: {e}')
                except Exception as f:
                    await self.client.get_user(474349369274007552).send(f'There was an error sending an error to the user: {e}\n{f}\nMessage: {msg.content}\nAuthor: {str(msg.author)}')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not await self.ifspchannel(reaction.message):
            return
        if str(reaction.emoji) == '🗑️':
            for i in reaction.message.attachments:
                if i.filename.startswith(str(user.id)):
                    await reaction.message.delete()
                    return