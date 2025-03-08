import bpy

class SNA_PT_HOLOUTILS_1B113(bpy.types.Panel):
    bl_label = 'HOLOUTILS'
    bl_idname = 'SNA_PT_HOLOUTILS_1B113'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HOLOUTILS'

    def draw(self, context):
        layout = self.layout
        layout.template_icon(icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, scale=2.0)
