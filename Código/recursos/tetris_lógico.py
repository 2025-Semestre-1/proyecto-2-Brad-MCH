matriz = [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]

posicion_central = (3, 3) 

def encontrar_figura(posicion_central, matriz):
    figura = []
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 1:
                figura.append(((i, j), (i - posicion_central[0], j - posicion_central[1])))
    return figura    

def rotar(posicion_central, matriz):
    figura = encontrar_figura(posicion_central, matriz)
    nueva_figura = []
    for (i, j), (x, y) in figura:
        print(f"i: {i}, j: {j}, x: {x}, y: {y}")
        if i < posicion_central[0]:
            nueva_figura.append((i+(1*x), j+(1*y)))
            print("i < posicion_central[0]")
        elif i > posicion_central[0]:
            nueva_figura.append((i-(1*x), j-(1*y)))
            print("i > posicion_central[0]")
        elif i == posicion_central[0] and  j < posicion_central[1]:
            nueva_figura.append((i+y, j+x))
            print("i == posicion_central[0] and j < posicion_central[1]")
        elif i == posicion_central[0] and  j > posicion_central[1]:
            nueva_figura.append((i+y, j-y))
            print("i == posicion_central[0] and j > posicion_central[1]")
        else:
            nueva_figura.append((i, j))
            print("else")

    return nueva_figura

def actualizar_matriz(matriz, figura):
    """
    Actualiza la matriz con la nueva figura.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 1:
                matriz[i][j] = 0
    for (i, j) in figura:
        matriz[i][j] = 1
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

correr_todo()
