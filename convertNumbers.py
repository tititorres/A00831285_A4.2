"""
convert_numbers.py

Este programa lee múltiples archivos que contienen números, los convierte a binario y hexadecimal,
y escribe los resultados en un archivo llamado ConvertionResults.txt. Maneja datos inválidos y
muestra el tiempo transcurrido de la ejecución.
"""

import sys
import time
import os


def decimal_to_binary(number):
    """Convierte un número decimal a binario usando un algoritmo básico."""
    if number == 0:
        return "0"
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number = number // 2
    return binary


def decimal_to_hexadecimal(number):
    """Convierte un número decimal a hexadecimal usando un algoritmo básico."""
    if number == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    while number > 0:
        remainder = number % 16
        hexadecimal = hex_chars[remainder] + hexadecimal
        number = number // 16
    return hexadecimal


def process_file(file_path):
    """Procesa el archivo, convierte los números y maneja errores."""
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                number = int(line.strip())
                binary = decimal_to_binary(number)
                hexadecimal = decimal_to_hexadecimal(number)
                results.append((line_number, number, binary, hexadecimal))
            except ValueError:
                print(
                    f"Error: Datos inválidos en la línea {line_number} del archivo '{file_path}' - "
                    f"'{line.strip()}'. Se omitirá esta línea."
                )
    return results


def write_results(all_results, elapsed_time):
    """Escribe los resultados en la consola y en el archivo de salida."""
    with open("ConvertionResults.txt", 'w', encoding='utf-8') as output_file:
        # Escribir encabezado
        header = "ÍTEM\tNúmero\tArchivo\tBIN\tHEX"
        print(header)
        output_file.write(header + "\n")

        # Escribir resultados para cada archivo
        for file_results in all_results:
            file_name = file_results["file_name"]
            results = file_results["results"]
            for item in results:
                line = f"{item[0]}\t{item[1]}\t{file_name}\t{item[2]}\t{item[3]}"
                print(line)
                output_file.write(line + "\n")

        # Escribir el tiempo transcurrido
        time_info = f"Tiempo transcurrido: {elapsed_time:.6f} segundos"
        print(time_info)
        output_file.write(time_info + "\n")


def main():
    """Función principal para manejar la ejecución del programa."""
    if len(sys.argv) < 2:
        print("Uso: python convert_numbers.py archivo1.txt archivo2.txt ...")
        sys.exit(1)

    start_time = time.time()
    all_results = []

    for file_path in sys.argv[1:]:
        try:
            # Extraer el nombre del archivo sin la extensión
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            results = process_file(file_path)
            all_results.append({"file_name": file_name, "results": results})
        except FileNotFoundError:
            print(f"Error: Archivo '{file_path}' no encontrado. Se omitirá este archivo.")

    elapsed_time = time.time() - start_time
    write_results(all_results, elapsed_time)


if __name__ == "__main__":
    main()
