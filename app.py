# -*- coding: utf-8 -*-
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging
from datetime import datetime
from config import FILE_TYPES, UI_CONFIG, LOG_CONFIG

# Configuración del logging
logging.basicConfig(
    filename=LOG_CONFIG["log_file"], level=logging.INFO, format=LOG_CONFIG["log_format"]
)


class FileOrganizer:
    def __init__(self):
        self.files_moved_count = 0
        self.folders_created_count = 0
        self.log_messages = []

    def get_file_extension(self, filename):
        """Obtiene la extensión de un archivo en minúsculas."""
        return os.path.splitext(filename)[1].lower()

    def get_category_for_extension(self, extension):
        """Determina la categoría (nombre de la carpeta) para una extensión dada."""
        for category, extensions in FILE_TYPES.items():
            if extension in extensions:
                return category
        return "Otros"

    def organize_files(self, source_directory, progress_callback=None):
        """
        Organiza los archivos en el directorio fuente moviéndolos a subcarpetas
        basadas en su tipo.
        """
        if not os.path.isdir(source_directory):
            error_message = (
                f"El directorio '{source_directory}' no existe o no es válido."
            )
            logging.error(error_message)
            return 0, 0, error_message

        self.files_moved_count = 0
        self.folders_created_count = 0
        self.log_messages = []

        try:
            # Obtener lista de archivos
            files = [
                f
                for f in os.listdir(source_directory)
                if os.path.isfile(os.path.join(source_directory, f))
            ]
            total_files = len(files)

            for index, item_name in enumerate(files, 1):
                if progress_callback:
                    progress = (index / total_files) * 100
                    progress_callback(progress)

                item_path = os.path.join(source_directory, item_name)
                file_extension = self.get_file_extension(item_name)
                category_name = self.get_category_for_extension(file_extension)

                # Crear carpeta de destino
                destination_folder_path = os.path.join(source_directory, category_name)
                if not os.path.exists(destination_folder_path):
                    try:
                        os.makedirs(destination_folder_path)
                        self.folders_created_count += 1
                        self.log_messages.append(
                            f"Carpeta creada: {destination_folder_path}"
                        )
                        logging.info(f"Carpeta creada: {destination_folder_path}")
                    except OSError as e:
                        error_msg = (
                            f"Error al crear carpeta {destination_folder_path}: {e}"
                        )
                        self.log_messages.append(error_msg)
                        logging.error(error_msg)
                        continue

                # Mover archivo
                destination_file_path = os.path.join(destination_folder_path, item_name)
                base_name, ext_name = os.path.splitext(item_name)
                counter = 1

                while os.path.exists(destination_file_path):
                    item_name = f"{base_name}_{counter}{ext_name}"
                    destination_file_path = os.path.join(
                        destination_folder_path, item_name
                    )
                    counter += 1

                try:
                    shutil.move(item_path, destination_file_path)
                    self.files_moved_count += 1
                    self.log_messages.append(
                        f"Movido: '{item_name}' -> '{category_name}/{item_name}'"
                    )
                    logging.info(
                        f"Archivo movido: {item_name} -> {category_name}/{item_name}"
                    )
                except Exception as e:
                    error_msg = f"Error al mover '{item_name}': {e}"
                    self.log_messages.append(error_msg)
                    logging.error(error_msg)

        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            logging.error(error_msg)
            return self.files_moved_count, self.folders_created_count, error_msg

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

        # Configurar tema y estilos
        self.setup_styles()
        self.setup_ui()
        self.file_organizer = FileOrganizer()

        # Cargar directorios iniciales
        self.load_initial_directories()

        # Vincular evento de redimensionamiento
        self.root.bind("<Configure>", self.on_window_resize)

    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        self.style = ttk.Style()

        # Configurar tema general
        self.style.configure(
            ".",
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        # Estilo para frames
        self.style.configure(
            "Custom.TLabelframe",
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",
            borderwidth=2,
            relief="solid",
        )

        # Estilo para botones
        self.style.configure(
            "Custom.TButton",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
            padding=10,
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
        )

        # Estilo para la barra de progreso
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=UI_CONFIG["theme"]["background_color"],
            background=UI_CONFIG["theme"]["primary_color"],
            thickness=20,
        )

        # Estilo para el Treeview
        self.style.configure(
            "Custom.Treeview",
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",
            fieldbackground=UI_CONFIG["theme"]["background_color"],
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        self.style.configure(
            "Custom.Treeview.Heading",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
        )

    def setup_ui(self):
        # Configurar el grid principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frame principal con padding y fondo
        main_frame = ttk.Frame(self.root, padding="20", style="Custom.TLabelframe")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(
            3, weight=1
        )  # Hacer que el área de log sea expansible
        main_frame.grid_columnconfigure(0, weight=1)

        # Título de la aplicación
        title_label = ttk.Label(
            main_frame,
            text="Organizador de Archivos",
            font=(UI_CONFIG["theme"]["font_family"], 16, "bold"),
            padding=(0, 0, 0, 20),
        )
        title_label.grid(row=0, column=0, sticky="ew")

        # Frame para la selección de directorio
        dir_selection_frame = ttk.Frame(main_frame)
        dir_selection_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        dir_selection_frame.grid_columnconfigure(0, weight=3)  # Árbol más ancho
        dir_selection_frame.grid_columnconfigure(1, weight=1)  # Controles más estrechos

        # Panel izquierdo para el árbol de directorios
        dir_tree_frame = ttk.LabelFrame(
            dir_selection_frame,
            text="Directorios Disponibles",
            padding="10",
            style="Custom.TLabelframe",
        )
        dir_tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        dir_tree_frame.grid_rowconfigure(0, weight=1)
        dir_tree_frame.grid_columnconfigure(0, weight=1)

        # Frame para el árbol y su scrollbar con padding adicional
        tree_container = ttk.Frame(dir_tree_frame)
        tree_container.grid(
            row=0, column=0, sticky="nsew", pady=(25, 0)
        )  # Padding superior para evitar solapamiento
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Crear Treeview para directorios
        self.dir_tree = ttk.Treeview(
            tree_container,
            columns=("path",),
            show="tree headings",
            style="Custom.Treeview",
        )
        self.dir_tree.heading("#0", text="Nombre")
        self.dir_tree.heading("path", text="Ruta")
        self.dir_tree.column("#0", width=200, minwidth=150)
        self.dir_tree.column("path", width=300, minwidth=200)

        # Configurar el estilo del árbol
        self.style.configure(
            "Treeview",
            rowheight=30,  # Aumentado para mejor legibilidad
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        # Estilo para las filas alternas y selección
        self.style.map(
            "Treeview",
            background=[("selected", UI_CONFIG["theme"]["primary_color"])],
            foreground=[("selected", UI_CONFIG["theme"]["text_color"])],
        )

        # Vincular evento de selección
        self.dir_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Scrollbar para el árbol
        tree_scroll = ttk.Scrollbar(
            tree_container, orient="vertical", command=self.dir_tree.yview
        )
        self.dir_tree.configure(yscrollcommand=tree_scroll.set)

        self.dir_tree.grid(
            row=0, column=0, sticky="nsew", padx=(0, 5)
        )  # Padding derecho para el scrollbar
        tree_scroll.grid(row=0, column=1, sticky="ns")

        # Panel derecho para controles
        controls_frame = ttk.Frame(dir_selection_frame)
        controls_frame.grid(
            row=0, column=1, sticky="n", padx=(5, 0)
        )  # Padding izquierdo para separación
        controls_frame.grid_columnconfigure(0, weight=1)

        # Botón para refrescar directorios
        refresh_button = ttk.Button(
            controls_frame,
            text="↻ Actualizar",
            command=self.refresh_directories,
            style="Custom.TButton",
        )
        refresh_button.grid(
            row=0, column=0, sticky="ew", pady=(0, 10)
        )  # Espaciado entre botones

        # Botón para seleccionar directorio personalizado
        custom_dir_button = ttk.Button(
            controls_frame,
            text="+ Otro Directorio",
            command=self.browse_directory,
            style="Custom.TButton",
        )
        custom_dir_button.grid(row=1, column=0, sticky="ew")

        # Frame para la ruta seleccionada
        selected_dir_frame = ttk.LabelFrame(
            main_frame,
            text="Directorio Seleccionado",
            padding="10",
            style="Custom.TLabelframe",
        )
        selected_dir_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        selected_dir_frame.grid_columnconfigure(0, weight=1)

        self.source_dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(
            selected_dir_frame,
            textvariable=self.source_dir_var,
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Frame para la barra de progreso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        progress_frame.grid_columnconfigure(0, weight=1)

        progress_label = ttk.Label(
            progress_frame,
            text="Progreso:",
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )
        progress_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="Custom.Horizontal.TProgressbar",
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        # Botón de organizar
        organize_button = ttk.Button(
            main_frame,
            text="Organizar Archivos",
            command=self.start_organization,
            style="Custom.TButton",
        )
        organize_button.grid(row=4, column=0, sticky="ew", pady=(0, 15))

        # Área de Log
        log_frame = ttk.LabelFrame(
            main_frame,
            text="Registro de Actividad",
            padding="10",
            style="Custom.TLabelframe",
        )
        log_frame.grid(row=5, column=0, sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # Contenedor para el área de texto y scrollbar
        log_container = ttk.Frame(log_frame)
        log_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        log_container.grid_rowconfigure(0, weight=1)
        log_container.grid_columnconfigure(0, weight=1)

        # Crear Text widget con scrollbar
        self.log_text = tk.Text(
            log_container,
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED,
            bg=UI_CONFIG["theme"]["background_color"],
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            padx=10,
            pady=10,
        )
        scrollbar = ttk.Scrollbar(
            log_container, orient=tk.VERTICAL, command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(
            row=0, column=0, sticky="nsew", padx=(0, 5)
        )  # Padding derecho para el scrollbar
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar colores para diferentes tipos de mensajes
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("success", foreground="green")

    def on_window_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        # Ajustar el tamaño de las columnas del árbol
        tree_width = self.dir_tree.winfo_width()
        self.dir_tree.column("#0", width=int(tree_width * 0.4))
        self.dir_tree.column("path", width=int(tree_width * 0.6))

    def load_initial_directories(self):
        """Carga los directorios iniciales en el árbol"""
        # Directorios comunes para buscar
        common_dirs = {
            "Home": os.path.expanduser("~"),
            "Documentos": os.path.expanduser("~/Documents"),
            "Descargas": os.path.expanduser("~/Downloads"),
            "Escritorio": os.path.expanduser("~/Desktop"),
            "Sistema": {"Raíz": "/", "Montajes": "/mnt", "Usuarios": "/home"},
        }

        # Limpiar el árbol
        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

        # Añadir directorios principales
        for name, path in common_dirs.items():
            if isinstance(path, dict):
                # Crear categoría principal
                parent = self.dir_tree.insert("", "end", text=name, values=("",))
                # Añadir subdirectorios
                for subname, subpath in path.items():
                    if os.path.exists(subpath):
                        self.dir_tree.insert(
                            parent, "end", text=subname, values=(subpath,)
                        )
            elif os.path.exists(path):
                self.dir_tree.insert("", "end", text=name, values=(path,))

        # Expandir el árbol
        for item in self.dir_tree.get_children():
            self.dir_tree.item(item, open=True)

    def add_directory_to_tree(self, dir_path, parent=""):
        """Añade un directorio al árbol con mejor organización"""
        try:
            # Obtener el nombre del directorio
            dir_name = os.path.basename(dir_path)
            if not dir_name:  # Si es la raíz
                dir_name = dir_path

            # Insertar en el árbol
            item = self.dir_tree.insert(
                parent, "end", text=dir_name, values=(dir_path,)
            )

            # Intentar cargar subdirectorios (hasta un nivel)
            try:
                for subdir in os.listdir(dir_path):
                    subdir_path = os.path.join(dir_path, subdir)
                    if os.path.isdir(subdir_path) and not subdir.startswith("."):
                        self.dir_tree.insert(
                            item, "end", text=subdir, values=(subdir_path,)
                        )
            except PermissionError:
                # Ignorar errores de permisos al listar subdirectorios
                pass

        except Exception as e:
            logging.error(f"Error al añadir directorio al árbol: {e}")

    def refresh_directories(self):
        """Actualiza la lista de directorios"""
        # Limpiar el árbol
        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

        # Recargar directorios
        self.load_initial_directories()
        self.add_log_message("Lista de directorios actualizada", "info")

    def browse_directory(self):
        """Abre un diálogo para seleccionar un directorio personalizado"""
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir_var.set(directory)
            self.add_directory_to_tree(directory)
            self.add_log_message(f"Directorio añadido: {directory}", "success")

    def on_tree_select(self, event):
        """Maneja la selección de un directorio en el árbol"""
        selected_items = self.dir_tree.selection()
        if selected_items:
            item = selected_items[0]
            dir_path = self.dir_tree.item(item)["values"][0]
            if dir_path:  # Solo actualizar si hay una ruta
                self.source_dir_var.set(dir_path)
                self.add_log_message(f"Directorio seleccionado: {dir_path}", "info")

    def add_log_message(self, message, message_type="info"):
        """Añade un mensaje al área de log con formato y color según el tipo"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"{timestamp} - {message}\n"

        self.log_text.insert(tk.END, formatted_message, message_type)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()

    def start_organization(self):
        source_dir = self.source_dir_var.get()
        if not source_dir:
            messagebox.showwarning(
                "Directorio no Especificado",
                "Por favor, selecciona un directorio para organizar.",
            )
            return

        self.clear_log()
        self.progress_var.set(0)
        self.add_log_message(f"Iniciando organización en: {source_dir}")

        confirm = messagebox.askyesno(
            "Confirmar Organización",
            f"¿Estás seguro de que deseas organizar los archivos en '{source_dir}'?\n"
            "Esta acción moverá los archivos a nuevas subcarpetas.\n"
            "Es recomendable hacer una copia de seguridad antes de proceder.",
        )

        if not confirm:
            self.add_log_message("Organización cancelada por el usuario.")
            return

        try:
            files_moved, folders_created, log_details = (
                self.file_organizer.organize_files(
                    source_dir, progress_callback=self.update_progress
                )
            )

            self.add_log_message(log_details)

            if files_moved > 0 or folders_created > 0:
                messagebox.showinfo(
                    "Organización Completa",
                    f"Proceso finalizado.\n\n"
                    f"Archivos movidos: {files_moved}\n"
                    f"Carpetas creadas: {folders_created}\n\n"
                    f"Revisa el registro para más detalles.",
                )
            else:
                messagebox.showinfo(
                    "Organización Completa",
                    "No se movieron archivos ni se crearon carpetas nuevas.",
                )

        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.add_log_message(error_msg, message_type="error")
            messagebox.showerror("Error", error_msg)
            logging.error(error_msg)


if __name__ == "__main__":
    root_window = tk.Tk()
    app = App(root_window)
    root_window.mainloop()
