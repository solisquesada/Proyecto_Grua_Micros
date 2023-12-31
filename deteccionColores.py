from PIL import Image
import numpy as np
import cv2

def tomarFoto():
    # Inicializa la cámara
    cap = cv2.VideoCapture(1)  # 0 para la cámara predeterminada (puede ser diferente en tu sistema)

    # Verifica si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()

    # Define la resolución deseada (ancho x alto)
    width = 1920
    height = 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Captura una imagen
    ret, frame = cap.read()

    # Se pinta la matriz:
    width, height = 50, 50
    for coordenada in coordenadas:
            y, x = coordenada
            color=frame[y,x]
            color = tuple(map(int,color))
            color = tuple(reversed(color))
            cv2.rectangle(frame, (x - width // 2, y - height // 2), (x + width // 2, y + height // 2), color, 4)

    # Cierra la cámara
    cap.release()

    if ret:
        # Guarda la imagen en un archivo
        cv2.imwrite("captura.jpg", frame)
        print("Imagen guardada como 'captura.jpg'")
    else:
        print("No se pudo capturar la imagen")

    # Abre la imagen
    imagen = Image.open("captura.jpg")
    return(imagen)

# Función para comparar el color de un píxel con tolerancia (opcional)
def verificar_color(pixel):
    diferencia=0
    diferenciaMinima=1000
    for nombre, valor in colores.items():
        diferencia = sum(abs(pixel[i] - valor[i]) for i in range(3))
        if (diferencia<=diferenciaMinima):
            diferenciaMinima=diferencia
            nombreReal=nombre
    return nombreReal

# Función que crea los valores de calibación correctos para los colores dados
def calibracion(imagen):
    i=1
    Tipo1Coord=[1,5,9]
    Tipo1Color=[]
    Tipo2Coord=[3,7]
    Tipo2Color=[]
    Tipo3Coord=[6,8]
    Tipo3Color=[]
    fondoCoord=[2,4]
    fondoColor=[]

    for coordenada in coordenadas:
        y, x = coordenada
        pixel = imagen.getpixel((x, y))
        print(f"En {i} se encontró el color: RGB {pixel[:3]}")
        if (i) in Tipo1Coord:
            Tipo1Color.append(pixel[:3])
        elif (i) in Tipo2Coord:
            Tipo2Color.append(pixel[:3])
        elif (i) in Tipo3Coord:
            Tipo3Color.append(pixel[:3])
        elif (i) in fondoCoord:
            fondoColor.append(pixel[:3])
        i=i+1
    
    Tipo1Promedio = np.mean(Tipo1Color, axis=0)
    print("TIPO 1 PROMEDIO: ")
    print(Tipo1Promedio)
    Tipo2Promedio = np.mean(Tipo2Color, axis=0)
    print("TIPO 2 PROMEDIO: ")
    print(Tipo2Promedio)
    Tipo3Promedio = np.mean(Tipo3Color, axis=0)
    print("TIPO 3 PROMEDIO: ")
    print(Tipo3Promedio)
    fondoPromedio = np.mean(fondoColor, axis=0)
    print("FONDO PROMEDIO: ")
    print(fondoPromedio)
    
    return Tipo1Promedio, Tipo2Promedio, Tipo3Promedio, fondoPromedio

def verCamara():
    # Inicializa la cámara
    cap = cv2.VideoCapture(1)  # 0 para la cámara predeterminada (puede ser diferente en tu sistema)

    # Verifica si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()

    # Crea una ventana con un nombre específico
    cv2.namedWindow("Camara en tiempo real", cv2.WINDOW_NORMAL)

    # Establece el tamaño deseado para la ventana
    window_width = 800
    window_height = 600
    cv2.resizeWindow("Camara en tiempo real", window_width, window_height)

    # Define la resolución deseada (ancho x alto)
    width = 1920
    height = 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Inicializa la matriz de colores con un color de fondo (puedes cambiarlo)
    matriz_colores = [[(0, 0, 0)] * 3 for relleno in range(3)]

    ventana_cerrada = False

    while (not ventana_cerrada):
        # Captura un fotograma de la cámara
        ret, frame = cap.read()

        if not ret:
            print("No se pudo capturar el fotograma")
            break

        # Se crean los cuadros de confirmación
        window_width, window_height = 50, 50  # Tamaño del cuadro
        i,j = 0,0                             # Posiciones de la matriz de confirmación

        for coordenada in coordenadas:
            # Se verifican los píxeles
            y, x = coordenada
            color = frame[y,x]
            color = tuple(map(int,color))
            color = tuple(reversed(color))
            nombre_color = verificar_color(color)
            if nombre_color=="TIPO1":
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores["TIPO1"])), 4)
                matriz_colores[j][i]=colores["TIPO1"]
            elif nombre_color=="TIPO2":
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores["TIPO2"])), 4)
                matriz_colores[j][i]=colores["TIPO2"]
            elif nombre_color=="TIPO3":
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores["TIPO3"])), 4)
                matriz_colores[j][i]=colores["TIPO3"]
            else:
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores["FONDO"])), 4)
                matriz_colores[j][i]=colores["FONDO"]

            # Se rastrea la matriz de confirmación
            if (i==2):
                i=0
                j=j+1
            else:
                i=i+1

        # Se dibuja la matriz de confirmación:
        for i in range(3):
            for j in range(3):
                color = tuple(reversed(matriz_colores[i][j]))
                y1, y2 = i * (window_height), (i + 1) * (window_height)
                x1, x2 = j * (window_width), (j + 1) * (window_width)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

        # Muestra el fotograma en una ventana
        cv2.imshow("Camara en tiempo real", frame)

        # Sale del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Verifica si la ventana se cerró
        if cv2.getWindowProperty("Camara en tiempo real", cv2.WND_PROP_VISIBLE) < 1:
            ventana_cerrada = True

    # Libera la cámara y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()
    # tomarFoto()

##################################################
#  FUNCIONAMIENTO
##################################################

# Se definen las coordenadas de los pixeles a analizar:
# La imagen tiene una resolución de 1920x1080 píxeles
coordenadas = [(90, 500), (90, 900), (90, 1300),
               (500, 500), (500, 900), (500, 1300),
               (900, 500), (900, 900), (900, 1300),]

# Se toma la foto desde la cámara
# imagen = tomarFoto()
imagen = Image.open("captura.jpg")

# Pruebas de calibración
resultadosCalibracion  = calibracion(imagen)

# Definir los valores de color en formato (R, G, B)
colores = {
    "TIPO1": resultadosCalibracion[0],
    "TIPO2": resultadosCalibracion[1],
    "TIPO3": resultadosCalibracion[2],
    "FONDO": resultadosCalibracion[3]
}

# Verifica los colores en las coordenadas especificadas
i=1
# imagen = tomarFoto()
print("COMRPOBACIÓN CON NUEVA IMAGEN")
for coordenada in coordenadas:
    y, x = coordenada  # Intercambia el orden de las coordenadas
    pixel = imagen.getpixel((x, y))  # Intercambia el orden de las coordenadas al llamar a getpixel
    print(f"Analizando el color en {i}: ")
    nombre_color = verificar_color(pixel[:3])  # Compara solo los tres primeros componentes (R, G, B)
    print(f"En {i} se encontró el color: {nombre_color}")
    i=i+1

verCamara()

