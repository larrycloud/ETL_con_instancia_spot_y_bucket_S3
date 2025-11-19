# WARNING - Instalaciones necesarias:
# pip3 install boto3
# Si deseas actualizar python:
# sudo amazon-linux-extras install python3.8
# sudo alternatives --set python /usr/bin/python3.8
# python3.9 -m pip install boto3
# python3.9 --version
import boto3

# Configuración
S3_BUCKET = "output-s3-spot-bucket"
ARCHIVO_ORIGEN = "input_data.txt"
ARCHIVO_DESTINO = "output_data.txt"

# Cliente S3
s3 = boto3.client("s3")

# Extract (Extracción)
with open(ARCHIVO_ORIGEN, "r") as archivo:
    datos = archivo.readlines()

# Transform (Transformación)
# - Mantener encabezado igual
# - Para cada línea de datos:
#   * Pasar a mayúsculas
#   * Agregar ";CHECKED_BY=ETL-SPOT"
lineas_transformadas = []
for i, linea in enumerate(datos):
    if i == 0:
        # Encabezado: lo dejamos casi igual, solo añadimos nueva "columna"
        encabezado = linea.strip() + ";CHECKED_BY\n"
        lineas_transformadas.append(encabezado)
    else:
        contenido = linea.strip().upper()
        nueva_linea = f"{contenido};ETL-SPOT\n"
        lineas_transformadas.append(nueva_linea)

# Guardar los datos transformados localmente
with open(ARCHIVO_DESTINO, "w") as archivo:
    archivo.writelines(lineas_transformadas)

# Load (Carga) - Subir el archivo transformado a S3
try:
    s3.upload_file(ARCHIVO_DESTINO, S3_BUCKET, ARCHIVO_DESTINO)
    print(f"Archivo '{ARCHIVO_DESTINO}' subido exitosamente a '{S3_BUCKET}'.")
except Exception as e:
    print(f"Error al subir el archivo a S3: {e}")
