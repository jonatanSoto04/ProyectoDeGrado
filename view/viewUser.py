import tkinter as tk
from tkinter import messagebox
from model.modelUser import ModeloUsuario
from controller.listController import Controlador  # Asegúrate de que esto esté bien importado
class VistaUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Agregar Usuario")
        self.root.geometry("1200x800")

        # Frame para el botón en la esquina superior izquierda
        top_left_frame = tk.Frame(self.root)
        top_left_frame.place(relx=0, rely=0, anchor=tk.NW)  # Anclar en la esquina superior izquierda

        # Botón para cerrar la ventana o ejecutar otra acción
        self.boton_cerrar = tk.Button(top_left_frame, text="Ver lista", command=self.cerrar_ventana)
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
            modelo.agregar_usuario(nombre, correo, numero_id, numero_celular)
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")

    def cerrar_ventana(self):
        # Cerrar la ventana actual y abrir VistaUsuarios
        self.root.destroy()  # Cierra la ventana actual
        if __name__ == "__main__":
            controlador = Controlador()
            controlador.iniciar()

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaUsuario(root)
    root.mainloop()