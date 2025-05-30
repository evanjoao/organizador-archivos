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


class App:
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

        self.setup_styles()
        self.setup_ui()
        self.load_initial_directories()
        self.root.bind("<Configure>", self.on_window_resize)

    def setup_styles(self):
        self.style = ttk.Style()

        # Try to set a base theme that allows more customization if possible
        # Common themes: 'clam', 'alt', 'default', 'classic'
        # 'clam' is usually good for customization
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            print("Theme 'clam' not available, using default theme.")

        # General style for all ttk widgets (if the theme allows)
        self.style.configure(
            ".",
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",  # Default text color
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        # Style for LabelFrame
        self.style.configure(
            "Custom.TLabelframe",
            background=UI_CONFIG["theme"]["background_color"],
            padding=UI_CONFIG["theme"]["padding"]["medium"],
        )
        self.style.configure(
            "Custom.TLabelframe.Label",  # Style for the label text of the LabelFrame
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
        )

        # Style for Buttons
        self.style.configure(
            "Custom.TButton",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
            relief="raised",  # Border style
            borderwidth=2,
        )
        self.style.map(
            "Custom.TButton",
            background=[
                ("active", UI_CONFIG["theme"]["secondary_color"]),
                ("pressed", UI_CONFIG["theme"]["secondary_color"]),
            ],
            relief=[("pressed", "sunken")],
        )

        # Style for Progress Bar
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=UI_CONFIG["theme"]["background_color"],  # Channel color
            background=UI_CONFIG["theme"]["primary_color"],  # Bar color
            thickness=20,
        )

        # Style for Treeview
        self.style.configure(
            "Custom.Treeview",
            background=UI_CONFIG["theme"][
                "background_color"
            ],  # General widget background
            fieldbackground=UI_CONFIG["theme"]["background_color"],  # Cell background
            foreground="black",  # Text color
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            rowheight=30,  # IMPROVEMENT: Increase row height
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"] + 1,
                "bold",
            ),  # Slightly larger and bold
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
            relief="raised",
        )
        self.style.map(
            "Custom.Treeview",
            background=[
                ("selected", UI_CONFIG["theme"]["primary_color"])
            ],  # IMPROVEMENT: Use config color
            foreground=[
                ("selected", UI_CONFIG["theme"]["text_color"])
            ],  # IMPROVEMENT: Use config color
        )
        # For Entry, there is no direct ttk style as flexible as in CTk, but we can use options
        # self.root.option_add("*TEntry*Font", (UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]))

    def setup_ui(self):
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
        # Configure rows for expansion, especially the log row
        main_frame.grid_rowconfigure(0, weight=0)  # title_label
        main_frame.grid_rowconfigure(
            1, weight=1
        )  # dir_selection_frame (contains the treeview that should expand)
        main_frame.grid_rowconfigure(2, weight=0)  # selected_dir_frame
        main_frame.grid_rowconfigure(3, weight=0)  # progress_frame
        main_frame.grid_rowconfigure(4, weight=0)  # organize_button
        main_frame.grid_rowconfigure(
            5, weight=2
        )  # log_frame (give it more weight to expand more)

        title_label = ttk.Label(
            main_frame,
            text="File Organizer",
            font=(
                UI_CONFIG["theme"]["font_family"],
                18,
                "bold",
            ),  # IMPROVEMENT: Larger font
            anchor="center",
            style="Custom.TLabelframe.Label",  # To take the correct background if needed
        )
        title_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["large"]),
        )

        dir_selection_frame = ttk.Frame(
            main_frame, style="Custom.TLabelframe"
        )  # Use the style for the background
        dir_selection_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )
        dir_selection_frame.grid_columnconfigure(0, weight=3)
        dir_selection_frame.grid_columnconfigure(1, weight=1)
        dir_selection_frame.grid_rowconfigure(
            0, weight=1
        )  # Allow the LabelFrame of the tree to expand

        dir_tree_frame = ttk.LabelFrame(
            dir_selection_frame,
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
        dir_tree_frame.grid_rowconfigure(
            0, weight=1
        )  # The tree_container will expand in this row
        dir_tree_frame.grid_columnconfigure(0, weight=1)

        # IMPROVEMENT: Top padding for tree_container to avoid overlap with the LabelFrame title
        tree_container = ttk.Frame(
            dir_tree_frame, style="Custom.TLabelframe"
        )  # To inherit background
        tree_container.grid(
            row=0, column=0, sticky="nsew", pady=(10, 0)
        )  # pady=(top_padding, bottom_padding)
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
        tree_scroll_x.grid(row=1, column=0, sticky="ew")  # Horizontal scrollbar below

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_rowconfigure(1, weight=0)  # For the X scrollbar
        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_columnconfigure(1, weight=0)  # For the Y scrollbar

        self.dir_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        controls_frame = ttk.Frame(
            dir_selection_frame, style="Custom.TLabelframe"
        )  # To inherit background
        controls_frame.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(UI_CONFIG["theme"]["padding"]["small"], 0),
        )  # sticky 'ns' to keep buttons at the top
        controls_frame.grid_columnconfigure(0, weight=1)

        refresh_button = ttk.Button(
            controls_frame,
            text="↻ Refresh",
            command=self.refresh_directories,
            style="Custom.TButton",
        )
        refresh_button.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )

        custom_dir_button = ttk.Button(
            controls_frame,
            text="+ Other Directory",
            command=self.browse_directory,
            style="Custom.TButton",
        )
        custom_dir_button.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )

        # Nuevo botón para configuración
        settings_button = ttk.Button(
            controls_frame,
            text="⚙ Settings",
            command=self.open_settings,
            style="Custom.TButton",
        )
        settings_button.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )

        # Nuevo botón para filtros
        filters_button = ttk.Button(
            controls_frame,
            text="🔍 Filters",
            command=self.open_filters,
            style="Custom.TButton",
        )
        filters_button.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["small"]),
        )

        # Nuevo botón para deshacer
        undo_button = ttk.Button(
            controls_frame,
            text="↶ Undo",
            command=self.open_undo_window,
            style="Custom.TButton",
        )
        undo_button.grid(row=4, column=0, sticky="ew")

        selected_dir_frame = ttk.LabelFrame(
            main_frame,
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
            ),  # Font for Entry
        )
        self.dir_entry.grid(
            row=0, column=0, sticky="ew", padx=5, pady=5
        )  # Internal padding in the LabelFrame

        progress_outer_frame = ttk.Frame(
            main_frame, style="Custom.TLabelframe"
        )  # Container for the label and the bar
        progress_outer_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )
        progress_outer_frame.grid_columnconfigure(0, weight=1)  # For the bar to expand

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

        # Botones de organización
        organize_buttons_frame = ttk.Frame(main_frame)
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

        organize_button = ttk.Button(
            organize_buttons_frame,
            text="🗂 Organize Files",
            command=self.start_organization,
            style="Custom.TButton",
        )
        organize_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # Guardar referencia al botón para poder deshabilitarlo
        self.organize_button = organize_button

        log_frame = ttk.LabelFrame(
            main_frame,
            text="Activity Log",
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            style="Custom.TLabelframe",
        )
        log_frame.grid(row=5, column=0, sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_container = ttk.Frame(
            log_frame, style="Custom.TLabelframe"
        )  # To inherit background
        log_container.grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5
        )  # Internal padding
        log_container.grid_rowconfigure(0, weight=1)
        log_container.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_container,
            wrap=tk.WORD,
            height=10,  # Initial height, will expand
            state=tk.DISABLED,
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            bg=UI_CONFIG["theme"]["background_color"],  # Text widget background
            fg="black",  # Default text color for the log
            padx=UI_CONFIG["theme"]["padding"]["small"],
            pady=UI_CONFIG["theme"]["padding"]["small"],
            relief=tk.SOLID,  # Border for the Text
            borderwidth=1,
        )
        log_scroll = ttk.Scrollbar(
            log_container, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll.grid(row=0, column=1, sticky="ns")

        # IMPROVEMENT: Configure colors for the log using UI_CONFIG
        self.log_text.tag_configure(
            "info", foreground=UI_CONFIG["theme"]["colors"].get("info_text", "black")
        )  # Use a specific color for info if it exists
        self.log_text.tag_configure(
            "error", foreground=UI_CONFIG["theme"]["colors"]["error"]
        )
        self.log_text.tag_configure(
            "success", foreground=UI_CONFIG["theme"]["colors"]["success"]
        )
        self.log_text.tag_configure(
            "warning", foreground=UI_CONFIG["theme"]["colors"]["warning"]
        )

    def on_window_resize(self, event=None):  # Allow calling without an event
        # Only adjust if the window already has a size (avoid errors at startup)
        if self.root.winfo_width() > 1 and self.dir_tree.winfo_width() > 1:
            tree_width = self.dir_tree.winfo_width()
            # Ensure columns are not too small
            col_0_width = int(tree_width * 0.4)
            col_1_width = int(tree_width * 0.6)

            if col_0_width < 100:
                col_0_width = 100  # Minimum for Name
            if col_1_width < 150:
                col_1_width = 150  # Minimum for Path

            self.dir_tree.column("#0", width=col_0_width)
            self.dir_tree.column("path", width=col_1_width)

    def load_initial_directories(self):
        common_dirs = {
            "Home": os.path.expanduser("~"),
            "Documents": os.path.expanduser("~/Documents"),
            "Downloads": os.path.expanduser("~/Downloads"),
            "Desktop": os.path.expanduser("~/Desktop"),
            "Pictures": os.path.expanduser("~/Pictures"),
            "Music": os.path.expanduser("~/Music"),
            "Videos": os.path.expanduser("~/Videos"),
            "System": {"Root": "/", "Mounts": "/mnt", "Users": "/home"},
        }

        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

        for name, path_or_dict in common_dirs.items():
            if isinstance(path_or_dict, dict):
                parent_id = self.dir_tree.insert(
                    "", "end", text=name, values=("",), open=False
                )  # Do not open by default
                for sub_name, sub_path in path_or_dict.items():
                    if os.path.exists(sub_path) and os.path.isdir(sub_path):
                        self.dir_tree.insert(
                            parent_id, "end", text=sub_name, values=(sub_path,)
                        )
            elif (
                isinstance(path_or_dict, str)
                and os.path.exists(path_or_dict)
                and os.path.isdir(path_or_dict)
            ):
                self.dir_tree.insert("", "end", text=name, values=(path_or_dict,))

        # Call on_window_resize once after loading to adjust columns
        self.root.after(100, self.on_window_resize)

    def add_directory_to_tree(self, dir_path, parent=""):
        try:
            dir_name = os.path.basename(dir_path) or dir_path
            # Avoid duplicates if it already exists with the same path
            for item_id in self.dir_tree.get_children(parent):
                if (
                    self.dir_tree.item(item_id, "values")
                    and self.dir_tree.item(item_id, "values")[0] == dir_path
                ):
                    self.dir_tree.selection_set(item_id)  # Select the existing one
                    self.dir_tree.focus(item_id)
                    return

            item = self.dir_tree.insert(
                parent, "end", text=dir_name, values=(dir_path,), open=True
            )
            self.dir_tree.selection_set(item)
            self.dir_tree.focus(item)

            # Optional: Load one level of subdirectories (can be slow for large directories)
            # for sub_item in os.listdir(dir_path):
            #     sub_item_path = os.path.join(dir_path, sub_item)
            #     if os.path.isdir(sub_item_path) and not sub_item.startswith("."):
            #         self.dir_tree.insert(item, "end", text=sub_item, values=(sub_item_path,))

        except Exception as e:
            logging.error(f"Error adding directory to tree: {dir_path}, {e}")
            self.add_log_message(f"Error accessing {dir_path}: {e}", "error")

    def refresh_directories(self):
        self.load_initial_directories()
        self.add_log_message("Directory list updated.", "info")

    def browse_directory(self):
        directory = filedialog.askdirectory(
            initialdir=self.source_dir_var.get() or os.path.expanduser("~")
        )
        if directory:
            self.source_dir_var.set(directory)
            self.add_directory_to_tree(directory)  # Add it to the tree
            self.add_log_message(
                f"Directory selected for organization: {directory}", "success"
            )

    def on_tree_select(self, event):
        selected_items = self.dir_tree.selection()
        if selected_items:
            item = selected_items[0]
            # Ensure 'values' is not empty and has at least one element
            item_values = self.dir_tree.item(item, "values")
            if item_values and item_values[0]:
                dir_path = item_values[0]
                self.source_dir_var.set(dir_path)
                # No need for a log here, it's too verbose. Log is more useful for actions.
            # else:
            # It's a parent category without a path, do nothing or clear the entry.
            # self.source_dir_var.set("")

    def add_log_message(self, message, message_type="info"):
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
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()  # Force UI update

    def start_organization(self):
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
        # The initial organization message is already added in FileOrganizer

        confirm = messagebox.askyesno(
            "Confirm Organization",
            f"Are you sure you want to organize files in '{source_dir}'?\n"
            "This action will move files to new subfolders.\n"
            "It is recommended to make a backup before proceeding.",
            icon="warning",  # Icon for the messagebox
        )

        if not confirm:
            self.add_log_message("Organization canceled by the user.", "warning")
            return

        try:
            # Disable button while organizing to avoid multiple clicks
            # This would require saving a reference to the button: self.organize_button.config(state=tk.DISABLED)
            # And then enabling it in a finally block: self.organize_button.config(state=tk.NORMAL)

            files_moved, folders_created, log_details_str = (
                self.file_organizer.organize_files(
                    source_dir, progress_callback=self.update_progress
                )
            )

            # log_details_str is already a string with line breaks
            self.add_log_message(
                log_details_str
            )  # Tags will be applied based on content if FileOrganizer is improved

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
            logging.exception(error_msg)  # Use logging.exception to include traceback
        finally:
            self.progress_var.set(100)  # Ensure the bar reaches the end
            # Enable organize button if it was disabled

    def open_settings(self):
        """Opens the category configuration window."""

        def on_settings_saved():
            self.add_log_message("Settings updated successfully.", "success")
            # Recargar las categorías en el organizador
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

        # Generar previsualización
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
            # Deshabilitar botón durante la organización
            if hasattr(self, "organize_button"):
                self.organize_button.config(state=tk.DISABLED)

            files_moved, folders_created, log_details_str = (
                self.file_organizer.organize_files(
                    source_dir, progress_callback=self.update_progress
                )
            )

            self.add_log_message(log_details_str)

            # Mostrar resultado final
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
            # Rehabilitar botón
            if hasattr(self, "organize_button"):
                self.organize_button.config(state=tk.NORMAL)

    def open_undo_window(self):
        """Opens the undo operations management window."""
        UndoWindow(self.root, self.undo_manager)

    def show_file_statistics(self):
        """Shows statistics of files in the selected directory."""
        source_dir = self.source_dir_var.get()
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

            # Agrupar por categorías
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

            # Crear ventana de estadísticas
            stats_window = tk.Toplevel(self.root)
            stats_window.title("File Statistics")
            stats_window.geometry("400x500")
            stats_window.transient(self.root)
            stats_window.grab_set()

            main_frame = ttk.Frame(stats_window, padding="10")
            main_frame.pack(fill="both", expand=True)

            ttk.Label(
                main_frame, text="File Statistics", font=("Arial", 14, "bold")
            ).pack(anchor="w", pady=(0, 10))

            ttk.Label(main_frame, text=f"Total files: {len(files)}").pack(anchor="w")
            ttk.Label(
                main_frame, text=f"Total size: {self.format_file_size(total_size)}"
            ).pack(anchor="w")
            ttk.Label(main_frame, text=f"Categories: {len(categories)}").pack(
                anchor="w", pady=(0, 10)
            )

            # Treeview para categorías
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(fill="both", expand=True, pady=(0, 10))

            tree = ttk.Treeview(
                tree_frame, columns=("count", "size"), show="tree headings"
            )
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
                    values=(data["count"], self.format_file_size(data["size"])),
                )

            tree.pack(fill="both", expand=True)

            ttk.Button(main_frame, text="Close", command=stats_window.destroy).pack(
                pady=(10, 0)
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error calculating statistics: {e}")

    def format_file_size(self, size_bytes):
        """Formats the file size in a readable way."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/1024**2:.1f} MB"
        else:
            return f"{size_bytes/1024**3:.1f} GB"


def main():
    """Main function to start the File Organizer application."""
    root = tk.Tk()
    app = App(root)

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
