import bpy

class SNA_PT_SPEAKERS_F8536(bpy.types.Panel):
    bl_label = 'Speakers'
    bl_idname = 'SNA_PT_SPEAKERS_F8536'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MESH_CUBE')

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.add_speakers_994c8', text='Import Speakers From .hol', icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, emboss=True, depress=False)
