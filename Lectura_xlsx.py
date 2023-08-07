import openpyxl

# La función leer_archivo se encarga de obtener información
# del excel. Como entrada se da el archivo donde el usuario
# ingresa el patrón y como salida se dan 2 matrices, una con
# la matriz que representa el patrón y otra con la matríz que
# representa el suministro.
def leer_archivo(archivo):
    Error = 0 # Se empieza el error en 0
    # Se definen las matrizes a llenar
    matrizPatron = [[None for _ in range(5)] for _ in range(5)]
    matrizSuministro = [[None for _ in range(5)] for _ in range(5)]
    matrizCarga = [[None for _ in range(5)] for _ in range(5)]

    try:
        # Se abre el archivo .xlsx
        workbook = openpyxl.load_workbook(archivo)
        sheet = workbook.active
    except FileNotFoundError:
        # En caso de no encontrarse el archivo se avisa al usuario
        Error = 101 # Se define el error 101 como error por no archivo
        print(f"El archivo '{archivo}' no fue encontrado.")
        return (matrizPatron, matrizSuministro, matrizCarga, Error)
    except PermissionError:
        # En caso de no tener permisos al archivo avisa al usuario
        Error = 102 # Se define el error 102 como error por archivo bloqueado
        print(f"El archivo '{archivo}' está bloqueado.")
        return (matrizPatron, matrizSuministro, matrizCarga, Error)

    # Se estudia el estado del patron dado por el usuario
    for fila in range(1, 6):
        for columna in range(1, 6):
            celda = sheet.cell(row=fila, column=columna).value
            if celda == "A":
                matrizPatron[fila-1][columna-1] = "A"
            elif celda == "B":
                matrizPatron[fila-1][columna-1] = "B"
            elif celda == "C":
                matrizPatron[fila-1][columna-1] = "C"
            else:
                matrizPatron[fila-1][columna-1] = None

    # Se estudia el estado de la matriz formada por el suministro
    for fila in range(1, 6):
        for columna in range(6, 11):
            celda = sheet.cell(row=fila, column=columna).value
            if celda == "A":
                matrizSuministro[fila-1][columna-6] = "A"
            elif celda == "B":
                matrizSuministro[fila-1][columna-6] = "B"
            elif celda == "C":
                matrizSuministro[fila-1][columna-6] = "C"
            else:
                matrizSuministro[fila-1][columna-6] = None            

    # Se estudia el estado de la matriz de carga
    for fila in range(1, 6):
        for columna in range(11, 16):
            celda = sheet.cell(row=fila, column=columna).value
            if celda == "A":
                matrizCarga[fila-1][columna-11] = "A"
            elif celda == "B":
                matrizCarga[fila-1][columna-11] = "B"
            elif celda == "C":
                matrizCarga[fila-1][columna-11] = "C"
            else:
                matrizCarga[fila-1][columna-11] = None  

    # Para que esta función funcione, el archivo tiene que tener el formato dado
    # por nosotros en la plantilla de excel.
    return (matrizPatron, matrizSuministro, matrizCarga, Error)

def imprimir_matriz(matriz):
    print ("\nIMPRIMIENNDO MATRIZ:\n")
    for fila in matriz:
        print(fila)

if __name__ == "__main__":
    archivo = "archivo.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV
    matrizPatron, matrizSuministro, matrizCarga, Error = leer_archivo(archivo)
    imprimir_matriz(matrizPatron)
    imprimir_matriz(matrizSuministro)
    imprimir_matriz(matrizCarga)

