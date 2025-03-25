import bpy

class SNA_OT_DeleteTrack(bpy.types.Operator):
    bl_idname = "sna.delete_track"
    bl_label = "Delete Track"
    bl_description = "Delete this track"
    bl_options = {'REGISTER', 'UNDO'}
    
    track_name: bpy.props.StringProperty()
    
    def execute(self, context):
        track = bpy.data.objects.get(self.track_name)
        if track:
            # Remove associated NodeOSC_keys
            if hasattr(context.scene, 'NodeOSC_keys'):
                # Create list of indices to remove (in reverse order)
                indices_to_remove = [
                    i for i, key in enumerate(context.scene.NodeOSC_keys)
                    if key.data_path and self.track_name in key.data_path
                ]
                
                # Remove keys in reverse order to avoid index shifting
                for i in reversed(indices_to_remove):
                    context.scene.NodeOSC_keys.remove(i)
                    print(f"Removed NodeOSC_key at index {i} for track {self.track_name}")
    
            # Remove the track object
            bpy.data.objects.remove(track, do_unlink=True)
            self.report({'INFO'}, f"Deleted track {self.track_name}")
        else:
            self.report({'WARNING'}, f"Track {self.track_name} not found")
        return {'FINISHED'}
