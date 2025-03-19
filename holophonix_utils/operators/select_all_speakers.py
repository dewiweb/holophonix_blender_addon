import bpy

class SNA_OT_SelectAllSpeakers(bpy.types.Operator):
    bl_idname = "sna.select_all_speakers"
    bl_label = "Select All Speakers"
    bl_description = "Select all speaker objects in the scene"
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        # Ensure there's at least one speaker in the scene
        return any(obj for obj in context.scene.objects if "speaker" in obj.name.lower())
    
    def execute(self, context):
        # Deselect all first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Find and select all speaker objects
        speakers = [obj for obj in context.scene.objects if "speaker" in obj.name.lower()]
        
        if not speakers:
            self.report({'INFO'}, "No speakers found in the scene")
            return {'CANCELLED'}
        
        # Select all speaker objects
        for obj in speakers:
            obj.select_set(True)
        
        # Set the active object to the first speaker
        if speakers:
            context.view_layer.objects.active = speakers[0]
            
        self.report({'INFO'}, f"Selected {len(speakers)} speaker objects")
        return {'FINISHED'}
