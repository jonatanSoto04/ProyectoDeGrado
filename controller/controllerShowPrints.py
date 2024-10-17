from model.modelShowPrints import ModeloHuellas  # Asegúrate de importar el modelo correctamente

from model.modelShowPrints import ModeloHuellas  # Asegúrate de importar el modelo correctamente

class ControladorHuellas:
    def __init__(self):
        self.modelo_huellas = ModeloHuellas()

    def obtener_huellas_usuario(self, user_id):
        # Utiliza el método del modelo directamente en lugar de 'ejecutar_query'
        huellas = self.modelo_huellas.obtener_huellas_usuario(user_id)
        print(f"Huellas recibidas en el controlador: {huellas}")
        return huellas