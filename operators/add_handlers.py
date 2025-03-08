import bpy

class SNA_OT_Add_Handlers(bpy.types.Operator):
    """Add special handlers for holophonix_utils"""
    bl_idname = "sna.add_handlers"
    bl_label = "Add Special OSC Handlers"

    def execute(self, context):
        if "NodeOSC" not in bpy.context.preferences.addons:
            self.report({'ERROR'}, "NodeOSC addon is not installed or enabled")
            return {'CANCELLED'}

        # Define handler configurations
        handler_configs = [
            {
                "data_path": "exec(\"import bpy\\nholophonix_utils = bpy.context.scene.holophonix_utils\\nholophonix_utils.dump(bpy.context, '{0}','{1}')\")",
                "osc_address": "/dump",
                "osc_type": "f",
                "osc_index": "()",
                "osc_direction": "INPUT",
                "filter_repetition": False,
                "dp_format_enable": True,
                "dp_format": "args",
                "loop_enable": False,
                "loop_range": "0, length, 1"
            },
            {
                "data_path": "exec(\"import bpy\\nholophonix_utils = bpy.context.scene.holophonix_utils\\nholophonix_utils.track(bpy.context, '{0}','{1}')\")",
                "osc_address": "/track/*",
                "osc_type": "f",
                "osc_index": "()",
                "osc_direction": "INPUT",
                "filter_repetition": False,
                "dp_format_enable": True,
                "dp_format": "args",
                "loop_enable": False,
                "loop_range": "0, length, 1"
            },
            {
                "data_path": "exec(\"import bpy\\nholophonix_utils = bpy.context.scene.holophonix_utils\\nholophonix_utils.speaker(bpy.context, '{0}','{1}')\")",
                "osc_address": "/speaker/*",
                "osc_type": "f",
                "osc_index": "()",
                "osc_direction": "INPUT",
                "filter_repetition": False,
                "dp_format_enable": True,
                "dp_format": "args",
                "loop_enable": False,
                "loop_range": "0, length, 1"
            },
            {
                "data_path": "exec(\"import bpy\\nholophonix_utils = bpy.context.scene.holophonix_utils\\nholophonix_utils.tc_to_frames(bpy.context, '{0}')\")",
                "osc_address": "/frames/str",
                "osc_type": "f",
                "osc_index": "()",
                "osc_direction": "INPUT",
                "filter_repetition": False,
                "dp_format_enable": True,
                "dp_format": "args",
                "loop_enable": False,
                "loop_range": "0, length, 1"
            }
        ]

        # Create handlers by adding items to NodeOSC_keys
        keys = bpy.context.scene.NodeOSC_keys
        for config in handler_configs:
            new_item = keys.add()
            new_item.data_path = config["data_path"]
            new_item.osc_address = config["osc_address"]
            new_item.osc_type = config["osc_type"]
            new_item.osc_index = config["osc_index"]
            new_item.osc_direction = config["osc_direction"]
            new_item.filter_repetition = config["filter_repetition"]
            new_item.dp_format_enable = config["dp_format_enable"]
            new_item.dp_format = config["dp_format"]
            new_item.loop_enable = config["loop_enable"]
            new_item.loop_range = config["loop_range"]

        # Set enabled state based on holophonix_utils properties
        for item in keys:
            if item.osc_address == "/dump":
                item.enabled = bpy.context.scene.holophonix_utils.enable_dump
            elif item.osc_address == "/track/*":
                item.enabled = bpy.context.scene.holophonix_utils.enable_track
            elif item.osc_address == "/speaker/*":
                item.enabled = bpy.context.scene.holophonix_utils.enable_speaker
            elif item.osc_address == "/frames/str":
                item.enabled = bpy.context.scene.holophonix_utils.enable_reaperTC

        self.report({'INFO'}, "Handlers added successfully")
        return {'FINISHED'}
