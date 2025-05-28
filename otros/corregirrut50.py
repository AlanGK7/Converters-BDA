import os
import pandas as pd
import time
from datetime import datetime

def formatear_persona(rut, nombre, edad, direccion):
    """ Asegura que los campos tengan el formato correcto y no estén vacíos. """
    
    # Validar y formatear RUT (rellena con ceros si falta longitud)
    rut = str(rut).strip().zfill(10)[:10] if pd.notna(rut) else '0000000000'

    # Validar y formatear Nombre (máx 50 caracteres, rellena con "N/A" si está vacío)
    nombre = str(nombre).strip().ljust(50)[:50] if pd.notna(nombre) and nombre.strip() else "N/A".ljust(50)

    # Validar y formatear Edad (2 caracteres, rellena con "00" si está vacío)
    edad = str(edad).strip().zfill(2)[:2] if pd.notna(edad) and edad.strip().isdigit() else "00"

    # Validar y formatear Dirección (máx 100 caracteres, rellena con "Sin dirección" si está vacío)
    direccion = str(direccion).strip().ljust(100)[:100] if pd.notna(direccion) and direccion.strip() else "Sin dirección".ljust(100)
    
    return [rut, nombre, edad, direccion]

def procesar_ruts_duplicados_txt(ruta_entrada, chunk_size=1_000_000):
    """ Procesa el archivo en bloques, eliminando duplicados y asegurando el formato de los datos. """

    # Definir ruta de salida
    ruta_salida = ruta_entrada.replace(".txt", "_sin_duplicados.txt")

    # Eliminar archivo de salida si ya existe
    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

    # Diccionario para rastrear RUTs ya vistos
    rut_counts = {}
    modificados = 0
    total_registros = 0
    start_time = time.time()

    with open(ruta_salida, 'w', encoding='utf-8') as salida:
        for i, chunk in enumerate(pd.read_csv(ruta_entrada, sep=r"\|", engine="python", header=None, dtype=str, chunksize=chunk_size)):

            # Nombrar columnas
            chunk.columns = ['rut', 'nombre', 'edad', 'direccion']

            # Asegurar que los datos tengan el formato correcto
            chunk = chunk.apply(lambda row: formatear_persona(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3]), axis=1, result_type='expand')


            # Procesar duplicados en el RUT
            for index, row in chunk.iterrows():
                rut = row[0]  # El RUT ya está formateado en `formatear_persona`

                if rut in rut_counts:
                    # Cambiar el último dígito a '0' si el RUT está repetido
                    nuevo_rut = rut[:-1] + '0'
                    chunk.at[index, 0] = nuevo_rut
                    modificados += 1
                    rut_counts[nuevo_rut] = 1  # Registrar el nuevo RUT modificado
                else:
                    rut_counts[rut] = 1  # Registrar el RUT válido

            # Guardar datos en archivo de salida conservando el formato de .txt
            chunk.to_csv(salida, index=False, header=False, mode='a', sep='|', encoding='utf-8')

            # Contar registros procesados
            total_registros += len(chunk)
            print(f"Lote {i+1}: {len(chunk):,} registros procesados. Total hasta ahora: {total_registros:,}")

    # Calcular tiempo total
    tiempo_total = time.time() - start_time
    hora_finalizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Mensaje final
    print("\n=== RESULTADOS ===")
    print(f"Total de registros procesados: {total_registros:,}")
    print(f"Total de RUTs modificados: {modificados:,}")
    print(f"Tiempo total: {tiempo_total:.2f} segundos")
    print(f"Archivo generado en: {ruta_salida}")
    print(f"Proceso finalizado a las: {hora_finalizacion}")

# Ruta del archivo de entrada
ruta_txt = r"C:\Users\Alan\Desktop\millones50_para_postgresql.txt"

# Ejecutar procesamiento por bloques
procesar_ruts_duplicados_txt(ruta_txt)