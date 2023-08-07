import openpyxl

def leer_archivo(archivo):
    try:
        workbook = openpyxl.load_workbook(archivo)
        sheet = workbook.active
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado.")
        return

    matriz = [[None for _ in range(5)] for _ in range(5)]
    objetos2_a = []
    objetos2_b = []
    objetos2_c = []
    celdas_sobrantes = []

    for fila in range(1, 6):
        for columna in range(1, 6):
            celda = sheet.cell(row=fila, column=columna).value

            if celda == "A":
                matriz[fila-1][columna-1] = "A"
                objetos2_a.append((fila, columna))
            elif celda == "B":
                matriz[fila-1][columna-1] = "B"
                objetos2_b.append((fila, columna))
            elif celda == "C":
                matriz[fila-1][columna-1] = "C"
                objetos2_c.append((fila, columna))
            else:
                celdas_sobrantes.append((fila,columna))
                matriz[fila-1][columna-1] = None

    return matriz, objetos2_a, objetos2_b, objetos2_c, celdas_sobrantes

def distribuir_cajas(matriz, objetos2_a, objetos2_b, objetos2_c):
    # Aquí deberías implementar la lógica para distribuir las cajas en la matriz.
    # Puedes utilizar algoritmos de planificación o técnicas heurísticas para
    # ubicar las cajas en las posiciones especificadas en los arrays de objetos2_a, objetos2_b y objetos2_c.

    # Ejemplo de una distribución simple para ilustrar:
    for fila in range(5):
        for columna in range(5):
            if matriz[fila][columna] is None:
                if objetos2_a:
                    matriz[fila][columna] = "A"
                    objetos2_a.pop(0)
                elif objetos2_b:
                    matriz[fila][columna] = "B"
                    objetos2_b.pop(0)
                elif objetos2_c:
                    matriz[fila][columna] = "C"
                    objetos2_c.pop(0)

    return matriz

def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)

if __name__ == "__main__":
    archivo = "Matriz.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV

    matriz2, objetos2_a, objetos2_b, objetos2_c, celdas_sobrantes = leer_archivo(archivo)
    #matriz_distribuida = distribuir_cajas(matriz, objetos2_a, objetos2_b, objetos2_c)
    imprimir_matriz(matriz2)
    print("Objetos A:", objetos2_a)
    print("Objetos B:", objetos2_b)
    print("Objetos C:", objetos2_c)
    print("Celdas sobrantes:", celdas_sobrantes)
