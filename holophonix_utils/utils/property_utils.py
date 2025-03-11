import bpy
import os
from bpy.utils import previews

class HolophonixUtilsProperties(bpy.types.PropertyGroup):
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

    project_imported: bpy.props.BoolProperty(
        name="Project Imported",
        description="Track whether a .zip file has been imported",
        default=False
    )

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

# Registration moved to __init__.py
