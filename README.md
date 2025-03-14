# Holophonix Utils

A Blender addon providing various utility functions for Holophonix projects, including management of Tracks, speakers, handlers, and OSC operations.

## Features

### Project Import System

The addon provides comprehensive Holophonix project import capabilities:

1. **Archive Processing**
   - Extracts and validates `.zip` project files
   - Maintains project relationships and structure
   - Handles errors and invalid files gracefully

2. **Integrated Workflow**
   - Single interface for venue, tracks, and speakers
   - Preserves project metadata from `manifest.json`
   - Automated NodeOSC handler configuration

3. **Component Management**
   - Import tracks and speakers from `.hol` files
   - Load venues from `.glb` files with metadata
   - Configure OSC settings for real-time control

### Track Management

- **Track Import**:
  - Imports Tracks from a Holophonix `.hol` preset file
  - Replaces existing Tracks with those from the imported file
  - Handles Track numbering and naming conventions

- **Track Properties**:
  - Manages Track coordinates (cartesian and spherical)
  - Handles Track colors and materials
  - Supports custom 3D models for Tracks

- **Track Creation**:
  - Creates Tracks from imported data
  - Assigns appropriate 3D models from the `amadeus.blend` file
  - Sets Track locations based on imported coordinates

- **Track Deletion**:
  - Clears existing Tracks before importing new ones
  - Removes unused meshes and materials

- **Coordinate Conversion**:
  - Converts between cartesian and spherical coordinate systems
  - Handles elevation, azimuth, and distance calculations

- **Import `.zip` Files**: Extract and validate Holophonix project folders from `.zip` files.
- **Optional Tracks and Speakers Import**: Import tracks and speakers from `.hol` files using a dropdown menu.

### Speaker Management

- **Speaker Import**:
  - Imports Speakers from a Holophonix `.hol` preset file
  - Replaces existing Speakers with those from the imported file
  - Handles Speaker numbering and naming conventions

- **Speaker Properties**:
  - Manages Speaker coordinates (cartesian and spherical)
  - Handles Speaker colors and materials
  - Supports custom 3D models for Speakers

- **Speaker Creation**:
  - Creates Speakers from imported data
  - Assigns appropriate 3D models from the `amadeus.blend` file
  - Sets Speaker locations based on imported coordinates

- **Speaker Deletion**:
  - Clears existing Speakers before importing new ones
  - Removes unused meshes and materials

- **Speaker Orientation**:
  - Manages Speaker rotation and orientation
  - Supports auto-orientation and manual rotation settings
  - Handles pan, tilt, and roll parameters

- **Coordinate Conversion**:
  - Converts between cartesian and spherical coordinate systems
  - Handles elevation, azimuth, and distance calculations

### Venue Loading System

The enhanced venue loading system:
- Maintains consistent scale and orientation
- Applies position/rotation from `manifest.json`
- Supports custom panel icons and default state
- Includes robust error handling

### Handler Management

Our addon provides integration with NodeOSC for:
- Automatic creation of track handlers
- Enable/disable control for incoming/outgoing handlers
- Configuration of handler properties and priorities
- Management of handler lifecycle and cleanup

### OSC Integration

The addon works with NodeOSC to:
- Configure handler settings for tracks
- Enable real-time control of audio parameters
- Support synchronization with visual elements

### AN Settings

- **Configure AN-Specific Settings**: Adjust settings related to Animation Nodes functionality. This includes settings for node execution, debugging, and performance optimization.
- **Manage AN Tree Imports**: Import and export AN trees for reuse across projects. This allows you to share complex animations and node setups with other users or projects.
- **Example Use Cases**:
  - Automating complex animations with imported AN trees, such as character rigging or physics simulations.
  - Sharing AN trees with other users or projects, enabling collaboration and reuse of complex node setups.

## User Guide

### Quick Start

1. **Enable the Addon**:
   - Go to Edit > Preferences > Add-ons
   - Search for 'Holophonix Utils' and enable it

2. **Access the Panel**:
   - Open the 3D View sidebar (N key)
   - Find the 'Holophonix Utils' tab

3. **Import Your Setup**:
   - Click 'Import' in the Sources or Speakers panel
   - Select your `.hol` preset file

4. **Configure OSC**:
   - Set up your OSC connections in the NodeOSC panel
   - Enable handlers for the features you need

### Practical Examples

**Live Performance Setup**:
1. Import your venue's speaker layout
2. Configure OSC to control audio parameters
3. Create visualizations that respond to audio

**Interactive Installation**:
1. Set up multiple Holophonix presets
2. Create handlers for interactive elements
3. Sync multiple installations via OSC

### Troubleshooting

**Issue**: Tracks/Speakers not appearing
- Verify your `.hol` file format
- Check Blender's console for import errors

**Issue**: OSC not working
- Confirm IP and port settings
- Check firewall/network settings
- Verify NodeOSC is properly configured

## About Holophonix

The Holophonix Processor is an advanced real-time immersive audio environment optimized for the performing arts field. It enables precise spatial audio control, allowing users to create immersive soundscapes for live performances, installations, and other artistic applications. The processor integrates advanced 2D and 3D sound algorithms developed at IRCAM, supporting object-based mixing and multiple spatialization techniques.

### Key Features
- **2D and 3D Spatialization**: Utilize cutting-edge algorithms for precise sound placement in both 2D and 3D spaces.
- **Object-Based Mixing**: Associate input channels with various object types for flexible and dynamic audio control.
- **Active Acoustic Enhancement**: Enhance the acoustic properties of a space in real-time.

For more details, visit the [Holophonix Documentation](https://holophonix.xyz/documentation/docs/intro).

### Purpose of the Blender Addon

The Holophonix Utils addon integrates the Holophonix Processor’s capabilities into Blender, enabling users to:
- **Visualize Audio in 3D**: Represent sound sources (e.g., tracks, speakers) as 3D objects in Blender, allowing for intuitive spatial audio design.
- **Synchronize Audio and Visuals**: Use OSC messages to control animations, lighting, and other visual elements in Blender, ensuring perfect synchronization with the audio.
- **Streamline Workflows**: Simplify the process of importing and managing Holophonix presets, tracks, and speakers within Blender.

## Installation

1. Download the latest release
2. In Blender, go to Edit > Preferences > Add-ons
3. Click 'Install...' and select the downloaded zip file
4. Enable the addon

## Dependencies

- Blender 4.3 or higher
- [Animation Nodes](https://github.com/JacquesLucke/animation_nodes): A node-based visual scripting system for Blender, enabling complex animations and procedural workflows. Required for AN tree functionality in the Holophonix Utils addon.
- [NodeOSC](https://github.com/maybites/NodeOSC): A Blender addon for Open Sound Control (OSC) communication, enabling real-time interaction between Blender and external devices. Required for OSC operations in the Holophonix Utils addon.

## Assets

The `amadeus.blend` file in the assets directory contains:
- 3D models of Amadeus speakers
- Track models supported by default in the Holophonix Processor
- Animation Nodes' AN Tree necessary for Animation Nodes functionalities

This file enables importing Tracks and speakers from a Holophonix project's `.hol` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## TODO

1. **Rework Request System**
   - Transition from `/dump` to `/get` request system
   - Update all related API calls and endpoints
   - Ensure backward compatibility during transition
