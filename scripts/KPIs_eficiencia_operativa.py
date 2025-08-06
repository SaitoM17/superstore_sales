import pandas as pd

# Carga del conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Tranformación fecha de object a datime
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')
df_store_sales['Ship Date'] = pd.to_datetime(df_store_sales['Ship Date'], format='%d/%m/%Y')

# Tiempoa promedio de envio
df_store_sales['Difference in Days'] = (df_store_sales['Ship Date'] - df_store_sales['Order Date'])
promedio_dias = df_store_sales['Difference in Days'].dt.days.mean()

print(f'Tiempo Promedio de Entrega(días): {promedio_dias:.0f} días')