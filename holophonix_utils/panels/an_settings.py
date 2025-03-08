import bpy
from ..utils.plugin_utils import plugin_exists
from ..utils.property_utils import property_exists

def plugin_folder(name, globals, locals):
    return name in bpy.context.preferences.addons

class SNA_PT_AN_SETTINGS_E1993(bpy.types.Panel):
    bl_label = 'AN Settings'
    bl_idname = 'SNA_PT_AN_SETTINGS_E1993'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 3
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        try:
            return 'animation_nodes' in context.preferences.addons
        except:
            return False

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        try:
            if 'animation_nodes' not in context.preferences.addons:
                layout.label(text='Install Animation Nodes First', icon_value=2)
                return
            if not context.preferences.addons['animation_nodes'].preferences:
                layout.label(text='Enable Animation Nodes in Preferences', icon_value=2)
                return
        except:
            pass
        if (property_exists("bpy.data.node_groups", globals(), locals()) and 'AN Tree' in bpy.data.node_groups):
            if hasattr(bpy.data.node_groups['AN Tree'].nodes['Data Input.001'].inputs[0], 'value'):
                layout.prop(bpy.data.node_groups['AN Tree'].nodes['Data Input.001'].inputs[0], 'value', text='View Names', icon_value=0, emboss=True)
            if hasattr(bpy.data.node_groups['AN Tree'].nodes['Data Input'].inputs[0], 'value'):
                layout.prop(bpy.data.node_groups['AN Tree'].nodes['Data Input'].inputs[0], 'value', text='Path to dump', icon_value=0, emboss=True)
        else:
            op = layout.operator('sna.import_an_tree_433db', text='Import AN Tree', icon_value=2, emboss=True, depress=False)
