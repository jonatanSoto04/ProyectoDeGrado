import tkinter as tk
from tkinter import filedialog, messagebox

from Pruebaimagenes.test import predecir_tipo_huella, model, tipo_huella
from controller.listController import Controlador
from controller.fingerprintController import ControladorHuellas
from PIL import Image, ImageTk  # Para manejar las imágenes

class VistaHuellas:
    def __init__(self, root, user_id, user_name):
        self.root = root
        self.root.title("Registro de Huellas")
        self.root.geometry("1200x800")
        self.root.config(bg='#f0f8ff')  # Fondo azul claro
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
        self.boton_volver = tk.Button(self.root, text="Volver a Lista", command=self.volver_a_lista, bg='#87CEEB', fg='white',
                                      activebackground='#4682B4', activeforeground='white', relief='flat', width=15)
        self.boton_volver.pack(anchor="nw", padx=10, pady=10)
        self.boton_volver.bind("<Enter>", lambda e: self.boton_volver.config(bg='#ADD8E6'))  # Animación hover
        self.boton_volver.bind("<Leave>", lambda e: self.boton_volver.config(bg='#87CEEB'))

        # Contenedor de tarjetas de huellas
        self.frame_tarjetas = tk.Frame(self.root, bg='#f0f8ff')
        self.frame_tarjetas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Crear tarjetas
        self.crear_tarjetas()

        # Botón para guardar los datos
        self.boton_guardar = tk.Button(self.root, text="Guardar Datos", command=self.guardar_datos, bg='#4682B4', fg='white',
                                       activebackground='#1E90FF', activeforeground='white', relief='flat', width=15)
        self.boton_guardar.pack(pady=20)
        self.boton_guardar.bind("<Enter>", lambda e: self.boton_guardar.config(bg='#87CEEB'))  # Animación hover
        self.boton_guardar.bind("<Leave>", lambda e: self.boton_guardar.config(bg='#4682B4'))

    def crear_tarjetas(self):
        # Crear tarjetas y ajustar la distribución
        for index, dedo in enumerate(self.dedos):
            tarjeta = self.crear_tarjeta(index, dedo)
            self.tarjetas.append(tarjeta)  # Agregar tarjeta a la lista

    def crear_tarjeta(self, index, dedo):
        frame = tk.Frame(self.frame_tarjetas, bd=2, relief=tk.RAISED, padx=10, pady=10, bg='#ffffff')  # Fondo blanco para las tarjetas
        frame.grid(row=index // 5, column=index % 5, padx=10, pady=10, sticky='nsew')

        # Hacer que la tarjeta sea responsiva
        self.frame_tarjetas.grid_rowconfigure(index // 5, weight=1)
        self.frame_tarjetas.grid_columnconfigure(index % 5, weight=1)

        try:
            self.default_img = Image.open("images/default.png").resize((150, 150))  # Imagen por defecto
        except FileNotFoundError:
            self.default_img = Image.new("RGB", (150, 150), "lightgray")  # Fondo gris si no hay imagen
        img = ImageTk.PhotoImage(self.default_img)
        label_imagen = tk.Label(frame, image=img, bg='#ffffff')
        label_imagen.image = img  # Mantener una referencia a la imagen
        label_imagen.pack()

        # Nombre del dedo
        label_dedo = tk.Label(frame, text=dedo, bg='#ffffff', font=('Arial', 10, 'bold'))
        label_dedo.pack(pady=(5, 10))  # Espaciado vertical

        # Label para tipo de huella
        label_tipo_huella = tk.Label(frame, text="Tipo de huella", bg='#ffffff', font=('Arial', 10))
        label_tipo_huella.pack(pady=(10, 5))  # Espaciado vertical

        # Nuevo Label para mostrar el tipo de huella
        label_tipo_huella_value = tk.Label(frame, text={tipo_huella}, bg='#ffffff', font=('Arial', 10, 'italic'))
        label_tipo_huella_value.pack(pady=5)

        # Label para numeración
        label_entero = tk.Label(frame, text="Numeración", bg='#ffffff', font=('Arial', 10))
        label_entero.pack(pady=(10, 5))  # Espaciado vertical

        # Nuevo Label para mostrar el valor
        label_entero_value = tk.Label(frame, text="15", bg='#ffffff', font=('Arial', 10, 'italic'))
        label_entero_value.pack(pady=5)

        # Ocultar temporalmente el tipo de huella y la numeración
        label_tipo_huella.pack_forget()
        label_tipo_huella_value.pack_forget()
        label_entero.pack_forget()
        label_entero_value.pack_forget()

        # Vincular evento de clic a la tarjeta completa
        frame.bind("<Button-1>", lambda event, d=dedo, l=label_imagen: self.cargar_imagen(d, l))
        label_imagen.bind("<Button-1>", lambda event, d=dedo, l=label_imagen: self.cargar_imagen(d, l))

        # Animación de hover para la tarjeta
        frame.bind("<Enter>", lambda e: self.animar_tarjeta(frame, hover=True))
        frame.bind("<Leave>", lambda e: self.animar_tarjeta(frame, hover=False))

        return {
            "frame": frame,
            "label_tipo_huella": label_tipo_huella,
            "label_entero": label_entero,
            "label_imagen": label_imagen,
            "imagen_path": None,  # Almacenar la ruta de la imagen
            "label_tipo_huella_value": label_tipo_huella_value,
            "label_entero_value": label_entero_value
        }

    def animar_tarjeta(self, frame, hover):
        if hover:
            frame.config(bg='#e0f7fa', bd=4)  # Cambia el color de fondo y el borde
        else:
            frame.config(bg='#ffffff', bd=2)  # Restaura el color original y el borde

    def cargar_imagen(self, dedo, label_imagen):
        # Seleccionar la imagen
        imagen_path = self.controlador.seleccionar_imagen()
        if imagen_path:
            # Guardar la imagen en una ubicación específica
            imagen_destino = self.controlador.guardar_imagen(self.user_id, self.user_name, imagen_path, dedo)
            # Cargar y mostrar la imagen seleccionada en la interfaz
            img = Image.open(imagen_destino).resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            label_imagen.config(image=img_tk)
            label_imagen.image = img_tk  # Guardar referencia para evitar que se borre

            # Realizar la predicción del tipo de huella con el modelo entrenado
            tipo_huella = predecir_tipo_huella(imagen_destino, model)

            # Actualizar el label del tipo de huella en la tarjeta correspondiente
            for tarjeta in self.tarjetas:
                if tarjeta["label_imagen"] == label_imagen:
                    tarjeta["imagen_path"] = imagen_destino
                    tarjeta["label_tipo_huella_value"].config(text=tipo_huella)  # Mostrar tipo de huella predicho

                    # Mostrar los labels que estaban ocultos
                    tarjeta["label_tipo_huella"].pack()  # Mostrar el label del tipo de huella
                    tarjeta["label_tipo_huella_value"].pack()  # Mostrar el valor del tipo predicho
                    tarjeta["label_entero"].pack()  # Mostrar el label de numeración
                    tarjeta["label_entero_value"].pack()  # Mostrar la numeración

    def guardar_datos(self):
        datos_guardados = True  # Variable para verificar si todos los datos se guardaron correctamente

        for tarjeta in self.tarjetas:
            tipo_huella = tarjeta["label_tipo_huella_value"].cget("text")
            resultado_analisis = tarjeta["label_entero_value"].cget("text")
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
            self.volver_a_lista()

    def volver_a_lista(self):
        self.root.quit()  # Cerrar la ventana actual sin destruirla
        self.root.destroy()  # Asegurarse de destruir la ventana de huellas
        from view.main import VistaUsuarios  # Importar la vista de la lista
        nuevo_root = tk.Tk()  # Crear nueva instancia de Tk
        controlador = Controlador()  # Crear nueva instancia del controlador
        vista = VistaUsuarios(controlador, nuevo_root)  # Crear la vista de usuarios
        nuevo_root.mainloop()  # Iniciar el bucle principal de la nueva ventana