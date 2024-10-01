import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.listController import Controlador
from viewUser import VistaUsuario  # Importar la vista de agregar usuario

class VistaUsuarios:
    def __init__(self, controlador):
        self.controlador = controlador
        self.root = tk.Tk()
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
        self.tabla = ttk.Treeview(self.root, columns=("Nombre", "Correo", "Número ID", "Número Celular"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Número ID", text="Número ID")
        self.tabla.heading("Número Celular", text="Número Celular")

        self.tabla.bind('<Double-1>', self.mostrar_detalles)
        self.tabla.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        usuarios = self.controlador.obtener_usuarios()
        for usuario in usuarios:
            self.tabla.insert("", tk.END, values=usuario)

    def mostrar_detalles(self, event):
        item_id = self.tabla.focus()
        item = self.tabla.item(item_id)
        user_id = item["values"][0]
        detalle_ventana = tk.Toplevel(self.root)
        detalle_ventana.title(f"Detalles de Usuario {user_id}")
        detalle_label = tk.Label(detalle_ventana, text=f"Detalles del usuario con ID: {user_id}")
        detalle_label.pack()

    def agregar_cliente(self):
        self.root.destroy()  # Cierra la ventana principal
        nuevo_root = tk.Tk()  # Crea una nueva ventana
        VistaUsuario(nuevo_root)  # Inicia la vista de agregar usuario
        nuevo_root.mainloop()  # Ejecuta el loop de la nueva ventana

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
    controlador.iniciar()