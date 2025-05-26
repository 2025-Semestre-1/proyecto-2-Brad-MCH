from tkinter import *
from PIL.ImageTk import PhotoImage as ImageTk
from PIL import Image
import random
from os import system
system("clear")

ventana = Tk()
ventana.title("Tetris")
ventana.geometry("660x660")
ventana.config(bg="black")

frame_tetris = Frame(ventana, bg="black")
frame_tetris.grid(row=0, column=0)

cubo_gris = Image.open("recursos/cubos/gris.png")
cubo_gris = cubo_gris.resize((30, 30), Image.LANCZOS)
cubo_gris = ImageTk(cubo_gris)

fondo_juego = Image.open("recursos/fondo_juegoo.png")
fondo_juego = fondo_juego.resize((360, 660), Image.LANCZOS)
fondo_juego = ImageTk(fondo_juego)
fondo = Label(frame_tetris, image=fondo_juego, bd=0, highlightthickness=0)
#fondo.grid(row=0, column=0, rowspan=22, columnspan=12)

# --- Inicialización del área de juego ---

# Crear matriz de 22x12
matriz = [[0 for _ in range(12)] for _ in range(22)]

# Crear una matriz para almacenar referencias de cubos
cubos = [[None for _ in range(12)] for _ in range(22)]

# Poner 1 en los bordes de la matriz
for linea in range(22):
    for columna in range(12):
        if linea == 0:
            matriz[linea][columna] = 1
        
        if columna == 0 or columna == 11:
            matriz[linea][columna] = 1

        if linea == 21:
            matriz[linea][columna] = 1

# Poner bloques grises en la matriz
for linea in range(22):
    for columna in range(12):
        if matriz[linea][columna] == 1:
            cubo = Label(frame_tetris, image=cubo_gris, bd=0, highlightthickness=0)
            cubo.grid(row=linea, column=columna)
            cubos[linea][columna] = cubo

posiciones_iniciales = {"O": [(1,5), (1,6), (2,5), (2,6)],
                        "I": [(1,5), (1,6), (1,7), (1,8)],
                        "T": [(1,4), (1,5), (1,6), (2,5)],
                        "L": [(1,5), (2,5), (3,5), (3,6)],
                        "J": [(1,6), (2,6), (3,6), (3,5)],
                        "S": [(1,5), (1,6), (2,6), (2,7)],
                        "Z": [(1,6), (1,7), (2,5), (2,6)],
                        "U": [(1,4), (2,4), (2,5), (2,6), (1,6)],
                        "+": [(1,5), (2,5), (3,5), (2,4), (2,6)]}

ejes_de_rotacion = {"O": (1,5),
                    "I": (1,6),
                    "T": (1,5),
                    "L": (2,5),
                    "J": (2,6),
                    "S": (1,6),
                    "Z": (1,6),
                    "U": (2,5),
                    "+": (2,5)}


colores = ["azul", "rojo", "verde", "morado", "rosado"]
for i, color in enumerate(colores):
    cubo_color = Image.open(f"recursos/cubos/{color}.png")
    cubo_color = cubo_color.resize((30, 30), Image.LANCZOS)
    cubo_color = ImageTk(cubo_color)
    colores[i] = cubo_color

# --- Funciones auxiliares ---

def imprimir_matriz():
    for fila in matriz:
        print(fila)

def abajo_limite(figura):
    for fila, columna in figura:
        if matriz[fila+1][columna] not in [0, "A"]:
            return True
    return False

def spawn_figura():
    fila_llena()

    for linea in range(22):
        for columna in range(12):
            if matriz[linea][columna] == "A":
                matriz[linea][columna] = 2

    global figura_aleatoria
    global color_aleatorio
    global ejes_de_rotacion
    global eje_de_rotacion

    figura_aleatoria = random.choice(list(posiciones_iniciales.keys()))
    color_aleatorio = random.choice(colores)
    eje_de_rotacion = ejes_de_rotacion[figura_aleatoria]

    for posicion in posiciones_iniciales[figura_aleatoria]:
        fila, columna = posicion
        matriz[fila][columna] = "A"
        cubo = Label(frame_tetris, image=color_aleatorio, bd=0, highlightthickness=0)
        cubo.grid(row=fila, column=columna)
        cubos[fila][columna] = cubo

