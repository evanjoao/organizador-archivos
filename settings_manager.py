# -*- coding: utf-8 -*-
"""
Sistema de configuración personalizable para el organizador de archivos.
Permite a los usuarios crear, editar y gestionar sus propias categorías de archivos.
"""

import json
import os
import logging
from typing import Dict, List, Any
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class SettingsManager:
    """Gestor de configuraciones personalizable para categorías de archivos."""

    def __init__(self, config_file: str = "user_config.json"):
        self.config_file = config_file
        self.default_categories = {
            "Imágenes": [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".tiff",
                ".svg",
                ".webp",
                ".ico",
            ],
            "Documentos": [
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
            "Videos": [
                ".mp4",
                ".mov",
                ".avi",
                ".mkv",
                ".wmv",
                ".flv",
                ".webm",
                ".m4v",
                ".3gp",
            ],
            "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a", ".wma"],
            "Archivos Comprimidos": [
                ".zip",
                ".rar",
                ".tar",
                ".gz",
                ".7z",
                ".bz2",
                ".xz",
            ],
            "Ejecutables e Instaladores": [
                ".exe",
                ".msi",
                ".dmg",
                ".pkg",
                ".deb",
                ".rpm",
                ".appimage",
            ],
            "Scripts y Código": [
                ".py",
                ".js",
                ".html",
                ".css",
                ".java",
                ".c",
                ".cpp",
                ".cs",
                ".php",
                ".rb",
                ".go",
                ".rs",
            ],
            "Hojas de Cálculo": [".csv", ".tsv", ".xlsx", ".xls", ".ods"],
            "Presentaciones": [".ppt", ".pptx", ".odp", ".key"],
            "Libros Electrónicos": [".epub", ".mobi", ".azw", ".azw3", ".fb2"],
            "Fuentes": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
            "Otros": [],
        }
        self.user_categories = self.load_config()

    def load_config(self) -> Dict[str, List[str]]:
        """Carga la configuración desde el archivo JSON."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    # Validar que la configuración tenga el formato correcto
                    if isinstance(config, dict) and "categories" in config:
                        return config["categories"]
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logging.warning(f"Error loading config file: {e}. Using defaults.")

        # Si no existe el archivo o hay error, usar las categorías por defecto
        return self.default_categories.copy()

    def save_config(self) -> bool:
        """Guarda la configuración actual en el archivo JSON."""
        try:
            config = {
                "categories": self.user_categories,
                "version": "1.0",
                "last_modified": str(tk.datetime.datetime.now()),
            }
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            return False

    def get_categories(self) -> Dict[str, List[str]]:
        """Devuelve las categorías actuales."""
        return self.user_categories

    def add_category(self, name: str, extensions: List[str]) -> bool:
        """Añade una nueva categoría."""
        if not name or not extensions:
            return False

        # Asegurar que las extensiones empiecen con punto
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        extensions = [ext.lower() for ext in extensions]  # Convertir a minúsculas

        self.user_categories[name] = extensions
        return self.save_config()

    def remove_category(self, name: str) -> bool:
        """Elimina una categoría."""
        if name in self.user_categories and name != "Otros":
            del self.user_categories[name]
            return self.save_config()
        return False

    def edit_category(
        self, old_name: str, new_name: str, extensions: List[str]
    ) -> bool:
        """Edita una categoría existente."""
        if old_name not in self.user_categories:
            return False

        # Asegurar que las extensiones empiecen con punto
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        extensions = [ext.lower() for ext in extensions]

        # Si el nombre cambió, eliminar la entrada antigua
        if old_name != new_name:
            del self.user_categories[old_name]

        self.user_categories[new_name] = extensions
        return self.save_config()

    def reset_to_defaults(self) -> bool:
        """Resetea las categorías a los valores por defecto."""
        self.user_categories = self.default_categories.copy()
        return self.save_config()


class SettingsWindow:
    """Ventana de configuración para gestionar categorías."""

    def __init__(self, parent, settings_manager: SettingsManager, callback=None):
        self.parent = parent
        self.settings_manager = settings_manager
        self.callback = callback
        self.window = None
        self.tree = None
        self.create_window()

    def create_window(self):
        """Crea la ventana de configuración."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Configuración de Categorías")
        self.window.geometry("600x500")
        self.window.transient(self.parent)
        self.window.grab_set()

        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Gestión de Categorías de Archivos",
            font=("Arial", 14, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Treeview para mostrar categorías
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame, columns=("extensions",), show="tree headings"
        )
        self.tree.heading("#0", text="Categoría")
        self.tree.heading("extensions", text="Extensiones")
        self.tree.column("#0", width=200)
        self.tree.column("extensions", width=350)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(
            buttons_frame, text="Añadir Categoría", command=self.add_category
        ).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(buttons_frame, text="Editar", command=self.edit_category).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(buttons_frame, text="Eliminar", command=self.remove_category).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(buttons_frame, text="Restablecer", command=self.reset_defaults).grid(
            row=0, column=3, padx=5
        )

        # Botones de cierre
        close_frame = ttk.Frame(main_frame)
        close_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(
            close_frame, text="Guardar y Cerrar", command=self.save_and_close
        ).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(close_frame, text="Cancelar", command=self.cancel).grid(
            row=0, column=1, padx=5
        )

        self.refresh_tree()

    def refresh_tree(self):
        """Actualiza el tree con las categorías actuales."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        categories = self.settings_manager.get_categories()
        for name, extensions in categories.items():
            ext_str = ", ".join(extensions) if extensions else "Sin extensiones"
            self.tree.insert("", "end", text=name, values=(ext_str,))

    def add_category(self):
        """Añade una nueva categoría."""
        dialog = CategoryDialog(self.window, "Añadir Categoría")
        if dialog.result:
            name, extensions = dialog.result
            if self.settings_manager.add_category(name, extensions):
                self.refresh_tree()
            else:
                messagebox.showerror("Error", "No se pudo añadir la categoría")

    def edit_category(self):
        """Edita la categoría seleccionada."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                "Advertencia", "Selecciona una categoría para editar"
            )
            return

        item = selection[0]
        old_name = self.tree.item(item, "text")

        categories = self.settings_manager.get_categories()
        old_extensions = categories.get(old_name, [])

        dialog = CategoryDialog(
            self.window, "Editar Categoría", old_name, old_extensions
        )
        if dialog.result:
            new_name, new_extensions = dialog.result
            if self.settings_manager.edit_category(old_name, new_name, new_extensions):
                self.refresh_tree()
            else:
                messagebox.showerror("Error", "No se pudo editar la categoría")

    def remove_category(self):
        """Elimina la categoría seleccionada."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                "Advertencia", "Selecciona una categoría para eliminar"
            )
            return

        item = selection[0]
        name = self.tree.item(item, "text")

        if name == "Otros":
            messagebox.showwarning(
                "Advertencia", "No se puede eliminar la categoría 'Otros'"
            )
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar la categoría '{name}'?"):
            if self.settings_manager.remove_category(name):
                self.refresh_tree()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")

    def reset_defaults(self):
        """Restablece las categorías por defecto."""
        if messagebox.askyesno(
            "Confirmar", "¿Restablecer todas las categorías a los valores por defecto?"
        ):
            if self.settings_manager.reset_to_defaults():
                self.refresh_tree()
            else:
                messagebox.showerror("Error", "No se pudo restablecer las categorías")

    def save_and_close(self):
        """Guarda y cierra la ventana."""
        if self.settings_manager.save_config():
            if self.callback:
                self.callback()  # Notificar al padre que se han guardado cambios
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración")

    def cancel(self):
        """Cancela y cierra la ventana."""
        self.window.destroy()


class CategoryDialog:
    """Diálogo para añadir/editar categorías."""

    def __init__(self, parent, title, name="", extensions=None):
        self.parent = parent
        self.result = None
        self.create_dialog(title, name, extensions or [])

    def create_dialog(self, title, name, extensions):
        """Crea el diálogo."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Nombre de la categoría
        ttk.Label(main_frame, text="Nombre de la categoría:").pack(anchor="w")
        self.name_var = tk.StringVar(value=name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.pack(fill="x", pady=(5, 10))

        # Extensiones
        ttk.Label(main_frame, text="Extensiones (separadas por comas):").pack(
            anchor="w"
        )
        ttk.Label(
            main_frame,
            text="Ejemplo: .pdf, .doc, .txt",
            font=("Arial", 8),
            foreground="gray",
        ).pack(anchor="w")

        self.ext_text = tk.Text(main_frame, height=8, width=40)
        self.ext_text.pack(fill="both", expand=True, pady=(5, 10))

        if extensions:
            self.ext_text.insert("1.0", ", ".join(extensions))

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Aceptar", command=self.accept).pack(
            side="right", padx=(5, 0)
        )
        ttk.Button(button_frame, text="Cancelar", command=self.cancel).pack(
            side="right"
        )

        name_entry.focus()

    def accept(self):
        """Acepta el diálogo."""
        name = self.name_var.get().strip()
        ext_text = self.ext_text.get("1.0", "end-1c").strip()

        if not name:
            messagebox.showerror(
                "Error", "El nombre de la categoría no puede estar vacío"
            )
            return

        # Procesar extensiones
        extensions = []
        if ext_text:
            extensions = [ext.strip() for ext in ext_text.split(",")]
            extensions = [ext for ext in extensions if ext]  # Eliminar vacíos

        self.result = (name, extensions)
        self.dialog.destroy()

    def cancel(self):
        """Cancela el diálogo."""
        self.dialog.destroy()
