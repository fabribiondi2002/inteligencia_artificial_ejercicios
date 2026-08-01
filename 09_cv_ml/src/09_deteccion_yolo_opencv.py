"""
09 - Detección de Objetos con YOLO
===================================

YOLO (You Only Look Once) - Detección de objetos en tiempo real.

CONEXIÓN CON MÓDULO 08 (Reconocimiento Facial):
- Haar Cascade: Detecta SOLO rostros
- YOLO: Detecta MÚLTIPLES tipos de objetos simultáneamente
- Haar: Rápido pero limitado
- YOLO: Más potente, detecta 80 categorías diferentes

¿Qué es YOLO?
- Algoritmo de detección de objetos en tiempo real
- Una sola pasada por la red neuronal (muy rápido)
- Detecta Y localiza objetos (bounding boxes)
- Versiones: YOLOv3, YOLOv4, YOLOv5, YOLOv8

¿Cómo funciona?
1. Divide imagen en grid (ej: 13x13)
2. Cada celda predice bounding boxes + confianza + clase
3. Non-Maximum Suppression para eliminar duplicados
4. Output: Cajas con [x, y, w, h, clase, confianza]

Ventajas vs Haar Cascade:
- Detecta múltiples objetos (personas, autos, animales, etc.)
- Más preciso
- Aprende de millones de imágenes
- Generaliza mejor

Aplicaciones:
- Vigilancia: contar personas, detectar intrusos
- Autos autónomos: detectar peatones, señales, vehículos
- Retail: contar productos en estanterías
- Deportes: tracking de jugadores/pelota
"""

import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("../img", exist_ok=True)

print("=" * 60)
print("DETECCIÓN DE OBJETOS CON YOLO v3")
print("=" * 60)

print(
    """
NOTA IMPORTANTE: YOLO necesita archivos de configuración y pesos.

Para usar YOLO completo, necesitas descargar:

1. yolov3.weights (237 MB) - Pesos del modelo entrenado
   https://pjreddie.com/media/files/yolov3.weights

2. yolov3.cfg - Configuración de la red
   https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg

3. coco.names - Nombres de las 80 clases
   https://github.com/pjreddie/darknet/blob/master/data/coco.names

Colócalos en la carpeta: src/yolo_files/

Para esta demostración, usaremos OpenCV DNN con YOLO si los archivos
están disponibles, o mostraremos cómo usarlo con imágenes sintéticas.
"""
)


# Verificar si existen archivos de YOLO
def verificar_archivos_yolo():
    """Verifica si existen los archivos necesarios de YOLO."""
    archivos = {
        "weights": "yolo_files/yolov3.weights",
        "config": "yolo_files/yolov3.cfg",
        "names": "yolo_files/coco.names",
    }

    todos_existen = all(os.path.exists(f) for f in archivos.values())

    return todos_existen, archivos


yolo_disponible, archivos_yolo = verificar_archivos_yolo()


