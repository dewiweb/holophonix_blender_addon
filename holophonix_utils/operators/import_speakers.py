import bpy
import os
import json
import numpy
from math import radians
from ..utils.math_utils import sph2cart

class SNA_OT_Import_Speakers(bpy.types.Operator):
    bl_idname = 'sna.import_speakers'
    bl_label = 'Import Speakers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.holophonix_utils
        
        if not props.holophonix_hol_files or not props.project_path:
            self.report({'ERROR'}, 'No valid .hol file selected')
            return {'CANCELLED'}
        
        preset_file_path = os.path.join(props.project_path, 'Presets', props.holophonix_hol_files)
        if not os.path.exists(preset_file_path):
            self.report({'ERROR'}, 'Selected .hol file does not exist')
            return {'CANCELLED'}

        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'amadeus.blend')

        # Clean up existing speakers
        for obj in bpy.context.scene.objects:
            if "speaker" in obj.name:
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
            hol_dict = hol_file_content['hol']
            hol_keys = list(hol_dict.keys())

            for i in range(1, 512):
                spk_sph_coord = [0, 0, 0]
                spk_cart_coord = [0, 0, 0]
                spk_glb = "Default 3D"
                spk_color = [0, 0, 0, 0]
                spk_auto_orient = False
                spk_pan = 0
                spk_tilt = 0
                spk_roll = False

                speaker = '/speaker/'
                params = ['/color','/azim','/elev','/dist','/view3D/file3D','/view3D/roll90deg','/view3D/pan','/view3D/tilt','/view3D/autoOrientation']
                prefix = speaker + str(i)

                if any(prefix in key for key in hol_keys):
                    for param in params:
                        tuple = prefix + param
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            if param == '/color':
                                spk_color = p_tuple
                            elif param == '/azim':
                                spk_sph_coord[0] = float(p_tuple[0])
                            elif param == '/elev':
                                spk_sph_coord[1] = float(p_tuple[0])
                            elif param == '/dist':
                                spk_sph_coord[2] = float(p_tuple[0])
                                spk_cart_coord = sph2cart(float(spk_sph_coord[1]), float(spk_sph_coord[0]), float(spk_sph_coord[2]))
                            elif param == '/view3D/file3D':
                                end_loc = len(p_tuple)-5
                                spk_glb = str(p_tuple[0])[18:end_loc]
                            elif param == '/view3D/roll90deg':
                                spk_roll = p_tuple[0]
                            elif param == '/view3D/pan':
                                spk_pan = p_tuple[0]
                            elif param == '/view3D/tilt':
                                spk_tilt = p_tuple[0]
                            elif param == '/view3D/autoOrientation':
                                spk_auto_orient = p_tuple[0]

                    # Append speaker model
                    result = bpy.ops.wm.append(
                        filepath=file_path,
                        directory=os.path.join(file_path, 'Object'),
                        filename=spk_glb
                    )

                    if result == {'FINISHED'}:
                        for spk in bpy.context.selected_objects:
                            spk.name = speaker + str(i) + "." + spk_glb
                            spk.name = spk.name.replace('/', '')
                            spk.data.name = spk.name
                            for k in range(0, 3):
                                spk.location[k] = spk_cart_coord[k]

                            spk_material = bpy.data.materials.new(name = spk.name+'.mat')
                            spk.data.materials.clear()
                            spk.data.materials.append(spk_material)
                            bpy.data.materials[spk.name+'.mat'].diffuse_color = spk_color

                            if spk_auto_orient == False:
                                if spk_roll == True:
                                    spk.rotation_euler[2] = radians(90)
                                    spk.rotation_euler[0] = radians(float(spk_pan))
                                    if float(spk_pan) > 90 :
                                        spk.rotation_euler[1] = radians(float(spk_tilt))
                                    else:
                                        spk.rotation_euler[1] = radians(-float(spk_tilt))
                                else:
                                    spk.rotation_euler[2] = radians(0)
                                    spk.rotation_euler[1] = radians(-float(spk_pan))
                                    spk.rotation_euler[0] = radians(float(spk_tilt))
                            else:
                                tracking = spk.constraints.new(type='TRACK_TO')

        self.report({'INFO'}, 'Speakers imported successfully!')
        return {'FINISHED'}
