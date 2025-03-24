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
    "version" : (1, 3, 1),
    "location" : "",
    "warning" : "",
    "doc_url": "",
    "tracker_url": "",
    "category" : "3D View"
}

import bpy
import os
from .utils import *
from .panels import *
from .operators import *


classes = [
    # Register AttributeValue first
    AttributeValue,
    # Then TrackHandlerProxy
    TrackHandlerProxy,
    # Then TrackHandlerManager
    TrackHandlerManager,
    # Then TrackHandlerSettings
    TrackHandlerSettings,
    # Then HolophonixUtilsProperties
    HolophonixUtilsProperties,
    # Other property classes
    HandlerProperties,
    FileProperties,
    IconUtils,
    # Panels
    SNA_PT_MAIN_PANEL,
    SNA_PT_SPECIALHANDLERS,
    SNA_PT_TRACKS_11FF6,
    SNA_PT_HolophonixNodeOSC,
    SNA_PT_SPEAKERS_F8536,
    SNA_PT_AN_SETTINGS_E1993,
    SNA_PT_Import_Holophonix_Project,
    SNA_PT_TrackHandlers,
    # Operators
    SNA_OT_Delete_Handlers_C2D71,
    SNA_OT_Add_Tracks_73B0D,
    SNA_OT_Import_An_Tree_433Db,
    SNA_OT_Tracks_Exporter_34F69,
    SNA_OT_Add_Speakers_994C8,
    SNA_OT_Add_Handlers,
    SNA_OT_ExportAndCreateHandlers,
    SNA_OT_ManageTrackHandlers,
    SNA_OT_Import_Holophonix_Project,
    SNA_OT_Load_Venue,
    SNA_OT_Import_Tracks,
    SNA_OT_Import_Speakers,
    SNA_OT_Select_Hol_File,
    SNA_OT_SelectAllTracks,
    SNA_OT_SelectAllSpeakers,
    SNA_OT_ResolveHolophonixHostname,
    SNA_OT_HolophonixCommunication
]

def register():
    from bpy.utils import register_class, previews
    import os

    # Register AttributeValue first
    from .utils.track_handler_proxy import AttributeValue
    register_class(AttributeValue)

    # Load custom icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'logo_icon.png')
    custom_icons = previews.new()
    custom_icons.load('logo_icon', icon_path, 'IMAGE')
    bpy.types.WindowManager.custom_icons = custom_icons

    # Register all classes
    for cls in classes:
        if cls != AttributeValue:  # Skip AttributeValue since we already registered it
            bpy.utils.register_class(cls)

    # Add custom property to the scene
    bpy.types.Scene.holophonix_utils = bpy.props.PointerProperty(type=HolophonixUtilsProperties)
    bpy.types.Scene.file_properties = bpy.props.PointerProperty(type=FileProperties)
    
    # Set initializing flag to prevent updates during registration
    # Use a safer approach that doesn't rely on bpy.context.scene which may not be available during registration
    def set_initializing_flag():
        for scene in bpy.data.scenes:
            if hasattr(scene, 'holophonix_utils'):
                scene.holophonix_utils.is_initializing = True
        return None
    
    # Defer setting the flag until the next frame when the scene should be available
    bpy.app.timers.register(set_initializing_flag, first_interval=0.1)

    # Defer icon registration until the scene is available
    def deferred_icon_registration():
        # Check if there are any scenes with holophonix_utils
        for scene in bpy.data.scenes:
            if hasattr(scene, 'holophonix_utils'):
                scene.holophonix_utils.register_icons()
                break
        return None  # Remove the timer
    
    # Use a timer instead of a depsgraph handler for more reliability
    bpy.app.timers.register(deferred_icon_registration, first_interval=0.5)

    # Icon registration is now handled by the timer
    
    # Add handler to initialize track handlers properties
    from .utils import initialize_track_handlers, setup_track_handler_proxy
    # First remove any existing copy of the handler to avoid duplicates
    if initialize_track_handlers in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(initialize_track_handlers)
    bpy.app.handlers.depsgraph_update_post.append(initialize_track_handlers)
    
    # Setup track handler proxy system
    setup_track_handler_proxy()
    
    # Clear initializing flag after registration
    def clear_initializing_flag():
        for scene in bpy.data.scenes:
            if hasattr(scene, 'holophonix_utils'):
                scene.holophonix_utils.is_initializing = False
        return None
    
    # Defer clearing the flag until the next frame when the scene should be available
    bpy.app.timers.register(clear_initializing_flag, first_interval=0.2)

def unregister():
    # Clean up app handlers
    from .utils import initialize_track_handlers, cleanup_track_handler_proxy
    if initialize_track_handlers in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(initialize_track_handlers)
        
    # Clean up track handler proxy system
    cleanup_track_handler_proxy()
        
    # Unregister icons for all scenes
    for scene in bpy.data.scenes:
        if hasattr(scene, 'holophonix_utils'):
            try:
                scene.holophonix_utils.unregister_icons()
            except Exception as e:
                print(f"Error unregistering icons: {e}")

    # Remove custom property from the scene
    del bpy.types.Scene.holophonix_utils
    del bpy.types.Scene.file_properties

    # Unregister all classes in reverse order
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

from .utils.plugin_utils import plugin_exists, plugin_folder
