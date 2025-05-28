
def clean_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        print("Limpieza de archivo en curso...")
        for line in infile:
            cleaned_parts = [part.strip() for part in line.split('|')]
            cleaned_line = '|'.join(cleaned_parts)
            outfile.write(cleaned_line + '\n')
print("Limpieza de archivo finalizada.")


input_path = 'C:/Users/Alan/Desktop/millones50.txt' 
output_path = 'C:/Users/Alan/Desktop/millones50_cleaned.txt'  




clean_file(input_path, output_path)
print("Archivo limpio guardado.")