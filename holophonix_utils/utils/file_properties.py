import bpy
import os

class FileProperties(bpy.types.PropertyGroup):
    project_path: bpy.props.StringProperty(
        name="Project Path",
        description="Path to the Holophonix project folder",
        default="",
        subtype='DIR_PATH'
    )

    project_imported: bpy.props.BoolProperty(
        name="Project Imported",
        description="Whether a Holophonix project has been imported",
        default=False
    )

    holophonix_hol_files: bpy.props.EnumProperty(
        name=".hol File",
        description="Select a .hol file from the Presets directory",
        items=lambda self, context: self.get_hol_files(context, self.project_path)
    )

    def update_selected_hol_file(self, context):
        if self.holophonix_hol_files:
            self.selected_hol_file = os.path.join(self.project_path, self.holophonix_hol_files)

    selected_hol_file: bpy.props.StringProperty(
        name="Selected HOL File",
        description="Path to the selected .hol file",
        subtype='FILE_PATH',
        update=update_selected_hol_file
    )

    def get_hol_files(self, context, project_path):
        if not project_path:
            print("No project path provided.")
            return [("NONE", "No .hol files found", "No .hol files found")]

        presets_path = os.path.join(project_path, 'Presets')
        if not os.path.exists(presets_path):
            print(f"Presets directory not found at {presets_path}")
            return [("NONE", "No .hol files found", "No .hol files found")]

        hol_files = []
        for file in os.listdir(presets_path):
            if file.endswith('.hol'):
                hol_files.append((file, file, file))

        if not hol_files:
            return [("NONE", "No .hol files found", "No .hol files found")]

        return hol_files
