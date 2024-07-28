import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Función para conectar a la base de datos de libros y crear la tabla
def conexionBBDD_libros():
    miConexion = sqlite3.connect("base.db")
    miCursor = miConexion.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS libro (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TITULO TEXT NOT NULL,
            AUTOR TEXT NOT NULL,
            CODIGO TEXT NOT NULL UNIQUE,
            DESCRIPCION TEXT,
            SECTOR TEXT NOT NULL)
            ''')
        miConexion.commit()
    except Exception as e:
        messagebox.showinfo("CONEXIÓN LIBROS", f"Error al conectar a la base de datos de libros: {e}")
    finally:
        miConexion.close()

# Función para conectar a la base de datos de préstamos y crear la tabla
def conexionBBDD_prestamos():
    miConexion = sqlite3.connect("prestamos.db")
    miCursor = miConexion.cursor()
    try:
        miCursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamo (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CODIGO_LIBRO TEXT NOT NULL,
            FECHA_PRESTAMO TEXT NOT NULL,
            ESTADO TEXT NOT NULL,
            FOREIGN KEY (CODIGO_LIBRO) REFERENCES libro(CODIGO))
            ''')
        miConexion.commit()
    except Exception as e:
        messagebox.showinfo("CONEXIÓN PRESTAMOS", f"Error al conectar a la base de datos de préstamos: {e}")
    finally:
        miConexion.close()

# Función para mostrar la ventana con la información del libro
def mostrar_informacion_libro(codigo):
    miConexion = sqlite3.connect("base.db")
    miCursor = miConexion.cursor()
    miCursor.execute("SELECT * FROM libro WHERE CODIGO=?", (codigo,))
    libro = miCursor.fetchone()
    miConexion.close()

    if libro:
        ventana_libro = tk.Toplevel(root)
        ventana_libro.title("Información del Libro")
        ventana_libro.geometry("400x300")

        tk.Label(ventana_libro, text="Título:").pack(pady=5)
        tk.Label(ventana_libro, text=libro[1]).pack(pady=5)
        tk.Label(ventana_libro, text="Autor:").pack(pady=5)
        tk.Label(ventana_libro, text=libro[2]).pack(pady=5)
        tk.Label(ventana_libro, text="Código:").pack(pady=5)
        tk.Label(ventana_libro, text=libro[3]).pack(pady=5)
        tk.Label(ventana_libro, text="Descripción:").pack(pady=5)
        tk.Label(ventana_libro, text=libro[4] if libro[4] else "N/A").pack(pady=5)
        tk.Label(ventana_libro, text="Sector:").pack(pady=5)
        tk.Label(ventana_libro, text=libro[5]).pack(pady=5)

        def prestar_libro():
            miConexion = sqlite3.connect("prestamos.db")
            miCursor = miConexion.cursor()
            fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                miCursor.execute("INSERT INTO prestamo (CODIGO_LIBRO, FECHA_PRESTAMO, ESTADO) VALUES (?, ?, ?)",
                                 (codigo, fecha_prestamo, "Prestado"))
                miConexion.commit()
                messagebox.showinfo("Éxito", "El libro ha sido prestado.")
            except Exception as e:
                messagebox.showwarning("ADVERTENCIA", f"Error al registrar el préstamo: {e}")
            finally:
                miConexion.close()
                ventana_libro.destroy()

        tk.Button(ventana_libro, text="Prestar", command=prestar_libro).pack(pady=10)

# Función para buscar libros por código y mostrar resultados
def buscar_libros():
    codigo = entry_codigo.get()
    miConexion = sqlite3.connect("base.db")
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)

    if codigo:
        try:
            miCursor.execute("SELECT * FROM libro WHERE CODIGO=?", (codigo,))
            libro = miCursor.fetchone()
            if libro:
                # Verifica el número de columnas en la tupla libro
                if len(libro) >= 6:
                    tree.insert("", 0, text=libro[0], values=(libro[1], libro[2], libro[3], libro[4], libro[5]))
                else:
                    messagebox.showwarning("ADVERTENCIA", "Datos del libro incompletos.")
            else:
                messagebox.showinfo("Resultado", "No se encontró ningún libro con el código proporcionado.")
        except Exception as e:
            messagebox.showwarning("ADVERTENCIA", f"Error al buscar el libro: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un código para buscar.")

    miConexion.close()

# Función para manejar el doble clic en la tabla
def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    if item:
        codigo = tree.item(item, "values")[2]
        mostrar_informacion_libro(codigo)

# Inicialización de la ventana principal
root = tk.Tk()
root.title("Aplicación de Biblioteca")
root.geometry("800x400")

# Definición de la tabla para mostrar los resultados
tree = ttk.Treeview(root, height=10, columns=('#0', '#1', '#2', '#3', '#4'))
tree.place(x=0, y=80)
tree.column('#0', width=50)
tree.heading('#0', text="ID", anchor=tk.CENTER)
tree.heading('#1', text="Título", anchor=tk.CENTER)
tree.heading('#2', text="Código", anchor=tk.CENTER)
tree.heading('#3', text="Descripción", anchor=tk.CENTER)
tree.heading('#4', text="Sector", anchor=tk.CENTER)

# Vinculación del evento para seleccionar un libro
tree.bind("<Double-1>", seleccionarUsandoClick)

# Creación de los widgets
tk.Label(root, text="Buscar por Código:").pack(pady=10)
entry_codigo = tk.Entry(root)
entry_codigo.pack(pady=5)

tk.Button(root, text="Buscar", command=buscar_libros).pack(pady=10)

# Creación de los menús
menubar = tk.Menu(root)
menubasedat = tk.Menu(menubar, tearoff=0)
menubasedat.add_command(label="Conectar Base de Datos Libros", command=conexionBBDD_libros)
menubasedat.add_command(label="Conectar Base de Datos Prestamos", command=conexionBBDD_prestamos)
menubar.add_cascade(label="Inicio", menu=menubasedat)

root.config(menu=menubar)

# Inicialización de las bases de datos
conexionBBDD_libros()
conexionBBDD_prestamos()

# Ejecutar la aplicación
root.mainloop()
