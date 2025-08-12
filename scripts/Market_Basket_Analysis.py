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