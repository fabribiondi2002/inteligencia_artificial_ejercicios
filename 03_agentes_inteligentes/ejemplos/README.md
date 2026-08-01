# Ejemplos de Agentes Inteligentes

Esta carpeta contiene ejemplos didácticos para comprender los conceptos fundamentales de agentes inteligentes, desde los más simples hasta agentes con Machine Learning.

## Contenido

### 01 - Agente Simple (Termostato)

**Concepto**: Agente reactivo simple
**Dificultad**: ⭐☆☆☆☆
**Tiempo**: 30 minutos

Un termostato que mantiene la temperatura. Ejemplo perfecto de agente reactivo simple con reglas directas condición-acción.

**Aprenderás**: Arquitectura básica, percepciones, acciones, reglas simples

### 02 - Agente Aspiradora (2 habitaciones)

**Concepto**: Agente reactivo simple con múltiples reglas
**Dificultad**: ⭐⭐☆☆☆
**Tiempo**: 45 minutos

Aspiradora robótica que limpia dos habitaciones. Introduce percepciones compuestas, múltiples acciones y limitaciones de agentes reactivos.

**Aprenderás**: Percepciones compuestas, múltiples acciones, análisis PEAS, limitaciones del agente reactivo simple

### 03 - Agente con Modelo del Mundo

**Concepto**: Agente basado en modelo con estado interno
**Dificultad**: ⭐⭐⭐☆☆
**Tiempo**: 1 hora

Aspiradora inteligente que mantiene un modelo interno del mundo. Supera las limitaciones del agente reactivo mediante memoria y razonamiento sobre estados.

**Aprenderás**: Estado interno, modelo del mundo, actualización de creencias, planificación básica, detección de terminación

### 04 - Agente con Aprendizaje (Q-Learning)

**Concepto**: Agente con Machine Learning (Reinforcement Learning)
**Dificultad**: ⭐⭐⭐⭐☆
**Tiempo**: 2 horas

Aspiradora en grid complejo que **aprende automáticamente** la política óptima mediante Q-Learning. Resuelve problemas donde escribir reglas manualmente es imposible.

**Aprenderás**: Q-Learning, exploración vs. explotación, sistema de recompensas, entrenamiento de agentes, visualización del aprendizaje

### 05 - Deep Reinforcement Learning (Stable-Baselines3)

**Concepto**: Deep RL con librerías profesionales
**Dificultad**: ⭐⭐⭐⭐⭐
**Tiempo**: 1-2 horas

Mismo problema del Ejemplo 04 pero usando **Stable-Baselines3**, la librería estándar de la industria. **10x menos código** (~20 líneas vs. 500), con redes neuronales automáticas y algoritmos de última generación (DQN, PPO, A2C).

**Aprenderás**: Stable-Baselines3, Deep Q-Networks, arquitecturas de RL profesionales, TensorBoard, Gym/Gymnasium API

## Progresión de Conceptos

```
01. Termostato
    ↓ (más percepciones)
02. Aspiradora 2 hab.
    ↓ (+ estado interno)
03. Con Modelo
    ↓ (+ Machine Learning básico)
04. Q-Learning Manual
    ↓ (+ Deep Learning + Librerías Pro)
05. Stable-Baselines3
```

## Comparación de Arquitecturas

| Ejemplo | Tipo | Memoria | Aprende | Complejidad Entorno |
|---------|------|---------|---------|---------------------|
| 01. Termostato | Reactivo Simple | ❌ | ❌ | Muy simple |
| 02. Aspiradora | Reactivo Simple | ❌ | ❌ | Simple |
| 03. Con Modelo | Basado en Modelo | ✅ | ❌ | Media |
| 04. Q-Learning | Con Aprendizaje | ✅ | ✅ | Alta |
| 05. Deep RL (SB3) | Deep Learning | ✅ | ✅ | Muy Alta |

## Cómo Usar los Ejemplos

1. **Lee el README de cada ejemplo** para entender el concepto teórico
2. **Ejecuta el código** y observa el comportamiento del agente
3. **Modifica parámetros** para experimentar y ver cómo cambia
4. **Compara arquitecturas** entre ejemplos consecutivos
5. **Responde las preguntas** de reflexión en cada README

## Orden Recomendado

### Ruta Básica (sin ML)

1. **01_agente_simple** - Entender agentes reactivos
2. **02_agente_aspiradora** - Percepciones y acciones múltiples
3. **03_agente_con_modelo** - Estado interno y modelo del mundo

### Ruta Completa (con ML)

1. **01_agente_simple** - Fundamentos
2. **02_agente_aspiradora** - Limitaciones de agentes reactivos
3. **03_agente_con_modelo** - Superar limitaciones con modelo
4. **04_agente_con_aprendizaje** - Aprendizaje automático (Q-Learning)

Cada ejemplo construye sobre los conceptos del anterior.

## Requisitos

### Para ejemplos 01-03

```bash
# Solo Python 3.10+, no requiere dependencias externas
python ejemplo.py
```

### Para ejemplo 04 (Q-Learning)

```bash
# Requiere numpy y matplotlib
cd 04_agente_con_aprendizaje
pip install -r requirements.txt
python agente_qlearning.py
```

## Conceptos Clave por Ejemplo

### Ejemplo 01

- ✅ Arquitectura agente-entorno
- ✅ Percepción → Acción
- ✅ Reglas condición-acción

### Ejemplo 02

- ✅ Percepciones compuestas
- ✅ Análisis PEAS
- ✅ Tabla de comportamiento
- ✅ Limitaciones de agentes reactivos

### Ejemplo 03

- ✅ Estado interno (memoria)
- ✅ Modelo del mundo
- ✅ Actualización de creencias
- ✅ Planificación simple

### Ejemplo 04

- ✅ Machine Learning (Q-Learning)
- ✅ Exploración vs. Explotación
- ✅ Sistema de recompensas
- ✅ Entrenamiento iterativo
- ✅ Visualización del aprendizaje