# Cargar clases COCO (80 categorías que YOLO puede detectar)
COCO_CLASSES = [
    "person",
    "bicycle",
    "car",
    "motorbike",
    "aeroplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "sofa",
    "pottedplant",
    "bed",
    "diningtable",
    "toilet",
    "tvmonitor",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

print(f"\n✓ YOLO puede detectar {len(COCO_CLASSES)} categorías de objetos")
print(f"  Ejemplos: {', '.join(COCO_CLASSES[:10])}, ...")


def cargar_yolo():
    """Carga modelo YOLO usando OpenCV DNN."""
    if not yolo_disponible:
        return None

    # Cargar red neuronal
    net = cv2.dnn.readNet(archivos_yolo["weights"], archivos_yolo["config"])

    # Configurar backend (CPU por defecto, puede usar GPU con CUDA)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Obtener nombres de capas de salida
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    return net, output_layers


def detectar_objetos_yolo(imagen, net, output_layers, confidence_threshold=0.5):
    """
    Detecta objetos en una imagen usando YOLO.

    Args:
        imagen: Imagen BGR de OpenCV
        net: Red YOLO cargada
        output_layers: Capas de salida de YOLO
        confidence_threshold: Umbral de confianza mínimo

    Returns:
        boxes: Lista de bounding boxes [x, y, w, h]
        confidences: Lista de confianzas
        class_ids: Lista de IDs de clase
    """
    height, width = imagen.shape[:2]

    # Preparar imagen para YOLO (blob)
    # YOLO espera entrada de 416x416
    blob = cv2.dnn.blobFromImage(
        imagen, 1 / 255.0, (416, 416), swapRB=True, crop=False
    )

    # Forward pass
    net.setInput(blob)
    outputs = net.forward(output_layers)

    # Procesar detecciones
    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]  # Probabilidades de cada clase
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > confidence_threshold:
                # Coordenadas del bounding box
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Esquina superior izquierda
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-Maximum Suppression para eliminar detecciones duplicadas
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)

    final_boxes = []
    final_confidences = []
    final_class_ids = []

    if len(indices) > 0:
        for i in indices.flatten():
            final_boxes.append(boxes[i])
            final_confidences.append(confidences[i])
            final_class_ids.append(class_ids[i])

    return final_boxes, final_confidences, final_class_ids


def dibujar_detecciones(imagen, boxes, confidences, class_ids):
    """Dibuja bounding boxes en la imagen."""
    colors = np.random.randint(0, 255, size=(len(COCO_CLASSES), 3), dtype=np.uint8)

    imagen_resultado = imagen.copy()

    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        class_id = class_ids[i]
        confidence = confidences[i]

        # Color según clase
        color = colors[class_id].tolist()

        # Dibujar caja
        cv2.rectangle(imagen_resultado, (x, y), (x + w, y + h), color, 2)

        # Etiqueta
        label = f"{COCO_CLASSES[class_id]}: {confidence:.2f}"
        cv2.putText(
            imagen_resultado,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2,
        )

    return imagen_resultado


# Crear imagen de demostración si no hay archivos YOLO
if not yolo_disponible:
    print("\n" + "=" * 60)
    print("MODO DEMOSTRACIÓN (sin archivos YOLO)")
    print("=" * 60)

    # Crear imagen sintética con formas
    imagen_demo = np.ones((480, 640, 3), dtype=np.uint8) * 255

    # Dibujar "objetos" simulados
    # Simular persona
    cv2.rectangle(imagen_demo, (50, 100), (150, 400), (0, 0, 255), -1)
    cv2.circle(imagen_demo, (100, 70), 30, (255, 200, 200), -1)

    # Simular auto
    cv2.rectangle(imagen_demo, (300, 300), (500, 420), (0, 255, 0), -1)
    cv2.circle(imagen_demo, (350, 420), 30, (0, 0, 0), -1)
    cv2.circle(imagen_demo, (450, 420), 30, (0, 0, 0), -1)

    # Simular perro
    cv2.rectangle(imagen_demo, (200, 350), (280, 450), (100, 50, 0), -1)

    # Dibujar "detecciones" simuladas
    detecciones = [
        (50, 50, 100, 350, "person", 0.95),
        (300, 280, 200, 150, "car", 0.89),
        (200, 330, 80, 120, "dog", 0.76),
    ]

    for x, y, w, h, clase, conf in detecciones:
        color = (0, 255, 0)
        cv2.rectangle(imagen_demo, (x, y), (x + w, y + h), color, 2)
        label = f"{clase}: {conf:.2f}"
        cv2.putText(
            imagen_demo,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )

    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(imagen_demo, cv2.COLOR_BGR2RGB))
    plt.title("DEMOSTRACIÓN: Cómo se verían las detecciones de YOLO")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("../img/09_yolo_demo.png", dpi=150, bbox_inches="tight")
    print("\n✓ Demostración guardada en: ../img/09_yolo_demo.png")
    plt.show()

    print(
        """
PARA USAR YOLO REAL:

1. Descarga los archivos necesarios:
   - yolov3.weights (237 MB)
   - yolov3.cfg
   - coco.names

2. Crea carpeta: src/yolo_files/

3. Coloca los archivos ahí

4. Vuelve a ejecutar este script

CÓDIGO EJEMPLO PARA USAR CON WEBCAM:

```python
import cv2

# Cargar YOLO
net, output_layers = cargar_yolo()

# Abrir webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Detectar objetos
    boxes, confs, class_ids = detectar_objetos_yolo(frame, net, output_layers)
    
    # Dibujar detecciones
    resultado = dibujar_detecciones(frame, boxes, confs, class_ids)
    
    cv2.imshow('YOLO', resultado)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
"""
    )

