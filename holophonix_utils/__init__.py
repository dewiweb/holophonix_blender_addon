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
    "version" : (1, 1, 1),  # Updated version to trigger the release workflow
    "location" : "",
    "warning" : "",
    "doc_url": "",
    "tracker_url": "",
    "category" : "3D View"
}

import bpy
import os
from .utils import (
    HolophonixUtilsProperties,
    HandlerProperties,
    FileProperties,
    IconUtils
)
from .panels import *
from .operators import *

classes = [
    # Properties
    HolophonixUtilsProperties,
    HandlerProperties,
    FileProperties,
    IconUtils,
    # Panels
    SNA_PT_HOLOUTILS_1B113,
    SNA_PT_NodeOSC_Operations,
    SNA_PT_SPECIALHANDLERS,
    SNA_PT_SOURCES_11FF6,
    SNA_PT_SPEAKERS_F8536,
    SNA_PT_AN_SETTINGS_E1993,
    SNA_PT_Import_Holophonix_Project,
    # Operators
    SNA_OT_Delete_Handlers_C2D71,
    SNA_OT_Add_Sources_73B0D,
    SNA_OT_Import_An_Tree_433Db,
    SNA_OT_Sources_Exporter_34F69,
    SNA_OT_Add_Speakers_994C8,
    SNA_OT_Add_Handlers,
    SNA_OT_ExportAndCreateHandlers,
    SNA_OT_Import_Holophonix_Project,
    SNA_OT_Load_Venue,
    SNA_OT_Import_Tracks,
    SNA_OT_Import_Speakers,
    SNA_OT_Select_Hol_File
]

def register():
    from bpy.utils import register_class, previews
    import os

    # Load custom icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'logo_icon.png')
    custom_icons = previews.new()
    custom_icons.load('logo_icon', icon_path, 'IMAGE')
    bpy.types.WindowManager.custom_icons = custom_icons

    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add custom property to the scene
    bpy.types.Scene.holophonix_utils = bpy.props.PointerProperty(type=HolophonixUtilsProperties)

    # Defer icon registration until the scene is available
    def deferred_icon_registration(scene):
        if hasattr(bpy.context, 'scene') and bpy.context.scene is not None:
            bpy.context.scene.holophonix_utils.register_icons()
            bpy.app.handlers.depsgraph_update_post.remove(deferred_icon_registration)

    bpy.app.handlers.depsgraph_update_post.append(deferred_icon_registration)

def unregister():
    if hasattr(bpy.context, 'scene') and bpy.context.scene is not None:
        bpy.context.scene.holophonix_utils.unregister_icons()

    # Remove custom property from the scene
    del bpy.types.Scene.holophonix_utils

    # Unregister all classes in reverse order
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

from .utils.plugin_utils import plugin_exists, plugin_folder
