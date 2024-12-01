import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from misc import cargar_imagenes, encontrar_similares

CARPETA_BASE = "tortugas_bd"
TAMANO_IMAGENES = (300, 200)

# Cargar imágenes base
imagenes_base = cargar_imagenes(CARPETA_BASE)


# Función para manejar la eliminación de una tortuga
def eliminar_tortuga(nombre):
    ruta = os.path.join(CARPETA_BASE, nombre)
    if os.path.exists(ruta):
        os.remove(ruta)
    if nombre in imagenes_base:
        del imagenes_base[nombre]
    cargar_tab_ver_tortugas()

# Función para cargar la pestaña de visualización de tortugas
def cargar_tab_ver_tortugas():
    # Limpiar el canvas y recargar imágenes
    canvas_ver_tortugas.delete("all")

    # Crear un frame dentro del canvas para colocar las imágenes
    frame_contenido = tk.Frame(canvas_ver_tortugas)
    contenido_id = canvas_ver_tortugas.create_window((0, 0), window=frame_contenido, anchor="n")

    # Mostrar imágenes en un grid de 3 columnas
    columnas = 3
    for idx, (nombre, imagen) in enumerate(imagenes_base.items()):
        row, col = divmod(idx, columnas)

        # Crear marco para cada imagen
        frame = tk.Frame(frame_contenido, padx=5, pady=5)
        frame.grid(row=row, column=col, padx=10, pady=10)

        # Crear y mostrar la miniatura
        imagen_tk = ImageTk.PhotoImage(imagen.resize(TAMANO_IMAGENES))
        etiqueta_imagen = tk.Label(frame, image=imagen_tk)
        etiqueta_imagen.image = imagen_tk
        etiqueta_imagen.pack()

        # Nombre de la imagen
        etiqueta_texto = tk.Label(frame, text=nombre, font=("Arial", 10))
        etiqueta_texto.pack()

        # Botón para eliminar
        boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda n=nombre: eliminar_tortuga(n), font=("Arial", 10))
        boton_eliminar.pack()

    # Ajustar scroll al contenido del frame
    frame_contenido.update_idletasks()
    canvas_ver_tortugas.config(scrollregion=canvas_ver_tortugas.bbox("all"))
    # Centrar el contenido horizontalmente
    def centrar_contenido(event=None):
        canvas_width = canvas_ver_tortugas.winfo_width()
        contenido_width = frame_contenido.winfo_width()
        if canvas_width > contenido_width:
            x_offset = (canvas_width - contenido_width) // 2
        else:
            x_offset = 0
        canvas_ver_tortugas.coords(contenido_id, x_offset, 0)

    # Llamar al centrado cuando cambie el tamaño del canvas
    canvas_ver_tortugas.bind("<Configure>", centrar_contenido)
    centrar_contenido()  # Asegurar el centrado inicial

