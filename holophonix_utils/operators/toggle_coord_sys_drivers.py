import bpy

class SNA_OT_Toggle_Coord_Sys_Drivers(bpy.types.Operator):
    bl_idname = "sna.toggle_coord_sys_drivers"
    bl_label = "Toggle Coordinate System Drivers"
    bl_description = "Toggle between Cartesian and spherical coordinate system drivers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or not obj.animation_data:
            self.report({'WARNING'}, "No object or animation data found")
            return {'CANCELLED'}

        # Toggle use_cartesian property
        use_cartesian = obj.get('use_cartesian', True)
        obj['use_cartesian'] = not use_cartesian

        # Toggle mute states based on use_cartesian
        for fcurve in obj.animation_data.drivers:
            if fcurve.data_path.startswith('location'):
                fcurve.mute = use_cartesian  # Mute if not using Cartesian
            else:
                fcurve.mute = not use_cartesian  # Mute if using Cartesian

        self.report({'INFO'}, f"Toggled drivers: {'Cartesian' if use_cartesian else 'Spherical'} coordinate system active")
        return {'FINISHED'}