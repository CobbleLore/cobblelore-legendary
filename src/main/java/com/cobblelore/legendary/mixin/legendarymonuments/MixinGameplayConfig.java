package com.cobblelore.legendary.mixin.legendarymonuments;

import com.cobblelore.legendary.legendarymonuments.PedestalConfigOverrides;
import com.jorgaomc.legendarymonuments.config.GameplayConfig;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = GameplayConfig.class, remap = false)
public abstract class MixinGameplayConfig {

    @Inject(method = "applyPedestalOverrides", at = @At("RETURN"))
    private static void cobblelore$reapplyCobblelorePedestalIds(CallbackInfo ci) {
        PedestalConfigOverrides.apply();
    }
}
