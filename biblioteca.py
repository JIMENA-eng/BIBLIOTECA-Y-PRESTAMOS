import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import os
import random
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
import sqlite3
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
   # Inicialización de la ventana principal
    root = tk.Tk()
    root.title("Aplicación CRUD con Base de Datos")
    root.geometry("700x400")

    # Variables para el CRUD
    miId = tk.StringVar()
    miTitulo = tk.StringVar()
    miAutor = tk.StringVar()
    miCodigo = tk.StringVar()
    miDescripcion = tk.StringVar()
    miSector = tk.StringVar()

    # Función para conectar y crear la base de datos
    def conexionBBDD():
        miConexion = sqlite3.connect("base.db")
        miCursor = miConexion.cursor()
        try:
            miCursor.execute('''
                CREATE TABLE IF NOT EXISTS libro (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITULO TEXT NOT NULL,
                AUTOR TEXT NOT NULL,
                CODIGO TEXT NOT NULL,
                DESCRIPCION TEXT,
                SECTOR TEXT NOT NULL)
                ''')
            messagebox.showinfo("CONEXIÓN", "Base de Datos Creada exitosamente")
        except Exception as e:
            messagebox.showinfo("CONEXIÓN", f"Error al crear la base de datos: {e}")
        finally:
            miConexion.close()

    # Función para eliminar la base de datos
    def eliminarBBDD():
        miConexion = sqlite3.connect("base.db")
        miCursor = miConexion.cursor()
        if messagebox.askyesno(message="¿Los Datos se perderán definitivamente, desea continuar?", title="ADVERTENCIA"):
            miCursor.execute("DROP TABLE IF EXISTS libro")
        miConexion.commit()
        miConexion.close()
        limpiarCampos()
        mostrar()

    # Función para salir de la aplicación
    def salirAplicacion():
        if messagebox.askquestion("Salir", "¿Está seguro que desea salir de la Aplicación?") == "yes":
            root.destroy()

    # Función para limpiar los campos de entrada
    def limpiarCampos():
        miId.set("")
        miTitulo.set("")
        miAutor.set("")
        miCodigo.set("")
        miDescripcion.set("")
        miSector.set("")

    # Función para mostrar información sobre la aplicación
    def mensaje():
        acerca = '''
        Aplicación CRUD
        Versión 1.0
        Tecnología Python Tkinter
        '''
        messagebox.showinfo(title="INFORMACIÓN", message=acerca)

    # Función para crear un nuevo registro
    def crear():
        miConexion = sqlite3.connect("base.db")
        miCursor = miConexion.cursor()
        try:
            datos = (miTitulo.get(), miAutor.get(), miCodigo.get(), miDescripcion.get(), miSector.get())
            miCursor.execute("INSERT INTO libro (TITULO, AUTOR, CODIGO, DESCRIPCION, SECTOR) VALUES (?, ?, ?, ?, ?)", datos)
            miConexion.commit()
        except Exception as e:
            messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al crear el registro: {e}")
        finally:
            miConexion.close()
        limpiarCampos()
        mostrar()

    # Función para mostrar los registros en la tabla
    def mostrar():
        miConexion = sqlite3.connect("base.db")
        miCursor = miConexion.cursor()
        registros = tree.get_children()
        for elemento in registros:
            tree.delete(elemento)
        try:
            miCursor.execute("SELECT * FROM libro")
            for row in miCursor:
                tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
        except Exception as e:
            messagebox.showwarning("ADVERTENCIA", f"Error al mostrar los registros: {e}")
        finally:
            miConexion.close()

    # Función para seleccionar un registro desde la tabla
    def seleccionarUsandoClick(event):
        item = tree.identify('item', event.x, event.y)
        miId.set(tree.item(item, "text"))
        miTitulo.set(tree.item(item, "values")[0])
        miAutor.set(tree.item(item, "values")[1])
        miCodigo.set(tree.item(item, "values")[2])
        miDescripcion.set(tree.item(item, "values")[3])
        miSector.set(tree.item(item, "values")[4])

    # Creación de la tabla para mostrar los datos
    tree = ttk.Treeview(root, height=10, columns=('#0', '#1', '#2', '#3', '#4'))
    tree.place(x=0, y=130)
    tree.column('#0', width=50)
    tree.heading('#0', text="ID", anchor=tk.CENTER)
    tree.heading('#1', text="Título", anchor=tk.CENTER)
    tree.heading('#2', text="Autor", anchor=tk.CENTER)
    tree.heading('#3', text="Código", anchor=tk.CENTER)
    tree.heading('#4', text="Descripción", anchor=tk.CENTER)
    tree.heading('#5', text="Sector", anchor=tk.CENTER)
    tree.column('#5', width=100)

    # Vinculación del evento para seleccionar un registro
    tree.bind("<Double-1>", seleccionarUsandoClick)

    # Función para actualizar un registro
    def actualizar():
        miConexion = sqlite3.connect("base.db")
        miCursor = miConexion.cursor()
        try:
            datos = (miTitulo.get(), miAutor.get(), miCodigo.get(), miDescripcion.get(), miSector.get(), miId.get())
            miCursor.execute("UPDATE libro SET TITULO=?, AUTOR=?, CODIGO=?, DESCRIPCION=?, SECTOR=? WHERE ID=?", datos)
            miConexion.commit()
        except Exception as e:
            messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al actualizar el registro: {e}")
        finally:
            miConexion.close()
        limpiarCampos()
        mostrar()

    # Función para borrar un registro
    def borrar():
        miConexion = sqlite3.connect("base.db")
        miCursor = miConexion.cursor()
        try:
            if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
                miCursor.execute("DELETE FROM libro WHERE ID=?", (miId.get(),))
                miConexion.commit()
        except Exception as e:
            messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al eliminar el registro: {e}")
        finally:
            miConexion.close()
        limpiarCampos()
        mostrar()

    # Creación de los menús
    menubar = tk.Menu(root)
    menubasedat = tk.Menu(menubar, tearoff=0)
    menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
    menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
    menubasedat.add_command(label="Salir", command=salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu = tk.Menu(menubar, tearoff=0)
    ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda", menu=ayudamenu)

    # Creación de etiquetas y cajas de texto
    l1 = tk.Label(root, text="ID")
    l1.place(x=50, y=10)
    e1 = tk.Entry(root, textvariable=miId, state='readonly')
    e1.place(x=100, y=10)

    l2 = tk.Label(root, text="Título")
    l2.place(x=50, y=40)
    e2 = tk.Entry(root, textvariable=miTitulo, width=50)
    e2.place(x=100, y=40)

    l3 = tk.Label(root, text="Autor")
    l3.place(x=50, y=70)
    e3 = tk.Entry(root, textvariable=miAutor)
    e3.place(x=100, y=70)

    l4 = tk.Label(root, text="Código")
    l4.place(x=50, y=100)
    e4 = tk.Entry(root, textvariable=miCodigo)
    e4.place(x=100, y=100)

    l5 = tk.Label(root, text="Descripción")
    l5.place(x=50, y=130)
    e5 = tk.Entry(root, textvariable=miDescripcion, width=50)
    e5.place(x=100, y=130)

    l6 = tk.Label(root, text="Sector")
    l6.place(x=50, y=160)
    e6 = tk.Entry(root, textvariable=miSector)
    e6.place(x=100, y=160)

    # Creación de botones
    b1 = tk.Button(root, text="Crear Registro", command=crear)
    b1.place(x=50, y=200)
    b2 = tk.Button(root, text="Modificar Registro", command=actualizar)
    b2.place(x=180, y=200)
    b3 = tk.Button(root, text="Mostrar Lista", command=mostrar)
    b3.place(x=320, y=200)
    b4 = tk.Button(root, text="Eliminar Registro", bg="red", command=borrar)
    b4.place(x=450, y=200)

    root.config(menu=menubar)
    root.mainloop()


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