else:
    # MODO COMPLETO: Con archivos YOLO
    print("\n" + "=" * 60)
    print("CARGANDO MODELO YOLO")
    print("=" * 60)

    net, output_layers = cargar_yolo()
    print("\n✓ Modelo YOLO cargado correctamente")

    # Probar con imagen (si existe alguna en ../img o módulos anteriores)
    rutas_imagenes = [
        "../../08_cv_deteccion_reconocimiento_facial/img/personas.jpg",
        "../img/test.jpg",
    ]

    imagen_test = None
    for ruta in rutas_imagenes:
        if os.path.exists(ruta):
            imagen_test = cv2.imread(ruta)
            if imagen_test is not None:
                print(f"\n✓ Imagen cargada: {ruta}")
                break

    if imagen_test is not None:
        print("\n" + "=" * 60)
        print("DETECCIÓN DE OBJETOS")
        print("=" * 60)

        # Detectar objetos
        boxes, confidences, class_ids = detectar_objetos_yolo(
            imagen_test, net, output_layers
        )

        print(f"\n✓ Detectados {len(boxes)} objetos:")
        for i in range(len(boxes)):
            print(
                f"  - {COCO_CLASSES[class_ids[i]]}: {confidences[i]:.2%} de confianza"
            )

        # Dibujar resultados
        resultado = dibujar_detecciones(imagen_test, boxes, confidences, class_ids)

        # Visualizar
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        axes[0].imshow(cv2.cvtColor(imagen_test, cv2.COLOR_BGR2RGB))
        axes[0].set_title("Imagen Original")
        axes[0].axis("off")

        axes[1].imshow(cv2.cvtColor(resultado, cv2.COLOR_BGR2RGB))
        axes[1].set_title(f"YOLO: {len(boxes)} objetos detectados")
        axes[1].axis("off")

        plt.tight_layout()
        plt.savefig("../img/09_yolo_detecciones.png", dpi=150, bbox_inches="tight")
        print("\n✓ Resultados guardados en: ../img/09_yolo_detecciones.png")
        plt.show()

    else:
        print(
            "\n⚠ No se encontró imagen de prueba. Coloca una imagen en ../img/test.jpg"
        )


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print("""
1. YOLO vs HAAR CASCADE (Módulo 08):
   - Haar: Solo rostros, rápido pero limitado
   - YOLO: 80 categorías, más potente y preciso

2. CÓMO FUNCIONA YOLO:
   - Una sola pasada por la red (You Only Look Once)
   - Grid sobre la imagen
   - Cada celda predice bounding boxes + clases
   - NMS elimina detecciones duplicadas

3. VENTAJAS:
   - Tiempo real (30+ FPS)
   - Múltiples objetos simultáneamente
   - Generaliza bien (entrenado en COCO)

4. APLICACIONES:
   - Vigilancia inteligente
   - Autos autónomos
   - Conteo de personas/objetos
   - Análisis de video deportivo
   - Retail analytics

5. VERSIONES:
   - YOLOv3: Buena precisión, usado aquí
   - YOLOv4: Mejoras de velocidad
   - YOLOv5: PyTorch, fácil de usar
   - YOLOv8: Estado del arte actual

6. DESCARGAR ARCHIVOS:
   Weights: https://pjreddie.com/media/files/yolov3.weights
   Config: https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
   Names: https://github.com/pjreddie/darknet/blob/master/data/coco.names

PRÓXIMO PASO: Practicar con ejercicios propuestos (archivo 10)
""")
