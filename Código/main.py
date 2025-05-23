from tkinter import *
from PIL.ImageTk import PhotoImage as ImageTk
from PIL import Image
from os import system
system("cls")

ventana = Tk()
ventana.title("Tetris")
ventana.geometry("360x660")
ventana.config(bg="black")

cubo_gris = Image.open("recursos/cubos/gris.png")
cubo_gris = cubo_gris.resize((30, 30), Image.LANCZOS)
cubo_gris = ImageTk(cubo_gris)

# Crear matriz de 22x12
matriz = [[0 for _ in range(12)] for _ in range(22)]

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
            Label(ventana, image=cubo_gris, bd=0, highlightthickness=0).grid(row=linea, column=columna)


           
# Inicialización
ventana.mainloop()