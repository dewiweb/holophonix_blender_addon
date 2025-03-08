# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Holophonix_Utils",
    "author" : "Dewiweb", 
    "description" : "",
    "blender" : (4, 3, 0),
    "version" : (1, 0, 8),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper
import math
from numpy import radians
import sys
import numpy
import os
import logging
import pickle

# Configure logging
logger = logging.getLogger(__name__)

def load_script(script_name):
    """Load a Python script from the addon's assets directory."""
    script_path = os.path.join(os.path.dirname(__file__), 'assets', script_name)
    if script_name not in bpy.data.texts:
        with open(script_path, 'r') as f:
            bpy.data.texts.new(script_name).from_string(f.read())


addon_keymaps = {}
_icons = None


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


def plugin_exists(self,context,touched_socket):
    if True is True:
        return True
    else:
        return False


def plugin_folder(self,context,touched_socket):
    if 'animation_nodes' != '':
        return 'animation_nodes'
    else:
        return False


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


class SNA_OT_Add_Sources_73B0D(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.add_sources_73b0d"
    bl_label = "Add_Sources"
    bl_description = "replace actual tracks by those in imported hol preset file"
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.hol', options={'HIDDEN'} )

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        preset_file_path = self.filepath
        file_path = os.path.join(os.path.dirname(__file__), 'assets', 'amadeus.blend')
        Variable = None
        import json
        import numpy

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
                return numpy.asarray([y, x, z])
            else:
                return y, x, z
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
                        trk_cart_coord = sph2cart(float(trk_sph_coord[1]),float(trk_sph_coord[0]),float(trk_sph_coord[2]))
                        print(i,"j'ai une dist",dist_path)
                elif param == params[5]:
                    name_path = [path for path in audio_engine_dict if tuple in path]
                    if name_path != []:
                        name_path = name_path[0].split('"')
                        trk_name = name_path[1]
                        print(i,"j'ai une name",name_path)
                if trk_name != "":
                    bpy.ops.wm.append(
                        directory=os.path.join(file_path, inner_path),
                        filename=trk_glb
                        )
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
        """
                if "/track/" in audio_engine_dict[i]:
                    if '"' in audio_engine_dict[i]:
                        separate = str(audio_engine_dict[i]).split('"')
            #            print('separate"',separate)
                    else:
                        separate = str(audio_engine_dict[i]).split()
            #            print("separate ",separate)
                    path = separate[0]
                    path_details = path.split('/')
                    if int(len(path_details)) > 1:
                        if path_details[2] != "indices":
                            trk_number = path_details[2]
                            if len(trk_number) == 1:
                                trk_number = '00'+trk_number
                            elif len(trk_number) == 2:
                                trk_number = '0'+trk_number
                            else:
                                trk_number = trk_number
                            if int(len(path_details)) == 4:
                                path_key = path_details[3]
                                if "name" in path_key:
                                    print("that's name")
                                    trk_name = str(separate[1])
                                elif "color" in path_key:
                                    del separate[0]
                                    print("col_idx",separate)
                                    trk_color = []
                                    for item in separate:
                                        trk_color.append(float(item))
                                elif "azim" in path_key:
            #                        print("azim",float(separate[1]))
                                    trk_sph_coord[0] = float(separate[1])
                                elif "elev" in path_key:
            #                        print("elev",float(separate[1]))
                                    trk_sph_coord[1] = float(separate[1])
                                elif "dist" in path_key:
            #                        print("dist",float(separate[1]))
                                    trk_sph_coord[2] = float(separate[1])
            #                        print("trk_sph_coord",trk_sph_coord)
                                    trk_cart_coord = sph2cart(float(trk_sph_coord[1]),float(trk_sph_coord[0]),float(trk_sph_coord[2]))
            #                        print("trk_cart_coord",trk_cart_coord)
        """
        return {"FINISHED"}


class SNA_OT_Import_An_Tree_433Db(bpy.types.Operator):
    bl_idname = "sna.import_an_tree_433db"
    bl_label = "Import_AN_Tree"
    bl_description = "Import AN Tree"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        file_path = os.path.join(os.path.dirname(__file__), 'assets', 'amadeus.blend')
        Variable = None
        inner_path = 'NodeTree'
        name = 'AN Tree'
        bpy.ops.wm.append(
                    directory=os.path.join(file_path, inner_path),
                    filename=name
                    ) 
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Sources_Exporter_34F69(bpy.types.Operator, ExportHelper):
    bl_idname = "sna.sources_exporter_34f69"
    bl_label = "Sources_Exporter"
    bl_description = ""
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
        file_path = os.path.join(os.path.dirname(__file__), 'assets', 'amadeus.blend')
        Variable = None
        import json
        import math
        from numpy import radians
        """
        coordinates conversion
        """

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
        """
        delete old speakers 
        """    
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
        """
        Create an Empty Plain Axes Object as Target for auto-orientation
        """
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        """
        read .hol file 
        """
        with open(preset_file_path) as f:
            preset_content = json.load(f)
            hol_dict = preset_content['hol']
            hol_keys = list(hol_dict.keys())
        """
        search matching entries in .hol file contents 
        """
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
                """
                create spk object with matching properties 
                """ 
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


class SNA_PT_HOLOUTILS_1B113(bpy.types.Panel):
    bl_label = 'HoloUtils'
    bl_idname = 'SNA_PT_HOLOUTILS_1B113'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HoloUtils'

    def draw(self, context):
        layout = self.layout
        """props = context.scene.holophonix_utils"""
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'logo_svg_blanc.png')), scale=2.0)


