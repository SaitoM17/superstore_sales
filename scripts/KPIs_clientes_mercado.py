import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv') 

# Conteo de clientes unicos
clientes_unicos = df_store_sales['Customer ID'].unique()
cantidad_clientes = len(clientes_unicos)

# Ventas por cliente
clientes_ventas = df_store_sales.groupby(['Customer ID', 'Customer Name'])['Sales'].sum()
clientes_ventas_ordenado = clientes_ventas.sort_values(ascending=False)

# Ventas por segmento de clientes
ventas_segmento_cliente = df_store_sales.groupby(['Segment'])['Sales'].sum()

print(f'Cantidad de Clientes Únicos: {cantidad_clientes}')
print(f'Ventas por Cliente(Top 10)\n{clientes_ventas_ordenado.head(10)}')
print(f'Ventas por Segmento de Clientes: ')
print(f'{"Segment":<10}{"Sales":>20}')
for segment, sales in ventas_segmento_cliente.items():
    print(f'{segment:<11}{"$":>7}{sales:>12,.2f}')
