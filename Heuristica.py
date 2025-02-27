import math

def distancia_euclidiana(posicion, objetivo):
    """
    Calcula la distancia euclidiana entre dos puntos en un plano 2D.
    """
    fila1, col1 = posicion
    fila2, col2 = objetivo
    return math.sqrt((fila1 - fila2) ** 2 + (col1 - col2) ** 2)

def distancia_manhattan(posicion, objetivo):
    """
    Calcula la distancia de Manhattan entre dos puntos en un plano 2D.
    """
    fila1, col1 = posicion
    fila2, col2 = objetivo
    return abs(fila1 - fila2) + abs(col1 - col2)