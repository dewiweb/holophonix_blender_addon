import bpy

class SNA_OT_ToggleTrackHandlers(bpy.types.Operator):
    bl_idname = 'sna.toggle_track_handlers'
    bl_label = 'Toggle Track Handlers'
    bl_description = 'Toggles the enabled state of all handlers for a track'
    bl_options = {'REGISTER', 'UNDO'}

    track_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return hasattr(context.scene, 'NodeOSC_keys')

    def execute(self, context):
        print(f"Searching handlers for track: {self.track_name}")
        track = context.scene.objects.get(self.track_name)
        if track:
            print(f"Found track: {track.name}")
            if hasattr(context.scene, 'NodeOSC_keys'):
                print(f"Found {len(context.scene.NodeOSC_keys)} NodeOSC_keys")
                track_handlers = [
                    key for key in context.scene.NodeOSC_keys
                    if key.data_path and self.track_name in key.data_path
                ]
                print(f"Found {len(track_handlers)} handlers for this track")
                if track_handlers:
                    print("Handler data paths:")
                    for key in track_handlers:
                        print(f"- {key.data_path}")
                    current_state = any(key.enabled for key in track_handlers)
                    print(f"Current state: {'Enabled' if current_state else 'Disabled'}")
                    for key in track_handlers:
                        key.enabled = not current_state
                    return {'FINISHED'}
            else:
                print("No NodeOSC_keys found in scene")
        else:
            print("Track not found in scene")
        return {'CANCELLED'}
