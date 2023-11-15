from PIL import Image
import numpy as np
import cv2

def tomarFoto(coordenadas):
    # Inicializa la cámara
    cap = cv2.VideoCapture(1)  # 0 para la cámara predeterminada

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
    width, height = 20, 20
    for coordenada in coordenadas:
            y, x = coordenada
            color=frame[y,x]
            color = tuple(map(int,color))
            color = tuple(reversed(color))
            cv2.rectangle(frame, (x - width // 2, y - height // 2), (x + width // 2, y + height // 2), color, -1)
            cv2.rectangle(frame, (x - width // 2, y - height // 2), (x + width // 2, y + height // 2), (0,0,0), 3)

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
def verificar_color(pixel, colores):
    diferencia=0
    diferenciaMinima=1000
    for nombre, valor in colores.items():
        diferencia = sum(abs(pixel[i] - valor[i]) for i in range(3))
        if (diferencia<=diferenciaMinima):
            diferenciaMinima=diferencia
            nombreReal=nombre
    return nombreReal

# Función que crea los valores de calibación correctos para los colores dados
def calibracion(coordenadas, imagen):
    i=1
    Tipo1Coord=[12,18,26,34]
    Tipo1Color=[]
    Tipo2Coord=[23,32,29]
    Tipo2Color=[]
    Tipo3Coord=[15,36,38]
    Tipo3Color=[]
    fondoCoord=[1,10,41,50]
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
    print("TIPO 100 PROMEDIO: ")
    print(Tipo1Promedio)
    Tipo2Promedio = np.mean(Tipo2Color, axis=0)
    print("TIPO 200 PROMEDIO: ")
    print(Tipo2Promedio)
    Tipo3Promedio = np.mean(Tipo3Color, axis=0)
    print("TIPO 300 PROMEDIO: ")
    print(Tipo3Promedio)
    fondoPromedio = np.mean(fondoColor, axis=0)
    print("FONDO 0 PROMEDIO: ")
    print(fondoPromedio)
    
    return Tipo1Promedio, Tipo2Promedio, Tipo3Promedio, fondoPromedio

def verCamara(coordenadas, colores):
    # Inicializa la cámara
    cap = cv2.VideoCapture(1)  # 0 para la cámara predeterminada

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
    matriz_colores = [[(0, 0, 0)] * 10 for relleno in range(5)]

    ventana_cerrada = False

    while (not ventana_cerrada):
        # Captura un fotograma de la cámara
        ret, frame = cap.read()

        if not ret:
            print("No se pudo capturar el fotograma")
            break

        # Se crean los cuadros de confirmación
        window_width, window_height = 20, 20  # Tamaño del cuadro
        i,j = 0,0                             # Posiciones de la matriz de confirmación

        for coordenada in coordenadas:
            # Se verifican los píxeles
            y, x = coordenada
            color = frame[y,x]
            color = tuple(map(int,color))
            color = tuple(reversed(color))
            nombre_color = verificar_color(color, colores)
            # BORDE NEGRO
            cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), (0,0,0), 3)
            if nombre_color==100:
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores[100])), 6)
                matriz_colores[j][i]=colores[100]
            elif nombre_color==200:
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores[200])), 6)
                matriz_colores[j][i]=colores[200]
            elif nombre_color==300:
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores[300])), 6)
                matriz_colores[j][i]=colores[300]
            else:
                cv2.rectangle(frame, (x - window_width // 2, y - window_height // 2), (x + window_width // 2, y + window_height // 2), tuple(reversed(colores[None])), 6)
                matriz_colores[j][i]=colores[None]

            # Se rastrea la matriz de confirmación
            if (i==9):
                i=0
                j=j+1
            else:
                i=i+1

        # Se dibuja la matriz de confirmación:
        for i in range(10):
            for j in range(5):
                color = tuple(reversed(matriz_colores[j][i]))
                y1, y2 = j * (window_height), (j + 1) * (window_height)
                x1, x2 = i * (window_width), (i + 1) * (window_width)
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
    if ret:
        # Guarda la imagen en un archivo
        # cv2.imwrite("captura.jpg", frame)
        # print("Imagen guardada como 'captura.jpg'")
        print("Cámara cerrada")
    else:
        print("No se pudo capturar la imagen")
    cv2.destroyAllWindows()
    # tomarFoto()

##################################################
#  FUNCIONAMIENTO
##################################################

def mapeo():
    # Se definen las coordenadas de los pixeles a analizar:
    # La imagen tiene una resolución de 1920x1080 píxeles
    coordenadas = [(270, 250), (270, 405), (270, 570), (270, 725), (270, 880), (270, 1035), (270, 1190), (270, 1345), (270, 1500), (270, 1655),
                   (425, 250), (425, 405), (425, 570), (425, 725), (425, 880), (425, 1035), (425, 1190), (425, 1345), (425, 1500), (425, 1655),
                   (580, 250), (580, 405), (580, 570), (580, 725), (580, 880), (580, 1035), (580, 1190), (580, 1345), (580, 1500), (580, 1655),
                   (735, 250), (735, 405), (735, 570), (735, 725), (735, 880), (735, 1035), (735, 1190), (735, 1345), (735, 1500), (735, 1655),
                   (890, 250), (890, 405), (890, 570), (890, 725), (890, 880), (890, 1035), (890, 1190), (890, 1345), (890, 1500), (890, 1655),]

    matrizSuministro = [[None for _ in range(5)] for _ in range(5)]
    matrizCarga = [[None for _ in range(5)] for _ in range(5)]

    # Se toma la foto desde la cámara
    # imagen = tomarFoto(coordenadas)
    imagen = Image.open("captura.jpg")

    # Se calibran los colores a partir de la imagen tomada
    resultadosCalibracion  = calibracion(coordenadas, imagen)

    # Definir los valores de color en formato (R, G, B)
    colores = {
        100: resultadosCalibracion[0],
        200: resultadosCalibracion[1],
        300: resultadosCalibracion[2],
        None: resultadosCalibracion[3]
    }

    # Verifica los colores en las coordenadas especificadas
    i=1
    # imagen = tomarFoto()
    print("COMRPOBACIÓN CON NUEVA IMAGEN")
    for coordenada in coordenadas:
        y, x = coordenada  # Intercambia el orden de las coordenadas
        pixel = imagen.getpixel((x, y))  # Intercambia el orden de las coordenadas al llamar a getpixel

        print(f"Analizando el color en {i}: ")
        nombre_color = verificar_color(pixel[:3], colores)  # Compara solo los tres primeros componentes (R, G, B)
        print(f"En {i} se encontró el color: {nombre_color}")
        if ((i%10) <= 5 and (i%10) > 0):
            matrizSuministro[(i//10)][(i%10) - 1] = nombre_color
        elif (i%10 != 0):
            matrizCarga[(i//10)][(i%10) - 6] = nombre_color
        else: 
            matrizCarga[(i//10) - 1][(i%10) - 1] = nombre_color
        i=i+1

    print(matrizSuministro)
    print(matrizCarga)
    # verCamara(coordenadas, colores)
    return(matrizSuministro, matrizCarga)
