import bpy

class SNA_OT_ManageTrackHandlers(bpy.types.Operator):
    """
    Create or update track handlers based on current settings.
    Directly interacts with NodeOSC_keys collection.
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
        
        # Check if auto-management is disabled
        if not settings.auto_manage_handlers:
            if not self.auto_triggered:
                self.report({'INFO'}, "Auto-management is disabled. Use NodeOSC panel for individual settings.")
            return {'CANCELLED'}
        
        # Get tracks
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        if not tracks:
            if not self.auto_triggered:
                self.report({'WARNING'}, "No tracks found")
            return {'CANCELLED'}
            
        try:
            # Set the executing flag to prevent recursion
            SNA_OT_ManageTrackHandlers._is_executing = True
            
            # Update directions for all handlers (enabled or not)
            self.update_handler_directions(context, tracks, settings)
            
            # Clear existing track handlers (disable them)
            self.clear_existing_handlers(context)
            
            # Create new handlers based on settings
            created_count = self.create_handlers(context, tracks, settings)
            
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
        
    def clear_existing_handlers(self, context):
        """Disable all existing track handlers in NodeOSC_keys collection
        
        Instead of removing handlers, we now just disable them using the enable attribute.
        This is more efficient than removing and recreating handlers each time.
        """
        keys = context.scene.NodeOSC_keys
        
        # Disable all track handlers
        disabled_count = 0
        for item in keys:
            if "/track/" in item.osc_address and not "/track/*" in item.osc_address:
                item.enabled = False  # Note: NodeOSC uses 'enabled', not 'enable'
                disabled_count += 1
            
        # Print debug info
        print(f"Disabled {disabled_count} existing track handlers")
            
    def create_handlers(self, context, tracks, settings):
        """Create or enable handlers for each track based on settings"""
        created_count = 0
        enabled_count = 0
        
        for obj in tracks:
            try:
                # Extract track ID from name
                track_parts = obj.name.split(".")
                if len(track_parts) > 1:
                    index = track_parts[1]
                    id = int(index)
                else:
                    # If no dot in name, try to extract numeric part
                    id = ''.join(filter(str.isdigit, obj.name))
                    if not id:
                        continue
                    id = int(id)
                
                # Position handlers
                if settings.position_enabled:
                    result = self.handle_position_handler(context, obj, id, settings.position_direction)
                    created_count += result[0]
                    enabled_count += result[1]
                
                # Name handlers
                if settings.name_enabled:
                    result = self.handle_name_handler(context, obj, id, settings.name_direction)
                    created_count += result[0]
                    enabled_count += result[1]
                
                # Color handlers
                if settings.color_enabled:
                    result = self.handle_color_handler(context, obj, id, settings.color_direction)
                    created_count += result[0]
                    enabled_count += result[1]
                    
            except Exception as e:
                print(f"Error handling handlers for {obj.name}: {e}")
                
        print(f"Created {created_count} new handlers, enabled {enabled_count} existing handlers")
        return created_count + enabled_count
                
    def update_handler_directions(self, context, tracks, settings):
        """Update directions for all handlers regardless of enabled state"""
        keys = context.scene.NodeOSC_keys
        updated_count = 0
        
        # Process each track
        for obj in tracks:
            try:
                # Extract track ID from name
                track_parts = obj.name.split(".")
                if len(track_parts) > 1:
                    index = track_parts[1]
                    id = int(index)
                else:
                    # If no dot in name, try to extract numeric part
                    id = ''.join(filter(str.isdigit, obj.name))
                    if not id:
                        continue
                    id = int(id)
                
                # Update position handlers
                for axis, _ in [('x', 0), ('y', 1), ('z', 2)]:
                    osc_address = f"/track/{id}/{axis}"
                    for item in keys:
                        if item.osc_address == osc_address:
                            item.osc_direction = settings.position_direction
                            updated_count += 1
                
                # Update name handler
                osc_address = f"/track/{id}/name"
                for item in keys:
                    if item.osc_address == osc_address:
                        item.osc_direction = settings.name_direction
                        updated_count += 1
                
                # Update color handler
                osc_address = f"/track/{id}/color"
                for item in keys:
                    if item.osc_address == osc_address:
                        item.osc_direction = settings.color_direction
                        updated_count += 1
                        
            except Exception as e:
                print(f"Error updating directions for {obj.name}: {e}")
        
        print(f"Updated directions for {updated_count} handlers")
        return updated_count
    
    def handle_position_handler(self, context, obj, id, direction):
        """Create or enable position handlers (x, y, z) for a track
        
        Returns a tuple of (created_count, enabled_count)
        """
        created = 0
        enabled = 0
        keys = context.scene.NodeOSC_keys
        
        for axis, index in [('x', 0), ('y', 1), ('z', 2)]:
            # Check if handler already exists
            osc_address = f"/track/{id}/{axis}"
            data_path = f"bpy.data.objects['{obj.name}'].location[{index}]"
            
            # Look for existing handler
            existing = None
            for item in keys:
                if item.osc_address == osc_address and item.data_path == data_path:
                    existing = item
                    break
            
            # Create new or update existing
            if existing:
                # Update existing handler
                existing.enabled = True
                existing.osc_direction = direction
                enabled += 1
            else:
                # Create new handler
                item = keys.add()
                item.osc_address = osc_address
                item.data_path = data_path
                item.osc_type = "f"
                item.osc_direction = direction
                item.enabled = True
                created += 1
            
        return (created, enabled)
        
    def handle_name_handler(self, context, obj, id, direction):
        """Create or enable name handler for a track
        
        Returns a tuple of (created_count, enabled_count)
        """
        keys = context.scene.NodeOSC_keys
        osc_address = f"/track/{id}/name"
        data_path = f"bpy.data.objects['{obj.name}'].name"
        
        # Look for existing handler
        existing = None
        for item in keys:
            if item.osc_address == osc_address and item.data_path == data_path:
                existing = item
                break
        
        # Create new or update existing
        if existing:
            # Update existing handler
            existing.enabled = True
            existing.osc_direction = direction
            return (0, 1)  # 0 created, 1 enabled
        else:
            # Create new handler
            item = keys.add()
            item.osc_address = osc_address
            item.data_path = data_path
            item.osc_type = "s"
            item.osc_direction = direction
            item.enabled = True
            return (1, 0)  # 1 created, 0 enabled
        
    def handle_color_handler(self, context, obj, id, direction):
        """Create or enable color handler for a track
        
        Returns a tuple of (created_count, enabled_count)
        """
        keys = context.scene.NodeOSC_keys
        
        # Check if object has a material
        if not obj.active_material:
            return (0, 0)
        
        osc_address = f"/track/{id}/color"
        data_path = f"bpy.data.objects['{obj.name}'].active_material.diffuse_color"
        
        # Look for existing handler
        existing = None
        for item in keys:
            if item.osc_address == osc_address and item.data_path == data_path:
                existing = item
                break
        
        # Create new or update existing
        if existing:
            # Update existing handler
            existing.enabled = True
            existing.osc_direction = direction
            return (0, 1)  # 0 created, 1 enabled
        else:
            # Create new handler
            item = keys.add()
            item.osc_address = osc_address
            item.data_path = data_path
            item.osc_type = "f"
            item.osc_index = "(0,1,2,3)"
            item.osc_direction = direction
            item.enabled = True
            return (1, 0)  # 1 created, 0 enabled
