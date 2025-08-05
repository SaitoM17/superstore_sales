import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Ventas totales
suma_sales = df_store_sales['Sales'].sum()

print(f'Ventas totales: ${suma_sales:.2f}')