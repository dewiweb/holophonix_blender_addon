import bpy

class SNA_OT_Delete_Handlers_C2D71(bpy.types.Operator):
    bl_idname = 'sna.delete_handlers_c2d71'
    bl_label = 'Delete Handlers'
    bl_description = 'Delete all NodeOSC handlers'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        keys = bpy.context.scene.NodeOSC_keys
        while len(keys) > 0:
            keys.remove(0)
        self.report({'INFO'}, "Handlers deleted successfully")
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)
