import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Preparación de datos
basket = (df_store_sales.groupby(['Order ID', 'Product Name'])['Product Name']
          .count().unstack().reset_index().fillna(0)
          .set_index('Order ID'))

# Convertir cantidades de 0 a 1
basket = basket.apply(lambda x: x > 0)

# Aplicar Apriori para encontrar combinaciones frecuentes
frequent_itemsets = apriori(basket, min_support=0.005, use_colnames=True)

if frequent_itemsets.empty:
    print('No se encontraron conjuntos frecuentes')
else:    
    # Reglas de asociación
    reglas = association_rules(frequent_itemsets, metric='lift', min_threshold=1)

    # Ordenar por lift más interesante
    reglas = reglas.sort_values(by='lift', ascending=False)

    # Mostrar resultados
    print('Combinación Frecuente')
    print(frequent_itemsets)

    print('\nReglas de Asociación')
    print(reglas[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    try:
        opcion = int(input(
            '¿Desea guardar los resultados en archivos CSV?\n'
            '(1 = Guardar los archivos, cualquier otra tecla = No guardar)\n> '
        ))

        if opcion == 1:
            frequent_itemsets.to_csv('./data/processed/frequent_itemsets.csv', index=False)
            reglas.to_csv('./data/processed/reglas.csv', index=False)

            print('Archivos guardados')
        else:
            print('No se guardaron los archivos de clientes VIP y en riesgo.')
            
    except ValueError:
        print('Entrada inválida. Debe ingresar un número (por ejemplo, 1 para guardar).')

    except Exception as e:
        print(f'Ocurrió un error al guardar los archivos: {e}')