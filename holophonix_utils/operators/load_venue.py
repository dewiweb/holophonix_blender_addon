import bpy
import json
import os

class SNA_OT_Load_Venue(bpy.types.Operator):
    bl_idname = 'sna.load_venue'
    bl_label = 'Load Venue'
    bl_description = 'Load the venue from the imported Holophonix project'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Path to the extracted project directory
        project_dir = os.path.splitext(bpy.context.scene.holophonix_utils.project_path)[0]

        # Load manifest.json
        manifest_path = os.path.join(project_dir, 'manifest.json')
        if not os.path.exists(manifest_path):
            self.report({'ERROR'}, 'manifest.json not found!')
            return {'CANCELLED'}

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Load the .glb file
        venue_path = os.path.join(project_dir, 'Venue', 'scene.glb')
        if not os.path.exists(venue_path):
            self.report({'ERROR'}, 'Venue/scene.glb not found!')
            return {'CANCELLED'}

        bpy.ops.import_scene.gltf(filepath=venue_path)

        # Apply metadata from manifest.json
        venue_obj = bpy.context.selected_objects[0]
        if 'venue' in manifest:
            venue_data = manifest['venue']
            if 'scale' in venue_data:
                venue_obj.scale = venue_data['scale']
            if 'position' in venue_data:
                venue_obj.location = venue_data['position']
            if 'rotation' in venue_data:
                venue_obj.rotation_euler = venue_data['rotation']

        self.report({'INFO'}, 'Venue loaded successfully!')
        return {'FINISHED'}
