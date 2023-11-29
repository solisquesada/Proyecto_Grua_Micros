import Decodificador
import mapeoCamara
import Lectura

def verificarCantidades(matrizPatron,matrizSuministro):
    ADisponible = 0
    BDisponible = 0
    CDisponible = 0
    
    # Se define la cantidad de objetos necesarios para el patron
    for filaPatron in range(5):
        for columnaPatron in range(5):
            objeto = matrizPatron[filaPatron][columnaPatron]
            if (objeto == 100):
                ADisponible = ADisponible + 1
            elif (objeto == 200):
                BDisponible = BDisponible + 1
            elif (objeto == 300):
                CDisponible = CDisponible + 1
    # Se repasa el material en el suministro para ver que
    # concuerde con el material necesario.
    for filaSuministro in range(5):
        for columnaSuministro in range(5):
            objeto = matrizSuministro[filaSuministro][columnaSuministro]
            if (objeto == 100):
                ADisponible = ADisponible - 1
            elif (objeto == 200):
                BDisponible = BDisponible - 1
            elif (objeto == 300):
                CDisponible = CDisponible - 1
    # Se verifica que el material sea exacto al cerrar en 0
    if (ADisponible != 0 or BDisponible != 0 or CDisponible != 0):
        print ("\nLa cantidad de materiales disponibles y necesitados no son iguales")
        if (ADisponible > 0 or BDisponible > 0 or CDisponible > 0):
            Error = 203 # Se define el código 203 como error por exceso de material
            return (Error)
        else:
            Error = 201 # Se define el código 201 como error por falta material
            return (Error)
    else:
        print ("\nSe ha suministrado la cantidad correcta de material :)")
        return (0)

def encontrarPosicion(matrizPatron, matrizSuministro):
    # Se recorre la matriz patrón
    matrizPosiciones = []
    for filaPatron in range(0, 5):
        for columnaPatron in range(0, 5):
            objeto = matrizPatron[filaPatron][columnaPatron]

            # Para los lugares donde hay un objeto en el patrón se encuentra cual objeto
            # del suministro puede cumplir.
            if (objeto != None):
                encontrado = False
                print("\nObjeto: " + str(objeto))
                # Se recorre la matriz suministro verificando que se trate de un material
                # que no se haya utilizado aún.
                # La bandera encontrado ayuda a hacer el break del segundo ciclo
                for filaSuministro in range(0, 5):
                    for columnaSuministro in range (0, 5):
                        if (matrizSuministro[filaSuministro][columnaSuministro]==objeto):
                            print("Se encontró la ubicación ideal del objeto " + str(objeto) + " en: " + str(filaPatron+1) + "," + str(columnaPatron+1) + 
                                  " desde: " + str(filaSuministro) + "," + str(columnaSuministro))
                            print((filaSuministro, columnaSuministro, filaPatron, columnaPatron+5))
                            # El objeto encontrado se sustituye por un None para no utilizarlo múltiples veces
                            matrizSuministro[filaSuministro][columnaSuministro] = None
                            # Se agregan las coordenadas a la matriz de posiciones
                            matrizPosiciones.append((filaSuministro, columnaSuministro, filaPatron, columnaPatron+5))# El +5 lo acomoda en la matriz de carga
                            encontrado = True
                            break
                    if (encontrado):
                        break
    
    # Se traducen las coordenadas a posiciones codificadas del 1-50
    matrizReacomodada = Decodificador.traducirPosicionesPatron(matrizPosiciones)
    # Se traducen los origenes y destinos codificados a pasos
    matrizMovimientos = Decodificador.traducirPosicionesPasos(matrizReacomodada)
    print("Matriz codificada")
    print(matrizReacomodada)
    print("Matriz movimientos")
    print(matrizMovimientos)
    return (matrizMovimientos)

def verificarCarga(matrizCarga):
    # Carga debería estar libre por lo que si se encuentra algo distinto a None, devuelve un código de error
    for fila in range(0, 5):
        for columna in range(0, 5):
            if (matrizCarga[fila][columna] != None):
                Error = 202     # Se define el error 202 como obtaculo en carga
                return Error
    return (0)

def vaciarBasura(matrizCarga):
    # Se define la casilla inicial para la basura. Solo son 10 espacios por lo que en y no se varía
    xBasura = 0
    yBasura = 6
    basura = []
    movimientosBasura = []
    # Por cada objeto en carga, se le asigna un lugar en la basura
    for fila in range(0, 5):
        for columna in range(0, 5):
            if (matrizCarga[fila][columna] != None):
                print("\nSe encontró basura en:")
                print(fila, columna + 6)
                basura.append((fila, columna+5, yBasura, xBasura))
                xBasura = xBasura + 1
    
    print(basura)
    # Se traducen las coordenadas a posiciones codificadas
    basura = Decodificador.traducirPosicionesPatron(basura)
    # Se traducen los origenes y destinos codificados a pasos
    movimientosBasura = Decodificador.traducirPosicionesPasos(basura)

    return(movimientosBasura)

def metodoPatron1(matrizPatron, matrizSuministro, matrizCarga):
    matrizSuministro2 = []
    for elemento in matrizSuministro:
        matrizSuministro2.append(elemento)
    print("ll")
    print(matrizSuministro2)
    
    
    matrizPosiciones = []
    print("\nEmpezando el método patrón\n")
    # Se inicializa el error en 0.
    Error = 0

    # Se leen los datos proporcionados por el usuario en el excel dado:
    # archivoPatron = "archivoPatron.xlsx"

    # Se realiza la lectura del excel con el patron que se desea realizar
    # print("\nSe lee el patrón\n")
    # matrizPatron, Error = Lectura.leerPatron(archivoPatron)
    # if (Error != 0):
        # print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        # return Error, matrizPosiciones
    
    # Se realiza el mapeo del área de suministro y del área de carga para asegurar
    # que se tiene el material adecuado y no hay basura.
    # print("\nSe lee suministro y carga\n")
    # matrizSuministro, matrizCarga = mapeoCamara.mapeo()
    
    # Se verifica que la zona de carga esté vacía:
    print("\nSe verifica la zona de carga\n")
    Error = verificarCarga(matrizCarga)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return Error, matrizPosiciones

    # Se verifica que la cantidad de objetos necesarios sea igual a la cantidad suministrada:
    print("\nSe verifica la cantidad de material\n")
    Error = verificarCantidades(matrizPatron, matrizSuministro)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return Error, matrizPosiciones
    
    # Se procede a acomodar los materiales del suministro a la carga
    matrizMovimientos = encontrarPosicion(matrizPatron, matrizSuministro)
    print("\nSe acomoda el material\n")
    # Error = AcomodarPatron(matrizMovimientos)
    # Se verifica que los movimientos se hicieron correctamente
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return Error, matrizPosiciones

    print("\nSe concluyó con éxito el método patrón :)")
    print(matrizSuministro)
    print(matrizMovimientos)
    return Error, matrizMovimientos
