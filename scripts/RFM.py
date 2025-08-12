import pandas as pd
import numpy as np
from datetime import datetime

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')
print(df_store_sales.head(5))

# Transformación de Order Date y Ship Date a formato fecha
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')
df_store_sales['Ship Date'] = pd.to_datetime(df_store_sales['Ship Date'], format= '%d/%m/%Y')

# Fecha de referencia
fecha_referencia = df_store_sales['Order Date'].max()

# Calcular métricas RFM
rfm = df_store_sales.groupby('Customer ID').agg({
    'Order Date': lambda x: (fecha_referencia - x.max()).days,
    'Customer ID': 'count',
    'Sales': 'sum'
})

# Renombrar columnas
rfm.rename(columns={
    'Order Date': 'Recency',
    'Customer ID': 'Frequency',
    'Sales': 'Monetary'
}, inplace=True)

print(rfm)