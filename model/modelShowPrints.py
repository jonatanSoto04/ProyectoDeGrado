from model.dbConnetion import conectar  # Asegúrate de que la conexión está importada correctamente
class ModeloHuellas:
    def __init__(self):
        self.conexion = conectar()
        if self.conexion is None:
            raise Exception("No se pudo establecer la conexión con la base de datos.")

    def obtener_huellas_usuario(self, user_id):
        cursor = self.conexion.cursor(dictionary=True)
        query = "SELECT idhuella, iduser, tipo_huella, resultado_analisis, imagen_path FROM huellas WHERE iduser = %s"
        cursor.execute(query, (user_id,))
        huellas = cursor.fetchall()
        cursor.close()
        return huellas
