#!/usr/bin/env python3
"""
Test script para demostrar las funcionalidades de File Organizer
Crea archivos de prueba para testing
"""

import os
import tempfile
from datetime import datetime, timedelta
import random
import json


def create_test_files():
    """Crea archivos de prueba en un directorio temporal"""

    # Crear directorio de prueba
    test_dir = os.path.expanduser("~/test_organizer")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Tipos de archivos para crear
    file_types = {
        "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
        "images": [".jpg", ".png", ".gif", ".bmp", ".svg"],
        "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
        "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "archives": [".zip", ".rar", ".7z", ".tar"],
        "code": [".py", ".js", ".html", ".css", ".json"],
    }

    # Nombres base para archivos
    base_names = [
        "report",
        "document",
        "image",
        "photo",
        "video",
        "movie",
        "song",
        "music",
        "backup",
        "archive",
        "script",
        "code",
        "presentation",
        "spreadsheet",
        "project",
        "data",
    ]

    created_files = []

    print(f"Creando archivos de prueba en: {test_dir}")

    for category, extensions in file_types.items():
        for i in range(3):  # 3 archivos por categoría
            # Seleccionar nombre y extensión aleatoria
            base_name = random.choice(base_names)
            extension = random.choice(extensions)

            # Crear nombre único
            filename = f"{base_name}_{category}_{i+1}{extension}"
            filepath = os.path.join(test_dir, filename)

            # Crear archivo con contenido dummy
            with open(filepath, "w") as f:
                f.write(f"Archivo de prueba: {filename}\n")
                f.write(f"Categoría: {category}\n")
                f.write(f"Creado: {datetime.now()}\n")
                f.write("Contenido de prueba " * 20)  # Contenido para dar tamaño

            # Modificar fecha de algunos archivos para testing de filtros
            if random.choice([True, False]):
                # Cambiar fecha de modificación aleatoria
                days_ago = random.randint(1, 30)
                old_time = datetime.now() - timedelta(days=days_ago)
                timestamp = old_time.timestamp()
                os.utime(filepath, (timestamp, timestamp))

            created_files.append(filepath)

    # Crear algunos archivos adicionales con nombres específicos para testing
    special_files = [
        "importante.pdf",
        "foto_vacaciones.jpg",
        "proyecto_final.py",
        "backup_2024.zip",
        "musica_favorita.mp3",
    ]

    for filename in special_files:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, "w") as f:
            f.write(f"Archivo especial: {filename}\n")
            f.write("Contenido de prueba específico\n")
        created_files.append(filepath)

    print(f"✅ Creados {len(created_files)} archivos de prueba")
    print(f"📁 Directorio: {test_dir}")

    # Mostrar resumen
    print("\n📊 Resumen de archivos creados:")
    file_count = {}
    for filepath in created_files:
        ext = os.path.splitext(filepath)[1].lower()
        file_count[ext] = file_count.get(ext, 0) + 1

    for ext, count in sorted(file_count.items()):
        print(f"   {ext}: {count} archivos")

    print(f"\n🚀 Puedes usar estos archivos para probar File Organizer:")
    print(f"   1. Ejecuta: python app.py")
    print(f"   2. Selecciona el directorio: {test_dir}")
    print(f"   3. Prueba las diferentes funcionalidades")

    return test_dir, created_files


def create_test_config():
    """Crea una configuración de prueba personalizada"""

    test_config = {
        "categories": {
            "Documentos Importantes": [".pdf", ".doc", ".docx"],
            "Fotos Personales": [".jpg", ".jpeg", ".png"],
            "Código Python": [".py", ".pyw"],
            "Archivos de Respaldo": [".zip", ".rar", ".7z", ".tar"],
            "Multimedia": [".mp4", ".mp3", ".avi", ".wav"],
        }
    }

    config_path = os.path.expanduser("~/test_organizer/test_settings.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)

    print(f"📋 Configuración de prueba creada: {config_path}")
    return config_path


if __name__ == "__main__":
    print("🧪 File Organizer - Script de Prueba")
    print("=" * 50)

    try:
        # Crear archivos de prueba
        test_dir, files = create_test_files()

        # Crear configuración de prueba
        config_path = create_test_config()

        print("\n✨ ¡Todo listo para probar File Organizer!")
        print("\n📝 Sugerencias de prueba:")
        print("   • Usa Settings para crear categorías personalizadas")
        print("   • Aplica filtros por tamaño (archivos pequeños/grandes)")
        print("   • Filtra por fecha (archivos recientes/antiguos)")
        print("   • Usa Preview para ver cambios antes de aplicar")
        print("   • Prueba el sistema Undo después de organizar")
        print("   • Revisa Statistics para ver la distribución")

    except Exception as e:
        print(f"❌ Error: {e}")
