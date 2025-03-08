def load_script(script_name):
    """Load a Python script from the addon's assets directory."""
    script_path = os.path.join(os.path.dirname(__file__), 'assets', script_name)
    if script_name not in bpy.data.texts:
        with open(script_path, 'r') as f:
            bpy.data.texts.new(script_name).from_string(f.read())
