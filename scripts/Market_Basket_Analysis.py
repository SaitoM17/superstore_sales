import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Crear matriz binaria de productos por pedido
basket = pd.crosstab(df_store_sales['Order ID'], df_store_sales['Product Name']) > 0

# Aplicar Apriori
frequent_itemsets = apriori(basket, min_support=0.002, use_colnames=True)

# Filtrar solo combinaciones de más de un producto
frequent_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(len) > 1]

if frequent_itemsets.empty:
    print('No se encontraron conjuntos frecuentes con el soporte especificado')
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