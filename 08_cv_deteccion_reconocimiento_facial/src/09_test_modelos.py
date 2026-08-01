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
# CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# ============================================================================

# Directorio con los datos de entrenamiento (debe contener subdirectorios por persona)
data_path = './Rostros encontrados'

# Modelo a utilizar (descomentar el que corresponda al modelo entrenado)
MODEL_TYPE = 'LBPH'  # Local Binary Patterns Histograms
#MODEL_TYPE = 'EigenFace'  # EigenFaces
#MODEL_TYPE = 'FisherFace'  # FisherFaces

# Archivos de modelos entrenados
MODEL_FILES = {
    'LBPH': 'modeloLBPHFace.xml',
    'EigenFace': 'modeloEigenFace.xml',
    'FisherFace': 'modeloFisherFace.xml'
}

# Umbrales de confianza para cada modelo (menor = más restrictivo)
CONFIDENCE_THRESHOLDS = {
    'LBPH': 70,        # Recomendado: 50-80
    'EigenFace': 5700, # Recomendado: 5000-6000
    'FisherFace': 500  # Recomendado: 400-600
}

# ============================================================================
# VALIDACIÓN DE DATOS
# ============================================================================

# Verificar que el directorio de datos existe
if not os.path.exists(data_path):
    print(f"Error: El directorio '{data_path}' no existe")
    print("\nPor favor, ejecute primero los scripts de captura y entrenamiento")
    exit()

# Cargar nombres de personas (subdirectorios del directorio de datos)
try:
    people_list = [item for item in os.listdir(data_path) 
                   if os.path.isdir(os.path.join(data_path, item))]
    people_list.sort()  # Ordenar alfabéticamente para consistencia
except Exception as e:
    print(f"Error al leer el directorio: {e}")
    exit()

# Verificar que hay personas registradas
if len(people_list) == 0:
    print(f"⚠ Error: No se encontraron personas en '{data_path}'")
    print("\nEl directorio debe contener subdirectorios con nombres de personas:")
    print("  ./Rostros encontrados/")
    print("    ├── Persona1/")
    print("    ├── Persona2/")
    print("    └── Persona3/")
    exit()

# ============================================================================
# INFORMACIÓN INICIAL
# ============================================================================

print("\n" + "=" * 70)
print("RECONOCIMIENTO FACIAL EN TIEMPO REAL")
print("=" * 70)
print(f"Directorio de datos: {data_path}")
print(f"Modelo seleccionado: {MODEL_TYPE}")
print(f"Archivo del modelo: {MODEL_FILES[MODEL_TYPE]}")
print(f"Umbral de confianza: {CONFIDENCE_THRESHOLDS[MODEL_TYPE]}")
print(f"Personas registradas: {len(people_list)}")
print(f"Lista de personas: {people_list}")
print("=" * 70)

# ============================================================================
# CARGA DEL MODELO ENTRENADO
# ============================================================================

print("\nCargando modelo entrenado...")

model_file = MODEL_FILES[MODEL_TYPE]

# Verificar que el archivo del modelo existe
if not os.path.exists(model_file):
    print(f"✗ Error: No se encontró el archivo del modelo '{model_file}'")
    print("\nPor favor, ejecute primero el script de entrenamiento:")
    print("  python 08_modelo_entrenado.py")
    exit()

# Crear el reconocedor según el tipo de modelo
if MODEL_TYPE == 'LBPH':
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
elif MODEL_TYPE == 'EigenFace':
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
elif MODEL_TYPE == 'FisherFace':
    face_recognizer = cv2.face.FisherFaceRecognizer_create()
else:
    print(f"✗ Error: Tipo de modelo '{MODEL_TYPE}' no válido")
    exit()

# Cargar el modelo entrenado
try:
    face_recognizer.read(model_file)
    print(f"✓ Modelo cargado exitosamente desde '{model_file}'")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")
    exit()

# ============================================================================
# CONFIGURACIÓN DE LA CÁMARA
# ============================================================================

# Inicializar captura de video
# Opción 1: Cámara web
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Opción 2: Archivo de video (descomentar para usar)
#cap = cv2.VideoCapture('Video.mp4')

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print("✗ Error: No se pudo abrir la cámara o el video")
    exit()

# Configurar propiedades de la cámara
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✓ Cámara iniciada correctamente")

# ============================================================================
# CONFIGURACIÓN DEL CLASIFICADOR DE ROSTROS
# ============================================================================

# Cargar clasificador Haar Cascade para detección de rostros
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Verificar que el clasificador se cargó correctamente
if faceClassif.empty():
    print("✗ Error: No se pudo cargar el clasificador Haar Cascade")
    cap.release()
    exit()

# ============================================================================
# PARÁMETROS DE RECONOCIMIENTO
# ============================================================================

