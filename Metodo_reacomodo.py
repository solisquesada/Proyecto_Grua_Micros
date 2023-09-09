import Lectura

# Logica del codigo
# COMPARA PATRON Y ACTUAL -> INDICA CUALES ESTAN MAL COLOCADAS (LAS CORRECTAS NO LAS MUEVE)
# -> LAS ENVIA A SUMINISTRO EN LA POSICION CORRESPONDIENTE A (x = PATRON, y = PATRON+5)
# -> LUEGO LAS COLOCA DONDE DEBEN IR EN CARGA (PATRON)


archivoPatron = "archivoPatron.xlsx" #Archivo debe recibir el nombre de la interfaz o saberlo de alguna forma
patron, Error = Lectura.leerPatron(archivoPatron) #El error no se usa en reacomodo pero no afecta

# Actual es una matriz que viene de la función de mapeos, pero eso no esta hasta que este la camara
# por eso se trabaja con matriz fija
actual = [
    [100, None, 200, 300, 100],
    [200, None, 100, 200, None],
    [300, None, None, None, None],
    [100, 100, 300, None, 100],
    [None, None, 100, None, 300]
]



# La idea del reacomodo

# Compara matriz de patron y la del mapeo y devuelve un diccionario con las posiciones
# correctas e incorrecta

# OJO: ES VITAL QUE PATRON Y ACTUAL TENGAN LA MISMA CANTIDAD DE OBJETOS PARA CADA TIPO,
# es decir si hay 3 A, 3 B y 4 C deben haber la misma cantidad en patron y actual.
def comparar_matrices(patron, actual):
    objetos = [100, 200, 300]
    correctas = {obj: [] for obj in objetos}
    incorrectas = {obj: [] for obj in objetos}
    none_values = []
    #Se recorre la matriz de patron y actual y se comparan objetos para saber los
    #que no se deben mover (Porque ya estan bien colocados) y los que si hay que mover

    for i in range(5):
        for j in range(5):
            if patron[i][j] is None:
                none_values.append((i, j))
            elif patron[i][j] == actual[i][j]:
                correctas[patron[i][j]].append((i, j))
            else:
                incorrectas[patron[i][j]].append((i, j))

    return correctas, incorrectas

# Este se usa para obtener las posiciones de los objetos A,B,C en
# patron y posiciones de inicio (actuales)
def recopilar_posiciones(matriz):
    objetos = [100, 200, 300]
    posiciones = {obj: [] for obj in objetos}
    posiciones[None] = []

    for i in range(5):
        for j in range(5):
            objeto = matriz[i][j]
            if objeto is not None:
                posiciones[objeto].append((i, j))
            else:
                posiciones[None].append((i, j))

    return posiciones


# Ejemplo de uso



#Estas son diccionario con A,B,C
correctas, incorrectas = comparar_matrices(patron, actual)
#imprimir_vectores(correctas, incorrectas)

# Ahora obtiene posiciones de actual y patron como diccionario
posiciones_actuales = recopilar_posiciones(actual)
posiciones_patrones = recopilar_posiciones(patron)

# Posiciones que corresponden en patron y mapeo
correctas_A = correctas[100]
correctas_B = correctas[200]
correctas_C = correctas[300]

# Todas las posiciones actuales para cada tipo de objeto (del mapeo)
actuales_A = posiciones_actuales[100]
actuales_B = posiciones_actuales[200]
actuales_C = posiciones_actuales[300]

#Todas las posiciones segun objeto de matriz
posicion_patron_A = posiciones_patrones[100]
posicion_patron_B = posiciones_patrones[200]
posicion_patron_C = posiciones_patrones[300]


# Esta funcion permite comparar las correctas con el patron y actuales
# Para saber donde estan los que hay que llevar (actuales)
# y a donde van (patron)

def generar_nuevo_vector(correctas, actual):
    nuevo_vector = []
    for objeto in actual:
        if objeto not in correctas:
            nuevo_vector.append(objeto)

    return nuevo_vector

#Esta correccion de coordenadas son para saber a donde se llevan a suministro
def correccion_coordenadas(posiciones_a_corregir):
    nuevo_vector = []

    for objeto in posiciones_a_corregir:
        nuevo_x = objeto[0] + 0
        nuevo_y = objeto[1] + 5
        nuevo_vector.append((nuevo_x, nuevo_y))

    return nuevo_vector


def convertir_a_numeros(vector):
    matriz_referencia = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
        [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    ]

    numeros_codificados = []

    for tupla in vector:
        fila, columna = tupla
        if 0 <= fila < 5 and 0 <= columna < 10:
            numero = matriz_referencia[fila][columna]
            numeros_codificados.append(numero)

    return numeros_codificados

def combinar_vectores(vector1, vector2, tipo_de_dato):
    if tipo_de_dato not in [100, 200, 300]:
        raise ValueError("El tipo_de_dato debe ser 100, 200 o 300")

    vector_global = []

    for val1, val2 in zip(vector1, vector2):
        vector_global.append(tipo_de_dato)
        vector_global.append(val1)
        vector_global.append(val2)


    return vector_global

def combinar_seis_vectores(vectores):
    vector_combinado = []
    for vector in vectores:
        vector_combinado.extend(vector)
    return vector_combinado



