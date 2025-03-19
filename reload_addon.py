import bpy

# Unregister and register the addon to get the changes
addon_name = "holophonix_utils"

# First disable/unregister the addon
if addon_name in bpy.context.preferences.addons:
    bpy.ops.preferences.addon_disable(module=addon_name)
    print(f"Disabled {addon_name} addon")

# Then enable/register it again
bpy.ops.preferences.addon_enable(module=addon_name)
print(f"Enabled {addon_name} addon")
print("Addon successfully reloaded with all new operators")
