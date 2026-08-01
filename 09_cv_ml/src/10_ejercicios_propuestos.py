"""
10 - Ejercicios Propuestos para Practicar
==========================================

Esta es una colección de ejercicios prácticos para reforzar los conceptos
aprendidos en el módulo 09 (Computer Vision + Machine Learning).

INSTRUCCIONES:
1. Lee cada ejercicio
2. Intenta resolverlo por tu cuenta
3. Ejecuta el código de solución para verificar
4. Modifica parámetros y observa cambios

Los ejercicios están organizados por dificultad:
⭐ Básico
⭐⭐ Intermedio
⭐⭐⭐ Avanzado
"""

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

print("=" * 80)
print(" " * 20 + "EJERCICIOS PROPUESTOS - ML + CV")
print("=" * 80)

# ============================================================================
# EJERCICIO 1: K-Means con diferentes valores de K ⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 1: Experimentar con K-Means                               ⭐   ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Comprender cómo el número de clusters (K) afecta la segmentación.

TAREA:
1. Cargar una imagen del módulo 07 (ej: colores.png)
2. Aplicar K-Means con K = 2, 3, 5, 8, 12
3. Visualizar resultados y comparar
4. ¿Qué valor de K funciona mejor? ¿Por qué?

PISTAS:
- Usar código de 01_kmeans_segmentacion_imagen.py
- La función segmentar_kmeans(imagen, k) ya está lista
- Probar con diferentes imágenes

CÓDIGO BASE:
"""
)

print(
    """
import cv2
from sklearn.cluster import KMeans

def ejercicio_kmeans():
    # Tu código aquí
    imagen = cv2.imread("ruta/a/imagen.png")
    
    for k in [2, 3, 5, 8, 12]:
        # Aplicar K-Means
        # Visualizar
        pass

# ejercicio_kmeans()
"""
)

input("\nPresiona Enter para continuar al siguiente ejercicio...")

# ============================================================================
# EJERCICIO 2: PCA - Reconstrucción de rostros ⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 2: Reconstrucción con diferentes componentes PCA          ⭐   ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Ver cómo el número de componentes principales afecta la calidad de reconstrucción.

TAREA:
1. Cargar dataset Olivetti Faces (o MNIST)
2. Aplicar PCA con n_components = [5, 10, 25, 50, 100, 200]
3. Reconstruir una imagen con cada valor
4. Calcular MSE (error) para cada reconstrucción
5. Graficar: MSE vs n_components

PREGUNTAS:
- ¿A partir de cuántos componentes la reconstrucción es aceptable?
- ¿Cuánta varianza se captura con 50 componentes?

CÓDIGO BASE:
"""
)

print(
    """
from sklearn.decomposition import PCA
from sklearn.datasets import fetch_olivetti_faces
from sklearn.metrics import mean_squared_error

def ejercicio_pca():
    dataset = fetch_olivetti_faces()
    X = dataset.data
    imagen_original = X[0]
    
    errores = []
    for n_comp in [5, 10, 25, 50, 100, 200]:
        pca = PCA(n_components=n_comp)
        # Transformar y reconstruir
        # Calcular MSE
        pass
    
    # Graficar errores vs componentes

# ejercicio_pca()
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 3: Autoencoder - Diferentes niveles de ruido ⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 3: Denoising con diferentes intensidades de ruido        ⭐⭐  ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Evaluar qué tan robusto es el autoencoder ante diferentes niveles de ruido.

TAREA:
1. Entrenar autoencoder con ruido de factor 0.3
2. Probar en imágenes con ruido de factores: 0.1, 0.3, 0.5, 0.7, 0.9
3. Calcular MAE para cada nivel de ruido
4. Graficar: Factor de ruido vs MAE
5. ¿El modelo generaliza bien a ruido más intenso?

EXTENSIÓN AVANZADA ⭐⭐⭐:
- Entrenar varios autoencoders con diferentes ruidos
- Comparar rendimiento
- Implementar "ensemble" de autoencoders

CÓDIGO BASE:
"""
)

