import cv2
import numpy as np

# Intentar importar imutils, si no está disponible, usar alternativa
try:
    import imutils
    IMUTILS_AVAILABLE = True
except ImportError:
    IMUTILS_AVAILABLE = False
    print("⚠ Advertencia: imutils no está instalado")
    print("  Instalarlo con: pip install imutils")
    print("  Usando método alternativo de redimensionamiento\n")

# ============================================================================
# FUNCIÓN AUXILIAR PARA REDIMENSIONAMIENTO
# ============================================================================

def resize_image(image, width=None, height=None):
    """
    Redimensiona una imagen manteniendo la proporción de aspecto.
    Alternativa a imutils.resize cuando no está disponible.
    
    Args:
        image: Imagen a redimensionar
        width: Ancho deseado
        height: Alto deseado
    
    Returns:
        Imagen redimensionada
    """
    if IMUTILS_AVAILABLE:
        if width is not None:
            return imutils.resize(image, width=width)
        elif height is not None:
            return imutils.resize(image, height=height)
    
    # Método alternativo si imutils no está disponible
    (h, w) = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# ============================================================================
# CONFIGURACIÓN DE RECURSOS
# ============================================================================

# Fuente de video (cámara web)
# Cambiar el índice si tiene múltiples cámaras:
#   0 = cámara principal
#   1 = cámara secundaria
CAMERA_INDEX = 0

# Imágenes disponibles para superponer (descomentar la que desee usar)
# NOTA: Las imágenes deben tener canal alfa (transparencia) formato PNG
IMAGE_PATH = '../img/dog.png'
#IMAGE_PATH = '../img/gorro_egresado.png'

# Parámetros de superposición
OVERLAY_SCALE_FACTOR = 1.6  # Factor de aumento del ancho (1.6 = 60% más ancho)
VERTICAL_OFFSET = 120        # Desplazamiento vertical del objeto

# ============================================================================
# INFORMACIÓN INICIAL
# ============================================================================

print("\n" + "=" * 70)
print("SUPERPOSICIÓN DE OBJETOS EN ROSTROS DETECTADOS")
print("=" * 70)
print(f"Imagen a superponer: {IMAGE_PATH}")
print(f"Fuente de video: Cámara {CAMERA_INDEX}")
print(f"Factor de escala: {OVERLAY_SCALE_FACTOR}")
print("=" * 70)

# ============================================================================
# CARGA DE LA IMAGEN A SUPERPONER
# ============================================================================

print("\nCargando imagen...")

# Leer la imagen con canal alfa (transparencia)
# IMREAD_UNCHANGED lee el canal alfa
overlay_image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)

# Verificar que la imagen se cargó correctamente
if overlay_image is None:
    print(f"✗ Error: No se pudo cargar la imagen '{IMAGE_PATH}'")
    print("\nVerifique que:")
    print("  1. La ruta del archivo es correcta")
    print("  2. El archivo existe")
    print("  3. El formato es compatible (PNG, JPG, etc.)")
    exit()

# Verificar que la imagen tiene canal alfa (4 canales: BGR + Alpha)
if len(overlay_image.shape) < 3 or overlay_image.shape[2] != 4:
    print(f"✗ Error: La imagen debe tener canal alfa (transparencia)")
    print(f"  Canales encontrados: {overlay_image.shape[2] if len(overlay_image.shape) == 3 else 1}")
    print("\nUse imágenes en formato PNG con transparencia")
    exit()

print(f"✓ Imagen cargada exitosamente")
print(f"  Dimensiones: {overlay_image.shape[1]}x{overlay_image.shape[0]}")
print(f"  Canales: {overlay_image.shape[2]} (incluye canal alfa)")

# ============================================================================
# CONFIGURACIÓN DE LA CÁMARA
# ============================================================================

print("\nIniciando cámara...")

# Inicializar captura de video
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print(f"✗ Error: No se pudo abrir la cámara {CAMERA_INDEX}")
    print("\nPosibles soluciones:")
    print("  1. Verifique que la cámara esté conectada")
    print("  2. Pruebe con otro índice de cámara (0, 1, 2...)")
    print("  3. Cierre otras aplicaciones que usen la cámara")
    exit()

# Configurar propiedades de la cámara
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("✓ Cámara iniciada correctamente")

# ============================================================================
# CONFIGURACIÓN DEL DETECTOR DE ROSTROS
# ============================================================================

# Cargar clasificador Haar Cascade para detección de rostros
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Verificar que el clasificador se cargó correctamente
if faceClassif.empty():
    print("✗ Error: No se pudo cargar el clasificador Haar Cascade")
    cap.release()
    exit()

print("✓ Detector de rostros cargado")

# ============================================================================
# PARÁMETROS DE DETECCIÓN
# ============================================================================

SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5
FRAME_WIDTH = 640

# Variables de estadísticas
frame_count = 0
faces_count = 0

# ============================================================================
# INSTRUCCIONES
# ============================================================================

print("\n" + "=" * 70)
print("INSTRUCCIONES:")
print("  - Presiona 'ESC' para SALIR")
print("  - Presiona '+' para AUMENTAR el tamaño del objeto")
print("  - Presiona '-' para DISMINUIR el tamaño del objeto")
print("=" * 70)
print("\nIniciando detección y superposición...\n")

