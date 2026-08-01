"""
04 - Clasificación de Dígitos MNIST con Red Neuronal
======================================================

APRENDIZAJE SUPERVISADO: Usamos imágenes etiquetadas para entrenar el modelo.

¿Qué es Aprendizaje Supervisado?
- Tenemos datos de entrada (imágenes) y salida conocida (etiquetas)
- El modelo aprende el mapeo: imagen → etiqueta
- Ejemplo: Imagen de "5" → Clase 5

MNIST Dataset:
- 70,000 imágenes de dígitos escritos a mano (0-9)
- 60,000 para entrenamiento, 10,000 para prueba
- Resolución: 28x28 píxeles en escala de grises
- Dataset estándar para empezar con Deep Learning

Arquitectura de Red Neuronal:
Input (784 píxeles) → Dense(128) → Dense(64) → Output(10 clases)

Aplicaciones:
- OCR (Optical Character Recognition)
- Lectura automática de códigos postales
- Digitalización de formularios
- Reconocimiento de dígitos en cheques bancarios
"""

import os

import matplotlib.pyplot as plt
import numpy as np

# Configurar TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from tensorflow.keras import layers

# Crear carpetas
os.makedirs("../img", exist_ok=True)
os.makedirs("../models", exist_ok=True)

print("=" * 60)
print("CARGANDO DATASET MNIST")
print("=" * 60)

# Cargar dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print(f"\n✓ Dataset cargado:")
print(f"  - Entrenamiento: {x_train.shape[0]} imágenes")
print(f"  - Prueba: {x_test.shape[0]} imágenes")
print(f"  - Resolución: {x_train.shape[1]}x{x_train.shape[2]} píxeles")
print(f"  - Clases: 10 dígitos (0-9)")

# Visualizar ejemplos del dataset
plt.figure(figsize=(12, 6))
for i in range(20):
    plt.subplot(4, 5, i + 1)
    plt.imshow(x_train[i], cmap="gray")
    plt.title(f"Etiqueta: {y_train[i]}")
    plt.axis("off")

plt.suptitle("Ejemplos del Dataset MNIST", fontsize=14)
plt.tight_layout()
plt.savefig("../img/04_mnist_ejemplos.png", dpi=150, bbox_inches="tight")
print("\n✓ Ejemplos guardados en: ../img/04_mnist_ejemplos.png")
plt.show()


# Preprocesamiento de datos
print("\n" + "=" * 60)
print("PREPROCESAMIENTO")
print("=" * 60)

# 1. Normalizar píxeles a rango [0, 1]
x_train_norm = x_train.astype("float32") / 255.0
x_test_norm = x_test.astype("float32") / 255.0

# 2. Aplanar imágenes de (28, 28) a (784,) para red densa
x_train_flat = x_train_norm.reshape(-1, 28 * 28)
x_test_flat = x_test_norm.reshape(-1, 28 * 28)

print(f"\n✓ Datos preprocesados:")
print(f"  - Forma original: {x_train.shape}")
print(f"  - Forma aplanada: {x_train_flat.shape}")
print(f"  - Rango de valores: [{x_train_flat.min()}, {x_train_flat.max()}]")


# Construir modelo de red neuronal
print("\n" + "=" * 60)
print("CONSTRUCCIÓN DEL MODELO")
print("=" * 60)


def crear_modelo():
    """
    Crea una red neuronal densa (fully connected) para clasificación.

    Arquitectura:
        Input (784) → Dense(128, relu) → Dropout(0.2)
        → Dense(64, relu) → Dropout(0.2)
        → Dense(10, softmax)
    """
    model = keras.Sequential(
        [
            layers.Input(shape=(784,), name="input_imagen"),
            # Primera capa oculta
            layers.Dense(128, activation="relu", name="hidden_1"),
            layers.Dropout(0.2),  # Dropout para evitar overfitting
            # Segunda capa oculta
            layers.Dense(64, activation="relu", name="hidden_2"),
            layers.Dropout(0.2),
            # Capa de salida: 10 neuronas (una por cada dígito)
            layers.Dense(10, activation="softmax", name="output"),
        ],
        name="mnist_classifier",
    )

    return model


# Crear y compilar modelo
model = crear_modelo()

model.compile(
    optimizer="adam",  # Optimizador adaptativo
    loss="sparse_categorical_crossentropy",  # Para clasificación multi-clase
    metrics=["accuracy"],  # Métrica: precisión
)

print("\n✓ Arquitectura del Modelo:")
model.summary()

print(
    """
EXPLICACIÓN DE COMPONENTES:
- Input(784): Imagen aplanada (28x28 = 784 píxeles)
- Dense(128): 128 neuronas, aprenden características
- ReLU: Función de activación (no linealidad)
- Dropout(0.2): Desactiva 20% de neuronas aleatoriamente (previene overfitting)
- Dense(10): 10 neuronas de salida (una por dígito)
- Softmax: Convierte salidas a probabilidades [0-1] que suman 1
"""
)


# Entrenar el modelo
print("\n" + "=" * 60)
print("ENTRENAMIENTO")
print("=" * 60)

print("\nEntrenando modelo (esto puede tardar 1-2 minutos)...\n")

history = model.fit(
    x_train_flat,
    y_train,
    epochs=10,  # 10 pasadas completas por el dataset
    batch_size=128,  # Procesar 128 imágenes a la vez
    validation_split=0.1,  # Usar 10% de datos para validación
    verbose=1,
)

print("\n✓ Entrenamiento completado")

# Guardar modelo
modelo_path = "../models/mnist_classifier.keras"
model.save(modelo_path)
print(f"✓ Modelo guardado en: {modelo_path}")


