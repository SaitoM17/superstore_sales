import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Preparación de datos
basket = (df_store_sales.groupby(['Order ID', 'Product Name'])['Product Name']
          .count().unstack().reset_index().fillna(0)
          .set_index('Order ID'))

# Convertir cantidades de 0 a 1
basket = basket.applymap(lambda x: 1 if x > 0 else 0)

# Aplicar Apriori para encontrar combinaciones frecuentes
frequent_itemsets = apriori(basket, min_support=0.02, use_colnames=True)

# Reglas de asociación
reglas = association_rules(frequent_itemsets, metric='lift', min_threshold=1)