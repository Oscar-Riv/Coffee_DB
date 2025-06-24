# Coffee_DB

Este repositorio contiene la metodología y los resultados obtenidos a partir del análisis de 30 años de consumo de café por país. El objetivo del proyecto fue extraer patrones de comportamiento, prever tendencias y proponer herramientas analíticas que faciliten la toma de decisiones comerciales para empresas exportadoras.

## 🔍 Metodología

A continuación se describen los pasos principales realizados en el análisis:

1. **Transformación de datos**  
   Conversión de la base original desde formato ancho a formato largo.

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

## 📊 Paso 2: Análisis Exploratorio de Datos

Una vez transformada la base, se realizaron diversos análisis exploratorios para comprender mejor el comportamiento del consumo de café por país, tipo y región.

---

### 🔹 Evolución del consumo total por país

Se generó una gráfica de líneas con escala logarítmica para representar la evolución anual del consumo por país, diferenciando la variedad de café. Dado que las magnitudes de consumo entre países varían mucho, la escala logarítmica ayuda a visualizar mejor las trayectorias.

📎 Archivo generado: [`Prod_cafe.png`](./outputs/Prod_cafe.png)

---

### 🔹 Estadísticas descriptivas por país y tipo

Se creó una tabla resumen con los principales estadísticos de consumo por país y tipo de café. Entre las métricas incluidas están:

- Consumo total
- Años con datos válidos
- Media, mediana, percentiles 25 y 75
- Varianza y desviación estándar
- Años de máximo y mínimo consumo

📎 Archivo generado: [`resumen_consumo_cafe.csv`](./outputs/resumen_consumo_cafe.csv)

Ejemplo de las primeras filas:

| Country                          | Coffee type     |   Total_Consumption |   Valid_Years_Count |             Mean |           Median |              P25 |              P75 |    Variance |          Std_Dev |   Year_Max_Consumption |   Year_Min_Consumption |
|:---------------------------------|:----------------|--------------------:|--------------------:|-----------------:|-----------------:|-----------------:|-----------------:|------------:|-----------------:|-----------------------:|-----------------------:|
| Angola                           | Robusta/Arabica |            46500000 |                  30 |      1.55e+06    |      1.8e+06     |      1.2e+06     |      1.8e+06     | 1.7431e+11  | 417505           |                   1997 |                   1995 |
| Bolivia (Plurinational State of) | Arabica         |            75180000 |                  30 |      2.506e+06   |      2.49e+06    |      1.9575e+06  |      3.0075e+06  | 4.24908e+11 | 651849           |                   2019 |                   1990 |
| Brazil                           | Arabica/Robusta |         27824700000 |                  30 |      9.2749e+08  |      9.1452e+08  |      7.005e+08   |      1.19962e+09 | 7.76548e+16 |      2.78666e+08 |                   2018 |                   1990 |
| Burundi                          | Arabica/Robusta |             3412020 |                  30 | 113734           | 120000           | 115950         
  | 120000           | 1.52345e+08 |  12342.8         |                   1990 |                   2007 |
| Cameroon                         | Robusta/Arabica |           143450940 |                  30 |      4.7817e+06  |      4.53951e+06 |      4.14e+06    |      4.99998e+06 | 5.40601e+11 | 735256           |                   1993 |                   2010 |
| Central African Republic         | Robusta         |            24794400 |                  30 | 826480           | 849990           | 245415         
  |      1.2e+06     | 2.66468e+11 | 516205           |                   1990 |                   2000 |
| Colombia                         | Arabica         |          2536776384 |                  30 |      8.45592e+07 |      7.86907e+07 |      7.62222e+07 |      8.96669e+07 | 1.70044e+14 |      1.30401e+07 |                   2019 |                   2006 |
| Congo                            | Robusta         |             5360040 |                  30 | 178668           | 180000           | 180000         
  | 180000           | 2.56957e+07 |   5069.09        |                   1990 |                   1991 |
| Costa Rica                       | Arabica         |           665335200 |                  30 |      2.21778e+07 |      2.25e+07    |      2.25e+07    |      2.25e+07    | 3.79619e+12 |      1.94838e+06 |                   2015 |                   2008 |
| Cuba                             | Arabica         |           384006000 |                  30 |      1.28002e+07 |      1.32e+07    |      1.2195e+07  |      1.32e+07    | 4.91687e+11 | 701204           |                   2002 |                   1996 |
| Côte d'Ivoire                    | Robusta         |           410260140 |                  30 |      1.36753e+07 |      1.9e+07     |      3e+06       |      1.902e+07   | 5.89464e+13 |      7.67765e+06 |                   2007 |                   1990 |
| Democratic Republic of Congo     | Robusta/Arabica |           359880000 |                  30 |      1.1996e+07  |      1.2e+07     |      1.2e+07     |      1.2e+07     | 4.8e+08     |  21908.9         |                   1990 |                   2019 |
| Dominican Republic               | Arabica/Robusta |           642823380 |                  30 |      2.14274e+07 |      2.26499e+07 |      1.95e+07    |      2.268e+07   | 2.79041e+12 |      1.67045e+06 |                   2016 |                   1990 |
| Ecuador                          | Arabica/Robusta |           381540000 |                  30 |      1.2718e+07  |      9.3e+06     |      9e+06       |      1.8e+07     | 2.53061e+13 |      5.03052e+06 |                   1990 |                   2019 |
| El Salvador                      | Arabica         |           417242040 |                  30 |      1.39081e+07 |      1.4229e+07  |      1.0975e+07  |      1.6545e+07  | 9.63029e+12 |      3.10327e+06 |                   2017 |                   2000 |
| Ethiopia                         | Arabica         |          4536540000 |                  30 |      1.51218e+08 |      1.5261e+08  |      1.0482e+08  |      1.9698e+08  | 2.60695e+15 |      5.10583e+07 |                   2019 |                   1990 |
| Gabon                            | Robusta         |             1123140 |                  30 |  37438           |  30510           |  18000         
  |  48000           | 4.00631e+08 |  20015.8         |                   1990 |                   2009 |
