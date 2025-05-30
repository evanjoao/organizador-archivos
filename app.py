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
            self.log_messages.append(error_message)  # Registrar también en log_messages
            return 0, 0, error_message

        self.files_moved_count = 0
        self.folders_created_count = 0
        self.log_messages = [
            f"Iniciando organización en: {source_directory}"
        ]  # Mensaje inicial

        try:
            files = [
                f
                for f in os.listdir(source_directory)
                if os.path.isfile(os.path.join(source_directory, f))
            ]
            total_files = len(files)
            if total_files == 0:
                self.log_messages.append("No se encontraron archivos para organizar.")
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
                        msg = f"Carpeta creada: {destination_folder_path}"
                        self.log_messages.append(msg)
                        logging.info(msg)
                    except OSError as e:
                        error_msg = (
                            f"Error al crear carpeta {destination_folder_path}: {e}"
                        )
                        self.log_messages.append(error_msg)
                        logging.error(error_msg)
                        continue

                destination_file_path = os.path.join(destination_folder_path, item_name)
                original_item_name = item_name  # Guardar nombre original para logs
                base_name, ext_name = os.path.splitext(item_name)
                counter = 1

                while os.path.exists(destination_file_path):
                    item_name_new = f"{base_name}_{counter}{ext_name}"
                    destination_file_path = os.path.join(
                        destination_folder_path, item_name_new
                    )
                    counter += 1

                # Si el nombre cambió por colisión, usar el nuevo nombre para el movimiento
                # pero el original para el mensaje de log si es posible.
                # En este caso, item_name ya está actualizado si hubo colisión.

                try:
                    shutil.move(item_path, destination_file_path)
                    self.files_moved_count += 1
                    # Usar item_name que es el nombre final del archivo (puede tener _counter)
                    msg = f"Movido: '{item_name}' -> '{category_name}/{item_name}'"
                    self.log_messages.append(msg)
                    logging.info(msg)
                except Exception as e:
                    error_msg = f"Error al mover '{original_item_name}': {e}"
                    self.log_messages.append(error_msg)
                    logging.error(error_msg)

        except Exception as e:
            error_msg = f"Error inesperado durante la organización: {str(e)}"
            self.log_messages.append(error_msg)
            logging.error(error_msg)
            # Devolver los conteos actuales y los mensajes de log acumulados
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
                "No se movieron archivos ni se crearon carpetas nuevas (posiblemente ya estaban organizados o hubo errores)."
            )
        elif total_files > 0:
            self.log_messages.append("Organización completada.")

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

        self.setup_styles()
        self.setup_ui()
        self.file_organizer = FileOrganizer()
        self.load_initial_directories()
        self.root.bind("<Configure>", self.on_window_resize)

    def setup_styles(self):
        self.style = ttk.Style()

        # Intentar establecer un tema base que permita más personalización si es posible
        # Temas comunes: 'clam', 'alt', 'default', 'classic'
        # 'clam' suele ser bueno para personalizar
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            print("Tema 'clam' no disponible, usando tema por defecto.")

        # Estilo general para todos los widgets ttk (si el tema lo permite)
        self.style.configure(
            ".",
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",  # Color de texto por defecto
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
        )

        # Estilo para LabelFrame
        self.style.configure(
            "Custom.TLabelframe",
            background=UI_CONFIG["theme"]["background_color"],
            padding=UI_CONFIG["theme"]["padding"]["medium"],
        )
        self.style.configure(
            "Custom.TLabelframe.Label",  # Estilo para el texto de la etiqueta del LabelFrame
            background=UI_CONFIG["theme"]["background_color"],
            foreground="black",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"],
                "bold",
            ),
        )

        # Estilo para Botones
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
            relief="raised",  # Estilo de borde
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

        # Estilo para Barra de Progreso
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=UI_CONFIG["theme"]["background_color"],  # Color del canal
            background=UI_CONFIG["theme"]["primary_color"],  # Color de la barra
            thickness=20,
        )

        # Estilo para Treeview
        self.style.configure(
            "Custom.Treeview",
            background=UI_CONFIG["theme"][
                "background_color"
            ],  # Fondo general del widget
            fieldbackground=UI_CONFIG["theme"][
                "background_color"
            ],  # Fondo de las celdas
            foreground="black",  # Color del texto
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            rowheight=30,  # MEJORA: Aumentar altura de fila
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            font=(
                UI_CONFIG["theme"]["font_family"],
                UI_CONFIG["theme"]["font_size"] + 1,
                "bold",
            ),  # Un poco más grande y negrita
            background=UI_CONFIG["theme"]["primary_color"],
            foreground=UI_CONFIG["theme"]["text_color"],
            relief="raised",
        )
        self.style.map(
            "Custom.Treeview",
            background=[
                ("selected", UI_CONFIG["theme"]["primary_color"])
            ],  # MEJORA: Usar color de config
            foreground=[
                ("selected", UI_CONFIG["theme"]["text_color"])
            ],  # MEJORA: Usar color de config
        )
        # Para Entry, no hay un estilo ttk directo tan flexible como en CTk, pero podemos usar opciones
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
        # Configurar filas para expansión, especialmente la del log
        main_frame.grid_rowconfigure(0, weight=0)  # title_label
        main_frame.grid_rowconfigure(
            1, weight=1
        )  # dir_selection_frame (contiene el treeview que debe expandirse)
        main_frame.grid_rowconfigure(2, weight=0)  # selected_dir_frame
        main_frame.grid_rowconfigure(3, weight=0)  # progress_frame
        main_frame.grid_rowconfigure(4, weight=0)  # organize_button
        main_frame.grid_rowconfigure(
            5, weight=2
        )  # log_frame (darle más peso para que se expanda más)

        title_label = ttk.Label(
            main_frame,
            text="Organizador de Archivos",
            font=(
                UI_CONFIG["theme"]["font_family"],
                18,
                "bold",
            ),  # MEJORA: Fuente más grande
            anchor="center",
            style="Custom.TLabelframe.Label",  # Para que tome el fondo correcto si es necesario
        )
        title_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["large"]),
        )

        dir_selection_frame = ttk.Frame(
            main_frame, style="Custom.TLabelframe"
        )  # Usar el estilo para el fondo
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
        )  # Permitir que el LabelFrame del árbol se expanda

        dir_tree_frame = ttk.LabelFrame(
            dir_selection_frame,
            text="Directorios Disponibles",
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
        )  # El tree_container se expandirá en esta fila
        dir_tree_frame.grid_columnconfigure(0, weight=1)

        # MEJORA: Padding superior para el tree_container para evitar solapamiento con el título del LabelFrame
        tree_container = ttk.Frame(
            dir_tree_frame, style="Custom.TLabelframe"
        )  # Para heredar fondo
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
        self.dir_tree.heading("#0", text="Nombre")
        self.dir_tree.heading("path", text="Ruta")
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
        tree_scroll_x.grid(row=1, column=0, sticky="ew")  # Scrollbar horizontal debajo

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_rowconfigure(1, weight=0)  # Para el scrollbar X
        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_columnconfigure(1, weight=0)  # Para el scrollbar Y

        self.dir_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        controls_frame = ttk.Frame(
            dir_selection_frame, style="Custom.TLabelframe"
        )  # Para heredar fondo
        controls_frame.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(UI_CONFIG["theme"]["padding"]["small"], 0),
        )  # sticky 'ns' para que los botones estén arriba
        controls_frame.grid_columnconfigure(0, weight=1)

        refresh_button = ttk.Button(
            controls_frame,
            text="↻ Actualizar",
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
            text="+ Otro Directorio",
            command=self.browse_directory,
            style="Custom.TButton",
        )
        custom_dir_button.grid(row=1, column=0, sticky="ew")

        selected_dir_frame = ttk.LabelFrame(
            main_frame,
            text="Directorio Seleccionado",
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
            ),  # Fuente para Entry
        )
        self.dir_entry.grid(
            row=0, column=0, sticky="ew", padx=5, pady=5
        )  # Padding interno en el LabelFrame

        progress_outer_frame = ttk.Frame(
            main_frame, style="Custom.TLabelframe"
        )  # Contenedor para la etiqueta y la barra
        progress_outer_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )
        progress_outer_frame.grid_columnconfigure(
            0, weight=1
        )  # Para que la barra se expanda

        progress_label = ttk.Label(
            progress_outer_frame, text="Progreso:", style="Custom.TLabelframe.Label"
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

        organize_button = ttk.Button(
            main_frame,
            text="Organizar Archivos",
            command=self.start_organization,
            style="Custom.TButton",
        )
        organize_button.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, UI_CONFIG["theme"]["padding"]["medium"]),
        )

        log_frame = ttk.LabelFrame(
            main_frame,
            text="Registro de Actividad",
            padding=UI_CONFIG["theme"]["padding"]["medium"],
            style="Custom.TLabelframe",
        )
        log_frame.grid(row=5, column=0, sticky="nsew")
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        log_container = ttk.Frame(
            log_frame, style="Custom.TLabelframe"
        )  # Para heredar fondo
        log_container.grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5
        )  # Padding interno
        log_container.grid_rowconfigure(0, weight=1)
        log_container.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_container,
            wrap=tk.WORD,
            height=10,  # Altura inicial, se expandirá
            state=tk.DISABLED,
            font=(UI_CONFIG["theme"]["font_family"], UI_CONFIG["theme"]["font_size"]),
            bg=UI_CONFIG["theme"]["background_color"],  # Fondo del Text widget
            fg="black",  # Color de texto por defecto para el log
            padx=UI_CONFIG["theme"]["padding"]["small"],
            pady=UI_CONFIG["theme"]["padding"]["small"],
            relief=tk.SOLID,  # Borde para el Text
            borderwidth=1,
        )
        log_scroll = ttk.Scrollbar(
            log_container, orient="vertical", command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll.grid(row=0, column=1, sticky="ns")

        # MEJORA: Configurar colores para el log usando UI_CONFIG
        self.log_text.tag_configure(
            "info", foreground=UI_CONFIG["theme"]["colors"].get("info_text", "black")
        )  # Usar un color específico para info si existe
        self.log_text.tag_configure(
            "error", foreground=UI_CONFIG["theme"]["colors"]["error"]
        )
        self.log_text.tag_configure(
            "success", foreground=UI_CONFIG["theme"]["colors"]["success"]
        )
        self.log_text.tag_configure(
            "warning", foreground=UI_CONFIG["theme"]["colors"]["warning"]
        )

    def on_window_resize(self, event=None):  # Permitir llamar sin evento
        # Solo ajustar si la ventana ya tiene un tamaño (evitar errores al inicio)
        if self.root.winfo_width() > 1 and self.dir_tree.winfo_width() > 1:
            tree_width = self.dir_tree.winfo_width()
            # Asegurarse de que las columnas no sean demasiado pequeñas
            col_0_width = int(tree_width * 0.4)
            col_1_width = int(tree_width * 0.6)

            if col_0_width < 100:
                col_0_width = 100  # Mínimo para Nombre
            if col_1_width < 150:
                col_1_width = 150  # Mínimo para Ruta

            self.dir_tree.column("#0", width=col_0_width)
            self.dir_tree.column("path", width=col_1_width)

    def load_initial_directories(self):
        common_dirs = {
            "Home": os.path.expanduser("~"),
            "Documentos": os.path.expanduser("~/Documents"),
            "Descargas": os.path.expanduser("~/Downloads"),
            "Escritorio": os.path.expanduser("~/Desktop"),
            "Imágenes": os.path.expanduser("~/Pictures"),
            "Música": os.path.expanduser("~/Music"),
            "Vídeos": os.path.expanduser("~/Videos"),
            "Sistema": {"Raíz": "/", "Montajes": "/mnt", "Usuarios": "/home"},
        }

        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

        for name, path_or_dict in common_dirs.items():
            if isinstance(path_or_dict, dict):
                parent_id = self.dir_tree.insert(
                    "", "end", text=name, values=("",), open=False
                )  # No abrir por defecto
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

        # Llamar a on_window_resize una vez después de cargar para ajustar columnas
        self.root.after(100, self.on_window_resize)

    def add_directory_to_tree(self, dir_path, parent=""):
        try:
            dir_name = os.path.basename(dir_path) or dir_path
            # Evitar duplicados si ya existe con la misma ruta
            for item_id in self.dir_tree.get_children(parent):
                if (
                    self.dir_tree.item(item_id, "values")
                    and self.dir_tree.item(item_id, "values")[0] == dir_path
                ):
                    self.dir_tree.selection_set(item_id)  # Seleccionar el existente
                    self.dir_tree.focus(item_id)
                    return

            item = self.dir_tree.insert(
                parent, "end", text=dir_name, values=(dir_path,), open=True
            )
            self.dir_tree.selection_set(item)
            self.dir_tree.focus(item)

            # Opcional: Cargar un nivel de subdirectorios (puede ser lento para directorios grandes)
            # for sub_item in os.listdir(dir_path):
            #     sub_item_path = os.path.join(dir_path, sub_item)
            #     if os.path.isdir(sub_item_path) and not sub_item.startswith("."):
            #         self.dir_tree.insert(item, "end", text=sub_item, values=(sub_item_path,))

        except Exception as e:
            logging.error(f"Error al añadir directorio al árbol: {dir_path}, {e}")
            self.add_log_message(f"Error al acceder a {dir_path}: {e}", "error")

    def refresh_directories(self):
        self.load_initial_directories()
        self.add_log_message("Lista de directorios actualizada.", "info")

    def browse_directory(self):
        directory = filedialog.askdirectory(
            initialdir=self.source_dir_var.get() or os.path.expanduser("~")
        )
        if directory:
            self.source_dir_var.set(directory)
            self.add_directory_to_tree(directory)  # Añadirlo al árbol
            self.add_log_message(
                f"Directorio seleccionado para organizar: {directory}", "success"
            )

    def on_tree_select(self, event):
        selected_items = self.dir_tree.selection()
        if selected_items:
            item = selected_items[0]
            # Asegurarse de que 'values' no esté vacío y tenga al menos un elemento
            item_values = self.dir_tree.item(item, "values")
            if item_values and item_values[0]:
                dir_path = item_values[0]
                self.source_dir_var.set(dir_path)
                # No es necesario un log aquí, es muy verboso. El log es más útil para acciones.
            # else:
            # Es una categoría padre sin ruta, no hacer nada o limpiar el entry.
            # self.source_dir_var.set("")

    def add_log_message(self, message, message_type="info"):
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Si el mensaje es una lista (de FileOrganizer), unirla
        if isinstance(message, list):
            message = "\n".join(message)

        # Dividir el mensaje en líneas para aplicar el tag a cada una si es multilínea
        lines = message.split("\n")
        for line in lines:
            if line.strip():  # Evitar líneas vacías o solo con espacios
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
        self.root.update_idletasks()  # Forzar actualización de la UI

    def start_organization(self):
        source_dir = self.source_dir_var.get()
        if not source_dir:
            messagebox.showwarning(
                "Directorio no Especificado",
                "Por favor, selecciona un directorio para organizar.",
            )
            return
        if not os.path.isdir(source_dir):
            messagebox.showerror(
                "Directorio Inválido",
                f"La ruta '{source_dir}' no es un directorio válido.",
            )
            return

        self.clear_log()
        self.progress_var.set(0)
        # El mensaje inicial de organización ya se añade en FileOrganizer

        confirm = messagebox.askyesno(
            "Confirmar Organización",
            f"¿Estás seguro de que deseas organizar los archivos en '{source_dir}'?\n"
            "Esta acción moverá los archivos a nuevas subcarpetas.\n"
            "Es recomendable hacer una copia de seguridad antes de proceder.",
            icon="warning",  # Icono para el messagebox
        )

        if not confirm:
            self.add_log_message("Organización cancelada por el usuario.", "warning")
            return

        try:
            # Deshabilitar botón mientras se organiza para evitar clics múltiples
            # Esto requeriría guardar una referencia al botón: self.organize_button.config(state=tk.DISABLED)
            # Y luego habilitarlo en un bloque finally: self.organize_button.config(state=tk.NORMAL)

            files_moved, folders_created, log_details_str = (
                self.file_organizer.organize_files(
                    source_dir, progress_callback=self.update_progress
                )
            )

            # log_details_str ya es una cadena con saltos de línea
            self.add_log_message(
                log_details_str
            )  # Se aplicarán tags según el contenido si se mejora FileOrganizer

            # Determinar el tipo de mensaje final basado en los resultados
            if files_moved > 0 or folders_created > 0:
                final_summary = (
                    f"Proceso finalizado.\n\n"
                    f"Archivos movidos: {files_moved}\n"
                    f"Carpetas creadas: {folders_created}\n\n"
                    f"Revisa el registro para más detalles."
                )
                messagebox.showinfo("Organización Completa", final_summary)

            elif (
                self.file_organizer.log_messages
                and "No se encontraron archivos para organizar."
                in self.file_organizer.log_messages[-1]
            ):
                messagebox.showinfo(
                    "Organización",
                    "No se encontraron archivos en el directorio especificado.",
                )

            elif (
                self.file_organizer.log_messages
                and "Organización cancelada" not in self.file_organizer.log_messages[-1]
            ):
                messagebox.showinfo(
                    "Organización Completa",
                    "No se realizaron cambios. Los archivos podrían estar ya organizados o no hubo archivos que mover.",
                )

        except Exception as e:
            error_msg = f"Error crítico durante la organización: {str(e)}"
            self.add_log_message(error_msg, "error")
            messagebox.showerror("Error Crítico", error_msg)
            logging.exception(
                error_msg
            )  # Usar logging.exception para incluir traceback
        finally:
            self.progress_var.set(100)  # Asegurar que la barra llegue al final
            # Habilitar botón de organizar si se deshabilitó


if __name__ == "__main__":
    root_window = tk.Tk()
    app = App(root_window)
    root_window.mainloop()
