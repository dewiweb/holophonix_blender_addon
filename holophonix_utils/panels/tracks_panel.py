import bpy
import traceback

class SNA_PT_TRACKS_11FF6(bpy.types.Panel):
    bl_label = 'Tracks'
    bl_idname = 'SNA_PT_TRACKS_11FF6'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_MAIN_PANEL'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MESH_ICOSPHERE')

    def draw(self, context):
        layout = self.layout
        props = context.scene.holophonix_utils
        
        # Track import section
        box = layout.box()
        box.label(text="Import Tracks", icon='IMPORT')
        col = box.column(align=True)
        col.scale_y = 1.2
        col.operator('sna.add_tracks_73b0d', 
                    text='Import Tracks from .hol File', 
                    icon='FILE_SOUND')
        
        # Check for tracks
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        
        # Track management section
        if tracks:
            box = layout.box()
            box.label(text="Track Management", icon='OUTLINER_OB_GROUP_INSTANCE')
            
            # Stats about tracks
            row = box.row()
            row.label(text=f"Tracks: {len(tracks)}", icon='MESH_ICOSPHERE') 
            
            # Track actions
            col = box.column(align=True)
            
            # Track selection controls
            row = col.row(align=True)
            row.scale_y = 1.2
            row.operator('sna.select_all_tracks', text='Select All Tracks', icon='RESTRICT_SELECT_OFF')
        else:
            # No tracks message
            box = layout.box()
            col = box.column(align=True)
            col.label(text="No Tracks Found", icon='INFO')
            col.label(text="Import tracks using the buttons above")
        
        # Track handlers configuration section
        # Only show if NodeOSC is available
        if not hasattr(context.scene, 'NodeOSC_keys'):
            layout.label(text="NodeOSC addon is not installed or enabled", icon='ERROR')
            return
        
        # Check if there are tracks
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        if not tracks:
            layout.label(text="No tracks found. Import tracks first.", icon='INFO')
            return
            
        # Handler configuration section - only if tracks and NodeOSC present
        if tracks:
            box = layout.box()
            box.label(text="OSC Track Handler Configuration", icon='NODETREE')
            
            track_handlers = props.track_handlers
            
            # Create a nice layout with columns
            col = box.column(align=True)
            
            # Add explanation section
            help_box = col.box()
            help_col = help_box.column(align=True)
            help_col.label(text="Data Flow Direction:", icon='INFO')
            help_col.label(text="INPUT: Blender → Holophonix (Blender controls Holophonix)")
            help_col.label(text="OUTPUT: Holophonix → Blender (Holophonix controls Blender)")
            
            # Handler types section
            col.separator()
            col.label(text="Handler Types:", icon='PRESET_NEW')
            
            # Use a table-like layout for clarity
            grid = col.grid_flow(row_major=True, columns=3, even_columns=True)
            grid.label(text="Handler Type")
            grid.label(text="Enabled")
            grid.label(text="Direction")
            
            # Position handlers
            grid.label(text="Position", icon='OBJECT_ORIGIN')
            grid.prop(track_handlers.position, "enabled", text="")
            if track_handlers.position.enabled:
                grid.prop(track_handlers.position, "direction", text="")
            else:
                grid.label(text="---")
                
            # Name handlers
            grid.label(text="Name", icon='FONT_DATA')
            grid.prop(track_handlers.name, "enabled", text="")
            if track_handlers.name.enabled:
                grid.prop(track_handlers.name, "direction", text="")
            else:
                grid.label(text="---")
            
            # Color handlers
            grid.label(text="Color", icon='COLOR')
            grid.prop(track_handlers.color, "enabled", text="")
            if track_handlers.color.enabled:
                grid.prop(track_handlers.color, "direction", text="")
            else:
                grid.label(text="---")
                
            col.separator()
            
            # Help text
            col.label(text="Settings will update automatically. Click below to create handlers:", icon='HELP')
            
            col.separator()
            
            # Create handlers button
            row = col.row()
            row.scale_y = 1.5
            row.operator("sna.create_track_handlers", text="Create OSC Handlers", icon='EXPORT')
            row.alignment = 'CENTER'
        
        # Note: Legacy global handler controls removed as they are no longer necessary
        # Individual handlers can now be controlled separately
    
    # Initialization is now handled by SNA_OT_InitializeTrackHandlers operator
    # Holophonix Communication panel moved to holophonix_communication_panel.py