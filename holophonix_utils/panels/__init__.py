from .main_panel import SNA_PT_MAIN_PANEL  # Renamed from SNA_PT_HOLOUTILS_1B113 for clearer identification
# from .osc_operations import SNA_PT_NodeOSC_Operations  # Functionality moved to SNA_PT_HolophonixNodeOSC
from .special_handlers_panel import SNA_PT_SPECIALHANDLERS
from .tracks_panel import SNA_PT_TRACKS_11FF6
from .holophonix_communication_panel import SNA_PT_HolophonixNodeOSC
from .speakers_panel import SNA_PT_SPEAKERS_F8536
from .an_settings_panel import SNA_PT_AN_SETTINGS_E1993
from .import_project_panel import SNA_PT_Import_Holophonix_Project

__all__ = [
    "SNA_PT_Import_Holophonix_Project",
    "SNA_PT_MAIN_PANEL",
    # "SNA_PT_NodeOSC_Operations",  # Functionality moved to SNA_PT_HolophonixNodeOSC
    "SNA_PT_SPECIALHANDLERS",
    "SNA_PT_TRACKS_11FF6",
    "SNA_PT_HolophonixNodeOSC",
    "SNA_PT_SPEAKERS_F8536",
    "SNA_PT_AN_SETTINGS_E1993"
]
