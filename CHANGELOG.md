# Changelog

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
- Clear existing track handlers when selecting a new .hol file or importing tracks directly

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
