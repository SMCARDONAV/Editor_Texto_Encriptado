import os
import secrets
from tkinter import Tk, Text, Menu, filedialog, messagebox
from encriptador import Encriptador  # Módulo C++ integrado con pybind11

KEY_FILE = "key.key"

# Generar o cargar clave de encriptación
def cargar_clave():
    """Genera una clave única si no existe y la guarda en un archivo."""
    if not os.path.exists(KEY_FILE):
        clave = secrets.token_bytes(32)  # Generar clave segura de 256 bits
        with open(KEY_FILE, "wb") as f:
            f.write(clave)
    else:
        with open(KEY_FILE, "rb") as f:
            clave = f.read()
    return clave

# Clave global
CLAVE = cargar_clave()

class EditorTexto:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Encriptado")
        self.file_path = None

        # Crear área de texto
        self.text_area = Text(self.root, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<<Modified>>", self.on_modified)

        # Crear barra de menú
        menu = Menu(self.root)
        self.root.config(menu=menu)

        archivo_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Salir", command=self.salir)

    def on_modified(self, event=None):
        """Actualizar título si hay cambios."""
        if self.file_path:
            self.root.title(f"Editor de Texto Encriptado - {os.path.basename(self.file_path)}*")
        else:
            self.root.title("Editor de Texto Encriptado - Nuevo archivo*")
        self.text_area.edit_modified(False)

    def verificar_cambios(self):
        """Verifica si hay cambios no guardados antes de continuar."""
        if self.text_area.edit_modified():
            respuesta = messagebox.askyesnocancel("Guardar cambios", "¿Deseas guardar los cambios antes de continuar?")
            if respuesta:  # Guardar
                self.guardar_archivo()
            elif respuesta is None:  # Cancelar
                return False
        return True

    def nuevo_archivo(self):
        """Limpia el área de texto y resetea la ruta."""
        if self.verificar_cambios():
            self.text_area.delete(1.0, "end")
            self.file_path = None
            self.root.title("Editor de Texto Encriptado - Nuevo archivo")

    def abrir_archivo(self):
        """Abre y desencripta un archivo existente."""
        if not self.verificar_cambios():
            return
        file_path = filedialog.askopenfilename(filetypes=[("Archivos encriptados", "*.enc")])
        if not file_path:
            return
        try:
            encriptador = Encriptador()
            with open(file_path, "rb") as f:
                datos_encriptados = f.read()
            contenido = encriptador.desencriptar(datos_encriptados.decode(), CLAVE.decode())
            self.text_area.delete(1.0, "end")
            self.text_area.insert(1.0, contenido)
            self.file_path = file_path
            self.root.title(f"Editor de Texto Encriptado - {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def guardar_archivo(self):
        """Guarda y encripta el contenido actual."""
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".enc",
                                                          filetypes=[("Archivos encriptados", "*.enc")])
        if not self.file_path:
            return
        try:
            encriptador = Encriptador()
            contenido = self.text_area.get(1.0, "end").strip()
            datos_encriptados = encriptador.encriptar(contenido, CLAVE.decode())
            with open(self.file_path, "wb") as f:
                f.write(datos_encriptados.encode())
            messagebox.showinfo("Guardar", "Archivo guardado exitosamente.")
            self.root.title(f"Editor de Texto Encriptado - {os.path.basename(self.file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def salir(self):
        """Cierra la aplicación."""
        if self.verificar_cambios():
            self.root.quit()

# Inicializar la aplicación
if __name__ == "__main__":
    root = Tk()
    app = EditorTexto(root)
    root.mainloop()
