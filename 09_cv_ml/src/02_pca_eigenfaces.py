"""
02 - PCA y Eigenfaces para Reconocimiento Facial
==================================================

APRENDIZAJE NO SUPERVISADO: PCA encuentra componentes principales sin etiquetas.

CONEXIÓN CON MÓDULO 08 (Reconocimiento Facial):
- En el módulo 08 usamos EigenFaces, FisherFaces y LBPH
- Este ejemplo muestra cómo funciona PCA detrás de EigenFaces
- PCA reduce dimensionalidad (de miles de píxeles a ~50 componentes principales)

¿Qué es PCA (Principal Component Analysis)?
- Técnica de reducción dimensional
- Encuentra las direcciones de máxima varianza en los datos
- Transforma datos de alta dimensión a espacio de menor dimensión
- Preserva la mayor información posible

¿Cómo funciona Eigenfaces?
1. Calcula el "rostro promedio" de todos los rostros
2. Resta el promedio a cada rostro (centra los datos)
3. Encuentra las "eigenfaces" (componentes principales)
4. Proyecta nuevos rostros en el espacio de eigenfaces
5. Compara por distancia euclidiana

Aplicaciones:
- Reconocimiento facial (método clásico)
- Compresión de imágenes
- Visualización de datos de alta dimensión
- Reducción de ruido
"""

import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_olivetti_faces
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

# Crear carpeta para resultados
os.makedirs("../img", exist_ok=True)
os.makedirs("../models", exist_ok=True)

print("=" * 60)
print("CARGANDO DATASET OLIVETTI FACES")
print("=" * 60)

# Cargar dataset de rostros (400 imágenes de 40 personas, 10 por persona)
print("\nDescargando dataset Olivetti Faces...")
dataset = fetch_olivetti_faces(shuffle=True, random_state=42)

# Características del dataset
X = dataset.data  # (400, 4096) - cada imagen es 64x64 = 4096 píxeles
y = dataset.target  # (400,) - etiquetas de 0 a 39 (40 personas)
n_samples, n_features = X.shape
n_classes = len(np.unique(y))
h, w = dataset.images.shape[1:3]  # 64x64

print(f"\n✓ Dataset cargado:")
print(f"  - {n_samples} imágenes de rostros")
print(f"  - {n_classes} personas diferentes")
print(f"  - Resolución: {h}x{w} píxeles")
print(f"  - Dimensionalidad original: {n_features} píxeles por imagen")

# Visualizar algunas imágenes del dataset
print("\n" + "=" * 60)
print("VISUALIZACIÓN DEL DATASET")
print("=" * 60)

plt.figure(figsize=(12, 6))
for i in range(20):
    plt.subplot(4, 5, i + 1)
    plt.imshow(dataset.images[i], cmap="gray")
    plt.title(f"Persona {y[i]}")
    plt.axis("off")

plt.suptitle("Muestra del Dataset Olivetti Faces", fontsize=14)
plt.tight_layout()
plt.savefig("../img/02_dataset_olivetti.png", dpi=150, bbox_inches="tight")
print("\n✓ Visualización guardada en: ../img/02_dataset_olivetti.png")
plt.show()


# Ejemplo 1: Aplicar PCA para reducción dimensional
print("\n" + "=" * 60)
print("EJEMPLO 1: Reducción Dimensional con PCA")
print("=" * 60)

# Elegir número de componentes principales
n_components = 150

print(f"\nAplicando PCA con {n_components} componentes...")
pca = PCA(n_components=n_components, whiten=True, random_state=42)
X_pca = pca.fit_transform(X)

print(f"\n✓ Dimensionalidad reducida:")
print(f"  - Original: {n_features} dimensiones (píxeles)")
print(f"  - Después de PCA: {n_components} dimensiones")
print(f"  - Reducción: {(1 - n_components/n_features) * 100:.1f}%")
print(
    f"  - Varianza explicada: {pca.explained_variance_ratio_.sum() * 100:.2f}% de la información original"
)


