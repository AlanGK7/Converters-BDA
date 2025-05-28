import os
import pandas as pd

def procesar_ruts_duplicados_txt():
    # Rutas - ahora con extensión .txt
    escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
    archivo_entrada = os.path.join(escritorio, 'millones50_para_postgresql.txt')
    archivo_salida = os.path.join(escritorio, '50m_sinDuplicados.txt')
    
    # Lee archivo TXT (asumiendo formato separado por comas)
    try:
        df = pd.read_csv(archivo_entrada, header=None, 
                        names=['rut', 'nombre', 'edad', 'direccion'], 
                        dtype=str, sep=',')  # Puedes cambiar el separador si es necesario
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return
    
    # Procesar duplicados (igual que antes)
    rut_counts = {}
    modificados = 0
    
    for index, row in df.iterrows():
        rut = str(row['rut']).strip().zfill(10)  # asegurar 10 dígitos
        
        if rut in rut_counts:
            # modificar el último dígito a 0
            nuevo_rut = rut[:-1] + '0'
            df.at[index, 'rut'] = nuevo_rut
            modificados += 1
            rut_counts[nuevo_rut] = 1  # registrar el nuevo RUT modificado
        else:
            rut_counts[rut] = 1
    
    # Guardar el resultado como TXT
    try:
        # Guardar como TXT con el mismo formato de entrada
        df.to_csv(archivo_salida, index=False, header=False, sep=',')
        print("Proceso completado con éxito!")
        print(f"- Archivo original: {archivo_entrada}")
        print(f"- Archivo procesado: {archivo_salida}")
        print(f"- Total registros: {len(df)}")
        print(f"- RUTs modificados: {modificados}")
    except Exception as e:
        print(f"Error guardando el archivo: {e}")


if __name__ == "__main__":
    print("Iniciando procesamiento de RUTs duplicados (TXT)...")
    procesar_ruts_duplicados_txt()
    input("Presiona Enter para salir...")