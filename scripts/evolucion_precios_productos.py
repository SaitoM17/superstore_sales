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

    print(f"\nBuscando palabras similares a '{palabra_buscada}' con un umbral del {umbral_similitud}%:\n")

    # Encuentra nombres similares a 'palabra_buscada' en la lista de nombres únicos
    # Usamos process.extractBests para obtener los mejores scores
    # score_cutoff: solo devuelve coincidencias con un puntaje igual o superior al umbral
    similares = process.extractBests(
        query=palabra_buscada,
        choices=nombres_unicos,
        scorer=scorer,
        score_cutoff=umbral_similitud
    )

    # Filtrar para obtener solo coincidencias que no son idénticas a la palabra_buscada
    # (fuzzywuzzy puede incluir la palabra_buscada con 100% de similitud si está en choices)
    resultados_filtrados = [
        (nombre_similar, score) for nombre_similar, score in similares
        if nombre_similar.lower() != palabra_buscada.lower() # Compara de forma insensible a mayúsculas/minúsculas
    ]

    if resultados_filtrados:
        print(f"Palabras similares encontradas para '{palabra_buscada}':")
        for nombre_similar, score in resultados_filtrados:
            print(f" - '{nombre_similar}' (Similitud: {score}%)")
    else:
        print(f"No se encontraron palabras similares a '{palabra_buscada}' con el umbral especificado.")

    return resultados_filtrados


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

# Parametros a ingresar a la función
df_lista = [df_2015_original, df_2016_original, df_2017_original, df_2018_original]
annios = ['2015', '2016', '2017', '2018']

nombre_producto = obtener_nombre_producto_aleatorio()

resultados = buscar_palabras_similares(nombre_producto,70)
print(resultados)

# evolucion_precio_producto(
#     data_frame_x=df_lista, 
#     lista_annios=annios, 
#     nom_producto=nombre_producto
# )