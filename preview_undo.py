# -*- coding: utf-8 -*-
"""
Sistema de previsualización y deshacer para el organizador de archivos.
Permite ver qué archivos se moverán antes de ejecutar la organización
y deshacer cambios si es necesario.
"""

import os
import json
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, messagebox


class PreviewManager:
    """Gestor de previsualización de cambios."""

    def __init__(self, file_organizer):
        self.file_organizer = file_organizer
        self.preview_data = []

    def generate_preview(self, source_directory: str) -> List[Dict]:
        """Genera una previsualización de los cambios que se realizarían."""
        if not os.path.isdir(source_directory):
            return []

        self.preview_data = []

        try:
            files = [
                f
                for f in os.listdir(source_directory)
                if os.path.isfile(os.path.join(source_directory, f))
            ]

            for file_name in files:
                file_path = os.path.join(source_directory, file_name)
                file_extension = self.file_organizer.get_file_extension(file_name)
                category = self.file_organizer.get_category_for_extension(
                    file_extension
                )

                destination_folder = os.path.join(source_directory, category)
                destination_path = os.path.join(destination_folder, file_name)

                # Verificar si ya existe el archivo
                file_exists = os.path.exists(destination_path)
                final_name = file_name

                if file_exists:
                    base_name, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(
                        os.path.join(destination_folder, f"{base_name}_{counter}{ext}")
                    ):
                        counter += 1
                    final_name = f"{base_name}_{counter}{ext}"

                file_size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                preview_item = {
                    "original_name": file_name,
                    "final_name": final_name,
                    "category": category,
                    "source_path": file_path,
                    "destination_folder": destination_folder,
                    "destination_path": os.path.join(destination_folder, final_name),
                    "file_size": file_size,
                    "modified_time": mod_time,
                    "extension": file_extension,
                    "will_rename": file_exists,
                    "action": "move",
                }

                self.preview_data.append(preview_item)

        except Exception as e:
            logging.error(f"Error generating preview: {e}")

        return self.preview_data


