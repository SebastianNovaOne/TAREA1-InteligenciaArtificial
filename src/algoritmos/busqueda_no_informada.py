import numpy as np
from collections import deque
import heapq

# Clase para gestionar los nodos y sus costos en la busqueda UCS
class NodoUcs:
    def __init__(self, estado, padre=None, costo_camino=0):
        self.estado = estado
        self.padre = padre
        self.costo_camino = costo_camino

    # Permite ordenar los nodos en la cola de prioridad segun su costo
    def __lt__(self, otro):
        return self.costo_camino < otro.costo_camino


class BusquedaNoInformada:
    DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Busqueda en anchura
    @staticmethod
    def BreadthFirstSearch(posicion_actual, posicion_salida, mapa_actual):
        filas, columnas = mapa_actual.shape
        cola = deque([(posicion_actual, [posicion_actual])])
        visitados = set()

        while cola:
            actual, camino = cola.popleft()

            if actual == posicion_salida:
                if len(camino) > 1:
                    return camino[1]
                return actual

            if actual in visitados:
                continue

            visitados.add(actual)

            for dx, dy in BusquedaNoInformada.DIRECCIONES:
                nx, ny = actual[0] + dx, actual[1] + dy
                if 0 <= nx < filas and 0 <= ny < columnas:
                    if mapa_actual[nx][ny] != 1 and mapa_actual[nx][ny] != 2:
                        cola.append(((nx, ny), camino + [(nx, ny)]))

        return posicion_actual

    # Busqueda por Costo Uniforme que prioriza rutas de menor costo acumulado
    @staticmethod
    def UniformCostSearch(posicion_actual, posicion_salida, mapa_actual, matriz_costos):
        filas, columnas = mapa_actual.shape
        frontera = []
        heapq.heappush(frontera, NodoUcs(posicion_actual))
        explorados = set()

        while frontera:
            nodo = heapq.heappop(frontera)

            if nodo.estado == posicion_salida:
                camino = []
                actual = nodo
                while actual:
                    camino.append(actual.estado)
                    actual = actual.padre
                camino = camino[::-1]
                if len(camino) > 1:
                    return camino[1]
                return posicion_actual

            explorados.add(nodo.estado)

            for dx, dy in BusquedaNoInformada.DIRECCIONES:
                nx, ny = nodo.estado[0] + dx, nodo.estado[1] + dy
                vecino = (nx, ny)

                if 0 <= nx < filas and 0 <= ny < columnas:
                    if mapa_actual[nx][ny] != 1 and mapa_actual[nx][ny] != 2:
                        if vecino not in explorados:
                            costo_hijo = nodo.costo_camino + matriz_costos[nx][ny]
                            nodo_hijo = NodoUcs(vecino, nodo, costo_hijo)

                            en_frontera_mejor = any(
                                n.estado == vecino and n.costo_camino <= costo_hijo
                                for n in frontera
                            )

                            if not en_frontera_mejor:
                                heapq.heappush(frontera, nodo_hijo)

        return posicion_actual