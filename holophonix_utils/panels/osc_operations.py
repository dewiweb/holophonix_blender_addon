import bpy
from ..utils.plugin_utils import plugin_folder

class SNA_PT_NodeOSC_Operations(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NodeOSC'
    bl_label = 'Holophonix Operations'
    bl_idname = 'SNA_PT_NodeOSC_Operations'
    bl_parent_id = 'OSC_PT_Operations'

    @classmethod
    def poll(cls, context):
        return plugin_folder('NodeOSC')

    def draw(self, context):
        try:
            layout = self.layout

            # Add delete handlers button
            try:
                if hasattr(context.scene, 'holophonix_utils') and hasattr(context.scene.holophonix_utils, 'icons'):
                    op = layout.operator('sna.delete_handlers_c2d71', 
                                       text='Delete all message handlers', 
                                       icon_value=context.scene.holophonix_utils.icons['logo_icon'].icon_id)
                else:
                    op = layout.operator('sna.delete_handlers_c2d71', 
                                       text='Delete all message handlers', 
                                       icon_value=context.window_manager.custom_icons['logo_icon'].icon_id)
            except Exception as e:
                logger.error(f'Error creating delete handlers operator: {str(e)}')
                layout.label(text='Error creating delete handlers operator', icon='ERROR')

            # Add export holo objects button
            try:
                op = layout.operator('sna.sources_exporter_34f69', 
                                   text='Export Holo objects to OSC handlers', 
                                   icon_value=context.window_manager.custom_icons['logo_icon'].icon_id, 
                                   emboss=True, 
                                   depress=False)
            except Exception as e:
                logger.error(f'Error creating sources exporter operator: {str(e)}')
                layout.label(text='Error creating sources exporter operator', icon='ERROR')

        except Exception as e:
            logger.error(f'Error drawing NodeOSC operations panel: {str(e)}')
            layout.label(text='Error loading panel content', icon='ERROR')
