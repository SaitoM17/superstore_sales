import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Cargar conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')
print(df_store_sales.head(5))