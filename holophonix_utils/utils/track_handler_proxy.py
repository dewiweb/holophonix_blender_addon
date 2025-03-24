import bpy
from bpy.app.handlers import persistent


# Custom property group for storing attribute values
class AttributeValue(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    bool_value: bpy.props.BoolProperty()
    int_value: bpy.props.IntProperty()
    float_value: bpy.props.FloatProperty()
    string_value: bpy.props.StringProperty()

class TrackHandlerProxy(bpy.types.PropertyGroup):
    """Proxy class for NodeOSC_keys that adds custom attributes"""
    bl_idname = "holophonix_utils.track_handler_proxy"
    
    nodeosc_key: bpy.props.StringProperty()
    attributes: bpy.props.CollectionProperty(type=AttributeValue)
    original_values: bpy.props.CollectionProperty(type=AttributeValue)

    def set_attr(self, name, value):
        """Set a custom attribute with validation"""
        if not isinstance(name, str):
            raise ValueError("Attribute name must be a string")
        
        # Store original value if not already set
        if not self._has_original(name):
            orig_val = self._add_to_collection(self.original_values, name, value)
        
        # Set the new value
        self._add_to_collection(self.attributes, name, value)
    
    def _add_to_collection(self, collection, name, value):
        """Add or update a value in a collection"""
        # Check if attribute already exists
        for item in collection:
            if item.name == name:
                # Update existing item
                self._set_typed_value(item, value)
                return item
        
        # Create new item
        new_item = collection.add()
        new_item.name = name
        self._set_typed_value(new_item, value)
        return new_item
    
    def _set_typed_value(self, item, value):
        """Set the appropriate typed value based on the value type"""
        if isinstance(value, bool):
            item.bool_value = value
        elif isinstance(value, int):
            item.int_value = value
        elif isinstance(value, float):
            item.float_value = value
        else:
            item.string_value = str(value)
    
    def _get_typed_value(self, item):
        """Get the appropriate typed value based on what's set"""
        if item.bool_value != False:
            return item.bool_value
        elif item.int_value != 0:
            return item.int_value
        elif item.float_value != 0.0:
            return item.float_value
        else:
            return item.string_value
    
    def _has_original(self, name):
        """Check if an original value exists"""
        for item in self.original_values:
            if item.name == name:
                return True
        return False
    
    def get_attr(self, name, default=None):
        """Get a custom attribute or default value"""
        for item in self.attributes:
            if item.name == name:
                return self._get_typed_value(item)
        return default
    
    def has_changed(self, name):
        """Check if an attribute has changed from its original value"""
        current_val = self.get_attr(name)
        
        for item in self.original_values:
            if item.name == name:
                return current_val != self._get_typed_value(item)
        
        # If no original value, it's changed if it has a current value
        return current_val is not None
    
    def cleanup(self):
        """Clean up custom attributes"""
        while len(self.attributes) > 0:
            self.attributes.remove(0)
        
        while len(self.original_values) > 0:
            self.original_values.remove(0)


class TrackHandlerManager(bpy.types.PropertyGroup):
    """Manager class for track handler proxies"""
    bl_idname = "holophonix_utils.track_handler_manager"
    
    proxies: bpy.props.CollectionProperty(type=TrackHandlerProxy)
    
    def get_proxy(self, nodeosc_key):
        """Get or create a proxy for the given NodeOSC key"""
        for proxy in self.proxies:
            if proxy.nodeosc_key == nodeosc_key:
                return proxy
                
        # Create new proxy if not found
        new_proxy = self.proxies.add()
        new_proxy.nodeosc_key = nodeosc_key
        return new_proxy
        
    def update_all(self):
        """Update all proxies with current settings"""
        for proxy in self.proxies:
            # Update proxy attributes based on current settings
            pass
            
    def remove_proxy(self, nodeosc_key):
        """Remove a proxy for the given NodeOSC key"""
        for i, proxy in enumerate(self.proxies):
            if proxy.nodeosc_key == nodeosc_key:
                # Clean up proxy before removing
                proxy.cleanup()
                self.proxies.remove(i)
                return True
        return False


def get_manager():
    """Get or create the track handler manager"""
    if not bpy.context.scene.holophonix_utils:
        return None
        
    if not hasattr(bpy.context.scene.holophonix_utils, 'track_handler_manager'):
        # Initialize manager if not present
        utils_props = bpy.context.scene.holophonix_utils
        utils_props.track_handler_manager = utils_props.bl_rna.properties['track_handler_manager'].fixed_type()
        
    return bpy.context.scene.holophonix_utils.track_handler_manager

@persistent
def on_nodeosc_update(scene):
    """Track NodeOSC_keys changes"""
    try:
        if not hasattr(scene, 'NodeOSC_keys'):
            return
            
        manager = get_manager()
        if not manager:
            return
            
        current_keys = set(getattr(scene, 'NodeOSC_keys', []))
        tracked_keys = {proxy.nodeosc_key for proxy in manager.proxies}
        
        # Handle new keys
        for new_key in current_keys - tracked_keys:
            try:
                proxy = manager.get_proxy(new_key)
                # Initialize proxy with current settings
                if hasattr(scene, 'holophonix_utils'):
                    settings = scene.holophonix_utils.track_handler_settings
                    if settings:
                        # Initialize all settings
                        proxy.set_attr('position_enabled', settings.position_enabled)
                        proxy.set_attr('position_direction', settings.position_direction)
                        proxy.set_attr('name_enabled', settings.name_enabled)
                        proxy.set_attr('name_direction', settings.name_direction)
                        proxy.set_attr('color_enabled', settings.color_enabled)
                        proxy.set_attr('color_direction', settings.color_direction)
                        print(f"Initialized proxy for {new_key} with current settings")
            except Exception as e:
                print(f"Error initializing proxy for {new_key}: {str(e)}")
                
        # Handle removed keys
        for removed_key in tracked_keys - current_keys:
            try:
                manager.remove_proxy(removed_key)
            except Exception as e:
                print(f"Error removing proxy for {removed_key}: {str(e)}")
                
    except Exception as e:
        print(f"Error in NodeOSC update handler: {str(e)}")



# Setup function to be called during registration
def setup():
    """Setup track handler proxy system"""
    # Add track handler manager to holophonix_utils properties
    from ..properties import HolophonixUtilsProperties
    if not hasattr(HolophonixUtilsProperties, 'track_handler_manager'):
        HolophonixUtilsProperties.track_handler_manager = bpy.props.PointerProperty(type=TrackHandlerManager)

# Cleanup function to be called during unregistration
def cleanup():
    """Clean up track handler proxy system"""
    # Remove handler
    if on_nodeosc_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(on_nodeosc_update)