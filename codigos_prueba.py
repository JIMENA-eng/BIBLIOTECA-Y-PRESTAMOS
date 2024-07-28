import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Crear la base de datos y las tablas si no existen
def create_db():
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS libro (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            TITULO TEXT NOT NULL,
            AUTOR TEXT NOT NULL,
            CODIGO TEXT NOT NULL,
            DESCRIPCION TEXT,
            SECTOR TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Función para buscar libros por sector y/o título
def buscar_libros(sector, titulo_similar):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    
    if sector == "Todos":
        query = "SELECT * FROM libro WHERE TITULO LIKE ?"
        params = (f"%{titulo_similar}%",)
    else:
        query = "SELECT * FROM libro WHERE SECTOR=? AND TITULO LIKE ?"
        params = (sector, f"%{titulo_similar}%")
    
    c.execute(query, params)
    libros = c.fetchall()
    conn.close()
    return libros

# Mostrar la información del libro seleccionado
def mostrar_info_libro(id_libro):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute("SELECT * FROM libro WHERE ID=?", (id_libro,))
    libro = c.fetchone()
    conn.close()

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
    else:
        messagebox.showinfo("Resultado", "No se encontró el libro con el ID proporcionado.")

# Función para mostrar los libros en la tabla según el sector seleccionado y el título buscado
def mostrar_libros():
    sector = combo_sector.get()
    titulo_similar = entry_buscar.get()
    
    if sector == "Seleccionar":
        sector = "Todos"
    
    libros = buscar_libros(sector, titulo_similar)
    for item in tree.get_children():
        tree.delete(item)
    
    for libro in libros:
        tree.insert("", "end", iid=libro[0], values=(libro[1], libro[2], libro[3]))

# Manejar el doble clic en la tabla para mostrar información del libro
def seleccionar_libro(event):
    if tree.selection():
        item = tree.selection()[0]
        id_libro = tree.item(item, "iid")
        mostrar_info_libro(id_libro)

# Inicialización de la ventana principal
root = tk.Tk()
root.title("Sistema de Libros")
root.geometry("600x400")

# Crear los widgets
tk.Label(root, text="Seleccionar Sector:").pack(pady=10)
combo_sector = tk.StringVar(value="Seleccionar")
combo = ttk.Combobox(root, textvariable=combo_sector, values=["Seleccionar", "SOCIALES", "INGENIERIA", "HUMANIDADES"])
combo.pack(pady=5)
combo.set("Seleccionar")

tk.Label(root, text="Buscar por Título:").pack(pady=10)
entry_buscar = tk.Entry(root)
entry_buscar.pack(pady=5)

tk.Button(root, text="Mostrar Libros", command=mostrar_libros).pack(pady=20)

# Crear la tabla para mostrar los libros
tree = ttk.Treeview(root, columns=("Título", "Autor", "Código"), show="headings")
tree.heading("Título", text="Título")
tree.heading("Autor", text="Autor")
tree.heading("Código", text="Código")
tree.pack(fill=tk.BOTH, expand=True)

# Configurar el doble clic en la tabla
tree.bind("<Double-1>", seleccionar_libro)

# Crear la base de datos y tabla
create_db()

# Ejecutar la aplicación
root.mainloop()
