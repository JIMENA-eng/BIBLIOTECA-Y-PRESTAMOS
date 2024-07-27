import tkinter as tk
from tkinter import messagebox

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
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    root = tk.Tk()
    root.title('Inicio de sesión como Asistente')

    # Etiquetas y entradas para usuario y contraseña
    label_usuario = tk.Label(root, text='Usuario:')
    label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    label_contrasena = tk.Label(root, text='Contraseña:')
    label_contrasena.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entry_contrasena = tk.Entry(root, show='*')
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    # Función para verificar el inicio de sesión como asistente
    def verificar_asistente():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        # Validar usuario y contraseña
        if usuario == 'asistente' and contrasena == 'asistente123':
            root.destroy()  # Cerrar la ventana de inicio de sesión
            ventana_asistente()  # Función para abrir ventana de asistente
        else:
            messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')

    # Botón para iniciar sesión como asistente
    btn_iniciar_sesion = tk.Button(root, text='Iniciar sesión', command=verificar_asistente)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def iniciar_sesion_usuario():
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    root = tk.Tk()
    root.title('Inicio de sesión como Usuario')

    # Etiquetas y entradas para usuario y contraseña
    label_usuario = tk.Label(root, text='Usuario:')
    label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    label_contrasena = tk.Label(root, text='Contraseña:')
    label_contrasena.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entry_contrasena = tk.Entry(root, show='*')
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    # Función para verificar el inicio de sesión como usuario
    def verificar_usuario():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        # Validar usuario y contraseña
        if usuario == 'usuario' and contrasena == 'usuario123':
            root.destroy()  # Cerrar la ventana de inicio de sesión
            ventana_usuario()  # Función para abrir ventana de usuario
        else:
            messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')

    # Botón para iniciar sesión como usuario
    btn_iniciar_sesion = tk.Button(root, text='Iniciar sesión', command=verificar_usuario)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

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
