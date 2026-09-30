package com.cobblelore.legendary.legendarymonuments;

import com.cobblelore.legendary.CobbleLoreLegendaryMod;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.jorgaomc.legendarymonuments.config.PedestalConfig;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Legendary Monuments reads pedestal item ids from {@link PedestalConfig}. The dedicated server loads
 * {@code config/LegendaryMonuments/config.json}, but the game client often keeps LM defaults — so
 * {@code handleSpecialAction} fails on the client, places a ghost stack on the pedestal, while the server spawns.
 */
public final class PedestalConfigOverrides {
    private static final String RESOURCE = "/legendary-monuments-pedestals-cobblelore.json";

    private static final Map<String, String> JSON_KEY_TO_FIELD = Map.ofEntries(
            Map.entry("enteiPedestalItem", "ENTEI_PEDESTAL_ITEM"),
            Map.entry("raikouPedestalItem", "RAIKOU_PEDESTAL_ITEM"),
            Map.entry("suicunePedestalItem", "SUICUNE_PEDESTAL_ITEM"),
            Map.entry("heatranPedestalItem", "HEATRAN_PEDESTAL_ITEM"),
            Map.entry("hoohPedestalItem", "HOOH_PEDESTAL_ITEM"),
            Map.entry("latiasPedestalItem", "LATIAS_PEDESTAL_ITEM"),
            Map.entry("latiosPedestalItem", "LATIOS_PEDESTAL_ITEM"),
            Map.entry("lugiaPedestalItem", "LUGIA_PEDESTAL_ITEM"),
            Map.entry("hoopaPedestalFirstItem", "HOOPA_PEDESTAL_FIRST_ITEM"),
            Map.entry("hoopaPedestalSecondItem", "HOOPA_PEDESTAL_SECOND_ITEM"),
            Map.entry("zekromPedestalFirstItem", "ZEKROM_PEDESTAL_FIRST_ITEM"),
            Map.entry("zekromPedestalSecondItem", "ZEKROM_PEDESTAL_SECOND_ITEM"),
            Map.entry("reshiramPedestalFirstItem", "RESHIRAM_PEDESTAL_FIRST_ITEM"),
            Map.entry("reshiramPedestalSecondItem", "RESHIRAM_PEDESTAL_SECOND_ITEM"),
            Map.entry("kyuremPedestalFirstItem", "KYUREM_PEDESTAL_FIRST_ITEM"),
            Map.entry("kyuremPedestalSecondItem", "KYUREM_PEDESTAL_SECOND_ITEM"),
            Map.entry("zacianPedestalFirstItem", "ZACIAN_PEDESTAL_FIRST_ITEM"),
            Map.entry("zacianPedestalSecondItem", "ZACIAN_PEDESTAL_SECOND_ITEM"),
            Map.entry("zamazentaPedestalFirstItem", "ZAMAZENTA_PEDESTAL_FIRST_ITEM"),
            Map.entry("zamazentaPedestalSecondItem", "ZAMAZENTA_PEDESTAL_SECOND_ITEM"));

    private PedestalConfigOverrides() {}

    public static void apply() {
        var stream = PedestalConfigOverrides.class.getResourceAsStream(RESOURCE);
        if (stream == null) {
            CobbleLoreLegendaryMod.LOGGER.warn("Missing {} — pedestal item ids not patched", RESOURCE);
            return;
        }
        try (InputStreamReader reader = new InputStreamReader(stream, StandardCharsets.UTF_8)) {
            JsonObject root = JsonParser.parseReader(reader).getAsJsonObject();
            JsonObject pedestals = root.getAsJsonObject("pedestals");
            if (pedestals == null) {
                return;
            }

            Map<String, Field> fieldsByName = new HashMap<>();
            for (Field field : PedestalConfig.class.getDeclaredFields()) {
                if (!Modifier.isStatic(field.getModifiers()) || field.getType() != String.class) {
                    continue;
                }
                String name = field.getName();
                if (!name.endsWith("_PEDESTAL_ITEM")
                        && !name.endsWith("_PEDESTAL_FIRST_ITEM")
                        && !name.endsWith("_PEDESTAL_SECOND_ITEM")) {
                    continue;
                }
                field.setAccessible(true);
                fieldsByName.put(name, field);
            }

            int applied = 0;
            for (Map.Entry<String, JsonElement> entry : pedestals.entrySet()) {
                String jsonKey = entry.getKey();
                if (jsonKey.startsWith("_")) {
                    continue;
                }
                String fieldName = JSON_KEY_TO_FIELD.get(jsonKey);
                if (fieldName == null) {
                    continue;
                }
                Field field = fieldsByName.get(fieldName);
                if (field == null || !entry.getValue().isJsonPrimitive()) {
                    continue;
                }
                String itemId = entry.getValue().getAsString();
                field.set(null, itemId);
                applied++;
            }
            CobbleLoreLegendaryMod.LOGGER.info("Applied {} Legendary Monuments pedestal item overrides", applied);
        } catch (Exception e) {
            CobbleLoreLegendaryMod.LOGGER.error("Failed to apply Legendary Monuments pedestal overrides", e);
        }
    }
}
