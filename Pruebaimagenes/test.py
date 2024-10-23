import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Cargar el modelo entrenado
model = load_model(r'C:\Users\Janus\OneDrive\Documentos\Proyecto de Grado\Pruebaimagenes\modelo_huellas_2.keras')

# Función para predecir el tipo de huella dactilar
def predecir_tipo_huella(imagen_path, model):
    img = image.load_img(imagen_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    tipo_huella = np.argmax(prediction, axis=1)
    
    if tipo_huella == 0:
        return "Arco"
    elif tipo_huella == 1:
        return "Presilla"
    else:
        return "Verticilo"

# Ejemplo de uso
# cambiar ruta
imagen_path = r"C:\Users\Janus\OneDrive\Documentos\Proyecto de Grado\Pruebaimagenes\arco6.jpg"
tipo_huella = predecir_tipo_huella(imagen_path, model)
print(f'El tipo de huella es: {tipo_huella}')
