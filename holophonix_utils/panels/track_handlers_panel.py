import bpy

class SNA_PT_TrackHandlers(bpy.types.Panel):
    """
    Panel for managing track handler settings.
    Provides a simple interface for configuring track handlers.
    """
    bl_label = "Track Handlers"
    bl_idname = "SNA_PT_TRACK_HANDLERS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'SNA_PT_TRACKS_11FF6'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        """Only show if NodeOSC is available"""
        return hasattr(context.scene, 'NodeOSC_keys')
        
    def draw(self, context):
        layout = self.layout
        settings = context.scene.holophonix_utils.track_handler_settings
        
        # Explanation
        box = layout.box()
        box.label(text="OSC Track Handler Settings", icon='NODETREE')
        
        # Auto-manage handlers option
        auto_row = box.row()
        auto_row.prop(settings, "auto_manage_handlers")
        if not settings.auto_manage_handlers:
            info_row = box.row()
            info_row.label(text="Manual mode: Use NodeOSC panel for individual settings", icon='INFO')
        
        help_col = box.column(align=True)
        help_col.label(text="Data Flow Direction:", icon='INFO')
        help_col.label(text="INPUT: Holophonix → Blender")
        help_col.label(text="OUTPUT: Blender → Holophonix")
        help_col.label(text="BOTH: Bidirectional communication")
        
        # Settings in a grid layout with 3 columns: Type, Enabled, Direction
        grid = layout.grid_flow(row_major=True, columns=3, even_columns=True)
        grid.label(text="Handler Type")
        grid.label(text="Enabled")
        grid.label(text="Direction")
        
        # Position
        grid.label(text="Position", icon='OBJECT_ORIGIN')
        grid.prop(settings, "position_enabled", text="")
        grid.prop(settings, "position_direction", text="")
        
        # Name
        grid.label(text="Name", icon='FONT_DATA')
        grid.prop(settings, "name_enabled", text="")
        grid.prop(settings, "name_direction", text="")
        
        # Color
        grid.label(text="Color", icon='COLOR')
        grid.prop(settings, "color_enabled", text="")
        grid.prop(settings, "color_direction", text="")
            
        # Manual update button (still useful for refreshing)
        row = layout.row()
        row.operator("sna.manage_track_handlers", text="Refresh Track Handlers", icon='FILE_REFRESH')
        
        # Status info
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        if tracks:
            layout.label(text=f"Found {len(tracks)} tracks", icon='CHECKMARK')
        else:
            layout.label(text="No tracks found", icon='ERROR')
