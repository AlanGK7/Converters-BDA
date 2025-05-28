import pandas as pd
import time
from datetime import datetime
import os

def formatear_persona(rut, nombre, edad, direccion):
    """Formatea cada campo de la persona según las reglas definidas."""
    rut = str(rut).strip().zfill(10) if len(str(rut).strip()) <= 10 else str(rut).strip()[:10]
    nombre = str(nombre).strip().ljust(50)[:50]
    edad = str(edad).strip().zfill(2) if len(str(edad).strip()) <= 2 else str(edad).strip()[:2]
    direccion = str(direccion).strip().ljust(100)[:100]
    
    return [rut, nombre, edad, direccion]

def procesar_archivo_por_bloques(ruta_txt, chunk_size=1_000_000):
    """Procesa el archivo en bloques de 1 millón de registros para optimizar el rendimiento."""
    
    
    start_time = time.time()
    total_registros = 0


    ruta_txt_salida = ruta_txt.replace(".txt", "_formateado.txt")


    if os.path.exists(ruta_txt_salida):
        os.remove(ruta_txt_salida)

    
    with open(ruta_txt_salida, 'w') as salida:
        for i, chunk in enumerate(pd.read_csv(ruta_txt, sep=r"\|", engine="python", header=None, dtype=str, chunksize=chunk_size)):
            
           
            chunk = chunk.apply(lambda row: formatear_persona(row[0], row[1], row[2], row[3]), axis=1, result_type='expand')

            for index, row in chunk.iterrows():
                salida.write('|'.join(row.astype(str)) + '\n')

           
            total_registros += len(chunk)
            print(f"Lote {i+1}: {len(chunk):,} registros procesados. Total hasta ahora: {total_registros:,}")

   
    tiempo_total = time.time() - start_time
    hora_finalizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    
    print("\n=== RESULTADOS ===")
    print(f"Total de registros procesados: {total_registros:,}")
    print(f"Tiempo total: {tiempo_total:.2f} segundos")
    print(f"Archivo generado en: {ruta_txt_salida}")
    print(f"Proceso finalizado a las: {hora_finalizacion}")


ruta_txt = r"C:\Users\Alan\Desktop\millones50.txt"

procesar_archivo_por_bloques(ruta_txt)
