import bpy
import os

class SNA_OT_Import_An_Tree_433Db(bpy.types.Operator):
    bl_idname = "sna.import_an_tree_433db"
    bl_label = "Import_AN_Tree"
    bl_description = "Import AN Tree"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'amadeus.blend')
        Variable = None
        inner_path = 'NodeTree'
        name = 'AN Tree'
        bpy.ops.wm.append(
                    directory=os.path.join(file_path, inner_path),
                    filename=name
                    )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
