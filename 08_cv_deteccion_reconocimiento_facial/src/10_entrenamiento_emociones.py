import cv2
import os
import numpy as np
import time

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
# FUNCIÓN PARA ENTRENAR Y GUARDAR MODELOS
# ============================================================================

def train_model(method, faces_data, labels, emotion_to_name):
    """
    Entrena y guarda un modelo de reconocimiento de emociones.
    
    Args:
        method (str): Tipo de modelo ('EigenFaces', 'FisherFaces', 'LBPH')
        faces_data (list): Lista de imágenes de rostros
        labels (list): Lista de etiquetas correspondientes
        emotion_to_name (dict): Diccionario de mapeo etiqueta->emoción
    
    Returns:
        tuple: (tiempo_entrenamiento, nombre_archivo)
    """
    print(f"\n[Entrenando modelo: {method}]")
    print("-" * 70)
    
    # Crear el reconocedor según el método
    if method == 'EigenFaces':
        emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
        print("  Tipo: EigenFaces (PCA)")
    elif method == 'FisherFaces':
        emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
        print("  Tipo: FisherFaces (LDA)")
    elif method == 'LBPH':
        emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
        print("  Tipo: LBPH (Local Binary Patterns Histograms)")
    else:
        print(f"  ✗ Error: Método '{method}' no válido")
        return None, None
    
    # Entrenar el modelo
    print(f"  Entrenando con {len(faces_data)} imágenes...")
    
    try:
        start_time = time.time()
        emotion_recognizer.train(faces_data, np.array(labels))
        training_time = time.time() - start_time
        
        print(f"  ✓ Entrenamiento completado en {training_time:.2f} segundos")
        
    except Exception as e:
        print(f"  ✗ Error durante el entrenamiento: {e}")
        return None, None
    
    # Guardar el modelo
    model_filename = f"modelo{method}.xml"
    
    try:
        emotion_recognizer.write(model_filename)
        file_size = os.path.getsize(model_filename)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"  ✓ Modelo guardado: {model_filename}")
        print(f"  Tamaño: {file_size_mb:.2f} MB")
        
    except Exception as e:
        print(f"  ✗ Error al guardar el modelo: {e}")
        return training_time, None
    
    return training_time, model_filename

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================

# Directorio con emociones organizadas en subdirectorios
# Estructura esperada:
# ./Rostros encontrados/emociones/
#   ├── Alegria/
#   ├── Tristeza/
#   ├── Furia/
#   └── Desagrado/

data_path = './Rostros encontrados/emociones'

# ============================================================================
# VALIDACIÓN DEL DIRECTORIO
# ============================================================================

# Verificar que el directorio existe
if not os.path.exists(data_path):
    print(f"Error: El directorio '{data_path}' no existe")
    print("\nEstructura esperada:")
    print("  ./Rostros encontrados/emociones/")
    print("    ├── Alegria/")
    print("    ├── Tristeza/")
    print("    ├── Furia/")
    print("    └── Desagrado/")
    exit()

# Obtener lista de emociones (subdirectorios)
try:
    emotions_list = [item for item in os.listdir(data_path) 
                     if os.path.isdir(os.path.join(data_path, item))]
    emotions_list.sort()  # Ordenar alfabéticamente
except Exception as e:
    print(f"Error al leer el directorio: {e}")
    exit()

# Verificar que hay emociones para entrenar
if len(emotions_list) == 0:
    print(f"⚠ Error: No se encontraron emociones en '{data_path}'")
    print("\nDebe contener subdirectorios con nombres de emociones")
    exit()

# ============================================================================
# INFORMACIÓN INICIAL
# ============================================================================

print("\n" + "=" * 70)
print("ENTRENAMIENTO DE MODELOS DE RECONOCIMIENTO DE EMOCIONES")
print("=" * 70)
print(f"Directorio de datos: {data_path}")
print(f"Número de emociones encontradas: {len(emotions_list)}")
print(f"Lista de emociones: {emotions_list}")
print("=" * 70)

# ============================================================================
# CARGA DE DATOS DE ENTRENAMIENTO
# ============================================================================

print("\nCargando datos de entrenamiento...")
print("-" * 70)

# Listas para almacenar datos
labels = []
faces_data = []
emotion_to_name = {}

