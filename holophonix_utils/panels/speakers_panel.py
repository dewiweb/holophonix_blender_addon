import bpy

class SNA_PT_SPEAKERS_F8536(bpy.types.Panel):
    bl_label = 'Speakers'
    bl_idname = 'SNA_PT_SPEAKERS_F8536'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=244, scale=1.2100000381469727)

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.add_speakers_994c8', text='Import Speakers From .hol', icon_value=108, emboss=True, depress=False)
