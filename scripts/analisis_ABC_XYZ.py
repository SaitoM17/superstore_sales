import pandas as pd
import numpy as np

# Cargar datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Calcular ventas totales por productos
ventas_totales = df_store_sales.groupby('Product Name')['Sales'].sum().reset_index()
ventas_totales.rename(columns={
    'Sales': 'Sales_totales'
}, inplace=True)
print(ventas_totales)