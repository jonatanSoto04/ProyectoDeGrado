from model.modelUser import ModeloUsuario

class ControladorUsuario:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloUsuario()

    def agregar_usuario(self, nombre, correo, numero_id, numero_celular, idhuellas):
        self.modelo.agregar_usuario(nombre, correo, numero_id, numero_celular, idhuellas)
