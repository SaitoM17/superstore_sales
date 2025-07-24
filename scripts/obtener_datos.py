import kagglehub
import shutil
import os

# Download latest version
path = kagglehub.dataset_download("rohitsahoo/sales-forecasting")

print("Ruta del conjunto de datos:", path)

origen_archivo = 'C:/Users/52771/.cache/kagglehub/datasets/rohitsahoo/sales-forecasting/versions/2/train.csv'

destino_archivo = 'C:/Workspace/Data Scientist/Portafolio/superstore_sales/data/raw'

if not os.path.exists(origen_archivo):
    print(f"Error: El archivo de origen no existe en '{origen_archivo}'")
else:
    os.makedirs(destino_archivo, exist_ok=True)
    try:
        shutil.move(origen_archivo, destino_archivo)
        print(f"'{origen_archivo}' movido exitosamente a '{destino_archivo}'")

    except Exception as e:
        print(f"Ocurrió un error al mover el archivo: {e}")