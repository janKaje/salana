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
import requests
from datetime import datetime as dt
    
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

class fun(commands.Cog):

    """FUN"""

    def __init__(self, client):
        self.client = client
        self.headers = {'Accept': 'application/vnd.heroku+json; version=3', 'Content-Type': 'application/json'}
        self.url = 'https://api.heroku.com/apps/salana/config-vars'
    
    #yes I am aware that this is just the Farey series at a number minus 2, but I'm keeping it. I developed this before I knew that the Farey series had been explored, so I'm proud of my accomplishments and don't want to remove this. 
    @commands.command()
    async def aleph(self, ctx, num):
        """Calculates the number of fractions between 0 and 1 with n being the maximum value of the denominator (excluding equivalent fractions).\n\nFor example, if n = 4, the possible fractions are 1/4, 1/3, 1/2, 2/3, and 3/4. The command will output the number of these, which in this case would be 5.\n\nThe maximum allowed value of n is 100000."""
        try:
            num = int(num)
        except ValueError:
            await ctx.send('Please only enter integers.')
            return
        if num > 100000 and ctx.author.id != 474349369274007552:
            await ctx.send('Calculations of n > 100000 (100,000) take a long time and clog the bot. Please enter a smaller value.')
            return
        if num < 1:
            await ctx.send('0 - Fractions with a denominator of 0 don\'t exist and fractions with a negative denominator don\'t fall between 0 and 1.')
            return
        async with ctx.typing():
            c = r(num)
        await ctx.send(c)

    #pr
    @commands.command()
    async def pr(self, ctx, a: int, b: int):
        """Calculates the perlition of two numbers."""
        try:
            a=float(a)
            b=float(b)
            result = math.fsum([a, (a**2/b), -(b**a), (a**b)])
            if isinstance(result, int):
                await ctx.send(f"{result}")
            else:
                await ctx.send(str(Fraction(result).limit_denominator()))
        except ValueError:
            await ctx.send("Please only enter numbers.")
    
    #Just for fun commands
    @commands.command()
    async def ping(self, ctx):
        """A simple ping command. Returns the latency of the bot in milliseconds."""
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=["8ball", '8'])
    async def _8ball(self, ctx):
        """Roll me and I'll decide your fate."""
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
        random.seed(item)
        rate_value = random.randint(0, 10)
        await ctx.send(f"I'd give {item} a {rate_value}/10")

    @commands.command(aliases=['rand'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def random(self, ctx):
        '''Gives a random number. Keeps track of high score.'''
        value = str(random.randint(0, 9))
        while True:
            if random.choice([True, False]):
                value += str(random.randint(0, 9))
            else:
                value = int(value)
                break
        highscore_user = os.environ['rand_highscore_user']
        highscore_value = int(os.environ['rand_highscore_value'])
        if value > highscore_value:
            embed = discord.Embed(color=discord.Color.blurple(), title='Congratulations!! :partying_face:', description='You beat the high score!')
            embed.add_field(name='Old high score:', value=f'{highscore_user} got {highscore_value}')
            embed.add_field(name='New high score:', value=f'{str(ctx.author)} got {value}')
            data = '{"rand_highscore_user": "'+str(ctx.author)+'", "rand_highscore_value": "'+str(value)+'"}'
            requests.patch(self.url, data=data, auth=(os.environ['usern'], os.environ['apitoken']), headers=self.headers)
            await ctx.send(dt.utcnow())
        else:
            embed = discord.Embed(color=discord.Color.lighter_grey(), title='Value:', description=str(value))
            embed.set_footer(text='You did not beat the high score.')
            embed.add_field(name='Current high score:', value=f'{highscore_user} got {highscore_value}')
        await ctx.send(embed=embed)