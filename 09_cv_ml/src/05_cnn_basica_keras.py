"""
05 - Red Neuronal Convolucional (CNN) Básica
==============================================

APRENDIZAJE SUPERVISADO con CNN para clasificación de imágenes.

CONEXIÓN CON MÓDULO 06 (Filtros y Extracción):
- En el módulo 06 aplicamos filtros manualmente (Sobel, Laplaciano, etc.)
- Las CNN APRENDEN automáticamente los mejores filtros para la tarea
- Cada capa convolucional es un conjunto de filtros aprendidos

¿Qué es una CNN (Convolutional Neural Network)?
- Red neuronal especializada para imágenes
- Usa operaciones de convolución (como en módulo 06)
- Aprende jerarquía de características: bordes → texturas → partes → objetos

Arquitectura típica:
Input → Conv → Pool → Conv → Pool → Flatten → Dense → Output

Ventajas vs Red Densa (archivo 04):
- Menos parámetros (weight sharing)
- Captura patrones espaciales locales
- Invariante a traslaciones
- Mucho mejor precisión en imágenes

Aplicaciones:
- Clasificación de imágenes
- Detección de objetos
- Segmentación semántica
- Reconocimiento facial
"""

import os

import matplotlib.pyplot as plt
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from tensorflow.keras import layers

os.makedirs("../img", exist_ok=True)
os.makedirs("../models", exist_ok=True)

print("=" * 60)
print("CARGANDO DATASET MNIST")
print("=" * 60)

# Cargar MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Preprocesamiento para CNN
# CNNs esperan entrada de forma (altura, ancho, canales)
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

print(f"\n✓ Dataset preprocesado:")
print(f"  - Entrenamiento: {x_train.shape}")
print(f"  - Prueba: {x_test.shape}")
print(f"  - Forma: (batch, height, width, channels)")


# Construir CNN
print("\n" + "=" * 60)
print("CONSTRUCCIÓN DE LA CNN")
print("=" * 60)


def crear_cnn():
    """
    Crea una CNN simple para clasificación.

    Arquitectura:
        Input(28,28,1)
        → Conv2D(32, 3×3) → MaxPool(2×2)
        → Conv2D(64, 3×3) → MaxPool(2×2)
        → Flatten → Dense(128) → Dense(10)
    """
    model = keras.Sequential(
        [
            # Input
            layers.Input(shape=(28, 28, 1), name="input"),
            # Primera capa convolucional: aprende 32 filtros de 3×3
            layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="conv1"),
            layers.MaxPooling2D((2, 2), name="pool1"),  # Reduce 28×28 → 14×14
            # Segunda capa convolucional: aprende 64 filtros de 3×3
            layers.Conv2D(64, (3, 3), activation="relu", padding="same", name="conv2"),
            layers.MaxPooling2D((2, 2), name="pool2"),  # Reduce 14×14 → 7×7
            # Aplanar para capas densas
            layers.Flatten(name="flatten"),
            # Capas densas para clasificación
            layers.Dense(128, activation="relu", name="dense1"),
            layers.Dropout(0.5, name="dropout"),
            layers.Dense(10, activation="softmax", name="output"),
        ],
        name="cnn_mnist",
    )

    return model


model = crear_cnn()

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

print("\n✓ Arquitectura de la CNN:")
model.summary()

print(
    """
EXPLICACIÓN DE COMPONENTES:

1. Conv2D(32, 3×3):
   - Aprende 32 filtros de 3×3 píxeles
   - Cada filtro detecta un patrón (ej: borde vertical, horizontal, diagonal)
   - Similar a aplicar Sobel/Laplaciano pero los filtros se APRENDEN

2. MaxPooling2D(2×2):
   - Reduce dimensionalidad tomando el máximo en ventanas de 2×2
   - Hace el modelo más robusto a traslaciones
   - Reduce costo computacional

3. Flatten:
   - Convierte matriz 2D a vector 1D para capas densas

4. Dense + Softmax:
   - Clasificación final basada en características extraídas
"""
)


# Entrenar
print("\n" + "=" * 60)
print("ENTRENAMIENTO")
print("=" * 60)

print("\nEntrenando CNN (2-3 minutos)...\n")

history = model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,
    verbose=1,
)

print("\n✓ Entrenamiento completado")

# Guardar
modelo_path = "../models/cnn_mnist.keras"
model.save(modelo_path)
print(f"✓ Modelo guardado en: {modelo_path}")


# Evaluar
print("\n" + "=" * 60)
print("EVALUACIÓN")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

print(f"\n✓ Resultados:")
print(f"  - Pérdida: {test_loss:.4f}")
print(f"  - Precisión: {test_accuracy * 100:.2f}%")
print(f"  - Mejora vs Red Densa: ~1-2%")


# Visualizar filtros aprendidos en la primera capa convolucional
print("\n" + "=" * 60)
print("VISUALIZACIÓN DE FILTROS APRENDIDOS")
print("=" * 60)

# Obtener pesos de la primera capa conv
filtros, _ = model.get_layer("conv1").get_weights()
# Shape: (3, 3, 1, 32) → (altura, ancho, canales_entrada, num_filtros)

# Normalizar para visualización
filtros_norm = (filtros - filtros.min()) / (filtros.max() - filtros.min())

# Mostrar los 32 filtros
plt.figure(figsize=(12, 6))
for i in range(32):
    plt.subplot(4, 8, i + 1)
    plt.imshow(filtros_norm[:, :, 0, i], cmap="gray")
    plt.axis("off")

