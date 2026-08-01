"""
07 - Transfer Learning con Modelos Pre-entrenados
==================================================

APRENDIZAJE SUPERVISADO: Reutilizar conocimiento de modelos entrenados en ImageNet.

¿Qué es Transfer Learning?
- Usar un modelo pre-entrenado en un dataset grande (ImageNet)
- Ajustarlo (fine-tuning) para nuestra tarea específica
- Aprovecha características aprendidas (bordes, texturas, formas)

Ventajas:
- Menos datos necesarios (no necesitamos millones de imágenes)
- Entrenamiento más rápido (solo ajustamos últimas capas)
- Mejor rendimiento (modelo ya sabe reconocer objetos generales)

Modelos populares pre-entrenados:
- VGG16, VGG19: Simples, muchos parámetros
- ResNet50, ResNet101: Muy profundos con "skip connections"
- MobileNet: Ligero para móviles
- EfficientNet: Estado del arte, eficiente

ImageNet:
- 14 millones de imágenes
- 1000 categorías (perros, gatos, vehículos, etc.)
- Competencia anual (ILSVRC)
"""

import os

import matplotlib.pyplot as plt
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2

os.makedirs("../img", exist_ok=True)
os.makedirs("../models", exist_ok=True)

print("=" * 60)
print("TRANSFER LEARNING CON MOBILENETV2")
print("=" * 60)

# Usaremos CIFAR-10 como dataset pequeño para demostrar Transfer Learning
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Normalizar
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
y_train = y_train.flatten()
y_test = y_test.flatten()

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

print(f"\n✓ Dataset CIFAR-10 cargado: {x_train.shape}")


# Cargar modelo pre-entrenado
print("\n" + "=" * 60)
print("CARGANDO MODELO PRE-ENTRENADO")
print("=" * 60)

# Cargar MobileNetV2 sin la capa de clasificación (include_top=False)
# Usamos pesos de ImageNet
base_model = MobileNetV2(
    input_shape=(32, 32, 3),
    include_top=False,  # Sin capa de clasificación
    weights="imagenet",  # Pesos pre-entrenados en ImageNet
    pooling="avg",  # Global average pooling al final
)

# Congelar capas del modelo base (no entrenar)
base_model.trainable = False

print(f"\n✓ MobileNetV2 cargado")
print(f"  - Parámetros: {base_model.count_params():,}")
print(f"  - Entrenado en: ImageNet (1.4M imágenes, 1000 clases)")
print(f"  - Capas congeladas: {len(base_model.layers)}")

print(
    """
ESTRATEGIA:
1. Usar MobileNetV2 como "extractor de características"
2. Sus capas están CONGELADAS (no se entrenan)
3. Solo entrenamos nuevas capas Dense al final
4. Esto es MUCHO más rápido y requiere menos datos
"""
)


# Construir modelo con Transfer Learning
print("\n" + "=" * 60)
print("CONSTRUCCIÓN DEL MODELO")
print("=" * 60)


def crear_modelo_transfer_learning(base_model, num_classes=10):
    """
    Crea modelo usando Transfer Learning.

    Args:
        base_model: Modelo pre-entrenado (MobileNetV2)
        num_classes: Número de clases a clasificar

    Returns:
        model: Modelo completo
    """
    inputs = keras.Input(shape=(32, 32, 3))

    # Data augmentation
    x = layers.RandomFlip("horizontal")(inputs)
    x = layers.RandomRotation(0.1)(x)

    # Modelo base (congelado)
    x = base_model(x, training=False)  # training=False para usar en modo inferencia

    # Nuevas capas de clasificación (estas SÍ se entrenan)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs, name="transfer_learning_model")

    return model


model = crear_modelo_transfer_learning(base_model)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

print("\n✓ Arquitectura completa:")
model.summary()


# Entrenar (solo las nuevas capas)
print("\n" + "=" * 60)
print("ENTRENAMIENTO (FASE 1: Solo capas nuevas)")
print("=" * 60)

print(
    """
FASE 1: Entrenar solo capas Dense nuevas
- Base model CONGELADO
- Rápido (2-3 minutos)
"""
)

