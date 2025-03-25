import bpy
from ..utils.track_handler_proxy import get_manager


class SNA_OT_ManageTrackHandlers(bpy.types.Operator):
    """
    Create or update track handlers using the proxy system.
    Manages track handlers based on current settings and proxy state.
    """
    bl_idname = "sna.manage_track_handlers"
    bl_label = "Manage Track Handlers"
    bl_description = "Create or update track handlers based on current settings"
    
    # Class-level flag to prevent recursive execution
    _is_executing = False
    
    auto_triggered: bpy.props.BoolProperty(
        name="Auto Triggered",
        description="Whether this operator was triggered automatically by a property change",
        default=False
    )
    
    def execute(self, context):
        # Prevent recursive execution
        if SNA_OT_ManageTrackHandlers._is_executing:
            print("Preventing recursive execution of track handler management")
            return {'CANCELLED'}
            
        # Get manager and validate context
        manager = get_manager()
        if not manager:
            if not self.auto_triggered:
                self.report({'ERROR'}, "Track handler manager not available")
            return {'CANCELLED'}
            
        # Check if we have a valid context with a scene
        if not hasattr(context, 'scene'):
            if not self.auto_triggered:
                self.report({'ERROR'}, "No active scene available")
            return {'CANCELLED'}
            
        # Check if NodeOSC is available
        if not hasattr(context.scene, 'NodeOSC_keys'):
            if not self.auto_triggered:
                self.report({'ERROR'}, "NodeOSC is not available")
            return {'CANCELLED'}
            
        # Check if holophonix_utils is available
        if not hasattr(context.scene, 'holophonix_utils'):
            if not self.auto_triggered:
                self.report({'ERROR'}, "Holophonix Utils is not properly initialized")
            return {'CANCELLED'}
            
        # Get settings
        settings = context.scene.holophonix_utils.track_handler_settings
        if not settings:
            if not self.auto_triggered:
                self.report({'ERROR'}, "No track handler settings available")
            return {'CANCELLED'}
            
        # Check if auto-management is disabled
        if not settings.auto_manage_handlers:
            if not self.auto_triggered:
                self.report({'INFO'}, "Auto-management is disabled. Use NodeOSC panel for individual settings.")
            return {'CANCELLED'}
            
        # Get tracks
        tracks = self._get_tracks(context)
        if not tracks:
            if not self.auto_triggered:
                self.report({'WARNING'}, "No tracks found")
            return {'CANCELLED'}
            
        # Process tracks through proxy system
        try:
            # Set the executing flag to prevent recursion
            SNA_OT_ManageTrackHandlers._is_executing = True
            
            result = self._process_tracks(manager, tracks, settings)
            
            # Force a UI update to reflect the changes
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
            
            if self.auto_triggered:
                print(f"Updated track handlers based on new settings")
            else:
                self.report({'INFO'}, f"Track handlers updated successfully")
            return {'FINISHED'}
        finally:
            # Always clear the executing flag
            SNA_OT_ManageTrackHandlers._is_executing = False
        
    def _process_tracks(self, manager, tracks, settings):
        """Process tracks using the proxy system"""
        processed_count = 0
        
        for obj in tracks:
            try:
                # Get track name
                track_name = obj.name
                
                # Find handlers for this track
                handlers = [h for h in bpy.context.scene.NodeOSC_keys 
                          if track_name in h.data_path]
                
                if not handlers:
                    print(f"No handlers found for track {track_name}")
                    continue
                    
                # Process each handler
                for handler in handlers:
                    # Get or create proxy
                    proxy = self._get_or_create_proxy(manager, obj)
                    if not proxy:
                        continue
                        
                    # Update proxy with current settings
                    self._update_proxy_settings(proxy, settings)
                    
                    # Apply handler changes
                    processed_count += self._apply_handler_changes(proxy)
                    
            except Exception as e:
                print(f"Error processing track {obj.name}: {e}")
                
        return processed_count
        
    def _get_or_create_proxy(self, manager, obj):
        """Get or create a proxy for the track"""
        track_id = self._extract_track_id(obj)
        if not track_id:
            return None
        return manager.get_proxy(track_id)
        
    def _extract_track_id(self, obj):
        """Extract track ID from object name"""
        track_parts = obj.name.split(".")
        if len(track_parts) > 1:
            return track_parts[1]
        return ''.join(filter(str.isdigit, obj.name))
        
    def _update_proxy_settings(self, proxy, settings):
        """Update proxy with current settings"""
        proxy.set_attr('position_enabled', settings.position_enabled)
        proxy.set_attr('position_direction', settings.position_direction)
        proxy.set_attr('name_enabled', settings.name_enabled)
        proxy.set_attr('name_direction', settings.name_direction)
        proxy.set_attr('color_enabled', settings.color_enabled)
        proxy.set_attr('color_direction', settings.color_direction)
        
    def _apply_handler_changes(self, proxy):
        """Apply handler changes based on proxy state"""
        # Implementation would use proxy.has_changed() to determine
        # which handlers need updating
        return 1
        
    def _get_tracks(self, context):
        """Get tracks from the scene"""
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        return tracks