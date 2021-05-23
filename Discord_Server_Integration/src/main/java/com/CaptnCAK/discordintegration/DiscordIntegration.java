package com.CaptnCAK.discordintegration;

import net.minecraft.block.Block;
import net.minecraft.block.Blocks;
import net.minecraft.entity.player.PlayerEntity;
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
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

// The value here should match an entry in the META-INF/mods.toml file
@Mod("discordintegration")
public class DiscordIntegration
{
    int millisBetweenDataUpdate = 2000;

    long timerStartTime = 0;

    List<PlayerEntity> players = new ArrayList<PlayerEntity>();
    List<String> playerNames = new ArrayList<String>();

    // Directly reference a log4j logger.
    private static final Logger LOGGER = LogManager.getLogger();

    public DiscordIntegration() {
        // Register the setup method for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);
        // Register the enqueueIMC method for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::enqueueIMC);
        // Register the processIMC method for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::processIMC);
        // Register the doClientStuff method for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::doClientStuff);

        // Register ourselves for server and other game events we are interested in
        MinecraftForge.EVENT_BUS.register(this);
    }

    private void setup(final FMLCommonSetupEvent event)
    {
        // some preinit code
        LOGGER.info("HELLO FROM PREINIT");
        LOGGER.info("DIRT BLOCK >> {}", Blocks.DIRT.getRegistryName());
    }

    private void doClientStuff(final FMLClientSetupEvent event) {
        // do something that can only be done on the client
        LOGGER.info("Got game settings {}", event.getMinecraftSupplier().get().options);
    }

    private void enqueueIMC(final InterModEnqueueEvent event)
    {
        // some example code to dispatch IMC to another mod
        InterModComms.sendTo("examplemod", "helloworld", () -> { LOGGER.info("Hello world from the MDK"); return "Hello world";});
    }

    private void processIMC(final InterModProcessEvent event)
    {
        // some example code to receive and process InterModComms from other mods
        LOGGER.info("Got IMC {}", event.getIMCStream().
                map(m->m.getMessageSupplier().get()).
                collect(Collectors.toList()));
    }

    /*private void Loop() {
        if (System.currentTimeMillis() - timerStartTime >= millisBetweenDataUpdate){
            timerStartTime = System.currentTimeMillis();
            LOGGER.info("current dir = " + System.getProperty("user.dir"));
        }
        Loop();
    }*/

    // You can use SubscribeEvent and let the Event Bus discover methods to call
    @SubscribeEvent
    public void onServerStarting(FMLServerStartingEvent event) {
        // do something when the server starts
        LOGGER.info("HELLO from server starting");
        timerStartTime = System.currentTimeMillis();

        //Loop();
    }

    @SubscribeEvent
    public void onChatEvent(ServerChatEvent event) {
        LOGGER.info(event.getPlayer() + " " + event.getUsername() + " " + event.getMessage());
    }

    @SubscribeEvent
    public void onPlayerConnectEvent(PlayerEvent.PlayerLoggedInEvent event){
        players.add(event.getPlayer());
        playerNames.add(event.getPlayer().getDisplayName().getString());
        LOGGER.info(event.getPlayer().getDisplayName().getString());
        UpdateServerData();
    }

    @SubscribeEvent
    public void onPlayerDisconnectEvent(PlayerEvent.PlayerLoggedOutEvent event){
        players.remove(event.getPlayer());
        playerNames.remove(event.getPlayer().getDisplayName().getString());
        UpdateServerData();
    }

    private void UpdateServerData() {
        try {
            PrintWriter pw = new PrintWriter("server_data.txt");
            pw.close();

            FileWriter fw = new FileWriter("server_data.txt");
            for (int i = 0; i < playerNames.size(); i++){
                fw.write(playerNames.get(i) + ", ");
            }
            fw.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("Could not write to server_data.txt");
            e.printStackTrace();
        }
    }

    // You can use EventBusSubscriber to automatically subscribe events on the contained class (this is subscribing to the MOD
    // Event bus for receiving Registry Events)
    @Mod.EventBusSubscriber(bus=Mod.EventBusSubscriber.Bus.MOD)
    public static class RegistryEvents {
        @SubscribeEvent
        public static void onBlocksRegistry(final RegistryEvent.Register<Block> blockRegistryEvent) {
            // register a new block here
            LOGGER.info("HELLO from Register Block");
        }
    }
}
