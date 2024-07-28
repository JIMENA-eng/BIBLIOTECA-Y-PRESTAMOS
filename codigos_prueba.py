import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Crear la base de datos y las tablas si no existen
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

def create_prestamos_db():
    conn = sqlite3.connect('prestamos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni_usuario TEXT NOT NULL,
            codigo_libro TEXT NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            FOREIGN KEY (dni_usuario) REFERENCES users(dni)
        )
    ''')
    conn.commit()
    conn.close()

# Buscar un usuario por DNI
def buscar_usuario_por_dni(dni):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE dni=?", (dni,))
    usuario = c.fetchone()
    conn.close()
    return usuario

# Registrar un préstamo en la base de datos
def registrar_prestamo(dni, codigo_libro):
    conn = sqlite3.connect('prestamos.db')
    c = conn.cursor()
    fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute("INSERT INTO prestamos (dni_usuario, codigo_libro, fecha_prestamo) VALUES (?, ?, ?)",
                  (dni, codigo_libro, fecha_prestamo))
        conn.commit()
        messagebox.showinfo("Éxito", "Préstamo registrado exitosamente.")
    except Exception as e:
        messagebox.showwarning("ADVERTENCIA", f"Error al registrar el préstamo: {e}")
    finally:
        conn.close()

# Mostrar la información del usuario y permitir el préstamo
def mostrar_info_usuario():
    dni = entry_dni.get()
    libro_codigo = entry_codigo_libro.get()
    usuario = buscar_usuario_por_dni(dni)
    
    if usuario:
        ventana_usuario = tk.Toplevel(root)
        ventana_usuario.title("Información del Usuario")
        ventana_usuario.geometry("400x300")

        tk.Label(ventana_usuario, text="Nombre:").pack(pady=5)
        tk.Label(ventana_usuario, text=usuario[1]).pack(pady=5)
        tk.Label(ventana_usuario, text="DNI:").pack(pady=5)
        tk.Label(ventana_usuario, text=usuario[2]).pack(pady=5)
        tk.Label(ventana_usuario, text="Email:").pack(pady=5)
        tk.Label(ventana_usuario, text=usuario[3]).pack(pady=5)
        tk.Label(ventana_usuario, text="Foto:").pack(pady=5)
        tk.Label(ventana_usuario, text=usuario[4] if usuario[4] else "N/A").pack(pady=5)

        tk.Label(ventana_usuario, text="Código del Libro a Prestar:").pack(pady=10)
        tk.Label(ventana_usuario, text=libro_codigo).pack(pady=5)

        def prestar_libro():
            registrar_prestamo(dni, libro_codigo)
            ventana_usuario.destroy()

        tk.Button(ventana_usuario, text="Prestar Libro", command=prestar_libro).pack(pady=10)
    else:
        messagebox.showinfo("Resultado", "No se encontró ningún usuario con el DNI proporcionado.")

# Inicialización de la ventana principal
root = tk.Tk()
root.title("Sistema de Préstamos de Libros")
root.geometry("400x200")

# Creación de los widgets
tk.Label(root, text="DNI del Usuario:").pack(pady=10)
entry_dni = tk.Entry(root)
entry_dni.pack(pady=5)

tk.Label(root, text="Código del Libro:").pack(pady=10)
entry_codigo_libro = tk.Entry(root)
entry_codigo_libro.pack(pady=5)

tk.Button(root, text="Buscar y Prestar", command=mostrar_info_usuario).pack(pady=20)

# Crear las bases de datos y tablas
create_db()
create_prestamos_db()

# Ejecutar la aplicación
root.mainloop()
