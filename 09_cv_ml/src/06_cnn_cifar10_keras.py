"""
06 - CNN para CIFAR-10 (Imágenes a Color)
==========================================

APRENDIZAJE SUPERVISADO con CNN en dataset más desafiante.

CIFAR-10 Dataset:
- 60,000 imágenes a color (32×32×3 RGB)
- 10 clases: avión, auto, pájaro, gato, ciervo, perro, rana, caballo, barco, camión
- Más difícil que MNIST: objetos complejos, variaciones de pose/iluminación
- Estado del arte: ~95% de precisión

Diferencias vs MNIST:
- Imágenes a color (3 canales RGB vs 1 escala de grises)
- Mayor variabilidad dentro de cada clase
- Resolución baja (32×32) dificulta reconocimiento

Técnicas para mejorar:
- Data Augmentation (rotaciones, flips, zoom)
- Batch Normalization
- CNN más profunda
- Dropout para regularización
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
print("CARGANDO DATASET CIFAR-10")
print("=" * 60)

# Cargar CIFAR-10
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Nombres de las clases
class_names = [
    "Avión",
    "Auto",
    "Pájaro",
    "Gato",
    "Ciervo",
    "Perro",
    "Rana",
    "Caballo",
    "Barco",
    "Camión",
]

print(f"\n✓ Dataset cargado:")
print(f"  - Entrenamiento: {x_train.shape}")
print(f"  - Prueba: {x_test.shape}")
print(f"  - Forma: (batch, 32, 32, 3) - imágenes RGB")
print(f"  - Clases: {len(class_names)}")

# Visualizar ejemplos
plt.figure(figsize=(15, 6))
for i in range(20):
    plt.subplot(4, 5, i + 1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i][0]], fontsize=9)
    plt.axis("off")

plt.suptitle("Ejemplos del Dataset CIFAR-10", fontsize=14)
plt.tight_layout()
plt.savefig("../img/06_cifar10_ejemplos.png", dpi=150, bbox_inches="tight")
print("\n✓ Ejemplos guardados en: ../img/06_cifar10_ejemplos.png")
plt.show()


# Preprocesamiento
print("\n" + "=" * 60)
print("PREPROCESAMIENTO")
print("=" * 60)

# Normalizar a [0, 1]
x_train_norm = x_train.astype("float32") / 255.0
x_test_norm = x_test.astype("float32") / 255.0

# Aplanar etiquetas
y_train = y_train.flatten()
y_test = y_test.flatten()

print(f"\n✓ Datos normalizados a rango [0, 1]")


# Construir CNN más profunda
print("\n" + "=" * 60)
print("CONSTRUCCIÓN DE CNN PARA CIFAR-10")
print("=" * 60)


def crear_cnn_cifar10():
    """
    CNN más profunda para CIFAR-10.

    Arquitectura:
        Input(32,32,3)
        → Conv(32) → Conv(32) → MaxPool
        → Conv(64) → Conv(64) → MaxPool
        → Conv(128) → MaxPool
        → Flatten → Dense(256) → Dense(10)
    """
    model = keras.Sequential(
        [
            layers.Input(shape=(32, 32, 3)),
            # Bloque 1: 32 filtros
            layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            # Bloque 2: 64 filtros
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.3),
            # Bloque 3: 128 filtros
            layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.4),
            # Clasificador
            layers.Flatten(),
            layers.Dense(256, activation="relu"),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(10, activation="softmax"),
        ],
        name="cnn_cifar10",
    )

    return model


model = crear_cnn_cifar10()

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

print("\n✓ Arquitectura:")
model.summary()

print(
    """
TÉCNICAS USADAS:

1. BatchNormalization:
   - Normaliza activaciones entre capas
   - Acelera entrenamiento y estabiliza
   - Reduce dependencia de inicialización

2. Dropout:
   - Desactiva neuronas aleatoriamente
   - Previene overfitting
   - Dropout mayor en capas más profundas

3. Bloques convolucionales:
   - Conv → Conv → Pool (patrón común)
   - Filtros aumentan: 32 → 64 → 128
   - Captura jerarquía de características
"""
)


# Data Augmentation (aumentar variedad de datos)
print("\n" + "=" * 60)
print("DATA AUGMENTATION")
print("=" * 60)

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),  # Voltear horizontalmente
        layers.RandomRotation(0.1),  # Rotar hasta 10%
        layers.RandomZoom(0.1),  # Zoom hasta 10%
    ],
    name="augmentation",
)

print(
    """
✓ Data Augmentation configurado:
  - RandomFlip: Voltea imágenes horizontalmente
  - RandomRotation: Rota ligeramente
  - RandomZoom: Acerca/aleja

