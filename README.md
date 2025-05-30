# Organizador de Archivos

Una aplicación de escritorio desarrollada en Python para organizar automáticamente archivos en carpetas según su tipo.

## Características

- Interfaz gráfica moderna y fácil de usar (Tkinter + ttk, estilos personalizados)
- Organización automática de archivos por tipo
- Soporte para múltiples tipos de archivos
- Visualización en tiempo real del progreso
- Registro detallado de operaciones con mensajes codificados por color
- Navegación intuitiva por directorios (árbol de directorios, selección personalizada)
- Compatible con Windows, Linux y macOS

## Requisitos

- Python 3.x
- tkinter (incluido en la mayoría de las instalaciones de Python)
- Sistema operativo: Windows, Linux o macOS

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/evanjoao/organizador-archivos.git
cd organizador-archivos
```

2. Instala las dependencias (si tienes requirements.txt):

```bash
pip install -r requirements.txt
```

> **Nota:** Si no existe `requirements.txt`, solo asegúrate de tener Python 3 y tkinter instalado.

## Uso

1. Ejecuta la aplicación:

```bash
python app.py
```

2. Selecciona el directorio que deseas organizar
3. Haz clic en "Organizar Archivos"
4. Espera a que se complete el proceso
5. Revisa el registro de actividad para ver los detalles

## Estructura del Proyecto

```
organizador-archivos/
├── app.py              # Aplicación principal (Tkinter)
├── config.py           # Configuración y constantes visuales
├── requirements.txt    # Dependencias del proyecto (opcional)
├── LICENSE             # Licencia MIT
└── README.md           # Este archivo
```

## Cambios recientes

- Migración completa a Tkinter y ttk para una experiencia visual moderna y multiplataforma
- Mejoras en la visualización del árbol de directorios y el área de log
- Mensajes de log codificados por color (info, éxito, advertencia, error)
- Mejoras en la organización y el diseño responsivo de la interfaz

## Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor y Contacto

Evan Joao - [evanjoaogarciamunoz@gmail.com](mailto:evanjoaogarciamunoz@gmail.com)

Link del Proyecto: [https://github.com/evanjoao/organizador-archivos](https://github.com/evanjoao/organizador-archivos)
