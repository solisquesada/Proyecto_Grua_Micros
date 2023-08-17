import Lectura

def verificarCantidades(matrizPatron,matrizSuministro):
    ADisponible = 0
    BDisponible = 0
    CDisponible = 0
    # Se define la cantidad de objetos necesarios para el patron
    for fila in range(5):
        for columna in range(5):
            objeto = matrizPatron[fila][columna]
            if (objeto == "A"):
                ADisponible = ADisponible + 1
            elif (objeto == "B"):
                BDisponible = BDisponible + 1
            elif (objeto == "C"):
                CDisponible = CDisponible + 1
    # Se repasa el material en el suministro para ver que
    # concuerde con el material necesario.
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
    # Se define la matrizPosiciones como una matriz de tuplas que contienen los objetos
    # en el orden del suministro y la posición a la que hay que levar cada objeto.
    matrizPosiciones = [None for _ in range(25)]
    # Se recorre la matriz patrón
    for filaObjetivo in range(0, 5):
        for columnaObjetivo in range(0, 5):
            objeto = matrizPatron[filaObjetivo][columnaObjetivo]
            # Para los lugares donde hay un objeto en el patrón se encuentra cual objeto
            # del suministro puede cumplir.
            if (objeto != None):
                print("Objeto: " + objeto)
                # Se recorre la matriz suministro verificando que se trate de un material
                # que no se haya utilizado aún.
                for fila in range(25):
                    if (matrizSuministro[fila]==objeto and matrizPosiciones[fila]==None):
                        print("Se encontró la ubiación ideal del objeto en: ")
                        print(str(filaObjetivo+1))
                        print(str(columnaObjetivo+1))
                        matrizPosiciones[fila]=(objeto,filaObjetivo+1,columnaObjetivo+1)
                        break
    Lectura.imprimir_matriz(matrizPosiciones)
    return (matrizPosiciones)

def AcomodarPatron(matrizPatron, matrizSuministro):
    #Se pide la matriz con el orden del suministrio y donde van ubicados los objetos.
    matrizPosiciones = encontrarPosicion(matrizPatron, matrizSuministro)
    for fila in range (25):
        #Se recorre el suministro, agarrando cada objeto y llevandolo al lugar correcto.
        objeto=matrizSuministro[fila]
        if (objeto!=None):
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
