import bpy
from bpy_extras.io_utils import ImportHelper
import os
import json
import math
from numpy import radians
import numpy

class SNA_OT_Add_Speakers_994C8(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.add_speakers_994c8"
    bl_label = "Add_Speakers"
    bl_description = "replace actual speakers by those in imported hol preset file"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.hol', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        preset_file_path = self.filepath
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'amadeus.blend')
        Variable = None

        def cart2sph(z, y, x):
            """Convert from cartesian coordinates (x,y,z) to spherical (elevation,
            azimuth, radius). Output is in degrees.
            usage:
                array3xN[el,az,rad] = cart2sph(array3xN[x,y,z])
                OR
                elevation, azimuth, radius = cart2sph(x,y,z)
                If working in DKL space, z = Luminance, y = S and x = LM
            """
            width = len(z)
            elevation = numpy.empty([width, width])
            radius = numpy.empty([width, width])
            azimuth = numpy.empty([width, width])
            radius = numpy.sqrt(x**2 + y**2 + z**2)
            azimuth = numpy.arctan2(y, x)
            # Calculating the elevation from x,y up
            elevation = numpy.arctan2(z, numpy.sqrt(x**2 + y**2))
            # convert azimuth and elevation angles into degrees
            azimuth *= 180.0 / numpy.pi
            elevation *= 180.0 / numpy.pi
            sphere = numpy.array([elevation, azimuth, radius])
            sphere = numpy.rollaxis(sphere, 0, 3)
            return sphere

        def sph2cart(*args):
            """Convert from spherical coordinates (elevation, azimuth, radius)
            to cartesian (x,y,z).
            usage:
                array3xN[x,y,z] = sph2cart(array3xN[el,az,rad])
                OR
                x,y,z = sph2cart(elev, azim, radius)
            """
            if len(args) == 1:  # received an Nx3 array
                elev = args[0][0, :]
                azim = args[0][1, :]
                radius = args[0][2, :]
                returnAsArray = True
            elif len(args) == 3:
                elev = args[0]
                azim = args[1]
                radius = args[2]
                returnAsArray = False
            z = radius * numpy.sin(radians(elev))
            x = radius * numpy.cos(radians(elev)) * numpy.cos(radians(azim))
            y = radius * numpy.cos(radians(elev)) * numpy.sin(radians(azim))
            if returnAsArray:
                return numpy.asarray([x, y, z])
            else:
                return y, x, z

        for obj in bpy.context.scene.objects:
            if "Empty" in obj.name:
                bpy.data.objects[obj.name].select_set(True)
                print(obj.name, ' deleted')
                bpy.ops.object.delete()
            elif "speaker" in obj.name:
                bpy.data.objects[obj.name].select_set(True)
                print(obj.name, ' deleted')
                bpy.ops.object.delete()
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        bpy.ops.object.empty_add(type='PLAIN_AXES')

        with open(preset_file_path) as f:
            preset_content = json.load(f)
            hol_dict = preset_content['hol']
            hol_keys = list(hol_dict.keys())

        for i in range(1,512):
            global spk_cart_coord
            global spk_sph_coord
            global spk_glb
            global spk_color
            global spk_auto_orient
            spk_sph_coord = [0,0,0]
            spk_cart_coord = [0,0,0]
            inner_path = 'Object'
            spk_glb = "Default 3D"
            spk_color = [0,0,0,0]
            spk_auto_orient = False
            spk_pan = 0
            spk_tilt = 0
            spk_roll = False
            speaker = '/speaker/'
            params = ['/color','/azim','/elev','/dist','/view3D/file3D','/view3D/roll90deg','/view3D/pan','/view3D/tilt','/view3D/autoOrientation']
            spk_rotation_mode = 'XYZ'
            digits = len(str(i))
            if digits == 1:
                spk_number = '00'+ str(i)
            elif digits == 2:
                spk_number = '0'+ str(i)
            else:
                spk_number = str(i)
            prefix = (speaker,str(i))
            prefix = ''.join(prefix)
            spk_exists = [spk for spk in  hol_keys if str(prefix) in spk]
            print("spk_exists",spk_exists)
            if spk_exists != []:
                for param in params:
                    tuple = (speaker,str(i),param)
                    tuple = ''.join(tuple)
                    if param == params[0]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_color = p_tuple
                    elif param == params[1]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_azim = p_tuple[0]
                            spk_sph_coord[0] = float(spk_azim)
                    elif param == params[2]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_elev = p_tuple[0]
                            spk_sph_coord[1] = float(spk_elev)
                    elif param == params[3]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_dist = p_tuple[0]
                            spk_sph_coord[2] = float(spk_dist)
                            spk_cart_coord = sph2cart(float(spk_sph_coord[1]),float(spk_sph_coord[0]),float(spk_sph_coord[2]))
                    elif param == params[4]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            end_loc = len(p_tuple)-5
                            spk_glb = str(p_tuple[0])[18:end_loc]
                            print(spk_glb)
                    elif param == params[5]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_roll = p_tuple[0]
                    elif param == params[6]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_pan = p_tuple[0]
                    elif param == params[7]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_tilt = p_tuple[0]
                    elif param == params[8]:
                        if tuple in hol_keys:
                            p_tuple = hol_dict[tuple]
                            spk_auto_orient = p_tuple[0]

                bpy.ops.wm.append(
                    directory=os.path.join(file_path, inner_path),
                    filename=spk_glb
                    )
                for spk in bpy.context.selected_objects:
                    spk.name = speaker +"."+ spk_number +"."+ spk_glb
                    spk.name = (spk.name).replace('/','')
                    spk.data.name = spk.name
                    for k in range(0,3):
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
                        tracking.target = bpy.context.scene.objects.get("Empty")
                        bpy.ops.object.visual_transform_apply()
                        spk.constraints.remove(tracking)
                print(str(spk.name), 'CREATED')
        bpy.ops.object.select_all(action='DESELECT')
        for empty in bpy.context.scene.objects:
            if "Empty" in empty.name:
                bpy.data.objects[empty.name].select_set(True)
                print(empty.name, ' deleted')
                bpy.ops.object.delete()
        return {"FINISHED"}
