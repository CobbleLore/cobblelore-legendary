package com.cobblelore.legendary.mixin.mythsandlegends;

import com.cobblelore.legendary.registry.ModItems;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(targets = "com.github.d0ctorleon.mythsandlegends.items.Items")
public class MixinItems {

    @Inject(method = "<clinit>", at = @At("RETURN"))
    private static void cobblelore$ensureKeyItemsRegistered(CallbackInfo ci) {
        // M&L 1.9.0 registers KEY_ITEM_NAMES as mythsandlegends:<path> only. CobbleLore items live
        // under cobblelore: and are matched by spawn JSON via full Identifier strings.
        ModItems.register();
    }
}
