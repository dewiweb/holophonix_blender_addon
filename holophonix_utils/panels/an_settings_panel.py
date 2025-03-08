class SNA_PT_HOLOUTILS_1B113(bpy.types.Panel):
    bl_label = 'HoloUtils'
    bl_idname = 'SNA_PT_HOLOUTILS_1B113'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HoloUtils'

    def draw(self, context):
        layout = self.layout
        """props = context.scene.holophonix_utils"""
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'logo_svg_blanc.png')), scale=2.0)
