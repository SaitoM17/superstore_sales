import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv') 

# Conteo de clientes unicos
clientes_unicos = df_store_sales['Customer ID'].unique()
cantidad_clientes = len(clientes_unicos)

# Ventas por cliente
clientes_ventas = df_store_sales.groupby(['Customer ID', 'Customer Name'])['Sales'].sum()
clientes_ventas_ordenado = clientes_ventas.sort_values(ascending=False)

print(f'Cantidad de Clientes Únicos: {cantidad_clientes}')
print(f'Ventas por Cliente(Top 10)\n{clientes_ventas_ordenado.head(10)}')