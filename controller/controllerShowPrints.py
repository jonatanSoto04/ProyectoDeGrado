from model.modelShowPrints import ModeloHuellas  # Asegúrate de importar el modelo correctamente

class ControladorHuellas:
    def __init__(self):
        self.modelo_huellas = ModeloHuellas()

    def obtener_huellas_usuario(self, user_id):
        return self.modelo_huellas.obtener_huellas_usuario(user_id)
