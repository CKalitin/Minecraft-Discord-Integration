import asyncio
import discord
from discord.ext import commands
from discord import embeds
from discord import colour
import asyncio
import csv

# Channel ID in discord to write to
channel = 846165990622494750

# Path to text file with data
file_path = ''

class ServerChat(commands.Cog):
    def __init__(self, client):
        self.client = client

    # When bot is ready print "Ready" and call starting functions
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready: Server Chat")


def setup(client):
    client.add_cog(ServerChat(client))
