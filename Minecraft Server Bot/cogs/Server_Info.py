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
server_name = "CEJA Server"
max_players = 0
players_online = 0
players = []

class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    # When bot is ready print "Ready" and call starting functions
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready: Server Info")

        await self.setup_embed()

        await self.get_starting_data()
        await self.update_data()
        await self.update_embed()

        await self.update()


    # Update is called every (update_time) and it reads new dat and updates the embed
    async def update(self):
        while True:
            await asyncio.sleep(update_time)
            await self.update_embed()
            await self.update_data()


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
        description = description[:-5]

        embed.description = description

        await embed_message.edit(embed=embed)


    # Read data from file
    async def update_data(self):
        global players_online
        global players

        # Open server_data.txt file
        with open(f'{file_path}server_data.txt') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=',')) # Get data in CSV format
            if len(csv_reader) > 0:
                players = csv_reader[0] # Get players online
                players_online = len(players) - 1 # Get num players online
            else:
                players = [] # Set players to 0
                players_online = 0 # Set num players online

    
    # Get data that doesn't change (Max Players)
    async def get_starting_data(self):
        global max_players

        # Open server_data.txt file
        with open(f'{file_path}server.properties') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=',')) # Get data in CSV format
            if len(csv_reader) > 0:
                max_players = int(csv_reader[24][0][12:]) # Get max players from server.properties and convert to int



def setup(client):
    client.add_cog(ServerInfo(client))
