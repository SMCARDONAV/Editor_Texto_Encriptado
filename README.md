# Editor de texto encriptado

Este proyecto es un editor de texto que permite la creación, edición, y visualización de archivos de texto plano encriptados. Los archivos se guardan encriptados para proteger su contenido, y se desencriptan automáticamente al abrirlos en el editor. El editor utiliza una interfaz gráfica simple y soporta operaciones básicas como crear, abrir, editar y guardar archivos.

---

## Características

- **Encriptación y Desencriptación**:
  - Los archivos se guardan encriptados utilizando la librería `cryptography` y el método **Fernet**.
  - Los archivos son desencriptados automáticamente al abrirlos desde el editor.

- **Interfaz gráfica**:
  - Construida con `Tkinter`, permitiendo una experiencia interactiva y amigable para el usuario.

- **Funciones básicas del editor**:
  - Crear archivos nuevos.
  - Abrir archivos existentes (desencriptándolos automáticamente).
  - Editar texto.
  - Guardar archivos (encriptándolos).

- **Gestión de claves de encriptación**:
  - Se genera una clave única en el archivo `key.key`.
  - La clave es ignorada por Git mediante un `.gitignore` para evitar subidas accidentales al repositorio.

## Tecnologías utilizadas

- **Python 3.8+**
- **Tkinter**: Para la interfaz gráfica del editor.
- **Cryptography**: Para la encriptación y desencriptación de los archivos.

## Requisitos previos

1. **Python**: Python 3.8 o superior instalado en tu máquina.
2. **Dependencias**: Instala la librería:
   **pip install cryptography**

## Ejecución del programa
Ejecuta el archivo principal: **python text_editor.py**

## Uso del editor
- Crear archivo nuevo: Ir a Archivo > Nuevo.
- Abrir archivo: Ir a Archivo > Abrir y selecciona un archivo encriptado. El contenido se desencriptará automáticamente.
- Guardar archivo: Ir a Archivo > Guardar como para guardar los cambios, encriptando el archivo en el proceso.

