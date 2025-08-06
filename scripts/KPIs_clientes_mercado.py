import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv') 

# Conteo de clientes unicos
clientes_unicos = df_store_sales['Customer ID'].unique()
cantidad_clientes = len(clientes_unicos)

print(f'Cantidad de clientes unicos: {cantidad_clientes}')
