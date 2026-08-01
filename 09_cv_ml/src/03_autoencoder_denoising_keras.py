"""
03 - Autoencoder para Denoising (Eliminación de Ruido)
========================================================

APRENDIZAJE NO SUPERVISADO: El autoencoder aprende a comprimir y reconstruir sin etiquetas.

CONEXIÓN CON MÓDULO 06 (Filtros):
- En el módulo 06 usamos filtros manuales (medianBlur, GaussianBlur, bilateral) para eliminar ruido
- El autoencoder APRENDE automáticamente el mejor filtro para el ruido específico
- Es más poderoso porque aprende patrones complejos de la imagen

¿Qué es un Autoencoder?
- Red neuronal que aprende a comprimir (encode) y reconstruir (decode) datos
- Arquitectura: Encoder → Bottleneck (latent space) → Decoder
- Se entrena para que salida ≈ entrada
- El bottleneck fuerza a aprender representación compacta

Tipos de Autoencoders:
1. Básico: Compresión y reconstrucción
2. Denoising: Reconstruir imagen limpia desde imagen con ruido
3. Variacional (VAE): Generación de nuevas imágenes
4. Convolucional: Usa Conv2D en vez de Dense (mejor para imágenes)

Aplicaciones:
- Eliminación de ruido (denoising)
- Compresión de imágenes
- Detección de anomalías
- Generación de datos sintéticos
"""

import os

import matplotlib.pyplot as plt
import numpy as np

# Configurar TensorFlow para evitar warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from tensorflow.keras import layers

# Crear carpetas necesarias
os.makedirs("../img", exist_ok=True)
os.makedirs("../models", exist_ok=True)

print("=" * 60)
print("CARGANDO DATASET MNIST")
print("=" * 60)

# Cargar dataset MNIST (dígitos manuscritos)
(x_train, _), (x_test, _) = keras.datasets.mnist.load_data()

# Normalizar a rango [0, 1]
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Agregar dimensión de canal (28, 28) → (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

print(f"\n✓ Dataset cargado:")
print(f"  - Entrenamiento: {x_train.shape[0]} imágenes")
print(f"  - Prueba: {x_test.shape[0]} imágenes")
print(f"  - Resolución: {x_train.shape[1]}x{x_train.shape[2]} píxeles")


# Función para agregar ruido gaussiano
def agregar_ruido(imagenes, factor_ruido=0.5):
    """
    Agrega ruido gaussiano a las imágenes.

    Args:
        imagenes: Array de imágenes
        factor_ruido: Intensidad del ruido (0.0 a 1.0)

    Returns:
        imagenes_ruido: Imágenes con ruido agregado
    """
    ruido = np.random.normal(loc=0.0, scale=factor_ruido, size=imagenes.shape)
    imagenes_ruido = imagenes + ruido

    # Clip para mantener valores en [0, 1]
    imagenes_ruido = np.clip(imagenes_ruido, 0.0, 1.0)

    return imagenes_ruido


# Crear versiones con ruido para entrenamiento
print("\n" + "=" * 60)
print("GENERANDO IMÁGENES CON RUIDO")
print("=" * 60)

factor_ruido = 0.3  # Reducido de 0.5 a 0.3 para que el modelo pueda aprender
x_train_ruido = agregar_ruido(x_train, factor_ruido)
x_test_ruido = agregar_ruido(x_test, factor_ruido)

print(f"\n✓ Ruido gaussiano agregado (factor={factor_ruido})")
print(f"  - Nota: Factor reducido a {factor_ruido} para facilitar el aprendizaje")

# Visualizar ejemplos con y sin ruido
plt.figure(figsize=(16, 4))
n_ejemplos = 10

for i in range(n_ejemplos):
    # Original
    plt.subplot(2, n_ejemplos, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap="gray")
    plt.axis("off")
    if i == 0:
        plt.title("Originales", fontsize=12)

    # Con ruido
    plt.subplot(2, n_ejemplos, n_ejemplos + i + 1)
    plt.imshow(x_test_ruido[i].squeeze(), cmap="gray")
    plt.axis("off")
    if i == 0:
        plt.title("Con Ruido", fontsize=12)

plt.suptitle("Comparación: Imágenes Originales vs Con Ruido", fontsize=14)
plt.tight_layout()
plt.savefig("../img/03_imagenes_ruido.png", dpi=150, bbox_inches="tight")
print("✓ Comparación guardada en: ../img/03_imagenes_ruido.png")
plt.show()


# Construir arquitectura del Autoencoder Convolucional
print("\n" + "=" * 60)
print("CONSTRUCCIÓN DEL AUTOENCODER")
print("=" * 60)


def crear_autoencoder(input_shape=(28, 28, 1)):
    """
    Crea un autoencoder convolucional para denoising.

    Arquitectura:
        Encoder: 28x28x1 → 14x14x32 → 7x7x64 → Latent Space (7x7x64)
        Decoder: 7x7x64 → 14x14x32 → 28x28x1
    """

    # --- ENCODER: Comprime la imagen ---
    encoder_input = keras.Input(shape=input_shape, name="imagen_entrada")

    # Primera capa convolucional + pooling
    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(encoder_input)
    x = layers.MaxPooling2D((2, 2), padding="same")(x)  # 28x28 → 14x14

    # Segunda capa convolucional + pooling
    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    encoder_output = layers.MaxPooling2D((2, 2), padding="same")(x)  # 14x14 → 7x7

    # --- DECODER: Reconstruye la imagen ---
    # Primera capa de upsampling + convolucional
    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(encoder_output)
    x = layers.UpSampling2D((2, 2))(x)  # 7x7 → 14x14

    # Segunda capa de upsampling + convolucional
    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(x)
    x = layers.UpSampling2D((2, 2))(x)  # 14x14 → 28x28

    # Capa final: reconstruir imagen con 1 canal
    decoder_output = layers.Conv2D(
        1, (3, 3), activation="sigmoid", padding="same", name="imagen_reconstruida"
    )(x)

    # Crear modelo completo
    autoencoder = keras.Model(encoder_input, decoder_output, name="autoencoder")

    return autoencoder


# Crear y compilar modelo
autoencoder = crear_autoencoder()

# binary_crossentropy funciona mejor que MSE para imágenes normalizadas con sigmoid
autoencoder.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",  # Mejor que MSE para sigmoid
    metrics=["mae"],
)

