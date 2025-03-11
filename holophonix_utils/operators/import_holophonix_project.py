import bpy
import zipfile
import os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

class SNA_OT_Import_Holophonix_Project(bpy.types.Operator, ImportHelper):
    bl_idname = 'sna.import_holophonix_project'
    bl_label = 'Import Holophonix Project'
    bl_description = 'Import a Holophonix project from a .zip file'
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default='*.zip',
        options={'HIDDEN'},
    )

    def execute(self, context):
        # Extract the .zip file
        with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(self.filepath))

        # Validate the project structure
        project_dir = os.path.splitext(self.filepath)[0]
        required_files = ['manifest.json', 'Venue', 'Presets']
        for file in required_files:
            if not os.path.exists(os.path.join(project_dir, file)):
                self.report({'ERROR'}, f'Missing required file/directory: {file}')
                return {'CANCELLED'}

        # TODO: Trigger venue, tracks, and speakers import
        self.report({'INFO'}, 'Project imported successfully!')
        context.scene.holophonix_utils.project_imported = True
        return {'FINISHED'}
