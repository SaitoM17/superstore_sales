import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Carga de conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Fecha
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')

# Calcular metricas
fecha_ultima = df_store_sales['Order Date'].max()

clientes = df_store_sales.groupby('Customer ID').agg({
    'Order Date': lambda x: (fecha_ultima - x.max()).days,
    'Customer ID': 'count',
    'Sales': 'sum'
})

clientes.rename(columns={
    'Order Date': 'Recency',
    'Customer ID': 'Frecuency',
    'Sales': 'Monetary'
}, inplace=True)

# Escalar datos
caracteristicas = ['Recency', 'Frecuency', 'Monetary']
escalador = StandardScaler()
clientes_escalador = escalador.fit_transform(clientes[caracteristicas])

# Determinar número óptimo de clusters
inertia = []
for k in range(2, 10):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(clientes_escalador)
    inertia.append(kmeans.inertia_)

plt.plot(range(2, 10), inertia, marker='o')
plt.xlabel('Número de Clusters')
plt.ylabel('Inercia (Dentro de la suma de cuadrados)')
plt.title('Método del Codo')
plt.show()