# Clase 2 - Carga y exploración de datos

## Notebook

- [`01_carga_y_exploracion_datos.ipynb`](01_carga_y_exploracion_datos.ipynb) — distintas formas de recolectar datos (CSV, API, base de datos, web scraping) y una primera exploración con Pandas: datos faltantes, duplicados, tipos de datos y visualizaciones básicas.

## Fuentes de datos

La notebook combina datos remotos (para mostrar distintas formas de recolección) y dos archivos locales en [`../datasets/`](../datasets/):

| Fuente | Origen | Uso en la notebook |
|---|---|---|
| `airtravel.csv` | Descargado en vivo desde `people.sc.fsu.edu` (dataset público de ejemplo de la Florida State University: pasajeros aéreos mensuales 1958-1960). | Ejemplo de carga de un CSV remoto con `pd.read_csv`. |
| API del SMN | `ws.smn.gob.ar`, la API pública del Servicio Meteorológico Nacional argentino. | Ejemplo de consumo de una API REST (pronóstico del clima por localidad). |
| `books.toscrape.com` | Sitio público pensado específicamente para practicar web scraping (no es una librería real). | Ejemplo de scraping con `requests` + `BeautifulSoup` (título, precio y rating de libros). |
| `../datasets/movie.sqlite` | Extracto tipo "IMDB 5000 movies", un dataset clásico usado en tutoriales de análisis de datos. Base SQLite con 3 tablas: `IMDB` (117 películas: rating, votos, presupuesto, duración), `earning` (recaudación doméstica/mundial) y `genre` (géneros por película). | Ejemplo de conexión a una base de datos con SQLAlchemy y consultas SQL con `pandas.read_sql`. |
| `../datasets/turismo.csv` | Estadística oficial de turismo receptivo y emisivo de Argentina (INDEC / Ministerio de Turismo), serie mensual desde 2010 (columnas `indice_tiempo`, `turismo_receptivo`, `turismo_emisivo`, `saldo`). | Base para la parte de exploración: nulos, duplicados, tipos de datos, columnas derivadas y visualización con matplotlib/seaborn. |

## Cómo abrirla

Con el entorno del repositorio ya configurado (ver [Quick start](../README.md#quick-start)):

```bash
jupyter notebook
```

y elegí el kernel **"Python (IA)"** al abrir la notebook.