history_1 = model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1,
    verbose=1,
)

print("\n✓ Fase 1 completada")


# Fine-tuning: Descongelar algunas capas del modelo base
print("\n" + "=" * 60)
print("FINE-TUNING (FASE 2: Ajustar últimas capas)")
print("=" * 60)

print(
    """
FASE 2: Fine-tuning
- Descongelar últimas capas del base model
- Entrenar con learning rate BAJO
- Ajusta características a nuestro dataset específico
"""
)

# Descongelar últimas 20 capas
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

print(
    f"\n✓ Descongeladas últimas 20 capas de MobileNetV2"
)

# Recompilar con learning rate MÁS BAJO
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),  # 10x más bajo
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

history_2 = model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1,
    verbose=1,
)

print("\n✓ Fine-tuning completado")

# Guardar
modelo_path = "../models/transfer_learning_cifar10.keras"
model.save(modelo_path)
print(f"✓ Modelo guardado en: {modelo_path}")


# Evaluar
print("\n" + "=" * 60)
print("EVALUACIÓN")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

print(f"\n✓ Resultados finales:")
print(f"  - Pérdida: {test_loss:.4f}")
print(f"  - Precisión: {test_accuracy * 100:.2f}%")
print(f"  - Comparación: CNN desde cero (~70%), Transfer Learning (~75-85%)")


# Visualizar curvas de aprendizaje
plt.figure(figsize=(12, 5))

# Combinar historias de fase 1 y 2
acc = history_1.history["accuracy"] + history_2.history["accuracy"]
val_acc = history_1.history["val_accuracy"] + history_2.history["val_accuracy"]
loss = history_1.history["loss"] + history_2.history["loss"]
val_loss = history_1.history["val_loss"] + history_2.history["val_loss"]

epochs_range = range(len(acc))

plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label="Train")
plt.plot(epochs_range, val_acc, label="Val")
plt.axvline(x=5, color="red", linestyle="--", label="Fine-tuning start")
plt.title("Precisión")
plt.xlabel("Época")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label="Train")
plt.plot(epochs_range, val_loss, label="Val")
plt.axvline(x=5, color="red", linestyle="--", label="Fine-tuning start")
plt.title("Pérdida")
plt.xlabel("Época")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.suptitle("Transfer Learning: Fase 1 + Fine-tuning", fontsize=14)
plt.tight_layout()
plt.savefig("../img/07_transfer_learning_curves.png", dpi=150, bbox_inches="tight")
print("\n✓ Curvas guardadas en: ../img/07_transfer_learning_curves.png")
plt.show()


# Predicciones
y_pred = np.argmax(model.predict(x_test[:20], verbose=0), axis=1)

plt.figure(figsize=(15, 6))
for i in range(20):
    plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[i])

    color = "green" if y_pred[i] == y_test[i] else "red"
    plt.title(f"{class_names[y_pred[i]]}", color=color, fontsize=8)
    plt.axis("off")

plt.suptitle("Predicciones con Transfer Learning", fontsize=14)
plt.tight_layout()
plt.savefig("../img/07_predicciones.png", dpi=150, bbox_inches="tight")
print("✓ Predicciones guardadas en: ../img/07_predicciones.png")
plt.show()


# Comparar Transfer Learning vs entrenar desde cero
print("\n" + "=" * 60)
print("COMPARACIÓN: TRANSFER LEARNING VS DESDE CERO")
print("=" * 60)

comparison_data = {
    "Aspecto": [
        "Precisión",
        "Tiempo de entrenamiento",
        "Datos necesarios",
        "Parámetros a entrenar",
        "Convergencia",
    ],
    "Desde Cero": [
        "~70%",
        "10-15 min (30 epochs)",
        "Miles de imágenes",
        "Todos (~500K)",
        "Lenta",
    ],
    "Transfer Learning": [
        "~75-85%",
        "5-7 min (10 epochs)",
        "Cientos de imágenes",
        "Pocas capas (~50K)",
        "Rápida",
    ],
}

