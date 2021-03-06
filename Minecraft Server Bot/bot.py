import discord
from discord.ext import commands
import sys
import os

client = discord.Client()
# Chaning activity is done here instead of in on_ready because someone said on stack overflow to never do it in on_ready and they sounded very convincing
client = commands.Bot(command_prefix='-', activity = discord.Game('with ur mom'))

discord_bot_path = "Minecraft Server Bot/"


@client.event
async def on_ready():
    print("Ready: Bot")


@client.command(aliases=['load'])
async def Load(ctx, extention):
    client.load_extension(f'cogs.{extention}')
    print(f'Loaded: cogs.{extention}')


@client.command(aliases=['unload', 'unLoad', 'UnLoad'])
async def Unload(ctx, extention):
    client.unload_extension(f'cogs.{extention}')
    print(f'Unloaded: cogs.{extention}')


@client.command(aliases=['reload', 'reLoad', 'ReLoad'])
async def Reload(ctx, extention):
    client.unload_extension(f'cogs.{extention}')
    client.load_extension(f'cogs.{extention}')
    
    print(f'Reloaded: cogs.{extention}')


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')
    print(f'{round(client.latency * 1000)}ms')


for filename in os.listdir(f"{discord_bot_path}cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded: cogs.{filename[:-3]}')

token_file = open(f"{discord_bot_path}Token", "r")
client.run(token_file.read())
token_file.close()
