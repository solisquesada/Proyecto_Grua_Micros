from typing import List, Any
import pygame
import serial
import sys
import time
import mapeoCamara
import Metodo_reacomodo_v2
import metodoPatron
import UART_write


pygame.init() # Inicializar Pygame

screen_width = 1100 # Configuración de la pantalla
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height)) # Crear la ventana con el tamaño especificado

pygame.display.set_caption("Proyecto grua") # Establecer el título de la ventana

# Colores
C1 = (255, 255, 255) #blanco
C2 = (0, 0, 0) #Negro
C3 = (157, 100, 132) #Verde poco saturado fondo
C4 = (214, 234, 248)  # Celeste
C5 = (255, 255, 255)  #
C6 = (109, 69, 111)  # celeste
C7 = (82, 81, 116)  # morado
C8 = (82, 59, 86)  # morado oscuro
C9 = (255, 0, 0) #Rojo 200
C10 = (0, 0, 255) #Azul 100
C11 = (29, 131, 71) #Verde 300
C12 = (133, 133, 133) #Gris

# Fuente
fontbotones = pygame.font.Font(None, 48)
fonttitulo = pygame.font.Font(None, 80)
fontmatriz = pygame.font.Font(None, 50)
fontpequena = pygame.font.Font(None, 35)
fontalarma = pygame.font.Font(None, 30)

