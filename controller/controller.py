class controller:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.vista.boton.config(command=self.gestionar_evento)

    def gestionar_evento(self):
        datos = self.modelo.obtener_datos()
        self.vista.actualizar_vista(datos)