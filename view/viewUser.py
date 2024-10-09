import tkinter as tk
from tkinter import messagebox
from model.modelUser import ModeloUsuario
from controller.listController import Controlador  # Asegúrate de que esto esté bien importado
from view.fingerprintView import VistaHuellas  # Importa la vista de huellas


class VistaUsuario:
    def __init__(self, root, parent_window=None):
        self.root = root
        self.parent_window = parent_window  # Guardamos la referencia a la ventana anterior
        self.root.title("Agregar Usuario")
        self.root.geometry("1200x800")

        # Frame para el botón en la esquina superior izquierda
        top_left_frame = tk.Frame(self.root)
        top_left_frame.place(relx=0, rely=0, anchor=tk.NW)  # Anclar en la esquina superior izquierda

        # Botón para cerrar la ventana o ejecutar otra acción
        self.boton_cerrar = tk.Button(top_left_frame, text="Ver lista", command=self.volver_a_lista)
        self.boton_cerrar.pack(padx=10, pady=10)

        # Frame principal donde se colocarán todos los elementos
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar el frame en la ventana

        # Configuración de los widgets dentro del frame
        self.crear_formulario(main_frame)

    def crear_formulario(self, frame):
        # Crear los campos para ingresar los datos, con mayor separación y centrado
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=20, pady=15, sticky='e')
        self.entry_nombre = tk.Entry(frame, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=20, pady=15)

        tk.Label(frame, text="Correo:").grid(row=1, column=0, padx=20, pady=15, sticky='e')
        self.entry_correo = tk.Entry(frame, width=40)
        self.entry_correo.grid(row=1, column=1, padx=20, pady=15)

        tk.Label(frame, text="Número de ID:").grid(row=2, column=0, padx=20, pady=15, sticky='e')
        self.entry_numero_id = tk.Entry(frame, width=40)
        self.entry_numero_id.grid(row=2, column=1, padx=20, pady=15)

        tk.Label(frame, text="Número de Celular:").grid(row=3, column=0, padx=20, pady=15, sticky='e')
        self.entry_numero_celular = tk.Entry(frame, width=40)
        self.entry_numero_celular.grid(row=3, column=1, padx=20, pady=15)

        # Botón para agregar usuario
        self.boton_agregar = tk.Button(frame, text="Agregar Usuario", command=self.agregar_usuario)
        self.boton_agregar.grid(row=5, column=0, columnspan=2, pady=30)

    def agregar_usuario(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        numero_id = self.entry_numero_id.get()
        numero_celular = self.entry_numero_celular.get()

        if nombre and correo and numero_id and numero_celular:
            modelo = ModeloUsuario()
            user_id = modelo.agregar_usuario(nombre, correo, numero_id, numero_celular)
            if user_id:  # Verificamos que el usuario se agregó correctamente
                messagebox.showinfo("Éxito", "Usuario agregado correctamente")

                # Limpiar campos después de agregar el usuario
                self.entry_nombre.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_numero_id.delete(0, tk.END)
                self.entry_numero_celular.delete(0, tk.END)

                # Después de limpiar, abrimos la pantalla de huellas
                self.abrir_vista_huellas(user_id, nombre)
            else:
                messagebox.showerror("Error", "No se pudo agregar el usuario.")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")

    def abrir_vista_huellas(self, user_id, user_name):
        # Cerramos la ventana actual
        self.root.destroy()
        # Abrimos la vista de huellas
        nuevo_root = tk.Toplevel()  # Crea una nueva ventana
        VistaHuellas(nuevo_root, user_id, user_name)  # Iniciamos la vista de huellas

    def volver_a_lista(self):
        # Destruye la ventana actual y vuelve a mostrar la ventana anterior
        self.root.destroy()
        if self.parent_window:  # Si hay una ventana principal oculta
            self.parent_window.deiconify()  # La volvemos a mostrar
