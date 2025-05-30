# -*- coding: utf-8 -*-
"""
File statistics functionality.
Provides file analysis and statistical information display.
"""
import os
import tkinter as tk
from tkinter import messagebox, ttk


class FileStatistics:
    """Handles file statistics analysis and display."""

    def __init__(self, file_organizer):
        self.file_organizer = file_organizer

    def show_file_statistics(self, source_dir, root_window):
        """Shows statistics of files in the selected directory."""
        if not source_dir or not os.path.isdir(source_dir):
            messagebox.showwarning("Warning", "Please select a valid directory first.")
            return

        try:
            files = self.file_organizer.get_files_to_organize(source_dir)

            if not files:
                messagebox.showinfo(
                    "Statistics", "No files found in the selected directory."
                )
                return

            # Group by categories
            categories = {}
            total_size = 0

            for file_name in files:
                file_path = os.path.join(source_dir, file_name)
                file_ext = self.file_organizer.get_file_extension(file_name)
                category = self.file_organizer.get_category_for_extension(file_ext)

                if category not in categories:
                    categories[category] = {"count": 0, "size": 0}

                categories[category]["count"] += 1
                try:
                    file_size = os.path.getsize(file_path)
                    categories[category]["size"] += file_size
                    total_size += file_size
                except OSError:
                    pass

            # Create statistics window
            self._create_statistics_window(root_window, files, categories, total_size)

        except Exception as e:
            messagebox.showerror("Error", f"Error calculating statistics: {e}")

    def _create_statistics_window(self, root_window, files, categories, total_size):
        """Create and display the statistics window."""
        stats_window = tk.Toplevel(root_window)
        stats_window.title("File Statistics")
        stats_window.geometry("400x500")
        stats_window.transient(root_window)
        stats_window.grab_set()

        main_frame = ttk.Frame(stats_window, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="File Statistics", font=("Arial", 14, "bold")).pack(
            anchor="w", pady=(0, 10)
        )

        ttk.Label(main_frame, text=f"Total files: {len(files)}").pack(anchor="w")
        ttk.Label(
            main_frame, text=f"Total size: {self._format_file_size(total_size)}"
        ).pack(anchor="w")
        ttk.Label(main_frame, text=f"Categories: {len(categories)}").pack(
            anchor="w", pady=(0, 10)
        )

        # Treeview for categories
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        tree = ttk.Treeview(tree_frame, columns=("count", "size"), show="tree headings")
        tree.heading("#0", text="Category")
        tree.heading("count", text="Files")
        tree.heading("size", text="Size")
        tree.column("#0", width=150)
        tree.column("count", width=80)
        tree.column("size", width=100)

        for category, data in sorted(categories.items()):
            tree.insert(
                "",
                "end",
                text=category,
                values=(data["count"], self._format_file_size(data["size"])),
            )

        tree.pack(fill="both", expand=True)

        ttk.Button(main_frame, text="Close", command=stats_window.destroy).pack(
            pady=(10, 0)
        )

    def _format_file_size(self, size_bytes):
        """Formats the file size in a readable way."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/1024**2:.1f} MB"
        else:
            return f"{size_bytes/1024**3:.1f} GB"
