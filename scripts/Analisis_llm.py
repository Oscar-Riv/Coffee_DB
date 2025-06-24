import openai
from openai import OpenAI
import pandas as pd
import os

# Configura tu clave de API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cargar dataframes desde archivos CSV
df_forecast_paises_top = pd.read_csv("forecast_paises_top.csv")
df_forecast_variedad = pd.read_csv("forecast_variedad_cafe.csv")
df_tendencias_pais = pd.read_csv("tendencias_pais.csv")
df_tendencias_tipo = pd.read_csv("tendencias_tipo.csv")
df_resumen_consumo = pd.read_csv("resumen_consumo_cafe.csv")
df_ciclo = pd.read_csv("clasificacion_ciclo_consumo.csv")
df_cluster = pd.read_csv("clustering_resultados.csv")

# Diccionario de análisis
analisis_dict = {
    'resumen_consumo_cafe': (df_resumen_consumo, """Este es un resumen estadístico del consumo de café por país y tipo.

Redacta un informe profesional que incluya:
- países con mayor y menor consumo total,
- medidas de tendencia central destacadas,
- diferencias por tipo de café,
- observaciones sobre varianza y dispersión.
"""),

    'tendencias_pais': (df_tendencias_pais, """Este es un análisis de tendencias de consumo por país.

Resume:
- países con mayor crecimiento o caída,
- patrones regionales,
- implicaciones comerciales.
"""),

    'tendencias_tipo': (df_tendencias_tipo, """Este es un análisis de tendencias por tipo de café.

Describe:
- cuál crece más,
- cuál es más estable,
- posibles causas y recomendaciones.
"""),

    'clasificacion_ciclo_consumo': (df_ciclo, """Esta es la clasificación de países según su ciclo de consumo (crecimiento, madurez, declive, volatilidad).

Redacta un análisis ejecutivo que indique:
- cuántos países hay por categoría,
- ejemplos relevantes,
- acciones sugeridas por grupo.
"""),

    'forecast_paises_top': (df_forecast_paises_top, """Este es un pronóstico ARIMA de consumo para los principales países.

Redacta un resumen que destaque:
- países con crecimiento proyectado,
- estancamientos o caídas,
- oportunidades y riesgos futuros.
"""),

    'forecast_variedad_cafe': (df_forecast_variedad, """Este es un pronóstico ARIMA por tipo de café.

Redacta un informe que indique:
- cuál variedad crecerá más,
- cuál se estabiliza,
- decisiones estratégicas a considerar.
"""),

    'clustering_resultados': (df_cluster, """Este es un resultado de clustering de países por patrón de consumo.

Explica:
- características de cada clúster,
- ejemplos por grupo,
- estrategias posibles para cada segmento.
""")
}

def generar_resumen(nombre, df, instrucciones, max_filas=15):
    prompt = f"""Datos para el análisis ({nombre}):

{df.head(max_filas).to_markdown(index=False)}

{instrucciones}
"""
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "user", "content": prompt}]
)

    resumen = response.choices[0].message.content  
    
    # Guardar resumen en archivo
    with open(f"{nombre}_resumen.txt", "w", encoding="utf-8") as f:
        f.write(resumen)

    print(f"Resumen generado para '{nombre}' y guardado en {nombre}_resumen.txt\n")

for nombre, (df, instrucciones) in analisis_dict.items():
    generar_resumen(nombre, df, instrucciones)