print("\n✓ Arquitectura del Autoencoder:")
autoencoder.summary()


# Entrenar el autoencoder
print("\n" + "=" * 60)
print("ENTRENAMIENTO DEL AUTOENCODER")
print("=" * 60)

print(
    "\nINPUT: Imágenes con ruido | OUTPUT: Imágenes originales (sin ruido)"
)
print("El modelo aprende a ELIMINAR el ruido\n")

# Entrenar (puede tardar unos minutos)
print("Entrenando con 20 epochs (esto tomará 3-5 minutos)...")
print("IMPORTANTE: Observa que la pérdida (loss) debe BAJAR progresivamente\n")

history = autoencoder.fit(
    x_train_ruido,  # Entrada: imágenes con ruido
    x_train,  # Salida deseada: imágenes limpias
    epochs=20,  # Aumentado de 10 a 20 para mejor aprendizaje
    batch_size=128,
    shuffle=True,
    validation_data=(x_test_ruido, x_test),
    verbose=1,
)

print("\n✓ Entrenamiento completado")

# Guardar modelo
modelo_path = "../models/autoencoder_denoising.keras"
autoencoder.save(modelo_path)
print(f"✓ Modelo guardado en: {modelo_path}")


# Visualizar curvas de aprendizaje
print("\n" + "=" * 60)
print("EVALUACIÓN DEL MODELO")
print("=" * 60)

plt.figure(figsize=(12, 4))

# Loss
plt.subplot(1, 2, 1)
plt.plot(history.history["loss"], label="Entrenamiento")
plt.plot(history.history["val_loss"], label="Validación")
plt.title("Pérdida (MSE)")
plt.xlabel("Época")
plt.ylabel("MSE")
plt.legend()
plt.grid(True)

# MAE
plt.subplot(1, 2, 2)
plt.plot(history.history["mae"], label="Entrenamiento")
plt.plot(history.history["val_mae"], label="Validación")
plt.title("Error Absoluto Medio")
plt.xlabel("Época")
plt.ylabel("MAE")
plt.legend()
plt.grid(True)

plt.suptitle("Curvas de Aprendizaje del Autoencoder", fontsize=14)
plt.tight_layout()
plt.savefig("../img/03_training_curves.png", dpi=150, bbox_inches="tight")
print("\n✓ Curvas guardadas en: ../img/03_training_curves.png")
plt.show()


# Probar el autoencoder en imágenes de prueba
print("\n" + "=" * 60)
print("RESULTADOS: DENOISING EN IMÁGENES DE PRUEBA")
print("=" * 60)

# Predecir (eliminar ruido)
x_test_reconstruido = autoencoder.predict(x_test_ruido, verbose=0)

