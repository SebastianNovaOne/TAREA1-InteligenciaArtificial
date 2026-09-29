import random
from collections import deque


class AlgoritmoGenetico:
    DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]

    TAMANO_POBLACION = 20
    GENERACIONES = 10
    HORIZONTE_PASOS = 5
    TASA_MUTACION = 0.1

    PENALIZACION_CHOQUE = 50
    PENALIZACION_ESPERA = 5

    mapa_guardado = None
    distancias_guardadas = None

    @staticmethod
    def calcular_distancias(mapa_actual, posicion_salida):
        clave = mapa_actual.tobytes()
        if AlgoritmoGenetico.mapa_guardado == clave:
            return AlgoritmoGenetico.distancias_guardadas

        filas, columnas = mapa_actual.shape
        salida = tuple(posicion_salida)
        distancias = {salida: 0}
        cola = deque([salida])

        while cola:
            x, y = cola.popleft()
            for dx, dy in AlgoritmoGenetico.DIRECCIONES[:4]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < filas and 0 <= ny < columnas and (nx, ny) not in distancias:
                    if mapa_actual[nx][ny] not in [1, 2]:
                        distancias[(nx, ny)] = distancias[(x, y)] + 1
                        cola.append((nx, ny))

        AlgoritmoGenetico.mapa_guardado = clave
        AlgoritmoGenetico.distancias_guardadas = distancias
        return distancias

    @staticmethod
    def crear_individuo(horizonte):
        return [random.randint(0, 4) for _ in range(horizonte)]

    @staticmethod
    def evaluar_fitness(individuo, posicion_actual, posicion_salida, mapa_actual, matriz_costos):
        filas, columnas = mapa_actual.shape
        distancias = AlgoritmoGenetico.calcular_distancias(mapa_actual, posicion_salida)
        salida = tuple(posicion_salida)
        pos_x, pos_y = posicion_actual
        penalizacion = 0
        suma_distancias = 0

        for gen in individuo:
            dx, dy = AlgoritmoGenetico.DIRECCIONES[gen]
            nuevo_x, nuevo_y = pos_x + dx, pos_y + dy

            if not (0 <= nuevo_x < filas and 0 <= nuevo_y < columnas) or mapa_actual[nuevo_x][nuevo_y] in [1, 2]:
                penalizacion += AlgoritmoGenetico.PENALIZACION_CHOQUE
            elif gen == 4:
                penalizacion += AlgoritmoGenetico.PENALIZACION_ESPERA
            else:
                pos_x, pos_y = nuevo_x, nuevo_y
                penalizacion += matriz_costos[pos_x][pos_y]
                if (pos_x, pos_y) == salida:
                    break

            suma_distancias += distancias.get((pos_x, pos_y), 999)

        distancia_meta = distancias.get((pos_x, pos_y), 999)
        return -(distancia_meta * 10 + suma_distancias + penalizacion)

    @staticmethod
    def seleccion_torneo(poblacion, fitness_poblacion):
        indices_azar = [random.randint(0, len(poblacion) - 1) for _ in range(3)]
        mejor_indice = indices_azar[0]

        for i in indices_azar:
            if fitness_poblacion[i] > fitness_poblacion[mejor_indice]:
                mejor_indice = i

        return poblacion[mejor_indice]

    @staticmethod
    def cruzar(padre1, padre2):
        punto_corte = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
        hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
        return hijo1, hijo2

    @staticmethod
    def mutar(individuo, tasa_mutacion):
        for i in range(len(individuo)):
            if random.random() < tasa_mutacion:
                individuo[i] = random.randint(0, 4)
        return individuo

    @staticmethod
    def genetico(posicion_actual, posicion_salida, mapa_actual, matriz_costos):
        poblacion = [AlgoritmoGenetico.crear_individuo(AlgoritmoGenetico.HORIZONTE_PASOS)
                     for _ in range(AlgoritmoGenetico.TAMANO_POBLACION)]
        mejor_individuo_global = None
        mejor_fitness_global = -float('inf')

        for _ in range(AlgoritmoGenetico.GENERACIONES):
            fitness_poblacion = []

            for individuo in poblacion:
                fit = AlgoritmoGenetico.evaluar_fitness(
                    individuo, posicion_actual, posicion_salida, mapa_actual, matriz_costos
                )
                fitness_poblacion.append(fit)

                if fit > mejor_fitness_global:
                    mejor_fitness_global = fit
                    mejor_individuo_global = list(individuo)

            nueva_poblacion = [list(mejor_individuo_global)]

            while len(nueva_poblacion) < AlgoritmoGenetico.TAMANO_POBLACION:
                padre1 = AlgoritmoGenetico.seleccion_torneo(poblacion, fitness_poblacion)
                padre2 = AlgoritmoGenetico.seleccion_torneo(poblacion, fitness_poblacion)

                hijo1, hijo2 = AlgoritmoGenetico.cruzar(padre1, padre2)

                hijo1 = AlgoritmoGenetico.mutar(hijo1, AlgoritmoGenetico.TASA_MUTACION)
                hijo2 = AlgoritmoGenetico.mutar(hijo2, AlgoritmoGenetico.TASA_MUTACION)

                nueva_poblacion.extend([hijo1, hijo2])

            poblacion = nueva_poblacion[:AlgoritmoGenetico.TAMANO_POBLACION]

        primer_movimiento = mejor_individuo_global[0]
        dx, dy = AlgoritmoGenetico.DIRECCIONES[primer_movimiento]
        nuevo_x, nuevo_y = posicion_actual[0] + dx, posicion_actual[1] + dy

        if 0 <= nuevo_x < mapa_actual.shape[0] and 0 <= nuevo_y < mapa_actual.shape[1]:
            if mapa_actual[nuevo_x][nuevo_y] not in [1, 2]:
                return (nuevo_x, nuevo_y)

        return posicion_actual