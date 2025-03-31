import bpy
import socket
import threading
import time
from bpy.props import StringProperty

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
        # Wait 10 seconds before first attempt
        time.sleep(10)
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


class SNA_OT_HolophonixCommunication(bpy.types.Operator):
    """
    Operator for managing Holophonix communication settings.
    Handles port configuration and hostname resolution.
    """
    bl_idname = "sna.holophonix_communication"
    bl_label = "Holophonix Communication"
    bl_description = "Configure Holophonix communication settings"
    
    set_port_only: bpy.props.BoolProperty(
        name="Set Port Only",
        description="Only set the NodeOSC port without resolving hostname",
        default=False
    )
    
    apply_ip_only: bpy.props.BoolProperty(
        name="Apply IP Only",
        description="Only apply the resolved IP address",
        default=False
    )
    
    def execute(self, context):
        # Check if NodeOSC is available
        if not self.check_nodeosc_available(context):
            return {'CANCELLED'}
        
        # Handle the different modes of operation
        if self.set_port_only:
            # Set only the port
            self.set_nodeosc_port(context)
            return {'FINISHED'}
            
        if self.apply_ip_only:
            # Only apply the resolved IP address
            self.apply_resolved_ip(context)
            return {'FINISHED'}
            
        # If no specific mode is selected, do both
        self.set_nodeosc_port(context)
        self.apply_resolved_ip(context)
        
        return {'FINISHED'}
    
    def check_nodeosc_available(self, context):
        """Check if NodeOSC addon is available and enabled"""
        if not hasattr(context.scene, 'nodeosc_envars'):
            self.report({'ERROR'}, "NodeOSC addon is not enabled")
            return False
        return True
    
    def set_nodeosc_port(self, context):
        """Set the NodeOSC port to 4003 (Holophonix default)"""
        if hasattr(context.scene, 'nodeosc_envars'):
            context.scene.nodeosc_envars.port_out = 4003
            self.report({'INFO'}, "Set NodeOSC port to 4003")
            return True
        return False
    
    def apply_resolved_ip(self, context):
        """Apply the resolved Holophonix IP address to NodeOSC UDP out"""
        if not hasattr(context.scene, 'holophonix_utils') or not hasattr(context.scene.holophonix_utils, 'holophonix_ip'):
            self.report({'WARNING'}, "No Holophonix IP address available")
            return False
            
        ip = context.scene.holophonix_utils.holophonix_ip
        if not ip:
            self.report({'WARNING'}, "No Holophonix IP address resolved")
            return False
            
        # Set the UDP out address
        context.scene.nodeosc_envars.udp_out = ip
        self.report({'INFO'}, f"Applied Holophonix IP address: {ip}")
        return True
