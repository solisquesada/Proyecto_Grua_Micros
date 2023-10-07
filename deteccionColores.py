from PIL import Image

# Abre la imagen
# Para las pruebas iniciales se usa una imagen hecha en excel de 537x149 pixeles
imagen = Image.open("tu_imagen.jpg")

# Se definen las coordenadas de los pixeles a analizar:
coordenadas = [(50, 30), (50, 78), (50, 126), (50, 174), (50, 222), (50, 318), (50, 366), (50, 414), (50, 462), (50, 510),
               (70, 30), (70, 78), (70, 126), (70, 174), (70, 222), (70, 318), (70, 366), (70, 414), (70, 462), (70, 510),
               (90, 30), (90, 78), (90, 126), (90, 174), (90, 222), (90, 318), (90, 366), (90, 414), (90, 462), (90, 510),
               (110, 30), (110, 78), (110, 126), (110, 174), (110, 222), (110, 318), (110, 366), (110, 414), (110, 462), (110, 510),
               (130, 30), (130, 78), (130, 126), (130, 174), (130, 222), (130, 318), (130, 366), (130, 414), (130, 462), (130, 510)]

# Función para comparar el color de un píxel con tolerancia (opcional)
def verificar_color(pixel, colores, tolerancia=0):
    for nombre, valor in colores.items():
        diferencia = sum(abs(pixel[i] - valor[i]) for i in range(3))  # Calcula la diferencia en cada componente de color
        if diferencia <= tolerancia:
            return nombre
    return "Color desconocido"

# Definir los valores de color en formato (R, G, B)
colores = {
    "BLANCO": (255, 255, 255),
    "ROJO": (255, 0, 0),
    "VERDE": (169, 208, 142),
    "AZUL": (142, 169, 219)
}

# Definir la tolerancia permitida (ajusta este valor según tus necesidades)
tolerancia = 30

# Verifica los colores en las coordenadas especificadas
i=1
for coordenada in coordenadas:
    y, x = coordenada  # Intercambia el orden de las coordenadas
    pixel = imagen.getpixel((x, y))  # Intercambia el orden de las coordenadas al llamar a getpixel
    nombre_color = verificar_color(pixel[:3], colores, tolerancia)  # Compara solo los tres primeros componentes (R, G, B)
    if(nombre_color!="BLANCO"):
        print(f"En {i} se encontró el color: {nombre_color}")
    i=i+1