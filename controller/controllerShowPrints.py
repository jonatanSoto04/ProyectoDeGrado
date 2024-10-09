from model.modelShowPrints import ModeloHuellas  # Asegúrate de importar el modelo correctamente

class ControladorHuellas:
    def __init__(self):
        self.modelo_huellas = ModeloHuellas()

    def obtener_huellas_usuario(self, user_id):
        huellas = self.modelo_huellas.obtener_huellas_usuario(user_id)
        print(f"Huellas recibidas en el controlador: {huellas}")  # Imprimir para verificar los datos
        return huellas
