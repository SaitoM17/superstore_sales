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
}).rename(columns={
    'Order Date': 'Recency',
    'Customer ID': 'Frequency',
    'Sales': 'Monetary'
}).reset_index()

# Escalar datos
caracteristicas = ['Recency', 'Frequency', 'Monetary']
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

# Entrenar modelo con k óptimo
k_optimo = 4
kmeans = KMeans(n_clusters=k_optimo, random_state=42, n_init=10)
clientes['Cluster'] = kmeans.fit_predict(clientes_escalador)

# Perfil de cada cluster
perfil_clusters = clientes.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': "mean",
    'Customer ID': 'count' # Deberia ser Customer ID
}).rename(columns={'Customer ID': 'Num_Clientes'}).round(2)

print('Perfil de Clusters')
print(perfil_clusters)

# Visualizar cluster
sns.scatterplot(
    data=clientes,
    x='Frequency',
    y='Monetary',
    hue='Cluster',
    palette='Set2'
)
plt.title('Segmentación de Clientes (K-Means)')
plt.show()

# Interpretación
for cluster_id, row in perfil_clusters.iterrows():
    print(f'\nCluster {cluster_id}:')
    if row['Recency'] < clientes['Recency'].mean() and row['Frequency'] > clientes['Frequency'].mean():
        print('Compradores Frecuentes')
    elif row['Recency'] > clientes['Recency'].mean() and row['Frequency'] < clientes['Frequency'].mean():
        print('Clientes inanctivos')
    elif row['Frequency'] > clientes['Frequency'].mean() and row['Monetary'] > clientes['Monetary'].mean():
        print('Grandes compradores')
    else:
        print('Compradores ocasionales')