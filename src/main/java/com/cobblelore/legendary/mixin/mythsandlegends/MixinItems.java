package com.cobblelore.legendary.mixin.mythsandlegends;

import com.cobblelore.legendary.registry.ModItems;
import net.minecraft.util.Identifier;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Mutable;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.ArrayList;
import java.util.List;

@Mixin(targets = "com.github.d0ctorleon.mythsandlegends.items.Items")
public class MixinItems {

    @Shadow
    @Mutable
    @Final
    private static List<String> ITEM_NAMES;

    @Inject(method = "<clinit>", at = @At("RETURN"))
    private static void cobblelore$registerKeyItems(CallbackInfo ci) {
        ModItems.register();
        List<String> names = new ArrayList<>(ITEM_NAMES);
        names.addAll(ModItems.keyItemIdsForMythsAndLegends());
        ITEM_NAMES = names;
    }
}
