import sqlite3
import random
import string
import tkinter as tk
from tkinter import messagebox

# Configuración de la base de datos SQLite
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
