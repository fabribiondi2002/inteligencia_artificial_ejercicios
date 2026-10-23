# Clase 11 - Clasificación

Modelos de clasificación con scikit-learn: regresión logística (binaria y multiclase), clasificador bayesiano ingenuo y el manejo de problemas con clases desbalanceadas, con las métricas de evaluación correspondientes en cada caso (matriz de confusión, precisión, recall, F1, curva ROC y AUC).

## Notebooks

- [`01_regresion_logistica.ipynb`](01_regresion_logistica.ipynb) — regresión logística sobre el dataset Iris: desde un modelo binario con un solo atributo hasta modelos multiclase, visualizando fronteras de decisión y evaluando con matriz de confusión, precisión, recall, F1 y curva ROC/AUC.
- [`02_clasificador_bayesiano_ingenuo.ipynb`](02_clasificador_bayesiano_ingenuo.ipynb) — clasificador Naive Bayes aplicado a análisis de sentimiento sobre reseñas de películas de IMDb (texto vectorizado con TF-IDF).
- [`03_clasificacion_desbalanceada.ipynb`](03_clasificacion_desbalanceada.ipynb) — regresión logística con `class_weight="balanced"` sobre un problema de incumplimiento de pago fuertemente desbalanceado, incluyendo búsqueda del mejor umbral de decisión.

## Ejercicio

- [`ejercicios/`](ejercicios/) — evaluación práctica: detección de SPAM comparando regresión logística y Naive Bayes. Ver su [README](ejercicios/README.md).

## Fuentes de datos

En [`datasets/`](datasets/):

| Archivo | Contenido | Usado en |
|---|---|---|
| `imbd_tfidf.parquet.gz` | Reseñas de IMDb preprocesadas con TF-IDF (~28.000 atributos, una palabra por columna) y su etiqueta de sentimiento. | `02` |
| `Default.csv` | Incumplimiento de pago de clientes de una tarjeta de crédito (`balance`, `student`, `income`, `default`). | `03` |

## Cómo abrirlas

Con el entorno del repositorio ya configurado (ver [Quick start](../README.md#quick-start)):

```bash
jupyter notebook
```

y elegí el kernel **"Python (IA)"** al abrir cada notebook.
