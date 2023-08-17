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
        return (Error)

def encontrarPosicion(matrizPatron, matrizSuministro):
    matrizPosiciones = [[None for _ in range(5)] for _ in range(5)]
    # Se seleccionan los objetos en el suministro uno por uno
    for fila in range(25):
            objeto = matrizSuministro[fila] # objeto es un string (A, B, C o None)
            if (objeto != None):
                for fila in range(1, 6):
                    for columna in range(1, 6):
                        if celda == "A":
                            matrizPatron[fila-1][columna-1] = "A"
                        elif celda == "B":
                            matrizPatron[fila-1][columna-1] = "B"
                        elif celda == "C":
                            matrizPatron[fila-1][columna-1] = "C"
                        else:
                            matrizPatron[fila-1][columna-1] = None
                #recogerObjeto()
                print("Se recoge el objeto del suministro")
                #dejarObjeto(filaObjetivo, columnaObjetivo)
                print("Se deja el objeto " + objeto + " en la posición: " + str(filaObjetivo) + str(columnaObjetivo))
    return

def AcomodarPatron(matrizPatron, matrizSuministro):
    # Se seleccionan los objetos en el suministro uno por uno
    for fila in range(25):
            objeto = matrizSuministro[fila] # objeto es un string (A, B, C o None)
            if (objeto != None):
                filaObjetivo, columnaObjetivo = encontrarPosicion(objeto)
                #recogerObjeto()
                print("Se recoge el objeto del suministro")
                #dejarObjeto(filaObjetivo, columnaObjetivo)
                print("Se deja el objeto " + objeto + " en la posición: " + str(filaObjetivo) + str(columnaObjetivo))
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
