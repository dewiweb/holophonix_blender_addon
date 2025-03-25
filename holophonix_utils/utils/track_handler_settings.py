import bpy
from .track_handler_proxy import get_manager


class TrackHandlerSettings(bpy.types.PropertyGroup):
    """Settings for track handlers with automatic update functionality"""
    _is_updating = False
    
    def update_handlers(self, context):
        """Update track handlers when settings change"""
        if self._is_updating:
            return
            
        manager = get_manager()
        if not manager or not hasattr(manager, 'update_all'):
            return
            
        try:
            # Update all proxies with current settings
            self._is_updating = True
            manager.update_all()
            
            # Apply changes to NodeOSC_keys
            bpy.ops.sna.manage_track_handlers(auto_triggered=True)
        except Exception as e:
            print(f"Error updating track handlers: {str(e)}")
        finally:
            self._is_updating = False

    position_enabled: bpy.props.BoolProperty(
        name="Enable Position Handlers",
        description="Enable position tracking for tracks",
        default=True,
        update=update_handlers
    )
    
    position_direction: bpy.props.EnumProperty(
        name="Position Direction",
        description="Direction for position handlers",
        items=[
            ('BOTH', "Both", "Send and receive position updates"),
            ('INPUT', "Input", "Only receive position updates"),
            ('OUTPUT', "Output", "Only send position updates")
        ],
        default='BOTH',
        update=update_handlers
    )
    
    name_enabled: bpy.props.BoolProperty(
        name="Enable Name Handlers",
        description="Enable name tracking for tracks",
        default=True,
        update=update_handlers
    )
    
    name_direction: bpy.props.EnumProperty(
        name="Name Direction",
        description="Direction for name handlers",
        items=[
            ('BOTH', "Both", "Send and receive name updates"),
            ('INPUT', "Input", "Only receive name updates"),
            ('OUTPUT', "Output", "Only send name updates")
        ],
        default='BOTH',
        update=update_handlers
    )
    
    color_enabled: bpy.props.BoolProperty(
        name="Enable Color Handlers",
        description="Enable color tracking for tracks",
        default=True,
        update=update_handlers
    )
    
    color_direction: bpy.props.EnumProperty(
        name="Color Direction",
        description="Direction for color handlers",
        items=[
            ('BOTH', "Both", "Send and receive color updates"),
            ('INPUT', "Input", "Only receive color updates"),
            ('OUTPUT', "Output", "Only send color updates")
        ],
        default='BOTH',
        update=update_handlers
    )
    
    auto_manage_handlers: bpy.props.BoolProperty(
        name="Auto Manage Handlers",
        description="Automatically manage track handlers based on settings",
        default=True,
        update=update_handlers
    )