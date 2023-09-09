# Vector final
vector_final = [100, (1, 2), (1, 9), 100, (3, 0), (3, 8), 100, (4, 2), (4, 5), 100,
                (0, 2), (0, 6), 200, (1, 0), (0, 8), 200, (1, 3), (4, 8), 200, (0, 3), (0, 9), 300,
                (2, 0), (1, 7), 300, (3, 2), (4, 7), 300, (1, 8), (1, 3), 100, (1, 9), (1, 4), 100,
                (3, 8), (3, 3), 100, (4, 5), (4, 0), 100, (0, 6), (0, 1), 200, (0, 8), (0, 3), 200,
                (4, 8), (4, 3), 200, (0, 9), (0, 4), 300, (1, 7), (1, 2), 300, (4, 7), (4, 2)]


def generar_matriz(vector_final):
    matriz = [[None] * 10 for _ in range(5)]  # Inicializa una matriz 5x10 con None
    matriz2 = [[None] * 10 for _ in range(5)]  # Inicializa una matriz 5x10 con None
    for i in range(0, len(vector_final)//2, 3):
        valor = vector_final[i]
        coordenadas1 = vector_final[i + 1]
        coordenadas2 = vector_final[i + 2]

        fila1, columna1 = coordenadas1
        fila2, columna2 = coordenadas2

        matriz[fila1][columna1] = valor
        matriz[fila2][columna2] = valor

    for i in range(len(vector_final) // 2, len(vector_final), 3):
        valorb = vector_final[i]
        coordenadas1b = vector_final[i + 1]
        coordenadas2b= vector_final[i + 2]

        fila1b, columna1b = coordenadas1b
        fila2b, columna2b = coordenadas2b

        matriz2[fila1b][columna1b] = valorb
        matriz2[fila2b][columna2b] = valorb

    return matriz, matriz2


# Ejemplo de uso:
vector_final = [100, (0, 4), (1, 8), 100, (1, 2), (1, 9), 100, (3, 0), (3, 8), 100, (4, 2), (4, 5), 200, (0, 2), (0, 6), 200, (1, 0), (0, 8), 200, (1, 3), (4, 8), 300, (0, 3), (0, 9), 300, (2, 0), (1, 7), 300, (3, 2), (4, 7), 100, (1, 8), (1, 3), 100, (1, 9), (1, 4), 100, (3, 8), (3, 3), 100, (4, 5), (4, 0), 200, (0, 6), (0, 1), 200, (0, 8), (0, 3), 200, (4, 8), (4, 3), 300, (0, 9), (0, 4), 300, (1, 7), (1, 2), 300, (4, 7), (4, 2)]

matriz_resultante, matriz_resultante2 = generar_matriz(vector_final)

print("ESTAS MATRICES NO TIENEN LOS VALORES BIEN COLOCADOS")
print("Matriz de posiciones iniciales y a donde van en suministro")
for fila in matriz_resultante:
    print(fila)
print("")
print("Matriz donde estan en suministro y a donde deberian ir")
for fila in matriz_resultante2:
    print(fila)



