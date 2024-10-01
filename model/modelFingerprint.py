import os
from model.modelUser import ModeloUsuario  # Para obtener la información del usuario
from model.dbConnetion import conectar# Tu conexión a la base de datos

class ModeloHuellas:
    def __init__(self):
        self.modelo_usuario = ModeloUsuario()  # Instancia para obtener el usuario

    def crear_directorio_usuario(self, user_id, user_name):
        # Crear directorio basado en ID y nombre del usuario
        base_dir = "images"
        user_dir = f"{user_id}_{user_name}"
        path = os.path.join(base_dir, user_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def guardar_imagen(self, user_id, user_name, imagen_path, dedo):
        # Guardar la imagen en el directorio del usuario
        user_dir = self.crear_directorio_usuario(user_id, user_name)
        imagen_destino = os.path.join(user_dir, f"{dedo}.png")  # Guardar con el nombre del dedo
        with open(imagen_path, 'rb') as src, open(imagen_destino, 'wb') as dst:
            dst.write(src.read())
        return imagen_destino

    def guardar_huella_en_bd(self, user_id, tipo_huella, resultado_analisis, imagen_path):
        conexion = conectar()  # Conectar a la base de datos
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                INSERT INTO huellas (iduser, tipo_huella, resultado_analisis, imagen_path)
                VALUES (%s, %s, %s, %s)
                """
                valores = (user_id, tipo_huella, resultado_analisis, imagen_path)
                cursor.execute(query, valores)
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al insertar en la base de datos: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()
        else:
            print("No se pudo conectar a la base de datos.")
            return False

    def obtener_huellas_usuario(self, user_id):
        cursor = self.conexion.cursor(dictionary=True)
        query = "SELECT idhuella, iduser, tipo_huella, resultado_analisis, imagen_path FROM proyetogrado.huellas WHERE iduser = %s"
        cursor.execute(query, (user_id,))
        huellas = cursor.fetchall()
        cursor.close()
        return huellas