def imprimir_figura(posiciones, color):
    for posicion in posiciones:
        fila, columna = posicion
        matriz[fila][columna] = "A"
        cubo = Label(frame_tetris, image=color, bd=0, highlightthickness=0)
        cubo.grid(row=fila, column=columna)
        cubos[fila][columna] = cubo

def mover(x, y):
    global nueva_posicion
    global eje_de_rotacion

    nueva_posicion = []
    posicion_vieja = []
    for linea in range(22):
        for columna in range(12):
            if matriz[linea][columna] == "A":
                posicion_vieja += [(linea, columna)]
                nueva_posicion += [(linea + x, columna + y)]

    for fila, columna in nueva_posicion:
        if matriz[fila][columna] not in [0, "A"]:
            return

    for fila, columna in posicion_vieja:
        if matriz[fila][columna] == "A":
            matriz[fila][columna] = 0
            eliminar_cubo(fila, columna)

    roto = True
    for fila, columna in nueva_posicion:
        # Validar que las nuevas posiciones están dentro de los límites
        if 0 <= fila < 22 and 0 <= columna < 12:
            if matriz[fila][columna] == 0:  # Verificar que la posición no esté ocupada
                matriz[fila][columna] = "A"
                cubo = Label(frame_tetris, image=color_aleatorio, bd=0, highlightthickness=0)
                cubo.grid(row=fila, column=columna)
                cubos[fila][columna] = cubo
                
            else:
                roto = False
        else:
            roto = False
    if roto:
        eje_de_rotacion = (eje_de_rotacion[0] + x, eje_de_rotacion[1] + y)

    if abajo_limite(nueva_posicion):
        return spawn_figura()

def eliminar_cubo(fila, columna):
    if cubos[fila][columna]:
        cubos[fila][columna].grid_forget()
        cubos[fila][columna] = None  # Eliminar la referencia

def rotar():
    
    if figura_aleatoria in ["O", "+"]: # Estas figuras no rotan visualmente
        return 

    global vieja_figura
    nueva_figura = []
    figura = []
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == "A":
                figura.append(((i, j), (abs(i - eje_de_rotacion[0]), abs(j - eje_de_rotacion[1]))))

    for (i, j), (x, y) in figura:  

        # Rotación cuando bloque está al norte, sur, este u oeste de la figura central 
        if i < eje_de_rotacion[0] and j == eje_de_rotacion[1]:
            nueva_figura += [(i+x, j+x)]
        elif i > eje_de_rotacion[0] and j == eje_de_rotacion[1]:
            nueva_figura += [(i-x, j-x)]
        elif i == eje_de_rotacion[0] and j < eje_de_rotacion[1]:
            nueva_figura += [(i-y, j+y)]
        elif i == eje_de_rotacion[0] and j > eje_de_rotacion[1]:
            nueva_figura += [(i+y, j-y)]

        # Rotación cuando bloque está en diagonal respecto a la figura central 
        elif i > eje_de_rotacion[0] and j > eje_de_rotacion[1]: 
            nueva_figura += [(i+(y-1), j-(y+1))]
        elif i > eje_de_rotacion[0] and j < eje_de_rotacion[1]:
            nueva_figura += [(i-(x+1), j-(x-1))]
        elif i < eje_de_rotacion[0] and j < eje_de_rotacion[1]:
            nueva_figura += [(i-(y-1), j+(y+1))]
        elif i < eje_de_rotacion[0] and j > eje_de_rotacion[1]:
            nueva_figura += [(i+(x+1), j+(x-1))]

        # El bloque es el eje de rotación, no se mueve
        else:
            nueva_figura += [(i, j)]

    for bloque in nueva_figura:
        fila, columna = bloque
        if fila < 0 or fila >= 22 or columna < 0 or columna >= 12:
            return
        
        if matriz[fila][columna] not in [0, "A"]:
            return
    
    for fila, columna in nueva_posicion:
        if matriz[fila][columna] == "A":
            matriz[fila][columna] = 0
            eliminar_cubo(fila, columna)

    for fila, columna in vieja_figura:
        matriz[fila][columna] = 0
        eliminar_cubo(fila, columna)

    for fila, columna in nueva_figura:
        matriz[fila][columna] = "A"
        cubo = Label(frame_tetris, image=color_aleatorio, bd=0, highlightthickness=0)
        cubo.grid(row=fila, column=columna)
        cubos[fila][columna] = cubo
    
    vieja_figura = nueva_figura

