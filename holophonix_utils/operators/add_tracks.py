import bpy
from bpy_extras.io_utils import ImportHelper
import os
import json
import numpy
from math import radians
from ..utils.math_utils import cart2sph, sph2cart

class SNA_OT_Add_Tracks_73B0D(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.add_tracks_73b0d"
    bl_label = "Add Tracks"
    bl_description = "replace actual tracks by those in imported hol preset file"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.hol', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        preset_file_path = self.filepath
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'amadeus.blend')
        Variable = None
        import json
        import numpy

        for obj in bpy.context.scene.objects:
            if "track" in obj.name:
                bpy.data.objects[obj.name].select_set(True)
                print(obj.name, ' deleted')
                bpy.ops.object.delete()
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)
        with open(preset_file_path) as f:
                hol_file_content = json.load(f)
                audio_engine_dict = hol_file_content['ae']
                print("ae",audio_engine_dict)
                hol_dict = hol_file_content['hol']
                hol_keys = list(hol_dict.keys())
        for i in range(1,128):
            global trk_name
            global trk_cart_coord
            global trk_sph_coord
            global trk_glb
            global trk_color
            trk_name =''
            trk_cart_coord = [0,0,0]
            inner_path = 'Object'
            trk_sph_coord = [0,0,0]
            trk_color = [0,0,0,0]
            trk_glb = "Dodecahedron"
            digits = len(str(i))
            if digits == 1:
                trk_number = '00'+ str(i)
            elif digits == 2:
                trk_number = '0'+ str(i)
            else:
                trk_number = str(i)
            track ='/track/'
            params = ['/view3D/file3D','/color','/azim','/elev','/dist',"/name"]
            for param in params:
                tuple = (track,str(i),param)
                tuple = ''.join(tuple)
                if param == params[0]:
                    if tuple in hol_keys:
                        p_tuple = hol_dict[tuple]
                        end_loc = len(p_tuple)-5
                        trk_glb = str(p_tuple[0])[18:end_loc]
                        print(i,"j'ai un glb",trk_glb)
                elif param == params[1]:
                    col_path = [path for path in audio_engine_dict if tuple in path]
                    if col_path != []:
                        print(i,"j'ai une couleur",col_path)
                        col_path = col_path[0].split()
                        for j in range(0,4):
                            trk_color[j] = float(col_path[j+1])
                elif param == params[2]:
                    azim_path = [path for path in audio_engine_dict if tuple in path]
                    if azim_path != []:
                        azim_path = azim_path[0].split()
                        trk_sph_coord[0] = float(azim_path[1])
                        print(i,"j'ai une azim",azim_path)
                elif param == params[3]:
                    elev_path = [path for path in audio_engine_dict if tuple in path]
                    if elev_path != []:
                        elev_path = elev_path[0].split()
                        trk_sph_coord[1] = float(elev_path[1])
                        print(i,"j'ai une elev",elev_path)
                elif param == params[4]:
                    dist_path = [path for path in audio_engine_dict if tuple in path]
                    if dist_path != []:
                        dist_path = dist_path[0].split()
                        trk_sph_coord[2] = float(dist_path[1])
                        trk_cart_coord = sph2cart(trk_sph_coord[1], trk_sph_coord[0], trk_sph_coord[2])
                        print(i,"j'ai une dist",dist_path)
                elif param == params[5]:
                    name_path = [path for path in audio_engine_dict if tuple in path]
                    if name_path != []:
                        name_path = name_path[0].split('"')
                        trk_name = name_path[1]
                        print(i,"j'ai une name",name_path)
                if trk_name != "":
                    DEFAULT_GLB = "Dodecahedron"  # Define the default model name
                    # Check if model exists in blend file
                    with bpy.data.libraries.load(file_path) as (data_from, data_to):
                        if trk_glb not in data_from.objects:
                            print(f'Model {trk_glb} not found in {file_path}')
                            print(f'Attempting to append default model {DEFAULT_GLB}')
                            trk_glb = DEFAULT_GLB
                    print(f'Attempting to append {trk_glb} from {file_path}')
                    result = bpy.ops.wm.append(
                        filepath=file_path,
                        directory=os.path.join(file_path, inner_path),
                        filename=trk_glb
                    )
                    print(f'Append result: {result}')
                    if result != {'FINISHED'}:
                        print(f'Failed to append object {trk_glb}')
                        continue
                    print(i,'track',trk_number,'created as',trk_name)
                    for trk in bpy.context.selected_objects:
                        trk.name = track +"."+ trk_number +"."+ trk_name
                        trk.name = (trk.name).replace('/','')
                        trk.data.name = trk.name
                        for k in range(0,3):
                            trk.location[k] = trk_cart_coord[k]
                        trk_material = bpy.data.materials.new(name = trk.name+'.mat')
                        trk.data.materials.clear()
                        trk.data.materials.append(trk_material)
                        bpy.data.materials[trk.name+'.mat'].diffuse_color = trk_color
        return {"FINISHED"}
