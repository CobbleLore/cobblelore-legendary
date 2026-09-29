package com.cobblelore.legendary.registry;

import com.cobblelore.legendary.CobbleLoreLegendaryMod;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

public final class ModItemGroups {
    public static ItemGroup LEGENDARY;

    public static void register() {
        ItemStack icon = new ItemStack(ModItems.all().values().iterator().next());
        LEGENDARY = Registry.register(
                Registries.ITEM_GROUP,
                Identifier.of(CobbleLoreLegendaryMod.MOD_ID, "legendary"),
                FabricItemGroup.builder()
                        .displayName(Text.translatable("itemGroup.cobblelore.legendary"))
                        .icon(() -> icon)
                        .entries((displayContext, entries) -> ModItems.all().values().forEach(entries::add))
                        .build()
        );
    }
}
