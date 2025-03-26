import bpy
import math
from bpy.props import FloatProperty
from bpy.types import Operator

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

        # Add spherical properties as both individual properties and a dictionary
        obj['azim'] = azimuth
        obj['elev'] = elevation
        obj['dist'] = distance
        obj['aed'] = {
            'azim': azimuth,
            'elev': elevation,
            'dist': distance
        }

        # Create drivers
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
        driver = obj.driver_add(f'["{target_prop}"]').driver

        # Add variables based on source property
        if source_prop == 'matrix_world.translation':
            # Driving spherical coordinates from translation
            var_x = driver.variables.new()
            var_x.name = 'x'
            var_x.targets[0].id = obj
            var_x.targets[0].data_path = 'matrix_world.translation[0]'

            var_y = driver.variables.new()
            var_y.name = 'y'
            var_y.targets[0].id = obj
            var_y.targets[0].data_path = 'matrix_world.translation[1]'

            var_z = driver.variables.new()
            var_z.name = 'z'
            var_z.targets[0].id = obj
            var_z.targets[0].data_path = 'matrix_world.translation[2]'

            # Set expression based on target property
            if target_prop == 'azim':
                driver.expression = 'degrees(atan2(y, x))'
            elif target_prop == 'elev':
                driver.expression = 'degrees(asin(z / sqrt(x*x + y*y + z*z)))' if 'sqrt(x*x + y*y + z*z) > 0' else '0'
            elif target_prop == 'dist':
                driver.expression = 'sqrt(x*x + y*y + z*z)'
        else:
            # Driving translation from spherical coordinates
            var_azim = driver.variables.new()
            var_azim.name = 'azim'
            var_azim.targets[0].id = obj
            var_azim.targets[0].data_path = f'["{source_prop}"]'

            var_elev = driver.variables.new()
            var_elev.name = 'elev'
            var_elev.targets[0].id = obj
            var_elev.targets[0].data_path = f'["{source_prop}"]'

            var_dist = driver.variables.new()
            var_dist.name = 'dist'
            var_dist.targets[0].id = obj
            var_dist.targets[0].data_path = f'["{source_prop}"]'

            # Set expression based on target property component
            if 'matrix_world.translation[0]' in target_prop:  # X
                driver.expression = 'dist * cos(radians(elev)) * cos(radians(azim))'
            elif 'matrix_world.translation[1]' in target_prop:  # Y
                driver.expression = 'dist * cos(radians(elev)) * sin(radians(azim))'
            elif 'matrix_world.translation[2]' in target_prop:  # Z
                driver.expression = 'dist * sin(radians(elev))'

        driver.type = 'SUM'
