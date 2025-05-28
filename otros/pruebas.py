import re
import os
from datetime import datetime

def corregir_longitud_nombres():
    # Configuración de rutas
    escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
    archivo_entrada = os.path.join(escritorio, 'millones50.txt')
    archivo_salida = os.path.join(escritorio, 'millones50_para_postgresql.txt')
    log_file = os.path.join(escritorio, 'correccion_longitud.log')
    
    # Contadores
    stats = {
        'total': 0,
        'exactos': 0,
        'recortados': 0,
        'errores': 0
    }

    with open(archivo_entrada, 'r', encoding='utf-8') as entrada, \
         open(archivo_salida, 'w', encoding='utf-8') as salida, \
         open(log_file, 'w', encoding='utf-8') as log:
        
        log.write(f"Inicio: {datetime.now()}\n")
        
        for linea in entrada:
            stats['total'] += 1
            
            try:
                partes = linea.split('|')
                if len(partes) < 4:
                    raise ValueError("Formato incorrecto")
                
                # Procesar cada campo
                rut = re.sub(r'[^0-9]', '', partes[0].strip())[:10].zfill(10)
                nombre = partes[1].strip()[:50].ljust(50)  # Asegurar 50 caracteres
                edad = partes[2].strip()[:2].zfill(2)
                direccion = partes[3].strip()[:100].ljust(100)
                
                # Verificar si se recortó el nombre
                if len(partes[1].strip()) > 50:
                    stats['recortados'] += 1
                    log.write(f"Línea {stats['total']}: Nombre recortado\n")
                else:
                    stats['exactos'] += 1
                
                # Escribir línea corregida
                salida.write(f"{rut}|{nombre}|{edad}|{direccion}\n")
                
            except Exception as e:
                stats['errores'] += 1
                log.write(f"Error línea {stats['total']}: {str(e)}\n")
                continue
        
        # Resumen final
        log.write("\n=== RESUMEN ===\n")
        log.write(f"Total líneas: {stats['total']}\n")
        log.write(f"Nombres con longitud exacta: {stats['exactos']}\n")
        log.write(f"Nombres recortados: {stats['recortados']}\n")
        log.write(f"Errores: {stats['errores']}\n")
        log.write(f"Finalizado: {datetime.now()}\n")
    
    print(f"Proceso completado. Archivo listo para PostgreSQL: {archivo_salida}")
    print(f"Nombres recortados: {stats['recortados']}")

if __name__ == "__main__":
    corregir_longitud_nombres()