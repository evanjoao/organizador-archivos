# -*- coding: utf-8 -*-
"""
Advanced filtering and search system for the file organizer.
Allows filtering files by type, size, date, name and other criteria.
"""

import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable
import tkinter as tk
from tkinter import ttk


class FileFilter:
    """File filtering system."""

    def __init__(self):
        self.active_filters = {}

    def add_filter(self, name: str, filter_func: Callable, params: Dict = None):
        """Añade un filtro."""
        self.active_filters[name] = {
            "function": filter_func,
            "params": params or {},
            "enabled": True,
        }

    def remove_filter(self, name: str):
        """Elimina un filtro."""
        if name in self.active_filters:
            del self.active_filters[name]

    def enable_filter(self, name: str, enabled: bool = True):
        """Habilita o deshabilita un filtro."""
        if name in self.active_filters:
            self.active_filters[name]["enabled"] = enabled

    def apply_filters(self, file_list: List[str], source_directory: str) -> List[str]:
        """Aplica todos los filtros activos a la lista de archivos."""
        filtered_files = file_list.copy()

        for filter_name, filter_data in self.active_filters.items():
            if filter_data["enabled"]:
                filter_func = filter_data["function"]
                params = filter_data["params"]
                filtered_files = [
                    f
                    for f in filtered_files
                    if filter_func(f, source_directory, **params)
                ]

        return filtered_files

    def clear_filters(self):
        """Limpia todos los filtros."""
        self.active_filters.clear()


# Predefined filter functions
def filter_by_extension(filename: str, source_dir: str, extensions: List[str]) -> bool:
    """Filters by file extensions."""
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in [ext.lower() for ext in extensions]


def filter_by_size(
    filename: str, source_dir: str, min_size: int = 0, max_size: int = None
) -> bool:
    """Filters by file size in bytes."""
    file_path = os.path.join(source_dir, filename)
    try:
        file_size = os.path.getsize(file_path)
        if file_size < min_size:
            return False
        if max_size is not None and file_size > max_size:
            return False
        return True
    except OSError:
        return False


def filter_by_date(
    filename: str,
    source_dir: str,
    date_from: datetime = None,
    date_to: datetime = None,
    date_type: str = "modified",
) -> bool:
    """Filters by date (modification, creation or access)."""
    file_path = os.path.join(source_dir, filename)
    try:
        if date_type == "modified":
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        elif date_type == "created":
            file_date = datetime.fromtimestamp(os.path.getctime(file_path))
        elif date_type == "accessed":
            file_date = datetime.fromtimestamp(os.path.getatime(file_path))
        else:
            return False

        if date_from and file_date < date_from:
            return False
        if date_to and file_date > date_to:
            return False
        return True
    except OSError:
        return False


def filter_by_name_pattern(
    filename: str,
    source_dir: str,
    pattern: str,
    regex: bool = False,
    case_sensitive: bool = False,
) -> bool:
    """Filters by name pattern."""
    name = filename if case_sensitive else filename.lower()
    search_pattern = pattern if case_sensitive else pattern.lower()

    if regex:
        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            return bool(re.search(search_pattern, name, flags))
        except re.error:
            return False
    else:
        return search_pattern in name


def filter_exclude_hidden(filename: str, source_dir: str) -> bool:
    """Excluye archivos ocultos (que empiezan con punto)."""
    return not filename.startswith(".")


def filter_by_category(
    filename: str, source_dir: str, file_organizer, categories: List[str]
) -> bool:
    """Filters by file category."""
    file_ext = os.path.splitext(filename)[1].lower()
    file_category = file_organizer.get_category_for_extension(file_ext)
    return file_category in categories


