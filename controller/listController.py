import subprocess
from model.modelUser import ModeloUsuario
class Controlador:
    def __init__(self):
        self.modelo = ModeloUsuario()

    def obtener_usuarios(self):
        return self.modelo.obtener_usuarios()

    def eliminar_usuario(self, user_id):
        self.modelo.eliminar_usuario(user_id)

    def importar_sql(self, archivo_sql):
        try:
            comando = f"mysql -u root -p < {archivo_sql}"  # Ajusta según tu configuración de MySQL
            subprocess.run(comando, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al importar SQL: {e}")
            return False

    def exportar_base_datos(self, archivo_sql):
        try:
            comando = f"mysqldump -u root -p proyectogrado > {archivo_sql}"  # Ajusta según tu configuración de MySQL
            subprocess.run(comando, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al exportar la base de datos: {e}")
            return False
    def iniciar(self):
        from view.main import VistaUsuarios
        self.vista = VistaUsuarios(self)
        self.vista.mainloop()

#if __name__ == "__main__":
#    controlador = Controlador()
#    controlador.iniciar()
