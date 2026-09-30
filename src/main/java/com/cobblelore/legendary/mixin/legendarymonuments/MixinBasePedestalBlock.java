package com.cobblelore.legendary.mixin.legendarymonuments;

import com.cobblelore.legendary.item.LegendaryKeyItem;
import com.jorgaomc.legendarymonuments.blocks.pedestals.BasePedestalBlock;
import com.jorgaomc.legendarymonuments.blocks.pedestals.entity.BasePedestalBlockEntity;
import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * LM default: item on pedestal + empty hand = pickup. CobbleLore: activate spawn and consume the pedestal item.
 *
 * <p>Pedestal item ids are aligned client/server via {@link
 * com.cobblelore.legendary.legendarymonuments.PedestalConfigOverrides}.
 */
@Mixin(value = BasePedestalBlock.class, remap = false)
public abstract class MixinBasePedestalBlock {

    @Inject(
            method = "method_55765",
            at = @At(
                    value = "INVOKE",
                    target =
                            "Lcom/jorgaomc/legendarymonuments/blocks/pedestals/entity/BasePedestalBlockEntity;method_5434(II)Lnet/minecraft/class_1799;",
                    remap = false),
            cancellable = true)
    private void cobblelore$spawnFromPedestalStack(
            ItemStack stack,
            BlockState state,
            World world,
            BlockPos pos,
            PlayerEntity player,
            Hand hand,
            BlockHitResult hitResult,
            CallbackInfoReturnable<ActionResult> cir) {
        if (world.isClient()) {
            return;
        }
        if (!stack.isEmpty()) {
            return;
        }
        if (!(world.getBlockEntity(pos) instanceof BasePedestalBlockEntity pedestal)) {
            return;
        }
        if (pedestal.isEmpty()) {
            return;
        }
        ItemStack onPedestal = pedestal.getStack(0);
        if (onPedestal.isEmpty() || !(onPedestal.getItem() instanceof LegendaryKeyItem)) {
            return;
        }

        if (pedestal.handleSpecialAction(player, onPedestal)) {
            pedestal.clear();
            world.updateListeners(pos, state, state, Block.NOTIFY_ALL);
            cir.setReturnValue(ActionResult.SUCCESS);
        }
    }
}
