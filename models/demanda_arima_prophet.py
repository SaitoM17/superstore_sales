import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Cargar conjunto de datos
df_store_sales = pd.read_csv('./data/processed/store_sales_limpio.csv')

# Fecha
df_store_sales['Order Date'] = pd.to_datetime(df_store_sales['Order Date'], format='%d/%m/%Y')

# Selección de Categoria
categorias_unicas = df_store_sales['Category'].unique()

print('Categorías existentes')
for i in categorias_unicas:
    print(i)

# Bucle para validar la selección de categoría
while True:
    categoria = str(input('Seleccione una Categoría válida: '))
    if categoria in categorias_unicas:
        categoria_seleccionda = df_store_sales[df_store_sales['Category'] == categoria]
        break # Si la categoría es válida, salimos del bucle
    else:
        print('Error: La categoría seleccionada no existe. Intente de nuevo.')

# Selección de Sub-Categoria
sub_categoria_unica = categoria_seleccionda['Sub-Category'].unique()
print(f'\nSub-Categorías de {categoria} ')
for i in sub_categoria_unica:
    print(i)

# Bucle para validar la selección de sub-categoría
while True:
    sub_categoria = str(input('Seleccione una Sub-categoría válida: '))
    if sub_categoria in sub_categoria_unica:
        sub_categoria_seleccionada = categoria_seleccionda[categoria_seleccionda['Sub-Category'] == sub_categoria]
        break # Si es válida, salimos
    else:
        print('Error: La sub-categoría seleccionada no existe. Intente de nuevo.')

# Selección de producto
productos_unicos = sub_categoria_seleccionada['Product Name'].unique()
print(f'\nNombre de Productos de la Sub-Caegoria {sub_categoria}')
for i in productos_unicos:
    print(i)

# Bucle para validar la selección de producto
while True:
    producto = str(input('Ingrese el nombre del producto válido: '))
    if producto in productos_unicos:
        break # Si el producto es válido, salimos
    else:
        print('Error: El producto seleccionado no existe. Intente de nuevo.')
print()
# Filtrar por productos
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

# Extraer resultados 
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