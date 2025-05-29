from tkinter import *
from PIL.ImageTk import PhotoImage as ImageTk
from PIL import Image
import random
import time

"""
AVISO IMPORTANTE PARA LA DOCUMENTACIÓN INTERNA:

En este código, toda función que no recibe parametros es una función de tipo VOID, es decir, no retorna nada.
Por ende, su entrada es nula su salida es nula y sus restricciones son nulas. 

Este código tiene 900 lineas de funciones, de las cuales 800 son de tipo VOID, por lo que para no
aglomerar el código, si una función es de tipo VOID y no tiene comentarios, se puede asumir que sus entradas, salidas y restricciones son nulas.

Las funciones que no sigan esta regla, tendrán comentarios que indiquen sus entradas, salidas y restricciones.
"""

ventana = Tk()
ventana.title("Tetris")
ventana.geometry("660x660")
ventana.resizable(False, False)
ventana.config(bg="black")

# --- Cargar imágenes ---
cubo_gris = Image.open("recursos/cubos/gris.png")
cubo_gris = cubo_gris.resize((30, 30), Image.LANCZOS)
cubo_gris = ImageTk(cubo_gris)
fondo_juego = Image.open("recursos/fondo_juego.jpg")
fondo_juego = fondo_juego.resize((360, 660), Image.LANCZOS)
fondo_juego = ImageTk(fondo_juego)
fondo_menu = Image.open("recursos/fondo_menu.png")
fondo_menu = fondo_menu.resize((660, 660), Image.LANCZOS)
fondo_menu = ImageTk(fondo_menu)
colores = ["azul", "rojo", "verde", "morado", "rosado"]
for i, color in enumerate(colores):
    cubo_color = Image.open(f"recursos/cubos/{color}.png")
    cubo_color = cubo_color.resize((30, 30), Image.LANCZOS)
    cubo_color = ImageTk(cubo_color)
    colores[i] = cubo_color

# --- Variables lógicas ---
matriz = [[0 for _ in range(12)] for _ in range(22)]
cubos = [[None for _ in range(12)] for _ in range(22)]

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

# --- Variables Globales ---

scores = {}
usuario = ""
archivo_juego = ""
estado_juego = False
controles_juego = False
ultimo_movimiento = 0
ultimo_rotar = 0
debounce_tiempo = 0.1
puntuacion_actual = 0
eje_de_rotacion = ()
vieja_figura = []
ultimo_retroceso = 0
veces_retroceso = 0


# --- Funciones auxiliares ---

"""
Entrada: lista
Salida: entero (longitud de la lista)
Restricciones: La entrada debe ser una lista.
"""
def len_lista(lista):
    contador = 0
    for _ in lista:
        contador += 1
    return contador

def reiniciar_matriz():
    global matriz, cubos
    # Poner 1 en los bordes de la matriz
    for linea in range(22):
        for columna in range(12):
            if linea == 0:
                matriz[linea][columna] = 1
            
            if columna == 0 or columna == 11:
                matriz[linea][columna] = 1

            if linea == 21:
                matriz[linea][columna] = 1

    # Poner obstaculos en la matriz
    for linea in range(5, 7 ):
        for columna in range(1, 11):
            if random.random() < 0.1:
                matriz[linea][columna] = 1

    # Poner bloques grises en la matriz
    for linea in range(22):
        for columna in range(12):
            if matriz[linea][columna] == 1:
                cubo = Label(frame_tetris, image=cubo_gris, bd=0, highlightthickness=0)
                cubo.grid(row=linea, column=columna)
                cubos[linea][columna] = cubo

