# 09 - Computer Vision + Machine Learning

Este módulo integra técnicas de **Machine Learning** (Aprendizaje Automático) con **Computer Vision** (Visión por Computadora), aplicando modelos de aprendizaje supervisado, no supervisado y por refuerzo a imágenes.

## 📋 Contenido

### Aprendizaje No Supervisado (Unsupervised Learning)

- **01_kmeans_segmentacion_imagen.py**: Segmentación de imágenes usando K-Means clustering para agrupar píxeles por color/similitud
- **02_pca_eigenfaces.py**: Reducción dimensional con PCA (Principal Component Analysis) aplicado a reconocimiento facial
- **03_autoencoder_denoising_keras.py**: Red neuronal autoencoder para eliminar ruido en imágenes

### Aprendizaje Supervisado (Supervised Learning)

- **04_clasificacion_mnist_keras.py**: Clasificación de dígitos manuscritos (0-9) con red neuronal densa
- **05_cnn_basica_keras.py**: Red neuronal convolucional (CNN) básica para clasificación de imágenes
- **06_cnn_cifar10_keras.py**: CNN más compleja para clasificar imágenes en 10 categorías (CIFAR-10)
- **07_transfer_learning_imagenet.py**: Transfer Learning usando modelos preentrenados (VGG16/ResNet50)

### Aprendizaje por Refuerzo (Reinforcement Learning)

- **08_rl_grid_vision.py**: Agente que aprende a navegar en un grid usando información visual de píxeles

### Detección de Objetos (Object Detection)

- **09_deteccion_yolo_opencv.py**: Detección de múltiples objetos en tiempo real usando YOLO v3

### Práctica

- **10_ejercicios_propuestos.py**: Ejercicios guiados para practicar cada técnica

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib tensorflow keras scikit-learn pillow
```

**Opcional para YOLO:**
- Descargar archivos de configuración y pesos de YOLO (se indica en el script)

## 📁 Estructura del Proyecto

```text
09_cv_ml/
├── README.md
├── src/
│   ├── 01_kmeans_segmentacion_imagen.py
│   ├── 02_pca_eigenfaces.py
│   ├── 03_autoencoder_denoising_keras.py
│   ├── 04_clasificacion_mnist_keras.py
│   ├── 05_cnn_basica_keras.py
│   ├── 06_cnn_cifar10_keras.py
│   ├── 07_transfer_learning_imagenet.py
│   ├── 08_rl_grid_vision.py
│   ├── 09_deteccion_yolo_opencv.py
│   └── 10_ejercicios_propuestos.py
├── img/                    # Imágenes de prueba
├── datasets/               # Datasets descargados automáticamente
└── models/                 # Modelos entrenados guardados
```

## 🚀 Uso

### Orden Sugerido para Aprendizaje

**1. Aprendizaje No Supervisado (empezar aquí - más exploratorio)**

```bash
cd src
python 01_kmeans_segmentacion_imagen.py
python 02_pca_eigenfaces.py
python 03_autoencoder_denoising_keras.py
```

**2. Aprendizaje Supervisado (progresión de complejidad)**

```bash
python 04_clasificacion_mnist_keras.py
python 05_cnn_basica_keras.py
python 06_cnn_cifar10_keras.py
python 07_transfer_learning_imagenet.py
```

**3. Aprendizaje por Refuerzo**

```bash
python 08_rl_grid_vision.py
```

**4. Detección de Objetos (bonus)**

```bash
python 09_deteccion_yolo_opencv.py
```

**5. Ejercicios Prácticos**

```bash
python 10_ejercicios_propuestos.py
```

## 📚 Conceptos Clave

### Machine Learning (ML)

**Machine Learning** es una rama de la IA que permite a las computadoras aprender patrones de los datos sin ser explícitamente programadas.

### Tipos de Aprendizaje

#### 1. **Aprendizaje No Supervisado**
- **Sin etiquetas**: El modelo encuentra patrones por sí mismo
- **Objetivo**: Descubrir estructura oculta en los datos
- **Ejemplos**: Clustering (K-Means), Reducción dimensional (PCA), Autoencoders

#### 2. **Aprendizaje Supervisado**
- **Con etiquetas**: Se entrena con datos de entrada y salida conocidas
- **Objetivo**: Aprender mapeo de entrada → salida
- **Ejemplos**: Clasificación (identificar dígitos), Regresión (predecir valores)

#### 3. **Aprendizaje por Refuerzo**
- **Basado en recompensas**: El agente aprende a tomar decisiones para maximizar recompensas
- **Objetivo**: Encontrar la mejor política de acción
- **Ejemplos**: Juegos, robótica, navegación

### Redes Neuronales Convolucionales (CNN)

Las **CNN** son especialmente efectivas para imágenes porque:
- **Capas convolucionales**: Detectan características locales (bordes, texturas, formas)
- **Pooling**: Reduce dimensionalidad manteniendo información importante
- **Jerarquía**: Capas iniciales detectan bordes, capas profundas detectan objetos completos

**Conexión con módulo 06**: Las CNN automatizan lo que hacíamos manualmente con filtros de convolución (Sobel, Laplaciano, etc.)

### Transfer Learning

Usar modelos pre-entrenados en grandes datasets (ImageNet) y ajustarlos a nuestro problema específico.

**Ventajas**:
- Menos datos de entrenamiento necesarios
- Entrenamiento más rápido
- Mejor rendimiento

## 🔗 Conexión con Módulos Anteriores

### Relación con Módulo 07 (Segmentación)

- **K-Means** es una forma de segmentación automática por color
- Complementa técnicas manuales como máscaras HSV y Watershed

### Relación con Módulo 08 (Reconocimiento Facial)

- **PCA/Eigenfaces** es una técnica clásica de reconocimiento facial
- **CNNs** son la evolución moderna (más precisas que Haar Cascade y LBPH)
- **YOLO** puede detectar rostros y muchos otros objetos simultáneamente

## 🛠️ Frameworks Utilizados

### TensorFlow + Keras

**Keras** es la API de alto nivel integrada en TensorFlow 2.x para construir redes neuronales fácilmente.

```python
from tensorflow import keras
from tensorflow.keras import layers

