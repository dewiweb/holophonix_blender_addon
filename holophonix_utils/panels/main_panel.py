import bpy

class SNA_PT_MAIN_PANEL(bpy.types.Panel):
    bl_label = ''
    bl_idname = 'SNA_PT_MAIN_PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HOLOUTILS'

    def draw(self, context):
        layout = self.layout
        
        # Logo and title section
        row = layout.row()
        row.prop(context.scene.holophonix_utils, "show_introduction", 
                 text="Holophonix Utils", 
                 icon='TRIA_DOWN' if context.scene.holophonix_utils.show_introduction else 'TRIA_RIGHT', 
                 emboss=False)
    
        if context.scene.holophonix_utils.show_introduction:
            row = layout.row()
            row.template_icon(icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, scale=1.0)
            col = row.column()
            col.label(text="Getting Started")
            
            # Quick getting started guide
            box = layout.box()
            col = box.column(align=True)
            col.label(text="1. Import project from zip file")
            col.label(text="2. Import 3D model of venue")
            col.label(text="3. Import tracks/speakers")
            col.label(text="4. You can also import tracks/")
            col.label(text="   speakers from .hol file")
        
        # The main panel now focuses solely on introduction and overview
        # Specific functionality is contained in respective sub-panels
