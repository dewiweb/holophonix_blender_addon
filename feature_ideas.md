# Future Features: Holophonix Project Importer

## Overview
The **Holophonix Project Importer** will allow users to import and explore Holophonix projects exported as `.zip` files. The feature will extract relevant files (e.g., `.glb` for venues, `.hol` for presets, and `manifest.json` for metadata) and integrate them into Blender for exploration and use.

---

## Key Features
1. **Import `.zip` Files:**
   - Extract and parse Holophonix project folders from `.zip` files.
   - Validate the project structure (Presets, Venue, `manifest.json`).

2. **Optional Venue Loading:**
   - Parse `manifest.json` for scale, position, and rotation information.
   - Provide a “Load Venue” button to load the `.glb` file into the scene.

3. **Optional Tracks and Speakers Import:**
   - Provide a dropdown menu to select `.hol` files from the Presets subfolder.
   - Enable “Import Tracks” and “Import Speakers” buttons after selecting a `.hol` file.
   - Import tracks and speakers only when the respective button is clicked.

4. **Configure OSC Settings:**
   - Parse OSC settings (IP and port) from `manifest.json`.
   - Import these settings into NodeOSC for real-time communication.

---

## Workflow

### **1. Import `.zip` File**
- User selects a `.zip` file exported from the Holophonix processor.
- The system extracts the `.zip` file and validates the project structure.

### **2. Optional Venue Loading**
- The system parses `manifest.json` for venue metadata.
- User clicks the “Load Venue” button.
- The system loads the `.glb` file into the scene, applying scale, position, and rotation from `manifest.json`.

### **3. Select `.hol` Preset File**
- The system provides a dropdown menu listing `.hol` files from the Presets subfolder.
- User selects a `.hol` file from the dropdown.
- The system enables the “Import Tracks” and “Import Speakers” buttons.

### **4. Optional Tracks and Speakers Import**
- User clicks the “Import Tracks” button.
  - The system imports tracks from the selected `.hol` file.
- User clicks the “Import Speakers” button.
  - The system imports speakers from the selected `.hol` file.

### **5. Configure OSC Settings**
- The system parses OSC settings from `manifest.json`.
- These settings are imported into NodeOSC for real-time communication.

---

## UI Enhancements
- **Import Panel:**
  - Button to select and import `.zip` files.
  - “Load Venue” button (disabled until a `.zip` file is imported).
  - Dropdown menu for selecting `.hol` files.
  - “Import Tracks” and “Import Speakers” buttons (disabled until a `.hol` file is selected).
  - Summary of the imported project (venue, presets, OSC settings).

---

## Implementation Details
### **Backend Logic**
- Use Python’s `zipfile` module to extract `.zip` files.
- Use `bpy.ops.import_scene.gltf` to load `.glb` files.
- Reuse the existing `.hol` file parser to import tracks and speakers.
- Use NodeOSC addon to handle OSC communication.

### **Error Handling**
- Validate the `.zip` file structure and contents.
- Handle missing or corrupted files gracefully.
- Provide feedback for invalid OSC settings or `.hol` files.

---

## Example Workflow
1. User selects a `.zip` file from the Holophonix processor.
2. The system extracts the `.zip` file and validates the project structure.
3. User clicks the “Load Venue” button.
   - The system loads the `.glb` file into the scene.
4. User selects a `.hol` file from the dropdown.
5. User clicks the “Import Tracks” button.
   - The system imports tracks from the selected `.hol` file.
6. User clicks the “Import Speakers” button.
   - The system imports speakers from the selected `.hol` file.
7. The system imports OSC settings into NodeOSC for real-time communication.

---

## Benefits
- **Seamless Integration:** Users can import and explore Holophonix projects directly in Blender.
- **Efficiency:** Automates the process of loading venues, tracks, and speakers.
- **Flexibility:** Users can modify and export project data for use in the Holophonix processor.
