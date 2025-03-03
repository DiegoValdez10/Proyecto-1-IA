# main.py
from Laberinto import Laberinto
from Busqueda import busqueda_amplitud, busqueda_profundidad, busqueda_voraz, busqueda_a_estrella
from Heuristica import distancia_euclidiana, distancia_manhattan
import time
import random

def imprimir_resultado(nombre_algoritmo, resultado):
    print(f"\n=== Resultados de {nombre_algoritmo} ===")
    print(f"Nodos visitados: {resultado['nodos_visitados']}")
    print(f"Tiempo de ejecución: {resultado['tiempo']:.6f} segundos")
    if resultado['camino']:
        print(f"Largo del camino solución: {resultado['largo_camino']}")
    else:
        print("No se encontró solución.")

def ejecutar_algoritmos(laberinto, inicio=None, objetivo=None):
    print("\n\n===== RESULTADOS DE LOS ALGORITMOS =====")
    
    resultado_bfs = busqueda_amplitud(laberinto, inicio, objetivo)
    imprimir_resultado("BFS", resultado_bfs)
    
    resultado_dfs = busqueda_profundidad(laberinto, inicio, objetivo)
    imprimir_resultado("DFS", resultado_dfs)
    
    resultado_greedy_euclidiana = busqueda_voraz(laberinto, distancia_euclidiana, inicio, objetivo)
    imprimir_resultado("Greedy (Euclidiana)", resultado_greedy_euclidiana)
    
    resultado_greedy_manhattan = busqueda_voraz(laberinto, distancia_manhattan, inicio, objetivo)
    imprimir_resultado("Greedy (Manhattan)", resultado_greedy_manhattan)
    
    resultado_astar_euclidiana = busqueda_a_estrella(laberinto, distancia_euclidiana, inicio, objetivo)
    imprimir_resultado("A* (Euclidiana)", resultado_astar_euclidiana)
    
    resultado_astar_manhattan = busqueda_a_estrella(laberinto, distancia_manhattan, inicio, objetivo)
    imprimir_resultado("A* (Manhattan)", resultado_astar_manhattan)

def generar_puntos_aleatorios(laberinto, cantidad=10):
    """
    Genera puntos de inicio aleatorios dentro del laberinto.
    """
    puntos = []
    filas = len(laberinto.matriz)
    columnas = len(laberinto.matriz[0])
    
    while len(puntos) < cantidad:
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)
        if laberinto.es_camino_valido((fila, columna)):
            puntos.append((fila, columna))
    
    return puntos

def main():
    # Cargar laberintos
    print("Cargando laberintos...")
    laberinto1 = Laberinto("./Laberintos/Laberinto1.txt")
    laberinto2 = Laberinto("./Laberintos/Laberinto2.txt")
    laberinto3 = Laberinto("./Laberintos/Laberinto3.txt")
    
    # Caso base con puntos predefinidos
    print("\n--- Caso Base ---")
    print("\n--- Laberinto 1 ---")
    ejecutar_algoritmos(laberinto1)
    print("\n--- Laberinto 2 ---")
    ejecutar_algoritmos(laberinto2)
    print("\n--- Laberinto 3 ---")
    ejecutar_algoritmos(laberinto3)

if __name__ == "__main__":
    main()