# Coffee_DB

Este repositorio contiene la metodología y los resultados obtenidos a partir del análisis de 30 años de consumo de café por país. El objetivo del proyecto fue extraer patrones de comportamiento, prever tendencias y proponer herramientas analíticas que faciliten la toma de decisiones comerciales para empresas exportadoras.

## 🔍 Metodología

A continuación se describen los pasos principales realizados en el análisis:

1. **Transformación de datos**  
   Conversión de la base original desde formato ancho a formato largo, limpieza de columnas de años, tipos y consumos, y estandarización para análisis posterior.

2. **Análisis exploratorio de datos (EDA)**  
   - Estadísticas descriptivas por país y tipo de café.  
   - Gráficas de consumo total y evolución anual.  
   - Visualizaciones agregadas por continente y tipo de variedad.

3. **Análisis de tendencias temporales**  
   - Evaluación de crecimiento o decrecimiento por tipo de café.  
   - Identificación de los países con mayores tendencias positivas y volúmenes más altos de consumo.

4. **Clasificación por ciclo de consumo y concentración de mercado**  
   - Agrupación de países según su etapa: crecimiento, madurez, declive o volatilidad.  
   - Cálculo de índices de concentración como Gini y HHI para evaluar la distribución del mercado.

5. **Pronósticos con modelos ARIMA**  
   - Proyección de consumo para los próximos 5 años en los países más relevantes.  
   - Modelos independientes para variedades de café y para países de alto consumo y crecimiento.

6. **Clusterización de países (K-Means)**  
   - Agrupamiento basado en patrones de consumo multianuales.  
   - Visualización en espacio reducido (PCA) para interpretar grupos similares y detectar oportunidades estratégicas.

7. **Exploración de estrategias basadas en IA generativa (LLMs)**  
   - Revisión de cómo herramientas como ChatGPT y modelos de lenguaje pueden integrarse para generar reportes automáticos, explicar resultados o responder consultas analíticas directamente sobre los datos procesados.

---

## 📂 Contenido

- `/data/`: datos procesados y exportaciones parciales
- `/scripts/`: Scripts de python con cada paso del análisis
- `/outputs/`: visualizaciones, tablas resumen y archivos de pronóstico

---
## 🧾 Paso 1: Transformación de los datos

La base de datos original contenía el consumo de café en formato ancho, con columnas por año (por ejemplo `'1990/91'`, `'1991/92'`, etc.). Para facilitar el análisis temporal, se aplicó una transformación a formato largo usando `pandas.melt()`.

El resultado fue un nuevo conjunto de datos con las columnas:

- `Country`: país de origen
- `Coffee type`: variedad de café (una por país)
- `Year`: año de consumo (extraído del formato `'1990/91'` como `1990`)
- `Consumption`: consumo total registrado ese año

Este archivo transformado fue guardado como [`coffee_db.csv`](./data/coffee_db.csv) en la carpeta `/data/`, y se utilizó como base para los análisis posteriores.

Vista previa de las primeras filas del archivo:
| Country                          | Coffee type     |   Total_domestic_consumption |   Year |   Consumption |
|:---------------------------------|:----------------|-----------------------------:|-------:|--------------:|
| Angola                           | Robusta/Arabica |                     46500000 |   1990 |       1200000 |
| Bolivia (Plurinational State of) | Arabica         |                     75180000 |   1990 |       1500000 |
| Brazil                           | Arabica/Robusta |                  27824700000 |   1990 |     492000000 |
| Burundi                          | Arabica/Robusta |                      3412020 |   1990 |        120000 |
| Ecuador                          | Arabica/Robusta |                    381540000 |   1990 |      21000000 |
