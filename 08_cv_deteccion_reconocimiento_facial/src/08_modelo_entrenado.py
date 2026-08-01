import cv2
import os
import numpy as np
from datetime import datetime
import time

# ============================================================================
# VERIFICACIÓN DE MÓDULOS REQUERIDOS
# ============================================================================

# Verificar que opencv-contrib-python está instalado
try:
    # Intentar acceder al módulo face de OpenCV
    _ = cv2.face
    print("✓ Módulo cv2.face disponible")
except AttributeError:
    print("\n" + "=" * 70)
    print("ERROR: El módulo cv2.face no está disponible")
    print("=" * 70)
    print("\nPara usar reconocimiento facial, necesita instalar opencv-contrib-python:")
    print("\n  OPCIÓN 1 - Desinstalar opencv-python e instalar opencv-contrib-python:")
    print("    pip uninstall opencv-python")
    print("    pip install opencv-contrib-python")
    print("\n  OPCIÓN 2 - Si ya tiene opencv-python, instale la versión contrib:")
    print("    pip install opencv-contrib-python")
    print("\nNOTA: Asegúrese de que las versiones coincidan.")
    print("=" * 70)
    exit()

# ============================================================================
# CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# ============================================================================

# Directorio con los datos de entrenamiento organizados por persona
data_path = './Rostros encontrados'

# Modelo a entrenar (descomentar el que desee usar)
# Opciones: 'LBPH', 'EigenFace', 'FisherFace'
MODEL_TYPE = 'LBPH'  # Recomendado: mejor rendimiento en general
#MODEL_TYPE = 'EigenFace'  # Requiere todas las imágenes del mismo tamaño
#MODEL_TYPE = 'FisherFace'  # Requiere todas las imágenes del mismo tamaño

# Nombres de archivos de salida para cada modelo
MODEL_FILES = {
    'LBPH': 'modeloLBPHFace.xml',
    'EigenFace': 'modeloEigenFace.xml',
    'FisherFace': 'modeloFisherFace.xml'
}

# ============================================================================
# VALIDACIÓN DEL DIRECTORIO
# ============================================================================

# Verificar que el directorio existe
if not os.path.exists(data_path):
    print(f"Error: El directorio '{data_path}' no existe")
    print("\nPor favor, ejecute primero los scripts de captura de rostros:")
    print("  - 04_capturas_entrenamiento.py")
    print("  - 05_entrenamiento_directorio.py")
    print("  - 06_entrenamiento_cam.py")
    exit()

# Obtener lista de directorios (cada uno representa una persona)
try:
    people_list = [item for item in os.listdir(data_path) 
                   if os.path.isdir(os.path.join(data_path, item))]
except Exception as e:
    print(f"Error al leer el directorio: {e}")
    exit()

# Verificar que hay personas para entrenar
if len(people_list) == 0:
    print(f"⚠ Error: No se encontraron subdirectorios de personas en '{data_path}'")
    print("\nEl directorio debe contener subdirectorios, uno por cada persona:")
    print("  ./Rostros encontrados/")
    print("    ├── Persona1/")
    print("    ├── Persona2/")
    print("    └── Persona3/")
    exit()

# ============================================================================
# INFORMACIÓN INICIAL
# ============================================================================

print("\n" + "=" * 70)
print("ENTRENAMIENTO DE MODELO DE RECONOCIMIENTO FACIAL")
print("=" * 70)
print(f"Directorio de datos: {data_path}")
print(f"Modelo seleccionado: {MODEL_TYPE}")
print(f"Archivo de salida: {MODEL_FILES[MODEL_TYPE]}")
print(f"Número de personas encontradas: {len(people_list)}")
print(f"Lista de personas: {people_list}")
print("=" * 70)

# ============================================================================
# CARGA DE DATOS DE ENTRENAMIENTO
# ============================================================================

print("\n[1/3] CARGANDO DATOS DE ENTRENAMIENTO")
print("-" * 70)

# Listas para almacenar datos
labels = []
faces_data = []
label_to_name = {}

# Variables de control
label = 0
total_images = 0
images_per_person = {}
valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

# Procesar cada subdirectorio (persona)
for person_name in people_list:
    
    person_path = os.path.join(data_path, person_name)
    label_to_name[label] = person_name
    
    print(f"\n  Cargando: {person_name} (Etiqueta {label})")
    
    person_image_count = 0
    
    try:
        # Obtener lista de archivos de imagen
        file_list = [f for f in os.listdir(person_path) 
                     if os.path.splitext(f)[1].lower() in valid_extensions]
        
        if len(file_list) == 0:
            print(f"    ⚠ Advertencia: No se encontraron imágenes en {person_path}")
            continue
        
        # Procesar cada archivo de imagen
        for idx, file_name in enumerate(file_list, 1):
            file_path = os.path.join(person_path, file_name)
            
            # Leer imagen en escala de grises
            image = cv2.imread(file_path, 0)
            
            if image is None:
                print(f"    ⚠ Error al cargar: {file_name}")
                continue
            
            # Agregar a las listas
            labels.append(label)
            faces_data.append(image)
            
            # Visualización breve
            cv2.imshow('Cargando Datos de Entrenamiento', image)
            cv2.waitKey(1)
            
            person_image_count += 1
            total_images += 1
            
            # Mostrar progreso cada 20 imágenes
            if idx % 20 == 0:
                print(f"    Progreso: {idx}/{len(file_list)}")
        
        images_per_person[person_name] = person_image_count
        print(f"    ✓ Cargadas: {person_image_count} imágenes")
        
    except Exception as e:
        print(f"    ✗ Error al procesar {person_name}: {e}")
        continue
    
    label += 1

