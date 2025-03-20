import bpy

def initialize_track_handlers(*args):
    """Initialize track handler settings if needed"""
    # Track if we've already initialized to prevent recursion
    if hasattr(bpy, '_holophonix_initializing') and bpy._holophonix_initializing:
        return
    
    # Set a flag to prevent recursion
    bpy._holophonix_initializing = True
    
    # Use a safer approach that doesn't rely on bpy.context.scene
    # Iterate through all scenes and initialize their track handlers
    for scene in bpy.data.scenes:
        if not hasattr(scene, 'holophonix_utils'):
            continue
        
        props = scene.holophonix_utils
        
        # Set initializing flag to prevent updates during initialization
        props.is_initializing = True
        
        # Initialize track handler settings if they exist
        if hasattr(props, 'track_handler_settings'):
            try:
                # Only set defaults if this is the first initialization
                # Check if this is the first time we're initializing
                if not hasattr(props, '_handlers_initialized'):
                    # Auto-manage handlers - default to enabled
                    props.track_handler_settings.auto_manage_handlers = True
                    
                    # Position handlers - default to output
                    props.track_handler_settings.position_enabled = True
                    props.track_handler_settings.position_direction = 'OUTPUT'
                    
                    # Name handlers - default to input 
                    props.track_handler_settings.name_enabled = True
                    props.track_handler_settings.name_direction = 'INPUT'
                    
                    # Color handlers - default to input
                    props.track_handler_settings.color_enabled = True
                    props.track_handler_settings.color_direction = 'INPUT'
                    
                    # Mark as initialized so we don't override user settings
                    props._handlers_initialized = True
                
                print("Holophonix Utils: Track handlers initialized successfully")
                
                # Don't call manage_track_handlers here to avoid recursion
                # Instead, schedule it for later with a timer
            except Exception as e:
                print(f"Holophonix Utils: Error initializing track handlers: {e}")
        
        # Clear initializing flag
        props.is_initializing = False
    
    # Schedule the track handler creation for later to avoid recursion
    def deferred_create_handlers():
        try:
            if hasattr(bpy.context, 'scene') and bpy.context.scene is not None:
                if hasattr(bpy.context.scene, 'NodeOSC_keys'):
                    bpy.ops.sna.manage_track_handlers(auto_triggered=True)
        except Exception as e:
            print(f"Holophonix Utils: Error creating track handlers: {e}")
        finally:
            # Clear the initialization flag
            if hasattr(bpy, '_holophonix_initializing'):
                del bpy._holophonix_initializing
        return None  # Remove the timer
    
    # Register the timer to create handlers later
    bpy.app.timers.register(deferred_create_handlers, first_interval=0.5)
