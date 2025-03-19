import bpy

class SNA_OT_InitializeTrackHandlers(bpy.types.Operator):
    """Initialize track handlers with default values"""
    bl_idname = "sna.initialize_track_handlers"
    bl_label = "Initialize Track Handlers"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    def execute(self, context):
        props = context.scene.holophonix_utils
        
        if not hasattr(props, 'track_handlers'):
            self.report({'ERROR'}, "Track handlers property not found")
            return {'CANCELLED'}
        
        # Position handlers - default to output
        props.track_handlers.position.enabled = True
        props.track_handlers.position.direction = 'OUTPUT'
        
        # Name handlers - default to input 
        props.track_handlers.name.enabled = True
        props.track_handlers.name.direction = 'INPUT'
        
        # Color handlers - default to input
        props.track_handlers.color.enabled = True
        props.track_handlers.color.direction = 'INPUT'
        
        # Mark as initialized
        props.track_handlers_initialized = True
        
        return {'FINISHED'}