# Función para manejar la búsqueda de imágenes similares
def buscar_similares():
    ruta_imagen = filedialog.askopenfilename(
        title="Seleccionar una imagen",
        filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg")]
    )
    if not ruta_imagen:
        return

    # Cargar la imagen subida y redimensionarla
    imagen_nueva = Image.open(ruta_imagen).resize((TAMANO_IMAGENES[0] * 2, TAMANO_IMAGENES[1] * 2))
    imagen_tk_nueva = ImageTk.PhotoImage(imagen_nueva)

    # Encontrar imágenes similares
    resultados = encontrar_similares(imagen_nueva, imagenes_base)

    # Limpiar canvas y mostrar resultados
    canvas_buscar_tortugas.delete("all")
    frame_resultados = tk.Frame(canvas_buscar_tortugas)
    contenido_id = canvas_buscar_tortugas.create_window((0, 0), window=frame_resultados, anchor="n")

    # Mostrar imagen subida en la primera celda (spans 2 rows and 2 columns)
    frame_imagen_nueva = tk.Frame(frame_resultados, padx=5, pady=5)
    frame_imagen_nueva.grid(row=0, column=0, rowspan=2, columnspan=2, padx=10, pady=10)

    tk.Label(frame_imagen_nueva, text="Imagen subida:", font=("Arial", 14)).pack()
    etiqueta_imagen_nueva = tk.Label(frame_imagen_nueva, image=imagen_tk_nueva)
    etiqueta_imagen_nueva.image = imagen_tk_nueva
    etiqueta_imagen_nueva.pack()

    # Mostrar imágenes similares en el grid
    columnas = 3  # Número de columnas para las imágenes similares (2 columnas para las imágenes)
    for idx, (nombre, distancia) in enumerate(resultados):
        # Ajustar fila para que inicie después de la imagen subida
        if idx < 2:
            row = idx  # Primeras dos filas para las imágenes similares
            col = 2    # Columna 2 para la imagen similar
        else:
            row = (idx - 2) // columnas + 2  # Después de la imagen subida
            col = (idx - 2) % columnas      # Continuar en la siguiente columna

        # Crear ruta de la imagen similar
        ruta = os.path.join(CARPETA_BASE, nombre)
        imagen_similar = Image.open(ruta).resize(TAMANO_IMAGENES)
        imagen_tk_similar = ImageTk.PhotoImage(imagen_similar)

        # Crear marco para cada imagen
        frame = tk.Frame(frame_resultados, padx=5, pady=5)
        frame.grid(row=row, column=col, padx=10, pady=10)

        etiqueta_imagen_similar = tk.Label(frame, image=imagen_tk_similar)
        etiqueta_imagen_similar.image = imagen_tk_similar
        etiqueta_imagen_similar.pack()

        etiqueta_texto = tk.Label(frame, text=f"{nombre}\nDistancia: {distancia:.2f}")
        etiqueta_texto.pack()


    # Actualizar scrollregion del Canvas
    frame_resultados.update_idletasks()  # Asegura que se haya actualizado la información antes de ajustar el scroll
    canvas_buscar_tortugas.config(scrollregion=canvas_buscar_tortugas.bbox("all"))

# Configuración de la interfaz de usuario
root = tk.Tk()
root.title("TortuGrefa")
root.geometry("1100x600")

# Crear notebook para pestañas
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Pestaña 1: Ver tortugas
tab_ver_tortugas = tk.Frame(notebook)
notebook.add(tab_ver_tortugas, text="Ver Tortugas")

# Añadir canvas y scrollbar para scroll vertical
canvas_ver_tortugas = tk.Canvas(tab_ver_tortugas)
scrollbar_ver_tortugas = ttk.Scrollbar(tab_ver_tortugas, orient="vertical", command=canvas_ver_tortugas.yview)
canvas_ver_tortugas.configure(yscrollcommand=scrollbar_ver_tortugas.set)

canvas_ver_tortugas.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar_ver_tortugas.pack(side=tk.RIGHT, fill="y")

cargar_tab_ver_tortugas()

# Pestaña 2: Subir y buscar tortugas
tab_buscar_tortugas = tk.Frame(notebook)
notebook.add(tab_buscar_tortugas, text="Buscar Tortugas")

# Add a container frame inside tab_buscar_tortugas
container_frame = tk.Frame(tab_buscar_tortugas)
container_frame.pack(fill="both", expand=True)  # Use pack here since notebook uses pack

# Define layout inside container_frame using grid
frame_carga = tk.Frame(container_frame)
frame_carga.grid(row=0, column=0, pady=10, sticky="n")

boton_cargar = tk.Button(frame_carga, text="Buscar Similares", command=buscar_similares, font=("Arial", 14))
boton_cargar.pack(padx=10, pady=10)  # Use pack to let the button take only the necessary space

# Añadir canvas y scrollbar para scroll vertical
canvas_buscar_tortugas = tk.Canvas(container_frame)
scrollbar_buscar_tortugas = ttk.Scrollbar(container_frame, orient="vertical", command=canvas_buscar_tortugas.yview)
canvas_buscar_tortugas.configure(yscrollcommand=scrollbar_buscar_tortugas.set)

canvas_buscar_tortugas.grid(row=1, column=0, sticky="nsew")
scrollbar_buscar_tortugas.grid(row=1, column=1, sticky="ns")

# Configure grid weights to ensure proper resizing
container_frame.grid_rowconfigure(1, weight=1)
container_frame.grid_columnconfigure(0, weight=1)

# Pestaña 3: Placeholder
tab_placeholder = tk.Frame(notebook)
notebook.add(tab_placeholder, text="Puntuación del Algoritmo")

tk.Label(tab_placeholder, text="Puntuación del Algoritmo (Placeholder)", font=("Arial", 16)).pack(pady=50)


# Ejecutar la interfaz
root.mainloop()
