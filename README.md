# Minecraft-Discord-Integration
Get info such as online players, max players, etc. directly into your discord server with this bot and the Minecraft data pack. Also, get Minecraft server chat in your discord server for a chat between Minecraft and discord.

Discord bot setup:
1. Drag the Minecraft Server Bot into your Minecraft Server folder.
2. VS Code Instructions: Open the minecraft server folder with VS Code and launch bot.py
2. Other VS Code Instructions (Not nessecery if you did the other instructions, this is just for quality of life): Change discord_bot_path in bot.py to "Minecraft Server Bot", and file_path in Server_Info.py and Server_Chat.py to "../" and open only the Minecraft Server Bot folder to launch the bot.

Mod Setup:
1. Make sure your minecraft server has Forge.
2. Drag the discordintegration-1.16.5.jar file from Discord_Server_Integration/build/libs into the mods folder of your Forge server (If you don't have a mods folder you either didn't install Forge correctly or have never booted up your server)