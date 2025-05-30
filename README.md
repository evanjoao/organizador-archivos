# File Organizer - Advanced Version

Una aplicación avanzada de organización de archivos desarrollada en Python con Tkinter, con funcionalidades extendidas de personalización, filtrado y control de cambios.

## 🚀 Características Principales

### 🔧 Gestión de Configuraciones Personalizable

- **Categorías personalizadas**: Define tus propias categorías de archivos y asigna extensiones
- **Configuración persistente**: Las configuraciones se guardan automáticamente en `settings.json`
- **Interfaz intuitiva**: Ventana dedicada para gestionar categorías y extensiones
- **Editor de categorías**: Agrega, edita y elimina categorías fácilmente

### 🔍 Sistema de Filtros Avanzados

- **Filtro por extensión**: Selecciona tipos específicos de archivos
- **Filtro por tamaño**: Define rangos de tamaño (KB, MB, GB)
- **Filtro por fecha**: Filtra por fecha de modificación o creación
- **Filtro por nombre**: Búsqueda por patrones en nombres de archivo
- **Filtro por categoría**: Organiza según categorías personalizadas
- **Combinación de filtros**: Usa múltiples criterios simultáneamente

### 👁️ Sistema de Previsualización

- **Vista previa detallada**: Ve exactamente qué archivos se moverán y a dónde
- **Información completa**: Tamaño, fecha de modificación, destino
- **Vista de árbol**: Organización jerárquica de archivos y carpetas de destino
- **Confirmación antes de ejecutar**: Previene errores de organización

### ↩️ Sistema de Deshacer Operaciones

- **Historial completo**: Registro de todas las operaciones realizadas
- **Deshacer selectivo**: Revierte operaciones específicas
- **Información detallada**: Ve qué archivos fueron movidos en cada operación
- **Persistencia**: El historial se guarda en `undo_history.json`

### 📊 Estadísticas de Archivos

- **Conteo por categoría**: Cuántos archivos hay de cada tipo
- **Información de tamaño**: Espacio ocupado por categoría
- **Análisis del directorio**: Vista general del contenido
- **Distribución visual**: Resumen claro de la composición del directorio

### 🎨 Interfaz Moderna

- Interfaz gráfica moderna y fácil de usar (Tkinter + ttk con estilos personalizados)
- Organización automática de archivos por tipo
- Soporte para múltiples tipos de archivo
- Visualización de progreso en tiempo real
- Log detallado de operaciones con mensajes codificados por colores
- Navegación intuitiva de directorios
- Compatible con Windows, Linux y macOS

## 🎛️ Nuevos Controles de la Interfaz

### Botones de Control Principal

- **Settings**: Abre la ventana de configuración de categorías
- **Filters**: Configura filtros avanzados para la organización
- **Preview**: Muestra una vista previa de los cambios antes de aplicarlos
- **Organize**: Ejecuta la organización de archivos
- **Undo**: Abre la ventana de historial para deshacer operaciones
- **Statistics**: Muestra estadísticas detalladas del directorio

### Ventanas Especializadas

#### Ventana de Configuraciones

- Lista de todas las categorías disponibles
- Botones para agregar, editar y eliminar categorías
- Editor de extensiones para cada categoría
- Guardado automático de cambios

#### Ventana de Filtros

- Múltiples tipos de filtros configurables
- Vista previa en tiempo real de archivos que coinciden
- Aplicación y limpieza de filtros
- Combinación de criterios

#### Ventana de Previsualización

- Vista de árbol que muestra la estructura de destino
- Información detallada de cada archivo
- Confirmación antes de proceder
- Cancelación segura

#### Ventana de Deshacer

- Historial cronológico de operaciones
- Información detallada de cada operación
- Selección y reversión de operaciones específicas
- Validación antes de deshacer

## 📋 Requisitos del Sistema

- **Python**: 3.6 o superior
- **Tkinter**: Incluido en la mayoría de instalaciones de Python
- **Sistema Operativo**: Windows, Linux o macOS
- **Espacio en disco**: Mínimo para archivos de configuración e historial