# Parámetros de detección de rostros
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5
FACE_SIZE = (150, 150)

# Umbral de confianza
confidence_threshold = CONFIDENCE_THRESHOLDS[MODEL_TYPE]

# Variables de estadísticas
frame_count = 0
faces_detected = 0
faces_recognized = 0
faces_unknown = 0

# ============================================================================
# INSTRUCCIONES
# ============================================================================

print("\n" + "=" * 70)
print("INSTRUCCIONES:")
print("  - Presiona 'ESC' para SALIR")
print("  - Presiona '+' para AUMENTAR umbral de confianza")
print("  - Presiona '-' para DISMINUIR umbral de confianza")
print("  - Presiona 'R' para RESETEAR estadísticas")
print("=" * 70)
print("\nIniciando reconocimiento facial en tiempo real...\n")

# ============================================================================
# BUCLE PRINCIPAL DE RECONOCIMIENTO
# ============================================================================

while True:
    # Capturar frame de la cámara
    ret, frame = cap.read()
    
    # Verificar que el frame se capturó correctamente
    if not ret:
        print("⚠ No se pudo leer el frame de la cámara")
        break
    
    frame_count += 1
    
    # Voltear horizontalmente (efecto espejo para mejor usabilidad)
    frame = cv2.flip(frame, 1)
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Crear copia para procesamiento
    aux_frame = gray.copy()
    
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
    # RECONOCIMIENTO DE ROSTROS
    # ========================================================================
    
    for (x, y, w, h) in faces:
        # Extraer región del rostro
        face_roi = aux_frame[y:y+h, x:x+w]
        
        # Redimensionar al tamaño esperado por el modelo
        face_resized = cv2.resize(face_roi, FACE_SIZE, interpolation=cv2.INTER_CUBIC)
        
        # Realizar predicción
        result = face_recognizer.predict(face_resized)
        label = result[0]      # Etiqueta (índice de la persona)
        confidence = result[1]  # Confianza (menor = mejor)
        
        # Determinar si el rostro es reconocido o desconocido
        if confidence < confidence_threshold:
            # Rostro reconocido
            if label < len(people_list):
                person_name = people_list[label]
                faces_recognized += 1
            else:
                person_name = f"ID:{label}"
                faces_unknown += 1
            
            # Dibujar rectángulo verde y nombre
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Fondo para el texto del nombre
            cv2.rectangle(frame, (x, y-35), (x+w, y), (0, 255, 0), -1)
            cv2.putText(frame, person_name, (x+5, y-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Mostrar nivel de confianza
            cv2.putText(frame, f'Conf: {int(confidence)}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            # Rostro desconocido
            faces_unknown += 1
            
            # Dibujar rectángulo rojo
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # Fondo para el texto
            cv2.rectangle(frame, (x, y-35), (x+w, y), (0, 0, 255), -1)
            cv2.putText(frame, 'Desconocido', (x+5, y-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Mostrar nivel de confianza
            cv2.putText(frame, f'Conf: {int(confidence)}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
        faces_detected += 1
    
    # ========================================================================
    # INTERFAZ DE USUARIO EN PANTALLA
    # ========================================================================
    
    # Panel de información superior
    cv2.rectangle(frame, (10, 5), (630, 100), (0, 0, 0), -1)
    cv2.rectangle(frame, (10, 5), (630, 100), (255, 255, 255), 2)
    
    # Título
    cv2.putText(frame, f'Reconocimiento: {MODEL_TYPE}', (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Estadísticas
    cv2.putText(frame, f'Rostros detectados: {len(faces)}', (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.putText(frame, f'Umbral: {confidence_threshold}', (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    
    cv2.putText(frame, f'Frame: {frame_count}', (20, 93),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Instrucciones en la parte inferior
    cv2.rectangle(frame, (10, 440), (630, 470), (0, 0, 0), -1)
    cv2.putText(frame, 'ESC=Salir  +=Aumentar umbral  -=Disminuir umbral  R=Reset', (20, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Mostrar frame
    cv2.imshow('Reconocimiento Facial en Tiempo Real', frame)
    
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
    
    # Presionar 'R' para resetear estadísticas
    elif key == ord('r') or key == ord('R'):
        frame_count = 0
        faces_detected = 0
        faces_recognized = 0
        faces_unknown = 0
        print("Estadísticas reseteadas")

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
print(f"Total de rostros detectados: {faces_detected}")
print(f"Rostros reconocidos: {faces_recognized}")
print(f"Rostros desconocidos: {faces_unknown}")
if faces_detected > 0:
    recognition_rate = (faces_recognized / faces_detected) * 100
    print(f"Tasa de reconocimiento: {recognition_rate:.2f}%")
print(f"Umbral final de confianza: {confidence_threshold}")
print("=" * 70)
print("\n✓ Aplicación finalizada correctamente")