def draw_text(text, font, color, x, y): #Funcion para crear texto
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def reordenar():# Pantalla para el metodo reacomodo
    running = True

    cx, cx1, cy = 620 - 545 + 145 - 72.5, 75 + 545 - 72.5, 65
    x_circulo, y_circulo = 130  + 72.5 , 250
    Mx, My, ICx, ICy, IMx, IMy = 0, 0, 600, 600, 600, 600  # Variables para movimientos de botones
    matriz_movimientos_x = [[0 for _ in range(5)] for _ in range(5)]  # Crea las matrices para hacer los moviminetos
    matriz_movimientos_y = [[0 for _ in range(5)] for _ in range(5)]
    matriz_movimientos_x_inicial = [[0 for _ in range(5)] for _ in range(5)]
    matriz_movimientos_y_inicial = [[0 for _ in range(5)] for _ in range(5)]
    alarma, iniciar_mapeo, mapeo_completado, alarma_verificada, iniciar_calculos, calculos_campletados, iniciar_movimientos = 0, 0, 0, 0, 0, 0, 0

    vector = [] #  Variables varias
    posicion = 0
    contador = 0
    v = 0
    soltar_agarrar = 1
    actualx = 0
    actualy = 0
    listo = 0
    termino_inicial = 0
    entrar=120
    Error = 0

    while running:
        mx, my = pygame.mouse.get_pos()
        # Codigo para el diseño de las matrices y numeracion
        Fondo_P = pygame.image.load("Fondo_P.jpg").convert()
        screen.blit(Fondo_P, [0, 0])
        draw_text("Reacomodar", fonttitulo, C1, 210, 55)
        D_opacity = 100
        D1_opacity = 150

        def draw_rect(x, y, width, height, color):
            rect = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(rect, color, (0, 0, width, height))
            screen.blit(rect, (x, y))

        for offset_x, offset_y in [(cx, cy)]:
            draw_rect(-35 + offset_x, 50 + cy, 880, 50, C6 + (D1_opacity,))
            draw_rect(-35 + offset_x, 100 + cy, 880, 465, C3 + (D_opacity,))
            draw_text("Matriz de suministro", fontmatriz, C1, 200 + offset_x, 75 + cy)
            draw_text("Matriz de Carga", fontmatriz, C1, 200 + offset_x + 400, 75 + cy)

        for i, letra in enumerate(["A", "B", "C", "D", "E"]):
            draw_text(letra, fontmatriz, C5, 55 + i * 80 + cx, 130 + cy)
            draw_text(letra, fontmatriz, C5, 55 + i * 80 + cx1, 130 + cy)

        for i, numero in enumerate(["1", "2", "3", "4", "5"]):
            draw_text(numero, fontmatriz, C5, -10 + cx, 185 + i * 80 + cy)

        P_opacity = 120
        start_x = 20 + cx #167.5
        start_y = 150 + cy #215
        x_step = 80
        y_step = 80

        Mapear = pygame.Rect(750 + Mx, 35 + My, 200, 50)  # agrega el boton de iniciar mapeo
        Iniciar_cal = pygame.Rect(750 + ICx, 35 + ICy, 200, 50)
        Iniciar_mov = pygame.Rect(750 + IMx, 35 + IMy, 200, 50)

        if iniciar_mapeo == 0:
            if Mapear.collidepoint((mx, my)):
                pygame.draw.rect(screen, C7, Mapear)
            else:
                pygame.draw.rect(screen, C8, Mapear)
            draw_text("Iniciar mapeo", fontpequena, C1, 850, 60)

        elif iniciar_mapeo == 1:
            draw_text("Mapeando...", fontpequena, C1, 850, 60)
            pygame.display.update()
            matriz, matriz_carga = mapeoCamara.mapeo() # LLAMA AL MAPEAR PARA OBTENER LA MATRIZ..................................................
            mapeo_completado = 1
            iniciar_mapeo = 2

        if mapeo_completado == 1:  # Entra cuando ya el mapeo esta competo
            if calculos_campletados == 0:
                if iniciar_calculos == 0:
                    Mx, My, ICx, ICy, IMx, IMy = 600, 600, 0, 0, 600, 600
                    if Iniciar_cal.collidepoint((mx, my)):
                        pygame.draw.rect(screen, C7, Iniciar_cal)
                    else:
                        pygame.draw.rect(screen, C8, Iniciar_cal)
                    draw_text("Calcular", fontpequena, C1, 850, 60)

                elif iniciar_calculos == 1:
                    draw_text("Procesando...", fontpequena, C1, 850, 60)
                    pygame.display.update()
                    vector = Metodo_reacomodo_v2.external_call_reorganized_method() #Llama para obtener vector de movimientos ......................................
                    print("Mi vector:", vector)
                    calculos_campletados = 1
            else:
                Mx, My, ICx, ICy, IMx, IMy = 600, 600, 600, 600, 0, 0
                if Iniciar_mov.collidepoint((mx, my)):
                    pygame.draw.rect(screen, C7, Iniciar_mov)
                else:
                    pygame.draw.rect(screen, C8, Iniciar_mov)
                draw_text("Iniciar", fontpequena, C1, 850, 60)

            # Crea una matriz 2D para almacenar las cuadros creadas
            matriz_superficies = []
            # Recorre la matriz que contiene los índices de color para cada celda
            row = 0
            while row < 5:
                fila_superficies = []  # Crea una lista para almacenar las superficies de esta fila
                col = 0
                while col < 5:
                    color_index = matriz_carga[row][col]
                    surface = None
                    # Comprueba el índice de color y crea la superficie con el color correspondiente
                    if color_index == 100:
                        surface = pygame.Surface((70, 70), pygame.SRCALPHA)
                        pygame.draw.rect(surface, C10 + (P_opacity,), (0, 0, 70, 70))
                    elif color_index == 200:
                        surface = pygame.Surface((70, 70), pygame.SRCALPHA)
                        pygame.draw.rect(surface, C9 + (P_opacity,), (0, 0, 70, 70))
                    elif color_index == 300:
                        surface = pygame.Surface((70, 70), pygame.SRCALPHA)
                        pygame.draw.rect(surface, C11 + (P_opacity,), (0, 0, 70, 70))

                    fila_superficies.append(surface)
                    if surface:  # Verifica si se creó una superficie y la coloca en la pantalla en la posición correcta
                        x_pos = start_x + col * x_step + 400
                        y_pos = start_y + row * y_step
                        if termino_inicial == 0:
                            matriz_movimientos_x_inicial[row][col] = start_x + col * x_step + 400
                            matriz_movimientos_y_inicial[row][col] = start_y + row * y_step
                        screen.blit(surface, (x_pos + matriz_movimientos_x[row][col], y_pos + matriz_movimientos_y[row][col]))  # Coloca la superficie en la pantalla
                    col += 1

                matriz_superficies.append(fila_superficies)  # Agrega la lista de superficies de esta fila a la matriz de superficies
                row += 1
            termino_inicial = 1

            if iniciar_movimientos == 1 and Error != 400:# Inicia con los movimientos

                pygame.draw.circle(screen, C2, (x_circulo, y_circulo), 20)  # muestra el circulo
                pygame.display.update()
                primer_elemento = vector[posicion]
                if vector[posicion] == - 1:
                    print("R:Agrarro o suelta")
                    #Error = UART_write.enviarMovimiento(5)
                    if soltar_agarrar == 6:
                            soltar_agarrar = 0
                    posicion+=1
                    soltar_agarrar += 1
                else:
                    mov = int(primer_elemento) / 445
                    mov1 = round(mov)
                    if mov1 < 0:
                        negativo = 1
                    else:
                        negativo = 0
                    mov1_absoluto = abs(mov1)
                    if v != mov1_absoluto:
                        if soltar_agarrar == 1 or soltar_agarrar == 4:
                            if negativo == 0:
                                if soltar_agarrar == 1:
                                    x_circulo += 80
                                    print("R:+x")
                                    #Error = UART_write.enviarMovimiento(1)
                                
                                if soltar_agarrar == 4 :
                                    if entrar == 1:
                                        x_circulo += 80
                                        matriz_movimientos_x[actualx][actualy] += 80
                                        matriz_movimientos_x_inicial[actualx][actualy] += 80
                                        print("R:+x")
                                        #Error = UART_write.enviarMovimiento(1)

                            if negativo == 1:
                                if soltar_agarrar == 1:
                                    x_circulo -= 80
                                    print("R:-x")
                                    #Error = UART_write.enviarMovimiento(2)
                                
                                if soltar_agarrar == 4:
                                    if entrar == 1:
                                        x_circulo -= 80
                                        matriz_movimientos_x[actualx][actualy] -= 80
                                        matriz_movimientos_x_inicial[actualx][actualy] -= 80
                                        print("R:-x")
                                        #Error = UART_write.enviarMovimiento(2)
                        else:
                            if negativo == 0:
                                if soltar_agarrar == 2:
                                    y_circulo += 80
                                    print("R:+y")
                                    #Error = UART_write.enviarMovimiento(3)
     
                                if soltar_agarrar == 4 or soltar_agarrar == 5:
                                    if entrar == 1:
                                        y_circulo += 80
                                        matriz_movimientos_y[actualx][actualy] += 80
                                        matriz_movimientos_y_inicial[actualx][actualy] += 80
                                        print("R:+y")
                                        #Error = UART_write.enviarMovimiento(3)
                            if negativo == 1:
                                if soltar_agarrar == 1 or soltar_agarrar == 2:
                                    y_circulo -= 80
                                    print("R:-y")
                                    #Error = UART_write.enviarMovimiento(4)
                                if soltar_agarrar == 4 or soltar_agarrar == 5:
                                    if entrar == 1:
                                        y_circulo -= 80
                                        matriz_movimientos_y[actualx][actualy] -= 80
                                        matriz_movimientos_y_inicial[actualx][actualy] -= 80
                                        print("R:-y")
                                        #Error = UART_write.enviarMovimiento(4)
                    v += 1
                    time.sleep(0.4)
                    if v == mov1_absoluto or mov1_absoluto == 0:
                        soltar_agarrar = soltar_agarrar + 1
                        posicion += 1
                        contador += 1
                        listo = 0
                        v = 0

                    if soltar_agarrar == 3 and listo == 0:
                        entrar = 1
                        if x_circulo == (matriz_movimientos_x_inicial[0][0] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[0][0] + 35):
                            actualx = 0
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[0][1] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[0][1] + 35):
                            actualx = 0
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[0][2] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[0][2] + 35):
                            actualx = 0
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[0][3] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[0][3] + 35):
                            actualx = 0
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[0][4] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[0][4] + 35):
                            actualx = 0
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[1][0] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[1][0] + 35):
                            actualx = 1
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[1][1] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[1][1] + 35):
                            actualx = 1
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[1][2] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[1][2] + 35):
                            actualx = 1
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[1][3] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[1][3] + 35):
                            actualx = 1
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[1][4] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[1][4] + 35):
                            actualx = 1
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[2][0] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[2][0] + 35):
                            actualx = 2
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[2][1] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[2][1] + 35):
                            actualx = 2
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[2][2] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[2][2] + 35):
                            actualx = 2
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[2][3] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[2][3] + 35):
                            actualx = 2
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[2][4] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[2][4] + 35):
                            actualx = 2
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[3][0] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[3][0] + 35):
                            actualx = 3
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[3][1] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[3][1] + 35):
                            actualx = 3
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[3][2] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[3][2] + 35):
                            actualx = 3
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[3][3] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[3][3] + 35):
                            actualx = 3
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[3][4] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[3][4] + 35):
                            actualx = 3
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[4][0] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[4][0] + 35):
                            actualx = 4
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[4][1] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[4][1] + 35):
                            actualx = 4
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[4][2] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[4][2] + 35):
                            actualx = 4
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[4][3] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[4][3] + 35):
                            actualx = 4
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[4][4] + 35) and y_circulo == (
                                matriz_movimientos_y_inicial[4][4] + 35):
                            actualx = 4
                            actualy = 4
                        else:
                            entrar = 0
                        listo = 1
                pygame.draw.circle(screen, C2, (x_circulo, y_circulo), 20)  # muestra el circulo
                if posicion == len(vector):
                    iniciar_movimientos = 2

        if iniciar_movimientos ==2:
            pygame.draw.circle(screen, C2, (x_circulo, y_circulo), 20)  # muestra el circulo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Evento para detectar clics en los botones
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Mapear.collidepoint((mx, my)):
                    iniciar_mapeo = 1
                if Iniciar_cal.collidepoint((mx, my)):
                    iniciar_calculos = 1
                if Iniciar_mov.collidepoint((mx, my)):
                    iniciar_movimientos = 1
        pygame.display.update()