## 🔧 Instalación

1.**Clona el repositorio**:

```bash
git clone https://github.com/evanjoao/organizador-archivos.git
cd organizador-archivos
```

2.**Verifica Python**:

```bash
python --version  # Debe ser 3.6+
```

3.**Ejecuta la aplicación**:

```bash
python app.py
```

> **Nota**: No se requieren dependencias adicionales más allá de Python y Tkinter.

## 📖 Guía de Uso

### 🔰 Uso Básico

1. **Inicia la aplicación**:

   ```bash
   python app.py
   ```

2. **Selecciona un directorio** usando el botón "Browse" o el árbol de directorios

3. **Organiza archivos**:
   - Haz clic directamente en "Organize" para usar configuraciones por defecto
   - O sigue el flujo avanzado para mayor control

### 🎯 Uso Avanzado

#### 1. Configurar Categorías Personalizadas

- Haz clic en **Settings**
- Usa "Add Category" para crear nuevas categorías
- Edita categorías existentes con "Edit Category"
- Asigna extensiones específicas a cada categoría
- Los cambios se guardan automáticamente

#### 2. Aplicar Filtros Específicos

- Haz clic en **Filters**
- Configura filtros por:
  - **Extensión**: Selecciona tipos específicos
  - **Tamaño**: Define rangos mínimos y máximos
  - **Fecha**: Filtra por fecha de modificación
  - **Nombre**: Usa patrones de búsqueda
  - **Categoría**: Filtra por categorías específicas
- Aplica los filtros antes de organizar

#### 3. Previsualizar Cambios

- Haz clic en **Preview** después de configurar filtros
- Revisa la vista de árbol que muestra:
  - Qué archivos se moverán
  - A qué carpetas irán
  - Información detallada de cada archivo
- Confirma los cambios o cancela para ajustar

#### 4. Gestionar Historial de Operaciones

- Usa **Undo** para ver todas las operaciones realizadas
- Selecciona operaciones específicas para revertir
- Ve información detallada de cada operación
- Confirma antes de deshacer cambios

#### 5. Analizar Directorios

- Haz clic en **Statistics** para ver:
  - Distribución de archivos por categoría
  - Conteo de archivos de cada tipo
  - Tamaño total por categoría
  - Resumen general del directorio

## 📁 Estructura del Proyecto

```text
App/
├── app.py                    # Aplicación principal
├── config.py                 # Configuraciones base y categorías por defecto
├── settings_manager.py       # Sistema de gestión de configuraciones
├── preview_undo.py          # Sistema de previsualización y deshacer
├── filters.py               # Sistema de filtros avanzados
├── settings.json            # Configuraciones personalizadas (auto-generado)
├── undo_history.json        # Historial de operaciones (auto-generado)
└── README.md               # Este archivo
```

### Descripción de Archivos

- **app.py**: Archivo principal que contiene la interfaz de usuario y la lógica de organización
- **config.py**: Definiciones de categorías por defecto y configuraciones básicas
- **settings_manager.py**: Manejo de configuraciones personalizadas y ventana de configuración
- **preview_undo.py**: Sistema de previsualización y gestión del historial de operaciones
- **filters.py**: Sistema de filtros avanzados con múltiples criterios
- **settings.json**: Archivo generado automáticamente para guardar configuraciones del usuario
- **undo_history.json**: Archivo generado automáticamente para guardar el historial de operaciones

## 🗂️ Categorías por Defecto

### Documentos

- **.pdf, .doc, .docx**: Documentos de texto
- **.txt, .rtf, .odt**: Archivos de texto plano y procesadores
- **.xls, .xlsx, .ppt, .pptx**: Hojas de cálculo y presentaciones

### Imágenes

- **.jpg, .jpeg, .png**: Formatos de imagen comunes
- **.gif, .bmp, .svg**: Formatos de imagen adicionales
- **.webp, .tiff**: Formatos de imagen modernos

### Videos

- **.mp4, .avi, .mkv**: Formatos de video populares
- **.mov, .wmv, .flv**: Formatos de video adicionales
- **.webm, .m4v**: Formatos de video modernos

