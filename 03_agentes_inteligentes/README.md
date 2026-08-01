# 03 - Agentes Inteligentes 🤖

## Introducción

En esta unidad aprenderás sobre **agentes inteligentes**, uno de los conceptos fundamentales de la Inteligencia Artificial. Un agente es cualquier entidad que percibe su entorno a través de sensores y actúa sobre ese entorno a través de actuadores.

## Objetivos de Aprendizaje

Al finalizar esta unidad, serás capaz de:

1. **Comprender** qué es un agente inteligente y sus componentes
2. **Diseñar** agentes usando el framework PEAS
3. **Implementar** diferentes arquitecturas de agentes:
   - Agentes reactivos simples
   - Agentes reactivos con modelo interno
   - Agentes basados en objetivos
4. **Evaluar** el desempeño de agentes en diferentes entornos
5. **Analizar** la racionalidad de un agente

## Conceptos Clave

### ¿Qué es un Agente Inteligente?

Un **agente** es cualquier cosa que:

- **Percibe** su entorno a través de sensores
- **Actúa** sobre el entorno a través de actuadores

### Framework PEAS

Para diseñar un agente, debemos especificar:

- **P**erformance (Medida de desempeño): ¿Cómo evaluamos el éxito?
- **E**nvironment (Entorno): ¿Dónde opera el agente?
- **A**ctuators (Actuadores): ¿Qué acciones puede realizar?
- **S**ensors (Sensores): ¿Qué puede percibir?

### Tipos de Entornos

Los entornos se pueden clasificar según:

- **Observable** vs. Parcialmente observable
- **Determinista** vs. Estocástico
- **Episódico** vs. Secuencial
- **Estático** vs. Dinámico
- **Discreto** vs. Continuo
- **Agente único** vs. Multiagente

### Arquitecturas de Agentes

#### 1. Agente Reactivo Simple

- Responde directamente a las percepciones
- Reglas del tipo: "Si [condición] entonces [acción]"
- Simple pero limitado

#### 2. Agente Reactivo con Modelo

- Mantiene un estado interno (modelo del mundo)
- Puede manejar observabilidad parcial
- Más flexible que el reactivo simple

#### 3. Agente Basado en Objetivos

- Tiene información sobre estados deseables (objetivos)
- Planifica acciones para alcanzar objetivos
- Más complejo pero más potente

## Estructura de esta Unidad

```
03_agentes_inteligentes/
│
├── README.md                  ← Este archivo
├── ejemplos/                  ← Ejemplos básicos para aprender
│   ├── 01_agente_simple/     ← Agente reactivo simple (termostato)
│   ├── 02_agente_aspiradora/ ← Aspiradora con reglas
│   └── 03_agente_con_modelo/ ← Agente con estado interno
│
├── ejercicios/               ← Ejercicios progresivos
│   ├── 01_basico/           ← Nivel 1: Fundamentos
│   ├── 02_intermedio/       ← Nivel 2: Con modelo
│   ├── 03_avanzado/         ← Nivel 3: Con objetivos
│   └── 04_desafio/          ← Nivel 4: Proyecto integrador
│
└── recursos/                 ← Material de apoyo
    └── teoria.md            ← Conceptos teóricos ampliados
```

## Requisitos

Para trabajar en esta unidad necesitas:

- Python 3.8+
- NumPy
- Matplotlib (para visualizaciones)

Asegúrate de tener el entorno virtual activado y las dependencias instaladas (ver `00_introduccion`).

## Comenzando

### Ruta de Aprendizaje Recomendada

1. **Ejemplos** (2-3 horas)
   - Comienza con `ejemplos/01_agente_simple/` para entender la estructura básica
   - Revisa `ejemplos/02_agente_aspiradora/` para ver reglas en acción
   - Estudia `ejemplos/03_agente_con_modelo/` para comprender el estado interno

2. **Ejercicios Básicos** (3-4 horas)
   - Implementa tu primer agente en `ejercicios/01_basico/`
   - Completa todos los ejercicios del nivel básico

3. **Ejercicios Intermedios** (4-5 horas)
   - Avanza a `ejercicios/02_intermedio/`
   - Implementa agentes con modelo interno

4. **Ejercicios Avanzados** (5-6 horas)
   - Trabaja en `ejercicios/03_avanzado/`
   - Implementa agentes basados en objetivos

5. **Desafío Final** (8-10 horas)
   - Proyecto integrador en `ejercicios/04_desafio/`

Cada ejercicio incluye:

- **README.md**: Enunciado y conceptos
- **template.py**: Código base para comenzar
- **test_*.py**: Tests automáticos
- **solucion_ref.py**: Solución de referencia (consultar después)

## Recursos Adicionales

### Bibliografía

- **Russell & Norvig** - *Artificial Intelligence: A Modern Approach* (Capítulo 2)
- **Wooldridge** - *An Introduction to MultiAgent Systems*

### Videos y Tutoriales

- [Conceptos básicos de agentes inteligentes](https://www.youtube.com/watch?v=Xh1Jv33RIKw)
- [Arquitecturas de agentes](https://www.youtube.com/watch?v=EEpGPj2yZ7E)

### Recursos Online

- [AI: A Modern Approach - Online Resources](http://aima.cs.berkeley.edu/)

## Tips para el Éxito

1. **Experimenta**: No tengas miedo de probar diferentes enfoques
2. **Documenta**: Comenta tu código para entender tu razonamiento
3. **Compara**: Analiza las diferencias entre tipos de agentes
4. **Pregunta**: Si algo no queda claro, consulta con el profesor

## Evaluación

Los ejercicios de esta unidad se evaluarán según:

- **Funcionamiento** (40%): ¿El código funciona correctamente?
- **Implementación** (30%): ¿Está bien estructurado?
- **Comprensión** (20%): ¿Demuestra entendimiento de conceptos?
- **Documentación** (10%): ¿Está bien documentado?

## Próximos Pasos

1. Lee y comprende los conceptos en este README
2. Espera las instrucciones del profesor sobre los ejercicios
3. Revisa ejemplos de código cuando estén disponibles
4. Comienza con ejercicios simples antes de avanzar a los complejos

---