def patron():
    running = True
    cx, cx1, cy = 620 - 545 + 145 - 72.5, 75 + 545 - 72.5, 65
    x_circulo, y_circulo = 130 + 72.5, 250
    Mx, My, ICx, ICy, IMx, IMy = 0, 0, 600, 600, 600, 600  # Variables para movimientos de botones
    matriz_movimientos_x = [[0 for _ in range(5)] for _ in range(5)]  # Crea las matrices para hacer los moviminetos
    matriz_movimientos_y = [[0 for _ in range(5)] for _ in range(5)]
    matriz_movimientos_x_inicial = [[0 for _ in range(5)] for _ in range(5)]
    matriz_movimientos_y_inicial = [[0 for _ in range(5)] for _ in range(5)]
    alarma, iniciar_mapeo, mapeo_completado, alarma_verificada, iniciar_calculos, calculos_campletados, iniciar_movimientos = 0, 0, 0, 0, 0, 0, 0

    posicion = 0
    contador = 0
    v = 0
    soltar_agarrar = 1
    actualx = 0
    actualy = 0
    listo = 0
    termino_inicial = 0
    entrar = 1
    Proceso_terminado = 0
    Error = 0
    electroiman = 0
    movimientosBasura = []


    while running:
        # Desde aca se define todo lo que se va a mostrar en pantalla,las matrices y diseño
        mx, my = pygame.mouse.get_pos()
        Fondo_P = pygame.image.load("Fondo_P.jpg").convert()
        screen.blit(Fondo_P, [0, 0])
        draw_text("Patrón", fonttitulo, C1, 130, 55)
        D_opacity = 100
        D1_opacity = 150

        def draw_rect(x, y, width, height, color):
            rect = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(rect, color, (0, 0, width, height))
            screen.blit(rect, (x, y))

        for offset_x, offset_y in [(cx, cy)]:
            draw_rect(-35 + offset_x, 50 + cy, 880, 50, C6 + (D1_opacity,))
            draw_rect(-35 + offset_x, 100 + cy, 880, 465, C3 + (D_opacity,))
            draw_text("Matriz de suministro", fontmatriz, C1, 200 + offset_x, 75 + cy)
            draw_text("Matriz de Carga", fontmatriz, C1, 200 + offset_x + 400, 75 + cy)

        for i, letra in enumerate(["A", "B", "C", "D", "E"]):
            draw_text(letra, fontmatriz, C5, 55 + i * 80 + cx, 130 + cy)
            draw_text(letra, fontmatriz, C5, 55 + i * 80 + cx1, 130 + cy)

        for i, numero in enumerate(["1", "2", "3", "4", "5"]):
            draw_text(numero, fontmatriz, C5, -10 + cx, 185 + i * 80 + cy)

        P_opacity = 120
        start_x = 20 + cx
        start_y = 150 + cy
        x_step = 80
        y_step = 80

        B_alarma_G = pygame.Rect(590, 35, 150, 50)  # Aca estan la creacion de lo cuadros necesarios para las alarmas
        pygame.draw.rect(screen, C12, B_alarma_G)  # Cuadro principla, gris
        B_alarma_NR = pygame.Rect(595, 40, 140, 40)  # Este es el que cambia de color entre Negro y Rojo
        Obstaculo_retirado = pygame.Rect(320, 35, 200, 50)

        Mapear = pygame.Rect(750 + Mx, 35 + My, 200, 50)  # agrega el boton de iniciar mapeo
        Iniciar_cal = pygame.Rect(750 + ICx, 35 + ICy, 200, 50)
        Iniciar_mov = pygame.Rect(750 + IMx, 35 + IMy, 200, 50)

        if alarma == 0:  # Este if es para determinar si se va haber la alarma o no
            pygame.draw.rect(screen, C2, B_alarma_NR)
        else:
            pygame.draw.rect(screen, C9, B_alarma_NR)
            iniciar_mapeo = 2  # Esto es solo para que cuando esta la alarma encendida no se vea el boton de mapear, ni "mapeando.."

        if alarma == 202:
            if Obstaculo_retirado.collidepoint((mx, my)):
                pygame.draw.rect(screen, C7, Obstaculo_retirado)
            else:
                pygame.draw.rect(screen, C8, Obstaculo_retirado)
            draw_text("Obstáculo retirado", fontalarma, C1, 420, 60)
            draw_text("Obtaculo detectado... ", fontpequena, C1, 900, 60)

        elif alarma == 201:
            if Obstaculo_retirado.collidepoint((mx, my)):
                pygame.draw.rect(screen, C7, Obstaculo_retirado)
            else:
                pygame.draw.rect(screen, C8, Obstaculo_retirado)
            draw_text("Retirar objetos", fontalarma, C1, 420, 60)
            draw_text("Sobran objetos... ", fontpequena, C1, 875, 60)

        elif alarma == 203:
            if Obstaculo_retirado.collidepoint((mx, my)):
                pygame.draw.rect(screen, C7, Obstaculo_retirado)
            else:
                pygame.draw.rect(screen, C8, Obstaculo_retirado)
            draw_text("Solucionado", fontalarma, C1, 420, 60)
            draw_text("Faltan objetos... ", fontpequena, C1, 875, 60)

        draw_text("Alarma", fontpequena, C2, 665, 60)  # Escribe la palabra alarma aca para que quede sobre los cuadros

        if iniciar_mapeo == 0:
            Mx, My, ICx, ICy, IMx, IMy = 0, 0, 600, 600, 600, 600  # Variables para movimientos de botones
            if Mapear.collidepoint((mx, my)):
                pygame.draw.rect(screen, C7, Mapear)
            else:
                pygame.draw.rect(screen, C8, Mapear)
            draw_text("Iniciar mapeo", fontpequena, C1, 850, 60)

        elif iniciar_mapeo == 1:
            draw_text("Mapeando...", fontpequena, C1, 850, 60)
            pygame.display.update()
            matriz_suministro, matriz_carga = mapeoCamara.mapeo()  # LLAMA AL MAPEAR PARA OBTENER LA MATRIZ..................................................
            mapeo_completado = 1
            iniciar_mapeo = 2
            calculos_campletados = 0
            iniciar_calculos = 0

        if mapeo_completado == 1:  # Entra cuando ya el mapeo esta competo
            # Crea una matriz 2D para almacenar las cuadros creadas
            matriz_superficies = []
            # Recorre la matriz que contiene los índices de color para cada celda
            for row in range(5):
                fila_superficies = []  # Crea una lista para almacenar las superficies de esta fila
                for col in range(5):
                    if alarma == 202:
                        color_index = matriz_carga[row][col]
                    else:
                        color_index = matriz_suministro[row][col]
                    surface = None

                    # Comprueba el índice de color y crea la superficie con el color correspondiente
                    if color_index == 100:
                        surface = pygame.Surface((70, 70), pygame.SRCALPHA)
                        pygame.draw.rect(surface, C10 + (P_opacity,), (0, 0, 70, 70))
                    elif color_index == 200:
                        surface = pygame.Surface((70, 70), pygame.SRCALPHA)
                        pygame.draw.rect(surface, C9 + (P_opacity,), (0, 0, 70, 70))
                    elif color_index == 300:
                        surface = pygame.Surface((70, 70), pygame.SRCALPHA)
                        pygame.draw.rect(surface, C11 + (P_opacity,), (0, 0, 70, 70))

                    fila_superficies.append(surface)
                    if surface:  # Verifica si se creó una superficie y la coloca en la pantalla en la posición correcta
                        if alarma == 202:
                            x_pos = start_x + col * x_step +400
                        else:
                            x_pos = start_x + col * x_step

                        y_pos = start_y + row * y_step
                        if termino_inicial == 0:
                            if alarma == 202:
                                matriz_movimientos_x_inicial[row][col] = start_x + col * x_step +400
                            else:
                                matriz_movimientos_x_inicial[row][col] = start_x + col * x_step
                            matriz_movimientos_y_inicial[row][col] = start_y + row * y_step
                        screen.blit(surface, (x_pos + matriz_movimientos_x[row][col], y_pos + matriz_movimientos_y[row][col]))  # Coloca la superficie en la pantalla
                matriz_superficies.append(fila_superficies)  # Agrega la lista de superficies de esta fila a la matriz de superficies

            if calculos_campletados == 0:
                if iniciar_calculos == 0:
                    Mx, My, ICx, ICy, IMx, IMy = 600, 600, 0, 0, 600, 600
                    if Iniciar_cal.collidepoint((mx, my)):
                        pygame.draw.rect(screen, C7, Iniciar_cal)
                    else:
                        pygame.draw.rect(screen, C8, Iniciar_cal)
                    draw_text("Calcular", fontpequena, C1, 850, 60)

                elif iniciar_calculos == 1:

                    draw_text("Procesando...", fontpequena, C1, 850, 60)
                    pygame.display.update()
                    alarma, vectorp = metodoPatron.metodoPatron1()  # Llama para obtener vector de movimientos ......................................

                    if alarma == 0:
                        calculos_campletados = 1
                    if alarma_verificada == 1:
                        calculos_campletados = 1
                        alarma = 0
                    iniciar_calculos = 2
            else:
                Mx, My, ICx, ICy, IMx, IMy = 600, 600, 600, 600, 0, 0
                if Iniciar_mov.collidepoint((mx, my)):
                    pygame.draw.rect(screen, C7, Iniciar_mov)
                else:
                    pygame.draw.rect(screen, C8, Iniciar_mov)
                draw_text("Iniciar", fontpequena, C1, 850, 60)

            if (iniciar_movimientos == 1 and calculos_campletados == 1 and Error != 400) or(iniciar_movimientos == 1 and alarma == 202):
                termino_inicial = 1
                pygame.draw.circle(screen, C2, (x_circulo, y_circulo), 20)  # muestra el circulo
                pygame.display.update()
                if alarma == 202:
                    primer_elemento = movimientosBasura[posicion]
                else:
                    primer_elemento = vectorp[posicion]

                if primer_elemento == -1:
                    posicion += 1
                    if electroiman == 0:
                        electroiman = 1
                    elif electroiman == 1:
                        electroiman = 0
                    print("R:agarrar o soltar ")
                    # Error = UART_write.enviarMovimiento(5)
                    if soltar_agarrar == 6:
                        soltar_agarrar = 0
                    soltar_agarrar += 1
                else:
                    if electroiman == 1 and listo == 0:
                        entrar = 1
                        if x_circulo == (matriz_movimientos_x_inicial[0][0] + 35) and y_circulo == (matriz_movimientos_y_inicial[0][0] + 35):
                            actualx = 0
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[0][1] + 35) and y_circulo == (matriz_movimientos_y_inicial[0][1] + 35):
                            actualx = 0
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[0][2] + 35) and y_circulo == (matriz_movimientos_y_inicial[0][2] + 35):
                            actualx = 0
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[0][3] + 35) and y_circulo == (matriz_movimientos_y_inicial[0][3] + 35):
                            actualx = 0
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[0][4] + 35) and y_circulo == (matriz_movimientos_y_inicial[0][4] + 35):
                            actualx = 0
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[1][0] + 35) and y_circulo == (matriz_movimientos_y_inicial[1][0] + 35):
                            actualx = 1
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[1][1] + 35) and y_circulo == (matriz_movimientos_y_inicial[1][1] + 35):
                            actualx = 1
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[1][2] + 35) and y_circulo == (matriz_movimientos_y_inicial[1][2] + 35):
                            actualx = 1
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[1][3] + 35) and y_circulo == (matriz_movimientos_y_inicial[1][3] + 35):
                            actualx = 1
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[1][4] + 35) and y_circulo == (matriz_movimientos_y_inicial[1][4] + 35):
                            actualx = 1
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[2][0] + 35) and y_circulo == (matriz_movimientos_y_inicial[2][0] + 35):
                            actualx = 2
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[2][1] + 35) and y_circulo == (matriz_movimientos_y_inicial[2][1] + 35):
                            actualx = 2
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[2][2] + 35) and y_circulo == (matriz_movimientos_y_inicial[2][2] + 35):
                            actualx = 2
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[2][3] + 35) and y_circulo == (matriz_movimientos_y_inicial[2][3] + 35):
                            actualx = 2
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[2][4] + 35) and y_circulo == (matriz_movimientos_y_inicial[2][4] + 35):
                            actualx = 2
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[3][0] + 35) and y_circulo == (matriz_movimientos_y_inicial[3][0] + 35):
                            actualx = 3
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[3][1] + 35) and y_circulo == (matriz_movimientos_y_inicial[3][1] + 35):
                            actualx = 3
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[3][2] + 35) and y_circulo == (matriz_movimientos_y_inicial[3][2] + 35):
                            actualx = 3
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[3][3] + 35) and y_circulo == (matriz_movimientos_y_inicial[3][3] + 35):
                            actualx = 3
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[3][4] + 35) and y_circulo == (matriz_movimientos_y_inicial[3][4] + 35):
                            actualx = 3
                            actualy = 4
                        elif x_circulo == (matriz_movimientos_x_inicial[4][0] + 35) and y_circulo == (matriz_movimientos_y_inicial[4][0] + 35):
                            actualx = 4
                            actualy = 0
                        elif x_circulo == (matriz_movimientos_x_inicial[4][1] + 35) and y_circulo == (matriz_movimientos_y_inicial[4][1] + 35):
                            actualx = 4
                            actualy = 1
                        elif x_circulo == (matriz_movimientos_x_inicial[4][2] + 35) and y_circulo == (matriz_movimientos_y_inicial[4][2] + 35):
                            actualx = 4
                            actualy = 2
                        elif x_circulo == (matriz_movimientos_x_inicial[4][3] + 35) and y_circulo == (matriz_movimientos_y_inicial[4][3] + 35):
                            actualx = 4
                            actualy = 3
                        elif x_circulo == (matriz_movimientos_x_inicial[4][4] + 35) and y_circulo == (matriz_movimientos_y_inicial[4][4] + 35):
                            actualx = 4
                            actualy = 4
                        else:
                            entrar = 0
                        listo = 1

                    mov = int(primer_elemento) / 445
                    mov1 = round(mov)
                    if mov1 < 0:
                        negativo = 1
                    else:
                        negativo = 0
                    mov1_absoluto = abs(mov1)

                    if v != mov1_absoluto:
                        if soltar_agarrar == 1 or soltar_agarrar == 4:
                            if negativo == 0:
                                if electroiman == 0:
                                    x_circulo += 80
                                    print("R:+x")
                                    # Error = UART_write.enviarMovimiento(1)
                                if electroiman == 1:
                                    if entrar == 1:
                                        x_circulo += 80
                                        matriz_movimientos_x[actualx][actualy] += 80
                                        matriz_movimientos_x_inicial[actualx][actualy] += 80
                                        print("R:+x")
                                        # Error = UART_write.enviarMovimiento(1)
                            if negativo == 1:
                                if electroiman == 0:
                                    x_circulo -= 80
                                    print("R:-x")
                                    # Error = UART_write.enviarMovimiento(2)
                                if electroiman == 1:
                                    if entrar == 1:
                                        x_circulo -= 80
                                        matriz_movimientos_x[actualx][actualy] -= 80
                                        matriz_movimientos_x_inicial[actualx][actualy] -= 80
                                        print("R:-x")
                                        # Error = UART_write.enviarMovimiento(2)
                        else:
                            if negativo == 0:
                                if electroiman == 0:
                                    y_circulo += 80
                                    print("R:+y")
                                    # Error = UART_write.enviarMovimiento(3)

                                if electroiman == 1:
                                    if entrar == 1:
                                        y_circulo += 80
                                        matriz_movimientos_y[actualx][actualy] += 80
                                        matriz_movimientos_y_inicial[actualx][actualy] += 80
                                        print("R:+y")
                                        # Error = UART_write.enviarMovimiento(3)
                            if negativo == 1:
                                if electroiman == 0:
                                    y_circulo -= 80
                                    print("R:-y")
                                    # Error = UART_write.enviarMovimiento(4)

                                if electroiman == 1:
                                    if entrar == 1:
                                        y_circulo -= 80
                                        matriz_movimientos_y[actualx][actualy] -= 80
                                        matriz_movimientos_y_inicial[actualx][actualy] -= 80
                                        print("R:-y")
                                        # Error = UART_write.enviarMovimiento(4)

                    time.sleep(0.1)
                    v += 1
                    print(soltar_agarrar)
                    if v == mov1_absoluto or mov1_absoluto == 0:
                        soltar_agarrar = soltar_agarrar + 1
                        posicion += 1
                        contador += 1
                        listo = 0
                        v = 0

                if posicion == (len(movimientosBasura)) and alarma ==202:
                    alarma_verificada = 1
                    iniciar_mapeo = 0
                    alarma = 0
                    posicion = 0
                    movimientosBasura =[]
                    contador = 0
                    soltar_agarrar = 1
                    electroiman = 0
                    v = 0
                    termino_inicial = 0
                    matriz_movimientos_x = [[0 for _ in range(5)] for _ in range(5)]  # Crea las matrices para hacer los moviminetos
                    matriz_movimientos_y = [[0 for _ in range(5)] for _ in range(5)]
                    matriz_movimientos_x_inicial = [[0 for _ in range(5)] for _ in range(5)]
                    matriz_movimientos_y_inicial = [[0 for _ in range(5)] for _ in range(5)]


                if posicion == (len(vectorp)) and alarma == 0:
                        iniciar_movimientos = 2
                pygame.draw.circle(screen, C2, (x_circulo, y_circulo), 20)  # muestra el circulo

            if iniciar_movimientos == 2:
                pygame.draw.circle(screen, C2, (x_circulo, y_circulo), 20)  # muestra el circulo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Evento para detectar clics en los botones
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Mapear.collidepoint((mx, my)):
                    iniciar_mapeo = 1
                if Obstaculo_retirado.collidepoint((mx, my)):
                    if alarma == 202:
                        print(alarma)
                        movimientosBasura = metodoPatron.vaciarBasura()
                        print(movimientosBasura)
                        iniciar_movimientos = 1
                    else:
                        alarma_verificada = 1
                        iniciar_mapeo = 0
                        alarma = 0
                if Iniciar_cal.collidepoint((mx, my)):
                    iniciar_calculos = 1
                if Iniciar_mov.collidepoint((mx, my)):
                    iniciar_movimientos = 1

        pygame.display.update()