Esto AUMENTA artificialmente el dataset y mejora generalización.
"""
)

# Visualizar efecto de augmentation
img_ejemplo = x_train_norm[0:1]

plt.figure(figsize=(15, 3))
plt.subplot(1, 6, 1)
plt.imshow(img_ejemplo[0])
plt.title("Original")
plt.axis("off")

for i in range(5):
    augmented = data_augmentation(img_ejemplo, training=True)
    plt.subplot(1, 6, i + 2)
    plt.imshow(augmented[0])
    plt.title(f"Aug {i+1}")
    plt.axis("off")

plt.suptitle("Efecto de Data Augmentation", fontsize=14)
plt.tight_layout()
plt.savefig("../img/06_augmentation.png", dpi=150, bbox_inches="tight")
print("✓ Visualización guardada en: ../img/06_augmentation.png")
plt.show()


# Entrenar (esto toma más tiempo)
print("\n" + "=" * 60)
print("ENTRENAMIENTO")
print("=" * 60)

print("\nEntrenando CNN en CIFAR-10 (5-10 minutos)...")
print("Para clase de 2h, recomendado entrenar solo 5 epochs\n")

# Callbacks
callbacks = [
    keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
]

history = model.fit(
    data_augmentation(x_train_norm, training=True),
    y_train,
    epochs=5,  # Reducido para clase, ideal sería 20-30
    batch_size=64,
    validation_split=0.1,
    callbacks=callbacks,
    verbose=1,
)

print("\n✓ Entrenamiento completado")

# Guardar
modelo_path = "../models/cnn_cifar10.keras"
model.save(modelo_path)
print(f"✓ Modelo guardado en: {modelo_path}")


# Evaluar
print("\n" + "=" * 60)
print("EVALUACIÓN")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(x_test_norm, y_test, verbose=0)

print(f"\n✓ Resultados en test:")
print(f"  - Pérdida: {test_loss:.4f}")
print(f"  - Precisión: {test_accuracy * 100:.2f}%")
print(
    f"  - Nota: Con más epochs (20-30) se puede alcanzar ~75-80%, estado del arte ~95%"
)


# Curvas de aprendizaje
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Entrenamiento")
plt.plot(history.history["val_accuracy"], label="Validación")
plt.title("Precisión")
plt.xlabel("Época")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Entrenamiento")
plt.plot(history.history["val_loss"], label="Validación")
plt.title("Pérdida")
plt.xlabel("Época")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.suptitle("Curvas de Aprendizaje - CIFAR-10", fontsize=14)
plt.tight_layout()
plt.savefig("../img/06_training_curves.png", dpi=150, bbox_inches="tight")
print("\n✓ Curvas guardadas en: ../img/06_training_curves.png")
plt.show()


# Predicciones
y_pred = np.argmax(model.predict(x_test_norm[:20], verbose=0), axis=1)

plt.figure(figsize=(15, 6))
for i in range(20):
    plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[i])

    real = class_names[y_test[i]]
    pred = class_names[y_pred[i]]
    color = "green" if y_pred[i] == y_test[i] else "red"

    plt.title(f"{pred}", color=color, fontsize=8)
    plt.axis("off")

plt.suptitle(
    "Predicciones en CIFAR-10 (Verde=Correcto, Rojo=Error)", fontsize=14
)
plt.tight_layout()
plt.savefig("../img/06_predicciones.png", dpi=150, bbox_inches="tight")
print("✓ Predicciones guardadas en: ../img/06_predicciones.png")
plt.show()


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print(f"""
1. CIFAR-10 ES MÁS DIFÍCIL QUE MNIST:
   - Objetos complejos vs dígitos simples
   - Variabilidad en pose, iluminación, fondo
   - Imágenes a color (3 canales)

2. PRECISIÓN ALCANZADA: {test_accuracy * 100:.1f}%
   - Con 5 epochs: ~60-70%
   - Con 30 epochs: ~75-80%
   - Estado del arte: ~95% (ResNet, EfficientNet)

3. TÉCNICAS IMPORTANTES:
   - BatchNormalization: Estabiliza entrenamiento
   - Data Augmentation: Aumenta variedad de datos
   - Dropout progresivo: 0.2 → 0.3 → 0.4 → 0.5
   - CNN profunda: Múltiples bloques Conv-Conv-Pool

4. COMPARACIÓN:
   - MNIST: Red simple → 98-99%
   - CIFAR-10: Red profunda → 75-80%

5. PRÓXIMOS PASOS PARA MEJORAR:
   - Entrenar más epochs (20-30)
   - Arquitecturas modernas (ResNet, MobileNet)
   - Transfer Learning (usar modelo pre-entrenado)

PRÓXIMO PASO: Transfer Learning con modelos pre-entrenados (archivo 07)
""")
