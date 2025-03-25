import bpy

class SNA_OT_SelectAllTracks(bpy.types.Operator):
    bl_idname = 'sna.select_all_tracks'
    bl_label = 'Select All Tracks'
    bl_description = 'Select/Deselect all track objects in the scene'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Ensure there's at least one track in the scene
        return any(obj for obj in context.scene.objects if 'track' in obj.name)
    
    def execute(self, context):
        tracks = [obj for obj in context.scene.objects if 'track' in obj.name]
        
        if not tracks:
            self.report({'INFO'}, 'No tracks found in the scene')
            return {'CANCELLED'}
        
        # Check if all tracks are already selected
        all_selected = all(obj.select_get() for obj in tracks)
        
        if all_selected:
            # Deselect all tracks
            for obj in tracks:
                obj.select_set(False)
            context.view_layer.objects.active = None
            self.report({'INFO'}, f'Deselected {len(tracks)} track objects')
        else:
            # Select all tracks
            for obj in tracks:
                obj.select_set(True)
            context.view_layer.objects.active = tracks[0]
            self.report({'INFO'}, f'Selected {len(tracks)} track objects')
        
        return {'FINISHED'}
