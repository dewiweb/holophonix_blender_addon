import bpy

class SNA_PT_MAIN_PANEL(bpy.types.Panel):
    bl_label = 'Holophonix Utils'
    bl_idname = 'SNA_PT_MAIN_PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HOLOUTILS'

    def draw(self, context):
        layout = self.layout
        
        # Logo and title section
        row = layout.row()
        row.template_icon(icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, scale=2.0)
        col = row.column()
        col.label(text="Holophonix Utils")
        col.label(text="Spatial Audio Tools", icon='SPEAKER')
        
        # Quick getting started guide
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Getting Started", icon='HELP')
        col.label(text="1. Import project or tracks")
        col.label(text="2. Configure track handlers")
        col.label(text="3. Create OSC connections")
        
        # The main panel now focuses solely on introduction and overview
        # Specific functionality is contained in respective sub-panels
