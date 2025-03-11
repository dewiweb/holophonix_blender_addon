# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Holophonix_Utils",
    "author" : "Dewiweb",
    "description" : "",
    "blender" : (4, 3, 0),
    "version" : (1, 0, 3),  # Updated version to trigger the release workflow
    "location" : "",
    "warning" : "",
    "doc_url": "",
    "tracker_url": "",
    "category" : "3D View"
}

import bpy
import os
from bpy.utils import register_class, unregister_class, previews

from .utils.property_utils import HolophonixUtilsProperties
from .panels.holoutils_panel import SNA_PT_HOLOUTILS_1B113
from .panels.osc_operations import SNA_PT_NodeOSC_Operations
from .operators.delete_handlers import SNA_OT_Delete_Handlers_C2D71
from .operators.add_sources import SNA_OT_Add_Sources_73B0D
from .operators.import_an_tree import SNA_OT_Import_An_Tree_433Db
from .operators.sources_exporter import SNA_OT_Sources_Exporter_34F69
from .operators.add_speakers import SNA_OT_Add_Speakers_994C8
from .operators.add_handlers import SNA_OT_Add_Handlers
from .panels.special_handlers_panel import SNA_PT_SPECIALHANDLERS
from .panels.sources_panel import SNA_PT_SOURCES_11FF6
from .panels.speakers_panel import SNA_PT_SPEAKERS_F8536
from .panels.an_settings import SNA_PT_AN_SETTINGS_E1993

def register():
    from bpy.utils import register_class, previews
    import os

    # Load custom icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'logo_icon.png')
    custom_icons = previews.new()
    custom_icons.load('logo_icon', icon_path, 'IMAGE')
    bpy.types.WindowManager.custom_icons = custom_icons

    bpy.utils.register_class(HolophonixUtilsProperties)
    bpy.types.Scene.holophonix_utils = bpy.props.PointerProperty(type=HolophonixUtilsProperties)

    # Defer icon registration until the scene is available
    def deferred_icon_registration(scene):
        if hasattr(bpy.context, 'scene') and bpy.context.scene is not None:
            bpy.context.scene.holophonix_utils.register_icons()
            bpy.app.handlers.depsgraph_update_post.remove(deferred_icon_registration)

    bpy.app.handlers.depsgraph_update_post.append(deferred_icon_registration)

    bpy.utils.register_class(SNA_OT_Add_Sources_73B0D)
    bpy.utils.register_class(SNA_OT_Import_An_Tree_433Db)
    bpy.utils.register_class(SNA_OT_Sources_Exporter_34F69)
    bpy.utils.register_class(SNA_OT_Add_Speakers_994C8)
    bpy.utils.register_class(SNA_OT_Delete_Handlers_C2D71)
    bpy.utils.register_class(SNA_OT_Add_Handlers)
    bpy.utils.register_class(SNA_PT_HOLOUTILS_1B113)
    try:
        if "NodeOSC" in bpy.context.preferences.addons:
            if hasattr(bpy.types, 'OSC_PT_Operations'):
                bpy.utils.register_class(SNA_PT_NodeOSC_Operations)
            else:
                bpy.utils.register_class(SNA_PT_NodeOSC_Operations)
        else:
            bpy.utils.register_class(SNA_PT_NodeOSC_Operations)
    except Exception as e:
        print(f"Error registering NodeOSC operations: {str(e)}")
    bpy.utils.register_class(SNA_PT_SPECIALHANDLERS)
    bpy.utils.register_class(SNA_PT_SOURCES_11FF6)
    bpy.utils.register_class(SNA_PT_SPEAKERS_F8536)
    bpy.utils.register_class(SNA_PT_AN_SETTINGS_E1993)

def unregister():
    if hasattr(bpy.context, 'scene') and bpy.context.scene is not None:
        bpy.context.scene.holophonix_utils.unregister_icons()
    bpy.utils.unregister_class(HolophonixUtilsProperties)
    del bpy.types.Scene.holophonix_utils
    bpy.utils.unregister_class(SNA_OT_Add_Sources_73B0D)
    bpy.utils.unregister_class(SNA_OT_Import_An_Tree_433Db)
    bpy.utils.unregister_class(SNA_OT_Sources_Exporter_34F69)
    bpy.utils.unregister_class(SNA_OT_Add_Speakers_994C8)
    bpy.utils.unregister_class(SNA_OT_Delete_Handlers_C2D71)
    bpy.utils.unregister_class(SNA_OT_Add_Handlers)
    bpy.utils.unregister_class(SNA_PT_HOLOUTILS_1B113)
    bpy.utils.unregister_class(SNA_PT_SPECIALHANDLERS)
    bpy.utils.unregister_class(SNA_PT_SOURCES_11FF6)
    bpy.utils.unregister_class(SNA_PT_SPEAKERS_F8536)
    bpy.utils.unregister_class(SNA_PT_AN_SETTINGS_E1993)
    bpy.utils.unregister_class(SNA_PT_NodeOSC_Operations)

from .utils.plugin_utils import plugin_exists, plugin_folder
