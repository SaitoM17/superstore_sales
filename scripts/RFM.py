import pandas as pd
import numpy as np

# Carga de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')
print(df_store_sales.head(5))