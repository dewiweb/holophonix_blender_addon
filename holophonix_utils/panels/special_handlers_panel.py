import bpy

class SNA_PT_SPECIALHANDLERS(bpy.types.Panel):
    bl_label = 'OSC Handlers'
    bl_idname = 'SNA_PT_SPECIALHANDLERS'
    bl_space_type = 'VIEW_3D'  # The panel will appear in the 3D Viewport
    bl_region_type = 'UI'  # The panel will appear in the sidebar
    bl_context = ''  # Optional: specify the context (e.g., 'objectmode')
    bl_order = 0  # Order of the panel within its category
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'  # Parent panel ID
    bl_ui_units_x = 0  # Width of the panel in UI units

    @classmethod
    def poll(cls, context):
        # Ensure the panel is only visible under certain conditions
        return not (False)

    def draw_header(self, context):
        # Custom header with an icon
        layout = self.layout
        layout.template_icon(icon_value=244, scale=1.2100000381469727)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        holophonix_utils = scene.holophonix_utils
        props = context.scene.holophonix_utils

        # Check if NodeOSC is installed
        if "NodeOSC" not in context.preferences.addons:
            layout.label(text="NodeOSC addon isn't installed!", icon_value=2)
            return

        # Check if NodeOSC is enabled
        if not context.preferences.addons["NodeOSC"].preferences:
            layout.label(text="Enable NodeOSC addon in preferences!", icon_value=2)
            return

        # Check if NodeOSC_keys collection exists
        if not hasattr(context.scene, 'NodeOSC_keys'):
            layout.label(text="NodeOSC keys collection not found!", icon_value=2)
            return

        keys = context.scene.NodeOSC_keys
        if not keys:
            layout.operator("sna.add_handlers", text="Add Special Handlers", icon_value=108, emboss=True, depress=False)
            return

        handler_addresses = {"/dump", "/track/*", "/speaker/*", "/frames/str"}
        existing_addresses = {item.osc_address for item in keys}
        handlers_exist = handler_addresses.issubset(existing_addresses)

        if handlers_exist:
            # Show checkboxes if handlers exist and link them to handler states
            for item in keys:
                if item.osc_address == "/dump":
                    layout.prop(props, "enable_dump", text="Enable Dump Handler")
                    if props.enable_dump != item.enabled:
                        try:
                            item.enabled = props.enable_dump
                        except:
                            pass
                    elif item.enabled != props.enable_dump:
                        props.enable_dump = item.enabled
                elif item.osc_address == "/track/*":
                    layout.prop(props, "enable_track", text="Enable Track Handler")
                    if props.enable_track != item.enabled:
                        try:
                            item.enabled = props.enable_track
                        except:
                            pass
                    elif item.enabled != props.enable_track:
                        props.enable_track = item.enabled
                elif item.osc_address == "/speaker/*":
                    layout.prop(props, "enable_speaker", text="Enable Speaker Handler")
                    if props.enable_speaker != item.enabled:
                        try:
                            item.enabled = props.enable_speaker
                        except:
                            pass
                    elif item.enabled != props.enable_speaker:
                        props.enable_speaker = item.enabled
                elif item.osc_address == "/frames/str":
                    layout.prop(props, "enable_reaperTC", text="Enable Reaper TC Handler")
                    if props.enable_reaperTC != item.enabled:
                        try:
                            item.enabled = props.enable_reaperTC
                        except:
                            pass
                    elif item.enabled != props.enable_reaperTC:
                        props.enable_reaperTC = item.enabled
        else:
            # Show button if handlers don't exist
            layout.operator("sna.add_handlers", text="Add Special Handlers", icon_value=108, emboss=True, depress=False)


class HolophonixUtilsProperties(bpy.types.PropertyGroup):
    enable_dump: bpy.props.BoolProperty(name="Enable Dump Handler", default=False)
    enable_track: bpy.props.BoolProperty(name="Enable Track Handler", default=False)
    enable_speaker: bpy.props.BoolProperty(name="Enable Speaker Handler", default=False)
    enable_reaperTC: bpy.props.BoolProperty(name="Enable Reaper TC Handler", default=False)


@bpy.app.handlers.persistent
def update_holophonix_properties(scene):
    if not hasattr(scene, 'NodeOSC_keys') or not hasattr(scene, 'holophonix_utils'):
        return
    
    props = scene.holophonix_utils
    for item in scene.NodeOSC_keys:
        if item.osc_address == "/dump":
            props.enable_dump = item.enabled
        elif item.osc_address == "/track/*":
            props.enable_track = item.enabled
        elif item.osc_address == "/speaker/*":
            props.enable_speaker = item.enabled
        elif item.osc_address == "/frames/str":
            props.enable_reaperTC = item.enabled

# Register the handler
bpy.app.handlers.depsgraph_update_post.append(update_holophonix_properties)
