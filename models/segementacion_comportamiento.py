import pandas as pd

# Carga de conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Fecha
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')

# Calcular metricas
fecha_ultima = df_store_sales['Order Date'].max()
print(fecha_ultima)
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

print(clientes)