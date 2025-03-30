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
            # Track table (collapsable)
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(context.scene.holophonix_utils, "show_track_table", text="Track List", icon='TRIA_DOWN' if context.scene.holophonix_utils.show_track_table else 'TRIA_RIGHT', emboss=False)
            row.label(text=f"({len(tracks)} tracks)", icon='MESH_ICOSPHERE')

            if context.scene.holophonix_utils.show_track_table:
                table = col.column(align=True)
                # Add headers
                header_row = table.row()
                header_row.label(text="No. - Track Name", icon='LINENUMBERS_ON')

                # Add rows for each track
                for track in tracks:
                    # Extract track number and name from obj.name
                    parts = track.name.split('.')
                    if len(parts) >= 3 and parts[0] == "track":
                        track_number = parts[1]
                        track_name = '.'.join(parts[2:])  # Handle cases where NAME contains dots
                        row = table.row()
                        
                        # Make the entire row clickable with toggle state
                        is_selected = track in context.selected_objects
                        op = row.operator("sna.select_track", text=track_number+" - "+track_name, emboss=True, icon='CHECKBOX_HLT' if is_selected else 'CHECKBOX_DEHLT')
                        op.track_name = track.name
                        
                        # Add delete button                      
                        del_op = row.operator("sna.delete_track", text="", icon='TRASH')
                        del_op.track_name = track.name

                        # Add handler toggle button
                        if hasattr(context.scene, 'NodeOSC_keys'):
                            track_handlers = [
                                key for key in context.scene.NodeOSC_keys
                                if key.data_path and track.name in key.data_path
                            ]
                            handler_state = any(key.enabled for key in track_handlers)
                            toggle_op = row.operator('sna.toggle_track_handlers', text='', icon='CHECKBOX_HLT' if handler_state else 'CHECKBOX_DEHLT', emboss=False)
                            toggle_op.track_name = track.name

                        ### Add direction controls
                        ##if hasattr(context.scene, 'NodeOSC_keys'):
                        ##    # Group position handlers (x, y, z)
                        ##    position_handlers = [
                        ##        key for key in context.scene.NodeOSC_keys
                        ##        if any(axis in key.osc_address for axis in ['x', 'y', 'z']) 
                        ##        and track.name in key.data_path
                        ##    ]
                        ##    
                        ##    if position_handlers and position_handlers[0] is not None:
                        ##        row = table.row()
                        ##        row.label(text="Position Direction:")
                        ##        op = row.operator('sna.update_position_directions', text=position_handlers[0].osc_direction)
                        ##        op.track_name = track.name
                        ##        op.direction = position_handlers[0].osc_direction
                        ##    
                        ##    # Individual handlers for color and name

                            row = table.row()
                            row.label(text="X,Y,Z :")
                            row.prop(track.track_props, "location_direction", text="")

                            individual_handlers = ['color', 'name']
                            for handler_type in individual_handlers:
                                track_handlers = [
                                    key for key in context.scene.NodeOSC_keys
                                    if handler_type in key.osc_address and track.name in key.data_path
                                ]
                                if track_handlers:
                                    row = table.row()
                                    row.label(text=f"{handler_type.capitalize()} :")
                                    row.prop(track_handlers[0], 'osc_direction', text="")


                        
                                    
                                    
                        

                            

            # Track actions
            col = box.column(align=True)
            
            # All Tracks selection controls
            row = col.row(align=True)
            #row.scale_y = 1.2
            all_selected = len(context.selected_objects) == len(tracks)
            row.operator('sna.select_all_tracks', text='Select All Tracks' if not all_selected else 'Deselect All Tracks', icon='RESTRICT_SELECT_OFF' if not all_selected else 'RESTRICT_SELECT_ON')
            row.operator('sna.delete_all_tracks', text='', icon='TRASH')

            # Bulk handler controls
            #row = col.row(align=True)
            #row.operator('sna.enable_all_handlers', text='Enable All')
            #row.operator('sna.disable_all_handlers', text='Disable All')

            #row = col.row(align=True)
            #row = col.row(align=True)
            row.prop(context.scene.holophonix_scene_props, 'all_handlers_enabled', 
                text="", 
                icon='CHECKBOX_HLT' if context.scene.holophonix_scene_props.all_handlers_enabled else 'CHECKBOX_DEHLT')

            # Direction controls
            row = col.row(align=True)
            row.label(text="All Directions:")
            row.prop(context.scene.holophonix_scene_props, 'all_directions', text="")

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

        ### Add a note about AED properties requirement for track handlers
        ##if not hasattr(context.scene, 'azim'):
        ##    box = layout.box()
        ##    box.label(text="AED properties are required for track handlers", icon='ERROR')
        ##    col = box.column()
        ##    col.label(text="Please add AED properties using the 'Add Custom Properties' button")
        ##    col.operator('sna.add_aed_properties', text='Add AED Properties', icon='PLUS')
        
        # Note: Legacy global handler controls removed as they are no longer necessary
        # Individual handlers can now be controlled separately
    
    # Initialization is now handled by SNA_OT_InitializeTrackHandlers operator
    # Holophonix Communication panel moved to holophonix_communication_panel.py