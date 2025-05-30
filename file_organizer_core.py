# -*- coding: utf-8 -*-
"""
Core file organization functionality.
Contains the main logic for organizing files into categories.
"""
import os
import shutil
import logging
from settings_manager import SettingsManager
from preview_undo import UndoManager
from filters import FileFilter


class FileOrganizer:
    """Core file organization logic."""

    def __init__(self, settings_manager=None):
        self.files_moved_count = 0
        self.folders_created_count = 0
        self.log_messages = []
        self.settings_manager = settings_manager or SettingsManager()
        self.file_filter = FileFilter()

    def get_file_extension(self, filename):
        """Gets the file extension in lowercase."""
        return os.path.splitext(filename)[1].lower()

    def get_category_for_extension(self, extension):
        """Determines the category (folder name) for a given extension."""
        categories = self.settings_manager.get_categories()
        for category, extensions in categories.items():
            if extension in extensions:
                return category
        return "Others"

    def get_files_to_organize(self, source_directory):
        """Gets the list of files to organize, applying filters."""
        if not os.path.isdir(source_directory):
            return []

        try:
            all_files = [
                f
                for f in os.listdir(source_directory)
                if os.path.isfile(os.path.join(source_directory, f))
            ]

            # Apply filters
            filtered_files = self.file_filter.apply_filters(all_files, source_directory)
            return filtered_files

        except Exception as e:
            logging.error(f"Error getting files: {e}")
            return []

    def organize_files(
        self, source_directory, progress_callback=None, create_operation_record=True
    ):
        """
        Organizes files in the source directory by moving them to subfolders
        based on their type.
        """
        if not os.path.isdir(source_directory):
            error_message = (
                f"The directory '{source_directory}' does not exist or is invalid."
            )
            logging.error(error_message)
            self.log_messages.append(error_message)
            return 0, 0, error_message

        self.files_moved_count = 0
        self.folders_created_count = 0
        self.log_messages = [f"Starting organization in: {source_directory}"]

        # For the undo system
        operation_moves = []
        folders_created = []

        try:
            files = self.get_files_to_organize(source_directory)
            total_files = len(files)

            if total_files == 0:
                self.log_messages.append(
                    "No files found to organize (after applying filters)."
                )
                return 0, 0, "\n".join(self.log_messages)

            for index, item_name in enumerate(files, 1):
                if progress_callback:
                    progress = (index / total_files) * 100
                    progress_callback(progress)

                item_path = os.path.join(source_directory, item_name)
                file_extension = self.get_file_extension(item_name)
                category_name = self.get_category_for_extension(file_extension)

                destination_folder_path = os.path.join(source_directory, category_name)
                if not os.path.exists(destination_folder_path):
                    try:
                        os.makedirs(destination_folder_path)
                        self.folders_created_count += 1
                        folders_created.append(destination_folder_path)
                        msg = f"Folder created: {destination_folder_path}"
                        self.log_messages.append(msg)
                        logging.info(msg)
                    except OSError as e:
                        error_msg = (
                            f"Error creating folder {destination_folder_path}: {e}"
                        )
                        self.log_messages.append(error_msg)
                        logging.error(error_msg)
                        continue

                destination_file_path = os.path.join(destination_folder_path, item_name)
                original_item_name = item_name
                base_name, ext_name = os.path.splitext(item_name)
                counter = 1

                while os.path.exists(destination_file_path):
                    item_name_new = f"{base_name}_{counter}{ext_name}"
                    destination_file_path = os.path.join(
                        destination_folder_path, item_name_new
                    )
                    counter += 1

                try:
                    shutil.move(item_path, destination_file_path)
                    self.files_moved_count += 1

                    # Record the movement for undo
                    if create_operation_record:
                        operation_moves.append(
                            {
                                "source_path": item_path,
                                "destination_path": destination_file_path,
                            }
                        )

                    final_name = os.path.basename(destination_file_path)
                    msg = f"Moved: '{original_item_name}' -> '{category_name}/{final_name}'"
                    self.log_messages.append(msg)
                    logging.info(msg)
                except Exception as e:
                    error_msg = f"Error moving '{original_item_name}': {e}"
                    self.log_messages.append(error_msg)
                    logging.error(error_msg)

            # Save operation for undo
            if create_operation_record and (
                self.files_moved_count > 0 or self.folders_created_count > 0
            ):
                undo_manager = UndoManager()
                operation_data = {
                    "source_directory": source_directory,
                    "moves": operation_moves,
                    "folders_created": folders_created,
                    "files_moved": self.files_moved_count,
                    "folders_created_count": self.folders_created_count,
                }
                undo_manager.save_operation(operation_data)

        except Exception as e:
            error_msg = f"Unexpected error during organization: {str(e)}"
            self.log_messages.append(error_msg)
            logging.error(error_msg)
            return (
                self.files_moved_count,
                self.folders_created_count,
                "\n".join(self.log_messages),
            )

        if (
            self.files_moved_count == 0
            and self.folders_created_count == 0
            and total_files > 0
        ):
            self.log_messages.append(
                "No files were moved or new folders created (possibly already organized or errors occurred)."
            )
        elif total_files > 0:
            self.log_messages.append("Organization completed.")

        return (
            self.files_moved_count,
            self.folders_created_count,
            "\n".join(self.log_messages),
        )
