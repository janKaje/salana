import discord
from discord.ext import commands
import math
from fractions import Fraction
import random
import functools
from functools import reduce
from functools import lru_cache
import re
import os
import json

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = json.loads(open(dir_path+'/config.json').read())
    
def setup(client):
    client.add_cog(fun(client))

#these three are for aleph. if you're interested in exactly how this works, contact me (janKaje) directly.
@lru_cache(maxsize=None)
def factors(n):
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

@lru_cache(maxsize=None)
def a(n):
    fac = factors(n)
    b = 0
    if fac == {1, n}:
        return n-1
    else:
        fac.remove(1)
        fac.remove(n)
        for i in fac:
            b += a(i)
        return n-1-b

@lru_cache(maxsize=None)
def r(n):
    c = 0
    for j in range(2, n+1):
        c += a(j)
    return c

class fun(commands.Cog, name='FUN'):

    """A general fun module. Always on."""

    def __init__(self, client):
        self.client = client
        self.newguildhighscores = dict()
        self.newpersonalhighscores = dict()
    
    #yes I am aware that this is just the Farey series at a number minus 2, but I'm keeping it. I developed this before I knew that the Farey series had been explored, so I'm proud of my accomplishments and don't want to remove this. 
    @commands.command()
    async def aleph(self, ctx, num):
        """Calculates the number of fractions between 0 and 1 with n being the maximum value of the denominator (excluding equivalent fractions).\n\nFor example, if n = 4, the possible fractions are 1/4, 1/3, 1/2, 2/3, and 3/4. The command will output the number of these, which in this case would be 5.\n\nThe maximum allowed value of n is 10000."""
        try:
            num = int(num)
        except ValueError:
            await ctx.send('Please only enter integers.')
            return
        if num > 10000 and ctx.author.id != 474349369274007552:
            await ctx.send('Calculations of n > 10000 (10,000) take a long time and clog the bot. Please enter a smaller value.')
            return
        if num < 1:
            await ctx.send('0 - Fractions with a denominator of 0 don\'t exist and fractions with a negative denominator don\'t fall between 0 and 1.')
            return
        async with ctx.typing():
            c = r(num)
        await ctx.send(c)

    #pr
    @commands.command()
    async def pr(self, ctx, a: float, b: float):
        """Calculates the perlition of two numbers."""
        result = math.fsum([a, (a**2/b), -(b**a), (a**b)])
        if isinstance(result, int):
            await ctx.send(f"{result}")
        else:
            await ctx.send(str(Fraction(result).limit_denominator()))
    
    #Just for fun commands
    @commands.command()
    async def ping(self, ctx):
        """A simple ping command. Returns the latency of the bot in milliseconds."""
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=["8ball", '8'])
    async def eightball(self, ctx):
        """Roll me and I'll decide your fate."""
        if await self.client.get_cog('TOKI PONA').iftokipona(ctx):
            responses = ['ken', 
                'ken a', 
                'mi sona ala.', 
                'sina toki e ni tawa mi tan seme? mi sona ala e sina', 
                'tenpo kama la lon, taso tenpo ni la ala',
                'sona mi la lon. taso mi sona lili. mi ilo taso.',
                'ken??? lukin mi la mi ken ala sona. o toki e ni tawa jan ante, ken la ona li sona.',
                'ala',
                'ala a! ni li ike mute >:(',
                'o pini a, mi wile ala toki tawa sina',
                'ni li ken, taso li ken ala kin',
                'tenpo ale la ni li lon',
                'tenpo ale la ala',
                'ala a',
                'a... lipu mi li sona ala. o lukin lon ma ante, mi a li sona ala',
                'seme? mi kute ike e sina. o toki sin',
                'a.........\n\n.\n\nmsa',
                'mi sona ala e wile sona sina, o moku e kala pona.',
                'tenpo ni la mi sona ala. tenpo suno kama la o toki sin e ni. ken la tenpo ni la mi sona.',
                'lon a!',
                'lon']
        else:
            responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def rate(self, ctx, *, item):
        """I'll rate whatever you tell me to."""
        r = random.getstate()
        random.seed(item)
        rate_value = random.randint(0, 10)
        random.setstate(r)
        await self.client.get_cog('TOKI PONA').safesend(ctx, f"I'd give {item} a {rate_value}/10", f'mi la {item} li {rate_value}/10')

    @commands.command(aliases=['rand', 'r'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def random(self, ctx):
        '''Gives a random number. Keeps track of high score.'''
        value = ''
        choices = [True]
        while True:
            if random.choice(choices):
                value += str(random.randint(0, 9))
                choices.append(False)
            else:
                value = int(value)
                break
        if ctx.guild is not None:
            guild_hsu = str(self.client.get_user(config[str(ctx.guild.id)]['hsu'])) if isinstance(config[str(ctx.guild.id)]['hsu'], int) else config[str(ctx.guild.id)]['hsu']
            guild_hsv = int(config[str(ctx.guild.id)]['hsv'])
        try:
            personal_hsv = config[str(ctx.author.id)]
        except:
            personal_hsv = -1
        if ctx.guild is not None:
            if value > guild_hsv:
                embed = discord.Embed(color=discord.Color.blurple(), title='Congratulations!! :partying_face:', description='You beat the guild high score!')
                embed.add_field(name='Old high score:', value=f'{guild_hsu} got {guild_hsv}')
                embed.add_field(name='New high score:', value=f'{str(ctx.author)} got {value}')
                config[str(ctx.guild.id)]['hsu'] = str(ctx.author)
                config[str(ctx.guild.id)]['hsv'] = value
                self.newguildhighscores[str(ctx.guild.id)] = [ctx.author.id, value]
                await ctx.send(embed=embed)
        if value > personal_hsv:
            embed = discord.Embed(color=discord.Color.blurple(), title='Congratulations!! :partying_face:', description='You beat your personal high score!')
            embed.add_field(name='Old high score:', value=str(personal_hsv))
            embed.add_field(name='New high score:', value=str(value))
            config[str(ctx.author.id)] = value
            self.newpersonalhighscores[str(ctx.author.id)] = value
            await ctx.send(embed=embed)
        elif value <= personal_hsv and (ctx.guild is None or value <= guild_hsv):
            embed = discord.Embed(color=discord.Color.lighter_grey(), title='Value:', description=str(value))
            embed.set_footer(text='You did not beat the high score.')
            try:
                embed.add_field(name='Current guild high score:', value=f'{guild_hsu} got {guild_hsv}')
            except:
                pass
            embed.add_field(name='Current personal high score:', value=str(personal_hsv))
            await ctx.send(embed=embed)