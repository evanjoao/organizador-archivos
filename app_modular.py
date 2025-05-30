# -*- coding: utf-8 -*-
"""
File Organizer - Modular version

This file maintains backward compatibility while using the new modular structure.
The application has been broken down into the following modules:

- file_organizer_core.py: Core file organization logic
- ui_components.py: UI styling and theme management
- directory_manager.py: Directory tree management
- statistics.py: File statistics functionality
- main_app.py: Main application orchestration

For new development, use main_app.py directly.
"""

# Import the modular components
from main_app import FileOrganizerApp, main
from file_organizer_core import FileOrganizer

# Maintain backward compatibility
App = FileOrganizerApp

# Re-export the main function for backward compatibility
if __name__ == "__main__":
    main()
