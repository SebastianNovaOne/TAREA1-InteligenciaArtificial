import random


class AlgoritmoGenetico:
    DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]

    @staticmethod
    def crear_individuo(horizonte):
        return [random.randint(0, 4) for _ in range(horizonte)]

    @staticmethod
    def evaluar_fitness(individuo, posicion_actual, posicion_salida, mapa_actual, matriz_costos):
        filas, columnas = mapa_actual.shape
        pos_x, pos_y = posicion_actual
        costo_acumulado = 0
        choco = False

        for gen in individuo:
            dx, dy = AlgoritmoGenetico.DIRECCIONES[gen]
            nuevo_x, nuevo_y = pos_x + dx, pos_y + dy

            if 0 <= nuevo_x < filas and 0 <= nuevo_y < columnas:
                if mapa_actual[nuevo_x][nuevo_y] in [1, 2]:
                    choco = True
                    break
                else:
                    pos_x, pos_y = nuevo_x, nuevo_y
                    costo_acumulado += matriz_costos[pos_x][pos_y]
            else:
                choco = True
                break

        distancia_meta = abs(pos_x - posicion_salida[0]) + abs(pos_y - posicion_salida[1])

        if choco:
            return -9999

        return -(distancia_meta * 10 + costo_acumulado)

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
        tamano_poblacion = 20
        generaciones = 10
        horizonte_pasos = 5
        tasa_mutacion = 0.1

        poblacion = [AlgoritmoGenetico.crear_individuo(horizonte_pasos) for _ in range(tamano_poblacion)]
        mejor_individuo_global = None
        mejor_fitness_global = -float('inf')

        for _ in range(generaciones):
            fitness_poblacion = []

            for individuo in poblacion:
                fit = AlgoritmoGenetico.evaluar_fitness(
                    individuo, posicion_actual, posicion_salida, mapa_actual, matriz_costos
                )
                fitness_poblacion.append(fit)

                if fit > mejor_fitness_global:
                    mejor_fitness_global = fit
                    mejor_individuo_global = list(individuo)

            nueva_poblacion = []

            while len(nueva_poblacion) < tamano_poblacion:
                padre1 = AlgoritmoGenetico.seleccion_torneo(poblacion, fitness_poblacion)
                padre2 = AlgoritmoGenetico.seleccion_torneo(poblacion, fitness_poblacion)

                hijo1, hijo2 = AlgoritmoGenetico.cruzar(padre1, padre2)

                hijo1 = AlgoritmoGenetico.mutar(hijo1, tasa_mutacion)
                hijo2 = AlgoritmoGenetico.mutar(hijo2, tasa_mutacion)

                nueva_poblacion.extend([hijo1, hijo2])

            poblacion = nueva_poblacion[:tamano_poblacion]

        if mejor_individuo_global:
            primer_movimiento = mejor_individuo_global[0]
            dx, dy = AlgoritmoGenetico.DIRECCIONES[primer_movimiento]
            nuevo_x, nuevo_y = posicion_actual[0] + dx, posicion_actual[1] + dy

            if 0 <= nuevo_x < mapa_actual.shape[0] and 0 <= nuevo_y < mapa_actual.shape[1]:
                if mapa_actual[nuevo_x][nuevo_y] not in [1, 2]:
                    return (nuevo_x, nuevo_y)

        return posicion_actual