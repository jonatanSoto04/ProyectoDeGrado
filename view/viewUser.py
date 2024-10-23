import tkinter as tk
from tkinter import messagebox
from model.modelUser import ModeloUsuario
from controller.listController import Controlador
from view.fingerprintView import VistaHuellas

class VistaUsuario:
    def __init__(self, root, parent_window=None):
        self.root = root
        self.parent_window = parent_window
        self.root.title("Agregar Usuario")
        self.root.geometry("1000x800")  # Tamaño de la ventana ajustado
        self.root.configure(bg="#e6f7ff")  # Fondo azul cielo

        # Frame superior con el título
        header_frame = tk.Frame(self.root, bg="#00aaff")  # Fondo azul más oscuro
        header_frame.pack(fill=tk.X)

        # Título dentro del header
        titulo = tk.Label(header_frame, text="Agregar Usuario", font=("Verdana Bold", 20), fg="white", bg="#00aaff")
        titulo.pack(side=tk.LEFT, padx=20, pady=10)

        # Botón para volver a la lista de usuarios
        self.boton_cerrar = tk.Button(header_frame, text="Ver lista", command=self.volver_a_lista, bg="#b3e0ff", fg="white", borderwidth=0, height=2, width=10)
        self.boton_cerrar.pack(side=tk.LEFT, padx=10, pady=10)  # Alineado a la izquierda
        self.boton_cerrar.bind("<Enter>", lambda e: self.boton_cerrar.config(bg="#0080ff", fg="white"))
        self.boton_cerrar.bind("<Leave>", lambda e: self.boton_cerrar.config(bg="#b3e0ff", fg="white"))

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#e6f7ff")
        main_frame.pack(expand=True, fill=tk.BOTH)  # Expandir y llenar el espacio

        # Frame para el formulario y el botón
        form_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RAISED)  # Recuadro para el formulario
        form_frame.pack(pady=20, padx=20, expand=False)  # No expande, solo ocupa el espacio necesario
        form_frame.config(width=600, height=400)  # Ajusta el tamaño del recuadro
        form_frame.place(relx=0.5, rely=0.5, anchor='center')  # Centra el recuadro

        # Título dentro del recuadro
        titulo_formulario = tk.Label(form_frame, text="Agregar Usuario", font=("Verdana Bold", 16), bg="white")
        titulo_formulario.grid(row=0, column=0, pady=10)

        # Crear formulario
        self.crear_formulario(form_frame)

    def crear_formulario(self, frame):
        # Labels e inputs con diseño mejorado
        styles = {
            'bg': 'white',
            'font': ('Verdana', 12)
        }

        # Crear cada label y entrada con un diseño mejorado
        tk.Label(frame, text="Nombre:", **styles).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.entry_nombre = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_nombre.grid(row=2, column=0, padx=20, pady=5)

        tk.Label(frame, text="Correo:", **styles).grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.entry_correo = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_correo.grid(row=4, column=0, padx=20, pady=5)

        tk.Label(frame, text="Número de ID:", **styles).grid(row=5, column=0, padx=20, pady=10, sticky='w')
        self.entry_numero_id = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_numero_id.grid(row=6, column=0, padx=20, pady=5)

        tk.Label(frame, text="Número de Celular:", **styles).grid(row=7, column=0, padx=20, pady=10, sticky='w')
        self.entry_numero_celular = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_numero_celular.grid(row=8, column=0, padx=20, pady=5)

        # Botón para agregar usuario
        self.boton_agregar = tk.Button(frame, text="Agregar Usuario", command=self.agregar_usuario, bg="#00aaff", fg="white", borderwidth=0, height=2, width=15)
        self.boton_agregar.grid(row=9, column=0, pady=20)
        self.boton_agregar.bind("<Enter>", lambda e: self.boton_agregar.config(bg="#66c2ff"))
        self.boton_agregar.bind("<Leave>", lambda e: self.boton_agregar.config(bg="#00aaff"))

    def agregar_usuario(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        numero_id = self.entry_numero_id.get()
        numero_celular = self.entry_numero_celular.get()

        if nombre and correo and numero_id and numero_celular:
            modelo = ModeloUsuario()
            user_id = modelo.agregar_usuario(nombre, correo, numero_id, numero_celular)
            if user_id:
                messagebox.showinfo("Éxito", "Usuario agregado correctamente")
                self.entry_nombre.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_numero_id.delete(0, tk.END)
                self.entry_numero_celular.delete(0, tk.END)
                self.abrir_vista_huellas(user_id, nombre)
            else:
                messagebox.showerror("Error", "No se pudo agregar el usuario.")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")

    def abrir_vista_huellas(self, user_id, user_name):
        self.root.destroy()
        nuevo_root = tk.Toplevel()
        VistaHuellas(nuevo_root, user_id, user_name)

    def volver_a_lista(self):
        self.root.destroy()
        if self.parent_window:
            self.parent_window.deiconify()