def cargar_partida():
    global puntuacion_actual
    partida_data = open(f"data/data_partidas/{archivo_juego}", "r")
    partida_lines = partida_data.readlines()
    partida_data.close()
    partida_lines = [linea.strip().split() for linea in partida_lines]

    if len_lista(partida_lines) == 0:
        # Poner 1 en los bordes de la matriz
        for linea in range(22):
            for columna in range(12):
                if linea == 0:
                    matriz[linea][columna] = 1
                
                if columna == 0 or columna == 11:
                    matriz[linea][columna] = 1

                if linea == 21:
                    matriz[linea][columna] = 1

        # Poner obstaculos en la matriz
        for linea in range(5, 7 ):
            for columna in range(1, 11):
                if random.random() < 0.1:
                    matriz[linea][columna] = 1

        # Poner bloques grises en la matriz
        for linea in range(22):
            for columna in range(12):
                if matriz[linea][columna] == 1:
                    cubo = Label(frame_tetris, image=cubo_gris, bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
    else:
        for linea in range(22):
            for columna in range(12):
                if partida_lines[linea][columna] == "1":
                    matriz[linea][columna] = 1
                    cubo = Label(frame_tetris, image=cubo_gris, bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
                elif partida_lines[linea][columna] == "2":
                    matriz[linea][columna] = 2
                    cubo = Label(frame_tetris, image=colores[0], bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
                elif partida_lines[linea][columna] == "3":
                    matriz[linea][columna] = 3
                    cubo = Label(frame_tetris, image=colores[1], bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
                elif partida_lines[linea][columna] == "4":
                    matriz[linea][columna] = 4
                    cubo = Label(frame_tetris, image=colores[2], bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
                elif partida_lines[linea][columna] == "5":
                    matriz[linea][columna] = 5
                    cubo = Label(frame_tetris, image=colores[3], bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
                elif partida_lines[linea][columna] == "6":
                    matriz[linea][columna] = 6
                    cubo = Label(frame_tetris, image=colores[4], bd=0, highlightthickness=0)
                    cubo.grid(row=linea, column=columna)
                    cubos[linea][columna] = cubo
            
            puntuacion_actual = int(partida_lines[-1][0])
            puntuacion.config(text=f"Puntuación Actual: {puntuacion_actual}pts")          

def abajo_limite(figura):
    for fila, columna in figura:
        if matriz[fila+1][columna] not in [0, "A"]:
            return True
    return False

def spawn_figura():
    global estado_juego

    desactivar_controles()
    fila_llena()
    activar_controles()

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
        if matriz[fila][columna] not in [0, "A"]:
            estado_juego = False
            return perdio()
            

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
            nueva_posicion = posicion_vieja
            posicion_vieja = []
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
        cubos[fila][columna].destroy()  
        cubos[fila][columna] = None 

def rotar():
    global ultimo_movimiento
    tiempo_actual = time.time()

    if tiempo_actual - ultimo_movimiento < debounce_tiempo:
        ventana.update()
        return

    ultimo_movimiento = tiempo_actual

    if figura_aleatoria in ["O", "+"]:
        return 

    global vieja_figura
    nueva_figura = []
    figura = []
    
    posicion_actual = []
    for i in range(22):
        for j in range(12):
            if matriz[i][j] == "A":
                figura += [((i, j), (abs(i - eje_de_rotacion[0]), abs(j - eje_de_rotacion[1])))]
                posicion_actual += [(i, j)]  

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

    for fila, columna in posicion_actual:
        if matriz[fila][columna] == "A":
            matriz[fila][columna] = 0
            eliminar_cubo(fila, columna)

    for fila, columna in nueva_figura:
        matriz[fila][columna] = "A"
        cubo = Label(frame_tetris, image=color_aleatorio, bd=0, highlightthickness=0)
        cubo.grid(row=fila, column=columna)
        cubos[fila][columna] = cubo
    
    vieja_figura = nueva_figura

def bajar_automaticamente():
    global estado_juego
    global controles_juego

    if not estado_juego:
        desactivar_controles()
        return frame_tetris.after(500, bajar_automaticamente)

    aumento_velocidad = puntuacion_actual // 200
    velocidad = 500 - aumento_velocidad * 50

    if velocidad < 100:
        velocidad = 100

    mover(1, 0)  
    activar_controles()
    frame_tetris.after(velocidad, bajar_automaticamente)  
    
def fila_llena():
    global puntuacion_actual
    for x, fila in enumerate(matriz[1:-1]):
        llena = True
        for y, celda in enumerate(fila[1:-1]):
            if celda == 0: 
                llena = False
        if llena == True:
            bordes_verdes()
            for columna in range(1, 11):
                matriz[x+1][columna] = 0
                eliminar_cubo(x+1, columna)
            bajar_figuras(x+1)
            puntuacion_actual += 100
            puntuacion.config(text=f"Puntuación Actual: {puntuacion_actual}pts")

def bajar_figuras(fila_destruida):
    for linea in range(fila_destruida-1, 0, -1):
        for columna in range(1, 11):
            cubo = cubos[linea][columna]
            if cubo:
                if cubo.cget('image') != str(cubo_gris):
                    matriz[linea+1][columna] = matriz[linea][columna]
                    matriz[linea][columna] = 0
                    cubo.grid(row=linea+1, column=columna)
                    cubos[linea+1][columna] = cubo
                    cubos[linea][columna] = None 

def inicio():
    cargar_partida()
    desactivar_controles()
    spawn_figura()
    activar_controles()
    bindings_inicio()
    frame_tetris.after(1000, bajar_automaticamente)

def iniciar_juego():
    limpiar_menu()
    cargar_leaderboard()
    menu_principal.grid_forget()
    frame_tetris.after(500, inicio)

def menu_login():

    boton_iniciar.lower()
    boton_salir.lower()
    fondo_menu_label.grid(columnspan=2, rowspan=4, sticky="nsew")
    label_username.grid(row=1, column=0, padx=10, pady=10, sticky="s")
    entryBox_username.grid(row=1, column=1, padx=10, pady=10, sticky="s")
    label_password.grid(row=2, column=0, padx=10, pady=10, sticky="n")
    entryBox_password.grid(row=2, column=1, padx=10, pady=10, sticky="n")
    boton_iniciar_sesion.grid(row=3, column=0, padx=10, pady=10, sticky="ne")
    boton_registrarse.grid(row=3, column=1, padx=10, pady=10, sticky="n")

def usuario_incorrecto():
    entryBox_username.delete(0, END)
    entryBox_password.delete(0, END)
    entryBox_username.insert(0, "Usuario incorrecto")
    entryBox_username.config(fg="red")
    menu_principal.after(2000, lambda: (entryBox_username.config(fg="white"), entryBox_username.delete(0, END)))
    
def contrasena_incorrecta():
    entryBox_password.delete(0, END)
    entryBox_password.insert(0, "Jaja, no sabe") # Esto no se mostrará
    entryBox_password.config(fg="red")
    menu_principal.after(2000, lambda: (entryBox_password.config(fg="white"), entryBox_password.delete(0, END)))

def limpiar_menu():
    entryBox_username.config(fg="white")
    entryBox_password.config(fg="white")
    entryBox_username.delete(0, END)
    entryBox_password.delete(0, END)
    label_username.grid_forget()
    entryBox_username.grid_forget()
    label_password.grid_forget()
    entryBox_password.grid_forget()
    boton_iniciar_sesion.grid_forget()
    boton_registrarse.grid_forget()
    fondo_menu_label.grid(rowspan=3, columnspan=1)

    boton_iniciar.lift()
    boton_salir.lift()

def login_correcto():
    entryBox_username.delete(0, END)
    entryBox_password.delete(0, END)
    entryBox_username.insert(0, "¡Regresaste!")
    entryBox_username.config(fg="#00FF00")
    menu_principal.after(2000, lambda: iniciar_juego())
    
def iniciar_sesion():
    global usuario, archivo_juego
    username = entryBox_username.get()
    password = entryBox_password.get()

    if username == "" or password == "":
        entryBox_username.delete(0, END)
        entryBox_password.delete(0, END)
        entryBox_username.insert(0, "Campos vacíos 🚫")
        entryBox_username.config(fg="red")
        menu_principal.after(2000, lambda: (entryBox_username.config(fg="white"), entryBox_username.delete(0, END)))
        return

    data = open("data/user_data.txt", "r")
    data_lines = data.readlines()
    data.close()

    usuarios = {}

    for linea in data_lines:
        if linea.split()[0] != "":
            usuarios[linea.split()[0]] = [linea.split()[1], linea.split()[3]]

    if username in usuarios:
        if usuarios[username][0] == password:
            usuario = username 
            archivo_juego = usuarios[username][1]
            login_correcto()
        else:
            contrasena_incorrecta()
    else:
        usuario_incorrecto()

"""
Entrada: lista_listas (lista de listas con formato [[usuario, score], ...])

Salida: tupla (usuario_maximo, maximo, indice_maximo) 
    Usuarion_maximo: nombre del usuario con la puntuación más alta.
    maximo: puntuación más alta.
    indice_maximo: índice del usuario con la puntuación más alta en la lista original.

Restricciones: La entrada debe ser una lista de listas donde cada sublista contiene un usuario y su puntuación.
"""
def maximo(lista_listas):
    usuario_maximo = "Por definir"
    maximo = 0
    indice_maximo = 0
    
    for i, [usuario, score] in enumerate(lista_listas):
        if score > maximo:
            maximo = score
            usuario_maximo = usuario
            indice_maximo = i 
    
    return usuario_maximo, maximo, indice_maximo

"""
Entrada: lista_listas (lista de listas)
Salida: entero (longitud de la lista de listas)
Restricciones: La entrada debe ser una lista de listas.
"""
def len_listas(lista_listas):
    contador = 0
    for _ in lista_listas:
        contador += 1
    return contador

def cargar_leaderboard():
    global leaderboard_data
    data = open("data/user_data.txt", "r")
    data_lines = data.readlines()
    data.close()

    scores = []
    for linea in data_lines:
        usuario = linea.split()[0]
        score = int(linea.split()[2])
        scores += [[usuario, score]]
    
    for i in range(10):
        if len_listas(scores) > 0:
            usuario_maximo, maximo_puntaje, indice = maximo(scores)
            scores.pop(indice)
            leaderboard_data[i] = [usuario_maximo, maximo_puntaje]
            jugadores[f"{i}"].config(text=f"{i+1}. {usuario_maximo}: {maximo_puntaje}pts")

        else:
            leaderboard_data[i][0] = "Por definir"
            leaderboard_data[i][1] = 0
            jugadores[f"{i}"].config(text=f"{i+1}. Por definir: 0pts")

"""
Entrada: String (usuario_) nombre de usuario a verificar
Salida: Booleano (True si el usuario existe, False si no)
Restricciones: El usuario debe de ser un string
"""
def usuario_existe(usuario_):
    global usuario
    global archivo_juego
    data = open("data/user_data.txt", "r")
    data_lines = data.readlines()
    data.close()

    for linea in data_lines:
        if linea.strip() == "":
            continue
        
        if linea.split()[0] == usuario_:
            return True
    return False

def error_usuario_existente():
    entryBox_username.delete(0, END)
    entryBox_username.insert(0, "Usuario ya existe")
    entryBox_username.config(fg="red")
    menu_principal.after(2000, lambda: (entryBox_username.config(fg="white"), entryBox_username.delete(0, END)))

def registro_exitoso():
    entryBox_username.delete(0, END)
    entryBox_password.delete(0, END)
    entryBox_username.insert(0, "¡Registro exitoso!")
    entryBox_username.config(fg="#00FF00")
    menu_principal.after(2000, lambda: (entryBox_username.config(fg="white"), entryBox_username.delete(0, END), iniciar_juego()))

def registrar_usuario():
    global usuario, archivo_juego
    username = entryBox_username.get()
    password = entryBox_password.get()

    if username == "" or password == "":
        entryBox_username.delete(0, END)
        entryBox_password.delete(0, END)
        entryBox_username.insert(0, "Campos vacíos 🚫")
        entryBox_username.config(fg="red")
        menu_principal.after(2000, lambda: (entryBox_username.config(fg="white"), entryBox_username.delete(0, END)))
        return

    def limpiar_campos():
        entryBox_username.config(fg="white")
        entryBox_password.config(fg="white")
        entryBox_username.delete(0, END)
        entryBox_password.delete(0, END)


    if " " in username or " " in password:
        entryBox_username.delete(0, END)
        entryBox_password.delete(0, END)
        entryBox_username.insert(0, "Espacios no 🚫")
        entryBox_username.config(fg="red")
        menu_principal.after(2000, limpiar_campos)
        return

    if usuario_existe(username):
        return error_usuario_existente()
    
    usuario = username
    archivo_juego = username + ".txt"

    data = open("data/user_data.txt", "a")
    data.write(f"{username} {password} 0 {username}.txt\n")
    data.close()

    data_partida = open(f"data/data_partidas/{username}.txt", "w")
    data_partida.close()
    return registro_exitoso()

def bordes_verdes():
    for columna in range(12):
        cubos[0][columna].config(image=colores[2])
        cubos[21][columna].config(image=colores[2])
    
    for fila in range(1, 21):
        cubos[fila][0].config(image=colores[2])
        cubos[fila][11].config(image=colores[2])

    ventana.after(500, bordes_grises)  

def bordes_rojos():
    for columna in range(12):
        cubos[0][columna].config(image=colores[1])
        cubos[21][columna].config(image=colores[1])
    
    for fila in range(1, 21):
        cubos[fila][0].config(image=colores[1])
        cubos[fila][11].config(image=colores[1])

def bordes_grises():
    for columna in range(12):
        cubos[0][columna].config(image=cubo_gris)
        cubos[21][columna].config(image=cubo_gris)
    
    for fila in range(1, 21):
        cubos[fila][0].config(image=cubo_gris)
        cubos[fila][11].config(image=cubo_gris)

def bordes_azules():
    for columna in range(12):
        cubos[0][columna].config(image=colores[0])
        cubos[21][columna].config(image=colores[0])
    
    for fila in range(1, 21):
        cubos[fila][0].config(image=colores[0])
        cubos[fila][11].config(image=colores[0])

def perdio():
    bordes_rojos()

    data = open("data/user_data.txt", "r")
    data_lines = data.readlines()
    data.close()
    
    for linea in data_lines:
        if linea.split()[0] == usuario:
            puntaje = int(linea.split()[2])
            if puntuacion_actual > puntaje:
                linea = f"{usuario} {linea.split()[1]} {puntuacion_actual} {archivo_juego}\n"
            else:
                linea = f"{usuario} {linea.split()[1]} {puntaje} {archivo_juego}\n"
        else:
            linea = linea
    
    return mostrar_pantalla_perdio()

def toggle_pausa():
    global estado_juego
    if  not estado_juego:
        pausa.config(text="Pausar Juego")
        bordes_grises()
    else:
        pausa.config(text="Continuar Juego")
        bordes_azules()
    estado_juego = not estado_juego

def desactivar_controles():
        ventana.unbind("<Left>")
        ventana.unbind("<Right>")
        ventana.unbind("<Down>")
        ventana.unbind("<Up>")
        ventana.unbind("<R>")
        ventana.unbind("<r>")
        ventana.unbind("<w>")
        ventana.unbind("<W>")
        ventana.unbind("<a>")
        ventana.unbind("<A>")
        ventana.unbind("<d>")
        ventana.unbind("<D>")
        ventana.unbind("<s>")
        ventana.unbind("<S>")

def activar_controles():
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

"""
Entrada: Nada
Salida: String (matriz_string) que representa la matriz de cubos para guardar en un archivo.
Restricciones: Ninguna
"""
def crear_matriz_para_guardar():
    matriz_guardar = [[0 for _ in range(12)] for _ in range(22)]

    """"
    Colores
    Azul: 2
    Rojo: 3
    Verde: 4
    Morado: 5
    Rosado: 6
    Grises: 1
    """

    for fila in range(22):
        for columna in range(12):
            cubo = cubos[fila][columna]
            if not cubo:
                pass
            elif matriz[fila][columna] == "A":
                pass
            elif cubo.cget('image') == str(cubo_gris):
                matriz_guardar[fila][columna] = 1
            elif cubo.cget('image') == str(colores[0]):
                matriz_guardar[fila][columna] = 2
            elif cubo.cget('image') == str(colores[1]):
                matriz_guardar[fila][columna] = 3
            elif cubo.cget('image') == str(colores[2]):
                matriz_guardar[fila][columna] = 4
            elif cubo.cget('image') == str(colores[3]):
                matriz_guardar[fila][columna] = 5
            elif cubo.cget('image') == str(colores[4]):
                matriz_guardar[fila][columna] = 6

    matriz_string = ""
    for fila in matriz_guardar:
        for columna in fila:
            matriz_string += str(columna) + " "
        matriz_string += "\n"
    matriz_string += f"\n{puntuacion_actual}\n"
    
    return matriz_string.strip()

def actualizar_archivo_guardado():
    matriz_guardar = crear_matriz_para_guardar()
    partida_guardada = open(f"data/data_partidas/{archivo_juego}", "w")
    partida_guardada.write(matriz_guardar)
    partida_guardada.close()

def actualizar_user_data():
    global puntuacion_actual
    user_data = open("data/user_data.txt", "r")
    user_data_lines = user_data.readlines()
    user_data.close()

    for i, linea in enumerate(user_data_lines):              
        if linea.split()[0] == usuario:                                                 
            puntaje_actual_archivo = int(linea.split()[2]) 
            if puntuacion_actual > puntaje_actual_archivo:  
                user_data_lines[i] = f"{usuario} {linea.split()[1]} {puntuacion_actual} {archivo_juego}\n" 
            break  
    
    user_data = open("data/user_data.txt", "w")
    user_data.writelines(user_data_lines)
    user_data.close()    

def guardar_y_salir():
    global estado_juego
    estado_juego = False
    actualizar_archivo_guardado()
    actualizar_user_data()
    crear_matriz_para_el_profe()
    ventana.quit()

def reiniciar_juego():

    actualizar_archivo_guardado()
    actualizar_user_data()
    crear_matriz_para_el_profe()
    cargar_leaderboard()
    toggle_pausa()

    global matriz, cubos, puntuacion_actual, estado_juego
    matriz = [[0 for _ in range(12)] for _ in range(22)]
    for fila in range(22):
        for columna in range(12):
            if cubos[fila][columna]:
                eliminar_cubo(fila, columna)
        
    
    puntuacion_actual = 0
    puntuacion.config(text=f"Puntuación Actual: {puntuacion_actual}pts")
    estado_juego = False
    pausa.config(text="Iniciar Juego")

    reiniciar_matriz()
    spawn_figura()

def crear_matriz_para_el_profe():
    matriz_profe = [[0 for _ in range(12)] for _ in range(22)]
    for fila in range(22):
        for columna in range(12):
            if matriz[fila][columna] == 1:
                matriz_profe[fila][columna] = "+"
            elif matriz[fila][columna] == "A":
                matriz_profe[fila][columna] = 0
            elif matriz[fila][columna] == 0:
                matriz_profe[fila][columna] = 0
            else:
                matriz_profe[fila][columna] = 1

    matriz_string = ""
    for fila in matriz_profe:
        for columna in fila:
            matriz_string += str(columna) + " "
        matriz_string += "\n"
    
    data_matriz_profe = open(f"data/matrices_Profe/{usuario}.txt", "w")
    data_matriz_profe.write(matriz_string.strip())
    data_matriz_profe.close()

def mostrar_pantalla_perdio():
    frame_perdio = Frame(frame_tetris, bg="black")
    frame_perdio.place(relx=0, rely=0, relwidth=1, relheight=1)

    label_perdio = Label(
        frame_perdio,
        text="Skill Issue",
        bg="black",
        fg="red",
        font=("Unispace", 32, "bold")
    )
    label_perdio.pack(pady=60)

    def jugar_otra_vez():
        frame_perdio.destroy()
        reiniciar_juego()

    boton_reintentar = Button(
        frame_perdio,
        text="Jugar otra vez",
        command=jugar_otra_vez,
        bg="black",
        fg="white",
        font=("Unispace", 20, "bold"),
        border=5,
        relief="groove"
    )
    boton_reintentar.pack(pady=20)

    def salir_perdio():
        data_usuario = open(f"data/data_partidas/{usuario}.txt", "w")
        data_usuario.close()

        ventana.quit()

    boton_salir_perdio = Button(
        frame_perdio,
        text="Salir",
        command=salir_perdio,
        bg="black",
        fg="white",
        font=("Unispace", 20, "bold"),
        border=5,
        relief="groove"
    )
    boton_salir_perdio.pack(pady=10)

def eliminar_obstaculos():
    global matriz, cubos, ultimo_retroceso, veces_retroceso
    tiempo_actual = time.time()
    if tiempo_actual - ultimo_retroceso < 0.5:
        veces_retroceso += 1
    else:
        veces_retroceso = 1
    ultimo_retroceso = tiempo_actual

    if veces_retroceso >= 3:
        for fila in range(1, 21):
            for columna in range(1, 11):
                if matriz[fila][columna] == 1:
                    matriz[fila][columna] = 0
                    eliminar_cubo(fila, columna)

def bindings_inicio():
    ventana.bind("<Escape>", lambda e: toggle_pausa())
    ventana.bind("<space>", lambda e: toggle_pausa())
    ventana.bind("<BackSpace>", lambda e: eliminar_obstaculos())

# GUI
frame_tetris = Frame(ventana, bg="black")
fondo = Label(frame_tetris, image=fondo_juego, bd=0, highlightthickness=0)
frame_stats = Frame(ventana, bg="black")
puntuacion = Label(frame_stats, text=f"Puntuación Actual: {puntuacion_actual}pts", bg="black",fg="white", font=("Arial", 16, "bold"))
frame_leaderboard = Frame(frame_stats, bg="black", border=5, relief="groove")
label_top_10 = Label(frame_leaderboard, text="Top 10 jugadores", bg="black", fg="white", font=("Arial", 14, "bold"))
pausa = Button(frame_stats, text="Iniciar Juego", command=toggle_pausa, bg="black", fg="white", font=("Unispace", 16, "bold"), border=5, relief="groove")
guardar = Button(frame_stats, text="Guardar y salir", command=guardar_y_salir, bg="black", fg="white", font=("Unispace", 16, "bold"), border=5, relief="groove")
menu_principal = Frame(ventana, bg="black")
fondo_menu_label = Label(menu_principal, image=fondo_menu, bd=0, highlightthickness=0)
boton_iniciar = Button(menu_principal, text="Jugar", command=menu_login, bg="black", fg="white", font=("Unispace", 30, "bold"), border=5, relief="groove")
boton_salir = Button(menu_principal, text="Salir", command=ventana.quit, bg="black", fg="white", font=("Unispace", 30, "bold"), border=5, relief="groove")
label_username = Label(menu_principal, text="Usuario", bg="black", fg="white", font=("Unispace", 20, "bold"), relief="raised", border=5, padx=10)
entryBox_username = Entry(menu_principal, bg="black", fg="white", font=("Unispace", 20), border=5, relief="groove")
label_password = Label(menu_principal, text="Contraseña", bg="black", fg="white", font=("Unispace", 20, "bold"), relief="raised", border=5, padx=10)
entryBox_password = Entry(menu_principal, show="*", bg="black", fg="white", font=("Unispace", 20), border=5, relief="groove")
boton_iniciar_sesion = Button(menu_principal, text="Iniciar Sesión", command=iniciar_sesion, bg="black", fg="white", font=("Unispace", 16, "bold"), border=5, relief="groove")
boton_registrarse = Button(menu_principal, text="Registrarse", command=registrar_usuario, bg="black", fg="white", font=("Unispace", 16, "bold"), border=5, relief="groove")

# Grids
frame_tetris.grid(row=0, column=0)
fondo.grid(row=0, column=0, rowspan=22, columnspan=12)
frame_stats.grid(row=0, column=1, sticky="nsew")
frame_stats.grid_rowconfigure(0, weight=0)
frame_stats.grid_columnconfigure(0, weight=1)
puntuacion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
frame_leaderboard.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
frame_leaderboard.grid_columnconfigure(0, weight=1)
label_top_10.grid(row=0, column=0, padx=5, pady=5, sticky="we")
pausa.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
guardar.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
menu_principal.grid(row=0, column=0, columnspan=2, sticky="nsew")
fondo_menu_label.grid(row=0, column=0, rowspan=3)
boton_iniciar.grid(row=1, column=0, padx=10, pady=10, sticky="s")
boton_salir.grid(row=2, column=0, padx=10, pady=10, sticky="n")

# Variables que requieren de la GUI para ser inicializadas
jugadores = {}
leaderboard_data = [["Por definir", 0] for _ in range(10)]
for i in range(10):
    jugadores[f"{i}"] = Label(frame_leaderboard, text=f"{i+1}. Por definir: 0pts", bg="black", fg="white", font=("Arial", 12))
    jugadores[f"{i}"].grid(row=i+1, column=0, padx=5, pady=5, sticky="w")

# iniciar el juego
desactivar_controles()
ventana.mainloop()