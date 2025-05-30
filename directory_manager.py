# -*- coding: utf-8 -*-
"""
Directory tree management functionality.
Handles directory browsing, tree population, and selection events.
"""
import os
import logging
from pathlib import Path
from typing import Dict, Union, Optional, Callable, Any
import tkinter as tk
from tkinter import filedialog, ttk


class DirectoryManager:
    """Manages directory tree operations and interactions."""

    # Class constants for better maintainability
    MIN_NAME_COLUMN_WIDTH = 100
    MIN_PATH_COLUMN_WIDTH = 150
    NAME_COLUMN_RATIO = 0.4
    PATH_COLUMN_RATIO = 0.6

    def __init__(
        self,
        dir_tree: ttk.Treeview,
        source_dir_var: tk.StringVar,
        add_log_callback: Callable[[str, str], None],
    ) -> None:
        """
        Initialize DirectoryManager.

        Args:
            dir_tree: Tkinter Treeview widget for displaying directories
            source_dir_var: StringVar to store selected directory path
            add_log_callback: Callback function for logging messages
        """
        self.dir_tree = dir_tree
        self.source_dir_var = source_dir_var
        self.add_log_message = add_log_callback
        self.logger = logging.getLogger(__name__)

    def _get_common_directories(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """Get dictionary of common system directories."""
        home_path = Path.home()

        return {
            "Home": str(home_path),
            "Documents": str(home_path / "Documents"),
            "Downloads": str(home_path / "Downloads"),
            "Desktop": str(home_path / "Desktop"),
            "Pictures": str(home_path / "Pictures"),
            "Music": str(home_path / "Music"),
            "Videos": str(home_path / "Videos"),
            "System": {"Root": "/", "Mounts": "/mnt", "Users": "/home"},
        }

    def _clear_tree(self) -> None:
        """Clear all items from the directory tree."""
        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

    def _add_tree_item(
        self, parent: str, name: str, path: str, open_item: bool = False
    ) -> Optional[str]:
        """
        Add an item to the tree if the path exists and is a directory.

        Args:
            parent: Parent item ID in the tree
            name: Display name for the tree item
            path: File system path
            open_item: Whether to expand the tree item

        Returns:
            Item ID if successfully added, None otherwise
        """
        path_obj = Path(path)
        if path_obj.exists() and path_obj.is_dir():
            return self.dir_tree.insert(
                parent, "end", text=name, values=(str(path_obj),), open=open_item
            )
        return None

    def _find_existing_item_by_path(self, path: str, parent: str = "") -> Optional[str]:
        """
        Find existing tree item with the given path.

        Args:
            path: Path to search for
            parent: Parent item to search within

        Returns:
            Item ID if found, None otherwise
        """
        for item_id in self.dir_tree.get_children(parent):
            item_values = self.dir_tree.item(item_id, "values")
            if item_values and item_values[0] == path:
                return item_id
        return None

    def _select_and_focus_item(self, item_id: str) -> None:
        """Select and focus on a tree item."""
        self.dir_tree.selection_set(item_id)
        self.dir_tree.focus(item_id)

    def load_initial_directories(self) -> None:
        """Load common directories into the tree view."""
        self._clear_tree()
        common_dirs = self._get_common_directories()

        for name, path_or_dict in common_dirs.items():
            if isinstance(path_or_dict, dict):
                # Handle nested directories (like System)
                parent_id = self.dir_tree.insert(
                    "", "end", text=name, values=("",), open=False
                )
                for sub_name, sub_path in path_or_dict.items():
                    self._add_tree_item(parent_id, sub_name, sub_path)
            elif isinstance(path_or_dict, str):
                # Handle direct directories
                self._add_tree_item("", name, path_or_dict)

    def add_directory_to_tree(self, dir_path: str, parent: str = "") -> None:
        """
        Add a specific directory to the tree view.

        Args:
            dir_path: Path of directory to add
            parent: Parent item ID (empty string for root)
        """
        try:
            path_obj = Path(dir_path)

            if not path_obj.exists():
                raise FileNotFoundError(f"Directory does not exist: {dir_path}")

            if not path_obj.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {dir_path}")

            # Check for existing item
            existing_item = self._find_existing_item_by_path(dir_path, parent)
            if existing_item:
                self._select_and_focus_item(existing_item)
                return

            # Add new item
            dir_name = path_obj.name or str(path_obj)
            item = self.dir_tree.insert(
                parent, "end", text=dir_name, values=(dir_path,), open=True
            )
            self._select_and_focus_item(item)

        except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
            self.logger.error(f"Error adding directory to tree: {dir_path}, {e}")
            self.add_log_message(f"Error accessing {dir_path}: {e}", "error")
        except Exception as e:
            self.logger.exception(f"Unexpected error adding directory: {dir_path}")
            self.add_log_message(f"Unexpected error: {e}", "error")

    def refresh_directories(self) -> None:
        """Refresh the directory tree."""
        self.load_initial_directories()
        self.add_log_message("Directory list updated.", "info")

    def browse_directory(self) -> None:
        """Open file dialog to browse for a directory."""
        directory = filedialog.askdirectory(
            initialdir=self.source_dir_var.get() or os.path.expanduser("~")
        )
        if directory:
            self.source_dir_var.set(directory)
            self.add_directory_to_tree(directory)
            self.add_log_message(
                f"Directory selected for organization: {directory}", "success"
            )

    def on_tree_select(self, event: tk.Event) -> None:
        """Handle tree selection events."""
        selected_items = self.dir_tree.selection()
        if selected_items:
            item = selected_items[0]
            # Ensure 'values' is not empty and has at least one element
            item_values = self.dir_tree.item(item, "values")
            if item_values and item_values[0]:
                dir_path = item_values[0]
                self.source_dir_var.set(dir_path)

    def on_window_resize(self, event: Optional[tk.Event] = None) -> None:
        """Handle window resize events to adjust tree columns."""
        # Only adjust if the window already has a size (avoid errors at startup)
        if self.dir_tree.winfo_width() > 1:
            tree_width = self.dir_tree.winfo_width()
            # Use class constants instead of magic numbers
            col_0_width = int(tree_width * self.NAME_COLUMN_RATIO)
            col_1_width = int(tree_width * self.PATH_COLUMN_RATIO)

            # Ensure columns meet minimum width requirements
            col_0_width = max(col_0_width, self.MIN_NAME_COLUMN_WIDTH)
            col_1_width = max(col_1_width, self.MIN_PATH_COLUMN_WIDTH)

            self.dir_tree.column("#0", width=col_0_width)
            self.dir_tree.column("path", width=col_1_width)
