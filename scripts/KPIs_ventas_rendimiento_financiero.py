import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Ventas totales
suma_sales = df_store_sales['Sales'].sum()

# Ventas por promedio por pedido
cantidad_registros, columnas = df_store_sales.shape
ventas_promedio_pedido = suma_sales/cantidad_registros

print(f'Ventas Totales: ${suma_sales:.2f}')
print(f'Ventas Promedio por Pedido: ${ventas_promedio_pedido:.2f}')