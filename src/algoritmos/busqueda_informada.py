import heapq


class BusquedaInformada:
    DIRECCIONES = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Calcula la distancia Manhattan en linea recta entre dos puntos
    @staticmethod
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Busqueda greedy guiada únicamente por la distancia a la meta
    @staticmethod
    def GreedyBestFirstSearch(posicion_actual, posicion_salida, mapa_actual):
        filas, columnas = mapa_actual.shape
        lista_abierta = []
        heapq.heappush(lista_abierta, (BusquedaInformada.heuristica(posicion_actual, posicion_salida), posicion_actual))
        vino_de = {posicion_actual: None}
        visitados = set()
        # Procesa la celda mas cercana a la salida segun la heuristica
        while lista_abierta:
            _, actual = heapq.heappop(lista_abierta)

            if actual == posicion_salida:
                camino = []
                mientras_actual = actual
                while mientras_actual:
                    camino.append(mientras_actual)
                    mientras_actual = vino_de[mientras_actual]
                camino = camino[::-1]
                if len(camino) > 1:
                    return camino[1]
                return posicion_actual

            visitados.add(actual)
            # Revisa las celdas vecinas navegables
            for dx, dy in BusquedaInformada.DIRECCIONES:
                vecino = (actual[0] + dx, actual[1] + dy)
                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                    if mapa_actual[vecino[0]][vecino[1]] != 1 and mapa_actual[vecino[0]][vecino[1]] != 2:
                        if vecino not in visitados:
                            visitados.add(vecino)
                            vino_de[vecino] = actual
                            heapq.heappush(lista_abierta,
                                           (BusquedaInformada.heuristica(vecino, posicion_salida), vecino))

        return posicion_actual

    # Busqueda A* que combina el costo acumulado con la distancia estimada a la meta
    @staticmethod
    def AStar(posicion_actual, posicion_salida, mapa_actual, matriz_costos):
        filas, columnas = mapa_actual.shape
        lista_abierta = []
        heapq.heappush(lista_abierta,
                       (0 + BusquedaInformada.heuristica(posicion_actual, posicion_salida), 0, posicion_actual))
        vino_de = {posicion_actual: None}
        costo_hasta_ahora = {posicion_actual: 0}
        # Procesa el nodo con el menor costo estimado total
        while lista_abierta:
            _, costo, actual = heapq.heappop(lista_abierta)

            if actual == posicion_salida:
                camino = []
                mientras_actual = actual
                while mientras_actual:
                    camino.append(mientras_actual)
                    mientras_actual = vino_de[mientras_actual]
                camino = camino[::-1]
                if len(camino) > 1:
                    return camino[1]
                return posicion_actual
            # Evalua el costo de moverse a casillas vecinas
            for dx, dy in BusquedaInformada.DIRECCIONES:
                vecino = (actual[0] + dx, actual[1] + dy)
                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                    if mapa_actual[vecino[0]][vecino[1]] != 1 and mapa_actual[vecino[0]][vecino[1]] != 2:
                        nuevo_costo = costo + matriz_costos[vecino[0]][vecino[1]]
                        if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:
                            costo_hasta_ahora[vecino] = nuevo_costo
                            prioridad = nuevo_costo + BusquedaInformada.heuristica(vecino, posicion_salida)
                            heapq.heappush(lista_abierta, (prioridad, nuevo_costo, vecino))
                            vino_de[vecino] = actual

        return posicion_actual