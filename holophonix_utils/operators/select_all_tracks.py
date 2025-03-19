import bpy

class SNA_OT_SelectAllTracks(bpy.types.Operator):
    bl_idname = "sna.select_all_tracks"
    bl_label = "Select All Tracks"
    bl_description = "Select all track objects in the scene"
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        # Ensure there's at least one track in the scene
        return any(obj for obj in context.scene.objects if "track" in obj.name)
    
    def execute(self, context):
        # Deselect all first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Find and select all track objects
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        
        if not tracks:
            self.report({'INFO'}, "No tracks found in the scene")
            return {'CANCELLED'}
        
        # Select all track objects
        for obj in tracks:
            obj.select_set(True)
        
        # Set the active object to the first track
        if tracks:
            context.view_layer.objects.active = tracks[0]
            
        self.report({'INFO'}, f"Selected {len(tracks)} track objects")
        return {'FINISHED'}
