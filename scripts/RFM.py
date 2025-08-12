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

# Calcular puntuación RFM del 1 al 5
rfm['R_score'] = pd.qcut(rfm['R_score'], 5, labels=[1,2,3,4,5])
rfm['F_score'] = pd.qcut(rfm['F_score'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['M_score'], 5, labels=[1,2,3,4,5])

# Calculo de score final
rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# Clasificación de clientes
def clasificacion_cliente(row):
    if row['R_score'] >= 4 and row['F_score'] >= 4 and row['M_score'] >= 4:
        return 'VIP'
    elif row['R_score'] <= 2 and row['F_score'] <= 2:
        return 'En riesgo'
    else:
        return 'Regular'

rfm['Segmento'] = rfm.apply(clasificacion_cliente, axis=1)