# Variables de control
label = 0
total_images = 0
images_per_emotion = {}
valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

# Procesar cada subdirectorio (emoción)
for emotion_name in emotions_list:
    
    emotion_path = os.path.join(data_path, emotion_name)
    emotion_to_name[label] = emotion_name
    
    print(f"\n  Cargando: {emotion_name} (Etiqueta {label})")
    
    emotion_image_count = 0
    
    try:
        # Obtener lista de archivos de imagen
        file_list = [f for f in os.listdir(emotion_path) 
                     if os.path.splitext(f)[1].lower() in valid_extensions]
        
        if len(file_list) == 0:
            print(f"    ⚠ Advertencia: No se encontraron imágenes en {emotion_path}")
            continue
        
        # Procesar cada archivo de imagen
        for idx, file_name in enumerate(file_list, 1):
            file_path = os.path.join(emotion_path, file_name)
            
            # Leer imagen en escala de grises
            image = cv2.imread(file_path, 0)
            
            if image is None:
                print(f"    ⚠ Error al cargar: {file_name}")
                continue
            
            # Agregar a las listas
            labels.append(label)
            faces_data.append(image)
            
            # Visualización breve
            cv2.imshow('Cargando Datos - Emociones', image)
            cv2.waitKey(1)
            
            emotion_image_count += 1
            total_images += 1
            
            # Mostrar progreso cada 20 imágenes
            if idx % 20 == 0:
                print(f"    Progreso: {idx}/{len(file_list)}")
        
        images_per_emotion[emotion_name] = emotion_image_count
        print(f"    ✓ Cargadas: {emotion_image_count} imágenes")
        
    except Exception as e:
        print(f"    ✗ Error al procesar {emotion_name}: {e}")
        continue
    
    label += 1

cv2.destroyAllWindows()

# Validar que se cargaron datos
if len(faces_data) == 0:
    print("\n✗ Error: No se cargaron imágenes para entrenamiento")
    exit()

print(f"\n✓ Total de imágenes cargadas: {total_images}")
print(f"✓ Distribución por emoción:")
for idx, (emotion, count) in enumerate(images_per_emotion.items()):
    print(f"    Etiqueta {idx} ({emotion}): {count} imágenes")

# ============================================================================
# ENTRENAMIENTO DE MODELOS
# ============================================================================

print("\n" + "=" * 70)
print("ENTRENAMIENTO DE MÚLTIPLES MODELOS")
print("=" * 70)

# Lista de métodos a entrenar
methods = ['EigenFaces', 'FisherFaces', 'LBPH']

# Diccionario para almacenar resultados
results = {}

# Entrenar cada modelo
for method in methods:
    training_time, model_file = train_model(method, faces_data, labels, emotion_to_name)
    
    if training_time is not None and model_file is not None:
        results[method] = {
            'time': training_time,
            'file': model_file,
            'success': True
        }
    else:
        results[method] = {
            'time': 0,
            'file': None,
            'success': False
        }

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 70)
print("RESUMEN DEL ENTRENAMIENTO")
print("=" * 70)
print(f"Total de emociones: {len(emotions_list)}")
print(f"Total de imágenes de entrenamiento: {total_images}")

print("\nDistribución de datos:")
labels_array = np.array(labels)
for idx in range(len(emotions_list)):
    count = np.count_nonzero(labels_array == idx)
    emotion_name = emotion_to_name.get(idx, f"Emocion{idx}")
    print(f"  Etiqueta {idx} ({emotion_name}): {count} imágenes")

print("\nModelos entrenados:")
for method, result in results.items():
    if result['success']:
        print(f"  ✓ {method}: {result['time']:.2f}s - {result['file']}")
    else:
        print(f"  ✗ {method}: Error en el entrenamiento")

print("\n" + "=" * 70)
print("✓ PROCESO COMPLETADO")
print("=" * 70)

print("\nPróximos pasos:")
print("  1. Pruebe los modelos con: 11_test_modelos_emociones.py")
print("  2. Los modelos pueden reconocer las siguientes emociones:")
for idx, name in emotion_to_name.items():
    print(f"     - {name} (etiqueta {idx})")

print(f"\nMapeo de etiquetas: {emotion_to_name}")