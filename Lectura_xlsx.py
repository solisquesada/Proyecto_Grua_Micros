import openpyxl

# La función leer_archivo se encarga de obtener información
# del excel. Como entrada se da el archivo donde el usuario
# ingresa el patrón y como salida se dan 2 matrices, una con
# la matriz que representa el patrón y otra con la matríz que
# representa el suministro.
def leer_archivo(archivo):
    try:
        # Se abre el archivo .xlsx
        workbook = openpyxl.load_workbook(archivo)
        sheet = workbook.active
    except FileNotFoundError:
        # En caso de no encontrarse el archivo se avisa al usuario 
        print(f"El archivo '{archivo}' no fue encontrado.")
        return

    # Se definen las matrizes a llenar
    matrizPatron = [[None for _ in range(5)] for _ in range(5)]
    matrizSuministro = [[None for _ in range(5)] for _ in range(5)]

    # Se estudia el patron dado por el usuario
    for fila in range(1, 5):
        for columna in range(1, 5):
            celda = sheet.cell(row=fila, column=columna).value
            if celda == "A":
                matrizPatron[fila-1][columna-1] = "A"
            elif celda == "B":
                matrizPatron[fila-1][columna-1] = "B"
            elif celda == "C":
                matrizPatron[fila-1][columna-1] = "C"
            else:
                matrizPatron[fila-1][columna-1] = None

    # Se estudia la matriz formada por el suministro
    for fila in range(1, 5):
        for columna in range(6, 11):
            celda = sheet.cell(row=fila, column=columna).value
            if celda == "A":
                matrizSuministro[fila-1][columna-6] = "A"
            elif celda == "B":
                matrizSuministro[fila-1][columna-6] = "B"
            elif celda == "C":
                matrizSuministro[fila-1][columna-6] = "C"
            else:
                matrizPatron[fila-1][columna-6] = None            

    # Para que esta función funcione, el archivo tiene que tener el formato dado
    # por nosotros en la plantilla de excel.
    return matrizPatron, matrizSuministro

def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)

if __name__ == "__main__":
    archivo = "archivo.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV
    matrizPatron, matrizSuministro = leer_archivo(archivo)
    imprimir_matriz(matrizPatron)
    imprimir_matriz(matrizSuministro)

