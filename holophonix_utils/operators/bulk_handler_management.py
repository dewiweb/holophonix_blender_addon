import bpy

class SNA_OT_EnableAllHandlers(bpy.types.Operator):
    bl_idname = "sna.enable_all_handlers"
    bl_label = "Enable All Handlers"
    
    def execute(self, context):
        for key in context.scene.NodeOSC_keys:
            if '/track/' in key.osc_address:
                key.enabled = True
        return {'FINISHED'}

class SNA_OT_DisableAllHandlers(bpy.types.Operator):
    bl_idname = "sna.disable_all_handlers"
    bl_label = "Disable All Handlers"
    
    def execute(self, context):
        for key in context.scene.NodeOSC_keys:
            if '/track/' in key.osc_address:
                key.enabled = False
        return {'FINISHED'}

class SNA_OT_ToggleAllHandlers(bpy.types.Operator):
    bl_idname = 'sna.toggle_all_handlers'
    bl_label = 'Toggle All Handlers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            # Get all track handlers
            track_handlers = [
                key for key in context.scene.NodeOSC_keys
                if '/track/' in key.osc_address
            ]
            
            if track_handlers:
                # Update handlers based on property state
                enabled = context.scene.holophonix_scene_props.all_handlers_enabled
                for key in track_handlers:
                    key.enabled = enabled
                
                return {'FINISHED'}
        return {'CANCELLED'}

class SNA_OT_SetAllDirections(bpy.types.Operator):
    bl_idname = "sna.set_all_directions"
    bl_label = "Set All Directions"
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.StringProperty()  # Changed from EnumProperty
    
    def execute(self, context):
        for obj in context.scene.objects:
            if "track" in obj.name:
                # Update track property
                obj.track_props.location_direction = self.direction
                
                # Update OSC handlers
                for key in context.scene.NodeOSC_keys:
                    if obj.name in key.data_path:
                        key.osc_direction = self.direction
        return {'FINISHED'}

class SNA_OT_ToggleLocationHandlers(bpy.types.Operator):
    bl_idname = 'sna.toggle_location_handlers'
    bl_label = 'Toggle Location Handlers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            # Get location handlers
            location_handlers = [
                key for key in context.scene.NodeOSC_keys
                if any(axis in key.osc_address for axis in ['/x', '/y', '/z'])
            ]
            
            if location_handlers:
                # Update handlers based on property state
                enabled = context.scene.holophonix_scene_props.location_handlers_enabled
                for key in location_handlers:
                    key.enabled = enabled
                
                return {'FINISHED'}
        return {'CANCELLED'}

class SNA_OT_SetLocationDirections(bpy.types.Operator):
    bl_idname = "sna.set_location_directions"
    bl_label = "Set Location Directions"
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.StringProperty()
    
    def execute(self, context):
        for obj in context.scene.objects:
            if "track" in obj.name:
                # Update track property
                obj.track_props.location_direction = self.direction
                
                # Update OSC handlers
                for key in context.scene.NodeOSC_keys:
                    if any(axis in key.osc_address for axis in ['/x', '/y', '/z']):
                        key.osc_direction = self.direction
        return {'FINISHED'}

class SNA_OT_ToggleColorHandlers(bpy.types.Operator):
    bl_idname = 'sna.toggle_color_handlers'
    bl_label = 'Toggle Color Handlers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            # Get color handlers
            color_handlers = [
                key for key in context.scene.NodeOSC_keys
                if "/color" in key.osc_address
            ]
            
            if color_handlers:
                # Update handlers based on property state
                enabled = context.scene.holophonix_scene_props.color_handlers_enabled
                for key in color_handlers:
                    key.enabled = enabled
                
                return {'FINISHED'}
        return {'CANCELLED'}

class SNA_OT_SetColorDirections(bpy.types.Operator):
    bl_idname = "sna.set_color_directions"
    bl_label = "Set Color Directions"
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.StringProperty()
    
    def execute(self, context):
        for obj in context.scene.objects:
            if "track" in obj.name:
                # Update track property
                obj.track_props.color_direction = self.direction
                
                # Update OSC handlers
                for key in context.scene.NodeOSC_keys:
                    if "/color" in key.osc_address:
                        key.osc_direction = self.direction
        return {'FINISHED'}

class SNA_OT_ToggleNameHandlers(bpy.types.Operator):
    bl_idname = 'sna.toggle_name_handlers'
    bl_label = 'Toggle Name Handlers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            # Get name handlers
            name_handlers = [
                key for key in context.scene.NodeOSC_keys
                if '/name' in key.osc_address
            ]
            
            if name_handlers:
                # Update handlers based on property state
                enabled = context.scene.holophonix_scene_props.name_handlers_enabled
                for key in name_handlers:
                    key.enabled = enabled
                
                return {'FINISHED'}
        return {'CANCELLED'}

class SNA_OT_SetNameDirections(bpy.types.Operator):
    bl_idname = "sna.set_name_directions"
    bl_label = "Set Name Directions"
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.StringProperty()
    
    def execute(self, context):
        for obj in context.scene.objects:
            if "track" in obj.name:
                # Update track property
                obj.track_props.name_direction = self.direction
                
                # Update OSC handlers
                for key in context.scene.NodeOSC_keys:
                    if '/name' in key.osc_address:
                        key.osc_direction = self.direction
        return {'FINISHED'}