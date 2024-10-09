import tkinter as tk
from tkinter import filedialog, messagebox
from controller.listController import Controlador
from controller.fingerprintController import ControladorHuellas
from PIL import Image, ImageTk  # Para manejar las imágenes

class VistaHuellas:
    def __init__(self, root, user_id, user_name):
        self.root = root
        self.root.title("Registro de Huellas")
        self.root.geometry("1200x800")
        self.controlador = ControladorHuellas()
        self.user_id = user_id
        self.user_name = user_name
        self.dedos = ["Pulgar Derecho", "Índice Derecho", "Medio Derecho", "Anular Derecho", "Meñique Derecho",
                      "Pulgar Izquierdo", "Índice Izquierdo", "Medio Izquierdo", "Anular Izquierdo",
                      "Meñique Izquierdo"]

        self.tarjetas = []  # Lista para almacenar referencias a las tarjetas
        self.crear_ui()

    def crear_ui(self):
        # Botón para volver a la lista
        self.boton_volver = tk.Button(self.root, text="Volver a Lista", command=self.volver_a_lista)
        self.boton_volver.pack(anchor="nw", padx=10, pady=10)

        # Contenedor de tarjetas de huellas
        self.frame_tarjetas = tk.Frame(self.root)
        self.frame_tarjetas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Crear tarjetas
        for index, dedo in enumerate(self.dedos):
            tarjeta = self.crear_tarjeta(index, dedo)
            self.tarjetas.append(tarjeta)  # Agregar tarjeta a la lista

        # Botón para guardar los datos
        self.boton_guardar = tk.Button(self.root, text="Guardar Datos", command=self.guardar_datos)
        self.boton_guardar.pack(pady=20)

    def crear_tarjeta(self, index, dedo):
        frame = tk.Frame(self.frame_tarjetas, bd=2, relief=tk.RAISED, padx=10, pady=10)
        frame.grid(row=index // 5, column=index % 5, padx=10, pady=10)

        try:
            self.default_img = Image.open("images/default.png").resize((150, 150))  # Imagen por defecto
        except FileNotFoundError:
            self.default_img = Image.new("RGB", (150, 150), "lightgray")  # Fondo gris si no hay imagen
        img = ImageTk.PhotoImage(self.default_img)
        label_imagen = tk.Label(frame, image=img)
        label_imagen.image = img  # Mantener una referencia a la imagen
        label_imagen.pack()

        # Nombre del dedo
        label_dedo = tk.Label(frame, text=dedo)
        label_dedo.pack()

        # Tipo de huella
        entry_tipo_huella = tk.Entry(frame, width=20)
        entry_tipo_huella.pack(pady=5)
        entry_tipo_huella.insert(0, "Tipo de huella")

        # Campo entero para análisis
        entry_entero = tk.Entry(frame, width=10)
        entry_entero.pack(pady=5)
        entry_entero.insert(0, "Valor")

        # Botón para cargar imagen
        boton_cargar = tk.Button(frame, text="Cargar Imagen", command=lambda: self.cargar_imagen(dedo, label_imagen))
        boton_cargar.pack(pady=5)

        return {
            "frame": frame,
            "tipo_huella": entry_tipo_huella,
            "resultado": entry_entero,
            "label_imagen": label_imagen,
            "imagen_path": None  # Almacenar la ruta de la imagen
        }

    def cargar_imagen(self, dedo, label_imagen):
        imagen_path = self.controlador.seleccionar_imagen()
        if imagen_path:
            imagen_destino = self.controlador.guardar_imagen(self.user_id, self.user_name, imagen_path, dedo)
            img = Image.open(imagen_destino).resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            label_imagen.config(image=img_tk)
            label_imagen.image = img_tk  # Guardar referencia para evitar que se borre

            # Actualizar la ruta de la imagen en la tarjeta
            for tarjeta in self.tarjetas:
                if tarjeta["label_imagen"] == label_imagen:
                    tarjeta["imagen_path"] = imagen_destino

    def guardar_datos(self):
        datos_guardados = True  # Variable para verificar si todos los datos se guardaron correctamente

        for tarjeta in self.tarjetas:
            tipo_huella = tarjeta["tipo_huella"].get()
            resultado_analisis = tarjeta["resultado"].get()
            imagen_path = tarjeta["imagen_path"]

            if tipo_huella and resultado_analisis and imagen_path:
                try:
                    resultado_analisis = int(resultado_analisis)
                except ValueError:
                    messagebox.showerror("Error", f"El valor de análisis para {tipo_huella} debe ser un número entero.")
                    datos_guardados = False
                    continue

                # Guardar los datos usando el controlador
                if not self.controlador.guardar_datos_huella(self.user_id, tipo_huella, resultado_analisis,
                                                             imagen_path):
                    datos_guardados = False
                    messagebox.showerror("Error", f"Error al guardar la huella para el dedo {tipo_huella}.")
                    break  # Detener el proceso si hay error al guardar
            else:
                messagebox.showwarning("Advertencia", f"Faltan datos para el dedo {tipo_huella}.")
                datos_guardados = False

        # Si todos los datos se guardaron correctamente, volvemos a la lista de usuarios
        if datos_guardados:
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
            self.volver_a_lista()  # Redirigir a la pantalla principal
        else:
            messagebox.showwarning("Advertencia", "No se guardaron todos los datos correctamente.")

    def volver_a_lista(self):
        self.root.quit()  # Cerrar la ventana actual sin destruirla
        self.root.destroy()  # Asegurarse de destruir la ventana de huellas
        from view.main import VistaUsuarios  # Importar la vista de la lista
        nuevo_root = tk.Tk()
        controlador = Controlador()  # Controlador de la vista principal
        VistaUsuarios(controlador, nuevo_root).mainloop()
