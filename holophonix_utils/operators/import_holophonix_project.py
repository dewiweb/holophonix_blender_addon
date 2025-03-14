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

            # Determine destination folder
            temp_files_path = bpy.context.preferences.filepaths.temporary_directory
            if temp_files_path and os.path.exists(temp_files_path):
                project_folder = os.path.join(temp_files_path, os.path.basename(master_folder))
            else:
                # Fallback to Blender's datafiles directory
                datafiles_path = bpy.utils.user_resource('DATAFILES')
                holophonix_projects_path = os.path.join(datafiles_path, 'HolophonixProjects')
                os.makedirs(holophonix_projects_path, exist_ok=True)
                project_folder = os.path.join(holophonix_projects_path, os.path.basename(master_folder))

            # Remove existing project folder if it exists
            if os.path.exists(project_folder):
                shutil.rmtree(project_folder)

            # Copy the master folder to destination
            shutil.copytree(master_folder, project_folder)

            # Extract project name from master folder
            project_name = os.path.basename(master_folder)

            # Set project path and name in HolophonixUtilsProperties
            context.scene.holophonix_utils.project_path = project_folder
            context.scene.holophonix_utils.project_name = project_name
            print(f"Project '{project_name}' imported successfully! Path: {project_folder}")

            self.report({'INFO'}, f'Project "{project_name}" imported successfully!')
        context.scene.holophonix_utils.project_imported = True
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}