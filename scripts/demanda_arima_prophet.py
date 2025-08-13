import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Cargar conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Fecha
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')

# Filtrar por productos
producto = "Eldon Fold 'N Roll Cart System"
df_producto = df_store_sales[df_store_sales['Product Name'] == producto]

# Agrupar por semana o mes usando la columna 'Order Date'
df_grouped = df_producto.groupby(pd.Grouper(key="Order Date", freq="ME")).agg({
    "Sales": "sum"
}).reset_index()

# Preparar datos para Prophet 
df_forecast = df_grouped.rename(columns={"Order Date": "ds", "Sales": "y"})

# Entrenar modelo Prophet
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,  # Desactivado para evitar ruido en series mensuales
    daily_seasonality=False,
    changepoint_prior_scale=0.5  # Suaviza los cambios de tendencia
)
model.fit(df_forecast)

# Proyectar próximos 12 meses
future = model.make_future_dataframe(periods=12, freq="ME")
forecast = model.predict(future)

# Eliminar valores negativos en yhat
forecast['yhat'] = forecast['yhat'].clip(lower=0)

# 8. Extraer resultados 
result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

# Gráfico combinado: ventas reales + predicción
plt.figure(figsize=(12, 6))

# Ventas históricas
plt.bar(df_forecast['ds'], df_forecast['y'], color='skyblue', label='Ventas reales')

# Predicción
plt.plot(forecast['ds'], forecast['yhat'], color='red', linewidth=2, label='Predicción')
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], 
                 color='pink', alpha=0.3, label='Intervalo de confianza')
plt.title(f"Proyección de demanda - {producto}")
plt.xlabel("Fecha")
plt.ylabel("Ventas")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Mostrar resumen
print(f"Proyección de ventas para {producto}:")
print(result.tail(12))

try:
    opcion = int(input(
        '¿Desea guardar los resultados en archivos CSV?\n'
        '(1 = Guardar los archivos, cualquier otra tecla = No guardar)\n> '
    ))

    if opcion == 1:
        result.to_csv(f'./data/processed/proyeccion_{producto}.csv', index=False)
        print('Archivos guardados')
    else:
        print('No se guardaron los archivos de clientes VIP y en riesgo.')
            
except ValueError:
    print('Entrada inválida. Debe ingresar un número (por ejemplo, 1 para guardar).')

except Exception as e:
    print(f'Ocurrió un error al guardar los archivos: {e}')