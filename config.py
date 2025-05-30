# -*- coding: utf-8 -*-

# File Types and Destination Folders Configuration
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".rtf",
        ".odt",
        ".ods",
        ".odp",
    ],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"],
    "Compressed Files": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Executables and Installers": [".exe", ".msi", ".dmg", ".pkg"],
    "Scripts": [".py", ".js", ".sh", ".bat", ".java", ".c", ".cpp", ".cs"],
    "Others": [],  # For files that don't match previous categories
}

# Interface configuration
UI_CONFIG = {
    "window_title": "File Organizer",
    "window_size": "800x600",  # Larger window
    "theme": {
        "primary_color": "#2196F3",  # Azul Material Design
        "secondary_color": "#FFC107",  # Amarillo Material Design
        "text_color": "white",
        "background_color": "#F5F5F5",  # Gris claro
        "font_family": "Segoe UI",  # Fuente más moderna
        "font_size": 11,
        "padding": {"small": 5, "medium": 10, "large": 20},
        "colors": {
            "success": "#4CAF50",  # Verde
            "error": "#F44336",  # Rojo
            "warning": "#FF9800",  # Naranja
            "info": "#2196F3",  # Azul
        },
    },
}

# Configuración de logging
LOG_CONFIG = {
    "max_log_entries": 1000,
    "log_file": "file_organizer.log",
    "log_format": "%(asctime)s - %(levelname)s - %(message)s",
}
