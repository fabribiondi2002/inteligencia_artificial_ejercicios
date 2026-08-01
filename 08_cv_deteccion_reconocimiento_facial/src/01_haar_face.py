import cv2
import numpy as np

# Cargar el clasificador Haar Cascade para patentes rusas
plateClassif = cv2.CascadeClassifier('./haarcascade_russian_plate_number.xml')

# También podemos probar con el clasificador de 16 etapas
# plateClassif = cv2.CascadeClassifier('./haarcascade_license_plate_rus_16stages.xml')

# Leer la imagen
image = cv2.imread('../img/patente.png')
if image is None:
    print("Error: No se pudo cargar la imagen")
    exit()

# Crear una copia para mostrar resultados
image_display = image.copy()

# Convertir a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocesamiento: ecualización de histograma para mejorar el contraste
gray = cv2.equalizeHist(gray)

# Aplicar un filtro bilateral para reducir ruido pero mantener bordes
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Detectar patentes con parámetros optimizados
plates = plateClassif.detectMultiScale(
    gray,
    scaleFactor=1.05,      # Menor escala = más detección (más lento pero más preciso)
    minNeighbors=3,        # Menos vecinos = más detecciones candidatas
    minSize=(80, 20),      # Tamaño mínimo típico de una patente
    maxSize=(400, 150),    # Tamaño máximo típico de una patente
    flags=cv2.CASCADE_SCALE_IMAGE
)

print(f"Patentes detectadas: {len(plates)}")

# Dibujar rectángulos alrededor de las patentes detectadas
for i, (x, y, w, h) in enumerate(plates):
    # Dibujar rectángulo verde
    cv2.rectangle(image_display, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
    # Añadir texto con información
    cv2.putText(image_display, f'Patente #{i+1}', (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Extraer y mostrar la región de la patente
    plate_roi = image[y:y+h, x:x+w]
    cv2.imshow(f'Patente #{i+1}', plate_roi)
    
    print(f"Patente #{i+1}: Posición ({x}, {y}), Tamaño {w}x{h}")

# Mostrar imagen con detecciones
cv2.imshow('Deteccion de Patentes', image_display)
print("\nPresiona cualquier tecla para cerrar las ventanas...")
cv2.waitKey(0)
cv2.destroyAllWindows()