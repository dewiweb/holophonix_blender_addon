import bpy
import os
from bpy.utils import previews

class IconUtils(bpy.types.PropertyGroup):
    def register_icons(self):
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
        self.icons = bpy.utils.previews.new()
        self.icons.load('logo_icon', os.path.join(icons_dir, 'logo_icon.png'), 'IMAGE')

    def unregister_icons(self):
        if hasattr(self, 'icons'):
            self.icons.clear()
            bpy.utils.previews.remove(self.icons)
