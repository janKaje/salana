import discord
from discord.ext import commands
import math
from fractions import Fraction
import random
import functools
from functools import reduce
from functools import lru_cache
from math import sqrt
    
def setup(client):
    client.add_cog(fun(client))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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
    
    @commands.command()
    async def aleph(self, ctx, num):
        """Calculates the number of fractions between 0 and 1 with n being the maximum value of the denominator (excluding equivalent fractions).\n\nFor example, if n = 4, the possible fractions are 1/4, 1/3, 1/2, 2/3, and 3/4. The command will output the number of these, which in this case would be 5.\n\nThe maximum allowed value of n is 100000."""
        if is_int(num):
            num = int(num)
            if num > 100000 and ctx.author.id != 474349369274007552:
                await ctx.send('Calculations of n > 100000 (100,000) take a long time and clog the bot. Please enter a smaller value.')
                return
            if num < 1:
                await ctx.send('0 - Fractions with a denominator of 0 don\'t exist and fractions with a negative denominator don\'t fall between 0 and 1.')
                return
            async with ctx.typing():
                c = r(num)
            await ctx.send(c)
        else:
            await ctx.send('Please only enter integers.')

    #Sicto's command
    @commands.command(hidden=True)
    async def pr(self, ctx, arg1, arg2):
        """A command that only sictoabu can use. It's complicated."""
        if ctx.author.id != 573295509360476170:
            await ctx.send("Only sictoabu can use this command.")
        elif is_number(arg1) and is_number(arg2):
            a=float(arg1)
            b=float(arg2)
            result=a**3/b-b**a+a**b
            if isinstance(result, int):
                await ctx.send(f"{result}")
            else:
                await ctx.send(str(Fraction(result).limit_denominator()))
        else:
            await ctx.send("Please only enter numbers.")
    
    #Just for fun commands
    @commands.command()
    async def ping(self, ctx):
        """A simple ping command. Returns the latency of the bot in milliseconds."""
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=["8ball"])
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
        rate_value = int(str(hash(item))[2:3])+1
        await ctx.send(f"I'd give {item} a {rate_value}/10")