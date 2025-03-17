# Changelog

## v1.1.2-beta (Current Version)

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
