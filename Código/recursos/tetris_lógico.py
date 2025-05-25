bloque = 1

matriz = [[8, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, bloque, 0, bloque, 0, 0],
          [0, 0, bloque, bloque, bloque, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]
 
posicion_central = (3, 3) 

def encontrar_figura(posicion_central, matriz):
    figura = []
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == bloque:
                figura.append(((i, j), (abs(i - posicion_central[0]), abs(j - posicion_central[1]))))
    return figura    


def rotar(posicion_central, matriz):
    figura = encontrar_figura(posicion_central, matriz)
    nueva_figura = []
    for (i, j), (x, y) in figura:

        # Rotación cuando bloque está al norte, sur, este u oeste de la figura central 
        if i < posicion_central[0] and j == posicion_central[1]:
            nueva_figura.append((i+x, j+x))
        elif i > posicion_central[0] and j == posicion_central[1]:
            nueva_figura.append((i-x, j-x))
        elif i == posicion_central[0] and  j < posicion_central[1]:
            nueva_figura.append((i-y, j+y))
        elif i == posicion_central[0] and  j > posicion_central[1]:
            nueva_figura.append((i+y, j-y))

        # Rotación cuando bloque está en diagonal respecto a la figura central 
        elif i > posicion_central[0] and j > posicion_central[1]: 
            nueva_figura.append((i+(y-1), j-(y+1)))
        elif i > posicion_central[0] and j < posicion_central[1]:
            nueva_figura.append((i-(x+1), j-(x-1)))
        elif i < posicion_central[0] and j < posicion_central[1]:
            nueva_figura.append((i-(y-1), j+(y+1)))
        elif i < posicion_central[0] and j > posicion_central[1]:
            nueva_figura.append((i+(x+1), j+(x-1)))

        # El bloque es el eje de rotación, no se mueve
        else:
            nueva_figura.append((i, j))


    return nueva_figura

def actualizar_matriz(matriz, figura):
    """
    Actualiza la matriz con la nueva figura.
    """
    for (x, y) in figura:
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if i == x and j == y:
                    if matriz[i][j] != 0:
                        return matriz

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == bloque:
                matriz[i][j] = 0
    for (i, j) in figura:
        matriz[i][j] = bloque
    return matriz

def imprimir_matriz(matriz):
    """
    Imprime la matriz en la consola.
    """
    for fila in matriz:
        print(fila)
    print("\n")

def correr_todo():
    """
    Función principal que ejecuta el programa.
    """
    global matriz
    print("Matriz original:")
    imprimir_matriz(matriz)
    
    figura = encontrar_figura(posicion_central, matriz)
    print("Figura encontrada:")
    print(figura)
    
    nueva_figura = rotar(posicion_central, matriz)
    print("Nueva figura:")
    print(nueva_figura)
    
    matriz = actualizar_matriz(matriz, nueva_figura)
    print("Matriz actualizada:")
    imprimir_matriz(matriz)


while True:
    print("Matriz original:")
    imprimir_matriz(matriz)


    input("Presiona Enter para rotar la figura...")
    
    correr_todo()
