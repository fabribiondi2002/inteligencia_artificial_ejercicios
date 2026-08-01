"""
01 - Segmentación de Imagen con K-Means Clustering
===================================================

APRENDIZAJE NO SUPERVISADO: El algoritmo agrupa píxeles similares sin etiquetas previas.

CONEXIÓN CON MÓDULO 07 (Segmentación):
- En el módulo 07 usamos máscaras HSV y Watershed para segmentar manualmente
- K-Means automatiza la segmentación agrupando píxeles por similitud de color
- Es útil cuando no conocemos a priori los colores a segmentar

¿Cómo funciona K-Means?
1. Elegimos K (número de grupos/clusters)
2. Inicializa K centroides aleatorios
3. Asigna cada píxel al centroide más cercano
4. Recalcula centroides como promedio de sus píxeles
5. Repite hasta convergencia

Aplicaciones:
- Compresión de imágenes (reducir paleta de colores)
- Segmentación automática de objetos
- Separar fondo de primer plano
"""

import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Crear carpeta para resultados si no existe
os.makedirs("../img", exist_ok=True)


def segmentar_kmeans(imagen, k=3):
    """
    Segmenta una imagen usando K-Means clustering.

    Args:
        imagen: Imagen BGR de OpenCV
        k: Número de clusters (grupos de colores)

    Returns:
        imagen_segmentada: Imagen con K colores únicos
        etiquetas: Array con la etiqueta de cluster de cada píxel
        centroides: Colores RGB de cada cluster
    """
    # Convertir de BGR (OpenCV) a RGB (para visualización correcta)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # Reshape: convertir imagen (H, W, 3) a array de píxeles (H*W, 3)
    # Cada fila es un píxel con sus 3 valores RGB
    pixeles = imagen_rgb.reshape(-1, 3)

    # Aplicar K-Means
    # n_init='auto' evita warnings de versiones nuevas de scikit-learn
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    kmeans.fit(pixeles)

    # Obtener etiquetas (a qué cluster pertenece cada píxel)
    etiquetas = kmeans.labels_

    # Obtener centroides (color promedio de cada cluster)
    centroides = kmeans.cluster_centers_.astype(int)

    # Crear imagen segmentada: reemplazar cada píxel por el color de su centroide
    imagen_segmentada = centroides[etiquetas]

    # Reshape de vuelta a forma de imagen
    imagen_segmentada = imagen_segmentada.reshape(imagen_rgb.shape)

    return imagen_segmentada, etiquetas.reshape(imagen_rgb.shape[:2]), centroides


def visualizar_clusters(etiquetas, k):
    """
    Crea una imagen donde cada cluster tiene un color único para visualización.
    """
    # Asignar colores distintivos a cada cluster
    colores = plt.cm.rainbow(np.linspace(0, 1, k))[:, :3] * 255
    imagen_clusters = colores[etiquetas].astype(np.uint8)
    return imagen_clusters


# Ejemplo 1: Segmentar imagen sintética
print("=" * 60)
print("EJEMPLO 1: Segmentación de imagen con colores definidos")
print("=" * 60)

# Crear imagen sintética con 3 regiones de colores
imagen_sintetica = np.zeros((300, 400, 3), dtype=np.uint8)
imagen_sintetica[:100, :] = [255, 0, 0]  # Azul
imagen_sintetica[100:200, :] = [0, 255, 0]  # Verde
imagen_sintetica[200:, :] = [0, 0, 255]  # Rojo

# Agregar ruido para hacerlo más realista
ruido = np.random.randint(-30, 30, imagen_sintetica.shape, dtype=np.int16)
imagen_sintetica = np.clip(imagen_sintetica.astype(np.int16) + ruido, 0, 255).astype(
    np.uint8
)

# Aplicar K-Means con K=3
k = 3
segmentada, etiquetas, centroides = segmentar_kmeans(imagen_sintetica, k)
clusters_visual = visualizar_clusters(etiquetas, k)

print(f"\nNúmero de clusters: {k}")
print(f"Centroides (colores RGB promedio de cada cluster):")
for i, centroide in enumerate(centroides):
    print(f"  Cluster {i}: RGB{tuple(centroide)}")

