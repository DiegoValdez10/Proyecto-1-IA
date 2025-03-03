import random
import copy

class Laberinto:
    def __init__(self, ruta_archivo):
        self.matriz = []
        self.inicio = None
        self.salida = None
        self.cargar_laberinto(ruta_archivo)
    
    def cargar_laberinto(self, ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
        
        self.matriz = [] 
        for i, linea in enumerate(lineas):
            fila = []
            valores = linea.strip().split(',')
            for j, valor in enumerate(valores):
                valor = valor.strip()
                fila.append(valor)
                if valor == '2': 
                    self.inicio = (i, j)
                elif valor == '3': 
                    self.salida = (i, j)
            self.matriz.append(fila)
    
    def es_camino_valido(self, posicion):
        fila, columna = posicion

        if fila < 0 or fila >= len(self.matriz) or columna < 0 or columna >= len(self.matriz[0]):
            return False

        return self.matriz[fila][columna] != '1'
    
    def obtener_vecinos(self, posicion):
        fila, columna = posicion
        vecinos = []

        movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for df, dc in movimientos:
            nueva_posicion = (fila + df, columna + dc)
            if self.es_camino_valido(nueva_posicion):
                vecinos.append(nueva_posicion)
        
        return vecinos
    
    def generar_laberinto_aleatorio(self, ruta_salida):

        matriz_nueva = copy.deepcopy(self.matriz)
        posiciones_validas = []
        for i in range(len(matriz_nueva)):
            for j in range(len(matriz_nueva[0])):
                if matriz_nueva[i][j] == '0':
                    posiciones_validas.append((i, j))
        fila_salida, col_salida = self.salida
        matriz_nueva[fila_salida][col_salida] = '0'
        if posiciones_validas:
            nueva_salida = random.choice(posiciones_validas)
            fila_nueva, col_nueva = nueva_salida
            matriz_nueva[fila_nueva][col_nueva] = '3'
        else:
            matriz_nueva[fila_salida][col_salida] = '3'
            nueva_salida = (fila_salida, col_salida)

        with open(ruta_salida, 'w') as archivo:
            for fila in matriz_nueva:
                archivo.write(','.join(fila) + '\n')
        
        return nueva_salida