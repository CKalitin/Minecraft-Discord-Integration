package com.CaptnCAK.discordintegration;

import java.util.List;

import net.minecraft.block.Block;
import net.minecraft.block.Blocks;
import net.minecraft.client.Minecraft;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.util.text.ITextComponent;
import net.minecraft.util.text.StringTextComponent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.InterModComms;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.event.lifecycle.InterModEnqueueEvent;
import net.minecraftforge.fml.event.lifecycle.InterModProcessEvent;
import net.minecraftforge.fml.event.server.FMLServerStartingEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.sql.ConnectionEvent;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.util.stream.Collectors;

// The value here should match an entry in the META-INF/mods.toml file
@Mod("discordintegration")
public class DiscordIntegration
{
    static List<PlayerEntity> players = new ArrayList<PlayerEntity>();
    static List<String> playerNames = new ArrayList<String>();

    // Directly reference a log4j logger.
    private static final Logger LOGGER = LogManager.getLogger();

    public DiscordIntegration() {
        // Register the setup method for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);

        // Register ourselves for server and other game events we are interested in
        MinecraftForge.EVENT_BUS.register(this);
    }

    private void setup(final FMLCommonSetupEvent event)
    {
        // some preinit code
        LOGGER.info("HELLO FROM PREINIT");
        LOGGER.info("DIRT BLOCK >> {}", Blocks.DIRT.getRegistryName());
    }

    // You can use SubscribeEvent and let the Event Bus discover methods to call
    @SubscribeEvent
    public void onServerStarting(FMLServerStartingEvent event) {
        // do something when the server starts

        Timer timer = new Timer(); // Create new Timer
        timer.schedule(new Loop(), 0, 1000); // Get Timer to call run in Loop class every second
    }

    @SubscribeEvent
    public void onChatEvent(ServerChatEvent event) {
        try {
            PrintWriter pw = new PrintWriter("minecraft_chat_data.txt"); // Open file minecraft_chat_data.txt
            pw.println(event.getUsername() + "¦ " + event.getMessage()); // Write username and message to bottom of file
            pw.close(); // Close file
        } catch (IOException e) {
            System.out.println("Could not write to minecraft_chat_data.txt");
            e.printStackTrace();
        }
    }

    @SubscribeEvent
    public void onPlayerConnectEvent(PlayerEvent.PlayerLoggedInEvent event){
        players.add(event.getPlayer()); // Add PlayerEntity to List of PlayerEntity's
        playerNames.add(event.getPlayer().getDisplayName().getString()); // Add player names to list of player names
        UpdateServerData(); // call Update server_data.txt function
    }

    @SubscribeEvent
    public void onPlayerDisconnectEvent(PlayerEvent.PlayerLoggedOutEvent event){
        players.remove(event.getPlayer()); // Remove PlayerEntity to List of PlayerEntity's
        playerNames.remove(event.getPlayer().getDisplayName().getString()); // Remove player names to list of player names
        UpdateServerData(); // call Update server_data.txt function
    }

    private void UpdateServerData() {
        // Nothing here is a true CSV, just writing text similar to a CSV
        try {
            PrintWriter pw = new PrintWriter("server_data.txt"); // Open server_data.txt and Clear all text from it
            pw.close(); // Close file

            FileWriter fw = new FileWriter("server_data.txt"); // Open server_data.txt
            for (int i = 0; i < playerNames.size(); i++){ // Loop through player names
                fw.write(playerNames.get(i) + ", "); // Write player name to server_data.txt
            }
            fw.close(); // Close server_data.txt
        } catch (IOException e) {
            System.out.println("Could not write to server_data.txt");
            e.printStackTrace();
        }
    }

    public static List<PlayerEntity> GetPlayers(){
        return players;
    }

    // Class is needed for timer in onServerStarting
    public class Loop extends TimerTask {
        // This function will be called every x seconds
        public void run(){
            try {
                List<PlayerEntity> localPlayers = DiscordIntegration.GetPlayers(); // Because this is a new class you need to get the players for the parent class
                try (BufferedReader br = new BufferedReader(new FileReader("discord_chat_data.txt"))) { // Open discord_chat_data.txt in try catch block in case of error
                    String line; // Current line of discord_chat_data.txt
                    while ((line = br.readLine()) != null) { // Loop through all lines
                        if (localPlayers.size() > 0){ // Check length of players to prevent error in for loop
                            for (int i = 0; i < localPlayers.size(); i++){ // Loop through players
                                PlayerEntity player = localPlayers.get(i); // Get current player
                                player.sendMessage(new StringTextComponent(line), player.getUUID()); // Create ITextComponent and Send message to current player
                                LOGGER.info(line); // Send message to console
                            }
                        }
                    }
                }
                PrintWriter pw = new PrintWriter("discord_chat_data.txt"); // Open discord_chat_data.txt and Clear all text from it
                pw.close(); // Close file
            } catch (IOException e){
                System.out.println("Could not read discord_chat_data.txt");
                e.printStackTrace();
            }
        }
    }
}