print("\n{:<30} {:<25} {:<25}".format("Aspecto", "Desde Cero", "Transfer Learning"))
print("-" * 80)
for i in range(len(comparison_data["Aspecto"])):
    print(
        "{:<30} {:<25} {:<25}".format(
            comparison_data["Aspecto"][i],
            comparison_data["Desde Cero"][i],
            comparison_data["Transfer Learning"][i],
        )
    )


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print(f"""
1. TRANSFER LEARNING ES PODEROSO:
   - Precisión: {test_accuracy * 100:.1f}% vs ~70% desde cero (CNN básica)
   - Menos tiempo de entrenamiento: ~5-7 min vs ~15 min
   - Requiere menos datos: Cientos vs miles de imágenes

2. ESTRATEGIA EN 2 FASES:
   FASE 1: Entrenar solo capas nuevas
   - Base model congelado (pesos de ImageNet)
   - Solo entrenar Dense layers nuevas
   - 5 epochs con LR normal (0.001)
   
   FASE 2: Fine-tuning (ajuste fino)
   - Descongelar últimas 20 capas del base model
   - Entrenar con LR muy bajo (0.0001)
   - 5 epochs adicionales
   - CUIDADO: LR alto destruiría pesos pre-entrenados

3. ¿POR QUÉ FUNCIONA?
   - ImageNet tiene 1.4 millones de imágenes, 1000 clases
   - Capas iniciales aprenden características genéricas:
     * Bordes, colores, texturas
     * Formas básicas
   - Estas características son útiles para CUALQUIER tarea de visión
   - Solo adaptamos las últimas capas a nuestra tarea específica

VENTAJAS de Transfer Learning:
✓ Requiere menos datos (cientos vs miles)
✓ Entrena más rápido (minutos vs horas)
✓ Mejor precisión con dataset pequeño
✓ Aprovecha conocimiento de ImageNet
✓ Menos propenso a overfitting
✓ Funciona bien aunque tu tarea sea diferente a ImageNet

DESVENTAJAS de Transfer Learning:
✗ Requiere modelo pre-entrenado (descarga ~14-90 MB)
✗ No funciona bien si tu dominio es muy diferente (ej: imágenes médicas microscópicas)
✗ Menos flexible que entrenar desde cero
✗ Puede heredar sesgos del dataset original (ImageNet)
✗ Arquitectura fija (no puedes modificar base model fácilmente)
✗ Fine-tuning delicado (LR incorrecto arruina todo)

4. ¿CUÁNDO USAR TRANSFER LEARNING?
   ✓ Dataset pequeño (< 10K imágenes) → SIEMPRE Transfer Learning
   ✓ Objetos similares a ImageNet (animales, vehículos, objetos cotidianos)
   ✓ Recursos limitados (tiempo, GPU)
   ✓ Prototipado rápido
   
   ✗ Dataset muy grande (> 100K imágenes) → Puedes entrenar desde cero
   ✗ Dominio muy específico (ej: rayos X, satélite) → Considerar desde cero

5. MODELOS PRE-ENTRENADOS POPULARES:
   - MobileNetV2: Ligero (14 MB), rápido, ideal para móviles/edge
   - ResNet50: Preciso (98 MB), más pesado, buena opción general
   - EfficientNet: Estado del arte, balance precisión/eficiencia
   - VGG16: Clásico, simple, bueno para aprender
   - InceptionV3: Muy potente, multi-escala

6. COMPARACIÓN CIFAR-10:
   - Archivo 06 (CNN desde cero): ~70-75% precisión, 15 min
   - Archivo 07 (Transfer Learning): ~{test_accuracy * 100:.1f}% precisión, 7 min
   - Ganancia: +{(test_accuracy - 0.72) * 100:.1f}% con la mitad del tiempo

7. APLICACIONES PRÁCTICAS:
   - Clasificar tus propias imágenes con pocos ejemplos
   - Apps móviles de reconocimiento (plantas, alimentos, etc.)
   - Prototipado rápido de sistemas de visión
   - Base para detección de objetos (YOLO, Faster R-CNN)
   - Sistemas de vigilancia personalizados

PRÓXIMO PASO: Ver Aprendizaje por Refuerzo con visión (archivo 08)
- Agente que aprende a navegar usando imágenes como entrada
- Combina RL + Deep Learning
""")