#PRINTS PARA FACILITAR ANALISIS
print("Objeto A:")
para_mover_A = generar_nuevo_vector(correctas_A, actuales_A)
print("Las que hay que mover estan en las posiciones:", para_mover_A)
codificados_para_mover_A = convertir_a_numeros(para_mover_A)
print("Se codifican como:", codificados_para_mover_A)

posiciones_a_mover_A = generar_nuevo_vector(correctas_A, posicion_patron_A)
posiciones_a_mover_A_suministro = correccion_coordenadas(posiciones_a_mover_A)
print("Se llevan a:", posiciones_a_mover_A_suministro)
codificados_hacia_suministro_A = convertir_a_numeros(posiciones_a_mover_A_suministro)
print("Se codifican como:", codificados_hacia_suministro_A)
print("Luego se llevan a la matriz de descarga a pos:", posiciones_a_mover_A)
codificados_hacia_carga_A = convertir_a_numeros(posiciones_a_mover_A)
print("Se codifican como:", codificados_hacia_carga_A)


print("Objeto B:")
para_mover_B = generar_nuevo_vector(correctas_B, actuales_B)
print("Las que hay que mover están en las posiciones:", para_mover_B)
codificados_para_mover_B = convertir_a_numeros(para_mover_B)
print("Se codifican como:", codificados_para_mover_B)

posiciones_a_mover_B = generar_nuevo_vector(correctas_B, posicion_patron_B)
posiciones_a_mover_B_suministro = correccion_coordenadas(posiciones_a_mover_B)
print("Se llevan a:", posiciones_a_mover_B_suministro)
codificados_hacia_suministro_B = convertir_a_numeros(posiciones_a_mover_B_suministro)
print("Se codifican como:", codificados_hacia_suministro_B)
print("Luego se llevan a la matriz de descarga a pos:", posiciones_a_mover_B)
codificados_hacia_carga_B = convertir_a_numeros(posiciones_a_mover_B)
print("Se codifican como:", codificados_hacia_carga_B)


print("Objeto C:")
para_mover_C = generar_nuevo_vector(correctas_C, actuales_C)
print("Las que hay que mover estan en las posiciones:", para_mover_C)
codificados_para_mover_C = convertir_a_numeros(para_mover_C)
print("Se codifican como:", codificados_para_mover_C)

posiciones_a_mover_C = generar_nuevo_vector(correctas_C, posicion_patron_C)
posiciones_a_mover_C_suministro = correccion_coordenadas(posiciones_a_mover_C)
print("Se llevan a:", posiciones_a_mover_C_suministro)
codificados_hacia_suministro_C = convertir_a_numeros(posiciones_a_mover_C_suministro)
print("Se codifican como:", codificados_hacia_suministro_C)
print("Luego se llevan a la matriz de descarga a pos:", posiciones_a_mover_C)
codificados_hacia_carga_C = convertir_a_numeros(posiciones_a_mover_C)
print("Se codifican como:", codificados_hacia_carga_C)

print("AHORA TODOS LOS VALORES UNIDOS") #ojo con el orden de vector es importante
Vector_1 = combinar_vectores(para_mover_A, posiciones_a_mover_A_suministro, 100)
Vector_4 = combinar_vectores(posiciones_a_mover_A_suministro, posiciones_a_mover_A, 100)
Vector_2 = combinar_vectores(para_mover_B, posiciones_a_mover_B_suministro, 200)
Vector_5 = combinar_vectores(posiciones_a_mover_B_suministro, posiciones_a_mover_B, 200)
Vector_3 = combinar_vectores(para_mover_C, posiciones_a_mover_C_suministro, 300)
Vector_6 = combinar_vectores(posiciones_a_mover_C_suministro, posiciones_a_mover_C, 300)

vectores_a_combinar = [Vector_1, Vector_2, Vector_3, Vector_4, Vector_5, Vector_6]
vector_a_enviar = combinar_seis_vectores(vectores_a_combinar)
print("VECTOR FINAL: ", vector_a_enviar)

print("AHORA TODOS LOS VALORES UNIDOS CODIFICADOS") #ojo con el orden de vector es importante
Vector_1_c = combinar_vectores(codificados_para_mover_A, codificados_hacia_suministro_A, 100)
Vector_4_c = combinar_vectores(codificados_hacia_suministro_A, codificados_hacia_carga_A, 100)
Vector_2_c = combinar_vectores(codificados_para_mover_B, codificados_hacia_suministro_B, 200)
Vector_5_c = combinar_vectores(codificados_hacia_suministro_B, codificados_hacia_carga_B, 200)
Vector_3_c = combinar_vectores(codificados_para_mover_C, codificados_hacia_suministro_C, 300)
Vector_6_c = combinar_vectores(codificados_hacia_suministro_C, codificados_hacia_carga_C, 300)

vectores_a_combinar_codificados = [Vector_1_c, Vector_2_c, Vector_3_c, Vector_4_c, Vector_5_c, Vector_6_c]
vector_a_enviar_codificados = combinar_seis_vectores(vectores_a_combinar_codificados)
print("VECTOR FINAL: ", vector_a_enviar_codificados)

