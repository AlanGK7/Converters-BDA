with open("C:/Users/Alan/Desktop/millones50_cleaned.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

ruts_unicos = set()
lines_filtradas = []
print("Eliminando duplicados...")
for line in lines:
    rut = line.split("|")[0] 
    if rut not in ruts_unicos:
        ruts_unicos.add(rut)
        lines_filtradas.append(line)

with open("C:/Users/Alan/Desktop/millones58_sinrepetidos_corregido.txt", "w", encoding="utf-8") as file:
    file.writelines(lines_filtradas)

print("Archivo guardado")

