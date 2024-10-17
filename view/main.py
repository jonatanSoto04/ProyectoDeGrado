import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.listController import Controlador
from viewUser import VistaUsuario  # Importar la vista de agregar usuario
from viewShowPrints import VistaHuellasUsuario  # Asegúrate de importar la vista de huellas


class VistaUsuarios:
    def __init__(self, controlador, root=None):
        self.controlador = controlador
        self.root = root or tk.Tk()
        self.root.title("Usuarios")
        self.root.geometry("1200x800")

        # Frame para los botones, ordenados verticalmente
        botones_frame = tk.Frame(self.root)
        botones_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.boton_importar = tk.Button(botones_frame, text="Importar SQL", command=self.importar_sql)
        self.boton_importar.pack(fill=tk.X, padx=5, pady=5)

        self.boton_exportar = tk.Button(botones_frame, text="Exportar Base de Datos", command=self.exportar_base_datos)
        self.boton_exportar.pack(fill=tk.X, padx=5, pady=5)

        self.boton_agregar = tk.Button(botones_frame, text="Agregar Cliente", command=self.agregar_cliente)
        self.boton_agregar.pack(fill=tk.X, padx=5, pady=5)

        # Tabla de usuarios
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre", "Correo", "Número ID", "Número Celular"),
                                  show="headings")
        self.tabla.heading("ID", text="ID Usuario")  # Columna de ID del usuario
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Número ID", text="Número ID")
        self.tabla.heading("Número Celular", text="Número Celular")

        self.tabla.column("ID", width=0, stretch=tk.NO)  # Ocultamos el ID de usuario (ancho 0)

        self.tabla.bind('<Double-1>', self.mostrar_detalles)
        self.tabla.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        usuarios = self.controlador.obtener_usuarios()
        for usuario in usuarios:
            # Suponiendo que el usuario es una tupla con (id_usuario, nombre, correo, numero_id, numero_celular)
            self.tabla.insert("", tk.END, values=usuario)

    def mostrar_detalles(self, event):
        item_id = self.tabla.focus()  # Obtiene la fila seleccionada
        item = self.tabla.item(item_id)  # Obtiene los valores de esa fila
        user_id = item["values"][0]  # Aquí estamos tomando el ID del usuario (columna 1)
        print(user_id)  # Verificar el ID del usuario
        # Abrir la ventana de huellas con el user_id del usuario seleccionado
        self.abrir_vista_huellas_usuario(user_id)

    def abrir_vista_huellas_usuario(self, user_id):
        # Ocultar la ventana principal después de que la nueva ventana haya sido creada
        self.root.withdraw()
        # Crear la nueva ventana de huellas para el usuario seleccionado
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.transient(self.root)  # Establecer la nueva ventana como hija de la ventana principal

        # Pasar el user_id al constructor de la vista de huellas
        VistaHuellasUsuario(nueva_ventana, user_id)

    def agregar_cliente(self):
        # En lugar de destruir la ventana, la ocultamos
        self.root.withdraw()  # Oculta la ventana actual
        nuevo_root = tk.Toplevel(self.root)  # Crea una nueva ventana
        VistaUsuario(nuevo_root, self.root)  # Inicia la vista de agregar usuario

    def importar_sql(self):
        archivo = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
        if archivo:
            resultado = self.controlador.importar_sql(archivo)
            if resultado:
                messagebox.showinfo("Éxito", "Archivo SQL importado correctamente.")
            else:
                messagebox.showerror("Error", "Ocurrió un error al importar el archivo SQL.")

    def exportar_base_datos(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL Files", "*.sql")])
        if archivo:
            resultado = self.controlador.exportar_base_datos(archivo)
            if resultado:
                messagebox.showinfo("Éxito", "Base de datos exportada correctamente.")
            else:
                messagebox.showerror("Error", "Ocurrió un error al exportar la base de datos.")

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    controlador = Controlador()
    app = VistaUsuarios(controlador)
    app.mainloop()
