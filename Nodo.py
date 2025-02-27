class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo_camino=0):
        self.estado = estado  # Estado como tupla (fila, columna)
        self.padre = padre
        self.accion = accion
        self.costo_camino = costo_camino
    
    def obtener_camino(self):
        nodo_actual = self
        camino = []
        while nodo_actual.padre is not None:
            camino.append((nodo_actual.accion, nodo_actual.estado))
            nodo_actual = nodo_actual.padre
        camino.append((None, nodo_actual.estado))
        return list(reversed(camino))
    
    def __str__(self):
        return f"Nodo(estado={self.estado}, costo_camino={self.costo_camino})"
    
    def __eq__(self, otro):
        if isinstance(otro, Nodo):
            return self.estado == otro.estado
        return False
    
    def __hash__(self):
        return hash(self.estado)