# Visualizar resultados
n_ejemplos = 10
plt.figure(figsize=(16, 6))

for i in range(n_ejemplos):
    # Imagen original (sin ruido)
    plt.subplot(3, n_ejemplos, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap="gray")
    plt.axis("off")
    if i == 0:
        plt.title("Original", fontsize=10)

    # Imagen con ruido (input)
    plt.subplot(3, n_ejemplos, n_ejemplos + i + 1)
    plt.imshow(x_test_ruido[i].squeeze(), cmap="gray")
    plt.axis("off")
    if i == 0:
        plt.title("Con Ruido (Input)", fontsize=10)

    # Imagen reconstruida (output del autoencoder)
    plt.subplot(3, n_ejemplos, 2 * n_ejemplos + i + 1)
    plt.imshow(x_test_reconstruido[i].squeeze(), cmap="gray")
    plt.axis("off")
    if i == 0:
        plt.title("Reconstruida (Output)", fontsize=10)

plt.suptitle(
    "Denoising con Autoencoder: Original → Con Ruido → Reconstruida", fontsize=14
)
plt.tight_layout()
plt.savefig("../img/03_denoising_results.png", dpi=150, bbox_inches="tight")
print("\n✓ Resultados guardados en: ../img/03_denoising_results.png")
plt.show()


# Calcular métricas de calidad
from sklearn.metrics import mean_absolute_error, mean_squared_error

mae_ruido = mean_absolute_error(x_test.flatten(), x_test_ruido.flatten())
mae_reconstruido = mean_absolute_error(x_test.flatten(), x_test_reconstruido.flatten())

mse_ruido = mean_squared_error(x_test.flatten(), x_test_ruido.flatten())
mse_reconstruido = mean_squared_error(x_test.flatten(), x_test_reconstruido.flatten())

print(f"\nMétricas de Calidad:")
print(f"  MAE (Original vs Con Ruido): {mae_ruido:.4f}")
print(f"  MAE (Original vs Reconstruida): {mae_reconstruido:.4f}")
print(f"  Mejora: {((mae_ruido - mae_reconstruido) / mae_ruido * 100):.1f}%")
print()
print(f"  MSE (Original vs Con Ruido): {mse_ruido:.4f}")
print(f"  MSE (Original vs Reconstruida): {mse_reconstruido:.4f}")
print(f"  Mejora: {((mse_ruido - mse_reconstruido) / mse_ruido * 100):.1f}%")


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print(f"""
1. AUTOENCODER es NO SUPERVISADO: Aprende patrones sin etiquetas de clase
   (pero SÍ necesita pares: imagen ruidosa → imagen limpia)

2. ARQUITECTURA:
   - Encoder: Comprime información (28x28x1 → 7x7x64 = 3136 píxeles)
   - Decoder: Reconstruye imagen limpia
   - Usa convoluciones (mejor que dense para imágenes)

3. DENOISING: Elimina ruido aprendiendo patrones de las imágenes limpias

4. CONEXIÓN CON MÓDULO 06:
   - Filtros manuales (Gaussian, Median): Reglas fijas
   - Autoencoder: APRENDE el mejor filtro para cada tipo de ruido
   - Más potente pero requiere entrenamiento

5. MEJORAS TÉCNICAS APLICADAS:
   - Función de pérdida: binary_crossentropy (mejor que MSE con sigmoid)
   - Ruido moderado: factor {factor_ruido} (ni muy poco ni demasiado)
   - Epochs suficientes: 20 (no 10, para convergencia adecuada)
   - Learning rate: 0.001 (balance entre velocidad y estabilidad)

6. VENTAJAS:
   - Se adapta al tipo específico de ruido
   - Puede aprender patrones complejos
   - Una vez entrenado, es muy rápido

7. DESVENTAJAS:
   - Necesita muchos datos de entrenamiento
   - Tiempo de entrenamiento (3-5 minutos)
   - Solo funciona con ruido similar al de entrenamiento

8. TIPS PARA MEJORAR:
   - Más epochs → Mejor reconstrucción (pero más lento)
   - Arquitectura más profunda → Captura más detalles
   - Batch normalization → Estabiliza entrenamiento
   - Skip connections (U-Net) → Preserva detalles

APLICACIONES PRÁCTICAS:
- Restauración de fotos antiguas
- Mejora de imágenes médicas
- Reducción de ruido en fotografía nocturna
- Compresión de imágenes (JPEG mejorado)

PRÓXIMO PASO: Ver clasificación supervisada con MNIST (archivo 04)
""")
