# -*- coding: utf-8 -*-
"""
Main File Organizer application.
Orchestrates all components and provides the main UI functionality.
"""
import os
import tkinter as tk
from tkinter import messagebox, ttk
import logging
from datetime import datetime

from config import UI_CONFIG, LOG_CONFIG
from file_organizer_core import FileOrganizer
from ui_components import UIStyles, LogManager
from directory_manager import DirectoryManager
from statistics import FileStatistics
from settings_manager import SettingsManager, SettingsWindow
from preview_undo import PreviewManager, UndoManager, PreviewWindow, UndoWindow
from filters import FilterWindow

# Logging configuration
logging.basicConfig(
    filename=LOG_CONFIG["log_file"], level=logging.INFO, format=LOG_CONFIG["log_format"]
)


class FileOrganizerApp:
    """Main File Organizer application class."""

    def __init__(self, root):
        self.root = root
        self.root.title(UI_CONFIG["window_title"])
        self.root.geometry(UI_CONFIG["window_size"])
        self.root.option_add(
            "*Font",
            (UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        # Initialize components
        self.settings_manager = SettingsManager()
        self.file_organizer = FileOrganizer(self.settings_manager)
        self.preview_manager = PreviewManager(self.file_organizer)
        self.undo_manager = UndoManager()

        # Initialize UI
        self.ui_styles = UIStyles(root)
        self.setup_ui()

        # Initialize managers
        self.directory_manager = DirectoryManager(
            self.dir_tree, self.source_dir_var, self.add_log_message
        )
        self.statistics_manager = FileStatistics(self.file_organizer)

        # Load initial data and setup event handlers
        self.directory_manager.load_initial_directories()
        self.root.bind("<Configure>", self.directory_manager.on_window_resize)

    def setup_ui(self):
        """Setup the main user interface."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.configure(background=UI_CONFIG["theme"]["background_color"])

        main_frame = ttk.Frame(
            self.root,
            padding=UI_CONFIG["theme"]["padding"]["large"],
            style="Custom.TLabelframe",
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        # Configure rows for expansion
        main_frame.grid_rowconfigure(0, weight=0)  # title_label
        main_frame.grid_rowconfigure(1, weight=1)  # dir_selection_frame
        main_frame.grid_rowconfigure(2, weight=0)  # selected_dir_frame
        main_frame.grid_rowconfigure(3, weight=0)  # progress_frame
        main_frame.grid_rowconfigure(4, weight=0)  # organize_button
        main_frame.grid_rowconfigure(5, weight=2)  # log_frame

        self._create_title_section(main_frame)
        self._create_directory_section(main_frame)
        self._create_selected_directory_section(main_frame)
        self._create_progress_section(main_frame)
        self._create_action_buttons_section(main_frame)
        self._create_log_section(main_frame)

    def _create_title_section(self, parent):
        """Create the title section."""
        title_label = ttk.Label(
            parent,
            text="File Organizer",
            font=(UI_CONFIG["theme"]["font_family"], 18, "bold"),
            anchor="center",
            style="Custom.TLabelframe.Label",
        )
        title_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["large"]),
        )

    def _create_directory_section(self, parent):
        """Create the directory selection section."""
        dir_selection_frame = ttk.Frame(parent, style="Custom.TLabelframe")
        dir_selection_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )
        dir_selection_frame.grid_columnconfigure(0, weight=3)
        dir_selection_frame.grid_columnconfigure(1, weight=1)
        dir_selection_frame.grid_rowconfigure(0, weight=1)

        # Directory tree
        self._create_directory_tree(dir_selection_frame)

        # Control buttons
        self._create_control_buttons(dir_selection_frame)

    def _create_directory_tree(self, parent):
        """Create the directory tree view."""
        dir_tree_frame = ttk.LabelFrame(
            parent,
            text="Available Directories",
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            style="Custom.TLabelframe",
        )
        dir_tree_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )
        dir_tree_frame.grid_rowconfigure(0, weight=1)
        dir_tree_frame.grid_columnconfigure(0, weight=1)

        tree_container = ttk.Frame(dir_tree_frame, style="Custom.TLabelframe")
        tree_container.grid(row=0, column=0, sticky="nsew", pady=(10, 0))
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        self.dir_tree = ttk.Treeview(
            tree_container,
            columns=("path",),
            show="tree headings",
            style="Custom.Treeview",
        )
        self.dir_tree.heading("#0", text="Name")
        self.dir_tree.heading("path", text="Path")
        self.dir_tree.column("#0", width=200, minwidth=150, stretch=tk.YES)
        self.dir_tree.column("path", width=300, minwidth=200, stretch=tk.YES)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(
            tree_container, orient="vertical", command=self.dir_tree.yview
        )
        tree_scroll_x = ttk.Scrollbar(
            tree_container, orient="horizontal", command=self.dir_tree.xview
        )
        self.dir_tree.configure(
            yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set
        )

        self.dir_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_rowconfigure(1, weight=0)
        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_columnconfigure(1, weight=0)

        # Bind selection event (will be handled by DirectoryManager)
        self.dir_tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _create_control_buttons(self, parent):
        """Create the control buttons section."""
        controls_frame = ttk.Frame(parent, style="Custom.TLabelframe")
        controls_frame.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(UI_CONFIG["theme"]["padding"]["small"], 0),
        )
        controls_frame.grid_columnconfigure(0, weight=1)

        buttons = [
            ("↻ Refresh", self._refresh_directories),
            ("+ Other Directory", self._browse_directory),
            ("⚙ Settings", self.open_settings),
            ("🔍 Filters", self.open_filters),
            ("↶ Undo", self.open_undo_window),
        ]

        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(
                controls_frame,
                text=text,
                command=command,
                style="Custom.TButton",
            )
            button.grid(
                row=i,
                column=0,
                sticky="ew",
                pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
            )

    def _create_selected_directory_section(self, parent):
        """Create the selected directory display section."""
        selected_dir_frame = ttk.LabelFrame(
            parent,
            text="Selected Directory",
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            style="Custom.TLabelframe",
        )
        selected_dir_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(
                UI_CONFIG["theme"]["padding"]["medium"],
                UI_CONFIG["theme"]["padding"]["medium"],
            ),
        )
        selected_dir_frame.grid_columnconfigure(0, weight=1)

        self.source_dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(
            selected_dir_frame,
            textvariable=self.source_dir_var,
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
            ),
        )
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    def _create_progress_section(self, parent):
        """Create the progress bar section."""
        progress_outer_frame = ttk.Frame(parent, style="Custom.TLabelframe")
        progress_outer_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )
        progress_outer_frame.grid_columnconfigure(0, weight=1)

        progress_label = ttk.Label(
            progress_outer_frame, text="Progress:", style="Custom.TLabelframe.Label"
        )
        progress_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 5),
            pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_outer_frame,
            variable=self.progress_var,
            maximum=100,
            style="Custom.Horizontal.TProgressbar",
        )
        self.progress_bar.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )

    def _create_action_buttons_section(self, parent):
        """Create the action buttons section."""
        organize_buttons_frame = ttk.Frame(parent)
        organize_buttons_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )
        organize_buttons_frame.grid_columnconfigure(0, weight=1)
        organize_buttons_frame.grid_columnconfigure(1, weight=1)

        preview_button = ttk.Button(
            organize_buttons_frame,
            text="📋 Preview Organization",
            command=self.preview_organization,
            style="Custom.TButton",
        )
        preview_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.organize_button = ttk.Button(
            organize_buttons_frame,
            text="🗂 Organize Files",
            command=self.start_organization,
            style="Custom.TButton",
        )
        self.organize_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _create_log_section(self, parent):
        """Create the activity log section."""
        log_frame = ttk.LabelFrame(
            parent,
            text="Activity Log",
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            style="Custom.TLabelframe",
        )
        log_frame.grid(row=5, column=0, sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_container = ttk.Frame(log_frame, style="Custom.TLabelframe")
        log_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        log_container.grid_rowconfigure(0, weight=1)
        log_container.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_container,
            wrap=tk.WORD,
            height=10,
            state=tk.DISABLED,
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            bg=UI_CONFIG["theme"]["background_color"],
            fg="black",
            padx=UI_CONFIG["theme"]["padding"]["small"],
            pady=UI_CONFIG["theme"]["padding"]["small"],
            relief=tk.SOLID,
            borderwidth=1,
        )
        log_scroll = ttk.Scrollbar(
            log_container, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll.grid(row=0, column=1, sticky="ns")

        # Initialize log manager for styling
        self.log_manager = LogManager(self.log_text)

    # Event handlers
    def _on_tree_select(self, event):
        """Handle tree selection events."""
        self.directory_manager.on_tree_select(event)

    def _refresh_directories(self):
        """Refresh the directory tree."""
        self.directory_manager.refresh_directories()

    def _browse_directory(self):
        """Browse for a directory."""
        self.directory_manager.browse_directory()

    # Utility methods
    def add_log_message(self, message, message_type="info"):
        """Add a message to the activity log."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # If the message is a list (from FileOrganizer), join it
        if isinstance(message, list):
            message = "\n".join(message)

        # Split the message into lines to apply the tag to each if multiline
        lines = message.split("\n")
        for line in lines:
            if line.strip():  # Avoid empty lines or lines with only spaces
                formatted_message = f"{timestamp} - {line}\n"
                self.log_text.insert(tk.END, formatted_message, message_type)

        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        """Clear the activity log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_progress(self, value):
        """Update the progress bar."""
        self.progress_var.set(value)
        self.root.update_idletasks()

    # Action methods
    def start_organization(self):
        """Start the file organization process."""
        source_dir = self.source_dir_var.get()
        if not source_dir:
            messagebox.showwarning(
                "Directory Not Specified",
                "Please select a directory to organize.",
            )
            return
        if not os.path.isdir(source_dir):
            messagebox.showerror(
                "Invalid Directory",
                f"The path '{source_dir}' is not a valid directory.",
            )
            return

        self.clear_log()
        self.progress_var.set(0)

        confirm = messagebox.askyesno(
            "Confirm Organization",
            f"Are you sure you want to organize files in '{source_dir}'?\n"
            "This action will move files to new subfolders.\n"
            "It is recommended to make a backup before proceeding.",
            icon="warning",
        )

        if not confirm:
            self.add_log_message("Organization canceled by the user.", "warning")
            return

        try:
            # Disable button while organizing
            if hasattr(self, "organize_button"):
                self.organize_button.config(state=tk.DISABLED)

            files_moved, folders_created, log_details_str = (
                self.file_organizer.organize_files(
                    source_dir, progress_callback=self.update_progress
                )
            )

            self.add_log_message(log_details_str)

            # Determine the final message type based on results
            if files_moved > 0 or folders_created > 0:
                final_summary = (
                    f"Process completed.\n\n"
                    f"Files moved: {files_moved}\n"
                    f"Folders created: {folders_created}\n\n"
                    f"Check the log for more details."
                )
                messagebox.showinfo("Organization Complete", final_summary)
            elif (
                self.file_organizer.log_messages
                and "No files found to organize."
                in self.file_organizer.log_messages[-1]
            ):
                messagebox.showinfo(
                    "Organization",
                    "No files found in the specified directory.",
                )
            elif (
                self.file_organizer.log_messages
                and "Organization canceled" not in self.file_organizer.log_messages[-1]
            ):
                messagebox.showinfo(
                    "Organization Complete",
                    "No changes were made. Files might already be organized or there were no files to move.",
                )

        except Exception as e:
            error_msg = f"Critical error during organization: {str(e)}"
            self.add_log_message(error_msg, "error")
            messagebox.showerror("Critical Error", error_msg)
            logging.exception(error_msg)
        finally:
            self.progress_var.set(100)
            # Enable organize button if it was disabled
            if hasattr(self, "organize_button"):
                self.organize_button.config(state=tk.NORMAL)

    def open_settings(self):
        """Opens the category configuration window."""

        def on_settings_saved():
            self.add_log_message("Settings updated successfully.", "success")
            # Reload categories in the organizer
            self.file_organizer.settings_manager = self.settings_manager

        SettingsWindow(self.root, self.settings_manager, callback=on_settings_saved)

    def open_filters(self):
        """Opens the advanced filters window."""

        def on_filters_applied():
            total_files = len(
                self.file_organizer.get_files_to_organize(
                    self.source_dir_var.get() or os.path.expanduser("~")
                )
            )
            self.add_log_message(
                f"Filters applied. {total_files} files match criteria.", "info"
            )

        FilterWindow(
            self.root,
            self.file_organizer.file_filter,
            self.file_organizer,
            callback=on_filters_applied,
        )

    def preview_organization(self):
        """Shows a preview of the changes that would be made."""
        source_dir = self.source_dir_var.get()
        if not source_dir:
            messagebox.showwarning(
                "Directory Not Specified",
                "Please select a directory to preview.",
            )
            return

        if not os.path.isdir(source_dir):
            messagebox.showerror(
                "Invalid Directory",
                f"The path '{source_dir}' is not a valid directory.",
            )
            return

        # Generate preview
        preview_data = self.preview_manager.generate_preview(source_dir)

        if not preview_data:
            messagebox.showinfo(
                "Preview", "No files found to organize in the selected directory."
            )
            return

        def on_preview_decision(proceed):
            if proceed:
                self.start_organization_direct()

        PreviewWindow(self.root, preview_data, callback=on_preview_decision)

    def start_organization_direct(self):
        """Starts organization directly without additional confirmation."""
        source_dir = self.source_dir_var.get()

        self.clear_log()
        self.progress_var.set(0)

        try:
            # Disable button during organization
            if hasattr(self, "organize_button"):
                self.organize_button.config(state=tk.DISABLED)

            files_moved, folders_created, log_details_str = (
                self.file_organizer.organize_files(
                    source_dir, progress_callback=self.update_progress
                )
            )

            self.add_log_message(log_details_str)

            # Show final result
            if files_moved > 0 or folders_created > 0:
                final_summary = (
                    f"Organization completed successfully!\n\n"
                    f"Files moved: {files_moved}\n"
                    f"Folders created: {folders_created}\n\n"
                    f"You can undo this operation if needed."
                )
                messagebox.showinfo("Organization Complete", final_summary)
            else:
                messagebox.showinfo(
                    "Organization Complete",
                    "No changes were made. Files might already be organized.",
                )

        except Exception as e:
            error_msg = f"Critical error during organization: {str(e)}"
            self.add_log_message(error_msg, "error")
            messagebox.showerror("Critical Error", error_msg)
            logging.exception(error_msg)
        finally:
            self.progress_var.set(100)
            # Re-enable button
            if hasattr(self, "organize_button"):
                self.organize_button.config(state=tk.NORMAL)

    def open_undo_window(self):
        """Opens the undo operations management window."""
        UndoWindow(self.root, self.undo_manager)

    def show_file_statistics(self):
        """Shows statistics of files in the selected directory."""
        self.statistics_manager.show_file_statistics(
            self.source_dir_var.get(), self.root
        )


def main():
    """Main function to start the File Organizer application."""
    root = tk.Tk()
    app = FileOrganizerApp(root)

    # Center the window on the screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    # Add a welcome message to the log
    app.add_log_message("File Organizer started successfully!", "success")
    app.add_log_message("Select a directory to organize files by type.", "info")

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