class SNA_OT_AddHandlers(bpy.types.Operator):
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

class SNA_OT_Delete_Handlers_C2D71(bpy.types.Operator):
    bl_idname = "sna.delete_handlers_c2d71"
    bl_label = "delete_handlers"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        handlers = bpy.data.scenes["Scene"].NodeOSC_keys
        #print("handlers",len(handlers))
        for i in range(0,int(len(handlers))):
            bpy.ops.nodeosc.deleteitem('INVOKE_DEFAULT')
        #    print("one handler deleted")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_to_osc_pt_operations_7D1DC(self, context):
    if not (False):
        layout = self.layout
        if bool(plugin_folder("'NodeOSC'", globals(), locals())):
            op = layout.operator('sna.delete_handlers_c2d71', text='Delete all message handlers', icon_value=0, emboss=True, depress=False)


def sna_add_to_osc_pt_operations_ACA0D(self, context):
    if not (False):
        layout = self.layout
        if bool(plugin_folder("'NodeOSC'", globals(), locals())):
            op = layout.operator('sna.sources_exporter_34f69', text='Export Holo objects to OSC handlers', icon_value=702, emboss=True, depress=False)


class SNA_PT_SOURCES_11FF6(bpy.types.Panel):
    bl_label = 'Sources'
    bl_idname = 'SNA_PT_SOURCES_11FF6'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=290, scale=1.2100000381469727)

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.add_sources_73b0d', text='Import Sources  From .hol', icon_value=108, emboss=True, depress=False)


class SNA_PT_SPEAKERS_F8536(bpy.types.Panel):
    bl_label = 'Speakers'
    bl_idname = 'SNA_PT_SPEAKERS_F8536'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=244, scale=1.2100000381469727)

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.add_speakers_994c8', text='Import Speakers From .hol', icon_value=108, emboss=True, depress=False)