# Evaluar en datos de prueba
print("\n" + "=" * 60)
print("EVALUACIÓN EN DATOS DE PRUEBA")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(x_test_flat, y_test, verbose=0)

print(f"\n✓ Resultados en datos de prueba:")
print(f"  - Pérdida: {test_loss:.4f}")
print(f"  - Precisión: {test_accuracy * 100:.2f}%")


# Visualizar curvas de aprendizaje
plt.figure(figsize=(12, 4))

# Precisión
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Entrenamiento")
plt.plot(history.history["val_accuracy"], label="Validación")
plt.title("Precisión durante el Entrenamiento")
plt.xlabel("Época")
plt.ylabel("Precisión")
plt.legend()
plt.grid(True)

# Pérdida
plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Entrenamiento")
plt.plot(history.history["val_loss"], label="Validación")
plt.title("Pérdida durante el Entrenamiento")
plt.xlabel("Época")
plt.ylabel("Pérdida")
plt.legend()
plt.grid(True)

plt.suptitle("Curvas de Aprendizaje", fontsize=14)
plt.tight_layout()
plt.savefig("../img/04_training_curves.png", dpi=150, bbox_inches="tight")
print("\n✓ Curvas guardadas en: ../img/04_training_curves.png")
plt.show()


# Hacer predicciones y visualizar
print("\n" + "=" * 60)
print("PREDICCIONES EN IMÁGENES DE PRUEBA")
print("=" * 60)

# Predecir en primeras 20 imágenes de prueba
n_ejemplos = 20
predicciones = model.predict(x_test_flat[:n_ejemplos], verbose=0)

# Para cada imagen, obtenemos un array de 10 probabilidades
# Tomamos el índice con mayor probabilidad como predicción
clases_predichas = np.argmax(predicciones, axis=1)

# Visualizar
plt.figure(figsize=(15, 8))

for i in range(n_ejemplos):
    plt.subplot(4, 5, i + 1)
    plt.imshow(x_test[i], cmap="gray")

    etiqueta_real = y_test[i]
    etiqueta_pred = clases_predichas[i]
    confianza = predicciones[i][etiqueta_pred] * 100

    # Color verde si es correcto, rojo si es incorrecto
    color = "green" if etiqueta_pred == etiqueta_real else "red"

    plt.title(f"Real: {etiqueta_real} | Pred: {etiqueta_pred}\n({confianza:.1f}%)", color=color, fontsize=9)
    plt.axis("off")

plt.suptitle("Predicciones del Modelo (Verde=Correcto, Rojo=Error)", fontsize=14)
plt.tight_layout()
plt.savefig("../img/04_predicciones.png", dpi=150, bbox_inches="tight")
print("\n✓ Predicciones guardadas en: ../img/04_predicciones.png")
plt.show()


# Matriz de confusión
print("\n" + "=" * 60)
print("ANÁLISIS DE ERRORES: MATRIZ DE CONFUSIÓN")
print("=" * 60)

from sklearn.metrics import classification_report, confusion_matrix

# Predecir en todo el conjunto de prueba
y_pred = np.argmax(model.predict(x_test_flat, verbose=0), axis=1)

# Calcular matriz de confusión
cm = confusion_matrix(y_test, y_pred)

# Visualizar
plt.figure(figsize=(10, 8))
plt.imshow(cm, interpolation="nearest", cmap="Blues")
plt.title("Matriz de Confusión")
plt.colorbar()

# Etiquetas
tick_marks = np.arange(10)
plt.xticks(tick_marks, range(10))
plt.yticks(tick_marks, range(10))
plt.xlabel("Predicción")
plt.ylabel("Etiqueta Real")

# Agregar números en cada celda
thresh = cm.max() / 2.0
for i in range(10):
    for j in range(10):
        plt.text(
            j,
            i,
            format(cm[i, j], "d"),
            ha="center",
            va="center",
            color="white" if cm[i, j] > thresh else "black",
        )

plt.tight_layout()
plt.savefig("../img/04_confusion_matrix.png", dpi=150, bbox_inches="tight")
print("\n✓ Matriz guardada en: ../img/04_confusion_matrix.png")
plt.show()

# Reporte de clasificación
print("\n" + "=" * 60)
print("REPORTE DE CLASIFICACIÓN DETALLADO")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=[str(i) for i in range(10)]))


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print(f"""
1. APRENDIZAJE SUPERVISADO: Usamos 60,000 imágenes etiquetadas para entrenar

2. PRECISIÓN ALCANZADA: {test_accuracy * 100:.2f}%
   - Muy bueno para un modelo simple
   - CNNs pueden alcanzar >99% (siguiente archivo)

3. ARQUITECTURA SIMPLE:
   - Solo capas Dense (fully connected)
   - No aprovecha estructura espacial de la imagen
   - 784 → 128 → 64 → 10 neuronas

4. VENTAJAS:
   - Rápido de entrenar (1-2 minutos)
   - Fácil de entender
   - Buena precisión para empezar

5. DESVENTAJAS:
   - Muchos parámetros (784×128 = ~100K en primera capa)
   - No captura patrones espaciales (vecindad de píxeles)
   - Menos preciso que CNNs

6. CONCEPTOS CLAVE:
   - Normalización: [0, 255] → [0, 1]
   - Dropout: Previene overfitting
   - Softmax: Salida como probabilidades
   - Categorical Crossentropy: Función de pérdida para clasificación

PRÓXIMO PASO: Mejorar con CNN que SÍ aprovecha estructura espacial (archivo 05)
""")