# Visualizar Eigenfaces (componentes principales)
print("\n" + "=" * 60)
print("EJEMPLO 2: Visualización de Eigenfaces")
print("=" * 60)

eigenfaces = pca.components_.reshape((n_components, h, w))

plt.figure(figsize=(15, 8))
for i in range(20):
    plt.subplot(4, 5, i + 1)
    plt.imshow(eigenfaces[i], cmap="gray")
    plt.title(f"Eigenface {i+1}\n({pca.explained_variance_ratio_[i]*100:.1f}%)")
    plt.axis("off")

plt.suptitle(
    "Las 20 Primeras Eigenfaces (Componentes Principales)", fontsize=14, y=1.02
)
plt.tight_layout()
plt.savefig("../img/02_eigenfaces.png", dpi=150, bbox_inches="tight")
print("\n✓ Eigenfaces guardadas en: ../img/02_eigenfaces.png")
plt.show()

print(
    """
INTERPRETACIÓN:
- Cada eigenface captura un "patrón" común en los rostros
- Las primeras eigenfaces capturan más varianza (son más importantes)
- La combinación lineal de estas eigenfaces puede reconstruir cualquier rostro
"""
)


# Ejemplo 3: Reconstrucción de rostros con diferentes números de componentes
print("\n" + "=" * 60)
print("EJEMPLO 3: Reconstrucción de Rostros")
print("=" * 60)

# Tomar un rostro de ejemplo
idx_ejemplo = 42
rostro_original = X[idx_ejemplo].reshape(h, w)

# Reconstruir con diferentes números de componentes
componentes_a_probar = [5, 10, 25, 50, 100, 150]

plt.figure(figsize=(16, 6))

# Mostrar rostro original
plt.subplot(2, 4, 1)
plt.imshow(rostro_original, cmap="gray")
plt.title("Original")
plt.axis("off")

# Calcular "rostro promedio"
rostro_promedio = pca.mean_.reshape(h, w)
plt.subplot(2, 4, 2)
plt.imshow(rostro_promedio, cmap="gray")
plt.title("Rostro Promedio")
plt.axis("off")

# Reconstruir con diferentes números de componentes
for idx, n_comp in enumerate(componentes_a_probar):
    # Aplicar PCA con n_comp componentes (fit en TODO el dataset)
    pca_temp = PCA(n_components=n_comp, whiten=True, random_state=42)
    pca_temp.fit(X)  # Fit con todo el dataset
    
    # Transformar solo la imagen de ejemplo
    X_reducido = pca_temp.transform(X[idx_ejemplo : idx_ejemplo + 1])
    X_reconstruido = pca_temp.inverse_transform(X_reducido)

    rostro_reconstruido = X_reconstruido[0].reshape(h, w)

    plt.subplot(2, 4, idx + 3)
    plt.imshow(rostro_reconstruido, cmap="gray")
    plt.title(f"{n_comp} componentes")
    plt.axis("off")

plt.suptitle("Reconstrucción de Rostro: Efecto del Número de Componentes", fontsize=14)
plt.tight_layout()
plt.savefig("../img/02_reconstruccion.png", dpi=150, bbox_inches="tight")
print("\n✓ Reconstrucción guardada en: ../img/02_reconstruccion.png")
plt.show()


# Ejemplo 4: Reconocimiento facial usando PCA
print("\n" + "=" * 60)
print("EJEMPLO 4: Reconocimiento Facial con PCA")
print("=" * 60)

# Dividir dataset en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"\nDatos de entrenamiento: {len(X_train)} imágenes")
print(f"Datos de prueba: {len(X_test)} imágenes")

# Entrenar PCA
n_components = 100
pca_model = PCA(n_components=n_components, whiten=True, random_state=42)
X_train_pca = pca_model.fit_transform(X_train)
X_test_pca = pca_model.transform(X_test)

print(f"\n✓ Modelo PCA entrenado con {n_components} componentes")


