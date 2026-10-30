# Evaluación práctica - Detector de SPAM

## Descripción del problema

En este ejercicio deben implementar dos modelos de **clasificación** para resolver un problema supervisado utilizando el conjunto de datos **Spambase**.

El dataset Spambase contiene 4601 observaciones de correos electrónicos, de los cuales 2788 son legítimos y 1813 son SPAM. Los correos ya fueron preprocesados mediante técnicas de NLP: cada atributo representa la frecuencia normalizada de una palabra o símbolo en el mensaje.

El objetivo es construir modelos capaces de predecir si un correo es SPAM (`spam = 1`) o legítimo (`spam = 0`) a partir de esas frecuencias de palabras.

## Instrucciones de entrega

- [`01_ejercicio_deteccion_spam.ipynb`](01_ejercicio_deteccion_spam.ipynb) — notebook a completar. Es **obligatorio** completar únicamente las secciones indicadas (marcadas con `##### COMPLETAR AQUI LO PEDIDO`), sin agregar contenido adicional.
- [`spambase.csv`](spambase.csv) — el dataset.

La notebook ya trae la carga de datos y el split train/test. Hay que completar dos partes:

1. **Armado de modelos**: un `Pipeline` con estandarización + regresión logística, y un clasificador de Bayes ingenuo (eligiendo la implementación de scikit-learn más apropiada para este tipo de datos).
2. **Evaluación**: para cada modelo, calcular matriz de confusión, precisión, recall y AUC, y responder las preguntas finales sobre cuál conviene según cada métrica.

## Cómo resolverla

Con el entorno del repositorio ya configurado (ver [Quick start](../../README.md#quick-start)):

```bash
jupyter notebook
```

y elegí el kernel **"Python (IA)"** al abrir la notebook. Podés usar como referencia [`../01_regresion_logistica.ipynb`](../01_regresion_logistica.ipynb) y [`../02_clasificador_bayesiano_ingenuo.ipynb`](../02_clasificador_bayesiano_ingenuo.ipynb), donde se aplican ambos modelos.
