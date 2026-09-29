package com.cobblelore.legendary.item;

import net.minecraft.item.Item;

/**
 * Legendary key item matching Delta Client / Academy gimmick items (durability 2, stack 1).
 */
public class LegendaryKeyItem extends Item {
    public LegendaryKeyItem() {
        super(new Settings().maxCount(1).maxDamage(2));
    }
}
