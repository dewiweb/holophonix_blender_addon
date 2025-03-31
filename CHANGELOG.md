# Changelog

## v1.3.4 - 2025-03-31

### Added
- New handler operators for toggling and setting directions:
  - ToggleLocationHandlers
  - SetLocationDirections
  - ToggleColorHandlers
  - SetColorDirections
  - ToggleNameHandlers
  - SetNameDirections
- Auto-Manage Handlers toggle for better control over track handlers
- Persistent handler configurations using enabled attribute

### Changed
- Improved icon management system
  - Added deferred icon registration
  - Better error handling
  - Proper cleanup during unregister
- Updated addon metadata with better descriptions and URLs
- Improved UI organization with sub-panels and better hierarchy
- Simplified track handler management system

### Removed
- Unused track handler code:
  - track_handler_settings.py
  - track_handler_proxy.py
  - handler_properties.py
  - manage_track_handlers.py

### Fixed
- Infinite update loop in track handler management
- Direction settings for disabled handlers

## v1.3.3-beta - 2025-03-30

### Added
- Global "Auto-Manage Handlers" toggle in Track Handlers panel

### Changed
- Improved track handler management system to respect individual handler customizations
- Enhanced track handlers panel UI to always show direction settings
- Optimized track handler management using enabled attribute

### Fixed
- Direction update issue for disabled track handlers
- Updated initialization and export files

## v1.3.2 - 2025-03-26

### Added
- Implemented spherical to Cartesian conversion with drivers.
- Added NodeOSC_keys cleanup when deleting tracks.

### Fixed
- Resolved merge conflicts and cleaned up track handler references.
- Fixed math domain errors in AED properties and drivers.
- Ensured values are within valid ranges in AED properties.

### Changed
- Updated AED properties and drivers for improved property definitions.
- Removed deprecated track handlers panel and updated related operators.
- Improved track handler management: clear handlers when selecting `.hol` files or importing tracks directly.

### Documentation
- Documented handler cleanup improvements and future track-handler lifecycle management tasks.

## v1.3.1-beta (Upcoming Release)

> Note: This release builds upon v1.3.0-beta with additional track handler management improvements

### Features
- Add auto-manage handlers toggle for improved NodeOSC integration
- Implement smarter track handler management system
- Add utility script for addon reloading during development

### Improvements
- Reorganize track handlers UI for better usability
- Always show direction settings for disabled handlers
- Improve addon registration and initialization process
- Add better support for multiple scenes
- Update panel parent-child relationships for better organization
- Rename main panel file and update class names for clarity

### Bug Fixes
- Fix issue where direction changes weren't applied to disabled handlers
- Prevent infinite update loops in track handler management
- Fix scene reference issue by setting globalScene for Animation Nodes Tree
- Handle null value for defaultPreset in project's manifest.json

### Refactoring
- Move hostname resolver to dedicated communication module
- Replace complex track handler properties with simplified implementation
- Improve code organization with better separation of concerns
- Add detailed implementation documentation
- Move Holophonix Communication panel to its own file
- Update core utility files and import systems
- Mark osc_operations.py as deprecated and improve error handling

## v1.2.0-stable

### Features
- Implement default .hol file selection from manifest
- Add venue asset tracking to prevent accidental cleanup
- Add scaling functionality to venue loading operator
- Add project_name property for Holophonix project metadata
- Add collection management system for speakers and tracks

### Improvements
- Enhance speaker-related operators with improved import and add functionality
- Update panel icons for better visual consistency
- Improve project import functionality and panel UI

### Bug Fixes
- Update class references in __init__.py
- Fix NodeOSCPreferences folder attribute issue

### Refactoring
- Update terminology from 'sources' to 'tracks'
- Consolidate properties into FileProperties class
- Organize properties into dedicated files:
  - file_properties.py for project-related properties
  - handler_properties.py for OSC handler configurations
  - icon_utils.py for icon management

## v1.1.2-beta
### Features
- Implement default .hol file selection from manifest
- Add venue asset tracking to prevent accidental cleanup
- Add scaling functionality to venue loading operator
- Add project_name property for Holophonix project metadata
- Add collection management system for speakers and tracks

### Improvements
- Enhance speaker-related operators with improved import and add functionality
- Update panel icons for better visual consistency
- Improve project import functionality and panel UI

### Bug Fixes
- Update class references in __init__.py
- Fix NodeOSCPreferences folder attribute issue

### Refactoring
- Update terminology from 'sources' to 'tracks'
- Consolidate properties into FileProperties class
- Organize properties into dedicated files:
  - file_properties.py for project-related properties
  - handler_properties.py for OSC handler configurations
  - icon_utils.py for icon management

## v1.1.1-beta
- Initial release with collection management and UI improvements