# Función simple de reconocimiento por distancia euclidiana
def reconocer_rostro(rostro_test, rostros_train, etiquetas_train, k=1):
    """
    Reconoce un rostro por k-vecinos más cercanos en espacio PCA.

    Args:
        rostro_test: Vector PCA del rostro a reconocer
        rostros_train: Vectores PCA de rostros conocidos
        etiquetas_train: Etiquetas de rostros conocidos
        k: Número de vecinos a considerar

    Returns:
        etiqueta_predicha: Persona identificada
    """
    # Calcular distancias euclidianas a todos los rostros de entrenamiento
    distancias = np.linalg.norm(rostros_train - rostro_test, axis=1)

    # Encontrar k vecinos más cercanos
    indices_cercanos = np.argsort(distancias)[:k]
    etiquetas_cercanas = etiquetas_train[indices_cercanos]

    # Votar por la etiqueta más común
    etiqueta_predicha = np.bincount(etiquetas_cercanas).argmax()

    return etiqueta_predicha, distancias[indices_cercanos[0]]


# Probar reconocimiento en imágenes de prueba
aciertos = 0
ejemplos_mostrar = 12

plt.figure(figsize=(16, 8))

for i in range(ejemplos_mostrar):
    rostro_test = X_test_pca[i]
    etiqueta_real = y_test[i]

    # Reconocer
    etiqueta_predicha, distancia = reconocer_rostro(rostro_test, X_train_pca, y_train)

    # Contar acierto
    if etiqueta_predicha == etiqueta_real:
        aciertos += 1

    # Visualizar
    plt.subplot(3, 4, i + 1)
    plt.imshow(X_test[i].reshape(h, w), cmap="gray")

    color = "green" if etiqueta_predicha == etiqueta_real else "red"
    plt.title(
        f"Real: {etiqueta_real} | Pred: {etiqueta_predicha}\nDist: {distancia:.2f}",
        color=color,
    )
    plt.axis("off")

plt.suptitle("Reconocimiento Facial con PCA + k-NN", fontsize=14)
plt.tight_layout()
plt.savefig("../img/02_reconocimiento.png", dpi=150, bbox_inches="tight")
print("\n✓ Resultados guardados en: ../img/02_reconocimiento.png")
plt.show()

# Calcular precisión total
precisiones_por_k = []
for k_val in [1, 3, 5]:
    aciertos_total = 0
    for i in range(len(X_test)):
        etiqueta_predicha, _ = reconocer_rostro(
            X_test_pca[i], X_train_pca, y_train, k=k_val
        )
        if etiqueta_predicha == y_test[i]:
            aciertos_total += 1

    precision = (aciertos_total / len(X_test)) * 100
    precisiones_por_k.append(precision)
    print(f"Precisión con k={k_val}: {precision:.1f}%")


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print(f"""
1. PCA es NO SUPERVISADO: Solo usa los datos, no las etiquetas (persona)
2. Reducción dramática: {n_features} → {n_components} dimensiones ({(1-n_components/n_features)*100:.0f}% menos)
3. Eigenfaces capturan patrones faciales comunes
4. Más componentes = mejor reconstrucción pero más costo computacional
5. Reconocimiento simple por distancia euclidiana es efectivo

CONEXIÓN CON MÓDULO 08:
- EigenFaces de OpenCV usa PCA internamente (lo que hicimos aquí)
- FisherFaces es similar pero usa LDA (Linear Discriminant Analysis)
- LBPH no usa reducción dimensional, trabaja con patrones locales

VENTAJAS DE PCA:
- Reduce dimensionalidad manteniendo información
- Rápido y eficiente
- Útil para visualización

DESVENTAJAS:
- Sensible a iluminación y pose
- Lineal (no captura relaciones no lineales)
- Necesita muchas imágenes por persona

PRECISIÓN OBTENIDA: {precisiones_por_k[0]:.1f}% con k=1
Comparable con métodos del módulo 08 en datasets pequeños.

PRÓXIMO PASO: Ver Autoencoders (redes neuronales para reducción dimensional) en archivo 03
""")

cv2.waitKey(0)
cv2.destroyAllWindows()
