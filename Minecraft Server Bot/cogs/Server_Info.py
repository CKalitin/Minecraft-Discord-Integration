import asyncio
import discord
from discord.ext import commands
from discord import embeds
from discord import colour
import asyncio
import csv

# Channel ID in discord to write to
channel_id = 846165990622494750

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
loop_time = 1

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

        await self.setup_embed(False)

        await self.get_starting_data()

        await self.loop()


    # Update is called every (update_time) and it reads new dat and updates the embed
    async def loop(self):
        while True:
            await self.update_embed()
            await self.update_data()
            await asyncio.sleep(loop_time)


    # Send embed with starting text
    async def setup_embed(self, newEmbed):
        global embed
        global embed_message

        # Open file 'embed_id.txt' and read it into embed_id variable
        embed_id_file = open('embed_id.txt', 'r')
        embed_id = embed_id_file.read()
        embed_id_file.close()

        # If this function should create a new embed and delete the old one.
        # It simply trys to get the old embed, if there is one it deletes it
        # and the rest of the code handles creating a new one.
        if newEmbed:
            try:
                embed_message = await self.client.get_channel(channel_id).fetch_message(embed_id)
                await embed_message.delete()
            except:
                pass
    
        # Try to get existing embed, if it can't be gotten, make a new one
        try: 
            embed_message = await self.client.get_channel(channel_id).fetch_message(embed_id)
            
            embed.set_thumbnail(url="https://hypixel.net/attachments/crafty_logo_shadowfixed_small-png.1035865/")

            embed.set_footer(text=f"Use the -players or -online or -status command." )
        except:
            embed.set_thumbnail(url="https://hypixel.net/attachments/crafty_logo_shadowfixed_small-png.1035865/")

            embed.set_footer(text=f"Use the -players or -online or -status command.")

            embed_message = await self.client.get_channel(channel_id).send(embed=embed)
            
            # Write embed_id to file
            embed_id_file = open('embed_id.txt', 'w')
            embed_id = embed_id_file.write(str(embed_message.id))
            embed_id_file.close()


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
        
        # Update activity of the bot to show current players
        if players_online <= 0:
            await self.client.change_presence(activity=discord.Game(f'with u in my dreams 😜'))
        elif players_online == 1:
            await self.client.change_presence(activity=discord.Game(f'with {players[0]}'))
        else:
            await self.client.change_presence(activity=discord.Game(f'with {players_online} players on CEJA.'))




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

        # Open server.properties file
        with open(f'{file_path}server.properties') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=',')) # Get data in CSV format
            if len(csv_reader) > 0:
                max_players = int(csv_reader[26][0][12:]) # Get max players from server.properties and convert to int


    @commands.command(aliases=['Online', 'Status', 'online', 'status', 'players', 'Players'])
    async def SendNewEmbed(self, ctx):
        await self.setup_embed(True)


def setup(client):
    client.add_cog(ServerInfo(client))
