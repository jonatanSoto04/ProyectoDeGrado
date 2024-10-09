import tkinter as tk
from tkinter import filedialog, messagebox
from controller.controllerShowPrints import ControladorHuellas
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class VistaHuellasUsuario:
    def __init__(self, root, user_id):
        self.root = root
        self.root = root
        self.user_id = user_id
        self.controlador = ControladorHuellas()

        # Obtener las huellas desde el controlador
        self.huellas = self.controlador.obtener_huellas_usuario(self.user_id)
        print(f"Huellas en la vista: {self.huellas}")  # Imprimir para verificar los datos

        self.root.title("Huellas de Usuario")
        self.root.geometry("1200x800")

        # Crear la interfaz de usuario
        self.crear_ui()

    def crear_ui(self):
        # Botón para volver a la lista
        self.boton_volver = tk.Button(self.root, text="Volver a Lista", command=self.volver_a_lista)
        self.boton_volver.grid(row=0, column=0, sticky="nw", padx=10, pady=10)  # Colocar en la esquina superior izquierda

        # Botón para descargar en PDF
        self.boton_pdf = tk.Button(self.root, text="Descargar en PDF", command=self.descargar_pdf)
        self.boton_pdf.grid(row=0, column=1, sticky="nw", padx=10, pady=10)  # Colocar al lado del botón de volver

        # Contenedor de tarjetas de huellas
        self.frame_tarjetas = tk.Frame(self.root)
        self.frame_tarjetas.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Hacer que el frame_tarjetas sea responsivo
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear tarjetas
        self.crear_tarjetas()

    def crear_tarjetas(self):
        if not self.huellas:
            print("No se encontraron huellas para este usuario.")
        else:
            print(f"Se encontraron {len(self.huellas)} huellas para el usuario.")

        for index, huella in enumerate(self.huellas):
            if index >= 10:  # Limitar a 10 tarjetas
                break

            frame_tarjeta = tk.Frame(self.frame_tarjetas, bd=2, relief=tk.RAISED, padx=10, pady=10)
            frame_tarjeta.grid(row=index // 5, column=index % 5, padx=10, pady=10, sticky="nsew")

            # Configurar pesos para que las tarjetas sean responsivas
            self.frame_tarjetas.grid_rowconfigure(index // 5, weight=1)
            self.frame_tarjetas.grid_columnconfigure(index % 5, weight=1)

            # Mostrar información en la tarjeta
            tk.Label(frame_tarjeta, text=f"ID Huella: {huella['idhuella']}").pack()
            tk.Label(frame_tarjeta, text=f"Tipo de Huella: {huella['tipo_huella']}").pack()
            tk.Label(frame_tarjeta, text=f"Resultado Análisis: {huella['resultado_analisis']}").pack()

            # Cargar y mostrar la imagen
            imagen_path = huella['imagen_path']
            try:
                img = Image.open(imagen_path)
                img = img.resize((200, 200))  # Cambiar el tamaño a 200x200
                img_tk = ImageTk.PhotoImage(img)
                tk.Label(frame_tarjeta, image=img_tk).pack()
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
        self.root.destroy()  # Cerrar la ventana actual
        from view.main import VistaUsuarios  # Importar la vista de la lista
        nuevo_root = tk.Tk()
        controlador = ControladorHuellas()
        VistaUsuarios(controlador).mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaHuellasUsuario(root)  # Cambia el user_id según sea necesario
    root.mainloop()