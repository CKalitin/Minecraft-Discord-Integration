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

# Seconds between loops
loop_time = 2

class ServerChat(commands.Cog):
    def __init__(self, client):
        self.client = client

    # When bot is ready print "Ready" and call starting functions
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready: Server Chat")
        await self.loop()


    # Update is called every (update_time) and it reads new dat and updates the embed
    async def loop(self):
        while True:
            await self.read_minecraft_chat_data()
            await asyncio.sleep(loop_time)

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == channel_id and message.author.id != self.client.user.id:
            # Open discord_chat_data.txt file to append to
            with open(f'{file_path}discord_chat_data.txt', "a") as f:
                f.write(f"{message.author.name}: {message.content}\n")
                print(f"Discord: {message.author.name}: {message.content}")

    
    async def read_minecraft_chat_data(self):
        # Open minecraft_chat_data.txt file
        with open(f'{file_path}minecraft_chat_data.txt') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter='¦')) # Get data in CSV format (CSV isn't great for this because people use comma's, had to change to obscure delimiter character)
            
            if len(csv_reader) > 0: # If file contains data
                for row in csv_reader: # Loop though the rows
                    await self.client.get_channel(channel_id).send(f"**{row[0]}:**{row[1]}") # Send message in current row
                    print(f"Minecraft: {row[0]}:{row[1]}")

        # Delete contents of file
        with open(f'{file_path}minecraft_chat_data.txt', "w") as f:
            f.write("")


# Get bot.py to get this cog
def setup(client):
    client.add_cog(ServerChat(client))
