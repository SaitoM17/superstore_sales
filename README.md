# 📊 SuperStore Sales
# SuperStore Sales Analysis

Este proyecto consiste en un dashboard interactivo y la generación de reportes ejecutivos. Ambas herramientas están diseñadas para analizar el rendimiento de la entrega de pedidos. Los datos utilizados provienen de un conjunto de datos real de entregas recopilado por [Rohit Sahoo](https://www.kaggle.com/rohitsahoo).

---

## 📚 Tabla de Contenidos

- [🎯 Propósito](#-propósito)
- [📦 Conjunto de Datos](#-conjunto-de-datos)
- [🧪 Desarrollo del Proyecto](#-desarrollo-del-proyecto)
- [📌 Vista previa del Dashboard](#-vista-previa-del-dashboard)
- [💡 Insight clave](#-insight-clave)
- [📈 Recomendaciones](#-recomendaciones)
- [🛠️ Tecnologías](#️-tecnologías)
- [⚙️ Instalación](#️-instalación)
- [📂 Archivos](#-archivos)
- [👤 Autor](#-autor)
- [📝 Licencia](#-licencia)

---

## 🎯 Propósito

El proyecto busca evaluar el comportamiento de las ventas de una tienda minorista a partir de datos históricos, considerando diferentes dimensiones clave como producto, cliente, categoría y región. El objetivo es descubrir patrones relevantes, identificar áreas de oportunidad, anticipar riesgos potenciales y establecer estrategias basadas en datos que impulsen decisiones comerciales informadas.

- Obtener KPI's:
   - KPI's de Ventas y Rendimiento Financiero
   - KPI's de Eficiencia Operativa
   - KPI's de Clientes y Mercado

- Analizar el rendimiento de ventas
   - Analizar los ingresos por productos vendidos
   - Analizar su comportamiento en distintos contextos

- Análisis de múltiples dimensiones (Productos, clientes, categorías y región)

- Detectar oportunidades de mejora
   - ¿Dónde se puede aumentar ventas, eficiencia o márgenes?

- Identificar riesgos
   - ¿Qué productos, categorías, clientes o región tiene bajas las ventas y representas un riesgo?

- Encontrar palancas estratégicas
   - ¿Qué están funcionando bien y si se puede escalar?

---

## 📦 Conjunto de Datos

El conjunto de datos utilizado contiene las siguientes columnas:

- `Row ID`: Id de la fila
- `Order ID`: Id del pedido
- `Order Date`: Fecha del pedido
- `Ship Date`: Fecha de envio
- `Ship Mode`: Modo barco
- `Customer ID`: Id del cliente
- `Customer Name`: Nombre del cliente
- `Segment`: Segmento
- `Country`: País
- `City`: Ciudad
- `State`: Estado
- `Postal Code`: Código postal
- `Region`: Región
- `Product ID`: Identificación del producto
- `Category`: Categoría
- `Sub-Category`: SubCategoría
- `Product Name`: Nombre del producto
- `Sales`: Ventas

Fuente: [Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting).

---

## 🧪 Desarrollo del Proyecto

### 1. **Carga y exploración inicial de los datos**
La primera fase de nuestro proyecto fue una exploración exhaustiva del conjunto de datos Superstore Sales. Esta etapa nos permitió obtener una visión general de su composición, confirmando que contiene 9800 registros y 18 columnas.

Esta exploración inicial es crucial para identificar posibles problemas que podrían afectar el análisis, como:
•	Valores duplicados.
•	Valores nulos.
•	Errores de registro (por ejemplo, errores tipográficos).
•	Valores atípicos (valores que se desvían significativamente de la mayoría de los datos).
•	Distribución de datos.

Durante este proceso, se identificaron dos problemas principales:
1.	Se encontraron 11 registros con valores nulos en la columna Postal Code. Afortunadamente, este problema no representa un gran obstáculo, ya que contamos con información complementaria en otras columnas que nos permitirá rellenar los datos faltantes de manera precisa.

2.	Se detectaron valores atípicos en el conjunto de datos. Para abordar este hallazgo, se llevará a cabo un análisis más profundo para comprender la naturaleza de estos registros. Esto nos ayudará a determinar si son datos erróneos que deben ser eliminados, o si representan eventos reales (como ventas excepcionalmente altas) que necesitan ser considerados en el análisis.

Este primer paso nos ha dado una base sólida para comenzar el proceso de limpieza y preparación de datos, asegurando que nuestro análisis posterior sea lo más preciso y fiable posible.

***Archivo:*** [exploracion_inicial.ipynb](notebooks/exploracion_inicial.ipynb)

### 2. **Análisis Valores Atípicos**

El análisis de los registros con valores atípicos en el conjunto de datos de Superstore Sales, respaldado por el script de Python y la visualización adjunta, ha demostrado que estas fluctuaciones en las ventas no son errores de datos. Por el contrario, representan escenarios de precios volátiles y estratégicos, algo común en mercados dinámicos.

![Evolución de las ventas](reports/figures/graficos_evolucion_ventas_outliers.png)
Como se puede observar en el gráfico, los precios fluctúan ampliamente a lo largo de los años 2015 a 2018. Esto sugiere que las variaciones son parte del comportamiento natural del mercado, posiblemente debido a promociones, cambios estacionales o estrategias de la empresa.

El script de Python, que utiliza la biblioteca fuzzywuzzy para comparar nombres de productos y un análisis de la evolución del precio por mes, permitió confirmar que estas fluctuaciones son consistentes con la dinámica de precios del mercado, en lugar de ser errores de registro. Este hallazgo es crucial para el proyecto, ya que nos permite mantener estos datos en el conjunto para un análisis más completo y realista.

***Archivos:*** 
* [eda_outliers.ipynb](notebooks/eda_outliers.ipynb)
* [evolucion_precios_productos.py](scripts/evolucion_precios_productos.py)


### 3. **Limpieza y preprocesamiento**
A partir del análisis exploratorio y del manejo de valores atípicos, se procede a la fase de limpieza de datos. El único problema identificado fue la presencia de 11 valores nulos en la columna Postal Code, lo cual se resolverá mediante una imputación.

Se imputaron los valores faltantes en la columna Postal Code con el código 05403. Esta decisión se tomó al verificar que el código postal de la ciudad de Burlington en Vermont (único registro sin Postal Code pero con todos los demás datos geográficos completos) es 05403.

Adicionalmente, se realizó una transformación del tipo de dato de la columna Postal Code, convirtiéndola de float a un formato de texto (string) y eliminando el .0 de los valores existentes para estandarizar el formato.

El script de Python utilizado para esta tarea es el siguiente:
```Python
# Rellenar los valores nulos en la columna Postal Code
df_store_sales['Postal Code'] = df_store_sales['Postal Code'].fillna('05403')

# Transformación de columna Postal Code
df_store_sales['Postal Code'] = df_store_sales['Postal Code'].astype(str)

# Eliminar .0 de los demás datos
df_store_sales['Postal Code'] = df_store_sales['Postal Code'].str.replace('.0', '', regex=False)

# Verificación de la cantidad de valores nulos
valores_nulos = df_store_sales['Postal Code'].isnull().sum()
print(f'Cantidad de valores nulos: {valores_nulos}')
# Salida: Cantidad de valores nulos: 0

# Filas donde se imputaron los valores nulos
filas_05403 = df_store_sales[df_store_sales['Postal Code'] == '05403']
print(filas_05403)
```

Nota: Las columnas de fecha (Order Date y Ship Date) se mantendrán en su formato actual y se convertirán a un tipo de dato de fecha (datetime) solo cuando sea necesario para un análisis específico, a fin de optimizar el rendimiento y la memoria.

Finalmente, el conjunto de datos, ahora limpio y preparado, se ha guardado en un nuevo archivo CSV llamado store_sales_limpio.csv para su uso en futuras etapas del análisis.

***Archivo:*** [limpieza.ipynb](notebooks/limpieza.ipynb)

3. **Análisis exploratorio de datos (EDA)**:
   - [Ej. Distribución, correlaciones, agrupaciones, etc.]

4. **Visualización de datos**:
   - Uso de gráficos de barras, líneas, cajas, dispersión y mapas de calor.

5. **Modelado o reportes (opcional)**:
   - [Si aplica: modelos de ML, clustering, predicciones, etc.]

---

## 📌 Vista previa del Dashboard

---

## 💡 Insight clave

---

## 📈 Recomendaciones

- [Insight 1]
- [Insight 2]
- [Recomendación práctica o estratégica basada en los datos]

---

## 🛠️ Tecnologías

- Python
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook / Google Colab
- [Otras herramientas que uses, como Scikit-learn, Plotly, etc.]

---

## ⚙️ Instalación

### 1. Clonar este repositorio:
```bash
git clone https://github.com/tu_usuario/nombre_del_proyecto.git
```
### 2. Uso de un Entorno Virtual para Aislar Dependencias

Para evitar conflictos con versiones de librerías, se recomienda usar entornos virtuales.

####  Crear y Activar un Entorno Virtual

##### Crear el entorno virtual:
```
python -m venv venv
```
##### Activar el entorno:
* #### En Windows:

    ```
    venv\Scripts\activate
    ```

* #### En Mac/Linux::

    ```
    source venv/bin/activate
    ```
#### 3. Instalar dependencias dentro del entorno:
* #### Opición 1:
    ```
    pip install -r requirements.txt
    ```

* #### Opción 2 (De forma manual):
    ```
    pip install numpy pandas matplotlib seaborn scikit-learn
    ```

---

## 📂 Archivos

---

## 👤 Autor

**Said Mariano Sánchez** –  📧 *smariano170@gmail.com*  
*Analista de Datos Jr. | Visualización | Power BI | Python | SQL*  
🌎 México  
Este proyecto forma parte de mi portafolio como analista de datos Jr.

---

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Puedes usarlo, modificarlo y distribuirlo libremente, siempre que menciones al autor original.

---