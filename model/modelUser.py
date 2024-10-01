import mysql
from model.dbConnetion import conectar
class ModeloUsuario:
    def __init__(self):
        self.conexion = conectar()

    def agregar_usuario(self, nombre, correo, numero_id, numero_celular, idhuellas= None ):
        cursor = self.conexion.cursor()
        try:
            query = """INSERT INTO user (name, correo, numero_id, numero_celular) 
                               VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (nombre, correo, numero_id, numero_celular))
            self.conexion.commit()
            print("Usuario agregado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al agregar usuario: {err}")
        finally:
            cursor.close()

    def obtener_usuarios(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT name, correo, numero_id, numero_celular FROM user")
        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def eliminar_usuario(self, user_id):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE iduser = %s", (user_id,))
            self.conexion.commit()
        except mysql.connector.Error as err:
            print(f"Error al eliminar usuario: {err}")
        finally:
            cursor.close()