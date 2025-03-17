import bpy

class HandlerProperties(bpy.types.PropertyGroup):
    def update_dump(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/dump":
                    item.enabled = self.enable_dump

    def update_track(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/track/*":
                    item.enabled = self.enable_track

    def update_incoming_tracks(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_direction == "INPUT" and "/track/" in item.osc_address:
                    item.enabled = self.enable_incoming_tracks

    def update_outgoing_tracks(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_direction == "OUTPUT" and "/track/" in item.osc_address:
                    item.enabled = self.enable_outgoing_tracks

    def update_speaker(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/speaker/*":
                    item.enabled = self.enable_speaker

    def update_reaperTC(self, context):
        if hasattr(context.scene, 'NodeOSC_keys'):
            for item in context.scene.NodeOSC_keys:
                if item.osc_address == "/frames/str":
                    item.enabled = self.enable_reaperTC

    def update_nodeosc_handlers(self, context):
        if not hasattr(context.scene, 'NodeOSC_keys'):
            return

        props = context.scene.holophonix_utils
        for item in context.scene.NodeOSC_keys:
            if item.osc_address == "/dump" and item.enabled != props.enable_dump:
                props.enable_dump = item.enabled
            elif item.osc_address == "/track/*" and item.enabled != props.enable_track:
                props.enable_track = item.enabled
            elif item.osc_direction == "INPUT" and "/track/" in item.osc_address and item.enabled != props.enable_incoming_tracks:
                props.enable_incoming_tracks = item.enabled
            elif item.osc_direction == "OUTPUT" and "/track/" in item.osc_address and item.enabled != props.enable_outgoing_tracks:
                props.enable_outgoing_tracks = item.enabled
            elif item.osc_address == "/speaker/*" and item.enabled != props.enable_speaker:
                props.enable_speaker = item.enabled
            elif item.osc_address == "/frames/str" and item.enabled != props.enable_reaperTC:
                props.enable_reaperTC = item.enabled

    enable_dump: bpy.props.BoolProperty(
        name="Enable Dump Handler",
        description="Enable/disable the dump handler",
        default=True,
        update=update_dump
    )

    enable_track: bpy.props.BoolProperty(
        name="Enable Track Handler",
        description="Enable/disable the track handler",
        default=True,
        update=update_track
    )

    enable_incoming_tracks: bpy.props.BoolProperty(
        name="Enable Incoming Tracks",
        description="Enable/disable incoming track handlers",
        default=True,
        update=update_incoming_tracks
    )

    enable_outgoing_tracks: bpy.props.BoolProperty(
        name="Enable Outgoing Tracks",
        description="Enable/disable outgoing track handlers",
        default=True,
        update=update_outgoing_tracks
    )

    enable_speaker: bpy.props.BoolProperty(
        name="Enable Speaker Handler",
        description="Enable/disable the speaker handler",
        default=True,
        update=update_speaker
    )

    enable_reaperTC: bpy.props.BoolProperty(
        name="Enable Reaper TC Handler",
        description="Enable/disable the ReaperTC handler",
        default=True,
        update=update_reaperTC
    )

    enable_populate: bpy.props.BoolProperty(
        name="Enable Populate Handler",
        description="Enable/disable the populate handler",
        default=True
    )
