import bpy
from bpy_extras.io_utils import ExportHelper

class SNA_OT_Tracks_Exporter_34F69(bpy.types.Operator, ExportHelper):
    bl_idname = "sna.tracks_exporter_34f69"
    bl_label = "Export Tracks"
    bl_description = "Export Holo objects to OSC handlers, you can then import them with 'import OSC config'"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'})
    filename_ext = '.json'

    def execute(self, context):
        handlers = []

        # Get all objects in the scene
        objects = [obj.name for obj in bpy.context.scene.objects]
        tracks = [t for t in objects if "track" in t]
        speakers = [s for s in objects if "speaker" in s]

        # Create track handlers
        for x in tracks:
            trk = bpy.data.objects[x]
            index = ((trk.name).split('.'))[1]
            id = int(index)

            handlers.extend([
                {
                    "address": f"/track/{id}/x",
                    "data_path": f"bpy.data.objects['{trk.name}'].matrix_world.translation[0]",
                    "osc_type": "f",
                    "osc_index": "()",
                    "osc_direction": "OUTPUT",
                    "filter_repetition": False,
                    "dp_format_enable": False,
                    "dp_format": "args",
                    "loop_enable": False,
                    "loop_range": "0, length, 1",
                    "enabled": bpy.context.scene.holophonix_utils.enable_track
                },
                {
                    "address": f"/track/{id}/y",
                    "data_path": f"bpy.data.objects['{trk.name}'].matrix_world.translation[1]",
                    "osc_type": "f",
                    "osc_index": "()",
                    "osc_direction": "OUTPUT",
                    "filter_repetition": False,
                    "dp_format_enable": False,
                    "dp_format": "args",
                    "loop_enable": False,
                    "loop_range": "0, length, 1",
                    "enabled": bpy.context.scene.holophonix_utils.enable_track
                },
                {
                    "address": f"/track/{id}/z",
                    "data_path": f"bpy.data.objects['{trk.name}'].matrix_world.translation[2]",
                    "osc_type": "f",
                    "osc_index": "()",
                    "osc_direction": "OUTPUT",
                    "filter_repetition": False,
                    "dp_format_enable": False,
                    "dp_format": "args",
                    "loop_enable": False,
                    "loop_range": "0, length, 1",
                    "enabled": bpy.context.scene.holophonix_utils.enable_track
                },
                {
                    "address": f"/track/{id}/color",
                    "data_path": f"bpy.data.objects['{trk.name}'].color",
                    "osc_type": "f",
                    "osc_index": "(0,1,2,3)",
                    "osc_direction": "INPUT",
                    "filter_repetition": False,
                    "dp_format_enable": False,
                    "dp_format": "args",
                    "loop_enable": False,
                    "loop_range": "0, length, 1",
                    "enabled": bpy.context.scene.holophonix_utils.enable_track
                },
                {
                    "address": f"/track/{id}/name",
                    "data_path": f"bpy.data.objects['{trk.name}'].name",
                    "osc_type": "s",
                    "osc_index": "(0)",
                    "osc_direction": "INPUT",
                    "filter_repetition": False,
                    "dp_format_enable": False,
                    "dp_format": "args",
                    "loop_enable": False,
                    "loop_range": "0, length, 1",
                    "enabled": bpy.context.scene.holophonix_utils.enable_track
                }
            ])

        # Write to file
        with open(self.filepath, 'w') as f:
            import json
            json.dump(handlers, f, indent=4)

        return {"FINISHED"}
