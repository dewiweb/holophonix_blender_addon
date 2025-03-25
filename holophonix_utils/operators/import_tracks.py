import bpy
import os
import json
import numpy
from math import radians
from ..utils.math_utils import sph2cart
from ..utils.file_properties import FileProperties
from ..utils.track_handler_proxy import get_manager

class SNA_OT_Import_Tracks(bpy.types.Operator):
    bl_idname = 'sna.import_tracks'
    bl_label = 'Import Tracks'
    bl_options = {'REGISTER', 'UNDO'}

    def _create_handlers_for_track(self, context, track, settings):
        """Create handlers for a track and initialize proxy"""
        # Create position handlers (x, y, z)
        axes = ['x', 'y', 'z']
        for i, axis in enumerate(axes):
            self._create_position_handler(context, track, i, axis)
        
        # Create name handler
        self._create_name_handler(context, track)
        
        # Create color handler
        self._create_color_handler(context, track)
        
        # Initialize proxy if manager is available
        manager = get_manager()
        if manager:
            # Get or create proxy using track name as key
            track_key = f"track.{track.name}"
            proxy = manager.get_proxy(track_key)
            if proxy:
                # Update proxy settings
                proxy.set_attr("position_enabled", settings.position_enabled)
                proxy.set_attr("position_direction", settings.position_direction)
                proxy.set_attr("name_enabled", settings.name_enabled)
                proxy.set_attr("name_direction", settings.name_direction)
                proxy.set_attr("color_enabled", settings.color_enabled)
                proxy.set_attr("color_direction", settings.color_direction)
        
        return True
    
    def _create_position_handler(self, context, obj, index, axis):
        """Create position handler for a track"""
        # Extract track ID from object name
        parts = obj.name.split('.')
        if len(parts) < 2:
            return
        
        track_id = parts[1]
        
        # Check if handler already exists
        osc_address = f"/track/{track_id}/{axis}"
        if any(key.osc_address == osc_address for key in context.scene.NodeOSC_keys):
            return
        
        item = context.scene.NodeOSC_keys.add()
        item.name = f"track.{obj.name}.{axis}"
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].matrix_world.translation[{index}]"
        item.osc_type = "f"
        item.osc_index = "()"
        item.osc_direction = "OUTPUT"
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = True
        item.ui_expanded = False
    
    def _create_name_handler(self, context, obj):
        """Create name handler for a track"""
        # Extract track ID from object name
        parts = obj.name.split('.')
        if len(parts) < 2:
            return
        
        track_id = parts[1]
        
        # Check if handler already exists
        osc_address = f"/track/{track_id}/name"
        if any(key.osc_address == osc_address for key in context.scene.NodeOSC_keys):
            return
        
        item = context.scene.NodeOSC_keys.add()
        item.name = f"track.{obj.name}.name"
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].name"
        item.osc_type = "s"
        item.osc_index = "(0)"
        item.osc_direction = "INPUT"
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = True
        item.ui_expanded = False
    
    def _create_color_handler(self, context, obj):
        """Create color handler for a track"""
        # Extract track ID from object name
        parts = obj.name.split('.')
        if len(parts) < 2:
            return
        
        track_id = parts[1]
        
        # Check if handler already exists
        osc_address = f"/track/{track_id}/color"
        if any(key.osc_address == osc_address for key in context.scene.NodeOSC_keys):
            return
        
        item = context.scene.NodeOSC_keys.add()
        item.name = f"track.{obj.name}.color"
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].color"
        item.osc_type = "f"
        item.osc_index = "(0,1,2,3)"
        item.osc_direction = "INPUT"
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = True
        item.ui_expanded = False
    
    def execute(self, context):
        props = context.scene.file_properties
        print(f"Selected .hol file: {props.holophonix_hol_files}")  # Debug print
        
        if not props.holophonix_hol_files or not props.project_path:
            self.report({'ERROR'}, 'No valid .hol file selected')
            return {'CANCELLED'}
        
        preset_file_path = os.path.join(props.project_path, 'Presets', props.holophonix_hol_files)
        print(f"Selected .hol file path: {preset_file_path}")  # Debug print
        if not os.path.exists(preset_file_path):
            self.report({'ERROR'}, 'Selected .hol file does not exist')
            return {'CANCELLED'}

        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'amadeus.blend')

        # Create or get Tracks collection
        tracks_collection = bpy.data.collections.get('Tracks')
        if not tracks_collection:
            tracks_collection = bpy.data.collections.new('Tracks')
            bpy.context.scene.collection.children.link(tracks_collection)

        # Track used meshes and materials
        track_meshes = set()
        track_materials = set()
        tracks_to_delete = []

        # Find all track objects
        for obj in bpy.context.scene.objects:
            if "track" in obj.name:
                print(f"Found track object: {obj.name}")
                # Collect used meshes and materials
                if obj.data:
                    track_meshes.add(obj.data.name)
                for mat_slot in obj.material_slots:
                    if mat_slot.material:
                        track_materials.add(mat_slot.material.name)
                tracks_to_delete.append(obj)
            else:
                print(f"Not a track object: {obj.name}")

        # Delete track objects directly
        for obj in tracks_to_delete:
            print(f"Deleting track object: {obj.name}")
            
            # Clean up related NodeOSC_keys
            if hasattr(bpy.context.scene, 'NodeOSC_keys'):
                keys_to_remove = [
                    key for key in bpy.context.scene.NodeOSC_keys
                    if obj.name in key.data_path
                ]
                for key in reversed(keys_to_remove):
                    index = bpy.context.scene.NodeOSC_keys.find(key.name)
                    if index >= 0:
                        bpy.context.scene.NodeOSC_keys.remove(index)
                        print(f"Removed NodeOSC_key for track {obj.name}")
            
            # Clean up related proxies in TrackHandlerManager
            from ..utils.track_handler_proxy import get_manager
            manager = get_manager()
            if manager:
                # Try different proxy key formats
                proxy_keys = [
                    f"track.{obj.name}",  # Main format
                    obj.name,              # Alternative format
                    f"{obj.name}"          # String format
                ]
                
                for proxy_key in proxy_keys:
                    if manager.remove_proxy(proxy_key):
                        print(f"Removed proxy for track {obj.name} with key {proxy_key}")
            
            # Delete the track object
            bpy.data.objects.remove(obj, do_unlink=True)

        # Clean up track meshes and materials
        for mesh_name in track_meshes:
            if mesh_name in bpy.data.meshes:
                bpy.data.meshes.remove(bpy.data.meshes[mesh_name])
        for mat_name in track_materials:
            if mat_name in bpy.data.materials:
                bpy.data.materials.remove(bpy.data.materials[mat_name])

        with open(preset_file_path) as f:
            hol_file_content = json.load(f)
            audio_engine_dict = hol_file_content['ae']
            hol_dict = hol_file_content['hol']
            hol_keys = list(hol_dict.keys())

            for i in range(1, 128):
                trk_name = ''
                trk_cart_coord = [0, 0, 0]
                trk_sph_coord = [0, 0, 0]
                trk_glb = "Dodecahedron"
                trk_color = [0, 0, 0, 0]

                digits = len(str(i))
                trk_number = f'{i:03d}'
                track = '/track/'
                params = ['/view3D/file3D','/color', '/azim', '/elev', '/dist', '/name']

                for param in params:
                    tuple = ''.join((track, str(i), param))
                    if param == '/view3D/file3D':
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            end_loc = len(p_tuple)-5
                            trk_glb = str(p_tuple[0])[18:end_loc]
                    elif param == '/color':
                        color_path = [path for path in audio_engine_dict if tuple in path]
                        if color_path:
                            color_path = color_path[0].split()
                            # Ensure we have enough values
                            if len(color_path) >= 5:  # Format should be like: /track/1/color 0.5 0.2 0.8 1.0
                                # Extract RGB and Alpha values
                                try:
                                    for j in range(0,4):
                                        trk_color[j] = float(color_path[j+1])
                                    print(f"Extracted color: {trk_color}")
                                except (ValueError, IndexError) as e:
                                    print(f"Error parsing color values: {e}")
                                    # Default to a visible color on error
                                    trk_color = [0.8, 0.2, 0.2, 1.0]
                            else:
                                print(f"Color data format unexpected: {color_path}")
                                # Default to a visible color if format is unexpected
                                trk_color = [0.2, 0.8, 0.2, 1.0]
                    elif param == '/azim':
                        azim_path = [path for path in audio_engine_dict if tuple in path]
                        if azim_path:
                            trk_sph_coord[0] = float(azim_path[0].split()[1])
                    elif param == '/elev':
                        elev_path = [path for path in audio_engine_dict if tuple in path]
                        if elev_path:
                            trk_sph_coord[1] = float(elev_path[0].split()[1])
                    elif param == '/dist':
                        dist_path = [path for path in audio_engine_dict if tuple in path]
                        if dist_path:
                            trk_sph_coord[2] = float(dist_path[0].split()[1])
                            trk_cart_coord = sph2cart(float(trk_sph_coord[1]), float(trk_sph_coord[0]), float(trk_sph_coord[2]))
                    elif param == '/name':
                        name_path = [path for path in audio_engine_dict if tuple in path]
                        if name_path:
                            trk_name = name_path[0].split('"')[1]

                if trk_name:
                    # Append track model
                    result = bpy.ops.wm.append(
                        filepath=file_path,
                        directory=os.path.join(file_path, 'Object'),
                        filename=trk_glb
                    )
                    if result == {'FINISHED'}:
                        for trk in bpy.context.selected_objects:
                            # Unlink from all collections
                            for col in trk.users_collection:
                                col.objects.unlink(trk)
                            # Link to Tracks collection
                            tracks_collection.objects.link(trk)

                            trk.name = track + "." + trk_number + "." + trk_name
                            trk.name = trk.name.replace('/', '')
                            trk.data.name = trk.name
                            for k in range(0, 3):
                                trk.location[k] = trk_cart_coord[k]
                            
                            # Create a new material and apply the color
                            trk_material = bpy.data.materials.new(name = trk.name+'.mat')
                            trk.data.materials.clear()
                            trk.data.materials.append(trk_material)
                            
                            # Debug output for color values
                            print(f"Track {trk.name} - Color before setting: {trk_color}")
                            
                            # Make sure the alpha is 1.0 if it's not specified
                            if len(trk_color) == 4 and trk_color[3] == 0:
                                trk_color[3] = 1.0
                            
                            # Ensure color is properly formatted for Blender
                            if all(c == 0 for c in trk_color[:3]):
                                # Default color if no color is specified
                                trk_color = [0.8, 0.8, 0.8, 1.0]
                            
                            print(f"Track {trk.name} - Color after adjustment: {trk_color}")
                            
                            # Apply the color to the material
                            bpy.data.materials[trk.name+'.mat'].diffuse_color = trk_color

        self.report({'INFO'}, 'Tracks imported successfully!')
        
        #create tracks handlers
        bpy.ops.sna.export_create_handlers()
        
        return {'FINISHED'}