class UndoManager:
    """Gestor de deshacer operaciones."""

    def __init__(self, backup_dir: str = "file_organizer_backups"):
        self.backup_dir = backup_dir
        self.operations_file = os.path.join(backup_dir, "operations.json")
        self.ensure_backup_dir()

    def ensure_backup_dir(self):
        """Asegura que existe el directorio de backups."""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def save_operation(self, operation_data: Dict) -> str:
        """Guarda información de una operación para poder deshacerla."""
        operation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        operation_data["id"] = operation_id
        operation_data["timestamp"] = datetime.now().isoformat()

        # Cargar operaciones existentes
        operations = self.load_operations()
        operations.append(operation_data)

        # Mantener solo las últimas 10 operaciones
        operations = operations[-10:]

        try:
            with open(self.operations_file, "w", encoding="utf-8") as f:
                json.dump(operations, f, indent=2, ensure_ascii=False, default=str)
            return operation_id
        except Exception as e:
            logging.error(f"Error saving operation: {e}")
            return ""

    def load_operations(self) -> List[Dict]:
        """Carga las operaciones guardadas."""
        if not os.path.exists(self.operations_file):
            return []

        try:
            with open(self.operations_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading operations: {e}")
            return []

    def undo_operation(self, operation_id: str) -> bool:
        """Deshace una operación específica."""
        operations = self.load_operations()
        operation = next((op for op in operations if op["id"] == operation_id), None)

        if not operation:
            return False

        try:
            # Deshacer los movimientos de archivos
            for move in operation.get("moves", []):
                source = move["destination_path"]
                destination = move["source_path"]

                if os.path.exists(source):
                    shutil.move(source, destination)
                    logging.info(f"Undid move: {source} -> {destination}")

            # Eliminar carpetas vacías creadas
            for folder in operation.get("folders_created", []):
                if os.path.exists(folder) and not os.listdir(folder):
                    os.rmdir(folder)
                    logging.info(f"Removed empty folder: {folder}")

            # Marcar operación como deshecha
            operation["undone"] = True
            operation["undo_timestamp"] = datetime.now().isoformat()

            # Guardar operaciones actualizadas
            with open(self.operations_file, "w", encoding="utf-8") as f:
                json.dump(operations, f, indent=2, ensure_ascii=False, default=str)

            return True

        except Exception as e:
            logging.error(f"Error undoing operation {operation_id}: {e}")
            return False


class PreviewWindow:
    """Ventana de previsualización de cambios."""

    def __init__(self, parent, preview_data: List[Dict], callback=None):
        self.parent = parent
        self.preview_data = preview_data
        self.callback = callback
        self.window = None
        self.tree = None
        self.create_window()

    def create_window(self):
        """Crea la ventana de previsualización."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Previsualización de Organización")
        self.window.geometry("800x600")
        self.window.transient(self.parent)
        self.window.grab_set()

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Título y estadísticas
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            title_frame, text="Previsualización de Cambios", font=("Arial", 14, "bold")
        ).pack(anchor="w")

        stats_text = f"Se moverán {len(self.preview_data)} archivos"
        categories = set(item["category"] for item in self.preview_data)
        stats_text += f" a {len(categories)} categorías"

        ttk.Label(title_frame, text=stats_text, font=("Arial", 10)).pack(anchor="w")

        # Treeview para mostrar la previsualización
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("category", "final_name", "size", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")

        self.tree.heading("#0", text="Archivo Original")
        self.tree.heading("category", text="Categoría")
        self.tree.heading("final_name", text="Nombre Final")
        self.tree.heading("size", text="Tamaño")
        self.tree.heading("status", text="Estado")

        self.tree.column("#0", width=200)
        self.tree.column("category", width=150)
        self.tree.column("final_name", width=200)
        self.tree.column("size", width=80)
        self.tree.column("status", width=100)

        scrollbar_v = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        scrollbar_h = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Llenar el tree con datos
        self.populate_tree()

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")

        ttk.Button(
            button_frame, text="Continuar con Organización", command=self.proceed
        ).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Cancelar", command=self.cancel).pack(
            side="right"
        )

        # Filtros (opcional)
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="5")
        filter_frame.pack(fill="x", pady=(10, 0))

        self.show_all_var = tk.BooleanVar(value=True)
        self.show_renamed_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            filter_frame,
            text="Mostrar todos",
            variable=self.show_all_var,
            command=self.apply_filters,
        ).pack(side="left")
        ttk.Checkbutton(
            filter_frame,
            text="Mostrar solo renombrados",
            variable=self.show_renamed_var,
            command=self.apply_filters,
        ).pack(side="left", padx=(10, 0))

    def populate_tree(self):
        """Llena el tree con los datos de previsualización."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agrupar por categoría
        categories = {}
        for data in self.preview_data:
            cat = data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(data)

        for category, files in categories.items():
            # Añadir nodo de categoría
            cat_node = self.tree.insert(
                "",
                "end",
                text=f"📁 {category}",
                values=(f"{len(files)} archivos", "", "", ""),
            )

            for file_data in files:
                size_str = self.format_file_size(file_data["file_size"])
                status = "Se renombrará" if file_data["will_rename"] else "Normal"

                self.tree.insert(
                    cat_node,
                    "end",
                    text=file_data["original_name"],
                    values=(category, file_data["final_name"], size_str, status),
                )

        # Expandir todos los nodos
        for item in self.tree.get_children():
            self.tree.item(item, open=True)

    def format_file_size(self, size_bytes: int) -> str:
        """Formatea el tamaño del archivo de manera legible."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/1024**2:.1f} MB"
        else:
            return f"{size_bytes/1024**3:.1f} GB"

    def apply_filters(self):
        """Aplica filtros a la vista."""
        # Implementar filtros si es necesario
        pass

    def proceed(self):
        """Procede con la organización."""
        if self.callback:
            self.callback(True)
        self.window.destroy()

    def cancel(self):
        """Cancela la operación."""
        if self.callback:
            self.callback(False)
        self.window.destroy()


class UndoWindow:
    """Ventana para gestionar operaciones de deshacer."""

    def __init__(self, parent, undo_manager: UndoManager):
        self.parent = parent
        self.undo_manager = undo_manager
        self.window = None
        self.tree = None
        self.create_window()

    def create_window(self):
        """Crea la ventana de gestión de deshacer."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Historial de Operaciones")
        self.window.geometry("700x500")
        self.window.transient(self.parent)
        self.window.grab_set()

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Título
        ttk.Label(
            main_frame, text="Historial de Operaciones", font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        # Treeview para operaciones
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("files", "folders", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")

        self.tree.heading("#0", text="Fecha y Hora")
        self.tree.heading("files", text="Archivos Movidos")
        self.tree.heading("folders", text="Carpetas Creadas")
        self.tree.heading("status", text="Estado")

        self.tree.column("#0", width=200)
        self.tree.column("files", width=120)
        self.tree.column("folders", width=120)
        self.tree.column("status", width=120)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Llenar el tree
        self.populate_tree()

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")

        ttk.Button(
            button_frame, text="Deshacer Seleccionada", command=self.undo_selected
        ).pack(side="left")
        ttk.Button(button_frame, text="Actualizar", command=self.populate_tree).pack(
            side="left", padx=(10, 0)
        )
        ttk.Button(button_frame, text="Cerrar", command=self.window.destroy).pack(
            side="right"
        )

    def populate_tree(self):
        """Llena el tree con las operaciones."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        operations = self.undo_manager.load_operations()
        operations.reverse()  # Mostrar las más recientes primero

        for op in operations:
            timestamp = datetime.fromisoformat(op["timestamp"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            files_count = len(op.get("moves", []))
            folders_count = len(op.get("folders_created", []))
            status = "Deshecha" if op.get("undone", False) else "Activa"

            self.tree.insert(
                "",
                "end",
                text=timestamp,
                values=(files_count, folders_count, status),
                tags=(op["id"],),
            )

    def undo_selected(self):
        """Deshace la operación seleccionada."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                "Advertencia", "Selecciona una operación para deshacer"
            )
            return

        item = selection[0]
        operation_id = self.tree.item(item, "tags")[0]

        # Verificar si ya fue deshecha
        operations = self.undo_manager.load_operations()
        operation = next((op for op in operations if op["id"] == operation_id), None)

        if operation and operation.get("undone", False):
            messagebox.showinfo("Información", "Esta operación ya fue deshecha")
            return

        if messagebox.askyesno("Confirmar", "¿Deshacer esta operación?"):
            if self.undo_manager.undo_operation(operation_id):
                messagebox.showinfo("Éxito", "Operación deshecha correctamente")
                self.populate_tree()
            else:
                messagebox.showerror("Error", "No se pudo deshacer la operación")