print(
    """
def ejercicio_autoencoder():
    # Entrenar con ruido 0.3
    modelo = entrenar_autoencoder(ruido=0.3)
    
    # Probar con diferentes ruidos
    for factor_ruido in [0.1, 0.3, 0.5, 0.7, 0.9]:
        x_test_ruido = agregar_ruido(x_test, factor_ruido)
        x_reconstruido = modelo.predict(x_test_ruido)
        mae = calcular_mae(x_test, x_reconstruido)
        print(f"Ruido {factor_ruido}: MAE = {mae:.4f}")

# ejercicio_autoencoder()
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 4: CNN - Data Augmentation ⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 4: Efecto del Data Augmentation en CNN                   ⭐⭐  ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Comparar precisión de CNN con y sin Data Augmentation.

TAREA:
1. Entrenar CNN en MNIST/CIFAR-10 SIN data augmentation
2. Entrenar CNN idéntica CON data augmentation
3. Comparar:
   - Precisión en entrenamiento
   - Precisión en validación
   - ¿Hay overfitting?
4. Graficar curvas de aprendizaje lado a lado

DATA AUGMENTATION A PROBAR:
- RandomFlip
- RandomRotation
- RandomZoom
- RandomBrightness (bonus)

CÓDIGO BASE:
"""
)

print(
    """
def ejercicio_augmentation():
    # Modelo SIN augmentation
    model_sin = crear_cnn()
    history_sin = model_sin.fit(x_train, y_train, ...)
    
    # Modelo CON augmentation
    model_con = crear_cnn()
    aug = keras.Sequential([RandomFlip(), RandomRotation(), ...])
    history_con = model_con.fit(aug(x_train), y_train, ...)
    
    # Comparar resultados
    comparar_historias(history_sin, history_con)

# ejercicio_augmentation()
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 5: Transfer Learning - Fine-tuning ⭐⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 5: Comparar estrategias de Transfer Learning            ⭐⭐⭐ ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Entender el impacto de diferentes estrategias de fine-tuning.

TAREA:
Entrenar 3 modelos diferentes:

1. ESTRATEGIA A: Base model 100% congelado
   - Solo entrenar capas Dense nuevas

2. ESTRATEGIA B: Base model 50% congelado
   - Descongelar últimas 20 capas

3. ESTRATEGIA C: Base model 100% entrenable
   - Todas las capas entrenables (con LR bajo)

Comparar:
- Tiempo de entrenamiento
- Precisión final
- Riesgo de overfitting

¿Cuál estrategia funciona mejor en tu caso?

CÓDIGO BASE:
"""
)

print(
    """
def ejercicio_transfer_learning():
    base = MobileNetV2(include_top=False, weights='imagenet')
    
    # Estrategia A
    base.trainable = False
    modelo_a = construir_modelo(base)
    # Entrenar...
    
    # Estrategia B
    base.trainable = True
    for layer in base.layers[:-20]:
        layer.trainable = False
    modelo_b = construir_modelo(base)
    # Entrenar...
    
    # Estrategia C
    base.trainable = True
    modelo_c = construir_modelo(base)
    modelo_c.compile(optimizer=Adam(lr=0.00001))
    # Entrenar...
    
    # Comparar

# ejercicio_transfer_learning()
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 6: RL - Diferentes recompensas ⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 6: Diseñar esquema de recompensas en RL                  ⭐⭐  ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Ver cómo el diseño de recompensas afecta el aprendizaje del agente.

TAREA:
Probar 3 esquemas de recompensas diferentes:

ESQUEMA 1 (ACTUAL):
- Cada paso: -0.1
- Meta: +10
- Obstáculo: -5

ESQUEMA 2 (MÁS PENALIZACIÓN):
- Cada paso: -0.5
- Meta: +10
- Obstáculo: -10

ESQUEMA 3 (INCENTIVO POR ACERCARSE):
- Cada paso: -0.1
- Acercarse a meta: +0.2
- Alejarse de meta: -0.2
- Meta: +10
- Obstáculo: -5

Comparar:
- Velocidad de convergencia
- Número de pasos promedio
- Tasa de éxito

CÓDIGO BASE:
"""
)