class SNA_PT_SPECIALHANDLERS(bpy.types.Panel):
    bl_label = 'OSC Handlers'
    bl_idname = 'SNA_PT_SPECIALHANDLERS'
    bl_space_type = 'VIEW_3D'  # The panel will appear in the 3D Viewport
    bl_region_type = 'UI'  # The panel will appear in the sidebar
    bl_context = ''  # Optional: specify the context (e.g., 'objectmode')
    bl_order = 0  # Order of the panel within its category
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'  # Parent panel ID
    bl_ui_units_x = 0  # Width of the panel in UI units

    @classmethod
    def poll(cls, context):
        # Ensure the panel is only visible under certain conditions
        return not (False)

    def draw_header(self, context):
        # Custom header with an icon
        layout = self.layout
        layout.template_icon(icon_value=244, scale=1.2100000381469727)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        holophonix_utils = scene.holophonix_utils
        props = context.scene.holophonix_utils
    
        # Check if NodeOSC is installed
        if "NodeOSC" not in context.preferences.addons:
            layout.label(text="NodeOSC addon isn't installed!", icon_value=2)
            return
    
        # Check if NodeOSC is enabled
        if not context.preferences.addons["NodeOSC"].preferences:
            layout.label(text="Enable NodeOSC addon in preferences!", icon_value=2)
            return
    
        # Check if NodeOSC_keys collection exists
        if not hasattr(context.scene, 'NodeOSC_keys'):
            layout.label(text="NodeOSC keys collection not found!", icon_value=2)
            return

        keys = context.scene.NodeOSC_keys
        if not keys:
            layout.operator("sna.add_handlers", text="Add Special Handlers", icon_value=108, emboss=True, depress=False)
            return

        handler_addresses = {"/dump", "/track/*", "/speaker/*", "/frames/str"}
        existing_addresses = {item.osc_address for item in keys}
        handlers_exist = handler_addresses.issubset(existing_addresses)

        if handlers_exist:
            # Show checkboxes if handlers exist and link them to handler states
            for item in keys:
                if item.osc_address == "/dump":
                    layout.prop(props, "enable_dump", text="Enable Dump Handler")
                    if props.enable_dump != item.enabled:
                        try:
                            item.enabled = props.enable_dump
                        except:
                            pass
                    elif item.enabled != props.enable_dump:
                        props.enable_dump = item.enabled
                elif item.osc_address == "/track/*":
                    layout.prop(props, "enable_track", text="Enable Track Handler")
                    if props.enable_track != item.enabled:
                        try:
                            item.enabled = props.enable_track
                        except:
                            pass
                    elif item.enabled != props.enable_track:
                        props.enable_track = item.enabled
                elif item.osc_address == "/speaker/*":
                    layout.prop(props, "enable_speaker", text="Enable Speaker Handler")
                    if props.enable_speaker != item.enabled:
                        try:
                            item.enabled = props.enable_speaker
                        except:
                            pass
                    elif item.enabled != props.enable_speaker:
                        props.enable_speaker = item.enabled
                elif item.osc_address == "/frames/str":
                    layout.prop(props, "enable_reaperTC", text="Enable Reaper TC Handler")
                    if props.enable_reaperTC != item.enabled:
                        try:
                            item.enabled = props.enable_reaperTC
                        except:
                            pass
                    elif item.enabled != props.enable_reaperTC:
                        props.enable_reaperTC = item.enabled
        else:
            # Show button if handlers don't exist
            layout.operator("sna.add_handlers", text="Add Special Handlers", icon_value=108, emboss=True, depress=False)

class SNA_PT_NODEOSC_SETTINGS_2B3D4(bpy.types.Panel):
    bl_label = 'NodeOSC Settings'
    bl_idname = 'SNA_PT_NODEOSC_SETTINGS_2B3D4'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (True)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=233, scale=1.2100000381469727)

    def draw(self, context):
        layout = self.layout
        op = layout.operator('nodeosc.deleteitem', text='My Button', icon_value=0, emboss=True, depress=False)


class SNA_PT_AN_SETTINGS_E1993(bpy.types.Panel):
    bl_label = 'AN Settings'
    bl_idname = 'SNA_PT_AN_SETTINGS_E1993'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 3
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        if plugin_exists("'Animation Nodes'", globals(), locals()):
            pass
        else:
            layout.label(text='Install Animation Nodes  Before', icon_value=2)
        if bool(plugin_folder("'animation_nodes'", globals(), locals())):
            pass
        else:
            layout.label(text='Enable  Animation Nodes  Before', icon_value=2)
        if (property_exists("bpy.data.node_groups", globals(), locals()) and 'AN Tree' in bpy.data.node_groups):
            layout.prop(bpy.data.node_groups['AN Tree'].nodes['Data Input.001'].inputs[0], 'value', text='View Names', icon_value=0, emboss=True)
            if (property_exists("bpy.data.node_groups", globals(), locals()) and 'AN Tree' in bpy.data.node_groups):
                layout.prop(bpy.data.node_groups['AN Tree'].nodes['Data Input'].inputs[0], 'value', text='Path to dump', icon_value=0, emboss=True)
        else:
            op = layout.operator('sna.import_an_tree_433db', text='Import AN Tree', icon_value=2, emboss=True, depress=False)


