import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

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
