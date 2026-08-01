import cv2
import os
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# ============================================================================

# Directorio de entrada con imágenes a procesar
images_path = "../imagenes"

# Directorio de salida para guardar los rostros encontrados
output_dir = 'Rostros encontrados'

# Verificar que el directorio de entrada existe
if not os.path.exists(images_path):
    print(f"Error: El directorio '{images_path}' no existe")
    print("Por favor, cree el directorio y agregue imágenes para procesar")
    exit()

# Obtener lista de imágenes en el directorio
try:
    images_path_list = os.listdir(images_path)
    # Filtrar solo archivos de imagen comunes
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    images_path_list = [img for img in images_path_list 
                        if os.path.splitext(img)[1].lower() in valid_extensions]
except Exception as e:
    print(f"Error al leer el directorio: {e}")
    exit()

# Verificar que hay imágenes para procesar
if len(images_path_list) == 0:
    print(f"Error: No se encontraron imágenes en '{images_path}'")
    print(f"Formatos válidos: {', '.join(valid_extensions)}")
    exit()

print(f"Directorio de entrada: {images_path}")
print(f"Total de imágenes encontradas: {len(images_path_list)}")

# Crear directorio de salida si no existe
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
# PARÁMETROS DE CONFIGURACIÓN
# ============================================================================

# Tamaño estándar para redimensionar todos los rostros
FACE_SIZE = (150, 150)

# Parámetros de detección
SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 5

# ============================================================================
# VARIABLES DE CONTROL
# ============================================================================

# Contador global de rostros guardados
count = 0

# Estadísticas
total_images_processed = 0
total_images_with_faces = 0
total_faces_saved = 0

print("\n" + "=" * 70)
print("INSTRUCCIONES")
print("=" * 70)
print("- Presiona 'S' para GUARDAR los rostros encontrados en la imagen actual")
print("- Presiona 'N' o cualquier otra tecla para OMITIR la imagen sin guardar")
print("- Presiona 'ESC' para SALIR del programa")
print("=" * 70)
print("\nIniciando procesamiento...\n")

# ============================================================================
# PROCESAMIENTO DE IMÁGENES
# ============================================================================

# Procesar cada imagen en el directorio
for idx, image_name in enumerate(images_path_list, 1):
    
    # Construir ruta completa de la imagen
    image_path = os.path.join(images_path, image_name)
    
    # Leer la imagen
    image = cv2.imread(image_path)
    
    # Verificar que la imagen se cargó correctamente
    if image is None:
        print(f"[{idx}/{len(images_path_list)}] Error: No se pudo cargar '{image_name}'. Omitiendo...")
        continue
    
    total_images_processed += 1
    
    # Crear una copia de la imagen original para extraer rostros
    image_aux = image.copy()
    
    # Convertir a escala de grises (requerido para Haar Cascade)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Ecualización de histograma para mejorar el contraste
    gray = cv2.equalizeHist(gray)
    
    # ========================================================================
    # DETECCIÓN DE ROSTROS
    # ========================================================================
    
    # Detectar rostros en la imagen
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=(30, 30)
    )
    
    # ========================================================================
    # VISUALIZACIÓN
    # ========================================================================
    
    # Dibujar rectángulos alrededor de los rostros detectados
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Añadir número de rostro
        cv2.putText(image, f'#{i+1}', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Crear banner con instrucciones en la parte superior
    cv2.rectangle(image, (10, 5), (640, 35), (255, 255, 255), -1)
    instruction_text = f'Imagen {idx}/{len(images_path_list)} - Rostros: {len(faces)} | S=Guardar N=Omitir ESC=Salir'
    cv2.putText(image, instruction_text, (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 0), 1, cv2.LINE_AA)
    
    # Banner con nombre de archivo
    cv2.rectangle(image, (10, 40), (640, 65), (240, 240, 240), -1)
    cv2.putText(image, f'Archivo: {image_name}', (15, 58),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Mostrar la imagen con las detecciones
    cv2.imshow('Deteccion de Rostros - Procesando Directorio', image)
    
    # Información en consola
    print("-" * 70)
    print(f"[{idx}/{len(images_path_list)}] Procesando: {image_name}")
    print(f"  - Dimensiones: {image.shape[1]}x{image.shape[0]} píxeles")
    print(f"  - Rostros detectados: {len(faces)}")
    
    # ========================================================================
    # CONTROL DE TECLADO
    # ========================================================================
    
    # Esperar entrada del usuario
    key = cv2.waitKey(0)
    
    # Presionar 'S' para guardar los rostros
    if key == ord('s') or key == ord('S'):
        if len(faces) > 0:
            total_images_with_faces += 1
            saved_count = 0
            
            for i, (x, y, w, h) in enumerate(faces):
                # Extraer la región del rostro
                rostro = image_aux[y:y + h, x:x + w]
                
                # Redimensionar el rostro a tamaño estándar
                rostro_resized = cv2.resize(rostro, FACE_SIZE, interpolation=cv2.INTER_CUBIC)
                
                # Generar nombre del archivo
                filename = f'rostro_{count}.jpg'
                filepath = os.path.join(output_dir, filename)
                
                # Guardar el rostro
                cv2.imwrite(filepath, rostro_resized)
                
                print(f"  Rostro #{i+1} guardado: {filepath}")
                
                count += 1
                saved_count += 1
            
            total_faces_saved += saved_count
            print(f"  Total guardados de esta imagen: {saved_count}")
        else:
            print("  No hay rostros para guardar en esta imagen")
    
    # Presionar ESC para salir
    elif key == 27:
        print("\n Proceso interrumpido por el usuario")
        break
    
    # Cualquier otra tecla omite la imagen
    else:
        print("  Imagen omitida (no se guardaron rostros)")

# ============================================================================
# RESUMEN Y LIMPIEZA
# ============================================================================

# Cerrar todas las ventanas
cv2.destroyAllWindows()

# Mostrar resumen final
print("\n" + "=" * 70)
print("RESUMEN DE PROCESAMIENTO")
print("=" * 70)
print(f"Total de imágenes en el directorio: {len(images_path_list)}")
print(f"Total de imágenes procesadas: {total_images_processed}")
print(f"Total de imágenes con rostros guardados: {total_images_with_faces}")
print(f"Total de rostros guardados: {total_faces_saved}")
print(f"Directorio de entrada: {images_path}")
print(f"Directorio de salida: {output_dir}")
print(f"Tamaño de rostros: {FACE_SIZE[0]}x{FACE_SIZE[1]} píxeles")
print("=" * 70)
print("\nProcesamiento completado exitosamente")