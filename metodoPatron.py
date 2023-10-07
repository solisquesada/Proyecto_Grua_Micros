import Lectura
import Mapeos
import movimientosGrua
import Decodificador

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
        Error = 201 # Se define el código 201 como error por material
        return (Error)
    else:
        print ("\nSe ha suministrado la cantidad correcta de material :)")
        return (0)

def encontrarPosicion(matrizPatron, matrizSuministro):
    # Se recorre la matriz patrón
    matrizPosiciones = []
    matrizReacomodada = [] 
    for filaObjetivo in range(0, 5):
        for columnaObjetivo in range(0, 5):
            objeto = matrizPatron[filaObjetivo][columnaObjetivo]
            # Para los lugares donde hay un objeto en el patrón se encuentra cual objeto
            # del suministro puede cumplir.
            if (objeto != None):
                print("\nObjeto: " + str(objeto))
                # Se recorre la matriz suministro verificando que se trate de un material
                # que no se haya utilizado aún.

                for filaOrigen in range(5):
                    for columnaOrigen in range (5):
                        if (matrizSuministro[filaOrigen][columnaOrigen]==objeto):
                            print("Se encontró la ubicación ideal del objeto " + str(objeto) + " en: " + str(filaObjetivo+1) + "," + str(columnaObjetivo+1))
                            matrizSuministro[filaOrigen][columnaOrigen]=None
                            matrizPosiciones.append((objeto,filaOrigen,columnaOrigen,filaObjetivo,columnaObjetivo+5))# El +5 lo acomoda en la matriz de carga
                            break
    matrizReacomodada = Decodificador.traducirPosicionesPatron(matrizPosiciones)
    Lectura.imprimir_matriz(matrizReacomodada)
    print(matrizReacomodada)
    return (matrizReacomodada)

def AcomodarPatron(matrizPatron, matrizSuministro):
    #Se pide la matriz con el orden del suministrio y donde van ubicados los objetos.
    matrizPosiciones = encontrarPosicion(matrizPatron, matrizSuministro)
    movimientosGrua.gruaReal(matrizPosiciones)
    return matrizPosiciones

def metodoPatron():
    print("\nEmpezando el método patrón\n")
    # Se inicializa el error en 0.
    Error = 0
    
    # Se leen los datos proporcionados por el usuario en el excel dado:
    archivoPatron = "archivoPatron.xlsx"

    # Se realiza la lectura del excel con el patron que se desea realizar
    print("\nSe lee el patrón\n")
    matrizPatron, Error = Lectura.leerPatron(archivoPatron)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return
    
    # Se realiza el mapeo del área de suministro y del área de carga para asegurar
    # que se tiene el material adecuado y no hay basura.
    print("\nSe lee suministro\n")
    matrizSuministro = Mapeos.mapeoSuministro()

    print("\nSe lee carga\n")
    matrizCarga = Mapeos.mapeoCarga()
    
    # Se verifica que la cantidad de objetos necesarios sea igual a la cantidad suministrada:
    print("\nSe verifica la cantidad de material\n")
    Error = verificarCantidades(matrizPatron, matrizSuministro)
    if (Error != 0):
        print("ERROR: " + str(Error) + " INTENTELO MÁS TARDE.")
        return
    
    # Se procede a acomodar los materiales del suministro a la carga
    print("\nSe acomoda el material\n")
    matrizPosiciones = AcomodarPatron(matrizPatron, matrizSuministro)

    print("\nSe concluyó con éxito el método patrón :)")
    return matrizPosiciones

metodoPatron()