print(
    """
def ejercicio_rl_recompensas():
    esquemas = [
        {'paso': -0.1, 'meta': 10, 'obstaculo': -5},
        {'paso': -0.5, 'meta': 10, 'obstaculo': -10},
        # ... esquema 3 con lógica de distancia
    ]
    
    for i, esquema in enumerate(esquemas):
        print(f"\\nEntrenando con Esquema {i+1}")
        env = GridWorldConRecompensas(esquema)
        modelo = entrenar_agente(env, episodes=200)
        evaluar_agente(modelo, env)

# ejercicio_rl_recompensas()
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 7: YOLO - Conteo de objetos ⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 7: Contador de objetos con YOLO                          ⭐⭐  ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Crear un sistema de conteo de personas/objetos en video.

TAREA:
1. Cargar un video (o usar webcam)
2. Detectar objetos frame por frame con YOLO
3. Contar objetos por categoría:
   - Personas
   - Vehículos (car, truck, bus)
   - Animales (dog, cat, bird)
4. Mostrar estadísticas en pantalla:
   - Total de personas detectadas
   - Objetos más comunes
   - Gráfico en tiempo real

BONUS ⭐⭐⭐:
- Implementar tracking (seguir mismo objeto entre frames)
- Detectar cuando entra/sale objeto de la escena
- Guardar log de detecciones

CÓDIGO BASE:
"""
)

print(
    """
def ejercicio_yolo_conteo():
    cap = cv2.VideoCapture('video.mp4')
    net, output_layers = cargar_yolo()
    
    contadores = {'person': 0, 'car': 0, 'dog': 0}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detectar
        boxes, confs, class_ids = detectar_objetos_yolo(frame, net, output_layers)
        
        # Contar
        for class_id in class_ids:
            clase = COCO_CLASSES[class_id]
            if clase in contadores:
                contadores[clase] += 1
        
        # Mostrar estadísticas
        cv2.putText(frame, f"Personas: {contadores['person']}", ...)
        cv2.imshow('Conteo', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ejercicio_yolo_conteo()
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 8: Proyecto Integrador ⭐⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 8: PROYECTO INTEGRADOR - Sistema de Vigilancia          ⭐⭐⭐ ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Combinar múltiples técnicas del módulo en un proyecto completo.

DESCRIPCIÓN DEL PROYECTO:
Sistema de vigilancia inteligente que:

1. DETECCIÓN (YOLO):
   - Detecta personas en video/webcam
   - Dibuja bounding boxes

2. RECONOCIMIENTO FACIAL (Módulo 08 + PCA):
   - Cuando detecta persona, extraer rostro
   - Usar PCA/CNN para identificar si es "conocida"

3. CLASIFICACIÓN DE ACTIVIDAD (CNN):
   - Clasificar si la persona está:
     * Parada
     * Caminando
     * Corriendo

4. ALERTA:
   - Si persona desconocida corre → Alerta roja
   - Si persona conocida → Log normal

TÉCNICAS INTEGRADAS:
- YOLO para detección
- CNN para clasificación de actividad
- PCA/Transfer Learning para reconocimiento
- OpenCV para procesamiento

PASOS:
1. Implementar pipeline de detección
2. Entrenar clasificador de actividad (puedes usar dataset público)
3. Integrar reconocimiento facial
4. Sistema de alertas
5. Interfaz visual

BONUS:
- Guardar video con anotaciones
- Base de datos de eventos
- Dashboard con estadísticas

¡Este es un proyecto completo que demuestra dominio del módulo!
"""
)

input("\nPresiona Enter para continuar...")

# ============================================================================
# EJERCICIO 9: Optimización de Hiperparámetros ⭐⭐⭐
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║ EJERCICIO 9: Grid Search de Hiperparámetros                       ⭐⭐⭐ ║
╚═══════════════════════════════════════════════════════════════════════════╝

OBJETIVO:
Encontrar la mejor configuración de hiperparámetros para una CNN.

TAREA:
Hacer grid search sobre:

