package com.cobblelore.legendary.registry;

import com.cobblelore.legendary.CobbleLoreLegendaryMod;
import com.cobblelore.legendary.item.LegendaryKeyItem;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import net.minecraft.item.Item;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class ModItems {
    private static final Map<Identifier, Item> ALL = new LinkedHashMap<>();
    private static boolean registered;

    private ModItems() {
    }

    public static void register() {
        if (registered) {
            return;
        }
        registered = true;
        List<String> ids = loadItemIds();
        for (String path : ids) {
            Identifier id = Identifier.of(CobbleLoreLegendaryMod.MOD_ID, path);
            Item item = Registry.register(Registries.ITEM, id, new LegendaryKeyItem());
            ALL.put(id, item);
        }
    }

    public static Map<Identifier, Item> all() {
        return Collections.unmodifiableMap(ALL);
    }

    private static List<String> loadItemIds() {
        try (var stream = ModItems.class.getClassLoader().getResourceAsStream("cobblelore/legendary_items.json")) {
            if (stream == null) {
                throw new IllegalStateException("Missing cobblelore/legendary_items.json");
            }
            JsonObject root = new Gson().fromJson(new InputStreamReader(stream, StandardCharsets.UTF_8), JsonObject.class);
            List<String> items = new ArrayList<>();
            root.getAsJsonArray("items").forEach(el -> items.add(el.getAsString()));
            return items;
        } catch (Exception e) {
            throw new IllegalStateException("Failed to load legendary item list", e);
        }
    }
}
