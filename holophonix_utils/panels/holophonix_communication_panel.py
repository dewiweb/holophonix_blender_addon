import bpy
import traceback

class SNA_PT_HolophonixNodeOSC(bpy.types.Panel):
    bl_label = 'Holophonix Communication'
    bl_idname = 'SNA_PT_HOLOPHONIX_NODEOSC'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_MAIN_PANEL'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        # Only show this panel if NodeOSC is installed and enabled
        return "NodeOSC" in context.preferences.addons and hasattr(context.scene, 'nodeosc_envars')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='NETWORK_DRIVE')

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        box = col.box()
        
        # Panel title
        box.label(text="NodeOSC Configuration for Holophonix", icon='SETTINGS')
        
        # Current status section
        status_box = box.box()
        status_box.label(text="Current Status:", icon='INFO')
        
        # Current NodeOSC port settings
        row = status_box.row()
        row.label(text=f"NodeOSC output port: {context.scene.nodeosc_envars.port_out} (Should be 4003)")
        
        # Current NodeOSC UDP out settings
        row = status_box.row()
        row.label(text=f"NodeOSC UDP output: {context.scene.nodeosc_envars.udp_out}")
        
        # Hostname info and resolution status
        row = status_box.row()
        hostname_text = "Hostname: holophonix.local"
        
        # Check if IP is resolved
        has_ip = hasattr(context.scene.holophonix_utils, 'holophonix_ip') and context.scene.holophonix_utils.holophonix_ip
        
        if has_ip:
            # Show resolved status with IP
            ip = context.scene.holophonix_utils.holophonix_ip
            row.label(text=f"{hostname_text} → Resolved to {ip}", icon='CHECKMARK')
        else:
            # Show unresolved status
            row.label(text=f"{hostname_text} → Not resolved", icon='ERROR')
        
        # Configuration section
        config_box = box.box()
        config_box.label(text="Configure Connection:", icon='MODIFIER')
        
        # Port configuration button
        port_row = config_box.row()
        port_op = port_row.operator("sna.holophonix_communication", 
                              text="Set Port to 4003", 
                              icon='CHECKMARK' if context.scene.nodeosc_envars.port_out == 4003 else 'ERROR')
        port_op.set_port_only = True
        port_op.apply_ip_only = False
        
        # If holophonix_ip is stored in scene props, show the UI to apply it
        if hasattr(context.scene, 'holophonix_utils') and hasattr(context.scene.holophonix_utils, 'holophonix_ip'):
            ip = context.scene.holophonix_utils.holophonix_ip
            if ip:
                # Show IP with apply button
                ip_row = config_box.row()
                ip_row.label(text=f"Found Holophonix at: {ip}", icon='CHECKMARK')
                
                # Only show Apply button if the IP doesn't match current UDP out
                if context.scene.nodeosc_envars.udp_out != ip:
                    apply_row = config_box.row()
                    hostname_op = apply_row.operator("sna.holophonix_communication", 
                                                text=f"Apply IP Address", 
                                                icon='URL')
                    hostname_op.set_port_only = False
                    hostname_op.apply_ip_only = True
                else:
                    ip_status_row = config_box.row()
                    ip_status_row.label(text="IP is already set correctly", icon='CHECKMARK')
        else:
            # Attempt to resolve in the background
            config_box.label(text="Attempting to resolve holophonix.local...", icon='INFO')
            
            # Start the background resolver
            # This uses a convenience function to trigger resolution without a button press
            bpy.ops.sna.resolve_holophonix_hostname('INVOKE_DEFAULT')
        
        # Configuration status
        if context.scene.nodeosc_envars.port_out == 4003 and context.scene.nodeosc_envars.udp_out != "127.0.0.1" and context.scene.nodeosc_envars.udp_out:
            config_box.label(text="NodeOSC correctly configured for Holophonix", icon='CHECKMARK')
            
        # Note: Handler management section removed as it's no longer necessary
