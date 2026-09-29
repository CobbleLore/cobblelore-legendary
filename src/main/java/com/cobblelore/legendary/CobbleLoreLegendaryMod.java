package com.cobblelore.legendary;

import com.cobblelore.legendary.registry.ModItemGroups;
import com.cobblelore.legendary.registry.ModItems;
import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class CobbleLoreLegendaryMod implements ModInitializer {
    public static final String MOD_ID = "cobblelore";
    public static final Logger LOGGER = LoggerFactory.getLogger("cobblelore-legendary");

    @Override
    public void onInitialize() {
        ModItems.register();
        ModItemGroups.register();
        LOGGER.info("Registered {} legendary key items", ModItems.all().size());
    }
}
