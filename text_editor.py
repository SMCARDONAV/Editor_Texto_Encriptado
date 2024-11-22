import os
import secrets
import base64
from tkinter import Tk, Text, Menu, filedialog, messagebox
from build.encriptador import Encriptador

KEY_FILE = "key.key"

def cargar_clave():
    if not os.path.exists(KEY_FILE):
        clave = secrets.token_bytes(32)
        clave_base64 = base64.b64encode(clave).decode("utf-8")
        with open(KEY_FILE, "w") as f:
            f.write(clave_base64)
    else:
        with open(KEY_FILE, "r") as f:
            clave_base64 = f.read()
        clave = base64.b64decode(clave_base64)
    if len(clave) != 32:
        raise ValueError("La clave debe tener exactamente 32 bytes.")
    return clave

# Clave global
try:
    CLAVE = cargar_clave()
except Exception as e:
    messagebox.showerror("Error Crítico", f"No se pudo cargar la clave de encriptación: {e}")
    exit(1)

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
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo, accelerator="Ctrl+N")
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo, accelerator="Ctrl+O")
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo, accelerator="Ctrl+s")
        archivo_menu.add_command(label="Salir", command=self.salir, accelerator="Esc")
        
        # Vincular atajos de teclado
        self.root.bind("<Control-n>", lambda event: self.nuevo_archivo())
        self.root.bind("<Control-o>", lambda event: self.abrir_archivo())
        self.root.bind("<Control-s>", lambda event: self.guardar_archivo())
        self.root.bind("<Escape>", lambda event: self.salir())

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
            contenido = encriptador.desencriptar(list(datos_encriptados), CLAVE)
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
            datos_encriptados = encriptador.encriptar(contenido, CLAVE)
            with open(self.file_path, "wb") as f:
                f.write(bytes(datos_encriptados))  # Asegura la escritura como binario
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