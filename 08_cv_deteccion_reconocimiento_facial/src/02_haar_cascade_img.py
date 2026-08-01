import cv2
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE CLASIFICADORES HAAR CASCADE
# ============================================================================
# Descomentar el clasificador que se desea utilizar según el objeto a detectar

# Detección de ojos con lentes
faceClassif = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# Detección de caras de gatos
#faceClassif = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
#faceClassif = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')

# Detección de rostros humanos (variantes)
#faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
#faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')

# Detección de cuerpo completo
#faceClassif = cv2.CascadeClassifier('haarcascade_fullbody.xml')

# Detección de ojos específicos
#faceClassif = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')

# Detección de patentes rusas
#faceClassif = cv2.CascadeClassifier('haarcascade_license_plate_rus_16stages.xml')
#faceClassif = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Detección de sonrisas
#faceClassif = cv2.CascadeClassifier('haarcascade_smile.xml')

# ============================================================================
# SELECCIÓN DE IMAGEN
# ============================================================================
# Descomentar la imagen que se desea procesar (están en la carpeta ../img/)

image = cv2.imread('../img/cara.jpg')
#image = cv2.imread('../img/gatos.jpg')
#image = cv2.imread('../img/caras.png')
#image = cv2.imread('../img/caminando.png')
#image = cv2.imread('../img/ironman.jpg')
#image = cv2.imread('../img/patente.png')
#image = cv2.imread('../img/sonrisas.png')

# Verificar que la imagen se cargó correctamente
if image is None:
    print("Error: No se pudo cargar la imagen")
    exit()

# Crear una copia para mostrar resultados
image_display = image.copy()

# ============================================================================
# PREPROCESAMIENTO DE LA IMAGEN
# ============================================================================

# Convertir a escala de grises (requerido para Haar Cascade)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Ecualización de histograma para mejorar el contraste
gray = cv2.equalizeHist(gray) # https://docs.opencv.org/3.4/d4/d1b/tutorial_histogram_equalization.html

# ============================================================================
# DETECCIÓN DE OBJETOS
# ============================================================================

# Aplicar el clasificador Haar Cascade
faces = faceClassif.detectMultiScale(
    gray,
    scaleFactor=1.1,      # Factor de escala entre niveles de la pirámide de imágenes
    minNeighbors=5,       # Mínimo de vecinos para considerar una detección válida
    minSize=(30, 30),     # Tamaño mínimo del objeto a detectar
    maxSize=(200, 200)    # Tamaño máximo del objeto a detectar
)

print(f"Objetos detectados: {len(faces)}")

# ============================================================================
# VISUALIZACIÓN DE RESULTADOS
# ============================================================================

# Dibujar rectángulos alrededor de los objetos detectados
for i, (x, y, w, h) in enumerate(faces):
    # Dibujar rectángulo verde con grosor de 2 píxeles
    cv2.rectangle(image_display, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Añadir etiqueta con número de detección
    cv2.putText(image_display, f'#{i+1}', (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Mostrar información en consola
    print(f"Detección #{i+1}: Posición ({x}, {y}), Tamaño {w}x{h}")

# Mostrar la imagen con las detecciones
cv2.imshow('Deteccion Haar Cascade', image_display)
print("\nPresiona cualquier tecla para cerrar la ventana...")
cv2.waitKey(0)
cv2.destroyAllWindows()