# Clase 2 - Análisis exploratorio de datos (EDA)

## Notebooks

- [`01_carga_y_exploracion_datos.ipynb`](01_carga_y_exploracion_datos.ipynb) — distintas formas de recolectar datos (CSV, API, base de datos, web scraping) y una primera exploración con Pandas: datos faltantes, duplicados, tipos de datos y visualizaciones básicas.
- [`02_correlacion.ipynb`](02_correlacion.ipynb) — qué mide (y qué no) la correlación: comparación de Pearson, Spearman y Kendall sobre relaciones lineales, monótonas y no monótonas, con datos sintéticos.
- [`03_eda_titanic.ipynb`](03_eda_titanic.ipynb) — EDA completo sobre el dataset Titanic: estadística descriptiva (tendencia central, dispersión, forma), exploración de variables categóricas, y relaciones entre variables (correlación, tablas de contingencia, pairplot, violin/box/strip/swarm plots).

## Fuentes de datos

La notebook de carga combina datos remotos (para mostrar distintas formas de recolección) y varios archivos locales en [`../datasets/`](../datasets/). La notebook de correlación no usa datasets: trabaja con datos sintéticos generados en la propia notebook. La notebook de EDA usa el dataset Titanic incluido en seaborn (`sns.load_dataset('titanic')`): no requiere ningún archivo local, pero sí conexión a internet la primera vez que se corre (seaborn lo descarga y lo cachea en `~/seaborn-data`).

| Fuente | Origen | Uso en la notebook |
|---|---|---|
| `airtravel.csv` | Descargado en vivo desde `people.sc.fsu.edu` (dataset público de ejemplo de la Florida State University: pasajeros aéreos mensuales 1958-1960). | Ejemplo de carga de un CSV remoto con `pd.read_csv`. |
| API del SMN | `ws.smn.gob.ar`, la API pública del Servicio Meteorológico Nacional argentino. Si no responde `200` (pasa, es una API pública que a veces está caída), la notebook cae automáticamente a `jsonplaceholder.typicode.com/users` como respaldo — misma forma de datos (lista de objetos con un campo anidado). | Ejemplo de consumo de una API REST (pronóstico del clima por localidad). |
| `books.toscrape.com` | Sitio público pensado específicamente para practicar web scraping (no es una librería real). | Ejemplo de scraping con `requests` + `BeautifulSoup` (título, precio y rating de libros). |
| `../datasets/movie.sqlite` | Extracto tipo "IMDB 5000 movies", un dataset clásico usado en tutoriales de análisis de datos. Base SQLite con 3 tablas: `IMDB` (117 películas: rating, votos, presupuesto, duración), `earning` (recaudación doméstica/mundial) y `genre` (géneros por película). | Ejemplo de conexión a una base de datos con SQLAlchemy y consultas SQL con `pandas.read_sql`. |
| `../datasets/turismo.csv` | Estadística oficial de turismo receptivo y emisivo de Argentina (INDEC / Ministerio de Turismo), serie mensual desde 2010 (columnas `indice_tiempo`, `turismo_receptivo`, `turismo_emisivo`, `saldo`). | Base para la parte de exploración: nulos, duplicados, tipos de datos, columnas derivadas y visualización con matplotlib/seaborn. |
| `../datasets/datos.csv` | Dataset *Adult / Census Income* (UCI Machine Learning Repository): 32.561 registros censales de EE.UU. (edad, nivel educativo, ocupación, horas trabajadas, ingresos, etc.), usado clásicamente para practicar clasificación. | Usado en el [ejercicio](ejercicios/) de la clase, no en la notebook principal. |

## Ejercicios

- [`ejercicios/`](ejercicios/) — para resolver por tu cuenta: primera inspección de un dataset nuevo, sin ejemplos resueltos.

## Cómo abrirlas

Con el entorno del repositorio ya configurado (ver [Quick start](../README.md#quick-start)):

```bash
jupyter notebook
```

y elegí el kernel **"Python (IA)"** al abrir cada notebook.