### Audio

- **.mp3, .wav, .flac**: Formatos de audio comunes
- **.aac, .ogg, .wma**: Formatos de audio adicionales
- **.m4a**: Formato de audio moderno

### Archivos Comprimidos

- **.zip, .rar, .7z**: Compresores populares
- **.tar, .gz, .bz2**: Compresores Unix/Linux

### Código

- **.py, .js, .html, .css**: Lenguajes web y Python
- **.java, .cpp, .c**: Lenguajes compilados
- **.json, .xml, .yaml**: Archivos de configuración

### Ejecutables

- **.exe, .msi**: Ejecutables Windows
- **.deb, .rpm**: Paquetes Linux
- **.dmg, .app**: Archivos macOS

## 🛡️ Características de Seguridad

- **Validación de archivos**: Verificación antes de mover archivos
- **Historial de operaciones**: Registro completo para deshacer cambios
- **Previsualización**: Confirmación antes de realizar cambios
- **Manejo de errores**: Gestión robusta de errores de archivo
- **Respaldos implícitos**: El sistema de deshacer actúa como respaldo

## 🎨 Personalización

### Crear Categorías Personalizadas

1. Abre **Settings**
2. Haz clic en "Add Category"
3. Ingresa el nombre de la categoría
4. Agrega extensiones separadas por comas
5. Confirma para guardar

### Modificar Categorías Existentes

1. Selecciona una categoría en la lista
2. Haz clic en "Edit Category"
3. Modifica el nombre o las extensiones
4. Los cambios se guardan automáticamente

### Eliminar Categorías

1. Selecciona la categoría a eliminar
2. Haz clic en "Delete Category"
3. Confirma la eliminación

## 💡 Consejos de Uso

### Mejores Prácticas

- **Siempre previsualiza**: Usa "Preview" antes de organizar
- **Configura filtros**: Para trabajar con tipos específicos de archivos
- **Revisa el historial**: El botón "Undo" te permite deshacer errores
- **Personaliza categorías**: Adapta las categorías a tus necesidades
- **Mantén respaldos**: Aunque hay sistema de deshacer, los respaldos son importantes

### Flujo de Trabajo Recomendado

1. **Selecciona el directorio** a organizar
2. **Configura categorías** personalizadas si es necesario
3. **Aplica filtros** para trabajar con archivos específicos
4. **Previsualiza** los cambios
5. **Ejecuta** la organización
6. **Revisa** el log de actividad
7. **Usa Statistics** para analizar el resultado

## 🔮 Desarrollo Futuro

### Funcionalidades Planeadas

- **Modo batch**: Organización de múltiples directorios
- **Integración cloud**: Soporte para servicios de almacenamiento en la nube
- **Sistema de plugins**: Extensiones personalizadas
- **Temas adicionales**: Más opciones de personalización visual
- **Programación de tareas**: Organización automática programada
- **Reglas avanzadas**: Lógica de organización más compleja

### Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. **Fork** el proyecto
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ve el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor y Contacto

**Evan Joao** - [evanjoaogarciamunoz@gmail.com](mailto:evanjoaogarciamunoz@gmail.com)

**Enlace del Proyecto**: [https://github.com/evanjoao/organizador-archivos](https://github.com/evanjoao/organizador-archivos)

---

### 📊 Resumen de Mejoras

Esta versión avanzada incluye:

- ✅ **4 nuevos módulos** con funcionalidades especializadas
- ✅ **6 nuevos botones** de control en la interfaz
- ✅ **4 ventanas especializadas** para gestión avanzada
- ✅ **Sistema de configuración** completamente personalizable
- ✅ **Filtros avanzados** con múltiples criterios
- ✅ **Previsualización completa** antes de realizar cambios
- ✅ **Sistema de deshacer** con historial persistente
- ✅ **Estadísticas detalladas** del directorio
- ✅ **Interfaz moderna** y funcional

La aplicación ha evolucionado de un organizador básico a una herramienta robusta y profesional para la gestión de archivos.
