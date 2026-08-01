import cv2
import os
import numpy as np
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# ============================================================================

# Directorio de salida para guardar los rostros capturados
output_dir = 'Rostros encontrados'

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
# CONFIGURACIÓN DE LA CÁMARA
# ============================================================================

# Inicializar la captura de video desde la cámara web
# CAP_DSHOW es específico para Windows y mejora el rendimiento
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

# Configurar propiedades de la cámara (opcional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("Cámara iniciada correctamente")

# ============================================================================
# PARÁMETROS DE CONFIGURACIÓN
# ============================================================================

# Tamaño estándar para redimensionar todos los rostros
FACE_SIZE = (150, 150)

# Parámetros de detección
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5

# ============================================================================
# VARIABLES DE CONTROL
# ============================================================================

# Contador de rostros guardados
count = 0

# Contador de frames procesados
frame_count = 0

# Activar/desactivar ecualización de histograma
use_equalization = True

# ============================================================================
# INSTRUCCIONES
# ============================================================================

print("\n" + "=" * 70)
print("CAPTURA DE ROSTROS DESDE CÁMARA WEB")
print("=" * 70)
print("INSTRUCCIONES:")
print("  - Presiona 'S' para GUARDAR el rostro actual")
print("  - Presiona 'E' para activar/desactivar ECUALIZACIÓN")
print("  - Presiona 'ESC' para SALIR del programa")
print("=" * 70)
print(f"\nDirectorio de salida: {output_dir}")
print("Iniciando captura en tiempo real...\n")

# ============================================================================
# BUCLE PRINCIPAL DE CAPTURA EN TIEMPO REAL
# ============================================================================

while True:
    # Capturar fotograma de la cámara
    ret, frame = cap.read()
    
    # Verificar que el fotograma se capturó correctamente
    if not ret:
        print("Error: No se pudo leer el fotograma de la cámara")
        break
    
    frame_count += 1
    
    # Voltear horizontalmente (efecto espejo)
    frame = cv2.flip(frame, 1)
    
    # Crear una copia del frame para extraer rostros
    frame_aux = frame.copy()
    
    # ========================================================================
    # PREPROCESAMIENTO
    # ========================================================================
    
    # Convertir a escala de grises (requerido para Haar Cascade)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Ecualización de histograma para mejorar el contraste (opcional)
    if use_equalization:
        gray = cv2.equalizeHist(gray)
    
    # ========================================================================
    # DETECCIÓN DE ROSTROS
    # ========================================================================
    
    # Detectar rostros en el frame
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=(30, 30)
    )
    
    # ========================================================================
    # CONTROL DE TECLADO
    # ========================================================================
    
    key = cv2.waitKey(1) & 0xFF
    
    # Presionar ESC para salir
    if key == 27:
        print("\nCerrando aplicación...")
        break
    
    # Presionar 'E' para activar/desactivar ecualización
    elif key == ord('e') or key == ord('E'):
        use_equalization = not use_equalization
        print(f"Ecualización de histograma: {'ACTIVADA' if use_equalization else 'DESACTIVADA'}")
    
    # ========================================================================
    # PROCESAMIENTO Y VISUALIZACIÓN DE ROSTROS
    # ========================================================================
    
    # Variable para rastrear si se guardó algún rostro en este frame
    saved_in_frame = False
    
    # Procesar cada rostro detectado
    for i, (x, y, w, h) in enumerate(faces):
        # Dibujar rectángulo verde alrededor del rostro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Añadir etiqueta con número de rostro
        cv2.putText(frame, f'Rostro #{i+1}', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Extraer la región del rostro
        rostro = frame_aux[y:y+h, x:x+w]
        
        # Redimensionar el rostro a tamaño estándar
        rostro_resized = cv2.resize(rostro, FACE_SIZE, interpolation=cv2.INTER_CUBIC)
        
        # Presionar 'S' para guardar el rostro
        if key == ord('s') or key == ord('S'):
            # Generar nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'rostro_{count}_{timestamp}.jpg'
            filepath = os.path.join(output_dir, filename)
            
            # Guardar el rostro
            cv2.imwrite(filepath, rostro_resized)
            
            # Mostrar el rostro guardado en una ventana temporal
            cv2.imshow('Rostro Guardado', rostro_resized)
            
            # Información en consola
            print(f"✓ Rostro #{count} guardado:")
            print(f"  - Archivo: {filepath}")
            print(f"  - Tamaño: {FACE_SIZE[0]}x{FACE_SIZE[1]} píxeles")
            print(f"  - Posición: ({x}, {y}), Tamaño original: {w}x{h}")
            print("-" * 70)
            
            count += 1
            saved_in_frame = True
    
    # ========================================================================
    # INTERFAZ DE USUARIO EN PANTALLA
    # ========================================================================
    
    # Banner superior con instrucciones
    cv2.rectangle(frame, (10, 5), (630, 35), (255, 255, 255), -1)
    instruction_text = 'S=Guardar | E=Ecualizar | ESC=Salir'
    cv2.putText(frame, instruction_text, (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 128, 0), 2, cv2.LINE_AA)
    
    # Banner con información de estado
    cv2.rectangle(frame, (10, 40), (630, 95), (240, 240, 240), -1)
    
    # Línea 1: Rostros detectados y guardados
    info_text1 = f'Rostros detectados: {len(faces)} | Total guardados: {count}'
    cv2.putText(frame, info_text1, (15, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Línea 2: Estado de ecualización
    eq_status = "ON" if use_equalization else "OFF"
    info_text2 = f'Ecualizacion: {eq_status} | Frame: {frame_count}'
    cv2.putText(frame, info_text2, (15, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    
    # Indicador visual si se guardó un rostro
    if saved_in_frame:
        cv2.rectangle(frame, (10, 100), (630, 130), (0, 255, 0), -1)
        cv2.putText(frame, 'ROSTRO GUARDADO!', (15, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Mostrar el frame con las detecciones
    cv2.imshow('Captura de Rostros - Camara Web', frame)

# ============================================================================
# RESUMEN Y LIMPIEZA
# ============================================================================

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

# Mostrar resumen final
print("\n" + "=" * 70)
print("RESUMEN DE CAPTURA")
print("=" * 70)
print(f"Total de frames procesados: {frame_count}")
print(f"Total de rostros guardados: {count}")
print(f"Directorio de salida: {output_dir}")
print(f"Tamaño de rostros: {FACE_SIZE[0]}x{FACE_SIZE[1]} píxeles")
print("=" * 70)
print("\nProcesamiento completado exitosamente")