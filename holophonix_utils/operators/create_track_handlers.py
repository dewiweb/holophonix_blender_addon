import bpy
import socket
import threading
import time
from bpy.props import StringProperty

class SNA_OT_CreateTrackHandlers(bpy.types.Operator):
    bl_idname = "sna.create_track_handlers"
    bl_label = "Create Track Handlers"
    bl_description = "Create NodeOSC handlers based on selected categories"
    bl_options = {"REGISTER", "UNDO"}
    
    set_port_only: bpy.props.BoolProperty(
        name="Set Port Only",
        description="Only set the NodeOSC port without creating handlers",
        default=False,
        options={"SKIP_SAVE", "HIDDEN"}
    )
    
    resolve_hostname_only: bpy.props.BoolProperty(
        name="Resolve Hostname Only",
        description="Only resolve the Holophonix hostname and set UDP output",
        default=False,
        options={"SKIP_SAVE", "HIDDEN"}
    )
    
    def execute(self, context):
        # Check if NodeOSC is available
        if not self.check_nodeosc_available(context):
            return {'CANCELLED'}
        
        # Handle the different modes of operation
        if self.set_port_only:
            # Set only the port, don't resolve hostname
            self.set_nodeosc_port(context, resolve_hostname=False)
            return {'FINISHED'}
            
        if self.resolve_hostname_only:
            # Only resolve hostname, don't set port
            self.resolve_holophonix_hostname(context)
            return {'FINISHED'}
            
        # Get track objects
        tracks = [obj for obj in context.scene.objects if "track" in obj.name]
        if not tracks:
            self.report({"WARNING"}, "No track objects found")
            return {'CANCELLED'}
            
        # Get track handler properties
        props = context.scene.holophonix_utils
        track_handlers = props.track_handlers
        
        # When creating handlers, we also want to ensure the port and UDP out are correctly set
        # This is separate from the buttons that only do one specific task
        self.set_nodeosc_port(context, resolve_hostname=True)
        
        # First, clean up any handlers that should no longer exist based on enabled state
        self.update_existing_handlers(context, track_handlers)
        
        # Create handlers for each category
        created_count = 0
        updated_count = 0
        
        # Position handlers
        if track_handlers.position.enabled:
            direction = track_handlers.position.direction
            for obj in tracks:
                try:
                    index = obj.name.split(".")[1]
                    id = int(index)
                    
                    if direction in ['INPUT', 'BOTH']:
                        result = self.create_track_handler(context, obj, id, "x", 0, "INPUT")
                        result += self.create_track_handler(context, obj, id, "y", 1, "INPUT")
                        result += self.create_track_handler(context, obj, id, "z", 2, "INPUT")
                        if result == 0:
                            updated_count += 3
                        else:
                            created_count += result
                        
                    if direction in ['OUTPUT', 'BOTH']:
                        result = self.create_track_handler(context, obj, id, "x", 0, "OUTPUT")
                        result += self.create_track_handler(context, obj, id, "y", 1, "OUTPUT")
                        result += self.create_track_handler(context, obj, id, "z", 2, "OUTPUT")
                        if result == 0:
                            updated_count += 3
                        else:
                            created_count += result
                except Exception as e:
                    self.report({"ERROR"}, f"Error creating position handlers for {obj.name}: {str(e)}")
        
        # Name handlers
        if track_handlers.name.enabled:
            direction = track_handlers.name.direction
            for obj in tracks:
                try:
                    index = obj.name.split(".")[1]
                    id = int(index)
                    
                    if direction in ['INPUT', 'BOTH']:
                        result = self.create_name_handler(context, obj, id, "INPUT")
                        if result == 0:
                            updated_count += 1
                        else:
                            created_count += result
                        
                    if direction in ['OUTPUT', 'BOTH']:
                        result = self.create_name_handler(context, obj, id, "OUTPUT")
                        if result == 0:
                            updated_count += 1
                        else:
                            created_count += result
                except Exception as e:
                    self.report({"ERROR"}, f"Error creating name handlers for {obj.name}: {str(e)}")
        
        # Color handlers
        if track_handlers.color.enabled:
            direction = track_handlers.color.direction
            for obj in tracks:
                try:
                    index = obj.name.split(".")[1]
                    id = int(index)
                    
                    if direction in ['INPUT', 'BOTH']:
                        result = self.create_color_handler(context, obj, id, "INPUT")
                        if result == 0:
                            updated_count += 1
                        else:
                            created_count += result
                        
                    if direction in ['OUTPUT', 'BOTH']:
                        result = self.create_color_handler(context, obj, id, "OUTPUT")
                        if result == 0:
                            updated_count += 1
                        else:
                            created_count += result
                except Exception as e:
                    self.report({"ERROR"}, f"Error creating color handlers for {obj.name}: {str(e)}")
                    
        # Update legacy properties
        track_handlers.update_legacy_properties(context)
        
        # Ensure track_handlers_initialized is set to True
        props.track_handlers_initialized = True
        
        # Prepare a detailed report
        if created_count > 0 and updated_count > 0:
            self.report({"INFO"}, f"Created {created_count} new handlers and updated {updated_count} existing handlers")
        elif created_count > 0:
            self.report({"INFO"}, f"Created {created_count} new handlers")
        elif updated_count > 0:
            self.report({"INFO"}, f"Updated {updated_count} existing handlers")
        else:
            self.report({"INFO"}, "No handlers needed to be created or updated")
            
        return {"FINISHED"}
        
    def update_existing_handlers(self, context, track_handlers):
        """Update or remove existing handlers based on current settings"""
        if not hasattr(context.scene, 'NodeOSC_keys'):
            return
            
        # Store handlers to be removed
        handlers_to_remove = []
        
        # Check each handler and disable or update as needed
        for idx, item in enumerate(context.scene.NodeOSC_keys):
            # Skip non-track handlers
            if not "/track/" in item.osc_address:
                continue
                
            # Extract track ID and property type
            parts = item.osc_address.split('/')
            if len(parts) < 4:
                continue
                
            track_id = parts[2]
            prop_type = parts[3]
            
            # Position handlers (x, y, z)
            if prop_type in ["x", "y", "z"]:
                if not track_handlers.position.enabled:
                    # Mark for removal if position is disabled
                    handlers_to_remove.append(idx)
                elif item.osc_direction == "INPUT" and track_handlers.position.direction not in ["INPUT", "BOTH"]:
                    # Mark for removal if direction doesn't match
                    handlers_to_remove.append(idx)
                elif item.osc_direction == "OUTPUT" and track_handlers.position.direction not in ["OUTPUT", "BOTH"]:
                    # Mark for removal if direction doesn't match
                    handlers_to_remove.append(idx)
            
            # Name handlers
            elif prop_type == "name":
                if not track_handlers.name.enabled:
                    # Mark for removal if name is disabled
                    handlers_to_remove.append(idx)
                elif item.osc_direction == "INPUT" and track_handlers.name.direction not in ["INPUT", "BOTH"]:
                    # Mark for removal if direction doesn't match
                    handlers_to_remove.append(idx)
                elif item.osc_direction == "OUTPUT" and track_handlers.name.direction not in ["OUTPUT", "BOTH"]:
                    # Mark for removal if direction doesn't match
                    handlers_to_remove.append(idx)
            
            # Color handlers
            elif prop_type == "color":
                if not track_handlers.color.enabled:
                    # Mark for removal if color is disabled
                    handlers_to_remove.append(idx)
                elif item.osc_direction == "INPUT" and track_handlers.color.direction not in ["INPUT", "BOTH"]:
                    # Mark for removal if direction doesn't match
                    handlers_to_remove.append(idx)
                elif item.osc_direction == "OUTPUT" and track_handlers.color.direction not in ["OUTPUT", "BOTH"]:
                    # Mark for removal if direction doesn't match
                    handlers_to_remove.append(idx)
        
        # Remove handlers in reverse order to avoid index issues
        for idx in sorted(handlers_to_remove, reverse=True):
            context.scene.NodeOSC_keys.remove(idx)
    
    def create_track_handler(self, context, obj, id, axis, index, direction):
        """Create or update a track position handler"""
        # Check if handler already exists with this direction
        osc_address = f"/track/{id}/{axis}"
        for key in context.scene.NodeOSC_keys:
            if key.osc_address == osc_address and key.osc_direction == direction:
                # Handler already exists, make sure it's enabled
                key.enabled = True
                return 0  # Return 0 for updated
        
        # Create new handler
        item = context.scene.NodeOSC_keys.add()
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].matrix_world.translation[{index}]"
        item.osc_type = "f"
        item.osc_index = "()"
        item.osc_direction = direction
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = True
        item.ui_expanded = False
        return 1  # Return 1 for created
        
    def create_name_handler(self, context, obj, id, direction):
        """Create or update a track name handler"""
        # Check if handler already exists with this direction
        osc_address = f"/track/{id}/name"
        for key in context.scene.NodeOSC_keys:
            if key.osc_address == osc_address and key.osc_direction == direction:
                # Handler already exists, make sure it's enabled
                key.enabled = True
                return 0  # Return 0 for updated
        
        # Create new handler
        item = context.scene.NodeOSC_keys.add()
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].name"
        item.osc_type = "s"
        item.osc_index = "(0)"
        item.osc_direction = direction
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = True
        item.ui_expanded = False
        return 1  # Return 1 for created
        
    def create_color_handler(self, context, obj, id, direction):
        """Create or update a track color handler"""
        # Check if handler already exists with this direction
        osc_address = f"/track/{id}/color"
        for key in context.scene.NodeOSC_keys:
            if key.osc_address == osc_address and key.osc_direction == direction:
                # Handler already exists, make sure it's enabled
                key.enabled = True
                return 0  # Return 0 for updated
        
        # Create new handler
        item = context.scene.NodeOSC_keys.add()
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].color"
        item.osc_type = "f"
        item.osc_index = "(0,1,2,3)"
        item.osc_direction = direction
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = True
        item.ui_expanded = False
        return 1  # Return 1 for created
        
    def check_nodeosc_available(self, context):
        """Check if NodeOSC is available and properly set up"""
        if "NodeOSC" not in context.preferences.addons:
            self.report({'ERROR'}, "NodeOSC addon is not installed")
            return False
            
        if not hasattr(context.scene, 'NodeOSC_keys'):
            self.report({'ERROR'}, "NodeOSC keys collection not found")
            return False
            
        return True
        
    def resolve_holophonix_hostname(self, context, hostname="holophonix.local"):
        """Resolve the Holophonix hostname to an IP address"""
        # If we already have a resolved IP address, use it directly
        if hasattr(context.scene, 'holophonix_utils') and hasattr(context.scene.holophonix_utils, 'holophonix_ip'):
            ip = context.scene.holophonix_utils.holophonix_ip
            if ip and hasattr(context.scene, 'nodeosc_envars'):
                # Set the NodeOSC UDP output to the resolved IP
                old_udp = context.scene.nodeosc_envars.udp_out
                context.scene.nodeosc_envars.udp_out = ip
                self.report({'INFO'}, f"NodeOSC UDP output set to {ip} (was {old_udp})")
                return
                
        # No IP available yet, trigger the background resolution
        bpy.ops.sna.resolve_holophonix_hostname('INVOKE_DEFAULT')
        return
        
    def set_nodeosc_port(self, context, resolve_hostname=True):
        """Set NodeOSC output port to 4003 for Holophonix compatibility"""
        try:
            # Access NodeOSC environmental variables
            if hasattr(context.scene, 'nodeosc_envars'):
                if context.scene.nodeosc_envars.port_out != 4003:
                    # Store the old port for reporting
                    old_port = context.scene.nodeosc_envars.port_out
                    
                    # Set output port to 4003 (Holophonix input port)
                    context.scene.nodeosc_envars.port_out = 4003
                    
                    self.report({'INFO'}, f"NodeOSC output port changed from {old_port} to 4003 for Holophonix compatibility")
                else:
                    self.report({'INFO'}, "NodeOSC output port already set to 4003 for Holophonix compatibility")
                        
                # Try to resolve the Holophonix hostname and set UDP out (if requested)
                if resolve_hostname:
                    self.resolve_holophonix_hostname(context)
        except Exception as e:
            # Just log the error but don't fail if this doesn't work
            print(f"Could not set NodeOSC output port: {str(e)}")
            self.report({'ERROR'}, f"Could not set NodeOSC output port: {str(e)}")
        
    def set_nodeosc_port(self, context, resolve_hostname=True):
        """Set NodeOSC output port to 4003 for Holophonix compatibility"""
        try:
            # Access NodeOSC environmental variables
            if hasattr(context.scene, 'nodeosc_envars'):
                if context.scene.nodeosc_envars.port_out != 4003:
                    # Store the old port for reporting
                    old_port = context.scene.nodeosc_envars.port_out
                    
                    # Set output port to 4003 (Holophonix input port)
                    context.scene.nodeosc_envars.port_out = 4003
                    
                    self.report({'INFO'}, f"NodeOSC output port changed from {old_port} to 4003 for Holophonix compatibility")
                else:
                    self.report({'INFO'}, "NodeOSC output port already set to 4003 for Holophonix compatibility")
                        
                # Try to resolve the Holophonix hostname and set UDP out (if requested)
                if resolve_hostname:
                    self.resolve_holophonix_hostname(context)
        except Exception as e:
            # Just log the error but don't fail if this doesn't work
            print(f"Could not set NodeOSC output port: {str(e)}")
            self.report({'ERROR'}, f"Could not set NodeOSC output port: {str(e)}")
        

