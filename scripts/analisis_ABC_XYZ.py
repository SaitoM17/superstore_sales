import pandas as pd
import numpy as np

# Cargar datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Calcular ventas totales por productos
ventas_totales = df_store_sales.groupby('Product Name')['Sales'].sum().reset_index()
ventas_totales.rename(columns={
    'Sales': 'Sales_totales'
}, inplace=True)

# Calcular porcentaje acumulado para ABC
ventas_totales = ventas_totales.sort_values(by='Sales_totales', ascending=False)
ventas_totales['Porcentaje'] = (ventas_totales['Sales_totales'] / ventas_totales['Sales_totales'].sum() * 100)
ventas_totales['Porcentaje_acumulado'] = ventas_totales['Porcentaje'].cumsum()

# Clasificar ABC
def clasificar_abc(pct_acum):
    if pct_acum <= 80:
        return 'A'
    elif pct_acum <= 95:
        return 'B'
    else:
        return 'C'
    
ventas_totales['ABC'] = ventas_totales['Porcentaje_acumulado'].apply(clasificar_abc)

# Calcular variabilidad de la demanda
variabilidad = df_store_sales.groupby('Product Name')['Sales'].agg(['mean','std']).reset_index()
variabilidad['cv'] = (variabilidad['std'] / variabilidad['mean']) * 100