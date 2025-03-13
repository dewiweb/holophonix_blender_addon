import bpy

class SNA_OT_ExportAndCreateHandlers(bpy.types.Operator):
    bl_idname = "sna.export_create_handlers"
    bl_label = "Create NodeOSC Handlers for Tracks"
    bl_description = "Export tracks and create OSC handlers in one step"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Get track objects
        tracks = [obj for obj in bpy.context.scene.objects if "track" in obj.name]
        if not tracks:
            self.report({"WARNING"}, "No track objects found")
            return {"CANCELLED"}

        # Create OSC handlers
        for obj in tracks:
            try:
                index = obj.name.split(".")[1]
                id = int(index)
                
                # Create track position handlers
                self.create_track_handler(context, obj, id, "x", 0)
                self.create_track_handler(context, obj, id, "y", 1)
                self.create_track_handler(context, obj, id, "z", 2)
                
                # Create track color handler
                self.create_color_handler(context, obj, id)
                
                # Create track name handler
                self.create_name_handler(context, obj, id)
                
            except Exception as e:
                self.report({"ERROR"}, f"Error creating handlers for {obj.name}: {str(e)}")
                continue

        self.report({"INFO"}, f"Created handlers for {len(tracks)} tracks")
        return {"FINISHED"}

    def create_track_handler(self, context, obj, id, axis, index):
        # Check if handler already exists
        osc_address = f"/track/{id}/{axis}"
        if any(key.osc_address == osc_address for key in context.scene.NodeOSC_keys):
            return
        
        item = context.scene.NodeOSC_keys.add()
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].matrix_world.translation[{index}]"
        item.osc_type = "f"
        item.osc_index = "()"
        item.osc_direction = "OUTPUT"
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = context.scene.holophonix_utils.enable_outgoing_tracks
        item.ui_expanded = False

    def create_color_handler(self, context, obj, id):
        # Check if handler already exists
        osc_address = f"/track/{id}/color"
        if any(key.osc_address == osc_address for key in context.scene.NodeOSC_keys):
            return
        
        item = context.scene.NodeOSC_keys.add()
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].color"
        item.osc_type = "f"
        item.osc_index = "(0,1,2,3)"
        item.osc_direction = "INPUT"
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = context.scene.holophonix_utils.enable_incoming_tracks
        item.ui_expanded = False

    def create_name_handler(self, context, obj, id):
        # Check if handler already exists
        osc_address = f"/track/{id}/name"
        if any(key.osc_address == osc_address for key in context.scene.NodeOSC_keys):
            return
        
        item = context.scene.NodeOSC_keys.add()
        item.osc_address = osc_address
        item.data_path = f"bpy.data.objects['{obj.name}'].name"
        item.osc_type = "s"
        item.osc_index = "(0)"
        item.osc_direction = "INPUT"
        item.filter_repetition = False
        item.dp_format_enable = False
        item.dp_format = "args"
        item.loop_enable = False
        item.loop_range = "0, length, 1"
        item.enabled = context.scene.holophonix_utils.enable_incoming_tracks
        item.ui_expanded = False