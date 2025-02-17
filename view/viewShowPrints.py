import tkinter as tk
from tkinter import filedialog, messagebox
from controller.controllerShowPrints import ControladorHuellas
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class VistaHuellasUsuario:
    def __init__(self, root, user_id, nombre_paciente, vista_usuarios):
        self.root = root
        self.user_id = user_id
        self.nombre_paciente = nombre_paciente  # Agregar el nombre del paciente
        self.controlador = ControladorHuellas()
        self.vista_usuarios = vista_usuarios  # Guardar referencia a la vista de usuarios

        # Obtener las huellas desde el controlador usando el user_id
        self.huellas = self.controlador.obtener_huellas_usuario(self.user_id)
        print(f"Huellas en la vista: {self.huellas}")  # Imprimir para verificar los datos

        self.root.title(f"Huellas de Usuario {self.user_id}")
        self.root.geometry("1200x800")
        self.root.config(bg='#f0f8ff')  # Fondo azul claro

        # Crear la interfaz de usuario
        self.crear_ui()

    def crear_ui(self):
        # Label para mostrar el nombre del paciente
        label_paciente = tk.Label(self.root, text=f"Paciente: {self.nombre_paciente}", bg='#f0f8ff', font=('Arial', 14))
        label_paciente.grid(row=0, column=0, columnspan=2, pady=(10, 5))  # Colocar en la parte superior central

        # Contenedor de botones centrados en la parte inferior
        self.frame_botones = tk.Frame(self.root, bg='#f0f8ff')
        self.frame_botones.grid(row=1, column=0, columnspan=2, pady=(10, 10))

        # Botón para volver a la lista
        self.boton_volver = tk.Button(self.frame_botones, text="Volver a Lista", command=self.volver_a_lista, bg='#87CEEB', fg='white',
                                      activebackground='#4682B4', activeforeground='white', relief='flat', width=15)
        self.boton_volver.pack(side=tk.LEFT, padx=10)  # Colocar a la izquierda
        self.boton_volver.bind("<Enter>", lambda e: self.boton_volver.config(bg='#ADD8E6'))  # Animación hover
        self.boton_volver.bind("<Leave>", lambda e: self.boton_volver.config(bg='#87CEEB'))

        # Botón para descargar en PDF
        self.boton_pdf = tk.Button(self.frame_botones, text="Descargar en PDF", command=self.descargar_pdf, bg='#4682B4', fg='white',
                                   activebackground='#1E90FF', activeforeground='white', relief='flat', width=15)
        self.boton_pdf.pack(side=tk.LEFT, padx=10)  # Colocar a la derecha
        self.boton_pdf.bind("<Enter>", lambda e: self.boton_pdf.config(bg='#87CEEB'))  # Animación hover
        self.boton_pdf.bind("<Leave>", lambda e: self.boton_pdf.config(bg='#4682B4'))

        # Contenedor de tarjetas de huellas
        self.frame_tarjetas = tk.Frame(self.root, bg='#f0f8ff')
        self.frame_tarjetas.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

        # Hacer que el frame_tarjetas sea responsivo
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear tarjetas con los datos de las huellas
        self.crear_tarjetas()

    def crear_tarjetas(self):
        if not self.huellas:
            print("No se encontraron huellas para este usuario.")
        else:
            print(f"Se encontraron {len(self.huellas)} huellas para el usuario {self.user_id}.")

        for index, huella in enumerate(self.huellas):
            if index >= 10:  # Limitar a 10 tarjetas
                break

            frame_tarjeta = tk.Frame(self.frame_tarjetas, bd=2, relief=tk.RAISED, padx=10, pady=10, bg='#ffffff')
            frame_tarjeta.grid(row=index // 5, column=index % 5, padx=10, pady=10, sticky="nsew")

            # Configurar pesos para que las tarjetas sean responsivas
            self.frame_tarjetas.grid_rowconfigure(index // 5, weight=1)
            self.frame_tarjetas.grid_columnconfigure(index % 5, weight=1)

            # Animación al pasar el ratón sobre la tarjeta
            frame_tarjeta.bind("<Enter>", lambda e, frame=frame_tarjeta: frame.config(bg='#e0f7fa'))
            frame_tarjeta.bind("<Leave>", lambda e, frame=frame_tarjeta: frame.config(bg='#ffffff'))

            # Mostrar información en la tarjeta
            tk.Label(frame_tarjeta, text=f"Tipo de Huella: {huella['tipo_huella']}", bg='#ffffff', font=('Arial', 12, 'bold')).pack(pady=(5, 0))
            tk.Label(frame_tarjeta, text=f"Resultado Análisis: {huella['resultado_analisis']}", bg='#ffffff', font=('Arial', 10)).pack(pady=(5, 10))

            # Cargar y mostrar la imagen
            imagen_path = huella['imagen_path']
            try:
                img = Image.open(imagen_path)
                img = img.resize((150, 150))  # Cambiar el tamaño a 150x150
                img_tk = ImageTk.PhotoImage(img)
                tk.Label(frame_tarjeta, image=img_tk, bg='#ffffff').pack(pady=(5, 0))
                frame_tarjeta.image = img_tk  # Mantener referencia a la imagen
            except Exception as e:
                print(f"Error al cargar la imagen: {imagen_path}. Error: {e}")

    def descargar_pdf(self):
        # Abrir un diálogo para seleccionar la ubicación de descarga
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return  # Si no se seleccionó ninguna ruta, salir de la función

        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Agregar título
        c.drawString(100, 750, "Huellas de Usuario")

        # Agregar información de las huellas
        y_position = 730
        for huella in self.huellas:
            # Agregar imagen
            imagen_path = huella['imagen_path']
            img = ImageReader(imagen_path)
            c.drawImage(img, 100, y_position - 50, width=50, height=50, preserveAspectRatio=True)  # Agregar la imagen

            # Agregar texto
            c.drawString(160, y_position - 20, f"Tipo de Huella: {huella['tipo_huella']}")
            c.drawString(160, y_position - 40, f"Resultado Análisis: {huella['resultado_analisis']}")
            c.drawString(160, y_position - 60, "-------------------------------------")
            y_position -= 80  # Espaciado entre huellas

            if y_position < 50:  # Si llega al final de la página, crear una nueva
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = 750

        c.save()
        messagebox.showinfo("Éxito", "PDF descargado correctamente.")

    def volver_a_lista(self):
        self.root.destroy()  # Destruir la ventana de huellas
        self.vista_usuarios.deiconify()  # Mostrar la ventana de gestión de usuarios nuevamente
#if __name__ == "__main__":
#    root = tk.Tk()
#    nombre_paciente = "Nombre del Paciente"  # Asigna aquí el nombre del paciente real
#    app = VistaHuellasUsuario(root, 13, nombre_paciente)
#   root.mainloop()