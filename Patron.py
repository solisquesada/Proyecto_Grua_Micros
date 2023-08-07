# Se importan las funciones para poder leer el excel
import Lectura_xlsx

def verificarCantidades(matrizPatron, matrizSuministro):
    ASuministro = 0
    BSuministro = 0
    CSuministro = 0
    Error = 0 # Se define 0 como que no hay error.
    # Se define la disponibilidad de cada material
    for fila in range(4):
        for columna in range(4):
            objeto = matrizSuministro[fila][columna]
            if (objeto == "A"):
                ASuministro = ASuministro + 1
            elif (objeto == "B"):
                BSuministro = BSuministro + 1
            elif (objeto == "C"):
                CSuministro = CSuministro + 1
    # Se define si el material basta para el patron deseado
    for fila in range(4):
        for columna in range(4):
            objeto = matrizPatron[fila][columna]
            if (objeto == "A"):
                ASuministro = ASuministro - 1
            elif (objeto == "B"):
                BSuministro = BSuministro - 1
            elif (objeto == "C"):
                CSuministro = CSuministro - 1
    # Se verifica que el material sea exacto al cerrar en 0
    if (ASuministro != 0 | BSuministro != 0 | CSuministro != 0):
        print ("La cantidad de materiales proporcionados y necesitados no son iguales")
        Error = 101 # Se define el código 101 como error por material
        return
    else:
        print ("Se ha suministrado la cantidad correcta de material :)")
        return

def Patron():
    error = 0 # Se inicializa el error en 0.
    archivo = "archivo.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV
    matrizPatron, matrizSuministro = Lectura_xlsx.leer_archivo(archivo)
    error = verificarCantidades(matrizPatron, matrizSuministro)

Patron()
