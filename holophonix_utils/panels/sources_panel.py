import bpy

class SNA_PT_SOURCES_11FF6(bpy.types.Panel):
    bl_label = 'Sources'
    bl_idname = 'SNA_PT_SOURCES_11FF6'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='FILE_SOUND')

    def draw(self, context):
        layout = self.layout
        props = context.scene.holophonix_utils

        # Add operator for importing sources
        op = layout.operator('sna.add_sources_73b0d', text='Import Sources  From .hol', icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, emboss=True, depress=False)

        # Check if there are track handlers in NodeOSC_keys
        if hasattr(context.scene, 'NodeOSC_keys'):
            has_incoming = any(item.osc_direction == "INPUT" and "/track/" in item.osc_address for item in context.scene.NodeOSC_keys)
            has_outgoing = any(item.osc_direction == "OUTPUT" and "/track/" in item.osc_address for item in context.scene.NodeOSC_keys)

            # Only show track handler section if there are relevant handlers
            if has_incoming or has_outgoing:
                box = layout.box()
                box.label(text="Track Handlers")
                if has_incoming:
                    row = box.row()
                    row.prop(props, "enable_incoming_tracks", text="Incoming Tracks")
                if has_outgoing:
                    row = box.row()
                    row.prop(props, "enable_outgoing_tracks", text="Outgoing Tracks")