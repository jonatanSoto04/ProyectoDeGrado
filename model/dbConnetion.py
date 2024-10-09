import mysql.connector
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",  # Mismo host que Spring
            user="root",       # Usuario root como en Spring
            password="Jonatan.soto04",  # Misma contraseña
            database="proyetogrado",    # Aquí debes asegurarte de que la base de datos exista
            port=3306  # El puerto predeterminado de MySQL es 3306 (lo mismo que en Spring)
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

