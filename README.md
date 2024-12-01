_Temporal (ChatGPT)_

# Identificación de Tortugas (Grefa)

Este repositorio contiene una Interfaz de Usuario para Grefa, diseñada para identificar tortugas basándose en las escamas de su caparazón. En Grefa, tienen un tipo de tortugas cuyo caparazón muestra unas escamas que pueden identificar a cada tortuga individualmente.

## Funcionalidades

- **Identificación de tortugas**: Permite tomar una foto de una tortuga y comprobar si es una de las que ya tienen en la base de datos mediante comparación de imágenes.
- **Gestión de la base de datos**: Permite añadir nuevas tortugas y eliminar tortugas existentes en la base de datos.
- **Uso educativo**: El código es modular y fácil de editar, especialmente diseñado para que los estudiantes puedan implementar y probar sus propios algoritmos.

## Ejemplo de imágenes

Aquí hay un par de ejemplos de las imágenes de tortugas en el directorio `tortugas_bd`:

![Tortuga 1](tortugas_bd/tortu1.jpg)
![Tortuga 2](tortugas_bd/tortu2.jpg)

## Cómo contribuir

Para contribuir, simplemente clona el repositorio, realiza un `git pull` para descargar el código y edita la función `calcular_distancia` en el archivo `algo.py`. Esta función toma dos imágenes como entrada y devuelve un valor que sería 0 si las dos imágenes corresponden a la misma tortuga.

```python
def calcular_distancia(imagen1, imagen2):
    # Implementa tu algoritmo aquí
    return distancia
```

¡Esperamos tus contribuciones y mejoras!