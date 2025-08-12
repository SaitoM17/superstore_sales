import pandas as pd
import numpy as np

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')
print(df_store_sales.head(5))

# Transformación de Order Date y Ship Date a formato fecha
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')
df_store_sales['Ship Date'] = pd.to_datetime(df_store_sales['Ship Date'], format= '%d/%m/%Y')

# Fecha de referencia
fecha_referencia = df_store_sales['Order Date'].max()