| Ghana                            | Robusta         |             9970800 |                  30 | 332360           | 120000           |  95400         
  | 165000           | 2.34066e+11 | 483803           |                   1994 |                   1998 |
| Guatemala                        | Arabica/Robusta |           590880000 |                  30 |      1.9696e+07  |      1.83e+07    |      1.8e+07     |      2.145e+07   | 4.94738e+12 |      2.22427e+06 |                   2017 |                   1990 |
| Guinea                           | Robusta         |            86730000 |                  30 |      2.891e+06   |      3e+06       |      3e+06       |      3e+06       | 1.98154e+11 | 445145           |                   1992 |                   1990 |
| Guyana                           | Robusta         |             9203040 |                  22 | 418320           | 501000           | 301515         
  | 532500           | 1.74734e+10 | 132187           |                   2015 |                   2000 |
| Haiti                            | Arabica         |           600600000 |                  30 |      2.002e+07   |      2.04e+07    |      1.98e+07    |      2.04e+07    | 1.74372e+12 |      1.3205e+06  |                   2018 |                   1990 |
| Honduras                         | Arabica         |           471850680 |                  30 |      1.57284e+07 |      1.455e+07   |      1.2e+07     |      2.0625e+07  | 2.09461e+13 |      4.57669e+06 |                   2017 |                   1998 |
| India                            | Robusta/Arabica |          2093460000 |                  30 |      6.9782e+07  |      7.32e+07    |      5.5005e+07  |      8.2125e+07  | 2.0416e+14  |      1.42885e+07 |                   2018 |                   1993 |
| Indonesia                        | Robusta/Arabica |          4920480000 |                  30 |      1.64016e+08 |      1.35e+08    |      9.261e+07   |      2.30505e+08 | 6.15991e+15 |      7.84851e+07 |                   2019 |                   1990 |
| Jamaica                          | Arabica         |            18688020 |                  30 | 622934           | 540000           | 540000         
  | 645000           | 3.5018e+10  | 187131           |                   1997 |                   1992 |
| Kenya                            | Arabica         |            95190000 |                  30 |      3.173e+06   |      3e+06       |      3e+06       |      3e+06       | 1.35042e+11 | 367481           |                   2019 |                   1990 |
| Lao People's Democratic Republic | Robusta         |           157980000 |                  18 |      8.77667e+06 |      9e+06       |      8.55e+06    |      9e+06       | 5.60671e+11 | 748779           |                   2002 |                   2003 |
| Liberia                          | Robusta         |             8640000 |                  30 | 288000           | 300000           | 300000         
  | 300000           | 1.34069e+09 |  36615.4         |                   1993 |                   1990 |
| Madagascar                       | Robusta         |           588705960 |                  30 |      1.96235e+07 |      2.175e+07   |      1.077e+07   |      2.67e+07    | 6.15157e+13 |      7.8432e+06  |                   2004 |                   1999 |
| Malawi                           | Arabica         |             2340000 |                  30 |  78000           |  60000           |  60000         
  | 120000           | 7.82069e+08 |  27965.5         |                   1990 |                   1999 |
| Mexico                           | Arabica/Robusta |          3189660000 |                  30 |      1.06322e+08 |      9.675e+07   |      7.5075e+07  |      1.4055e+08  | 1.02575e+15 |      3.20273e+07 |                   2018 |                   1994 |
| Nicaragua                        | Arabica         |           299700300 |                  30 |      9.99001e+06 |      1.11299e+07 |      7.647e+06   |      1.24328e+07 | 9.36227e+12 |      3.05978e+06 |                   2018 |                   1990 |
| Nigeria                          | Robusta         |            70740000 |                  30 |      2.358e+06   |      2.4e+06     |      2.4e+06     |      2.4e+06     | 2.20562e+10 | 148513           |                   1993 |                   1990 |
| Panama                           | Arabica         |           122916960 |                  30 |      4.09723e+06 |      4.02e+06    |      4.02e+06    |      4.02e+06    | 5.36294e+10 | 231580           |                   1997 |                   1990 |
| Papua New Guinea                 | Arabica/Robusta |             3608400 |                  30 | 120280           | 120000           | 120000         
  | 120000           | 6.25501e+08 |  25010           |                   1990 |                   1998 |
