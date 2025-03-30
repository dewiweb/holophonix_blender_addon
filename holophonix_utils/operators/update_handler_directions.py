import bpy

class SNA_OT_UpdateHandlerDirections(bpy.types.Operator):
    bl_idname = 'sna.update_handler_directions'
    bl_label = 'Update Handler Directions'
    bl_options = {'REGISTER', 'UNDO'}

    track_name: bpy.props.StringProperty()
    handler_type: bpy.props.StringProperty()
    direction: bpy.props.StringProperty()

    def execute(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            track_handlers = [
                key for key in context.scene.NodeOSC_keys
                if key.data_path and self.track_name in key.data_path
            ]
            for handler_type in ['x', 'y', 'z', 'color', 'name']:
                prop_name = f"{self.track_name}_{handler_type}_direction"
                if hasattr(context.scene, prop_name):
                    direction = getattr(context.scene, prop_name)
                    handler = next((h for h in track_handlers if handler_type in h.data_path), None)
                    if handler:
                        handler.direction = direction
        return {'FINISHED'}

class SNA_OT_UpdatePositionDirections(bpy.types.Operator):
    bl_idname = "sna.update_position_directions"
    bl_label = "Update Position Directions"
    
    direction: bpy.props.EnumProperty(
        name="Direction",
        items=[
            ('INPUT', "Input", "Receive data"),
            ('OUTPUT', "Output", "Send data"), 
            ('BOTH', "Both", "Send and receive")
        ]
    )
    track_name: bpy.props.StringProperty(name="Track Name")
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'direction', text="Direction")
    
    def execute(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            position_handlers = [
                key for key in context.scene.NodeOSC_keys
                if any(axis in key.osc_address for axis in ['x', 'y', 'z']) 
                and self.track_name in key.data_path
            ]
            for handler in position_handlers:
                handler.osc_direction = self.direction
        return {'FINISHED'}
