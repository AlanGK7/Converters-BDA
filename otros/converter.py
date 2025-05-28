import pandas as pd

ruta_txt = "C:\\Users\\Alan\\Desktop\\millones50-Copia.text"

df = pd.read_csv(ruta_txt, sep=r"\|", engine="python", header=None)
ruta_csv = ruta_txt.replace(".txt", ".csv")

df.to_csv(ruta_csv, index=False, header=False)

print(f"Archivo convertido con éxito: {ruta_csv}")
