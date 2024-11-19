import os
from cryptography.fernet import Fernet
from tkinter import Tk, Text, Menu, filedialog, messagebox, END

# Generar o cargar la clave de encriptación
KEY_FILE = "key.key"

def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

# Inicializamos el cifrador Fernet
fernet = load_or_generate_key()

# Funciones del editor
class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Encriptado")
        self.file_path = None

        # Configuración de la interfaz
        self.text_area = Text(self.root, wrap="word", font=("Arial", 12))
        self.text_area.pack(expand=1, fill="both")
        self._create_menu()

    def _create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        # Menú Archivo
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu.add_cascade(label="Archivo", menu=file_menu)

    # Funciones del menú
    def new_file(self):
        self.text_area.delete(1.0, END)
        self.file_path = None
        self.root.title("Nuevo Archivo - Editor de Texto Encriptado")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos encriptados", "*.enc"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    encrypted_data = file.read()
                    decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, decrypted_data)
                self.file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - Editor de Texto Encriptado")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def save_file(self):
        if self.file_path:
            self._save_to_file(self.file_path)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Archivos encriptados", "*.enc"), ("Todos los archivos", "*.*")])
        if file_path:
            self._save_to_file(file_path)

    def _save_to_file(self, file_path):
        try:
            plain_text = self.text_area.get(1.0, END).strip()
            encrypted_data = fernet.encrypt(plain_text.encode("utf-8"))
            with open(file_path, "wb") as file:
                file.write(encrypted_data)
            self.file_path = file_path
            self.root.title(f"{os.path.basename(file_path)} - Editor de Texto Encriptado")
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Iniciar la aplicación
if __name__ == "__main__":
    root = Tk()
    app = TextEditor(root)
    root.geometry("800x600")
    root.mainloop()
