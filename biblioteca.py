import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import os
import random
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
import string

def iniciar_sesion_admin():
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    root = tk.Tk()
    root.title('Inicio de sesión como Administrador')

    # Etiquetas y entradas para usuario y contraseña
    label_usuario = tk.Label(root, text='Usuario:')
    label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    label_contrasena = tk.Label(root, text='Contraseña:')
    label_contrasena.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entry_contrasena = tk.Entry(root, show='*')
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    # Función para verificar el inicio de sesión como administrador
    def verificar_admin():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        # Validar usuario y contraseña
        if usuario == 'admin' and contrasena == 'admin123':
            root.destroy()  # Cerrar la ventana de inicio de sesión
            ventana_administrador()  # Función para abrir ventana de administrador
        else:
            messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')

    # Botón para iniciar sesión como administrador
    btn_iniciar_sesion = tk.Button(root, text='Iniciar sesión', command=verificar_admin)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def iniciar_sesion_asistente():
    def crear_tabla():
        """Crea la tabla de asistentes si no existe."""
        conn = sqlite3.connect('asistentes.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def generar_contrasena():
        """Genera una contraseña única de 6 dígitos."""
        return ''.join(random.choices(string.digits, k=6))

    def registrar_asistente(nombre, correo):
        """Registra al asistente en la base de datos con la contraseña generada."""
        contrasena = generar_contrasena()
        
        conn = sqlite3.connect('asistentes.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO asistentes (nombre, correo, contrasena) VALUES (?, ?, ?)
            ''', (nombre, correo, contrasena))
            conn.commit()
            return contrasena
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def iniciar_sesion(contrasena):
        """Permite al asistente iniciar sesión si la contraseña es correcta."""
        conn = sqlite3.connect('asistentes.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM asistentes WHERE contrasena = ?
        ''', (contrasena,))
        asistente = cursor.fetchone()
        conn.close()
        
        if asistente:
            return asistente
        else:
            return None

    # Funciones para las ventanas
    def mostrar_ventana_inicio():
        """Muestra la ventana de inicio de sesión."""
        ventana_inicio = tk.Tk()
        ventana_inicio.title("Inicio de Sesión")
        
        tk.Label(ventana_inicio, text="Introduce tu contraseña:").pack(pady=10)
        entry_contrasena = tk.Entry(ventana_inicio, show='*', width=40)
        entry_contrasena.pack(pady=5)

        def verificar_contrasena():
            contrasena = entry_contrasena.get()
            asistente = iniciar_sesion(contrasena)
            if asistente:
                messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
                ventana_inicio.destroy()  # Cerrar la ventana de inicio de sesión
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        
        boton_ingresar = tk.Button(ventana_inicio, text="Ingresar", command=verificar_contrasena)
        boton_ingresar.pack(pady=20)
        
        ventana_inicio.mainloop()

    def registrar():
        """Función llamada cuando el usuario hace clic en el botón de registro."""
        nombre = entry_nombre.get()
        correo = entry_correo.get()
        
        if not correo.endswith('@unap.edu.pe'):
            messagebox.showerror("Error", "El correo electrónico debe terminar en '@unap.edu.pe'.")
            return
        
        contrasena = registrar_asistente(nombre, correo)
        
        if contrasena:
            messagebox.showinfo("Éxito", f"Registro completado con éxito!\nContraseña generada: {contrasena}")
            ventana_registro.destroy()  # Cerrar la ventana de registro
            mostrar_ventana_inicio()  # Mostrar ventana de inicio de sesión
        else:
            messagebox.showerror("Error", "El correo electrónico ya está registrado.")

    # Configuración de la interfaz gráfica para el registro
    def configurar_gui():
        """Configura la interfaz gráfica de usuario con tkinter."""
        global ventana_registro
        ventana_registro = tk.Tk()
        ventana_registro.title("Registro de Asistente")

        tk.Label(ventana_registro, text="Nombre Completo:").pack(pady=5)
        global entry_nombre
        entry_nombre = tk.Entry(ventana_registro, width=40)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_registro, text="Correo Institucional:").pack(pady=5)
        global entry_correo
        entry_correo = tk.Entry(ventana_registro, width=40)
        entry_correo.pack(pady=5)

        boton_registrar = tk.Button(ventana_registro, text="Registrar", command=registrar)
        boton_registrar.pack(pady=20)

        ventana_registro.mainloop()

    # Ejecutar la aplicación
    if __name__ == "__main__":
        crear_tabla()
        configurar_gui()

def iniciar_sesion_usuario():
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

    # Función para generar una contraseña única de 4 dígitos
    def generate_password():
        return f"{random.randint(1000, 9999)}"

    # Registrar un nuevo usuario
    def register_user(name, dni, email, photo_path, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # Insertar datos en la base de datos
        c.execute('''
            INSERT INTO users (name, dni, email, photo_path, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, dni, email, photo_path, hash_password(password)))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Registro Exitoso", f"Usuario registrado con DNI {dni}.\nContraseña única generada: {password}")

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

            # Mostrar la foto en la GUI
            image = Image.open(filename)
            image.thumbnail((200, 200))  # Redimensionar la imagen para que quepa en la interfaz
            photo_image = ImageTk.PhotoImage(image)

            # Actualizar el Label con la imagen
            global photo_label
            if 'photo_label' in globals():
                photo_label.config(image=photo_image)
                photo_label.image = photo_image
            else:
                photo_label = Label(root, image=photo_image)
                photo_label.grid(row=4, column=1, padx=10, pady=10)

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

        password = generate_password()

        # Copiar la foto al directorio de fotos
        if not os.path.exists('photos'):
            os.makedirs('photos')
        photo_dest = os.path.join('photos', os.path.basename(photo))
        Image.open(photo).save(photo_dest)
        
        register_user(name, dni, email, photo_dest, password)

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
        global entry_dni_login, entry_password_login, root
        
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

        Button(root, text="Registrar", command=register).grid(row=5, column=1, pady=10)

        # Inicio de sesión
        Label(root, text="DNI").grid(row=6, column=0, padx=10, pady=10)
        entry_dni_login = Entry(root)
        entry_dni_login.grid(row=6, column=1, padx=10, pady=10)

        Label(root, text="Contraseña").grid(row=7, column=0, padx=10, pady=10)
        entry_password_login = Entry(root, show="*")
        entry_password_login.grid(row=7, column=1, padx=10, pady=10)

        Button(root, text="Iniciar Sesión", command=login).grid(row=8, column=1, pady=10)

        root.mainloop()

    if __name__ == "__main__":
        create_db()
        setup_gui()
        
        
def ventana_administrador():
    # Aquí se define la ventana principal para el administrador
    pass

def ventana_asistente():
    # Aquí se define la ventana principal para el asistente
    pass

def ventana_usuario():
    # Aquí se define la ventana principal para el usuario
    pass

# Crear la ventana principal para seleccionar tipo de usuario
top = tk.Tk()
top.title('Seleccionar tipo de usuario')

# Botones para seleccionar tipo de usuario
btn_admin = tk.Button(top, text='Iniciar sesión como Administrador', command=iniciar_sesion_admin)
btn_admin.pack(pady=20)

btn_asistente = tk.Button(top, text='Iniciar sesión como Asistente', command=iniciar_sesion_asistente)
btn_asistente.pack(pady=20)

btn_usuario = tk.Button(top, text='Iniciar sesión como Usuario', command=iniciar_sesion_usuario)
btn_usuario.pack(pady=20)

top.mainloop()
