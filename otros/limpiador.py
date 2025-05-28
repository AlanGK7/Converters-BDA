import pandas as pd


def formatear_persona(rut, nombre, edad, direccion):
    
    rut = str(rut).strip().zfill(10) if len(str(rut).strip()) <= 10 else str(rut).strip()[:10]
    nombre = str(nombre).strip().ljust(50)[:50]
    edad = str(edad).strip().zfill(2) if len(str(edad).strip()) <= 2 else str(edad).strip()[:2]
    direccion = str(direccion).strip().ljust(100)[:100]
    
    return [rut, nombre, edad, direccion]


ruta_txt = r"C:\Users\Alan\Desktop\diezmil.txt"
df = pd.read_csv(ruta_txt, sep=r"\|", engine="python", header=None, dtype=str)
df = df.apply(lambda row: formatear_persona(row[0], row[1], row[2], row[3]), axis=1, result_type='expand')
ruta_csv = ruta_txt.replace(".txt", "_formateado.csv")
df.to_csv(ruta_csv, index=False, header=False)

print(f"Archivo CSV formateado correctamente: {ruta_csv}")

