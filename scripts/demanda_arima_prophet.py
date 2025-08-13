import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Cargar conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv', parse_dates=['Order Date'])
print(df_store_sales.head(5))

# Filtrar por producto
producto = "Eldon Fold 'N Roll Cart System"
df_producto = df_store_sales[df_store_sales['Product Name'] == producto]

# Agrupar por semana o mes usando la columna 'Order Date'
df_grouped = df_producto.groupby(pd.Grouper(key="Order Date", freq="W")).agg({
    "Sales": "sum"
}).reset_index()

print(df_grouped)