# ============================================================================
# BUCLE PRINCIPAL DE PROCESAMIENTO
# ============================================================================

overlay_scale = OVERLAY_SCALE_FACTOR

while True:
    # Capturar frame de la cámara
    ret, frame = cap.read()
    
    if not ret:
        print("⚠ No se pudo leer el frame de la cámara")
        break
    
    frame_count += 1
    
    # Redimensionar frame para mejor rendimiento
    frame = resize_image(frame, width=FRAME_WIDTH)
    
    # Convertir a escala de grises para detección
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # ========================================================================
    # DETECCIÓN DE ROSTROS
    # ========================================================================
    
    faces = faceClassif.detectMultiScale(
        gray,
        scaleFactor=SCALE_FACTOR,
        minNeighbors=MIN_NEIGHBORS,
        minSize=(50, 50)
    )
    
    # ========================================================================
    # SUPERPOSICIÓN DE OBJETOS
    # ========================================================================
    
    for (x, y, w, h) in faces:
        faces_count += 1
        
        try:
            # Calcular nuevo ancho basado en el factor de escala
            new_width = int(w * overlay_scale)
            
            # Redimensionar la imagen del objeto
            resized_overlay = resize_image(overlay_image, width=new_width)
            overlay_height = resized_overlay.shape[0]
            overlay_width = resized_overlay.shape[1]
            
            # Calcular desplazamiento horizontal para centrar el objeto
            x_offset = (new_width - w) // 2
            x_start = max(0, x - x_offset)
            x_end = min(frame.shape[1], x_start + overlay_width)
            
            # Calcular posición vertical del objeto
            vertical_portion = (overlay_height // 3) + VERTICAL_OFFSET
            
            # Determinar región del frame donde se superpondrá el objeto
            if y + vertical_portion - overlay_height >= 0:
                y_start = y + vertical_portion - overlay_height
                y_end = y + vertical_portion
                frame_region = frame[y_start:y_end, x_start:x_end]
            else:
                y_start = 0
                y_end = y + vertical_portion
                frame_region = frame[y_start:y_end, x_start:x_end]
            
            # Ajustar dimensiones de la región
            region_height, region_width = frame_region.shape[:2]
            
            # Ajustar imagen del objeto a las dimensiones de la región
            resized_overlay = resized_overlay[-region_height:, :region_width]
            
            # Extraer el canal alfa (máscara de transparencia)
            alpha_channel = resized_overlay[:, :, 3]
            alpha_inv = cv2.bitwise_not(alpha_channel)
            
            # Ajustar máscaras al tamaño de la región
            alpha_channel = alpha_channel[-region_height:, :region_width]
            alpha_inv = alpha_inv[-region_height:, :region_width]
            
            # Extraer la parte RGB del objeto
            overlay_rgb = resized_overlay[:, :, 0:3]
            
            # Aplicar máscaras para combinar imágenes
            # Objeto sobre fondo negro
            overlay_fg = cv2.bitwise_and(overlay_rgb, overlay_rgb, mask=alpha_channel)
            
            # Frame con "agujero" donde va el objeto
            frame_bg = cv2.bitwise_and(frame_region, frame_region, mask=alpha_inv)
            
            # Combinar ambas imágenes
            result = cv2.add(overlay_fg, frame_bg)
            
            # Colocar el resultado en el frame original
            frame[y_start:y_end, x_start:x_end] = result
            
        except Exception as e:
            # Si hay algún error en el procesamiento, continuar con el siguiente rostro
            print(f"⚠ Error al procesar rostro: {e}")
            continue
    
    # ========================================================================
    # INTERFAZ DE USUARIO EN PANTALLA
    # ========================================================================
    
    # Panel de información
    cv2.rectangle(frame, (10, 5), (400, 70), (0, 0, 0), -1)
    cv2.rectangle(frame, (10, 5), (400, 70), (255, 255, 255), 2)
    
    cv2.putText(frame, 'Superposicion de Objetos', (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.putText(frame, f'Rostros: {len(faces)} | Escala: {overlay_scale:.1f}', (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Mostrar frame
    cv2.imshow('Superposicion de Objetos - ESC para salir', frame)
    
    # ========================================================================
    # CONTROL DE TECLADO
    # ========================================================================
    
    key = cv2.waitKey(1) & 0xFF
    
    # Presionar ESC para salir
    if key == 27:
        print("\nCerrando aplicación...")
        break
    
    # Presionar '+' para aumentar escala
    elif key == ord('+') or key == ord('='):
        overlay_scale += 0.1
        print(f"Escala aumentada a: {overlay_scale:.1f}")
    
    # Presionar '-' para disminuir escala
    elif key == ord('-') or key == ord('_'):
        overlay_scale = max(0.5, overlay_scale - 0.1)
        print(f"Escala disminuida a: {overlay_scale:.1f}")

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
print(f"Total de rostros procesados: {faces_count}")
print(f"Escala final del objeto: {overlay_scale:.1f}")
print("=" * 70)
print("\n✓ Aplicación finalizada correctamente")