| Paraguay                         | Arabica         |            35100000 |                  30 |      1.17e+06    |      1.2e+06     |      1.2e+06     |      1.2e+06     | 8.37931e+09 |  91538.6         |                   1993 |                   1990 |
| Peru                             | Arabica         |           402000000 |                  30 |      1.34e+07    |      1.32e+07    |      1.2e+07     |      1.5e+07     | 2.01931e+12 |      1.42102e+06 |                   2008 |                   1990 |
| Philippines                      | Robusta/Arabica |          2807280000 |                  30 |      9.3576e+07  |      6.18e+07    |      4.9215e+07  |      1.3725e+08  | 3.18016e+15 |      5.6393e+07  |                   2018 |                   1990 |
| Rwanda                           | Arabica         |             2139960 |                  30 |  71332           |  60000           |  60000         
  |  60000           | 1.34313e+09 |  36648.7         |                   1997 |                   2002 |
| Sierra Leone                     | Robusta         |            10080000 |                  30 | 336000           | 300000           | 300000         
  | 300000           | 6.85241e+09 |  82779.3         |                   1990 |                   1993 |
| Sri Lanka                        | Robusta/Arabica |            58300020 |                  30 |      1.94333e+06 |      1.8e+06     |      1.8e+06     |      2.1e+06     | 4.09191e+11 | 639681           |                   1991 |                   1993 |
| Tanzania                         | Arabica/Robusta |            76425060 |                  30 |      2.5475e+06  |      2.52e+06    |      1.002e+06   |      4.11075e+06 | 3.32555e+12 |      1.82361e+06 |                   2019 |                   1991 |
| Thailand                         | Robusta/Arabica |          1248600000 |                  30 |      4.162e+07   |      3e+07       |      2.526e+07   |      6.735e+07   | 6.17329e+14 |      2.48461e+07 |                   2018 |                   1990 |
| Timor-Leste                      | Arabica         |              294000 |                  10 |  29400           |  29400           |  29400         
  |  29400           | 0           |      0           |                   2010 |                   2010 |
| Togo                             | Robusta         |             2167620 |                  30 |  72254           |  60000           |  15330         
  | 120000           | 2.11054e+09 |  45940.6         |                   1998 |                   2014 |
| Trinidad & Tobago                | Robusta         |            21090000 |                  30 | 703000           | 660000           | 600000         
  | 840000           | 1.41321e+10 | 118878           |                   1994 |                   1990 |
| Uganda                           | Robusta/Arabica |           284816400 |                  30 |      9.49388e+06 |      8.76e+06    |      6.29355e+06 |      1.287e+07   | 1.39688e+13 |      3.73749e+06 |                   2019 |                   1990 |
| Venezuela                        | Arabica         |          2386067999 |                  30 |      7.95356e+07 |      8.21421e+07 |      6.34e+07    |      9.89889e+07 | 3.44195e+14 |      1.85525e+07 |                   2009 |                   1990 |
| Viet Nam                         | Robusta/Arabica |          1920928320 |                  30 |      6.40309e+07 |      4.48907e+07 |      1.91054e+07 |      1.06875e+08 | 2.66315e+15 |      5.16057e+07 |                   2019 |                   1990 |
| Yemen                            | Arabica         |           121620000 |                  17 |      7.15412e+06 |      7.8e+06     |      6.9e+06     |      7.8e+06     | 2.20074e+12 |      1.48349e+06 |                   2003 |                   2019 |
| Zambia                           | Arabica         |              991920 |                  19 |  52206.3         |  36000           |  36000         
  |  60000           | 4.75209e+08 |  21799.3         |                   1990 |                   1995 |
| Zimbabwe                         | Arabica         |             8595960 |                  30 | 286532           | 240000           | 240000         
  | 240000           | 9.21925e+09 |  96017           |                   1993 |                   1996 |

---

### 🔹 Consumo por continente

Se agregaron los datos por región geográfica (continente) mediante un mapeo manual de países, y se generaron las siguientes visualizaciones:

- **Gráfico de barras** con el consumo total acumulado por continente:  
  📎 [`Consumo_Total_Continente.png`](./outputs/Consumo_Total_Continente.png)

- **Gráfico de líneas** con la evolución temporal del consumo por continente, incluyendo en la leyenda los países involucrados:  
  📎 [`Consumo_Anual_Continente.png`](./outputs/Consumo_Anual_Continente.png)

---

### 🔹 Consumo por tipo de café

También se analizaron los patrones por variedad de café (Arabica, Robusta, etc.):

- **Gráfico de barras** con el consumo total por tipo:  
  📎 [`Consumo_Total_Tipo.png`](./outputs/Consumo_Total_Tipo.png)

- **Gráfico de líneas** con la evolución anual del consumo por tipo:  
  📎 [`Evolucion_Consumo_Tipo.png`](./outputs/Evolucion_Consumo_Tipo.png)

