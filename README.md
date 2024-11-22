## Video de Sustentación
**[Video en DRIVE](https://drive.google.com/file/d/1CTIwFtoR6vd6ellOqxm2x5oW6lLBoJ9H/view?usp=sharing)**

---

# Editor de texto encriptado

Este proyecto es un editor de texto que permite la creación, edición, y visualización de archivos de texto plano encriptados. Los archivos se guardan encriptados para proteger su contenido, y se desencriptan automáticamente al abrirlos en el editor. Utiliza Python como controlador principal y C++ para manejar la encriptación/desencriptación de forma eficiente. El editor incluye una interfaz gráfica construida con Tkinter.

---

## Características

- **Encriptación y Desencriptación**:
- Los archivos se guardan encriptados utilizando el algoritmo de AES en C++.
- La desencriptación ocurre automáticamente al abrir los archivos desde el editor.
- La clave de encriptación se guarda en un archivo seguro (key.key).

- **Interfaz gráfica**:
  - Construida con `Tkinter`, permitiendo una experiencia interactiva y amigable para el usuario.

- **Funciones básicas del editor**:
  1. Crear archivos nuevos.
  2. Abrir archivos existentes (desencriptándolos automáticamente).
  3. Editar el contenido del archivo.
  4. Guardar cambios encriptando automáticamente el contenido.

- **Gestión de claves de encriptación**:
  - Se genera una clave única en el archivo `key.key`.
  - La clave es ignorada por Git mediante un `.gitignore` para evitar subidas accidentales al repositorio.

## Tecnologías utilizadas

- **Python 3.8+:** Para la lógica principal y la interfaz gráfica.
- **Tkinter:** Para construir la interfaz gráfica del editor.
- **Pybind11:** Para integrar funciones en C++ con Python.
- **OpenSSL:** Se utiliza esta biblioteca para realizar la encriptación y desencriptación.


## Requisitos previos

1. **Python**: Python 3.8 o superior instalado en tu máquina.
2. **Dependencias**: Instala las librerías:
  ```bash
  pip install cryptography pybind11
  ```
3. Instalar herramientas y dependencias de C++:   

**En Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get update   
  sudo apt-get install build-essential cmake libcrypto++-dev python3-dev
  ```


**En MacOS:**
  ```bash
  brew install cmake cryptopp pybind11
  ```

  ## Compilar el módulo de C++:
  ```bash
  mkdir build
  cd build
  cmake ../cpp
  make
  ```

## Ejecución del programa
Ejecuta el archivo principal:   
```python
python text_editor.py
```
## Uso del editor
**Crear archivo nuevo:** Ir a Archivo > Nuevo.   
**Abrir archivo:** Ir a Archivo > Abrir y seleccionar un archivo encriptado. El contenido será desencriptado automáticamente.   
**Guardar archivo:** Ir a Archivo > Guardar para guardar los cambios y encriptar el archivo.

#### Atajos de teclado

| Acción   | Atajo de Teclado |
|----------|------------------|
| Crear    | Ctrl + N         |
| Abrir    | Ctrl + O         |
| Guardar  | Ctrl + S         |
| Salir    | Esc              |




