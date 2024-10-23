import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.listController import Controlador
from viewUser import VistaUsuario  # Importar la vista de agregar usuario
from viewShowPrints import VistaHuellasUsuario  # Asegúrate de importar la vista de huellas

class VistaUsuarios:
    def __init__(self, controlador, root=None):
        self.controlador = controlador
        self.root = root or tk.Tk()
        self.root.title("Gestión de Usuario")
        self.root.geometry("1200x800")
        self.root.configure(bg="#e6f7ff")  # Fondo azul cielo

        # Frame superior con el título
        header_frame = tk.Frame(self.root, bg="#00aaff")  # Fondo azul más oscuro
        header_frame.pack(fill=tk.X)

        titulo = tk.Label(header_frame, text="Gestión de Usuario", font=("Verdana Bold", 30), fg="white", bg="#00aaff")
        titulo.pack(padx=20, pady=10)

        # Frame para los botones, ordenados verticalmente
        botones_frame = tk.Frame(self.root, bg="#e6f7ff")
        botones_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Crear botones con estilo personalizado
        self.boton_importar = self.crear_boton(botones_frame, "Importar SQL", self.importar_sql)
        self.boton_exportar = self.crear_boton(botones_frame, "Exportar Base de Datos", self.exportar_base_datos)
        self.boton_agregar = self.crear_boton(botones_frame, "Agregar Cliente", self.agregar_cliente)

        # Frame para la tabla y scrollbar
        table_frame = tk.Frame(self.root)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollbar para la tabla
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabla de usuarios con estilo personalizado
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Correo", "Número ID", "Número Celular"),
                                   show="headings", yscrollcommand=scrollbar.set)

        # Encabezado con evento de clic para ordenar
        self.tabla.heading("ID", text="ID Usuario", command=lambda: self.ordenar_columna("ID"))
        self.tabla.heading("Nombre", text="Nombre", command=lambda: self.ordenar_columna("Nombre"))
        self.tabla.heading("Correo", text="Correo", command=lambda: self.ordenar_columna("Correo"))
        self.tabla.heading("Número ID", text="Número ID", command=lambda: self.ordenar_columna("Número ID"))
        self.tabla.heading("Número Celular", text="Número Celular", command=lambda: self.ordenar_columna("Número Celular"))

        # Configuración de columnas
        self.tabla.column("ID", width=100, anchor=tk.CENTER)
        self.tabla.column("Nombre", width=150, anchor=tk.W)
        self.tabla.column("Correo", width=200, anchor=tk.W)
        self.tabla.column("Número ID", width=150, anchor=tk.CENTER)
        self.tabla.column("Número Celular", width=150, anchor=tk.CENTER)

        # Estilos para encabezado y filas
        style = ttk.Style(self.root)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="white", foreground="black", rowheight=35)
        style.configure("Treeview", rowheight=30, font=("Arial", 12))

        # Scroll de la tabla
        scrollbar.config(command=self.tabla.yview)

        self.tabla.tag_configure("oddrow", background="#e6f7ff")  # Fondo azul cielo para filas impares
        self.tabla.tag_configure("evenrow", background="#ccf2ff")  # Azul claro para filas pares

        # Evento para cambiar el color de las filas al pasar el mouse
        self.tabla.bind('<Motion>', self.on_mouse_over_row)

        # Evento para seleccionar fila y abrir vista de huellas
        self.tabla.bind("<Double-1>", self.seleccionar_usuario)

        # Inserción de la tabla en el frame
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Variable para recordar la última fila sobre la que se pasó el mouse
        self.previous_row = None

        self.cargar_usuarios()

    def cargar_usuarios(self):
        usuarios = self.controlador.obtener_usuarios()
        for index, usuario in enumerate(usuarios):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tabla.insert("", tk.END, values=usuario, tags=(tag,))

    def crear_boton(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, height=2, width=20, bg="#00aaff", fg="white", borderwidth=0)
        button.bind("<Enter>", self.on_hover)
        button.bind("<Leave>", self.on_leave)
        button.pack(fill=tk.X, padx=5, pady=5)

        return button

    def agregar_cliente(self):
        self.root.withdraw()
        nuevo_root = tk.Toplevel(self.root)
        VistaUsuario(nuevo_root, self.root)

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

    def on_hover(self, event):
        self.after_id = self.root.after(200, lambda: event.widget.config(bg="white", fg="#00aaff"))  # Fondo blanco y texto azul cielo

    def on_leave(self, event):
        self.root.after_cancel(self.after_id)  # Cancelar la acción de cambio de color si se sale del botón
        event.widget.config(bg="#00aaff", fg="white")  # Volver al color original

    def on_mouse_over_row(self, event):
        """ Cambia el fondo de la fila sobre la que pasa el mouse, sin afectar el encabezado. """
        row_id = self.tabla.identify_row(event.y)

        # Restaurar color de la fila anterior
        if self.previous_row:
            tag = self.tabla.item(self.previous_row, "tags")[0]
            if tag == "oddrow":
                self.tabla.tag_configure(self.previous_row, background="#e6f7ff")
            else:
                self.tabla.tag_configure(self.previous_row, background="#ccf2ff")

        # Cambiar el color de la fila actual
        if row_id:  # Asegurarse de que no es el encabezado
            self.tabla.tag_configure(row_id, background="#cceeff")  # Azul muy suave
            self.previous_row = row_id  # Guardar la fila actual

    def ordenar_columna(self, col):
        """ Ordena la tabla por la columna especificada. """
        # Obtener datos de la tabla
        data = [(self.tabla.item(item)["values"], item) for item in self.tabla.get_children()]
        data.sort(key=lambda x: x[0][self.tabla["columns"].index(col)])  # Ordenar por el valor de la columna

        # Limpiar la tabla actual y volver a insertar los datos ordenados
        self.tabla.delete(*self.tabla.get_children())
        for index, (values, item) in enumerate(data):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tabla.insert("", tk.END, values=values, tags=(tag,))

        # Resetear previous_row
        self.previous_row = None

    def seleccionar_usuario(self, event):
        """ Maneja la selección de un usuario de la tabla y abre la vista de huellas. """
        selected_item = self.tabla.selection()
        if selected_item:
            user_id = self.tabla.item(selected_item, "values")[0]  # Obtener el ID del usuario
            nombre_paciente = self.tabla.item(selected_item, "values")[1]  # Obtener el nombre del usuario (asumiendo que es el segundo valor)
            print(f"Usuario seleccionado: ID={user_id}, Nombre={nombre_paciente}")
            self.abrir_vista_huellas(user_id, nombre_paciente)

    def abrir_vista_huellas(self, user_id, nombre_paciente):
        """ Abre la vista de huellas para el usuario seleccionado. """
        self.root.withdraw()  # Oculta la ventana actual
        nuevo_root = tk.Toplevel(self.root)
        VistaHuellasUsuario(nuevo_root, user_id, nombre_paciente,
                            self.root)  # Pasar referencia a la ventana de usuarios


if __name__ == "__main__":
    controlador = Controlador()  # Asegúrate de tener tu controlador inicializado
    app = VistaUsuarios(controlador)
    app.root.mainloop()