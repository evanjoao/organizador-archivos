#!/usr/bin/env python3
"""
Test script to demonstrate File Organizer functionalities
Creates test files for testing
"""

import os
import tempfile
from datetime import datetime, timedelta
import random
import json


def create_test_files():
    """Creates test files in a temporary directory"""

    # Create test directory
    test_dir = os.path.expanduser("~/test_organizer")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # File types to create
    file_types = {
        "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
        "images": [".jpg", ".png", ".gif", ".bmp", ".svg"],
        "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
        "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "archives": [".zip", ".rar", ".7z", ".tar"],
        "code": [".py", ".js", ".html", ".css", ".json"],
    }

    # Base names for files
    base_names = [
        "report",
        "document",
        "image",
        "photo",
        "video",
        "movie",
        "song",
        "music",
        "backup",
        "archive",
        "script",
        "code",
        "presentation",
        "spreadsheet",
        "project",
        "data",
    ]

    created_files = []

    print(f"Creating test files in: {test_dir}")

    for category, extensions in file_types.items():
        for i in range(3):  # 3 files per category
            # Select random name and extension
            base_name = random.choice(base_names)
            extension = random.choice(extensions)

            # Create unique name
            filename = f"{base_name}_{category}_{i+1}{extension}"
            filepath = os.path.join(test_dir, filename)

            # Create file with dummy content
            with open(filepath, "w") as f:
                f.write(f"Test file: {filename}\n")
                f.write(f"Category: {category}\n")
                f.write(f"Created: {datetime.now()}\n")
                f.write("Test content " * 20)  # Content to give size

            # Modify date of some files for filter testing
            if random.choice([True, False]):
                # Change modification date randomly
                days_ago = random.randint(1, 30)
                old_time = datetime.now() - timedelta(days=days_ago)
                timestamp = old_time.timestamp()
                os.utime(filepath, (timestamp, timestamp))

            created_files.append(filepath)

    # Create some additional files with specific names for testing
    special_files = [
        "importante.pdf",
        "foto_vacaciones.jpg",
        "proyecto_final.py",
        "backup_2024.zip",
        "musica_favorita.mp3",
    ]

    for filename in special_files:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, "w") as f:
            f.write(f"Special file: {filename}\n")
            f.write("Specific test content\n")
        created_files.append(filepath)

    print(f"✅ Created {len(created_files)} test files")
    print(f"📁 Directory: {test_dir}")

    # Show summary
    print("\n📊 Summary of created files:")
    file_count = {}
    for filepath in created_files:
        ext = os.path.splitext(filepath)[1].lower()
        file_count[ext] = file_count.get(ext, 0) + 1

    for ext, count in sorted(file_count.items()):
        print(f"   {ext}: {count} files")

    print(f"\n🚀 You can use these files to test File Organizer:")
    print(f"   1. Run: python app.py")
    print(f"   2. Select directory: {test_dir}")
    print(f"   3. Test the different functionalities")

    return test_dir, created_files


def create_test_config():
    """Creates a custom test configuration"""

    test_config = {
        "categories": {
            "Important Documents": [".pdf", ".doc", ".docx"],
            "Personal Photos": [".jpg", ".jpeg", ".png"],
            "Python Code": [".py", ".pyw"],
            "Backup Files": [".zip", ".rar", ".7z", ".tar"],
            "Multimedia": [".mp4", ".mp3", ".avi", ".wav"],
        }
    }

    config_path = os.path.expanduser("~/test_organizer/test_settings.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)

    print(f"📋 Test configuration created: {config_path}")
    return config_path


if __name__ == "__main__":
    print("🧪 File Organizer - Test Script")
    print("=" * 50)

    try:
        # Create test files
        test_dir, files = create_test_files()

        # Create test configuration
        config_path = create_test_config()

        print("\n✨ Everything ready to test File Organizer!")
        print("\n📝 Test suggestions:")
        print("   • Use Settings to create custom categories")
        print("   • Apply size filters (small/large files)")
        print("   • Filter by date (recent/old files)")
        print("   • Use Preview to see changes before applying")
        print("   • Test the Undo system after organizing")
        print("   • Check Statistics to see the distribution")

    except Exception as e:
        print(f"❌ Error: {e}")
