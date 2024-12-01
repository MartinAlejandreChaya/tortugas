import os
from PIL import Image

from algo import calcular_distancia

# Función para encontrar las imágenes más similares
def encontrar_similares(imagen_nueva, imagenes_base, top_n=10):
    distancias = []
    for nombre, imagen_base in imagenes_base.items():
        distancia = calcular_distancia(imagen_nueva, imagen_base)
        distancias.append((nombre, distancia))
    distancias.sort(key=lambda x: x[1])  # Ordenar por distancia
    return distancias[:top_n]

# Cargar todas las imágenes de la carpeta base
def cargar_imagenes(carpeta):
    imagenes = {}
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(('png', 'jpg', 'jpeg')):
            ruta = os.path.join(carpeta, archivo)
            imagenes[archivo] = Image.open(ruta)
    return imagenes