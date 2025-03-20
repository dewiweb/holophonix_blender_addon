import bpy
import os
from ..operators.manage_track_handlers import SNA_OT_ManageTrackHandlers

def init_default_selection(self, context):
    if self.default_hol_file:
        files = self.get_hol_files(context, self.project_path)
        for i, file in enumerate(files):
            if file[0] == self.default_hol_file:
                # Set using the actual enum value instead of string index
                self.holophonix_hol_files = file[0]
                
                # Clear existing track handlers when the default .hol file is selected
                # Note: We don't call self.clear_track_handlers here because self is FileProperties
                # and this function is called outside the class context
                if hasattr(context.scene, 'file_properties'):
                    context.scene.file_properties.clear_track_handlers(context)
                break

class FileProperties(bpy.types.PropertyGroup):

   

    project_path: bpy.props.StringProperty(
        name="Project Path",
        description="Path to the Holophonix project folder",
        default="",
        subtype='DIR_PATH',
        update=init_default_selection
    )

    project_imported: bpy.props.BoolProperty(
        name="Project Imported",
        description="Whether a Holophonix project has been imported",
        default=False
    )

    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="Name of the imported Holophonix project",
        default=""
    )

    holophonix_hol_files: bpy.props.EnumProperty(
        name=".hol File",
        description="Select a .hol file from the Presets directory",
        items=lambda self, context: self.get_hol_files(context, self.project_path),
        default=0
    )

    manifest_path: bpy.props.StringProperty(
        name="Manifest Path",
        description="Path to the manifest.json file",
        default="",
        subtype='FILE_PATH'
    )




    def update_selected_hol_file(self, context):
        if self.holophonix_hol_files:
            self.selected_hol_file = os.path.join(self.project_path, self.holophonix_hol_files)
            
            # Clear existing track handlers when a new .hol file is selected
            self.clear_track_handlers(context)
    
    def clear_track_handlers(self, context):
        """Clear existing track handlers when a new .hol file is selected"""
        # Check if NodeOSC is available
        if not hasattr(context.scene, 'NodeOSC_keys'):
            print("NodeOSC is not available, skipping handler cleanup")
            return
            
        # Create an instance of the handler manager
        handler_manager = SNA_OT_ManageTrackHandlers()
        
        # Call the clear_existing_handlers method
        handler_manager.clear_existing_handlers(context)
        print(f"Cleared existing track handlers for new .hol file: {self.holophonix_hol_files}")

    selected_hol_file: bpy.props.StringProperty(
        name="Selected HOL File",
        description="Path to the selected .hol file",
        subtype='FILE_PATH',
        update=update_selected_hol_file
    )


    default_hol_file: bpy.props.StringProperty(
        name="Default HOL File",
        description="Name of the default .hol file",
        default=""
    )
    
    holophonix_hol_files: bpy.props.EnumProperty(
        name=".hol File",
        description="Select a .hol file from the Presets directory",
        items=lambda self, context: self.get_hol_files(context, self.project_path),
        default=0
    )



    def parse_manifest(self, project_path):
        manifest_path = os.path.join(project_path, 'manifest.json')
        if not os.path.exists(manifest_path):
            return None
            
        try:
            with open(manifest_path, 'r') as f:
                import json
                manifest = json.load(f)
                return manifest.get('defaultPreset')
        except Exception as e:
            print(f"Error parsing manifest.json: {e}")
            return None

    def get_hol_files(self, context, project_path):
        if not project_path:
            print("No project path provided.")
            return [("NONE", "No .hol files found", "No .hol files found")]
    
        presets_path = os.path.join(project_path, 'Presets')
        if not os.path.exists(presets_path):
            print(f"Presets directory not found at {presets_path}")
            return [("NONE", "No .hol files found", "No .hol files found")]
    
        # Get default preset from manifest
        default_preset = self.parse_manifest(project_path)
        
        files = []
        for file in os.listdir(presets_path):
            if file.endswith('.hol'):
                files.append((file, file, file))
                if default_preset and file == default_preset:
                    self.default_hol_file = file
    
        if not files:
            return [("NONE", "No .hol files found", "No .hol files found")]
            
        return files
            
        
