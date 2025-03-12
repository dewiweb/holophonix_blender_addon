import bpy
import os

class SNA_OT_Select_Hol_File(bpy.types.Operator):
    bl_idname = "sna.select_hol_file"
    bl_label = "Select HOL File"
    
    def execute(self, context):
        props = context.scene.holophonix_utils
        if props.holophonix_hol_files:
            props.selected_hol_file = os.path.join(props.project_path, props.holophonix_hol_files)
        return {'FINISHED'}