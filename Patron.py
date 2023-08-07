# Se importan las funciones para poder leer el excel
import Lectura_xlsx

def verificarCantidades(matrizPatron, matrizSuministro, matrizCarga):
    ADisponible = 0
    BDisponible = 0
    CDisponible = 0
    Error = 0 # Se define 0 como que no hay error.
    # Se define la disponibilidad de cada material
    # Se analiza el material del suministro
    for fila in range(5):
        for columna in range(5):
            objeto = matrizSuministro[fila][columna]
            if (objeto == "A"):
                ADisponible = ADisponible + 1
            elif (objeto == "B"):
                BDisponible = BDisponible + 1
            elif (objeto == "C"):
                CDisponible = CDisponible + 1
    # Se analiza el material en la plataforma de carga
    for fila in range(5):
        for columna in range(5):
            objeto = matrizCarga[fila][columna]
            if (objeto == "A"):
                ADisponible = ADisponible + 1
            elif (objeto == "B"):
                BDisponible = BDisponible + 1
            elif (objeto == "C"):
                CDisponible = CDisponible + 1
    # Se define si el material basta para el patron deseado
    for fila in range(5):
        for columna in range(5):
            objeto = matrizPatron[fila][columna]
            if (objeto == "A"):
                ADisponible = ADisponible - 1
            elif (objeto == "B"):
                BDisponible = BDisponible - 1
            elif (objeto == "C"):
                CDisponible = CDisponible - 1
    # Se verifica que el material sea exacto al cerrar en 0
    if (ADisponible != 0 or BDisponible != 0 or CDisponible != 0):
        print ("La cantidad de materiales disponibles y necesitados no son iguales")
        Error = 201 # Se define el código 201 como error por material
        return (Error)
    else:
        print ("Se ha suministrado la cantidad correcta de material :)")
        return (Error)

def AcomodarPatron(matrizPatron, matrizSuministro, matrizCarga):
    ZonaBloqueada = 1 # Esta va a ser la señal que determina que la zona está libre
    if (ZonaBloqueada == 1):
        Error = 202 # Se define el error 202 para bloqueos en la zona
    return (Error)

def Patron():
    Error = 0 # Se inicializa el error en 0.
    archivo = "archivo.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV
    matrizPatron, matrizSuministro, matrizCarga, Error = Lectura_xlsx.leer_archivo(archivo)

    # Se verifica que la lectura haya sido correcta
    if (Error == 0):
        Error = verificarCantidades(matrizPatron, matrizSuministro, matrizCarga)
    else:
        print ("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return

    # Se verifica que la cantidad de material sea el adecuado
    if (Error == 0):
        #Se procede a acomodar el material de acuerdo al patron
        Error = AcomodarPatron(matrizPatron, matrizSuministro, matrizCarga)
        if (Error == 0):
            return
        else:
            print ("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
            return
    else:
        print ("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return

Patron()
