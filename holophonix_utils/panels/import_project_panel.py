import bpy
from bpy.props import PointerProperty
from ..operators.import_holophonix_project import SNA_OT_Import_Holophonix_Project
import os

def load_preview_icon(path):
    return bpy.data.images.load(path, check_existing=True).preview

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
        layout = self.layout

        # Import .zip file button
        layout.operator(SNA_OT_Import_Holophonix_Project.bl_idname, text='Import .zip File')

        # Load Venue button (enabled when .zip is imported)
        row = layout.row()
        row.enabled = context.scene.holophonix_utils.project_imported
        row.operator('sna.load_venue', text='Load Venue')

        # Dropdown for .hol files (disabled until .zip is imported)
        row = layout.row()
        row.enabled = False  # TODO: Enable when .zip is imported
        row.prop(context.scene, 'holophonix_hol_files', text='.hol File')

        # Import Tracks and Speakers buttons (disabled until .hol is selected)
        row = layout.row()
        row.enabled = False  # TODO: Enable when .hol is selected
        row.operator('sna.import_tracks', text='Import Tracks')
        row.operator('sna.import_speakers', text='Import Speakers')
