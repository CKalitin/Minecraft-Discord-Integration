import discord
from discord.ext import commands
import sys
import os

client = discord.Client()
client = commands.Bot(command_prefix='-')

admin_id = 304272355830530051


@client.event
async def on_ready():
    #await client.change_presence(activity=discord.Game(''))
    print("Ready: Bot")


@client.command(aliases=['load'])
async def Load(ctx, extention):
    if ctx.message.author.id == admin_id:
        client.load_extension(f'cogs.{extention}')
        print(f'Loaded: cogs.{extention}')


@client.command(aliases=['unload', 'unLoad', 'UnLoad'])
async def Unload(ctx, extention):
    if ctx.message.author.id == admin_id:
        client.unload_extension(f'cogs.{extention}')
        print(f'Unloaded: cogs.{extention}')


@client.command(aliases=['reload', 'reLoad', 'ReLoad'])
async def Reload(ctx, extention):
    if ctx.message.author.id == admin_id:
        client.unload_extension(f'cogs.{extention}')
        client.load_extension(f'cogs.{extention}')
        print(f'Reloaded: cogs.{extention}')


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')
    print(f'{round(client.latency * 1000)}ms')


@client.command()
async def kill(ctx):
    await ctx.send(f'Eventually I\'ll be the one Killing you')
    sys.exit()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded: cogs.{filename[:-3]}')

client.run("ODMxOTU0MjQwMDc0NDE2MTc4.YHcvww.xNzdN5Ugzg-RgWgyF6MX1ARqxmw")
