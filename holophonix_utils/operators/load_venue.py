import bpy
import json
import os
import math

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

        # Calculate scale factor from widthMeters
        scale_factor = 1.0
        if 'widthMeters' in manifest:
            try:
                # Get the expected width from the manifest
                expected_width = manifest['widthMeters']
                
                # Import the GLTF file with scale factor
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
                
                # Create a new empty object as parent
                parent_obj = bpy.data.objects.new('Venue', None)
                bpy.context.scene.collection.objects.link(parent_obj)
                
                # Parent all imported objects to the new parent
                imported_objects = bpy.context.selected_objects
                for obj in imported_objects:
                    obj.parent = parent_obj
                
                # Set the venue object to the parent
                venue_obj = parent_obj

                # Calculate scale factor to match widthMeters
                bbox = venue_obj.bound_box
                try:
                    # Get the current width of the imported model
                    current_width = max(v[0] for v in bbox) - min(v[0] for v in bbox)
                    
                    if current_width == 0:
                        self.report({'WARNING'}, 'Venue has zero width, using default scale')
                        scale_factor = 1.0
                    else:
                        # Calculate scale factor to match the desired width
                        scale_factor = expected_width / current_width
                        self.report({'INFO'}, f'Scaling venue to match width of {expected_width} meters')
                    
                    # Apply uniform scale to maintain proportions
                    venue_obj.scale = (scale_factor, scale_factor, scale_factor)
                except Exception as e:
                    self.report({'ERROR'}, f'Failed to calculate venue scale: {str(e)}')
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'}, f'Failed to import venue: {str(e)}')
                return {'CANCELLED'}
        if 'widthMeters' in manifest:
            # Scale the venue based on widthMeters
            bbox = venue_obj.bound_box
            try:
                width = max(v[0] for v in bbox) - min(v[0] for v in bbox)
                if width == 0:
                    self.report({'WARNING'}, 'Venue has zero width, using default scale')
                    scale_factor = 1.0
                else:
                    scale_factor = manifest['widthMeters'] / width
                venue_obj.scale = (scale_factor, scale_factor, scale_factor)
            except Exception as e:
                self.report({'ERROR'}, f'Failed to calculate venue scale: {str(e)}')
                return {'CANCELLED'}

        if 'center' in manifest:
            # Convert three.js (Y-up) to Blender (Z-up) coordinates
            center = manifest['center']
            self.report({'INFO'}, f'Adjusting center: X={center["x"]}, Y={center["y"]}, Z={center["z"]}')
            venue_obj.location.x = center['x'] * venue_obj.scale.x
            venue_obj.location.z = center['y'] * venue_obj.scale.z  # Y -> Z
            venue_obj.location.y = -center['z'] * venue_obj.scale.y  # Z -> -Y
            self.report({'INFO'}, f'New center position: {venue_obj.location}')

        if 'position' in manifest:
            # Convert three.js (Y-up) to Blender (Z-up) coordinates
            pos = manifest['position']
            self.report({'INFO'}, f'Setting position: X={pos["x"]}, Y={pos["y"]}, Z={pos["z"]}')
            venue_obj.location.x = pos['x'] * venue_obj.scale.x
            venue_obj.location.z = pos['y'] * venue_obj.scale.z  # Y -> Z
            venue_obj.location.y = -pos['z'] * venue_obj.scale.y  # Z -> -Y
            self.report({'INFO'}, f'Final position: {venue_obj.location}')

        if 'rotation' in manifest:
            # TODO: Revisit coordinate system conversion
            # Convert three.js rotations to Blender's coordinate system
            rot = manifest['rotation']
            self.report({'INFO'}, f'Applying rotation: X={rot["x"]}°, Y={rot["y"]}°, Z={rot["z"]}°')
            venue_obj.rotation_euler.x = math.radians(rot['x'])
            venue_obj.rotation_euler.z = math.radians(-rot['y'])  # Y -> -Z
            venue_obj.rotation_euler.y = math.radians(rot['z'])
            self.report({'INFO'}, f'Final rotation: {venue_obj.rotation_euler}')

        self.report({'INFO'}, 'Venue loaded successfully!')
        return {'FINISHED'}