HIPERPARÁMETROS A PROBAR:
- Learning rate: [0.0001, 0.001, 0.01]
- Batch size: [32, 64, 128]
- Dropout: [0.2, 0.3, 0.5]
- Filtros primera capa: [16, 32, 64]
- Optimizer: [Adam, SGD, RMSprop]

1. Entrenar modelo para cada combinación
2. Registrar precisión de validación
3. Encontrar mejor combinación
4. Visualizar resultados (heatmap, gráficos)

NOTA: Esto puede tardar mucho, limitar epochs a 5 o usar subconjunto de datos.

CÓDIGO BASE:
"""
)

print(
    """
from itertools import product

def ejercicio_grid_search():
    # Definir hiperparámetros
    learning_rates = [0.0001, 0.001, 0.01]
    batch_sizes = [32, 64, 128]
    dropouts = [0.2, 0.3, 0.5]
    
    resultados = []
    
    # Grid search
    for lr, bs, drop in product(learning_rates, batch_sizes, dropouts):
        print(f"\\nProbando: LR={lr}, BS={bs}, Dropout={drop}")
        
        model = crear_cnn_parametrizada(dropout=drop)
        model.compile(optimizer=Adam(lr=lr), ...)
        
        history = model.fit(x_train, y_train, batch_size=bs, epochs=5)
        
        val_acc = max(history.history['val_accuracy'])
        resultados.append({
            'lr': lr, 'bs': bs, 'dropout': drop,
            'val_acc': val_acc
        })
    
    # Encontrar mejor
    mejor = max(resultados, key=lambda x: x['val_acc'])
    print(f"\\nMejor configuración: {mejor}")

# ejercicio_grid_search()
"""
)

input("\nPresiona Enter para ver resumen...")

# ============================================================================
# RESUMEN Y RECURSOS
# ============================================================================

print(
    """
╔═══════════════════════════════════════════════════════════════════════════╗
║                            RESUMEN DE EJERCICIOS                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

EJERCICIOS BÁSICOS ⭐:
1. K-Means: Experimentar con diferentes valores de K
2. PCA: Reconstrucción con diferentes componentes

EJERCICIOS INTERMEDIOS ⭐⭐:
3. Autoencoder: Robustez ante diferentes ruidos
4. CNN: Impacto del Data Augmentation
6. RL: Diseñar esquemas de recompensas
7. YOLO: Contador de objetos

EJERCICIOS AVANZADOS ⭐⭐⭐:
5. Transfer Learning: Estrategias de fine-tuning
8. Proyecto Integrador: Sistema de vigilancia completo
9. Grid Search: Optimización de hiperparámetros

═══════════════════════════════════════════════════════════════════════════

RECURSOS ADICIONALES:

📚 TUTORIALES:
- TensorFlow: https://www.tensorflow.org/tutorials
- Keras: https://keras.io/examples/
- OpenCV: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

💾 DATASETS:
- Kaggle: https://www.kaggle.com/datasets
- UCI ML Repository: https://archive.ics.uci.edu/ml/
- ImageNet: https://www.image-net.org/

🎓 CURSOS:
- CS231n Stanford: http://cs231n.stanford.edu/
- Fast.ai: https://www.fast.ai/
- DeepLearning.ai: https://www.deeplearning.ai/

🔧 HERRAMIENTAS:
- Google Colab: GPU gratis para experimentos
- Weights & Biases: Tracking de experimentos
- TensorBoard: Visualización de entrenamiento

═══════════════════════════════════════════════════════════════════════════

CONSEJOS PARA PRACTICAR:

1. Empieza con ejercicios básicos y avanza gradualmente
2. Modifica parámetros y observa qué pasa
3. Intenta resolver antes de ver solución
4. Experimenta con tus propias imágenes/datos
5. Documenta tus resultados y aprendizajes
6. Comparte tu código con compañeros

═══════════════════════════════════════════════════════════════════════════

¡Éxito con los ejercicios! 🚀

Para consultas: usar canales oficiales de la materia.
"""
)

print("\n" + "=" * 80)
print(" " * 30 + "FIN DEL MÓDULO 09")
print("=" * 80)
