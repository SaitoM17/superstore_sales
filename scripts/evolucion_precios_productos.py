import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

# Cargar los conjuntos de datos
# Conjunto de datos con Outlier(Valores atípicos)
df_store_sales_outliers = pd.read_csv('./data/raw/store_sales_con_outliers.csv')

# Conjunto de datos Original
df_store_sales_original = pd.read_csv('./data/raw/train.csv')


# Explorar el conjunto de datos con Outliers y tomar varios nombres de productos
def obtener_nombre_producto_aleatorio():
    nombre_productos = df_store_sales_outliers['Product Name'].value_counts()
    datos_aleatorios = nombre_productos.sample(n=1)
    nombre_producto_aleatorio = datos_aleatorios.index[0]

    return nombre_producto_aleatorio

def buscar_palabras_similares(palabra_buscada, umbral_similitud=90):
    
    scorer=fuzz.ratio

    # Obtener la lista de nombres únicos y limpios del DataFrame global
    nombres_unicos = df_store_sales_original['Product Name'].dropna().unique()

    similares = process.extractBests(
        query=palabra_buscada,
        choices=nombres_unicos,
        scorer=scorer,
        score_cutoff=umbral_similitud
    )

    lista_nombres_similares = [
        nombre_similar for nombre_similar, score in similares
        if nombre_similar.lower() != palabra_buscada.lower() # Compara de forma insensible a mayúsculas/minúsculas
    ]

    return lista_nombres_similares

# Función para obtener la evolución del precio por producto
def evolucion_precio_producto(data_frame_x, lista_annios, nom_producto):

    # Lista de data frame para recorrer
    for a, data in enumerate(data_frame_x):

        # Obtener los meses por el año en cuestion 
        meses_annio_x = data['Order Month'].unique()
        meses_annio_x.sort()

        # Lista para almacenar los DataFrames procesados de cada mes para este año
        resultados_mensuales = [] 

        for i in meses_annio_x:

            # Extraer el mes en orden
            mes_x = data[data['Order Month'] == i]
            
            if not mes_x.empty: # Solo procesar si hay datos para el mes
                # Agrupar precio del producto por mes(crear lista)
                df_agrupado = mes_x.groupby(['Product Name', 'Order Month'])['Sales'].apply(list).reset_index()

                # Renombrar la columna 'Sales' a algo más descriptivo temporalmente
                df_agrupado = df_agrupado.rename(columns={'Sales': 'Sales_Lista_Temporal'})

                # Crear la columna Sales en formato String
                df_agrupado['Sales en el mes'] = df_agrupado['Sales_Lista_Temporal'].apply(lambda x: ', '.join(map(str, x)))

                # Calcular el "Sales Promedio Mensual"
                df_agrupado['Sales Promedio Mensual'] = df_agrupado['Sales_Lista_Temporal'].apply(lambda x: np.mean(x))

                # Eliminar la columna auxiliar 'Sales_Lista_Temporal'
                df_preliminar = df_agrupado.drop(columns=['Sales_Lista_Temporal'])

                # print(f'Datas Frames del {lista_annios[a % len(lista_annios)]}')

                # Filtrado
                df_filtrado_producto = df_preliminar[df_preliminar['Product Name'] == nom_producto]

                # print(df_final)
                if not df_filtrado_producto.empty:
                    resultados_mensuales.append(df_filtrado_producto)

        # Si hay resultados para este año y producto, concatenarlos
        if resultados_mensuales:
            df_final_anual = pd.concat(resultados_mensuales, ignore_index=True)
            print(f'\nDatos para el producto "{nom_producto}" en el año {lista_annios[a]}:')
            print(df_final_anual)
        else:
            print(f'\nNo se encontraron datos para el producto "{nom_producto}" en el año {lista_annios[a]}')


# Transformacioón de Order Date conjunto original
df_store_sales_original['Order Date'] = pd.to_datetime(df_store_sales_original['Order Date'], format='%d/%m/%Y')

# Tranformación de Ship Date conjunto original
df_store_sales_original['Ship Date'] = pd.to_datetime(df_store_sales_original['Ship Date'], format='%d/%m/%Y')

df_store_sales_original['Order Year'] = df_store_sales_original['Order Date'].dt.year
df_store_sales_original['Order Month'] = df_store_sales_original['Order Date'].dt.month

# Crear DataFrame para cada año que conforman el conjunto original
df_2015_original = df_store_sales_original[df_store_sales_original['Order Year'] == 2015]
df_2016_original = df_store_sales_original[df_store_sales_original['Order Year'] == 2016]
df_2017_original = df_store_sales_original[df_store_sales_original['Order Year'] == 2017]
df_2018_original = df_store_sales_original[df_store_sales_original['Order Year'] == 2018]

# Parametros a ingresar a las funciones
df_lista = [df_2015_original, df_2016_original, df_2017_original, df_2018_original]
annios = ['2015', '2016', '2017', '2018']

nombre_producto = obtener_nombre_producto_aleatorio()

resultados = buscar_palabras_similares(nombre_producto,70)

print('-' * 100)
print(f"Evolución del precio del producto '{nombre_producto}'")
print('-' * 100)
evolucion_precio_producto(
    data_frame_x=df_lista, 
    lista_annios=annios, 
    nom_producto=nombre_producto
)

print('-' * 100)

if not resultados:
    print(f"Sin productos similarea para -> '{nombre_producto}'")
else:
    print(f"\nEvolución del precio de productos similares a -> '{nombre_producto}'")
    for i,nombre_similar in enumerate(resultados):
        print(f'{i}.-{nombre_similar}')

    print('-' * 100)

    for nombre_similar in resultados:
        evolucion_precio_producto(
            data_frame_x=df_lista,
            lista_annios=annios,
            nom_producto=nombre_similar
        )
        print('-' * 100)