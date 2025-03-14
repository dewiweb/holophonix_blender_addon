import bpy
import os
import json
import numpy
from math import radians
from ..utils.math_utils import sph2cart

class SNA_OT_Import_Tracks(bpy.types.Operator):
    bl_idname = 'sna.import_tracks'
    bl_label = 'Import Tracks'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.holophonix_utils
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

        # Clean up existing tracks
        for obj in bpy.context.scene.objects:
            if "track" in obj.name:
                bpy.data.objects[obj.name].select_set(True)
                bpy.ops.object.delete()

        # Clean up unused meshes and materials
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

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
                            for j in range(0,4):
                                trk_color[j] = float(color_path[j+1])
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
                            trk.name = track + "." + trk_number + "." + trk_name
                            trk.name = trk.name.replace('/', '')
                            trk.data.name = trk.name
                            for k in range(0, 3):
                                trk.location[k] = trk_cart_coord[k]
                            trk_material = bpy.data.materials.new(name = trk.name+'.mat')
                            trk.data.materials.clear()
                            trk.data.materials.append(trk_material)
                            bpy.data.materials[trk.name+'.mat'].diffuse_color = trk_color

        self.report({'INFO'}, 'Tracks imported successfully!')
        return {'FINISHED'}
