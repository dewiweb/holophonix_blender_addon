import bpy

def initialize_track_handlers(*args):
    """Initialize track handlers properties if needed"""
    if not hasattr(bpy.context.scene, 'holophonix_utils'):
        return
    
    props = bpy.context.scene.holophonix_utils
    
    # Only initialize if needed and if the properties exist
    if hasattr(props, 'track_handlers') and not props.track_handlers_initialized:
        try:
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
            
            print("Holophonix Utils: Track handlers initialized successfully")
        except Exception as e:
            print(f"Holophonix Utils: Error initializing track handlers: {e}")
