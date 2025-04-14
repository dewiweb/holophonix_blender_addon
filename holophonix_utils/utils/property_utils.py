import bpy
import os
from bpy.utils import previews
from ..utils.file_properties import FileProperties
#from ..utils.track_handler_settings import TrackHandlerSettings

class HolophonixUtilsProperties(bpy.types.PropertyGroup):
    # Flag to prevent updates during initialization
    is_initializing: bpy.props.BoolProperty(default=False)
    
    # Property to store resolved Holophonix IP address
    holophonix_ip: bpy.props.StringProperty(
        name="Holophonix IP Address",
        description="The resolved IP address of holophonix.local",
        default=""
    )
    
    def register_icons(self):
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
        self.icons = bpy.utils.previews.new()
        self.icons.load('logo_icon', os.path.join(icons_dir, 'logo_icon.png'), 'IMAGE')

    def unregister_icons(self):
        if hasattr(self, 'icons'):
            self.icons.clear()
            bpy.utils.previews.remove(self.icons)

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

    def update_incoming_tracks(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_direction == "INPUT" and "/track/" in item.osc_address:
                    item.enabled = self.enable_incoming_tracks

    def update_outgoing_tracks(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_direction == "OUTPUT" and "/track/" in item.osc_address:
                    item.enabled = self.enable_outgoing_tracks

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
            elif item.osc_direction == "INPUT" and "/track/" in item.osc_address and item.enabled != props.enable_incoming_tracks:
                props.enable_incoming_tracks = item.enabled
            elif item.osc_direction == "OUTPUT" and "/track/" in item.osc_address and item.enabled != props.enable_outgoing_tracks:
                props.enable_outgoing_tracks = item.enabled
            elif item.osc_address == "/speaker/*" and item.enabled != props.enable_speaker:
                props.enable_speaker = item.enabled
            elif item.osc_address == "/frames/str" and item.enabled != props.enable_reaperTC:
                props.enable_reaperTC = item.enabled

    enable_dump: bpy.props.BoolProperty(
        name="Enable Dump Handler",
        description="Enable/disable the dump handler",
        default=True,
        update=update_dump
    )

    enable_track: bpy.props.BoolProperty(
        name="Enable Track Handler",
        description="Enable/disable the track handler",
        default=True,
        update=update_track
    )

    enable_incoming_tracks: bpy.props.BoolProperty(
        name="Enable Incoming Tracks",
        description="Enable/disable incoming track handlers",
        default=True,
        update=update_incoming_tracks
    )

    enable_outgoing_tracks: bpy.props.BoolProperty(
        name="Enable Outgoing Tracks",
        description="Enable/disable outgoing track handlers",
        default=True,
        update=update_outgoing_tracks
    )
    
    # Track handler configuration properties
    #track_handler_settings: bpy.props.PointerProperty(type=TrackHandlerSettings)

    enable_speaker: bpy.props.BoolProperty(
        name="Enable Speaker Handler",
        description="Enable/disable the speaker handler",
        default=True,
        update=update_speaker
    )

    enable_reaperTC: bpy.props.BoolProperty(
        name="Enable Reaper TC Handler",
        description="Enable/disable the ReaperTC handler",
        default=True,
        update=update_reaperTC
    )

    enable_populate: bpy.props.BoolProperty(
        name="Enable Populate Handler",
        description="Enable/disable the populate handler",
        default=True
    )

    show_track_table: bpy.props.BoolProperty(
        name="Show Track Table",
        default=True
    )

    show_introduction: bpy.props.BoolProperty(
        name="Show Introduction",
        default=True
    )
    '''
    project_path: bpy.props.StringProperty(
        name="Project Path",
        description="Path to the Holophonix project folder",
        default="",
        subtype='DIR_PATH'
    )
    project_imported: bpy.props.BoolProperty(
        name="Project Imported",
        description="Whether a Holophonix project has been imported",
        default=False
    )

    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="Name of the imported Holophonix project",
        default=""
    )

    holophonix_hol_files: bpy.props.EnumProperty(
        name=".hol File",
        description="Select a .hol file from the Presets directory",
        items=lambda self, context: FileProperties.get_hol_files(self, context, self.project_path)
    )
    def update_selected_hol_file(self, context):
        if self.holophonix_hol_files:
            self.selected_hol_file = os.path.join(self.project_path, self.holophonix_hol_files)
    
    selected_hol_file: bpy.props.StringProperty(
        name="Selected HOL File",
        description="Path to the selected .hol file",
        subtype='FILE_PATH',
        update=update_selected_hol_file
    )
    
    
    def get_hol_files(self, context, project_path):
        # Check if project_path is set
        if not project_path:
            print("No project path provided.")
            return [("NONE", "No .hol files found", "No .hol files found")]
    
        # Construct the path to the Presets directory
        presets_path = os.path.join(project_path, 'Presets')
    
        # Check if the Presets directory exists
        if not os.path.exists(presets_path):
            print(f"Presets directory does not exist: {presets_path}")
            return [("NONE", "Presets directory not found", "Presets directory not found")]
    
        # Find all .hol files in the Presets directory
        hol_files = []
        for file in os.listdir(presets_path):
            if file.endswith('.hol'):
                hol_files.append((file, file, file))
    
        if not hol_files:
            print("No .hol files found in the Presets directory.")
            return [("NONE", "No .hol files found", "No .hol files found")]
    
        return hol_files
    '''

    def register_property(self, context):
        try:
            if not hasattr(bpy.types.Scene, 'holophonix_utils'):
                bpy.types.Scene.holophonix_utils = bpy.props.PointerProperty(type=HolophonixUtilsProperties)
        except Exception as e:
            print(f'Failed to register property: {str(e)}')

    def unregister_property(self, context):
        try:
            if hasattr(bpy.types.Scene, 'holophonix_utils'):
                del bpy.types.Scene.holophonix_utils
        except Exception as e:
            print(f'Failed to unregister property: {str(e)}')

    def tc_to_frames(self, context, timecode):
        print(f'Received timecode: {timecode}')
        if self.enable_reaperTC:
            try:
                # Ensure timecode is a clean string (remove any tuple formatting)
                timecode = str(timecode).strip("(),'")
                fps = context.scene.render.fps
                hours, minutes, seconds, frames = map(int, timecode.split(':'))
                total_frames = int((hours * 3600 + minutes * 60 + seconds) * fps + frames)
                print(f'Converted timecode {timecode} to frames: {total_frames} (FPS: {fps})')
                context.scene.frame_set(total_frames, subframe=0.0)
                return total_frames
            except Exception as e:
                print(f'Error converting timecode {timecode}: {str(e)}')
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

def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def update_location_direction(self, context):
    if hasattr(context.scene, 'NodeOSC_keys'):
        handlers = [
            key for key in context.scene.NodeOSC_keys 
            if any(axis in key.osc_address for axis in ['x', 'y', 'z'])
            and self.id_data.name in key.data_path
        ]
        for handler in handlers:
            handler.osc_direction = self.location_direction

class TrackProperties(bpy.types.PropertyGroup):
    location_direction: bpy.props.EnumProperty(
        name="",
        items=[
            ('INPUT', "Input", "Receive data", 'IMPORT', 0),
            ('OUTPUT', "Output", "Send data", 'EXPORT', 1), 
            ('BOTH', "Both", "Send and receive", 'FILE_REFRESH', 2)
        ],
        update=update_location_direction
    )

class SceneProperties(bpy.types.PropertyGroup):
    all_handlers_enabled: bpy.props.BoolProperty(
        name="All Handlers Enabled",
        description="Toggle all track handlers",
        default=True,
        update=lambda self, context: (bpy.ops.sna.toggle_all_handlers(), None)[1]
    )

    all_directions: bpy.props.EnumProperty(
        name="All Directions",
        items=[
            ('INPUT', "Input", "Receive data", 'IMPORT', 0),
            ('OUTPUT', "Output", "Send data", 'EXPORT', 1), 
            ('BOTH', "Both", "Send and receive", 'FILE_REFRESH', 2)
        ],
        update=lambda self, context: (bpy.ops.sna.set_all_directions(direction=self.all_directions), None)[1]
    )
    
    location_handlers_enabled: bpy.props.BoolProperty(
        name="Location Handlers Enabled",
        description="Toggle location track handlers",
        default=True,
        update=lambda self, context: (bpy.ops.sna.toggle_location_handlers(), None)[1]
    )
    
    location_handlers_direction: bpy.props.EnumProperty(
        name="Location Handlers Direction",
        items=[
            ('INPUT', "Input", "Receive data", 'IMPORT', 0),
            ('OUTPUT', "Output", "Send data", 'EXPORT', 1), 
            ('BOTH', "Both", "Send and receive", 'FILE_REFRESH', 2)
        ],
        update=lambda self, context: (bpy.ops.sna.set_location_directions(direction=self.location_handlers_direction), None)[1]
    )
    
    color_handlers_enabled: bpy.props.BoolProperty(
        name="Color Handlers Enabled",
        description="Toggle color track handlers",
        default=True,
        update=lambda self, context: (bpy.ops.sna.toggle_color_handlers(), None)[1]
    )
    
    color_handlers_direction: bpy.props.EnumProperty(
        name="Color Handlers Direction",
        items=[
            ('INPUT', "Input", "Receive data", 'IMPORT', 0),
            ('OUTPUT', "Output", "Send data", 'EXPORT', 1), 
            ('BOTH', "Both", "Send and receive", 'FILE_REFRESH', 2)
        ],
        update=lambda self, context: (bpy.ops.sna.set_color_directions(direction=self.color_handlers_direction), None)[1]
    )
    
    name_handlers_enabled: bpy.props.BoolProperty(
        name="Name Handlers Enabled",
        description="Toggle name track handlers",
        default=True,
        update=lambda self, context: (bpy.ops.sna.toggle_name_handlers(), None)[1]
    )
    
    name_handlers_direction: bpy.props.EnumProperty(
        name="Name Handlers Direction",
        items=[
            ('INPUT', "Input", "Receive data", 'IMPORT', 0),
            ('OUTPUT', "Output", "Send data", 'EXPORT', 1), 
            ('BOTH', "Both", "Send and receive", 'FILE_REFRESH', 2)
        ],
        update=lambda self, context: (bpy.ops.sna.set_name_directions(direction=self.name_handlers_direction), None)[1]
    )
    
# Registration moved to __init__.py
