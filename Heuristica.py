import math

def distancia_euclidiana(posicion, objetivo):

    fila1, col1 = posicion
    fila2, col2 = objetivo
    return math.sqrt((fila1 - fila2) ** 2 + (col1 - col2) ** 2)

def distancia_manhattan(posicion, objetivo):
    fila1, col1 = posicion
    fila2, col2 = objetivo
    return abs(fila1 - fila2) + abs(col1 - col2)