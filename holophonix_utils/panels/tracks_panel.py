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
        
        # Note: Track handlers configuration is now in a sub-panel
        # See track_handlers_panel.py for the implementation
        
        # Add a note about NodeOSC requirement for track handlers
        if not hasattr(context.scene, 'NodeOSC_keys'):
            box = layout.box()
            box.label(text="NodeOSC addon is required for track handlers", icon='ERROR')
            col = box.column()
            col.label(text="Please install and enable the NodeOSC addon")
        
        # Note: Legacy global handler controls removed as they are no longer necessary
        # Individual handlers can now be controlled separately
    
    # Initialization is now handled by SNA_OT_InitializeTrackHandlers operator
    # Holophonix Communication panel moved to holophonix_communication_panel.py