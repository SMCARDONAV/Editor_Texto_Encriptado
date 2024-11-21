import os
import secrets
from tkinter import Tk, Text, Menu, filedialog, messagebox
from encriptador import Encriptador

KEY_FILE = "key.key"

def cargar_clave():
    if not os.path.exists(KEY_FILE):
        clave = secrets.token_bytes(32)
        with open(KEY_FILE, "wb") as f:
            f.write(clave)
    else:
        with open(KEY_FILE, "rb") as f:
            clave = f.read()
    if len(clave) != 32:
        raise ValueError("La clave debe tener exactamente 32 bytes.")
    return clave

CLAVE = cargar_clave()

class EditorTexto:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Encriptado")
        self.file_path = None
        self.text_area = Text(self.root, wrap="word", undo=True)
        self.text_area.pack(expand=True, fill="both")

        menu = Menu(self.root)
        self.root.config(menu=menu)
        archivo_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Salir", command=self.salir)

    def nuevo_archivo(self):
        self.text_area.delete(1.0, "end")
        self.file_path = None

    def abrir_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos encriptados", "*.enc")])
        if file_path:
            encriptador = Encriptador()
            with open(file_path, "rb") as f:
                datos = f.read()
            texto = encriptador.desencriptar(list(datos), CLAVE.decode())
            self.text_area.delete(1.0, "end")
            self.text_area.insert(1.0, texto)
            self.file_path = file_path

    def guardar_archivo(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".enc",
                                                          filetypes=[("Archivos encriptados", "*.enc")])
        if self.file_path:
            encriptador = Encriptador()
            contenido = self.text_area.get(1.0, "end").strip()
            datos = encriptador.encriptar(contenido, CLAVE.decode())
            with open(self.file_path, "wb") as f:
                f.write(bytes(datos))

    def salir(self):
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    app = EditorTexto(root)
    root.mainloop()