# Crear modelo
model = keras.Sequential([
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

### Scikit-learn

Librería para ML clásico (K-Means, PCA, SVM, etc.)

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
```

## 📊 Datasets Utilizados

- **MNIST**: 60,000 imágenes de dígitos manuscritos (28x28 píxeles)
- **CIFAR-10**: 60,000 imágenes en 10 clases (32x32 píxeles, color)
- **ImageNet**: Millones de imágenes en 1000 categorías (para modelos preentrenados)
- **Olivetti Faces**: 400 imágenes de rostros (64x64 píxeles) para PCA

## 💡 Consejos Prácticos

1. **Empezar simple**: Probar con modelos pequeños antes de ir a redes profundas
2. **Normalizar datos**: Escalar píxeles a rango [0,1] mejora el entrenamiento
3. **Data augmentation**: Rotar, voltear imágenes para aumentar dataset
4. **Evitar overfitting**: Usar dropout, regularización, y validación cruzada
5. **Guardar modelos**: No re-entrenar cada vez, guardar pesos entrenados
6. **GPU acelera**: TensorFlow automáticamente usa GPU si está disponible

## 🎯 Aplicaciones Prácticas

- **Clasificación**: Identificar objetos, animales, enfermedades en imágenes médicas
- **Detección**: Localizar personas, vehículos, señales de tráfico
- **Segmentación**: Separar fondo de primer plano, identificar tumores
- **Generación**: Crear imágenes sintéticas (GANs - módulo futuro)
- **Reconocimiento facial**: Sistemas de seguridad, desbloqueo de dispositivos
- **OCR**: Reconocimiento de texto en imágenes (Google Lens, escaneo documentos)

## 📖 Referencias

### Documentación Oficial

- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)
- [Keras Documentation](https://keras.io/)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [OpenCV DNN Module](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)

### Tutoriales y Recursos

- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [Keras Examples](https://keras.io/examples/)
- [CS231n: CNN for Visual Recognition (Stanford)](http://cs231n.stanford.edu/)
- [YOLO Official Site](https://pjreddie.com/darknet/yolo/)

### Papers Importantes

- [ImageNet Classification with Deep CNNs (AlexNet)](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
- [You Only Look Once (YOLO)](https://arxiv.org/abs/1506.02640)
- [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)

## 🎓 Glosario

- **Epoch**: Una pasada completa por todo el dataset de entrenamiento
- **Batch**: Subconjunto de datos procesados simultáneamente
- **Learning Rate**: Tasa de aprendizaje, controla velocidad de ajuste de pesos
- **Overfitting**: Modelo memoriza datos de entrenamiento pero no generaliza
- **Underfitting**: Modelo muy simple, no captura patrones importantes
- **Accuracy**: Porcentaje de predicciones correctas
- **Loss**: Función de error que el modelo intenta minimizar
- **Dropout**: Técnica para prevenir overfitting desactivando neuronas aleatoriamente
- **Activation Function**: Función no lineal (ReLU, sigmoid, softmax)
- **Backpropagation**: Algoritmo para ajustar pesos de la red neuronal

## ⚠️ Notas Importantes

1. **Entrenamiento toma tiempo**: Modelos profundos pueden tardar minutos/horas
2. **RAM necesaria**: Algunos modelos requieren 4GB+ de RAM
3. **GPU opcional**: Acelera entrenamiento 10-100x, pero no es obligatoria
4. **Primeras epochs lentas**: TensorFlow compila el grafo, luego acelera
5. **Aleatoridad**: Resultados pueden variar ligeramente entre ejecuciones

---

**Última actualización**: Noviembre 2025

**Profesor**: Ing. Alexis González - IUA 2025
