import bpy
from bpy.props import PointerProperty
from ..operators.import_holophonix_project import SNA_OT_Import_Holophonix_Project
from ..operators.import_tracks import SNA_OT_Import_Tracks
from ..operators.import_speakers import SNA_OT_Import_Speakers
import os

# Track last selected file for debug print
_last_hol_file = None

class SNA_PT_Import_Holophonix_Project(bpy.types.Panel):
    bl_idname = 'SNA_PT_Import_Holophonix_Project'
    bl_label = 'Import Holophonix Project'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Holophonix'
    bl_parent_id = 'SNA_PT_HOLOUTILS_1B113'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, scale=1.2)

    def draw(self, context):
        global _last_hol_file
        layout = self.layout
        utils_props = context.scene.holophonix_utils
        
        # Debug print only when value changes
        if utils_props.holophonix_hol_files != _last_hol_file:
            print(f"Current .hol file selection: {utils_props.holophonix_hol_files}")
            _last_hol_file = utils_props.holophonix_hol_files
        
        # Import .zip file button
        layout.operator(SNA_OT_Import_Holophonix_Project.bl_idname, text='Import .zip File')
        
        # Load Venue button (enabled when .zip is imported)
        row = layout.row()
        row.enabled = utils_props.project_imported
        row.operator('sna.load_venue', text='Load Venue')
        
        # Dropdown for .hol files (enabled when .zip is imported and project_path is set)
        row = layout.row()
        row.enabled = utils_props.project_imported and bool(utils_props.project_path)
        row.prop(utils_props, 'holophonix_hol_files', text='.hol File')
        
        # Display selected file path
        if utils_props.selected_hol_file:
            layout.label(text=f"Selected: {utils_props.selected_hol_file}")
        
        # Import Tracks and Speakers buttons (enabled when .hol is selected)
        row = layout.row()
        row.enabled = utils_props.holophonix_hol_files != ''
        row.operator(SNA_OT_Import_Tracks.bl_idname, text='Import Tracks')
        row.operator(SNA_OT_Import_Speakers.bl_idname, text='Import Speakers')