cv2.destroyAllWindows()

# Validar que se cargaron datos
if len(faces_data) == 0:
    print("\n✗ Error: No se cargaron imágenes para entrenamiento")
    exit()

# Convertir labels a numpy array
labels_array = np.array(labels)

print(f"\n✓ Total de imágenes cargadas: {total_images}")
print(f"✓ Distribución por persona:")
for idx, (person, count) in enumerate(images_per_person.items()):
    print(f"    Etiqueta {idx} ({person}): {count} imágenes")

# ============================================================================
# CREACIÓN DEL MODELO
# ============================================================================

print("\n[2/3] CREANDO MODELO DE RECONOCIMIENTO")
print("-" * 70)

# Crear el reconocedor según el tipo seleccionado
if MODEL_TYPE == 'LBPH':
    print("  Modelo: Local Binary Patterns Histograms (LBPH)")
    print("  Características:")
    print("    - Funciona con imágenes de diferentes tamaños")
    print("    - Robusto a cambios de iluminación")
    print("    - Recomendado para uso general")
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

elif MODEL_TYPE == 'EigenFace':
    print("  Modelo: EigenFaces (PCA)")
    print("  Características:")
    print("    - Requiere imágenes del mismo tamaño")
    print("    - Rápido en entrenamiento")
    print("    - Sensible a iluminación")
    face_recognizer = cv2.face.EigenFaceRecognizer_create()

elif MODEL_TYPE == 'FisherFace':
    print("  Modelo: FisherFaces (LDA)")
    print("  Características:")
    print("    - Requiere imágenes del mismo tamaño")
    print("    - Mejor que EigenFace en condiciones variables")
    print("    - Necesita al menos 2 clases")
    face_recognizer = cv2.face.FisherFaceRecognizer_create()

else:
    print(f"✗ Error: Tipo de modelo '{MODEL_TYPE}' no válido")
    exit()

# ============================================================================
# ENTRENAMIENTO DEL MODELO
# ============================================================================

print("\n[3/3] ENTRENANDO MODELO")
print("-" * 70)
print(f"  Iniciando entrenamiento con {len(faces_data)} imágenes...")

# Medir tiempo de entrenamiento
start_time = time.time()

try:
    # Entrenar el modelo
    face_recognizer.train(faces_data, labels_array)
    
    training_time = time.time() - start_time
    
    print(f"  ✓ Entrenamiento completado en {training_time:.2f} segundos")
    
except Exception as e:
    print(f"  ✗ Error durante el entrenamiento: {e}")
    print("\nPosibles soluciones:")
    print("  - Para EigenFace/FisherFace: Asegúrese de que todas las imágenes tienen el mismo tamaño")
    print("  - Para FisherFace: Necesita al menos 2 personas diferentes")
    print("  - Use el modelo LBPH si tiene imágenes de diferentes tamaños")
    exit()

# ============================================================================
# GUARDADO DEL MODELO
# ============================================================================

print("\nGUARDANDO MODELO")
print("-" * 70)

output_file = MODEL_FILES[MODEL_TYPE]

try:
    # Guardar el modelo entrenado
    face_recognizer.write(output_file)
    
    # Obtener información del archivo
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"  ✓ Modelo guardado exitosamente")
    print(f"  Archivo: {output_file}")
    print(f"  Tamaño: {file_size_mb:.2f} MB")
    
except Exception as e:
    print(f"  ✗ Error al guardar el modelo: {e}")
    exit()

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 70)
print("RESUMEN DEL ENTRENAMIENTO")
print("=" * 70)
print(f"Modelo entrenado: {MODEL_TYPE}")
print(f"Total de personas: {len(people_list)}")
print(f"Total de imágenes de entrenamiento: {total_images}")
print(f"Tiempo de entrenamiento: {training_time:.2f} segundos")
print(f"Archivo del modelo: {output_file}")
print(f"Tamaño del archivo: {file_size_mb:.2f} MB")

print("\nDistribución de datos:")
for idx in range(len(people_list)):
    count = np.count_nonzero(labels_array == idx)
    person_name = label_to_name.get(idx, f"Persona{idx}")
    print(f"  Etiqueta {idx} ({person_name}): {count} imágenes")

print("\n" + "=" * 70)
print("✓ MODELO ENTRENADO Y GUARDADO EXITOSAMENTE")
print("=" * 70)

print("\nPróximos pasos:")
print("  1. Use el modelo entrenado en el script de reconocimiento")
print("  2. Pruebe el modelo con: 09_test_modelos.py")
print("  3. El modelo puede reconocer las siguientes personas:")
for idx, name in label_to_name.items():
    print(f"     - {name} (etiqueta {idx})")

print("\nNOTA: Guarde el mapeo de etiquetas para poder identificar personas:")
print(f"  {label_to_name}")