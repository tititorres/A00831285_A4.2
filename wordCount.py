"""
Este programa procesa archivos de texto y cuenta la frecuencia de las palabras en cada archivo.
Los resultados se muestran en consola y se guardan en un archivo de salida.
"""

import sys
import time


def process_line(line):
    """
    Procesa una línea, dividiéndola en palabras y eliminando caracteres no alfabéticos.

    Args:
        line (str): Línea de texto a procesar.

    Returns:
        list: Lista de palabras procesadas (en minúsculas y sin caracteres no alfabéticos).
    """
    words = line.split()
    processed_words = []
    for word in words:
        cleaned_word = "".join([char for char in word if char.isalpha()]).lower()
        if cleaned_word:
            processed_words.append(cleaned_word)
    return processed_words


def count_words(filename):
    """
    Cuenta la frecuencia de las palabras en un archivo.

    Args:
        filename (str): Nombre del archivo a procesar.

    Returns:
        dict: Diccionario con la frecuencia de las palabras.
    """
    word_count = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                words = process_line(line)
                for word in words:
                    word_count[word] = word_count.get(word, 0) + 1
    except FileNotFoundError as file_error:
        print(f"Error al abrir el archivo {filename}: {file_error}")
        return None
    return word_count


def save_results(results, time_elapsed):
    """
    Guarda los resultados de la cuenta de palabras en un archivo.

    Args:
        results (dict): Diccionario con los resultados de la cuenta de palabras por archivo.
        time_elapsed (float): Tiempo transcurrido durante la ejecución.
    """
    try:
        with open("word_count_results.txt", "w", encoding="utf-8") as result_file:
            result_file.write("Word Count Results:\n")
            for filename, word_count in results.items():
                result_file.write(f"\nResultados para {filename}:\n")
                if word_count:
                    for word, count in word_count.items():
                        result_file.write(f"{word}: {count}\n")
                else:
                    result_file.write("Error procesando el archivo.\n")
            result_file.write(
                f"\nTiempo transcurrido: {time_elapsed:.2f} segundos\n"
            )
    except IOError as io_error:
        print(f"Error guardando los resultados en archivo: {io_error}")


def main():
    """
    Función que procesa los archivos proporcionados y calcula la frecuencia de las palabras.
    Los resultados se imprimen en consola y se guardan en un archivo.
    """
    if len(sys.argv) < 2:
        print("Uso: python word_count.py <archivo1> <archivo2> ...")
        sys.exit(1)

    filenames = sys.argv[1:]
    results = {}
    start_time = time.time()

    for filename in filenames:
        results[filename] = count_words(filename)

    end_time = time.time()
    time_elapsed = end_time - start_time

    print("Resultados de la cuenta de palabras:")
    for filename, word_count in results.items():
        print(f"\nResultados para {filename}:")
        if word_count:
            for word, count in word_count.items():
                print(f"{word}: {count}")
        else:
            print("Error procesando el archivo.")
    print(f"\nTiempo transcurrido: {time_elapsed:.2f} segundos")
    save_results(results, time_elapsed)


if __name__ == "__main__":
    main()
