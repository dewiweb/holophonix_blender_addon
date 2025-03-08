import bpy

def plugin_exists(plugin_name):
    try:
        return plugin_name in bpy.context.preferences.addons
    except:
        return False

def plugin_folder(plugin_name):
    try:
        addon = bpy.context.preferences.addons.get(plugin_name)
        return addon is not None and hasattr(addon, 'preferences')
    except:
        return False