def main_menu():
    element_color = (90, 113, 163)  # morado
    element_opacity = 95  # Valor de opacidad (0-255)
    element_rect = pygame.Surface((400, 400), pygame.SRCALPHA)  # SRCALPHA permite la transparencia
    pygame.draw.rect(element_rect, element_color + (element_opacity,), (0, 0, 400, 400))
    while True:
        # Llena la pantalla con el color turquesa
        Fondo = pygame.image.load("Fondo.jpg").convert()
        screen.blit(Fondo, [0, 0])

        # Obtiene la posición del mouse
        mx, my = pygame.mouse.get_pos()
        screen.blit(element_rect, (350, 150))

        # Crea rectángulos para los botones
        button_1 = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 100, 300, 100)
        button_2 = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 50, 300, 100)

        # Comprueba si el mouse está sobre los botones y cambia el color en consecuencia
        if button_1.collidepoint((mx, my)):
            pygame.draw.rect(screen, C7, button_1)
        else:
            pygame.draw.rect(screen, C8, button_1)

        if button_2.collidepoint((mx, my)):
            pygame.draw.rect(screen, C7, button_2)
        else:
            pygame.draw.rect(screen, C8, button_2)

        # Dibuja el texto de los botones en el menú principal
        draw_text("Método patrón", fontbotones, C1, screen_width // 2, screen_height // 2 - 50)
        draw_text("Método reordenar", fontbotones, C1, screen_width // 2, screen_height // 2 + 100)
        draw_text("Inicio", fonttitulo, C1, 550, 100)

        # Eventos para salir del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Evento para detectar clics en los botones
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint((mx, my)):
                    patron()
                elif button_2.collidepoint((mx, my)):
                    reordenar()
        # Actualiza la pantalla para mostrar los cambios
        pygame.display.update()

# Inicia el menú principal
if __name__ == "__main__":
    main_menu()

pygame.quit()
sys.exit()
