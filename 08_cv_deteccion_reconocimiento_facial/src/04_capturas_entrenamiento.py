import cv2
import os
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# ============================================================================

# Directorio de salida para guardar las capturas de rostros
output_dir = '../img/capturas'

# Crear la carpeta capturas si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directorio creado: {output_dir}")
else:
    print(f"Usando directorio existente: {output_dir}")

# ============================================================================
# CONFIGURACIÓN DEL CLASIFICADOR HAAR CASCADE
# ============================================================================

# Cargar el clasificador para detección de rostros frontales
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Verificar que el clasificador se cargó correctamente
if faceClassif.empty():
    print("Error: No se pudo cargar el clasificador Haar Cascade")
    exit()

# ============================================================================
# CARGA Y VERIFICACIÓN DE LA IMAGEN
# ============================================================================

# Ruta de la imagen con rostros para entrenar
image_path = '../img/caras_para_entrenar.png'

# Leer la imagen
image = cv2.imread(image_path)

# Verificar que la imagen se cargó correctamente
if image is None:
    print(f"Error: No se pudo cargar la imagen desde {image_path}")
    exit()

print(f"Imagen cargada: {image_path}")
print(f"Dimensiones de la imagen: {image.shape[1]}x{image.shape[0]} píxeles")

# Crear una copia de la imagen original para extraer rostros
image_aux = image.copy()

# ============================================================================
# PREPROCESAMIENTO DE LA IMAGEN
# ============================================================================

# Convertir a escala de grises (requerido para Haar Cascade)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Ecualización de histograma para mejorar el contraste
gray = cv2.equalizeHist(gray)

# ============================================================================
# DETECCIÓN DE ROSTROS
# ============================================================================

print("\nDetectando rostros...")

# Detectar rostros en la imagen
faces = faceClassif.detectMultiScale(
    gray,
    scaleFactor=1.2,      # Factor de escala entre niveles de la pirámide de imágenes
    minNeighbors=10,      # Mínimo de vecinos para considerar una detección válida
    minSize=(30, 30)      # Tamaño mínimo del rostro a detectar
)

print(f"Rostros detectados: {len(faces)}")

# ============================================================================
# EXTRACCIÓN Y GUARDADO DE ROSTROS
# ============================================================================

# Contador de rostros guardados
count = 0

# Tamaño estándar para redimensionar todos los rostros
FACE_SIZE = (150, 150)

print("\nPresiona cualquier tecla para pasar al siguiente rostro...")
print("-" * 60)

# Procesar cada rostro detectado
for i, (x, y, w, h) in enumerate(faces):
    
    # Dibujar rectángulo morado alrededor del rostro
    cv2.rectangle(image, (x, y), (x+w, y+h), (128, 0, 255), 2)
    
    # Añadir etiqueta con número de rostro
    cv2.putText(image, f'Rostro #{i+1}', (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 0, 255), 2)
    
    # Extraer la región del rostro de la imagen original
    rostro = image_aux[y:y+h, x:x+w]
    
    # Redimensionar el rostro a un tamaño estándar para el entrenamiento
    # Interpolación cúbica para mejor calidad
    rostro_resized = cv2.resize(rostro, FACE_SIZE, interpolation=cv2.INTER_CUBIC)
    
    # Generar nombre del archivo
    filename = f'rostro_{count}.jpg'
    filepath = os.path.join(output_dir, filename)
    
    # Guardar el rostro redimensionado
    cv2.imwrite(filepath, rostro_resized)
    
    # Información en consola
    print(f"Rostro #{i+1}:")
    print(f"  - Posición: ({x}, {y})")
    print(f"  - Tamaño original: {w}x{h}")
    print(f"  - Tamaño redimensionado: {FACE_SIZE[0]}x{FACE_SIZE[1]}")
    print(f"  - Guardado en: {filepath}")
    print("-" * 60)
    
    # Incrementar contador
    count += 1
    
    # Mostrar el rostro extraído y redimensionado
    cv2.imshow('Rostro Extraido', rostro_resized)
    
    # Mostrar la imagen completa con el rectángulo
    cv2.imshow('Imagen con Detecciones', image)
    
    # Esperar a que el usuario presione una tecla para continuar
    cv2.waitKey(0)

# ============================================================================
# RESUMEN Y LIMPIEZA
# ============================================================================

# Cerrar todas las ventanas
cv2.destroyAllWindows()

# Mostrar resumen final
print("\n" + "=" * 60)
print("RESUMEN DE PROCESAMIENTO")
print("=" * 60)
print(f"Total de rostros detectados: {len(faces)}")
print(f"Total de rostros guardados: {count}")
print(f"Directorio de salida: {output_dir}")
print(f"Tamaño de rostros: {FACE_SIZE[0]}x{FACE_SIZE[1]} píxeles")
print("=" * 60)
print("\nProcesamiento completado exitosamente")