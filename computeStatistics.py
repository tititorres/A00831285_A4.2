"""Módulo para calcular métricas estadísticas básicas a partir de múltiples archivos."""
import sys
import time

def compute_statistics(numbers):
    """Calcula estadísticas básicas a partir de una lista de números."""
    if not numbers:
        return None

    mean = sum(numbers) / len(numbers)
    sorted_numbers = sorted(numbers)
    mid = len(sorted_numbers) // 2
    median = (sorted_numbers[mid] if len(sorted_numbers) % 2 != 0
              else (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2)
    mode = max(set(numbers), key=numbers.count)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    std_dev = variance ** 0.5

    return {
        "media": mean,
        "mediana": median,
        "moda": mode,
        "varianza": variance,
        "desviación estándar": std_dev
    }

def process_file(filename):
    """
    Lee un archivo, extrae los números y calcula las estadísticas.
    Devuelve una tupla con el nombre base (sin extensión), el conteo de datos,
    las estadísticas calculadas, los errores y el tiempo de ejecución.
    """
    numbers = []
    errors = []
    start_time = time.time()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    numbers.append(float(line.strip()))
                except ValueError:
                    errors.append(f"Datos inválidos en {filename}: {line.strip()}")
    except FileNotFoundError:
        error_msg = f"Error: Archivo '{filename}' no encontrado."
        print(error_msg)
        return filename.rstrip('.txt'), 0, None, [error_msg], 0.0

    count = len(numbers)
    results = compute_statistics(numbers)
    elapsed_time = time.time() - start_time

    # Extraer la base del nombre del archivo (sin la extensión .txt)
    if filename.lower().endswith('.txt'):
        base_name = filename[:-4]
    else:
        base_name = filename

    return base_name, count, results, errors, elapsed_time

def generate_table(results_list):
    """
    Genera una tabla (lista de cadenas) con la métricas estadísticas para cada archivo.
    La tabla tendrá una fila para el encabezado y una fila para cada métrica.
    """

    # Extraer las cabeceras (nombre base de cada archivo)
    headers = ["TC"] + [item["base"] for item in results_list]

    # Inicializa la tabla con la cabecera
    table = ["\t".join(headers)]

    # Prepara cada métrica por fila
    # Para cada archivo, si results es None (no hay datos válidos), se mostrará "#N/A"
    count_row = ["COUNT"] + [str(item["count"]) if item["count"] > 0 else "#N/A"
                               for item in results_list]
    mean_row = ["MEAN"]
    median_row = ["MEDIAN"]
    mode_row = ["MODE"]
    sd_row = ["SD"]
    variance_row = ["VARIANCE"]

    for item in results_list:
        stats = item["stats"]
        if stats is None:
            # Sin datos válidos, se usa "#N/A" en cada campo
            mean_row.append("#N/A")
            median_row.append("#N/A")
            mode_row.append("#N/A")
            sd_row.append("#N/A")
            variance_row.append("#N/A")
        else:
            # Convertir cada valor a cadena; puedes ajustar el formato si lo deseas.
            mean_row.append(str(stats["media"]))
            median_row.append(str(stats["mediana"]))
            mode_row.append(str(stats["moda"]))
            sd_row.append(str(stats["desviación estándar"]))
            variance_row.append(str(stats["varianza"]))

    table.append("\t".join(count_row))
    table.append("\t".join(mean_row))
    table.append("\t".join(median_row))
    table.append("\t".join(mode_row))
    table.append("\t".join(sd_row))
    table.append("\t".join(variance_row))

    return table

def write_combined_results(results_list):
    """
    Escribe en un único archivo los resultados de todos los archivos procesados en
    formato de tabla. Además, imprime la tabla en consola.
    """
    output_filename = "StatisticsResults.txt"
    table_lines = generate_table(results_list)
    with open(output_filename, "w", encoding='utf-8') as file:
        for line in table_lines:
            file.write(line + "\n")
            print(line)
    print(f"\nLos resultados se han guardado en: {output_filename}\n")

def main():
    """Función principal para gestionar el análisis de argumentos y el flujo de ejecución."""
    if len(sys.argv) < 2:
        print("Uso: python compute_statistics.py archivo1.txt [archivo2.txt ...]")
        sys.exit(1)

    filenames = sys.argv[1:]
    results_list = []

    # Procesar cada archivo y almacenar sus resultados en la lista.
    for filename in filenames:
        base_name, count, stats, errors, elapsed_time = process_file(filename)
        # Se muestran los errores (si los hubiera) para cada archivo en consola.
        if errors:
            print(f"\nErrores en el archivo {filename}:")
            for error in errors:
                print(error)
        # Almacenar la información relevante.
        results_list.append({
            "base": base_name,
            "count": count,
            "stats": stats,
            "time": elapsed_time,
            "errors": errors
        })

    # Escribir la tabla combinada en un único archivo.
    write_combined_results(results_list)

if __name__ == "__main__":
    main()