# Visualizar resultados
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(imagen_sintetica, cv2.COLOR_BGR2RGB))
plt.title("Imagen Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(clusters_visual)
plt.title(f"Clusters Identificados (K={k})")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(segmentada)
plt.title("Imagen Segmentada")
plt.axis("off")

plt.tight_layout()
plt.savefig("../img/01_kmeans_sintetica.png", dpi=150, bbox_inches="tight")
print("\n✓ Resultado guardado en: ../img/01_kmeans_sintetica.png")
plt.show()


# Ejemplo 2: Compresión de imagen (reducir paleta de colores)
print("\n" + "=" * 60)
print("EJEMPLO 2: Compresión de imagen reduciendo colores")
print("=" * 60)

# Crear imagen con gradiente de colores
x = np.linspace(0, 255, 400)
y = np.linspace(0, 255, 300)
X, Y = np.meshgrid(x, y)

imagen_gradiente = np.zeros((300, 400, 3), dtype=np.uint8)
imagen_gradiente[:, :, 0] = X.astype(np.uint8)  # Canal B
imagen_gradiente[:, :, 1] = Y.astype(np.uint8)  # Canal G
imagen_gradiente[:, :, 2] = (255 - X).astype(np.uint8)  # Canal R

# Comparar diferentes valores de K
valores_k = [2, 5, 10, 20]

plt.figure(figsize=(16, 10))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(imagen_gradiente, cv2.COLOR_BGR2RGB))
plt.title(f"Original ({300 * 400} colores)")
plt.axis("off")

for idx, k_val in enumerate(valores_k):
    segmentada, _, _ = segmentar_kmeans(imagen_gradiente, k_val)

    plt.subplot(2, 3, idx + 2)
    plt.imshow(segmentada)
    plt.title(f"K={k_val} colores")
    plt.axis("off")

plt.suptitle("Compresión de Imagen: Reducción de Paleta de Colores con K-Means")
plt.tight_layout()
plt.savefig("../img/01_kmeans_compresion.png", dpi=150, bbox_inches="tight")
print("\n✓ Resultado guardado en: ../img/01_kmeans_compresion.png")
plt.show()


# Ejemplo 3: Uso con imagen real (si existe)
print("\n" + "=" * 60)
print("EJEMPLO 3: Aplicación a imagen real")
print("=" * 60)

# Intentar cargar una imagen del módulo 07
rutas_posibles = [
    "../img/colores.png",
    "../../07_cv_segmentacion/img/colores.png",
    "../../07_cv_segmentacion/img/rosas.jpeg",
]

imagen_real = None
for ruta in rutas_posibles:
    if os.path.exists(ruta):
        imagen_real = cv2.imread(ruta)
        if imagen_real is not None:
            print(f"\n✓ Imagen cargada desde: {ruta}")
            break

if imagen_real is not None:
    # Redimensionar si es muy grande
    altura, ancho = imagen_real.shape[:2]
    if ancho > 600:
        factor = 600 / ancho
        imagen_real = cv2.resize(
            imagen_real, (600, int(altura * factor)), interpolation=cv2.INTER_AREA
        )

    # Aplicar K-Means con diferentes valores de K
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(imagen_real, cv2.COLOR_BGR2RGB))
    plt.title("Imagen Original")
    plt.axis("off")

    for idx, k in enumerate([3, 5, 7, 10, 15]):
        segmentada, _, _ = segmentar_kmeans(imagen_real, k)

        plt.subplot(2, 3, idx + 2)
        plt.imshow(segmentada)
        plt.title(f"K={k} clusters")
        plt.axis("off")

    plt.suptitle("Segmentación con K-Means: Diferentes Valores de K")
    plt.tight_layout()
    plt.savefig("../img/01_kmeans_real.png", dpi=150, bbox_inches="tight")
    print("✓ Resultado guardado en: ../img/01_kmeans_real.png")
    plt.show()
else:
    print(
        "\n⚠ No se encontró imagen de ejemplo. "
        "Coloca una imagen en ../img/ para probar con imagen real."
    )


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print("""
1. K-Means NO SUPERVISADO: No necesita etiquetas, encuentra patrones automáticamente
2. K pequeño: Simplifica imagen (bueno para compresión)
3. K grande: Captura más detalles (mejor segmentación)
4. TRADE-OFF: Más clusters = más detalle pero más costo computacional
5. CONEXIÓN con Módulo 07: K-Means complementa segmentación manual por color

VENTAJAS:
- Simple y rápido
- No necesita conocer los colores a priori
- Útil para compresión y segmentación automática

DESVENTAJAS:
- Necesita definir K manualmente
- Sensible a valores iniciales
- Agrupa por color, no por semántica (puede dividir un objeto en varios clusters)

PRÓXIMO PASO: Ver PCA para reducción dimensional (archivo 02)
""")

cv2.waitKey(0)
cv2.destroyAllWindows()
