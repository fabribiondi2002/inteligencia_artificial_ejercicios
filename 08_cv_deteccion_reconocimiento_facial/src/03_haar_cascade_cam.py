import cv2
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE CLASIFICADORES HAAR CASCADE
# ============================================================================
# Descomentar el clasificador que se desea utilizar según el objeto a detectar

# Detección de ojos con lentes
faceClassif = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# Detección de sonrisas
#faceClassif = cv2.CascadeClassifier('haarcascade_smile.xml')

# Detección de rostros (método alternativo según versión de OpenCV)
#faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Verificar que el clasificador se cargó correctamente
if faceClassif.empty():
    print("Error: No se pudo cargar el clasificador Haar Cascade")
    exit()

# ============================================================================
# CONFIGURACIÓN DE LA CÁMARA
# ============================================================================

# Inicializar la captura de video desde la cámara web (0 = cámara por defecto)
cap = cv2.VideoCapture(0)

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

# Configurar propiedades de la cámara (opcional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Ancho del frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto del frame
cap.set(cv2.CAP_PROP_FPS, 30)            # Frames por segundo

print("Cámara iniciada correctamente")
print("Presiona 'q' para salir")
print("Presiona 'e' para activar/desactivar ecualización")
print("-" * 50)

# ============================================================================
# VARIABLES DE CONTROL
# ============================================================================

frame_count = 0
use_equalization = True  # Activar/desactivar ecualización de histograma

# ============================================================================
# BUCLE PRINCIPAL DE DETECCIÓN EN TIEMPO REAL
# ============================================================================

while True:
    # Capturar fotograma de la cámara
    ret, frame = cap.read()
    
    # Verificar que el fotograma se capturó correctamente
    if not ret:
        print("Error: No se pudo leer el fotograma de la cámara")
        break
    
    frame_count += 1
    
    # Crear una copia del frame original para mostrar
    frame_display = frame.copy()
    
    # ========================================================================
    # PREPROCESAMIENTO
    # ========================================================================
    
    # Convertir a escala de grises (requerido para Haar Cascade)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Ecualización de histograma para mejorar el contraste (opcional)
    if use_equalization:
        gray = cv2.equalizeHist(gray)
    
    # ========================================================================
    # DETECCIÓN DE OBJETOS
    # ========================================================================
    
    # Configuración principal de detección
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=1.1,      # Factor de escala entre niveles de la pirámide de imágenes
        minNeighbors=5,       # Mínimo de vecinos para considerar una detección válida
        minSize=(30, 30),     # Tamaño mínimo del objeto a detectar
        maxSize=(200, 200)    # Tamaño máximo del objeto a detectar
    )
    
    # Configuración alternativa más restrictiva (descomentar para probar)
    '''
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=1.5,      # Escalado más grande = menos detecciones pero más rápido
        minNeighbors=25,      # Más vecinos = detecciones más confiables pero menos sensibles
        minSize=(30, 30),     # Tamaño mínimo del objeto
        maxSize=(100, 100)    # Tamaño máximo del objeto
    )
    '''
    
    # ========================================================================
    # VISUALIZACIÓN DE RESULTADOS
    # ========================================================================
    
    # Dibujar rectángulos alrededor de los objetos detectados
    for i, (x, y, w, h) in enumerate(faces):
        # Dibujar rectángulo verde con grosor de 2 píxeles
        cv2.rectangle(frame_display, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Añadir etiqueta con número de detección
        cv2.putText(frame_display, f'#{i+1}', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Información en pantalla
    info_text = f'Detecciones: {len(faces)} | Frame: {frame_count}'
    cv2.putText(frame_display, info_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Indicador de ecualización
    eq_text = f'Ecualizacion: {"ON" if use_equalization else "OFF"}'
    cv2.putText(frame_display, eq_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Mostrar el frame con las detecciones
    cv2.imshow('Deteccion en Tiempo Real - Presiona Q para salir', frame_display)
    
    # ========================================================================
    # CONTROL DE TECLADO
    # ========================================================================
    
    key = cv2.waitKey(1) & 0xFF
    
    # Presionar 'q' para salir
    if key == ord('q'):
        print("\nCerrando aplicación...")
        break
    
    # Presionar 'e' para activar/desactivar ecualización
    elif key == ord('e'):
        use_equalization = not use_equalization
        print(f"Ecualización de histograma: {'ACTIVADA' if use_equalization else 'DESACTIVADA'}")
    
    # Presionar 's' para tomar una captura
    elif key == ord('s'):
        filename = f'captura_frame_{frame_count}.png'
        cv2.imwrite(filename, frame_display)
        print(f"Captura guardada: {filename}")

# ============================================================================
# LIMPIEZA Y CIERRE
# ============================================================================

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

print(f"\nEstadísticas finales:")
print(f"Total de frames procesados: {frame_count}")
print("Programa finalizado correctamente")
