import cv2
import os
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================

# Directorio raíz que contiene subdirectorios por cada persona
# Estructura esperada:
# ./Rostros encontrados/
#   ├── Persona1/
#   │   ├── rostro_0.jpg
#   │   ├── rostro_1.jpg
#   │   └── ...
#   ├── Persona2/
#   │   ├── rostro_0.jpg
#   │   └── ...
#   └── ...

data_path = './Rostros encontrados'

# ============================================================================
# VALIDACIÓN DEL DIRECTORIO
# ============================================================================

# Verificar que el directorio existe
if not os.path.exists(data_path):
    print(f"Error: El directorio '{data_path}' no existe")
    print("Por favor, cree el directorio y organize las imágenes por persona")
    print("\nEstructura esperada:")
    print("  ./Rostros encontrados/")
    print("    ├── NombrePersona1/")
    print("    │   ├── rostro_0.jpg")
    print("    │   └── rostro_1.jpg")
    print("    └── NombrePersona2/")
    print("        └── rostro_0.jpg")
    exit()

# Obtener lista de directorios (cada uno representa una persona)
try:
    people_list = [item for item in os.listdir(data_path) 
                   if os.path.isdir(os.path.join(data_path, item))]
except Exception as e:
    print(f"Error al leer el directorio: {e}")
    exit()

# Verificar que hay personas (subdirectorios) para procesar
if len(people_list) == 0:
    print(f"⚠ Advertencia: No se encontraron subdirectorios de personas en '{data_path}'")
    print("\nEl directorio debe contener subdirectorios, uno por cada persona.")
    print("Ejemplo:")
    print("  ./Rostros encontrados/")
    print("    ├── Juan/")
    print("    ├── Maria/")
    print("    └── Pedro/")
    exit()

# ============================================================================
# INFORMACIÓN INICIAL
# ============================================================================

print("\n" + "=" * 70)
print("PREPARACIÓN DE DATOS PARA ENTRENAMIENTO")
print("=" * 70)
print(f"Directorio de datos: {data_path}")
print(f"Número de personas encontradas: {len(people_list)}")
print(f"Lista de personas: {people_list}")
print("=" * 70)

# ============================================================================
# VARIABLES DE ALMACENAMIENTO
# ============================================================================

# Lista para almacenar las etiquetas numéricas (0, 1, 2, ...)
labels = []

# Lista para almacenar las imágenes de rostros en escala de grises
faces_data = []

# Diccionario para mapear etiquetas numéricas a nombres de personas
label_to_name = {}

# Contador de etiqueta actual
label = 0

# Estadísticas
total_images = 0
images_per_person = {}
valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

# ============================================================================
# PROCESAMIENTO DE IMÁGENES POR PERSONA
# ============================================================================

print("\nIniciando lectura de imágenes...")
print("-" * 70)

# Procesar cada subdirectorio (persona)
for person_name in people_list:
    
    # Construir ruta completa del directorio de la persona
    person_path = os.path.join(data_path, person_name)
    
    # Guardar mapeo de etiqueta a nombre
    label_to_name[label] = person_name
    
    print(f"\n[Persona {label}] Procesando: {person_name}")
    print(f"  Directorio: {person_path}")
    
    # Contar imágenes para esta persona
    person_image_count = 0
    
    try:
        # Obtener lista de archivos de imagen
        file_list = [f for f in os.listdir(person_path) 
                     if os.path.splitext(f)[1].lower() in valid_extensions]
        
        if len(file_list) == 0:
            print(f"  ⚠ Advertencia: No se encontraron imágenes válidas en {person_path}")
            continue
        
        print(f"  Total de imágenes encontradas: {len(file_list)}")
        
        # Procesar cada archivo de imagen
        for idx, file_name in enumerate(file_list, 1):
            
            # Construir ruta completa del archivo
            file_path = os.path.join(person_path, file_name)
            
            # Leer la imagen en escala de grises
            image = cv2.imread(file_path, 0)
            
            # Verificar que la imagen se cargó correctamente
            if image is None:
                print(f"  ⚠ Error al cargar: {file_name}")
                continue
            
            # Agregar etiqueta y datos de la imagen
            labels.append(label)
            faces_data.append(image)
            
            # Mostrar la imagen brevemente
            cv2.imshow('Cargando Imagenes de Entrenamiento', image)
            cv2.waitKey(10)  # Mostrar por 10ms
            
            person_image_count += 1
            total_images += 1
            
            # Mostrar progreso cada 10 imágenes
            if idx % 10 == 0:
                print(f"  Procesadas: {idx}/{len(file_list)}")
        
        # Guardar estadísticas de esta persona
        images_per_person[person_name] = person_image_count
        print(f"  ✓ Total cargadas para {person_name}: {person_image_count}")
        
    except Exception as e:
        print(f"  ✗ Error al procesar {person_name}: {e}")
        continue
    
    # Incrementar etiqueta para la siguiente persona
    label += 1

# Cerrar ventanas de visualización
cv2.destroyAllWindows()

# ============================================================================
# VALIDACIÓN DE DATOS CARGADOS
# ============================================================================

if len(faces_data) == 0:
    print("\n✗ Error: No se cargaron imágenes para entrenamiento")
    print("Verifique que los directorios de personas contienen imágenes válidas")
    exit()

# ============================================================================
# ESTADÍSTICAS Y RESUMEN
# ============================================================================

print("\n" + "=" * 70)
print("RESUMEN DE DATOS CARGADOS")
print("=" * 70)

# Información general
print(f"Total de personas: {len(people_list)}")
print(f"Total de imágenes cargadas: {len(faces_data)}")
print(f"Total de etiquetas generadas: {len(labels)}")

# Detalles por persona
print("\nDistribución de imágenes por persona:")
print("-" * 70)
for idx, (person, count) in enumerate(images_per_person.items()):
    print(f"  Etiqueta {idx} ({person}): {count} imágenes")

# Estadísticas de etiquetas
print("\nEstadísticas de etiquetas:")
print("-" * 70)
labels_array = np.array(labels)
for idx in range(len(people_list)):
    count = np.count_nonzero(labels_array == idx)
    person_name = label_to_name.get(idx, f"Persona{idx}")
    print(f"  Etiqueta {idx} ({person_name}): {count} imágenes")

# Información de dimensiones
if len(faces_data) > 0:
    sample_shape = faces_data[0].shape
    print(f"\nDimensiones de las imágenes: {sample_shape[1]}x{sample_shape[0]} píxeles")

print("\n" + "=" * 70)
print("✓ Datos preparados exitosamente para entrenamiento")
print("=" * 70)

# ============================================================================
# INFORMACIÓN ADICIONAL
# ============================================================================

print("\nLos datos están listos para ser utilizados en el entrenamiento de modelos.")
print("Variables disponibles:")
print(f"  - faces_data: Lista con {len(faces_data)} imágenes (numpy arrays)")
print(f"  - labels: Lista con {len(labels)} etiquetas numéricas")
print(f"  - label_to_name: Diccionario de mapeo etiqueta->nombre")
print("\nPara entrenar un modelo, puede usar estos datos con:")
print("  - cv2.face.EigenFaceRecognizer_create()")
print("  - cv2.face.FisherFaceRecognizer_create()")
print("  - cv2.face.LBPHFaceRecognizer_create()")