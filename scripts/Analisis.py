import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings

warnings.filterwarnings("ignore")

path = 'D:/Documentos/NTT_DATA/coffee_db.parquet'
df = pd.read_parquet(path)
print(df.shape)
print(df.keys())
print(len(df['Country']))
print(len(np.unique(df['Country'])))
print(len(np.unique(df['Coffee type'])))

# Melt del dataframe para transponerlo
df_T = df.melt(
    id_vars=['Country', 'Coffee type','Total_domestic_consumption'], 
    value_vars=[col for col in df.columns if '/' in col],  # columnas con formato '1990/91'
    var_name='Year', 
    value_name='Consumption'
)

df_T['Year'] = df_T['Year'].str[:4].astype(int)

df_T['Consumption'] = pd.to_numeric(df_T['Consumption'], errors='coerce')
df_T.to_csv("coffee_db.csv", index=False)
print(df_T.isnull().sum())

# Grafica para ver el comportamiento de los datos:
plt.figure(figsize=(24, 12))
sns.lineplot(data=df_T, 
             x='Year', 
             y='Consumption', 
             hue='Country', 
             style='Coffee type', 
             palette='tab10')

plt.yscale('log')
plt.title('Producción de café (escala logarítmica)')
plt.xlabel('Año')
plt.ylabel('Producción')
plt.legend(title='País / Tipo de café', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("Prod_cafe.png", dpi=300)

# Filtrar valores válidos (positivos)
df_valid = df_T[df_T['Consumption'] > 0].copy()

# Agrupación y estadísticas por grupo
summary_stats = df_valid.groupby(['Country', 'Coffee type']).agg(
    Total_Consumption=('Consumption', 'sum'),
    Valid_Years_Count=('Year', 'nunique'),
    Mean=('Consumption', 'mean'),
    Median=('Consumption', 'median'),
    P25=('Consumption', lambda x: x.quantile(0.25)),
    P75=('Consumption', lambda x: x.quantile(0.75)),
    Variance=('Consumption', 'var'),
    Std_Dev=('Consumption', 'std')
).reset_index()

# Obtener año de mayor y menor consumo
max_min_years = df_valid.groupby(['Country', 'Coffee type']).apply(
    lambda g: pd.Series({
        'Year_Max_Consumption': g.loc[g['Consumption'].idxmax(), 'Year'],
        'Year_Min_Consumption': g.loc[g['Consumption'].idxmin(), 'Year']
    })
).reset_index()

# Combinar ambas tablas
final_summary = pd.merge(summary_stats, max_min_years, on=['Country', 'Coffee type'])

# Guardar en CSV si deseas exportarlo
final_summary.to_csv('resumen_consumo_cafe.csv', index=False)

# Mostrar resumen
print(final_summary.head())


# ============ Graficas de consumo por pais/continente ============
# Mapeo manual de países a continentes
pais_a_continente = {
    'Angola': 'Africa', 'Bolivia (Plurinational State of)': 'South America', 'Brazil': 'South America',
    'Burundi': 'Africa', 'Cameroon': 'Africa', 'Central African Republic': 'Africa',
    'Colombia': 'South America', 'Congo': 'Africa', 'Costa Rica': 'Central America',
    'Cuba': 'Central America', "CÃ´te d'Ivoire": 'Africa', 'Democratic Republic of Congo': 'Africa',
    'Dominican Republic': 'Central America', 'Ecuador': 'South America', 'El Salvador': 'Central America',
    'Ethiopia': 'Africa', 'Gabon': 'Africa', 'Ghana': 'Africa', 'Guatemala': 'Central America',
    'Guinea': 'Africa', 'Guyana': 'South America', 'Haiti': 'Central America', 'Honduras': 'Central America',
    'India': 'Asia', 'Indonesia': 'Asia', 'Jamaica': 'Central America', 'Kenya': 'Africa',
    "Lao People's Democratic Republic": 'Asia', 'Liberia': 'Africa', 'Madagascar': 'Africa',
    'Malawi': 'Africa', 'Mexico': 'North America', 'Nicaragua': 'Central America', 'Nigeria': 'Africa',
    'Panama': 'Central America', 'Papua New Guinea': 'Oceania', 'Paraguay': 'South America',
    'Peru': 'South America', 'Philippines': 'Asia', 'Rwanda': 'Africa', 'Sierra Leone': 'Africa',
    'Sri Lanka': 'Asia', 'Tanzania': 'Africa', 'Thailand': 'Asia', 'Timor-Leste': 'Asia',
    'Togo': 'Africa', 'Trinidad & Tobago': 'Central America', 'Uganda': 'Africa', 'Venezuela': 'South America',
    'Viet Nam': 'Asia', 'Yemen': 'Asia', 'Zambia': 'Africa', 'Zimbabwe': 'Africa'
}

df_T['Continent'] = df_T['Country'].map(pais_a_continente)


# Filtrar valores válidos
df_valid = df_T[df_T['Consumption'] > 0].copy()

# Total por continente
total_por_continente = df_valid.groupby('Continent')['Consumption'].sum().reset_index()

# Lista de países por continente
paises_por_continente = df_valid.groupby('Continent')['Country'].unique().reset_index()
paises_por_continente['Country'] = paises_por_continente['Country'].apply(lambda x: ', '.join(sorted(np.unique(x))))

# Graficar
plt.figure(figsize=(10, 6))
sns.barplot(data=total_por_continente, x='Continent', y='Consumption', palette='Set3')
plt.title('Consumo Total por Continente')
plt.ylabel('Consumo Total')
plt.xlabel('Continente')
plt.tight_layout()
plt.savefig("Consumo_Total_Continente.png", dpi=300)


# Evolución anual por continente
anual_continente = df_valid.groupby(['Year', 'Continent'])['Consumption'].sum().reset_index()

# Países en cada grupo para agregar en la leyenda
legend_labels = df_valid.groupby('Continent')['Country'].unique().apply(lambda x: ', '.join(sorted(np.unique(x)))).to_dict()

# Graficar
plt.figure(figsize=(12, 6))
sns.lineplot(data=anual_continente, x='Year', y='Consumption', hue='Continent', marker='o', palette='tab10')

# Customizar leyenda con países
handles, labels = plt.gca().get_legend_handles_labels()
new_labels = [f"{label} ({legend_labels[label]})" if label in legend_labels else label for label in labels]
plt.legend(handles, new_labels, title='Continente (Países)', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.title('Evolución del Consumo Anual por Continente')
plt.xlabel('Año')
plt.ylabel('Consumo')
plt.tight_layout()
plt.savefig("Consumo_Anual_Continente.png", dpi=300)


# ============ Graficas de consumo por tipo de café ============
tipo_total = df_T[df_T['Consumption'] > 0].groupby('Coffee type')['Consumption'].sum().reset_index()

plt.figure(figsize=(8, 6))
sns.barplot(data=tipo_total, x='Coffee type', y='Consumption', palette='muted')
plt.title('Consumo Total por Tipo de Café')
plt.xlabel('Tipo de Café')
plt.ylabel('Consumo Total')
plt.tight_layout()
plt.savefig("Consumo_Total_Tipo.png", dpi=300)
plt.close()

tipo_anual = df_T[df_T['Consumption'] > 0].groupby(['Year', 'Coffee type'])['Consumption'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=tipo_anual, x='Year', y='Consumption', hue='Coffee type', marker='o')
plt.title('Evolución del Consumo por Tipo de Café')
plt.xlabel('Año')
plt.ylabel('Consumo')
plt.tight_layout()
plt.savefig("Evolucion_Consumo_Tipo.png", dpi=300)
plt.close()


# ============ Revisar la rendencia de cada variedad de café ============

# Calculamos pendiente de regresión lineal para cada tipo
tendencias = []

for tipo in tipo_anual['Coffee type'].unique():
    sub_df = tipo_anual[tipo_anual['Coffee type'] == tipo]
    X = sub_df[['Year']]
    y = sub_df['Consumption']
    model = LinearRegression()
    model.fit(X, y)
    pendiente = model.coef_[0]
    r2 = model.score(X, y)
    tendencias.append({
        'Coffee type': tipo,
        'Trend (slope)': pendiente,
        'R²': r2
    })

tendencias_df = pd.DataFrame(tendencias)
tendencias_df.to_csv('tendencias_tipo.csv', index=False)
print(tendencias_df)

plt.figure(figsize=(10, 6))
sns.lmplot(data=tipo_anual, x='Year', y='Consumption', hue='Coffee type', ci=None, aspect=1.5)
plt.title('Tendencia del Consumo por Tipo de Café (Regresión Lineal)')
plt.xlabel('Año')
plt.ylabel('Consumo Total')
plt.tight_layout()
plt.savefig("Tendencia_Tipo_Cafe_LinearFit.png", dpi=300)
plt.close()

# ============ Revisar la rendencia de paises importantes ============
# Agrupamos por país y año
consumo_anual_pais = df_valid.groupby(['Country', 'Year'])['Consumption'].sum().reset_index()

# Calculamos la pendiente para cada país
tendencias_paises = []

for pais in consumo_anual_pais['Country'].unique():
    sub_df = consumo_anual_pais[consumo_anual_pais['Country'] == pais]
    if len(sub_df) >= 2:  # mínimo dos puntos para regresión
        X = sub_df[['Year']]
        y = sub_df['Consumption']
        model = LinearRegression()
        model.fit(X, y)
        pendiente = model.coef_[0]
        r2 = model.score(X, y)
        tendencias_paises.append({
            'Country': pais,
            'Trend (slope)': pendiente,
            'R²': r2
        })

tendencias_df = pd.DataFrame(tendencias_paises)
tendencias_df.to_csv('tendencias_pais.csv', index=False)
print(tendencias_df)

top_positivos = tendencias_df.sort_values(by='Trend (slope)', ascending=False).head(4)['Country'].tolist()

df_top_positivos = consumo_anual_pais[consumo_anual_pais['Country'].isin(top_positivos)]

plt.figure(figsize=(10, 6))
sns.lmplot(data=df_top_positivos, x='Year', y='Consumption', hue='Country')
plt.title('Tendencia de Consumo – 4 Países con Mayor Tendencia Positiva')
plt.xlabel('Año')
plt.ylabel('Consumo')
plt.tight_layout()
plt.savefig("Tendencias_Top4_Paises_Pos.png", dpi=300)
plt.close()


paises_volumen = [
    'Brazil', 'Indonesia', 'Ethiopia', 'Mexico', 'Philippines', 'Colombia',
    'Venezuela', 'India', 'Viet Nam', 'Thailand'
]

df_paises_grandes = consumo_anual_pais[consumo_anual_pais['Country'].isin(paises_volumen)]

plt.figure(figsize=(12, 6))
sns.lmplot(data=df_paises_grandes, x='Year', y='Consumption', hue='Country')
plt.title('Tendencia de Consumo – Países con Mayor Volumen Total')
plt.xlabel('Año')
plt.ylabel('Consumo')
plt.tight_layout()
plt.savefig("Tendencias_Paises_Mayor_Volumen.png", dpi=300)
plt.close()

# =========== ciclos de consumo
# Agrupar por país y año
df_valid = df_T[df_T['Consumption'] > 0].copy()
pais_anual = df_valid.groupby(['Country', 'Year'])['Consumption'].sum().reset_index()

# Inicializar lista de resultados
etiquetas = []

for pais in pais_anual['Country'].unique():
    sub_df = pais_anual[pais_anual['Country'] == pais]
    
    if len(sub_df) >= 4:
        X = sub_df[['Year']]
        y = sub_df['Consumption']
        
        # Regresión lineal
        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        std = y.std()
        mean = y.mean()
        cv = std / mean if mean > 0 else 0  # coeficiente de variación
        
        # Clasificación según pendiente y variabilidad
        if slope > 5 and cv < 0.25:
            ciclo = 'Crecimiento'
        elif slope < -5:
            ciclo = 'Declinante'
        elif cv >= 0.4:
            ciclo = 'Volátil'
        else:
            ciclo = 'Maduro'
        
        etiquetas.append({
            'Country': pais,
            'Slope': slope,
            'CV': cv,
            'Classification': ciclo
        })

df_ciclo_consumo = pd.DataFrame(etiquetas)
df_ciclo_consumo.to_csv("clasificacion_ciclo_consumo.csv", index=False)

# ========== Analisis de concentracion de mercado
# Consumo total por país
total_pais = df_valid.groupby('Country')['Consumption'].sum().reset_index()

# Gini
def gini_coefficient(x):
    x_sorted = np.sort(x)
    n = len(x)
    cumulative = np.cumsum(x_sorted)
    return (n + 1 - 2 * np.sum(cumulative) / cumulative[-1]) / n

gini = gini_coefficient(total_pais['Consumption'].values)

# HHI (Herfindahl-Hirschman Index)
shares = total_pais['Consumption'] / total_pais['Consumption'].sum()
hhi = np.sum((shares * 100) ** 2)  # multiplicado por 100 para usar en base porcentual

print(f"Gini: {gini:.4f}")
print(f"HHI: {hhi:.2f}")

# ============ Forecast con ARIMA ============
# Forecast por tipo de café
resultados_tipo = {}

for tipo in tipo_anual['Coffee type'].unique():
    serie = tipo_anual[tipo_anual['Coffee type'] == tipo].set_index('Year')['Consumption']
    
    modelo = ARIMA(serie, order=(1, 1, 1))  # Parámetros estándar, se pueden ajustar con AIC/BIC
    modelo_fit = modelo.fit()
    
    forecast = modelo_fit.forecast(steps=5)
    resultados_tipo[tipo] = forecast
    print(f"\nPronóstico para {tipo}:\n", forecast)
    
# Inicializar lista para recolectar resultados
forecast_tipo_rows = []

for tipo, forecast in resultados_tipo.items():
    last_year = tipo_anual[tipo_anual['Coffee type'] == tipo]['Year'].max()
    forecast_years = [last_year + i for i in range(1, len(forecast)+1)]
    
    for year, value in zip(forecast_years, forecast):
        forecast_tipo_rows.append({
            'Year': year,
            'Coffee type': tipo,
            'Consumption': value,
            'Forecast': True
        })

df_forecast_tipo = pd.DataFrame(forecast_tipo_rows)

    
# Lista de países seleccionados
paises_objetivo = ['Brazil', 'Indonesia', 'Ethiopia', 'Mexico', 'Philippines']

# Agrupar por año y país
pais_anual = df_T[df_T['Consumption'] > 0].groupby(['Year', 'Country'])['Consumption'].sum().reset_index()

# Forecast por país
resultados_pais = {}

for pais in paises_objetivo:
    serie = pais_anual[pais_anual['Country'] == pais].set_index('Year')['Consumption']
    
    if len(serie) > 5:  # asegurar suficientes datos
        modelo = ARIMA(serie, order=(1, 1, 1))
        modelo_fit = modelo.fit()
        forecast = modelo_fit.forecast(steps=5)
        resultados_pais[pais] = forecast
        print(f"\nPronóstico para {pais}:\n", forecast)

# Inicializar lista para recolectar resultados
forecast_pais_rows = []

for pais, forecast in resultados_pais.items():
    last_year = pais_anual[pais_anual['Country'] == pais]['Year'].max()
    forecast_years = [last_year + i for i in range(1, len(forecast)+1)]
    
    for year, value in zip(forecast_years, forecast):
        forecast_pais_rows.append({
            'Year': year,
            'Country': pais,
            'Consumption': value,
            'Forecast': True
        })

df_forecast_pais = pd.DataFrame(forecast_pais_rows)

df_forecast_tipo.to_csv("forecast_variedad_cafe.csv", index=False)
df_forecast_pais.to_csv("forecast_paises_top.csv", index=False)

# ========== Clusterizacion k means ==========

# Filtrar datos válidos
df_valid = df_T[df_T['Consumption'] > 0].copy()

# Pivotear: una fila por país, columnas por año
pivot_df = df_valid.pivot_table(index='Country', columns='Year', values='Consumption')

# Imputar nulos (opción: usar 0 o la media del país)
pivot_df = pivot_df.fillna(0)

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(pivot_df)

# Suponiendo que ya tienes X_scaled
inertias = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# Graficar el codo
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertias, marker='o')
plt.title('Método del Codo para Selección de k')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inertia')
plt.xticks(k_values)
plt.grid(True)
plt.tight_layout()
plt.savefig("Elbow_Method_KMeans.png", dpi=300)
plt.close()


# K-Means clustering (elige k=4 como punto de partida)
kmeans = KMeans(n_clusters=3, random_state=42)
pivot_df['Cluster'] = kmeans.fit_predict(X_scaled)

# Reducción de dimensionalidad para visualización
pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)
pivot_df['PC1'] = coords[:, 0]
pivot_df['PC2'] = coords[:, 1]

# Visualización
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pivot_df, x='PC1', y='PC2', hue='Cluster', palette='tab10', s=100)
plt.title('Clustering de Países según Consumo Anual de Café')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend(title='Cluster')
plt.tight_layout()
plt.savefig("Clustering_Paises_Cafe.png", dpi=300)
plt.close()

# Guardar países y sus clústers
pivot_df[['Cluster', 'PC1', 'PC2']].to_csv("clustering_resultados.csv")
