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

# Clasificación XYZ
def clasificar_xyz(cv):
    if cv <= 10:
        return 'X'
    elif cv <= 25:
        return 'Y'
    else:
        return 'Z'
    
variabilidad['XYZ'] = variabilidad['cv'].apply(clasificar_xyz)

# Unir clasificación
clasificacion = pd.merge(ventas_totales, variabilidad, on='Product Name')
clasificacion['ABC_XYZ'] = clasificacion['ABC'] + clasificacion['XYZ']

if clasificacion.empty:
    print('No se encontraron conjuntos frecuentes con el soporte especificado')
else:    
    # Mostrar resultados
    print(clasificacion)
    try:
        opcion = int(input(
            '¿Desea guardar los resultados en archivos CSV?\n'
            '(1 = Guardar los archivos, cualquier otra tecla = No guardar)\n> '
        ))

        if opcion == 1:
            clasificacion.to_csv('./data/processed/frequent_itemsets.csv', index=False)
            print('Archivos guardados')
        else:
            print('No se guardaron los archivos de clientes VIP y en riesgo.')
            
    except ValueError:
        print('Entrada inválida. Debe ingresar un número (por ejemplo, 1 para guardar).')

    except Exception as e:
        print(f'Ocurrió un error al guardar los archivos: {e}')