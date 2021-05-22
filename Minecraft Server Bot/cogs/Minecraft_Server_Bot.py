import asyncio
import discord
from discord.ext import commands
from discord import embeds
from discord import colour
import asyncio
import csv

import time

# Channel ID in discord to write to
channel = 832688833375109151

# Path to text file with data
file_path = 'Minecraft Server Bot/'

# The embed that the bot created
embed = embeds.Embed(
            title="CEJA Server Info",
            colour=colour.Color(0x004A19),
        )
# The message that has the embed
embed_message = None
# Seconds between data updates
update_time = 3

# Server vars
server_name = ""
max_players = 0
players_online = 0
players = []

class MinecraftServerBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    # When bot is ready print "Ready" and call starting functions
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready: Server Text")
        await self.setup_embed()
        await self.update()


    # Update is called every (update_time) and it reads new dat and updates the embed
    async def update(self):
        await self.update_embed()

        await asyncio.sleep(update_time)

        await self.update_data()
        await self.update()


    # Send embed with starting text
    async def setup_embed(self):
        global embed
        global embed_message

        embed.set_thumbnail(
            url="https://pbs.twimg.com/profile_images/1169125587157340160/qtOBELUS_400x400.jpg"
        )

        #embed.set_author(name="CEJA Server Bot")

        embed.set_footer(
            text=f"Developed by CaptnCAK."
        )

        embed_message = await self.client.get_channel(channel).send(embed=embed)



    # Update embed text
    async def update_embed(self):
        global embed

        description = f"""
        Players Online ({players_online} / {max_players}):
        """
        for player in players:
            description += f"{player}, "
        description = description[:-2]

        embed.description = description
        embed.title = server_name

        await embed_message.edit(embed=embed)


    # Read data from file
    async def update_data(self):
        global server_name
        global max_players
        global players_online
        global players

        # Open server_data.txt file
        with open(f'{file_path}server_data.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',') # Get data in CSV format
            line_count = 0 # index of for loop

            # Loop through all rows in CSV
            for row in csv_reader:
                if line_count == 0:
                    server_name = row[0]
                elif line_count == 1:
                    max_players = int(row[0])
                elif line_count == 2:
                    players = row
                    players_online = len(players)
                
                line_count += 1



def setup(client):
    client.add_cog(MinecraftServerBot(client))
