import bpy
import math
from bpy.props import FloatProperty
from bpy.types import Operator

# Define properties at the module level
if not hasattr(bpy.types.Object, 'azim'):
    bpy.types.Object.azim = FloatProperty(name="azim", subtype='ANGLE', precision=1, min=-180, max=180, step=1)
if not hasattr(bpy.types.Object, 'elev'):
    bpy.types.Object.elev = FloatProperty(name="elev", subtype='ANGLE', precision=1, min=-180, max=180, step=1)
if not hasattr(bpy.types.Object, 'dist'):
    bpy.types.Object.dist = FloatProperty(name="dist", precision=2, min=0)

class SNA_OT_Add_AED_Properties(Operator):
    bl_idname = 'sna.add_aed_properties'
    bl_label = 'Add AED Properties'
    bl_description = 'Adds azimuth, elevation, distance and world matrix drivers'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None


    def execute(self, context):
        obj = context.object
        location = obj.matrix_world.translation

        # Calculate spherical coordinates
        distance = math.sqrt(location[0]**2 + location[1]**2 + location[2]**2)
        azimuth = math.degrees(math.atan2(location[1], location[0]))
        elevation = math.degrees(math.asin(location[2] / distance)) if distance > 0 else 0

        # Register custom properties
        obj.azim = azimuth
        obj.elev = elevation
        obj.dist = distance
        #obj['aed'] = [azimuth, elevation, distance]
        obj['use_cartesian'] = True

        # Create drivers for bidirectional conversion
        self._create_driver(obj, 'matrix_world.translation', 'azim')
        self._create_driver(obj, 'matrix_world.translation', 'elev')
        self._create_driver(obj, 'matrix_world.translation', 'dist')
        self._create_driver(obj, 'azim', 'matrix_world.translation[0]')
        self._create_driver(obj, 'elev', 'matrix_world.translation[1]')
        self._create_driver(obj, 'dist', 'matrix_world.translation[2]')

        self.report({'INFO'}, 'Added all custom properties and drivers')
        return {'FINISHED'}

    def _create_driver(self, obj, source_prop, target_prop):
        # Create driver for target property
        if target_prop.startswith('matrix_world.translation'):
            fcurve = obj.driver_add('location', int(target_prop[-2]))
            driver = fcurve.driver
            fcurve.mute = not obj.get('use_cartesian', True)  # Mute if not using Cartesian
        else:
            fcurve = obj.driver_add(target_prop)
            driver = fcurve.driver
            fcurve.mute = obj.get('use_cartesian', True)  # Mute if using Cartesian

        if source_prop == 'matrix_world.translation':
            # Driving spherical coordinates from translation
            var_x = driver.variables.new()
            var_x.name = 'x'
            var_x.type = 'TRANSFORMS'
            var_x.targets[0].id = obj
            var_x.targets[0].transform_type = 'LOC_X'
            var_x.targets[0].transform_space = 'WORLD_SPACE'

            var_y = driver.variables.new()
            var_y.name = 'y'
            var_y.type = 'TRANSFORMS'
            var_y.targets[0].id = obj
            var_y.targets[0].transform_type = 'LOC_Y'
            var_y.targets[0].transform_space = 'WORLD_SPACE'

            var_z = driver.variables.new()
            var_z.name = 'z'
            var_z.type = 'TRANSFORMS'
            var_z.targets[0].id = obj
            var_z.targets[0].transform_type = 'LOC_Z'
            var_z.targets[0].transform_space = 'WORLD_SPACE'

            # Set expression based on target property
            if target_prop == 'azim':
                driver.expression = 'atan2(y,x)'
            elif target_prop == 'elev':
                driver.expression = 'asin(z/sqrt(x*x+y*y+z*z)) if x*x+y*y+z*z != 0 else 0'
            elif target_prop == 'dist':
                driver.expression = 'sqrt(x*x+y*y+z*z) if x*x+y*y+z*z != 0 else 0'

        else:
            # Driving translation from spherical coordinates
            if target_prop.startswith('matrix_world.translation'):
                if source_prop == 'azim':
                    var_azim = driver.variables.new()
                    var_azim.name = 'azim'
                    var_azim.targets[0].id = obj
                    var_azim.targets[0].data_path = 'azim'

                    var_elev = driver.variables.new()
                    var_elev.name = 'elev'
                    var_elev.targets[0].id = obj
                    var_elev.targets[0].data_path = 'elev'

                    var_dist = driver.variables.new()
                    var_dist.name = 'dist'
                    var_dist.targets[0].id = obj
                    var_dist.targets[0].data_path = 'dist'

                    # Set expression based on target property
                    if target_prop == 'matrix_world.translation[0]':
                        driver.expression = 'dist * cos(elev) * cos(azim)'
                    elif target_prop == 'matrix_world.translation[1]':
                        driver.expression = 'dist * cos(elev) * sin(azim)'
                    elif target_prop == 'matrix_world.translation[2]':
                        driver.expression = 'dist * sin(elev)'
                elif source_prop == 'elev':
                    var_azim = driver.variables.new()
                    var_azim.name = 'azim'
                    var_azim.targets[0].id = obj
                    var_azim.targets[0].data_path = 'azim'

                    var_elev = driver.variables.new()
                    var_elev.name = 'elev'
                    var_elev.targets[0].id = obj
                    var_elev.targets[0].data_path = 'elev'

                    var_dist = driver.variables.new()
                    var_dist.name = 'dist'
                    var_dist.targets[0].id = obj
                    var_dist.targets[0].data_path = 'dist'

                    # Set expression based on target property
                    if target_prop == 'matrix_world.translation[0]':
                        driver.expression = 'dist * cos(elev) * cos(azim)'
                    elif target_prop == 'matrix_world.translation[1]':
                        driver.expression = 'dist * cos(elev) * sin(azim)'
                    elif target_prop == 'matrix_world.translation[2]':
                        driver.expression = 'dist * sin(elev)'
                elif source_prop == 'dist':
                    var_azim = driver.variables.new()
                    var_azim.name = 'azim'
                    var_azim.targets[0].id = obj
                    var_azim.targets[0].data_path = 'azim'

                    var_elev = driver.variables.new()
                    var_elev.name = 'elev'
                    var_elev.targets[0].id = obj
                    var_elev.targets[0].data_path = 'elev'

                    var_dist = driver.variables.new()
                    var_dist.name = 'dist'
                    var_dist.targets[0].id = obj
                    var_dist.targets[0].data_path = 'dist'

                    # Set expression based on target property
                    if target_prop == 'matrix_world.translation[0]':
                        driver.expression = 'dist * cos(elev) * cos(azim)'
                    elif target_prop == 'matrix_world.translation[1]':
                        driver.expression = 'dist * cos(elev) * sin(azim)'
                    elif target_prop == 'matrix_world.translation[2]':
                        driver.expression = 'dist * sin(elev)'
            else:
                var_azim = driver.variables.new()
                var_azim.name = 'azim'
                var_azim.targets[0].id = obj
                var_azim.targets[0].data_path = 'azim'

                var_elev = driver.variables.new()
                var_elev.name = 'elev'
                var_elev.targets[0].id = obj
                var_elev.targets[0].data_path = 'elev'

                var_dist = driver.variables.new()
                var_dist.name = 'dist'
                var_dist.targets[0].id = obj
                var_dist.targets[0].data_path = 'dist'

                # Set expression based on target property
                if target_prop == 'matrix_world.translation[0]':
                    driver.expression = 'dist * cos(elev) * cos(azim)'
                elif target_prop == 'matrix_world.translation[1]':
                    driver.expression = 'dist * cos(elev) * sin(azim)'
                elif target_prop == 'matrix_world.translation[2]':
                    driver.expression = 'dist * sin(elev)'

        driver.type = 'SCRIPTED'
