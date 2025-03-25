import bpy

class SNA_OT_SelectTrack(bpy.types.Operator):
    bl_idname = "sna.select_track"
    bl_label = "Select Track"
    bl_options = {"REGISTER", "UNDO"}

    track_name: bpy.props.StringProperty()

    def execute(self, context):
        # Find the track object by name
        track = bpy.data.objects.get(self.track_name)
        if track:
            # Toggle selection
            track.select_set(not track.select_get())
            if track.select_get():
                context.view_layer.objects.active = track
                self.report({'INFO'}, f"Selected track: {track.name}")
            else:
                self.report({'INFO'}, f"Deselected track: {track.name}")
        else:
            self.report({'ERROR'}, f"Track not found: {self.track_name}")
        return {'FINISHED'}