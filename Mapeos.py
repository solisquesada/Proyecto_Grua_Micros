import Lectura
import movimientosGrua

def mapeoSuministro():
    # Se llama a la función que mueve y controla la grua para que realice
    # la lectura de objetos en cada una de las posiciones del suministro

    # Se define la matriz suministro
    matrizSuministro = [[None for _ in range(5)] for _ in range(5)]
    # Se lee el resto de la matriz
    print("\nMapeando zona de suministro")
    for fila in range(5):
        for columna in range(5):
            if (fila==0 and columna==0):
                print("Se lee: " + str(fila) + str(columna))
            else:
                print("Se lee: " + str(fila) + str(columna))
    
    matrizSuministro=Lectura.leerSuministro("archivoSuministro.xlsx") #De momento se va a definir la matriz sumistro con un excel
    Lectura.imprimir_matriz(matrizSuministro)

    movimientosGrua.grua((5,5),(0,0),0)

    return (matrizSuministro)

def mapeoCarga():
    # Se llama a la función que mueve y controla la grua para que realice
    # la lectura de objetos en cada una de las posiciones de la carga

    # Se define la matriz carga
    matrizCarga = [[None for _ in range(5)] for _ in range(5)]
    # Se lee el resto de la matriz
    print("\nMapeando zona de carga")
    for fila in range(5):
        for columna in range(5):
            if (fila==0 and columna==0):
                print("Se lee: " + str(fila) + str(columna))
            else:
                print("Se lee: " + str(fila) + str(columna))
    
    matrizCarga=[[None for _ in range(5)] for _ in range(5)] #De momento se va define manualmente la matriz carga
    Lectura.imprimir_matriz(matrizCarga)

    movimientosGrua.grua((9,9),(0,0),0)

    return (matrizCarga)