plt.suptitle(
    "Filtros Aprendidos en Conv1 (Similar a Sobel/Laplaciano del Módulo 06)",
    fontsize=12,
)
plt.tight_layout()
plt.savefig("../img/05_filtros_aprendidos.png", dpi=150, bbox_inches="tight")
print("\n✓ Filtros guardados en: ../img/05_filtros_aprendidos.png")
plt.show()

print(
    """
CONEXIÓN CON MÓDULO 06:
- Estos filtros son como los que aplicamos manualmente (Sobel, Laplaciano)
- Pero fueron APRENDIDOS automáticamente por la CNN
- La red encuentra los mejores filtros para detectar dígitos
"""
)


# Visualizar activaciones (qué detecta cada capa)
print("\n" + "=" * 60)
print("VISUALIZACIÓN DE ACTIVACIONES")
print("=" * 60)

# Tomar una imagen de ejemplo
imagen_ejemplo = x_test[0:1]  # Shape: (1, 28, 28, 1)
etiqueta_ejemplo = y_test[0]

# Crear modelo que devuelve activaciones de capas intermedias
layer_outputs = [layer.output for layer in model.layers if "conv" in layer.name]
activation_model = keras.Model(inputs=model.inputs, outputs=layer_outputs)

# Obtener activaciones
activations = activation_model.predict(imagen_ejemplo, verbose=0)

# Visualizar
plt.figure(figsize=(16, 8))

# Imagen original
plt.subplot(2, 5, 1)
plt.imshow(imagen_ejemplo[0, :, :, 0], cmap="gray")
plt.title(f"Input\nDígito: {etiqueta_ejemplo}")
plt.axis("off")

# Activaciones de Conv1 (mostrar 8 de 32 filtros)
for i in range(8):
    plt.subplot(2, 5, i + 2)
    plt.imshow(activations[0][0, :, :, i], cmap="viridis")
    plt.title(f"Conv1\nFiltro {i}")
    plt.axis("off")

# Nueva fila para Conv2
plt.subplot(2, 5, 10)
plt.imshow(activations[1][0, :, :, 0], cmap="viridis")
plt.title("Conv2\nFiltro 0")
plt.axis("off")

plt.suptitle("Activaciones: Qué Detecta Cada Capa Convolucional", fontsize=14)
plt.tight_layout()
plt.savefig("../img/05_activaciones.png", dpi=150, bbox_inches="tight")
print("\n✓ Activaciones guardadas en: ../img/05_activaciones.png")
plt.show()


# Comparar predicciones
y_pred = np.argmax(model.predict(x_test[:20], verbose=0), axis=1)

plt.figure(figsize=(15, 6))
for i in range(20):
    plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[i, :, :, 0], cmap="gray")

    color = "green" if y_pred[i] == y_test[i] else "red"
    plt.title(f"{y_pred[i]}", color=color, fontsize=12)
    plt.axis("off")

plt.suptitle("Predicciones de la CNN (Verde=Correcto, Rojo=Error)", fontsize=14)
plt.tight_layout()
plt.savefig("../img/05_predicciones.png", dpi=150, bbox_inches="tight")
print("✓ Predicciones guardadas en: ../img/05_predicciones.png")
plt.show()


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print(f"""
1. CNN vs RED DENSA:
   - CNN: {test_accuracy * 100:.2f}% de precisión
   - Red Densa (archivo 04): ~97-98%
   - CNN GANA con menos parámetros

2. ARQUITECTURA:
   Input(28×28×1) → Conv2D(32) → MaxPool → Conv2D(64) → MaxPool → Dense → Output(10)
   - Total parámetros: ~100K (vs ~800K de red densa)
   - Weight sharing: mismo filtro en toda la imagen = eficiencia

3. CONEXIÓN CON MÓDULO 06 (Filtros):
   - Conv2D ≈ Aplicar filtros de convolución
   - DIFERENCIA: Aquí los filtros se APRENDEN automáticamente
   - Módulo 06: Sobel, Gaussian (filtros fijos predefinidos)
   - CNN: Encuentra los mejores filtros para la tarea

4. JERARQUÍA DE CARACTERÍSTICAS:
   - Conv1 (capa 1): Detecta bordes, líneas simples
   - Conv2 (capa 2): Combina bordes → formas más complejas
   - Dense: Toma decisión final basada en características

VENTAJAS de CNN:
✓ Menos parámetros (más eficiente)
✓ Captura patrones espaciales (vecindad importa)
✓ Invariante a pequeñas traslaciones
✓ Aprende jerarquía de características automáticamente
✓ Weight sharing = generalización
✓ Pooling = robustez a variaciones

DESVENTAJAS de CNN:
✗ Más lenta de entrenar que red densa simple
✗ Requiere más memoria (activaciones intermedias)
✗ Más compleja de interpretar
✗ Necesita más datos para entrenar bien

5. ¿POR QUÉ FUNCIONA MEJOR QUE RED DENSA?
   - Red Densa: Trata cada píxel independiente → ignora estructura espacial
   - CNN: Explota vecindad de píxeles → entiende que píxeles cercanos forman patrones
   - Ejemplo: En un "7", los píxeles del borde superior están conectados

6. APLICACIONES PRÁCTICAS:
   - Clasificación de imágenes (como MNIST)
   - Reconocimiento facial (Módulo 08 mejorado)
   - Detección de objetos (YOLO usa CNNs)
   - Segmentación de imágenes
   - Diagnóstico médico (rayos X, resonancias)

PRÓXIMO PASO: Aplicar CNN a dataset más complejo CIFAR-10 (archivo 06)
- Imágenes a color (3 canales)
- 10 clases (aviones, autos, pájaros, etc.)
- Más desafiante que MNIST
""")