def bajar_automaticamente():
    mover(1, 0)  # Mueve la figura hacia abajo
    frame_tetris.after(500, bajar_automaticamente)  # Llama a esta función nuevamente después de 500 ms

puntuacion_actual = 0
def fila_llena():
    global puntuacion_actual
    for x, fila in enumerate(matriz[1:-1]):
        llena = True
        for y, celda in enumerate(fila[1:-1]):
            if celda == 0: 
                llena = False
        if llena == True:
            for columna in range(1, 11):
                matriz[x+1][columna] = 0
                eliminar_cubo(x+1, columna)
            bajar_figuras(x+1)
            puntuacion_actual += 100
            puntuacion.config(text=f"Puntuación Actual: {puntuacion_actual}pts")

    
def bajar_figuras(fila_destruida):

    for linea in range(fila_destruida-1, 0, -1):
        for columna in range(1, 11):
            matriz[linea+1][columna] = matriz[linea][columna]
            cubo = cubos[linea][columna]
            if cubo:
                cubo.grid(row=linea+1, column=columna)
                cubos[linea+1][columna] = cubo
                cubos[linea][columna] = None  # Eliminar la referencia

eje_de_rotacion = ()
vieja_figura = []
spawn_figura()
bajar_automaticamente()

# --- Eventos de teclado ---
ventana.bind("<Left>", lambda e: mover(0, -1))
ventana.bind("<Right>", lambda e: mover(0, 1))
ventana.bind("<Down>", lambda e: mover(1, 0))
ventana.bind("<Up>", lambda e: rotar())
ventana.bind("<R>", lambda e: rotar())
ventana.bind("<r>", lambda e: rotar())  
ventana.bind("<w>", lambda e: rotar())
ventana.bind("<W>", lambda e: rotar())
ventana.bind("<a>", lambda e: mover(0, -1))
ventana.bind("<A>", lambda e: mover(0, -1))
ventana.bind("<d>", lambda e: mover(0, 1))
ventana.bind("<D>", lambda e: mover(0, 1))
ventana.bind("<s>", lambda e: mover(1, 0))
ventana.bind("<S>", lambda e: mover(1, 0))

# GUI
frame_stats = Frame(ventana, bg="black")
frame_stats.grid(row=0, column=1, sticky="nsew")
frame_stats.grid_rowconfigure(0, weight=0)
frame_stats.grid_columnconfigure(0, weight=1)
puntuacion = Label(frame_stats, text=f"Puntuación Actual: {puntuacion_actual}pts", bg="black",fg="white", font=("Arial", 16, "bold"))
puntuacion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
frame_leaderboard = Frame(frame_stats, bg="black", border=5, relief="groove")
frame_leaderboard.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
frame_leaderboard.grid_columnconfigure(0, weight=1)
Label(frame_leaderboard, text="Top 10 jugadores", bg="black", fg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="we")
jugadores = {}
leaderboard_data = [["Por definir", 0] for _ in range(10)]  


for i in range(10):
    jugadores[f"{i+1}"] = Label(frame_leaderboard, text=f"{i+1}. Por definir: 0pts", bg="black", fg="white", font=("Arial", 12))
    jugadores[f"{i+1}"].grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
# Inicialización
frame_tetris.mainloop()
