import pandas as pd

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

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
rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])

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

# Resultados
clientes_VIP = rfm[rfm['Segmento'] == 'VIP']
clientes_riesgo = rfm[rfm['Segmento'] == 'En riesgo']

print('Clientes VIP')
print(clientes_VIP)

print('Clientes En riesgo')
print(clientes_riesgo)

# Guardar resultados
try:
    opcion = int(input(
        '¿Desea guardar los resultados en archivos CSV?\n'
        '(1 = Guardar los archivos, cualquier otra tecla = No guardar)\n> '
    ))

    if opcion == 1:
        clientes_VIP.to_csv('./data/processed/clientes_vip.csv', index=False)
        clientes_riesgo.to_csv('./data/processed/clientes_riesgo.csv', index=False)

        print('Archivos guardados')
    else:
        print('No se guardaron los archivos de clientes VIP y en riesgo.')

except ValueError:
    print('Entrada inválida. Debe ingresar un número (por ejemplo, 1 para guardar).')

except Exception as e:
    print(f'Ocurrió un error al guardar los archivos: {e}')