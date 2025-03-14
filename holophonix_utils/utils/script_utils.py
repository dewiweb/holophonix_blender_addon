import os
import bpy
from typing import Optional


# ------------------------------
# Script Loading
# ------------------------------

def load_script(script_name: str) -> Optional[bpy.types.Text]:
    """
    Load a Python script from the addon's assets directory.

    Args:
        script_name (str): Name of the script file to load

    Returns:
        Optional[bpy.types.Text]: The loaded text block, or None if failed
    """
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'assets', script_name)
        
        # Check if script is already loaded
        if script_name in bpy.data.texts:
            return bpy.data.texts[script_name]

        # Load and create new text block
        with open(script_path, 'r') as f:
            text_block = bpy.data.texts.new(script_name)
            text_block.from_string(f.read())
            return text_block

    except FileNotFoundError:
        print(f"Script file not found: {script_name}")
        return None
    except Exception as e:
        print(f"Error loading script {script_name}: {str(e)}")
        return None
