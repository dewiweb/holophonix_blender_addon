import bpy

class TrackHandlerSettings(bpy.types.PropertyGroup):
    """
    Settings for track handlers with automatic update functionality.
    This simplified approach directly interacts with NodeOSC_keys collection.
    """
    
    # Class-level flag to prevent recursive updates
    _is_updating = False
    
    def update_handlers(self, context):
        """
        Update track handlers when settings change.
        Uses a timer and flags to avoid recursion issues.
        """
        # Check if we have a valid context with a scene
        if not hasattr(context, 'scene'):
            return
            
        # Skip if we're already updating or initializing
        scene = context.scene
        if not hasattr(scene, 'holophonix_utils') or not hasattr(scene.holophonix_utils, 'is_initializing'):
            return
            
        # Prevent recursive updates
        if TrackHandlerSettings._is_updating:
            return
            
        if not scene.holophonix_utils.is_initializing:
            # Store the current property values to ensure they're preserved
            self.store_current_values()
            
            # Schedule the update with a small delay to avoid recursion
            if not bpy.app.timers.is_registered(self.do_update_handlers):
                bpy.app.timers.register(lambda: self.do_update_handlers(context), first_interval=0.1)
    
    def store_current_values(self):
        """Store current property values to ensure they're not lost"""
        if not hasattr(self, '_stored_values'):
            self._stored_values = {}
            
        # Store all property values
        self._stored_values['position_enabled'] = self.position_enabled
        self._stored_values['position_direction'] = self.position_direction
        self._stored_values['name_enabled'] = self.name_enabled
        self._stored_values['name_direction'] = self.name_direction
        self._stored_values['color_enabled'] = self.color_enabled
        self._stored_values['color_direction'] = self.color_direction
    
    def do_update_handlers(self, context):
        """Execute the track handler management operator"""
        try:
            # Set the updating flag to prevent recursive updates
            TrackHandlerSettings._is_updating = True
            
            # Ensure we're using the stored values
            if hasattr(self, '_stored_values'):
                # Restore stored values if they exist
                for prop, value in self._stored_values.items():
                    if hasattr(self, prop):
                        setattr(self, prop, value)
            
            # Now call the operator
            bpy.ops.sna.manage_track_handlers(auto_triggered=True)
        except Exception as e:
            print(f"Error updating track handlers: {e}")
        finally:
            # Always clear the updating flag when done
            TrackHandlerSettings._is_updating = False
        return None  # Remove timer
    
    # Global management setting
    auto_manage_handlers: bpy.props.BoolProperty(
        name="Auto-Manage Handlers",
        description="When enabled, this addon will automatically manage track handlers. Disable this if you want to manually configure handlers in NodeOSC panel",
        default=True
    )
    
    # Position handler settings
    position_enabled: bpy.props.BoolProperty(
        name="Position",
        description="Enable position handlers for tracks",
        default=True,
        update=update_handlers
    )
    position_direction: bpy.props.EnumProperty(
        name="Position Direction",
        description="Direction for position handlers",
        items=[
            ('INPUT', 'Input', 'Receive OSC messages only'),
            ('OUTPUT', 'Output', 'Send OSC messages only'),
            ('BOTH', 'Both', 'Send and receive OSC messages')
        ],
        default='OUTPUT',
        update=update_handlers
    )
    
    # Name handler settings
    name_enabled: bpy.props.BoolProperty(
        name="Name",
        description="Enable name handlers for tracks",
        default=True,
        update=update_handlers
    )
    name_direction: bpy.props.EnumProperty(
        name="Name Direction",
        description="Direction for name handlers",
        items=[
            ('INPUT', 'Input', 'Receive OSC messages only'),
            ('OUTPUT', 'Output', 'Send OSC messages only'),
            ('BOTH', 'Both', 'Send and receive OSC messages')
        ],
        default='INPUT',
        update=update_handlers
    )
    
    # Color handler settings
    color_enabled: bpy.props.BoolProperty(
        name="Color",
        description="Enable color handlers for tracks",
        default=True,
        update=update_handlers
    )
    color_direction: bpy.props.EnumProperty(
        name="Color Direction",
        description="Direction for color handlers",
        items=[
            ('INPUT', 'Input', 'Receive OSC messages only'),
            ('OUTPUT', 'Output', 'Send OSC messages only'),
            ('BOTH', 'Both', 'Send and receive OSC messages')
        ],
        default='INPUT',
        update=update_handlers
    )
