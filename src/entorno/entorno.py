import numpy as np
from src.entorno.agente import Agente


class EntornoSimulacion:
    VACIO = 0
    MURO = 1
    FUEGO = 2
    SALIDA = 3

    # Inicializa el mapa, la salida y la posicion del fuego
    def __init__(self, matriz_mapa, k, sensibilidad_congestion=1.0, fuego_aleatorio=False, capacidad_maxima=3):
        self.mapa_base = np.copy(matriz_mapa)
        self.mapa_actual = np.copy(matriz_mapa)
        self.k = k
        self.sensibilidad_congestion = sensibilidad_congestion
        self.capacidad_maxima = capacidad_maxima
        self.turno_actual = 0
        self.agentes = []
        self.portadores = set()
        self.coordenadas_salidas = np.argwhere(self.mapa_actual == self.SALIDA)
        self.posicion_salida = tuple(self.coordenadas_salidas[0])
        # Ubica el fuego aleatoriamente alejado de la salida
        if fuego_aleatorio:
            self.mapa_actual[self.mapa_actual == self.FUEGO] = self.VACIO
            vacias = np.argwhere(self.mapa_actual == self.VACIO)

            vacias_seguras = []
            # Filtra posiciones para que el fuego no aparezca muy cerca de la salida
            for v in vacias:
                distancia = min(abs(v[0] - s[0]) + abs(v[1] - s[1]) for s in self.coordenadas_salidas)
                if distancia > 8:
                    vacias_seguras.append(v)

            if len(vacias_seguras) == 0:
                vacias_seguras = vacias

            pos_fuego = vacias_seguras[np.random.choice(len(vacias_seguras))]
            self.mapa_actual[tuple(pos_fuego)] = self.FUEGO

    # Crea e inserta la lista de agentes en la simulacion
    def agregar_agentes(self, posiciones_iniciales):
        # Recorre las coordenadas asignadas a cada agente
        for i, pos in enumerate(posiciones_iniciales):
            self.agentes.append(Agente(i, pos))

    # Genera la matriz de costos basada en la densidad de agentes por celda
    def matriz_costos(self):
        filas, columnas = self.mapa_actual.shape
        matriz_costos = np.ones((filas, columnas), dtype=float)
        # Cuenta la presencia de agentes vivos en el mapa
        for agente in self.agentes:
            if agente.estado == "VIVO":
                f, c = agente.posicion
                matriz_costos[f][c] += 1.0
        # Aplica la penalizacion por congestion a cada celda
        for f in range(filas):
            for c in range(columnas):
                ocupacion = matriz_costos[f][c] - 1.0
                matriz_costos[f][c] = 1.0 + self.sensibilidad_congestion * (ocupacion ** 2)
                if self.mapa_actual[f][c] in [self.MURO, self.FUEGO]:
                    matriz_costos[f][c] = float('inf')

        return matriz_costos

    # Expande el fuego a casillas adyacentes respetando la zona segura de salida
    def propagar_fuego(self):
        filas, columnas = self.mapa_actual.shape
        nuevo_mapa = np.copy(self.mapa_actual)
        nuevos_portadores = set(self.portadores)
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        fuentes = [tuple(p) for p in np.argwhere(self.mapa_actual == self.FUEGO)] + list(self.portadores)
        # Recorre todos los focos activos de fuego
        for f, c in fuentes:
            # Revisa las casillas vecinas para expandir la llama
            for df, dc in direcciones:
                nf, nc = f + df, c + dc
                if 0 <= nf < filas and 0 <= nc < columnas:
                    if self.mapa_actual[nf][nc] not in [self.MURO, self.SALIDA]:
                        dist = min(abs(nf - s[0]) + abs(nc - s[1]) for s in self.coordenadas_salidas)
                        # Aplica zona de proteccion cerca de las salidas
                        if dist > 2:
                            nuevo_mapa[nf][nc] = self.FUEGO
                        else:
                            nuevos_portadores.add((nf, nc))

        self.mapa_actual = nuevo_mapa
        self.portadores = nuevos_portadores

    # Avanza un turno de simulacion, moviendo agentes y propagando fuego
    def avanzar_turno(self, acciones_agentes):
        self.turno_actual += 1
        # Propaga el fuego segun k
        if self.turno_actual % self.k == 0:
            self.propagar_fuego()

        conteo = {}
        # Conteo previo de agentes en cada casilla
        for a in self.agentes:
            if a.estado == "VIVO":
                conteo[a.posicion] = conteo.get(a.posicion, 0) + 1
        # Procesa las acciones individuales de cada agente
        for agente in self.agentes:
            if agente.estado != "VIVO":
                continue

            destino = acciones_agentes.get(agente.id_agente, agente.posicion)

            # Limita el movimiento si el destino excede la capacidad maxima
            if destino != agente.posicion and conteo.get(destino, 0) >= self.capacidad_maxima:
                destino = agente.posicion
            # Verifica si el agente entra a una celda quemada
            if self.mapa_actual[destino] == self.FUEGO:
                conteo[agente.posicion] -= 1
                agente.morir()
                continue
            # Actualiza el conteo de celdas al desplazarse
            if destino != agente.posicion:
                conteo[agente.posicion] -= 1
                if destino != self.posicion_salida:
                    conteo[destino] = conteo.get(destino, 0) + 1

            agente.mover(destino)
            # Evalua si el agente llega a la salida o no
            if agente.posicion == self.posicion_salida:
                agente.evacuar()
            elif self.mapa_actual[agente.posicion] == self.FUEGO:
                agente.morir()

    # Comprueba si no quedan agentes vivos activos
    def terminado(self):
        return not any(a.estado == "VIVO" for a in self.agentes)