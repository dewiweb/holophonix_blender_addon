import bpy

class SNA_OT_DeleteAllTracks(bpy.types.Operator):
    bl_idname = 'sna.delete_all_tracks'
    bl_label = 'Delete All Tracks'
    bl_description = 'Deletes all tracks and associated NodeOSC_keys from the scene'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        track_objects = [obj for obj in bpy.data.objects if 'track' in obj.name.lower()]
        track_count = len(track_objects)
        print(f"Poll: track_count={track_count}")
        return track_count > 0

    def execute(self, context):
        print("Executing delete_all_tracks operator")
        
        # Get all track objects
        track_objects = [obj for obj in bpy.data.objects if 'track' in obj.name.lower()]
        print(f"Found {len(track_objects)} track objects")

        # Remove associated NodeOSC_keys
        if hasattr(context.scene, 'NodeOSC_keys'):
            print(f"Found {len(context.scene.NodeOSC_keys)} NodeOSC_keys")
            # Create list of indices to remove (in reverse order)
            indices_to_remove = [
                i for i, key in enumerate(context.scene.NodeOSC_keys)
                if key.data_path and any(track.name in key.data_path for track in track_objects)
            ]
            print(f"Removing {len(indices_to_remove)} NodeOSC_keys")
            
            # Remove keys in reverse order to avoid index shifting
            for i in reversed(indices_to_remove):
                context.scene.NodeOSC_keys.remove(i)
                print(f"Removed NodeOSC_key at index {i}")

        # Remove track objects
        for track in track_objects:
            track_name = track.name  # Store name before removal
            bpy.data.objects.remove(track)
            print(f"Removed track object: {track_name}")

        # Clear all tracks from scene collection
        if hasattr(context.scene, 'tracks'):
            print(f"Removing {len(context.scene.tracks)} tracks from scene collection")
            context.scene.tracks.clear()
        return {'FINISHED'}
