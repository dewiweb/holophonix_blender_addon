# Track Handler System Implementation Plan

## Overview
This document outlines the plan to replace the current complex track handler system with a simplified approach that directly interacts with the NodeOSC_keys collection. The new implementation will provide automatic updates, a cleaner codebase, and improved user experience.

## Implementation Tasks

### 1. Create New Files

- [x] **Create `utils/track_handler_settings.py`**
  - Implement `TrackHandlerSettings` property group
  - Add automatic update callbacks for all properties
  - Ensure proper initialization handling

- [x] **Create `operators/manage_track_handlers.py`**
  - Implement `SNA_OT_ManageTrackHandlers` operator
  - Add functionality to clear existing handlers
  - Add functionality to create new handlers based on settings
  - Support both manual and automatic triggering

- [x] **Create `panels/track_handlers_panel.py`**
  - Implement `SNA_PT_TrackHandlers` panel
  - Create UI for managing track handler settings
  - Add informational elements for better user guidance

### 2. Update Module __init__.py Files

- [x] **Update `utils/__init__.py`**
  - Add import for `TrackHandlerSettings`
  - Add `TrackHandlerSettings` to `__all__` list
  - Remove imports for old track handler classes (if removing them)

- [x] **Update `operators/__init__.py`**
  - Add import for `SNA_OT_ManageTrackHandlers`
  - Add `SNA_OT_ManageTrackHandlers` to `__all__` list
  - Update imports for old track handler operators (if removing them)

- [x] **Update `panels/__init__.py`**
  - Add import for `SNA_PT_TrackHandlers`
  - Add `SNA_PT_TrackHandlers` to `__all__` list
  - Update imports for old track handler panels (if removing them)

### 3. Remove or Comment Out Old Code

- [ ] **Update `utils/handler_properties.py`**
  - Remove or comment out `TrackHandlerCategoryProperties`
  - Remove or comment out `TrackHandlerProperties`
  - Keep any code that might be needed by other parts of the addon

- [ ] **Update `operators/create_track_handlers.py`**
  - Remove or comment out track handler creation code
  - Keep any code that might be needed by other parts of the addon (e.g., hostname resolution)

- [ ] **Update `panels/tracks_panel.py`**
  - Remove or comment out track handler UI code
  - Keep any code that might be needed by other parts of the addon

### 4. Update Root __init__.py

- [x] **Update class registration**
  - Remove old track handler classes from the `classes` list
  - Add new track handler classes to the `classes` list in the proper order
  - Ensure classes are registered in the correct dependency order

- [x] **Update property registration**
  - Remove registration of old track handler properties
  - Add registration for new `track_handler_settings` property
  - Update unregistration code accordingly

### 5. Update app_handlers.py

- [x] **Replace old initialization code**
  - Implement new `initialize_track_handlers` function
  - Ensure proper handling of the `is_initializing` flag
  - Add any necessary error handling

### 6. Testing

- [ ] **Test basic functionality**
  - Verify that the new panel appears correctly
  - Verify that settings can be changed
  - Verify that track handlers are created correctly

- [ ] **Test automatic updates**
  - Verify that changing settings automatically updates handlers
  - Verify that the update process doesn't cause recursion or other issues
  - Test with various combinations of settings

- [ ] **Test edge cases**
  - Test with no tracks in the scene
  - Test with NodeOSC not available
  - Test with various track naming patterns

### 7. Documentation

- [ ] **Update code comments**
  - Add clear comments to all new code
  - Explain the purpose and functionality of each component

- [ ] **Update user documentation**
  - Update any user-facing documentation to reflect the new system
  - Add tooltips and help text in the UI

## Implementation Notes

- This plan assumes a direct replacement of the old system without maintaining backward compatibility
- The implementation focuses on simplicity, maintainability, and user experience
- All new code should follow the addon's existing coding style and patterns
- The new system should be thoroughly tested before finalizing the implementation

## Completion Criteria

The implementation will be considered complete when:
1. All new files and code changes are implemented
2. The old code is removed or properly commented out
3. The new system functions correctly in all test cases
4. The code is well-documented and follows the addon's coding standards

### Current Task: Handler Cleanup When Loading New .hol Files

**Issue:**
When loading a new .hol file, old track handlers are only disabled but remain in the NodeOSC_keys collection, potentially causing resource leaks and state confusion.

**Solution:**
1. **Full Handler Removal**
   - Remove old handlers from NodeOSC_keys collection
   - Ensure complete cleanup before adding new handlers
   - Add error handling for the transition

2. **Distinct Cleanup Modes**
   - Full removal for .hol file changes
   - Disable/enable for regular updates

3. **State Tracking**
   - Track handler source (.hol file)
   - Clear handlers by source

**Implementation Steps:**
1. Add handler removal method
2. Modify execute method to call removal before creation
3. Update clear method to handle both modes
4. Add error handling and logging

### Future Task: Track-Handler Lifecycle Management

**Objective:** 
Link track objects to their handlers for automatic cleanup and better resource management.

**Implementation Steps:**

1. **Track-Handler Association**
   - Add track reference to handler properties
   - Store track ID in handler metadata
   - Create mapping between tracks and handlers

2. **Automatic Cleanup**
   - Add handler removal when track is deleted
   - Implement through Blender's app handlers
   - Add error handling for edge cases

3. **UI Integration**
   - Add visual feedback for linked handlers
   - Provide cleanup options in UI
   - Add status indicators

**Expected Benefits:**
- Automatic cleanup of orphaned handlers
- Better resource management
- More intuitive user experience
- Easier debugging and troubleshooting
