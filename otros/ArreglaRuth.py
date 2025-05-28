import os
import pandas as pd

def procesar_ruts_duplicados_windows():
    #rutas
    escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
    archivo_entrada = os.path.join(escritorio, 'diezmil_formateado.csv')
    archivo_salida = os.path.join(escritorio, 'diezmil_sin_duplicados.csv')
    
    # lee archivo CSV
    try:
        df = pd.read_csv(archivo_entrada, header=None, 
                        names=['rut', 'nombre', 'edad', 'direccion'], 
                        dtype=str, sep=',')
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return
    
    # procesar duplicados
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
    
    # guardar el resultado
    try:
        df.to_csv(archivo_salida, index=False, header=False)
        print("Proceso completado con éxito!")
        print(f"- Archivo original: {archivo_entrada}")
        print(f"- Archivo procesado: {archivo_salida}")
        print(f"- Total registros: {len(df)}")
        print(f"- RUTs modificados: {modificados}")
    except Exception as e:
        print(f"Error guardando el archivo: {e}")


if __name__ == "__main__":
    print("Iniciando procesamiento de RUTs duplicados...")
    procesar_ruts_duplicados_windows()
    input("Presiona Enter para salir...")





