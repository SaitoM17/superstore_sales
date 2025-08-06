import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv') 

# Conteo de clientes unicos
clientes_unicos = df_store_sales['Customer ID'].unique()
cantidad_clientes = len(clientes_unicos)

# Ventas por cliente
clientes_ventas = df_store_sales.groupby(['Customer ID', 'Customer Name'])['Sales'].sum()
clientes_ventas_ordenado = clientes_ventas.sort_values(ascending=False)
clientes_ventas_top = clientes_ventas_ordenado.head(10)

# Ventas por segmento de clientes
ventas_segmento_cliente = df_store_sales.groupby(['Segment'])['Sales'].sum()

print("     KPI's de Clientes y Mercado")
print(f'\nCantidad de Clientes Únicos: {cantidad_clientes}')
print(f'\nVentas por Cliente(Top 10)')
print(f'{"Customer ID":<10}{"Customer Name":>17}{"Sales":>17}')
for (customer_id, customer_name), customer_sales  in clientes_ventas_top.items():
    print(f'{customer_id:<15}{customer_name:<25}{"$"}{customer_sales:>10,.2f}')
print(f'\nVentas por Segmento de Clientes')
print(f'{"Segment":<10}{"Sales":>13}')
for segment, sales in ventas_segmento_cliente.items():
    print(f'{segment:<18}{"$"} {sales:>12,.2f}')