class SNA_OT_ResolveHolophonixHostname(bpy.types.Operator):
    """Resolve the Holophonix hostname to an IP address in the background"""
    bl_idname = "sna.resolve_holophonix_hostname"
    bl_label = "Resolve Holophonix Hostname"
    bl_options = {"REGISTER"}
    
    hostname: StringProperty(
        name="Hostname",
        description="The hostname to resolve",
        default="holophonix.local"
    )
    
    def execute(self, context):
        # We don't actually do anything in execute
        # This just makes the operator appear to finish immediately
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Start the background thread to resolve the hostname
        thread = threading.Thread(target=self._resolve_hostname_thread, args=(context, self.hostname))
        thread.daemon = True
        thread.start()
        return {'FINISHED'}
        
    def _resolve_hostname_thread(self, context, hostname):
        """Background thread function to resolve hostname"""
        try:
            # Try to resolve the hostname
            ip_address = socket.gethostbyname(hostname)
            print(f"Resolved {hostname} to {ip_address}")
            
            # Store the resolved IP in the scene properties
            # Run in the main thread to update Blender properties
            def update_holophonix_ip():
                try:
                    # Store the resolved IP
                    context.scene.holophonix_utils.holophonix_ip = ip_address
                    
                    # Update the NodeOSC UDP output if available
                    if hasattr(context.scene, 'nodeosc_envars'):
                        # Don't override existing custom value with 127.0.0.1
                        if ip_address != "127.0.0.1" or context.scene.nodeosc_envars.udp_out == "":
                            context.scene.nodeosc_envars.udp_out = ip_address
                            print(f"NodeOSC UDP output set to {ip_address}")
                            
                    return None  # Remove timer
                except Exception as e:
                    print(f"Error updating holophonix IP: {str(e)}")
                    return None  # Remove timer
                
            # Schedule the update in the main thread
            bpy.app.timers.register(update_holophonix_ip, first_interval=0.1)
            
        except socket.gaierror:
            # Handle hostname resolution failure
            print(f"Could not resolve hostname {hostname}")
            return
        except Exception as e:
            # Handle any other errors
            print(f"Error resolving hostname: {str(e)}")
            return
    
    
        # Keep the original method for backward compatibility, but use a different implementation
        def resolver_thread(hostname, context, operator):
            try:
                # Attempt to resolve the hostname
                ip_address = socket.gethostbyname(hostname)
                print(f"Resolved {hostname} to {ip_address}")
                
                # Update NodeOSC settings if we found an IP
                if hasattr(context.scene, 'nodeosc_envars'):
                    # Use a timer to run this on the main thread
                    def update_udp_out():
                        try:
                            current_udp = context.scene.nodeosc_envars.udp_out
                            context.scene.nodeosc_envars.udp_out = ip_address
                            if operator.set_port_only:
                                if current_udp != ip_address:
                                    operator.report({'INFO'}, f"Set NodeOSC UDP output to {ip_address}")
                                else:
                                    operator.report({'INFO'}, f"NodeOSC UDP output already set to {ip_address}")
                        except Exception as e:
                            print(f"Error setting UDP out: {str(e)}")
                            if operator.set_port_only:
                                operator.report({'ERROR'}, f"Error setting UDP out: {str(e)}")
                        return None  # Remove timer
                    
                    bpy.app.timers.register(update_udp_out, first_interval=0.5)
            except socket.gaierror:
                # Could not resolve hostname
                print(f"Could not resolve hostname {hostname}")
                if operator.set_port_only:
                    def show_error():
                        operator.report({'WARNING'}, f"Could not resolve Holophonix hostname {hostname}")
                        return None  # Remove timer
                    bpy.app.timers.register(show_error, first_interval=0.5)
            except Exception as e:
                print(f"Error resolving hostname: {str(e)}")
                if operator.set_port_only:
                    def show_error():
                        operator.report({'ERROR'}, f"Error resolving hostname: {str(e)}")
                        return None  # Remove timer
                    bpy.app.timers.register(show_error, first_interval=0.5)
        
        # Start the resolver in a background thread to avoid blocking the UI
        thread = threading.Thread(target=resolver_thread, args=(hostname, context, self))
        thread.daemon = True
        thread.start()
