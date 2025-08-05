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

1. **Carga y exploración inicial de los datos**:
   - Exploración básica con `.head()`, `.info()`, `.describe()`, etc.

2. **Limpieza y preprocesamiento**:
   - Manejo de valores nulos, duplicados, formatos y conversiones de fechas.

3. **Análisis exploratorio de datos (EDA)**:
   - [Ej. Distribución, correlaciones, agrupaciones, etc.]

4. **Visualización de datos**:
   - Uso de gráficos de barras, líneas, cajas, dispersión y mapas de calor.

5. **Modelado o reportes (opcional)**:
   - [Si aplica: modelos de ML, clustering, predicciones, etc.]

6. **Conclusiones y recomendaciones**:
   - Síntesis de hallazgos clave y propuestas de acción.

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