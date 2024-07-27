import sqlite3
import hashlib
import os
from PIL import Image
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox

# Crear una conexión con la base de datos SQLite
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            photo_path TEXT,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para generar un hash de la contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para verificar la contraseña
def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

# Registrar un nuevo usuario
def register_user(name, dni, email, photo_path):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Generar un hash de la contraseña
    password = hash_password(dni)  # Usar el DNI como contraseña por simplicidad
    
    # Insertar datos en la base de datos
    c.execute('''
        INSERT INTO users (name, dni, email, photo_path, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, dni, email, photo_path, password))
    
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Registro Exitoso", f"Usuario registrado con DNI {dni} y contraseña única generada.")

# Autenticar usuario
def authenticate_user(dni, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT password FROM users WHERE dni = ?', (dni,))
    result = c.fetchone()
    
    conn.close()
    
    if result:
        stored_password = result[0]
        return verify_password(stored_password, password)
    return False

# Funciones para la GUI
def browse_photo():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if filename:
        photo_path_entry.delete(0, 'end')  # Limpiar el contenido actual
        photo_path_entry.insert(0, filename)  # Insertar la nueva ruta de la foto

def register():
    name = entry_name.get()
    dni = entry_dni.get()
    email = entry_email.get()
    photo = photo_path_entry.get()

    if not name or not dni or not email or not photo:
        messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
        return
    
    if not os.path.isfile(photo):
        messagebox.showerror("Archivo No Encontrado", "El archivo de la foto no existe.")
        return

    # Copiar la foto al directorio de fotos
    if not os.path.exists('photos'):
        os.makedirs('photos')
    photo_dest = os.path.join('photos', os.path.basename(photo))
    Image.open(photo).save(photo_dest)
    
    register_user(name, dni, email, photo_dest)

def login():
    dni = entry_dni_login.get()
    password = entry_password_login.get()
    
    if authenticate_user(dni, password):
        messagebox.showinfo("Inicio de Sesión Exitoso", "¡Autenticación exitosa!")
    else:
        messagebox.showerror("Error de Inicio de Sesión", "DNI o contraseña incorrectos.")

# Configuración de la GUI
def setup_gui():
    global entry_name, entry_dni, entry_email, photo_path_entry
    global entry_dni_login, entry_password_login
    
    root = Tk()
    root.title("Registro e Inicio de Sesión")

    # Registro
    Label(root, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
    entry_name = Entry(root)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="DNI").grid(row=1, column=0, padx=10, pady=10)
    entry_dni = Entry(root)
    entry_dni.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Email").grid(row=2, column=0, padx=10, pady=10)
    entry_email = Entry(root)
    entry_email.grid(row=2, column=1, padx=10, pady=10)

    Label(root, text="Foto").grid(row=3, column=0, padx=10, pady=10)
    photo_path_entry = Entry(root)
    photo_path_entry.grid(row=3, column=1, padx=10, pady=10)
    Button(root, text="Buscar Foto", command=browse_photo).grid(row=3, column=2, padx=10, pady=10)

    Button(root, text="Registrar", command=register).grid(row=4, column=1, pady=10)

    # Inicio de sesión
    Label(root, text="DNI").grid(row=5, column=0, padx=10, pady=10)
    entry_dni_login = Entry(root)
    entry_dni_login.grid(row=5, column=1, padx=10, pady=10)

    Label(root, text="Contraseña").grid(row=6, column=0, padx=10, pady=10)
    entry_password_login = Entry(root, show="*")
    entry_password_login.grid(row=6, column=1, padx=10, pady=10)

    Button(root, text="Iniciar Sesión", command=login).grid(row=7, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_db()
    setup_gui()
