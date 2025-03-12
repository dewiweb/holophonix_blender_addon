import bpy
import os
import zipfile
import tempfile
import shutil

class SNA_OT_Import_Holophonix_Project(bpy.types.Operator):
    bl_idname = "sna.import_holophonix_project"
    bl_label = "Import Holophonix Project"
    bl_description = "Import a Holophonix project from a .zip file"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Ensure the selected file is a .zip file
        if not self.filepath.endswith('.zip'):
            self.report({'ERROR'}, 'Please select a valid .zip file')
            return {'CANCELLED'}

        # Create a temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the .zip file
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)


            # Find the master folder by checking for required files
            master_folder = None
            for root, dirs, files in os.walk(temp_dir):
                if 'manifest.json' in files and 'Venue' in dirs:
                    # Check if 'Presets' is nested one level inside
                    presets_path = os.path.join(root, 'Presets')
                    if os.path.exists(presets_path):
                        master_folder = root
                        break

            if not master_folder:
                self.report({'ERROR'}, 'No valid Holophonix project found in the .zip file')
                return {'CANCELLED'}

            # Copy the master folder to a permanent location
            project_folder = os.path.join(os.path.dirname(self.filepath), os.path.basename(master_folder))
            shutil.copytree(master_folder, project_folder, dirs_exist_ok=True)

            # Set the project path in HolophonixUtilsProperties
            context.scene.holophonix_utils.project_path = project_folder
            print(f"Project path set to: {project_folder}")

        self.report({'INFO'}, 'Project imported successfully!')
        context.scene.holophonix_utils.project_imported = True
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}