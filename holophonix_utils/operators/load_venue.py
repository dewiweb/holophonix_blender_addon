import bpy
import json
import os
import math
from ..utils.file_properties import FileProperties

class SNA_OT_Load_Venue(bpy.types.Operator):
    bl_idname = 'sna.load_venue'
    bl_label = 'Load Venue'
    bl_description = 'Load the venue from the imported Holophonix project'
    bl_options = {'REGISTER', 'UNDO'}

    def _remove_existing_venue(self, context):
        # Find existing venue object
        venue_obj = next((obj for obj in bpy.data.objects if obj.name == 'Venue'), None)
        if not venue_obj:
            return

        # Collect all objects in hierarchy
        all_objects = [venue_obj] + list(venue_obj.children_recursive)

        # Clean up materials and data
        for obj in all_objects:
            # Materials
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    bpy.data.materials.remove(mat_slot.material)
            # Data
            if obj.data:
                data_type = type(obj.data).__name__.lower()
                if data_type in dir(bpy.data):
                    data_collection = getattr(bpy.data, data_type + 's')
                    if obj.data.name in data_collection:
                        data_collection.remove(obj.data)

        # Remove all objects
        for obj in reversed(all_objects):
            bpy.data.objects.remove(obj, do_unlink=True)

    def execute(self, context):
        # Path to the extracted project directory
        project_dir = os.path.splitext(bpy.context.scene.file_properties.project_path)[0]

        # Load manifest.json
        manifest_path = os.path.join(project_dir, 'manifest.json')
        if not os.path.exists(manifest_path):
            self.report({'ERROR'}, 'manifest.json not found!')
            return {'CANCELLED'}

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Import the GLTF file
        model_dir = os.path.join(project_dir, 'Venue', 'Model')
        if not os.path.exists(model_dir):
            self.report({'ERROR'}, 'Venue/Model directory not found!')
            return {'CANCELLED'}

        glb_files = [f for f in os.listdir(model_dir) if f.endswith('.glb')]
        if not glb_files:
            self.report({'ERROR'}, 'No .glb file found in Venue/Model!')
            return {'CANCELLED'}

        # Use the first .glb file found
        venue_path = os.path.join(model_dir, glb_files[0])

        # Import the GLTF file and group all objects
        bpy.ops.import_scene.gltf(filepath=venue_path)

        # Only clean up existing venue if import was successful
        if bpy.context.selected_objects:
            self._remove_existing_venue(context)

        # Create a new empty object as parent
        parent_obj = bpy.data.objects.new('Venue', None)
        bpy.context.scene.collection.objects.link(parent_obj)
        
        # Parent all imported objects to the new parent
        imported_objects = bpy.context.selected_objects
        for obj in imported_objects:
            obj.parent = parent_obj
        
        # Set the venue object to the parent
        venue_obj = parent_obj

        # Track venue-related assets
        venue_meshes = set()
        venue_materials = set()

        for obj in imported_objects:
            if obj.data:
                venue_meshes.add(obj.data.name)
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    venue_materials.add(mat_slot.material.name)

        # Store in scene properties
        context.scene['venue_meshes'] = list(venue_meshes)
        context.scene['venue_materials'] = list(venue_materials)

        if 'rotation' in manifest:
            # Convert three.js rotations to Blender's coordinate system
            rot = manifest['rotation']
            self.report({'INFO'}, f'Applying rotation: X={rot["x"]}°, Y={rot["y"]}°, Z={rot["z"]}°')
            venue_obj.rotation_euler.x = math.radians(rot['x'] - 90)  # X -> X - 90
            venue_obj.rotation_euler.y = math.radians(rot['z'])  # Z -> Y
            venue_obj.rotation_euler.z = math.radians(rot['y'])  # Y -> Z
            self.report({'INFO'}, f'Final rotation: {venue_obj.rotation_euler}')

#        if 'center' in manifest:
#            center = manifest['center']
#            self.report({'INFO'}, f'Adjusting center: X={center["x"]}, Y={center["y"]}, Z={center["z"]}')
#            venue_obj.location.x += center['x']
#            venue_obj.location.y += center['y']
#            venue_obj.location.z += center['z']
#            self.report({'INFO'}, f'New center position: {venue_obj.location}')

        if 'position' in manifest:
            # Apply translation values to the object's current location
            pos = manifest['position']
            self.report({'INFO'}, f'Applying translation: X={pos["x"]}, Y={pos["y"]}, Z={pos["z"]}')
            venue_obj.location.x = venue_obj.location.x + pos['x']
            venue_obj.location.y = venue_obj.location.y + pos['y']
            venue_obj.location.z = venue_obj.location.z + pos['z']
            self.report({'INFO'}, f'New position after translation: {venue_obj.location}')

        if 'scale' in manifest:
            scale = float(manifest['scale'])
            self.report({'INFO'}, f'Applying scale: X={scale}, Y={scale}, Z={scale}')
            venue_obj.scale.x = scale
            venue_obj.scale.y = scale
            venue_obj.scale.z = scale
            self.report({'INFO'}, f'New scale: {venue_obj.scale}')

        self.report({'INFO'}, 'Venue loaded successfully!')
        return {'FINISHED'}
