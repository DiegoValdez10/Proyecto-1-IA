import time
from Cola import ColaFIFO, ColaLIFO, ColaPrioridad
from Nodo import Nodo
from Heuristica import distancia_euclidiana, distancia_manhattan

def busqueda_amplitud(laberinto, inicio=None, objetivo=None):
    inicio = inicio or laberinto.inicio
    objetivo = objetivo or laberinto.salida
    
    tiempo_inicio = time.time()
    
    frontera = ColaFIFO()
    frontera.add(Nodo(inicio))
    explorados = set()
    nodos_visitados = 0
    
    while not frontera.empty():
        nodo = frontera.pop()
        nodos_visitados += 1
        
        if nodo.estado == objetivo:
            tiempo_fin = time.time()
            camino = nodo.obtener_camino()
            return {
                "camino": camino,
                "nodos_visitados": nodos_visitados,
                "tiempo": tiempo_fin - tiempo_inicio,
                "largo_camino": len(camino) - 1  
            }
        
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            for vecino in laberinto.obtener_vecinos(nodo.estado):
                if vecino not in explorados:
                    direccion = obtener_direccion(nodo.estado, vecino)
                    nuevo_nodo = Nodo(
                        estado=vecino,
                        padre=nodo,
                        accion=direccion,
                        costo_camino=nodo.costo_camino + 1
                    )
                    frontera.add(nuevo_nodo)
    
    tiempo_fin = time.time()
    return {
        "camino": None,
        "nodos_visitados": nodos_visitados,
        "tiempo": tiempo_fin - tiempo_inicio,
        "largo_camino": float("inf")
    }

def busqueda_profundidad(laberinto, inicio=None, objetivo=None):

    inicio = inicio or laberinto.inicio
    objetivo = objetivo or laberinto.salida
    
    tiempo_inicio = time.time()
    
    frontera = ColaLIFO()
    frontera.add(Nodo(inicio))
    explorados = set()
    nodos_visitados = 0
    
    while not frontera.empty():
        nodo = frontera.pop()
        nodos_visitados += 1
        
        if nodo.estado == objetivo:
            tiempo_fin = time.time()
            camino = nodo.obtener_camino()
            return {
                "camino": camino,
                "nodos_visitados": nodos_visitados,
                "tiempo": tiempo_fin - tiempo_inicio,
                "largo_camino": len(camino) - 1  
            }
        
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            for vecino in laberinto.obtener_vecinos(nodo.estado):
                if vecino not in explorados:
                    direccion = obtener_direccion(nodo.estado, vecino)
                    nuevo_nodo = Nodo(
                        estado=vecino,
                        padre=nodo,
                        accion=direccion,
                        costo_camino=nodo.costo_camino + 1
                    )
                    frontera.add(nuevo_nodo)
    
    tiempo_fin = time.time()
    return {
        "camino": None,
        "nodos_visitados": nodos_visitados,
        "tiempo": tiempo_fin - tiempo_inicio,
        "largo_camino": float("inf")
    }

def busqueda_voraz(laberinto, heuristica=distancia_euclidiana, inicio=None, objetivo=None):
 
    inicio = inicio or laberinto.inicio
    objetivo = objetivo or laberinto.salida
    
    tiempo_inicio = time.time()
    
    frontera = ColaPrioridad()
    nodo_inicial = Nodo(inicio)
    frontera.add(nodo_inicial, heuristica(inicio, objetivo))
    explorados = set()
    nodos_visitados = 0
    
    while not frontera.empty():
        nodo = frontera.pop()
        nodos_visitados += 1
        
        if nodo.estado == objetivo:
            tiempo_fin = time.time()
            camino = nodo.obtener_camino()
            return {
                "camino": camino,
                "nodos_visitados": nodos_visitados,
                "tiempo": tiempo_fin - tiempo_inicio,
                "largo_camino": len(camino) - 1  
            }
        
        if nodo.estado not in explorados:
            explorados.add(nodo.estado)
            for vecino in laberinto.obtener_vecinos(nodo.estado):
                if vecino not in explorados:
                    direccion = obtener_direccion(nodo.estado, vecino)
                    nuevo_nodo = Nodo(
                        estado=vecino,
                        padre=nodo,
                        accion=direccion,
                        costo_camino=nodo.costo_camino + 1
                    )
                    frontera.add(nuevo_nodo, heuristica(vecino, objetivo))
    
    tiempo_fin = time.time()
    return {
        "camino": None,
        "nodos_visitados": nodos_visitados,
        "tiempo": tiempo_fin - tiempo_inicio,
        "largo_camino": float("inf")
    }

def busqueda_a_estrella(laberinto, heuristica=distancia_euclidiana, inicio=None, objetivo=None):

    inicio = inicio or laberinto.inicio
    objetivo = objetivo or laberinto.salida
    
    tiempo_inicio = time.time()

    frontera = ColaPrioridad()
    nodo_inicial = Nodo(inicio)

    frontera.add(nodo_inicial, 0 + heuristica(inicio, objetivo))
    

    explorados = {}
    

    nodos_frontera = {inicio: nodo_inicial}
    
    nodos_visitados = 0
    
    while not frontera.empty():

        nodo = frontera.pop()
        estado_actual = nodo.estado
        nodos_visitados += 1
        

        if estado_actual in explorados and explorados[estado_actual] < nodo.costo_camino:
            continue
            

        if estado_actual == objetivo:
            tiempo_fin = time.time()
            camino = nodo.obtener_camino()
            return {
                "camino": camino,
                "nodos_visitados": nodos_visitados,
                "tiempo": tiempo_fin - tiempo_inicio,
                "largo_camino": len(camino) - 1
            }

        explorados[estado_actual] = nodo.costo_camino

        if estado_actual in nodos_frontera:
            del nodos_frontera[estado_actual]
        

        for vecino in laberinto.obtener_vecinos(estado_actual):
            nuevo_costo = nodo.costo_camino + 1
            

            if vecino in explorados and explorados[vecino] <= nuevo_costo:
                continue
                

            if vecino in nodos_frontera and nodos_frontera[vecino].costo_camino <= nuevo_costo:
                continue
                

            direccion = obtener_direccion(estado_actual, vecino)
            nuevo_nodo = Nodo(
                estado=vecino,
                padre=nodo,
                accion=direccion,
                costo_camino=nuevo_costo
            )
            

            f_n = nuevo_costo + heuristica(vecino, objetivo)
            

            frontera.add(nuevo_nodo, f_n)
            nodos_frontera[vecino] = nuevo_nodo
    

    tiempo_fin = time.time()
    return {
        "camino": None,
        "nodos_visitados": nodos_visitados,
        "tiempo": tiempo_fin - tiempo_inicio,
        "largo_camino": float("inf")
    }

def obtener_direccion(origen, destino):

    fila_origen, col_origen = origen
    fila_destino, col_destino = destino
    
    if fila_destino < fila_origen:
        return "Arriba"
    elif col_destino > col_origen:
        return "Derecha"
    elif fila_destino > fila_origen:
        return "Abajo"
    elif col_destino < col_origen:
        return "Izquierda"
    else:
        return "No hay movimiento"