class HolophonixUtilsProperties(bpy.types.PropertyGroup):
    def update_dump(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/dump":
                    item.enabled = self.enable_dump

    def update_track(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/track/*":
                    item.enabled = self.enable_track

    def update_speaker(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/speaker/*":
                    item.enabled = self.enable_speaker

    def update_reaperTC(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/frames/str":
                    item.enabled = self.enable_reaperTC

    def update_nodeosc_handlers(self, context):
        if not hasattr(context.scene, 'NodeOSC_keys'):
            return

        props = context.scene.holophonix_utils
        for item in context.scene.NodeOSC_keys:
            if item.osc_address == "/dump" and item.enabled != props.enable_dump:
                props.enable_dump = item.enabled
            elif item.osc_address == "/track/*" and item.enabled != props.enable_track:
                props.enable_track = item.enabled
            elif item.osc_address == "/speaker/*" and item.enabled != props.enable_speaker:
                props.enable_speaker = item.enabled
            elif item.osc_address == "/frames/str" and item.enabled != props.enable_reaperTC:
                props.enable_reaperTC = item.enabled

    enable_reaperTC: bpy.props.BoolProperty(
        name="Enable ReaperTC Handler",
        description="Enable/disable the ReaperTC handler",
        default=True,
        update=update_reaperTC
    )
    enable_track: bpy.props.BoolProperty(
        name="Enable Track Handler",
        description="Enable/disable the track handler",
        default=True,
        update=update_track
    )
    enable_dump: bpy.props.BoolProperty(
        name="Enable Dump Handler",
        description="Enable/disable the dump handler",
        default=True,
        update=update_dump
    )
    enable_populate: bpy.props.BoolProperty(
        name="Enable Populate Handler",
        description="Enable/disable the populate handler",
        default=True
    )
    enable_speaker: bpy.props.BoolProperty(  # Add this property
        name="Enable Speaker Handler",
        description="Enable/disable the speaker handler",
        default=True,
        update=update_speaker
    )

    def tc_to_frames(self, context, timecode):
        logger.debug(f'Received timecode: {timecode}')
        if self.enable_reaperTC:
            try:
                # Ensure timecode is a clean string (remove any tuple formatting)
                timecode = str(timecode).strip("(),'\"")
                fps = context.scene.render.fps
                hours, minutes, seconds, frames = map(int, timecode.split(':'))
                total_frames = int((hours * 3600 + minutes * 60 + seconds) * fps + frames)
                logger.debug(f'Converted timecode {timecode} to frames: {total_frames} (FPS: {fps})')
                context.scene.frame_set(total_frames, subframe=0.0)
                return total_frames
            except Exception as e:
                logger.error(f'Error converting timecode {timecode}: {str(e)}')
                return 0

    def populate(self, context, address, args):
        if self.enable_populate:
            data_file = open("received.txt", "rb")
            datas = pickle.load(data_file)
            data_file.close()
            data_file = open('received.txt', 'wb')
            pickle.dump(datas +[[address,args]], data_file)
            data_file.close()
            data_file = open("received.txt", "rb")
            datas = pickle.load(data_file)
            data_file.close()
            print("received datas :", datas)

    def dump(self, context, address, args):
        if self.enable_dump:
            print("dump received :",address, args)
            context.data.node_groups["AN Tree"].nodes["Data Input"].inputs[0].value = args

    def track(self, context, address, args):
        if self.enable_track:
            print("address :" + address + "; args :" + args)
            arguments = args.replace('(','').replace(')','').split(',')
            arguments = [x for x in arguments if x]
            properties = ['color', 'x', 'y', 'z', 'name', 'xyz']
            track = 'track'
            if track in address:
                sepTerms = address.split('/')
                if len(sepTerms[2]) == 1:
                    id =  "00"+ sepTerms[2]
                elif len(sepTerms[2]) == 2:
                    id =  "0"+ sepTerms[2]
                elif len(sepTerms[2]) == 3:
                    id =   sepTerms[2]
                objects = [obj.name for obj in context.scene.objects]
                matching = [s for s in objects if id in s]
                if matching == []:
                    debug = str(id)
                    bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0))
                    if len(sepTerms[2]) == 1 :
                        context.active_object.name = 'track.00'+ sepTerms[2]
                        context.active_object.show_name = True
                    elif len(sepTerms[2]) == 2:
                        context.active_object.name = 'track.0'+ sepTerms[2]
                        context.active_object.show_name = True
                    else:
                        context.active_object.name = 'track.'+ sepTerms[2]
                        context.active_object.show_name = True
                    if sepTerms[3] == properties[5]:
                        context.active_object.location.x = float(arguments[0])
                        context.active_object.location.y = float(arguments[1])
                        context.active_object.location.z = float(arguments[2])
                        return
                    elif sepTerms[3] == properties[1]:
                        context.active_object.location.x = float(arguments[0])
                        return
                    elif sepTerms[3] == properties[2]:
                        context.active_object.location.y = float(arguments[0])
                        return
                    elif sepTerms[3] == properties[3]:
                        context.active_object.location.z = float(arguments[0])
                        return
                    elif sepTerms[3] == properties[0]:
                        context.active_object.color = (float(arguments[0]),float(arguments[1]),float(arguments[2]),float(arguments[3]))
                        return
                    else:
                        if sepTerms[3] == properties[4]:
                            context.active_object.name = str(context.active_object.name) + "." + str(arguments[0]).replace("'",'')
                            return
                else:
                    for x in objects:
                        ob = context.data.objects[x]
                        index = ((ob.name).split('.'))[1]
                        if index == id:
                            if sepTerms[3] == properties[5]:
                                ob.location.x = float(arguments[0])
                                ob.location.y = float(arguments[1])
                                ob.location.z = float(arguments[2])
                                return
                            elif sepTerms[3] == properties[1]:
                                ob.location.x = float(arguments[0])
                                return
                            elif sepTerms[3] == properties[2]:
                                ob.location.y = float(arguments[0])
                                return
                            elif sepTerms[3] == properties[3]:
                                ob.location.z = float(arguments[0])
                                return
                            elif sepTerms[3] == properties[0]:
                                ob.color = (float(arguments[0]),float(arguments[1]),float(arguments[2]),float(arguments[3]))
                                return
                            else:
                                if sepTerms[3] == properties[4]:
                                    inname = str(arguments[0]).replace("'",'')
                                    if len((ob.name).split('.')) == 3:
                                        exname = str(((ob.name).split('.'))[2])
                                        debug = exname
                                        ob.name = (ob.name).replace( exname, inname)
                                        return
                                    else:
                                        ob.name = (ob.name) + "." + inname
                                        return


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(HolophonixUtilsProperties)
    bpy.types.Scene.holophonix_utils = bpy.props.PointerProperty(type=HolophonixUtilsProperties)
    bpy.app.handlers.depsgraph_update_post.append(HolophonixUtilsProperties.update_nodeosc_handlers)
    bpy.utils.register_class(SNA_OT_AddHandlers)
    bpy.utils.register_class(SNA_OT_Add_Sources_73B0D)
    bpy.utils.register_class(SNA_OT_Import_An_Tree_433Db)
    bpy.utils.register_class(SNA_OT_Sources_Exporter_34F69)
    bpy.utils.register_class(SNA_OT_Add_Speakers_994C8)
    bpy.utils.register_class(SNA_PT_HOLOUTILS_1B113)
    bpy.utils.register_class(SNA_OT_Delete_Handlers_C2D71)
    
    # Check if NodeOSC addon is enabled and OSC_PT_Operations exists
    if "NodeOSC" in bpy.context.preferences.addons and hasattr(bpy.types, 'OSC_PT_Operations'):
        bpy.types.OSC_PT_Operations.prepend(sna_add_to_osc_pt_operations_7D1DC)
        bpy.types.OSC_PT_Operations.append(sna_add_to_osc_pt_operations_ACA0D)
    else:
        print("Warning: NodeOSC addon is not enabled or OSC_PT_Operations panel not found. Skipping prepend and append operations.")
    
    bpy.utils.register_class(SNA_PT_SPECIALHANDLERS)
    bpy.utils.register_class(SNA_PT_SOURCES_11FF6)
    bpy.utils.register_class(SNA_PT_SPEAKERS_F8536)
    bpy.utils.register_class(SNA_PT_NODEOSC_SETTINGS_2B3D4)
    bpy.utils.register_class(SNA_PT_AN_SETTINGS_E1993)

    


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    bpy.app.handlers.depsgraph_update_post.remove(HolophonixUtilsProperties.update_nodeosc_handlers)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_OT_AddHandlers)
    bpy.utils.unregister_class(SNA_OT_Add_Sources_73B0D)
    bpy.utils.unregister_class(SNA_OT_Import_An_Tree_433Db)
    bpy.utils.unregister_class(SNA_OT_Sources_Exporter_34F69)
    bpy.utils.unregister_class(SNA_OT_Add_Speakers_994C8)
    bpy.utils.unregister_class(SNA_PT_HOLOUTILS_1B113)
    bpy.utils.unregister_class(SNA_OT_Delete_Handlers_C2D71)
    bpy.types.OSC_PT_Operations.remove(sna_add_to_osc_pt_operations_7D1DC)
    bpy.types.OSC_PT_Operations.remove(sna_add_to_osc_pt_operations_ACA0D)
    bpy.utils.unregister_class(SNA_PT_SPECIALHANDLERS)
    bpy.utils.unregister_class(SNA_PT_SOURCES_11FF6)
    bpy.utils.unregister_class(SNA_PT_SPEAKERS_F8536)
    bpy.utils.unregister_class(SNA_PT_NODEOSC_SETTINGS_2B3D4)
    bpy.utils.unregister_class(SNA_PT_AN_SETTINGS_E1993)
    bpy.utils.unregister_class(HolophonixUtilsProperties)
