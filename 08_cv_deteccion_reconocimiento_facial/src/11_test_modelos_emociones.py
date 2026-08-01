import cv2
import os
import numpy as np

# ============================================================================
# VERIFICACIÓN DE MÓDULOS REQUERIDOS
# ============================================================================

try:
    _ = cv2.face
    print("✓ Módulo cv2.face disponible")
except AttributeError:
    print("\n" + "=" * 70)
    print("ERROR: El módulo cv2.face no está disponible")
    print("=" * 70)
    print("\nInstale opencv-contrib-python:")
    print("  pip uninstall opencv-python")
    print("  pip install opencv-contrib-python")
    print("=" * 70)
    exit()

# ============================================================================
# FUNCIÓN PARA CARGAR IMAGEN DE EMOCIÓN
# ============================================================================

def load_emotion_image(emotion, target_height=480, target_width=300):
    """
    Carga y redimensiona una imagen de emoji según la emoción detectada.
    
    Args:
        emotion (str): Nombre de la emoción
        target_height (int): Alto objetivo de la imagen
        target_width (int): Ancho objetivo de la imagen
    
    Returns:
        numpy.ndarray: Imagen del emoji redimensionada
    """
    # Imagen negra por defecto
    default_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    
    # Agregar texto indicando que no hay emoji
    cv2.putText(default_image, 'No hay emoji', (50, target_height//2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(default_image, f'para: {emotion}', (50, target_height//2 + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Normalizar nombre de emoción
    emotion_lower = emotion.lower().strip()
    
    # Corregir errores de ortografía comunes
    emotion_corrections = {
        'tristreza': 'tristeza',
        'alegría': 'alegria',
        'enojo': 'furia',
        'asco': 'desagrado'
    }
    
    emotion_lower = emotion_corrections.get(emotion_lower, emotion_lower)
    
    # Mapeo de emociones a rutas de imágenes
    emotion_paths = {
        'alegria': '../Emojis/alegria.jpg',
        'furia': '../Emojis/furia.jpg',
        'desagrado': '../Emojis/desagrado.jpg',
        'tristeza': '../Emojis/tristeza.jpg',
        # Agregar más emociones según sea necesario
    }
    
    image_path = emotion_paths.get(emotion_lower)
    
    # Cargar y redimensionar la imagen si existe
    if image_path and os.path.exists(image_path):
        image = cv2.imread(image_path)
        if image is not None:
            # Redimensionar al tamaño objetivo
            image = cv2.resize(image, (target_width, target_height), 
                             interpolation=cv2.INTER_CUBIC)
            return image
        else:
            print(f"⚠ No se pudo cargar la imagen: {image_path}")
    else:
        if image_path:
            print(f"⚠ Archivo no encontrado: {image_path}")
        else:
            print(f"⚠ No hay emoji definido para la emoción: {emotion}")
    
    return default_image

# ============================================================================
# CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# ============================================================================

# Directorio con datos de emociones
data_path = './Rostros encontrados/emociones'

# Modelo a utilizar (descomentar el que corresponda al modelo entrenado)
MODEL_TYPE = 'LBPH'  # Recomendado
#MODEL_TYPE = 'EigenFaces'
#MODEL_TYPE = 'FisherFaces'

# Umbrales de confianza para cada modelo
CONFIDENCE_THRESHOLDS = {
    'LBPH': 60,        # Recomendado: 50-70
    'EigenFaces': 5700,
    'FisherFaces': 500
}

# Dimensiones del panel de emoji
EMOJI_HEIGHT = 480
EMOJI_WIDTH = 300

# ============================================================================
# VALIDACIÓN DE DATOS
# ============================================================================

# Verificar que el directorio de datos existe
if not os.path.exists(data_path):
    print(f"Error: El directorio '{data_path}' no existe")
    print("\nEjecute primero: 10_entrenamiento_emociones.py")
    exit()

# Cargar nombres de emociones (subdirectorios)
try:
    emotions_list = [item for item in os.listdir(data_path) 
                     if os.path.isdir(os.path.join(data_path, item))]
    emotions_list.sort()  # Ordenar alfabéticamente
except Exception as e:
    print(f"Error al leer el directorio: {e}")
    exit()

# Verificar que hay emociones registradas
if len(emotions_list) == 0:
    print(f"⚠ Error: No se encontraron emociones en '{data_path}'")
    exit()

# ============================================================================
# INFORMACIÓN INICIAL
# ============================================================================

print("\n" + "=" * 70)
print("RECONOCIMIENTO DE EMOCIONES EN TIEMPO REAL")
print("=" * 70)
print(f"Directorio de datos: {data_path}")
print(f"Modelo seleccionado: {MODEL_TYPE}")
print(f"Umbral de confianza: {CONFIDENCE_THRESHOLDS[MODEL_TYPE]}")
print(f"Emociones registradas: {len(emotions_list)}")
print(f"Lista de emociones: {emotions_list}")
print("=" * 70)

# ============================================================================
# CARGA DEL MODELO ENTRENADO
# ============================================================================

print("\nCargando modelo entrenado...")

model_file = f"modelo{MODEL_TYPE}.xml"

# Verificar que el archivo del modelo existe
if not os.path.exists(model_file):
    print(f"✗ Error: No se encontró el archivo del modelo '{model_file}'")
    print("\nEjecute primero: python 10_entrenamiento_emociones.py")
    exit()

# Crear el reconocedor según el tipo de modelo
if MODEL_TYPE == 'LBPH':
    emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
elif MODEL_TYPE == 'EigenFaces':
    emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
elif MODEL_TYPE == 'FisherFaces':
    emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
else:
    print(f"✗ Error: Tipo de modelo '{MODEL_TYPE}' no válido")
    exit()

# Cargar el modelo
try:
    emotion_recognizer.read(model_file)
    print(f"✓ Modelo cargado exitosamente desde '{model_file}'")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")
    exit()

# ============================================================================
# CONFIGURACIÓN DE LA CÁMARA
# ============================================================================

# Inicializar captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print("✗ Error: No se pudo abrir la cámara")
    exit()

# Configurar propiedades de la cámara
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✓ Cámara iniciada correctamente")

# ============================================================================
# CONFIGURACIÓN DEL CLASIFICADOR DE ROSTROS
# ============================================================================

# Cargar clasificador Haar Cascade
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Verificar que el clasificador se cargó correctamente
if faceClassif.empty():
    print("✗ Error: No se pudo cargar el clasificador Haar Cascade")
    cap.release()
    exit()

# ============================================================================
# PARÁMETROS DE RECONOCIMIENTO
# ============================================================================

SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5
FACE_SIZE = (150, 150)

confidence_threshold = CONFIDENCE_THRESHOLDS[MODEL_TYPE]

# Variables de estadísticas
frame_count = 0
emotions_detected = {}

# ============================================================================
# INSTRUCCIONES
# ============================================================================

print("\n" + "=" * 70)
print("INSTRUCCIONES:")
print("  - Presiona 'ESC' para SALIR")
print("  - Presiona '+' para AUMENTAR umbral de confianza")
print("  - Presiona '-' para DISMINUIR umbral de confianza")
print("=" * 70)
print("\nIniciando reconocimiento de emociones...\n")

# ============================================================================
# BUCLE PRINCIPAL DE RECONOCIMIENTO
# ============================================================================

while True:
    # Capturar frame de la cámara
    ret, frame = cap.read()
    
    if not ret:
        print("⚠ No se pudo leer el frame de la cámara")
        break
    
    frame_count += 1
    
    # Voltear horizontalmente (efecto espejo)
    frame = cv2.flip(frame, 1)
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aux_frame = gray.copy()
    
    # Panel negro por defecto para el emoji
    emoji_panel = np.zeros((EMOJI_HEIGHT, EMOJI_WIDTH, 3), dtype=np.uint8)
    
    # Agregar título al panel
    cv2.putText(emoji_panel, 'EMOCION DETECTADA', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    
    # ========================================================================
    # DETECCIÓN DE ROSTROS
    # ========================================================================
    
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=(100, 100)
    )
    
    # ========================================================================
    # RECONOCIMIENTO DE EMOCIONES
    # ========================================================================
    
    for (x, y, w, h) in faces:
        # Extraer región del rostro
        face_roi = aux_frame[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, FACE_SIZE, interpolation=cv2.INTER_CUBIC)
        
        # Realizar predicción
        result = emotion_recognizer.predict(face_resized)
        label = result[0]
        confidence = result[1]
        
        # Determinar si la emoción es reconocida
        if confidence < confidence_threshold and label < len(emotions_list):
            # Emoción reconocida
            emotion_name = emotions_list[label]
            
            # Actualizar estadísticas
            emotions_detected[emotion_name] = emotions_detected.get(emotion_name, 0) + 1
            
            # Dibujar rectángulo verde
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Fondo para el texto
            cv2.rectangle(frame, (x, y-35), (x+w, y), (0, 255, 0), -1)
            cv2.putText(frame, emotion_name, (x+5, y-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Nivel de confianza
            cv2.putText(frame, f'Conf: {int(confidence)}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            
            # Cargar emoji de la emoción
            emoji_panel = load_emotion_image(emotion_name, EMOJI_HEIGHT, EMOJI_WIDTH)
            
        else:
            # Emoción no identificada
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            cv2.rectangle(frame, (x, y-35), (x+w, y), (0, 0, 255), -1)
            cv2.putText(frame, 'No identificado', (x+5, y-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            cv2.putText(frame, f'Conf: {int(confidence)}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    
    # ========================================================================
    # PANEL DE INFORMACIÓN
    # ========================================================================
    
    # Agregar información en el panel de emoji
    cv2.putText(emoji_panel, f'Modelo: {MODEL_TYPE}', (20, EMOJI_HEIGHT-60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.putText(emoji_panel, f'Umbral: {confidence_threshold}', (20, EMOJI_HEIGHT-35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.putText(emoji_panel, f'Frame: {frame_count}', (20, EMOJI_HEIGHT-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Concatenar frame con panel de emoji
    combined_frame = cv2.hconcat([frame, emoji_panel])
    
    # Mostrar frame combinado
    cv2.imshow('Reconocimiento de Emociones - ESC para salir', combined_frame)
    
    # ========================================================================
    # CONTROL DE TECLADO
    # ========================================================================
    
    key = cv2.waitKey(1) & 0xFF
    
    # Presionar ESC para salir
    if key == 27:
        print("\nCerrando aplicación...")
        break
    
    # Presionar '+' para aumentar umbral
    elif key == ord('+') or key == ord('='):
        confidence_threshold += 5
        print(f"Umbral aumentado a: {confidence_threshold}")
    
    # Presionar '-' para disminuir umbral
    elif key == ord('-') or key == ord('_'):
        confidence_threshold = max(0, confidence_threshold - 5)
        print(f"Umbral disminuido a: {confidence_threshold}")

# ============================================================================
# LIMPIEZA Y RESUMEN FINAL
# ============================================================================

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

# Mostrar estadísticas finales
print("\n" + "=" * 70)
print("ESTADÍSTICAS FINALES")
print("=" * 70)
print(f"Total de frames procesados: {frame_count}")
print(f"\nEmociones detectadas:")
if emotions_detected:
    for emotion, count in sorted(emotions_detected.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {emotion}: {count} veces")
else:
    print("  No se detectaron emociones")
print("=" * 70)
print("\n✓ Aplicación finalizada correctamente")