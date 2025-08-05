import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Ventas totales
suma_sales = df_store_sales['Sales'].sum()

# Ventas por promedio por pedido
cantidad_registros, columnas = df_store_sales.shape
ventas_promedio_pedido = suma_sales/cantidad_registros

# Ventas por categoria y sub-categoria
categoria_subcategoria = df_store_sales.groupby(['Category','Sub-Category'])['Sales'].sum()

# Ventas por región
ventas_region = df_store_sales.groupby('Region')['Sales'].sum()

print(f'Ventas Totales: ${suma_sales:.2f}')
print(f'Ventas Promedio por Pedido: ${ventas_promedio_pedido:.2f}')
print(f'Ventas por Categoria y Sub-Categoria\n{categoria_subcategoria}')
print(f'Ventas por Región\n{ventas_region}')