class FilterWindow:
    """Ventana de configuración de filtros avanzados."""

    def __init__(
        self, parent, file_filter: FileFilter, file_organizer=None, callback=None
    ):
        self.parent = parent
        self.file_filter = file_filter
        self.file_organizer = file_organizer
        self.callback = callback
        self.window = None
        self.filter_vars = {}
        self.create_window()

    def create_window(self):
        """Crea la ventana de filtros."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Filtros Avanzados")
        self.window.geometry("500x700")
        self.window.transient(self.parent)
        self.window.grab_set()

        # Main frame with scroll
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main_frame, text="Configure Filters", font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 15))

        # Filter by extensions
        self.create_extension_filter(main_frame)

        # Filter by size
        self.create_size_filter(main_frame)

        # Filter by date
        self.create_date_filter(main_frame)

        # Filter by name
        self.create_name_filter(main_frame)

        # Filter by categories
        if self.file_organizer:
            self.create_category_filter(main_frame)

        # Miscellaneous filters
        self.create_misc_filters(main_frame)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))

        ttk.Button(button_frame, text="Apply Filters", command=self.apply_filters).pack(
            side="right", padx=(5, 0)
        )
        ttk.Button(button_frame, text="Clear All", command=self.clear_filters).pack(
            side="right"
        )
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(
            side="right", padx=(0, 5)
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_extension_filter(self, parent):
        """Crea el filtro por extensiones."""
        frame = ttk.LabelFrame(parent, text="Filtrar por Extensiones", padding="10")
        frame.pack(fill="x", pady=(0, 10))

        self.filter_vars["ext_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Activar filtro por extensiones",
            variable=self.filter_vars["ext_enabled"],
        ).pack(anchor="w")

        ttk.Label(frame, text="Extensiones (separadas por comas):").pack(
            anchor="w", pady=(10, 5)
        )
        self.filter_vars["extensions"] = tk.StringVar()
        ttk.Entry(frame, textvariable=self.filter_vars["extensions"], width=50).pack(
            fill="x"
        )

        ttk.Label(
            frame,
            text="Ejemplo: .pdf, .jpg, .txt",
            font=("Arial", 8),
            foreground="gray",
        ).pack(anchor="w")

    def create_size_filter(self, parent):
        """Crea el filtro por tamaño."""
        frame = ttk.LabelFrame(parent, text="Filtrar por Tamaño", padding="10")
        frame.pack(fill="x", pady=(0, 10))

        self.filter_vars["size_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Activar filtro por tamaño",
            variable=self.filter_vars["size_enabled"],
        ).pack(anchor="w")

        size_frame = ttk.Frame(frame)
        size_frame.pack(fill="x", pady=(10, 0))

        # Minimum size
        ttk.Label(size_frame, text="Minimum size:").grid(row=0, column=0, sticky="w")
        self.filter_vars["min_size"] = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.filter_vars["min_size"], width=15).grid(
            row=0, column=1, padx=(5, 0)
        )

        self.filter_vars["min_size_unit"] = tk.StringVar(value="KB")
        ttk.Combobox(
            size_frame,
            textvariable=self.filter_vars["min_size_unit"],
            values=["B", "KB", "MB", "GB"],
            width=5,
            state="readonly",
        ).grid(row=0, column=2, padx=(5, 0))

        # Maximum size
        ttk.Label(size_frame, text="Maximum size:").grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        self.filter_vars["max_size"] = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.filter_vars["max_size"], width=15).grid(
            row=1, column=1, padx=(5, 0), pady=(5, 0)
        )

        self.filter_vars["max_size_unit"] = tk.StringVar(value="MB")
        ttk.Combobox(
            size_frame,
            textvariable=self.filter_vars["max_size_unit"],
            values=["B", "KB", "MB", "GB"],
            width=5,
            state="readonly",
        ).grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

    def create_date_filter(self, parent):
        """Crea el filtro por fecha."""
        frame = ttk.LabelFrame(parent, text="Filtrar por Fecha", padding="10")
        frame.pack(fill="x", pady=(0, 10))

        self.filter_vars["date_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Activar filtro por fecha",
            variable=self.filter_vars["date_enabled"],
        ).pack(anchor="w")

        # Date type
        type_frame = ttk.Frame(frame)
        type_frame.pack(fill="x", pady=(10, 5))

        ttk.Label(type_frame, text="Date type:").pack(side="left")
        self.filter_vars["date_type"] = tk.StringVar(value="modified")
        ttk.Combobox(
            type_frame,
            textvariable=self.filter_vars["date_type"],
            values=["modified", "created", "accessed"],
            state="readonly",
            width=15,
        ).pack(side="left", padx=(10, 0))

        # Date range
        date_frame = ttk.Frame(frame)
        date_frame.pack(fill="x")

        ttk.Label(date_frame, text="From:").grid(row=0, column=0, sticky="w")
        self.filter_vars["date_from"] = tk.StringVar()
        ttk.Entry(
            date_frame, textvariable=self.filter_vars["date_from"], width=20
        ).grid(row=0, column=1, padx=(5, 0))

        ttk.Label(date_frame, text="To:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.filter_vars["date_to"] = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.filter_vars["date_to"], width=20).grid(
            row=1, column=1, padx=(5, 0), pady=(5, 0)
        )

        ttk.Label(
            frame, text="Formato: YYYY-MM-DD", font=("Arial", 8), foreground="gray"
        ).pack(anchor="w")

    def create_name_filter(self, parent):
        """Crea el filtro por nombre."""
        frame = ttk.LabelFrame(parent, text="Filtrar por Nombre", padding="10")
        frame.pack(fill="x", pady=(0, 10))

        self.filter_vars["name_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Activar filtro por nombre",
            variable=self.filter_vars["name_enabled"],
        ).pack(anchor="w")

        ttk.Label(frame, text="Patrón de búsqueda:").pack(anchor="w", pady=(10, 5))
        self.filter_vars["name_pattern"] = tk.StringVar()
        ttk.Entry(frame, textvariable=self.filter_vars["name_pattern"], width=50).pack(
            fill="x"
        )

        options_frame = ttk.Frame(frame)
        options_frame.pack(fill="x", pady=(10, 0))

        self.filter_vars["name_regex"] = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Usar expresiones regulares",
            variable=self.filter_vars["name_regex"],
        ).pack(side="left")

        self.filter_vars["name_case_sensitive"] = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Distinguir mayúsculas",
            variable=self.filter_vars["name_case_sensitive"],
        ).pack(side="left", padx=(20, 0))

    def create_category_filter(self, parent):
        """Crea el filtro por categorías."""
        frame = ttk.LabelFrame(parent, text="Filtrar por Categorías", padding="10")
        frame.pack(fill="x", pady=(0, 10))

        self.filter_vars["category_enabled"] = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Activar filtro por categorías",
            variable=self.filter_vars["category_enabled"],
        ).pack(anchor="w")

        # Lista de categorías con checkboxes
        categories_frame = ttk.Frame(frame)
        categories_frame.pack(fill="x", pady=(10, 0))

        from config import FILE_TYPES

        self.category_vars = {}

        row = 0
        col = 0
        for category in FILE_TYPES.keys():
            self.category_vars[category] = tk.BooleanVar()
            ttk.Checkbutton(
                categories_frame, text=category, variable=self.category_vars[category]
            ).grid(row=row, column=col, sticky="w", padx=(0, 20))

            col += 1
            if col > 2:  # 3 columnas
                col = 0
                row += 1

    def create_misc_filters(self, parent):
        """Crea filtros varios."""
        frame = ttk.LabelFrame(parent, text="Filtros Adicionales", padding="10")
        frame.pack(fill="x", pady=(0, 10))

        self.filter_vars["exclude_hidden"] = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame,
            text="Excluir archivos ocultos",
            variable=self.filter_vars["exclude_hidden"],
        ).pack(anchor="w")

    def convert_size_to_bytes(self, size_str: str, unit: str) -> int:
        """Convierte tamaño con unidad a bytes."""
        try:
            size = float(size_str)
            multipliers = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
            return int(size * multipliers.get(unit, 1))
        except (ValueError, TypeError):
            return 0

    def parse_date(self, date_str: str) -> datetime:
        """Parsea una fecha en formato YYYY-MM-DD."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

    def apply_filters(self):
        """Aplica los filtros configurados."""
        self.file_filter.clear_filters()

        # Filtro por extensiones
        if self.filter_vars["ext_enabled"].get():
            ext_text = self.filter_vars["extensions"].get().strip()
            if ext_text:
                extensions = [ext.strip() for ext in ext_text.split(",")]
                extensions = [
                    ext if ext.startswith(".") else f".{ext}" for ext in extensions
                ]
                self.file_filter.add_filter(
                    "extensions", filter_by_extension, {"extensions": extensions}
                )

        # Filtro por tamaño
        if self.filter_vars["size_enabled"].get():
            min_size_str = self.filter_vars["min_size"].get().strip()
            max_size_str = self.filter_vars["max_size"].get().strip()

            params = {}
            if min_size_str:
                params["min_size"] = self.convert_size_to_bytes(
                    min_size_str, self.filter_vars["min_size_unit"].get()
                )
            if max_size_str:
                params["max_size"] = self.convert_size_to_bytes(
                    max_size_str, self.filter_vars["max_size_unit"].get()
                )

            if params:
                self.file_filter.add_filter("size", filter_by_size, params)

        # Filtro por fecha
        if self.filter_vars["date_enabled"].get():
            date_from_str = self.filter_vars["date_from"].get().strip()
            date_to_str = self.filter_vars["date_to"].get().strip()

            params = {"date_type": self.filter_vars["date_type"].get()}

            if date_from_str:
                date_from = self.parse_date(date_from_str)
                if date_from:
                    params["date_from"] = date_from

            if date_to_str:
                date_to = self.parse_date(date_to_str)
                if date_to:
                    params["date_to"] = date_to

            if len(params) > 1:  # Más que solo date_type
                self.file_filter.add_filter("date", filter_by_date, params)

        # Filtro por nombre
        if self.filter_vars["name_enabled"].get():
            pattern = self.filter_vars["name_pattern"].get().strip()
            if pattern:
                params = {
                    "pattern": pattern,
                    "regex": self.filter_vars["name_regex"].get(),
                    "case_sensitive": self.filter_vars["name_case_sensitive"].get(),
                }
                self.file_filter.add_filter("name", filter_by_name_pattern, params)

        # Filtro por categorías
        if (
            hasattr(self, "category_vars")
            and self.filter_vars["category_enabled"].get()
        ):
            selected_categories = [
                cat for cat, var in self.category_vars.items() if var.get()
            ]
            if selected_categories:
                self.file_filter.add_filter(
                    "categories",
                    filter_by_category,
                    {
                        "file_organizer": self.file_organizer,
                        "categories": selected_categories,
                    },
                )

        # Filtros varios
        if self.filter_vars["exclude_hidden"].get():
            self.file_filter.add_filter("exclude_hidden", filter_exclude_hidden)

        if self.callback:
            self.callback()

        self.window.destroy()

    def clear_filters(self):
        """Limpia todos los filtros."""
        self.file_filter.clear_filters()
        if self.callback:
            self.callback()
        self.window.destroy()

    def cancel(self):
        """Cancela sin aplicar cambios."""
        self.window.destroy()
