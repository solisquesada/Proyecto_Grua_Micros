import Lectura

def verificarCantidades(matrizPatron,matrizSuministro):
    ADisponible = 0
    BDisponible = 0
    CDisponible = 0
    # Se define la disponibilidad de cada material
    # Se analiza el material del suministro
    for fila in range(5):
        for columna in range(5):
            objeto = matrizPatron[fila][columna]
            if (objeto == "A"):
                ADisponible = ADisponible + 1
            elif (objeto == "B"):
                BDisponible = BDisponible + 1
            elif (objeto == "C"):
                CDisponible = CDisponible + 1
    # Se analiza el material en la plataforma de carga
    for fila in range(25):
            objeto = matrizSuministro[fila]
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
        return (0)

def encontrarPosicion(matrizPatron, matrizSuministro):
    matrizPosiciones = [None for _ in range(25)]
    for filaObjetivo in range(0, 5):
        for columnaObjetivo in range(0, 5):
            objeto = matrizPatron[filaObjetivo][columnaObjetivo]
            if (objeto != None):
                print("Objeto: " + objeto)
                for fila in range(25):
                    print("Revisando la fila " + str(fila+1) + " de la matriz suministro")
                    if (matrizSuministro[fila]==objeto and matrizPosiciones[fila]==None):
                        print("Se encontró el objeto")
                        print(filaObjetivo)
                        print(columnaObjetivo)
                        matrizPosiciones[fila]=(objeto,filaObjetivo,columnaObjetivo)
                        break
    Lectura.imprimir_matriz(matrizPosiciones)
    return (matrizPosiciones)

def AcomodarPatron(matrizPatron, matrizSuministro):
    matrizPosiciones = encontrarPosicion(matrizPatron, matrizSuministro)
    for fila in range (25):
        objeto=matrizSuministro[fila]
        #recogerObjeto()
        print("Se recoge el objeto del suministro")
        #dejarObjeto(filaObjetivo, columnaObjetivo)
        print("Se deja el objeto " + str(matrizPosiciones[fila]))
    return

def meteodoPatron():
    # Se inicializa el error en 0.
    Error = 0 
    
    # Se leen los datos proporcionados por el usuario:
    archivoPatron = "archivoPatron.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV
    archivoSuministro = "archivoSuministro.xlsx"  # Reemplaza con la ruta a tu archivo XLSX o CSV
    matrizPatron, Error = Lectura.leerPatron(archivoPatron)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return
    matrizSuministro, Error = Lectura.leerSuministro(archivoSuministro)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return
    
    # Se verifica que la cantidad de objetos necesarios sea igual a la cantidad suministrada:
    Error = verificarCantidades(matrizPatron, matrizSuministro)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return
    AcomodarPatron(matrizPatron, matrizSuministro)
    print("Se concluyó con éxito el método patrón :)")
    # Se procede a acomodar los objetos en su lugar respectivo:

meteodoPatron()
