import random

import numpy as np

from src.entorno.entorno import EntornoSimulacion
from src.evaluacion.metricas import Metricas

# Selecciona aleatoriamente celdas vacias para posicionar a los agentes
def obtener_posiciones_vacias(matriz_mapa, cantidad):
    posiciones_vacias = np.argwhere(matriz_mapa == 0)
    indices_elegidos = np.random.choice(len(posiciones_vacias), cantidad, replace=False)
    posiciones_seleccionadas = posiciones_vacias[indices_elegidos]
    return [tuple(pos) for pos in posiciones_seleccionadas]

# Ejecuta una sola prueba de la simulacion hasta que finalice
def ejecutar_iteracion(mapa_elegido, funcion_algoritmo, cantidad_agentes, semilla, k, sensibilidad, capacidad):
    # Fija semillas para las pruebas
    np.random.seed(semilla)
    random.seed(semilla)

    entorno = EntornoSimulacion(
        matriz_mapa=mapa_elegido,
        k=k,
        sensibilidad_congestion=sensibilidad,
        fuego_aleatorio=True,
        capacidad_maxima=capacidad
    )
    entorno.agregar_agentes(obtener_posiciones_vacias(entorno.mapa_actual, cantidad_agentes))

    turno_evacuacion = {}
    # Bucle principal de la prueba turno a turno
    while not entorno.terminado():
        acciones = {}
        matriz_costos = entorno.matriz_costos()
        # Obtiene la accion de cada agente vivo
        for agente in entorno.agentes:
            if agente.estado == "VIVO":
                acciones[agente.id_agente] = funcion_algoritmo(
                    agente.posicion,
                    entorno.posicion_salida,
                    entorno.mapa_actual,
                    matriz_costos
                )

        entorno.avanzar_turno(acciones)
        # Registra el turno exacto de evacuacion para cada agente
        for agente in entorno.agentes:
            if agente.estado == "EVACUADO" and agente.id_agente not in turno_evacuacion:
                turno_evacuacion[agente.id_agente] = entorno.turno_actual

    sobrevivientes = len(turno_evacuacion)
    tiempo_despeje = max(turno_evacuacion.values()) if turno_evacuacion else None
    return sobrevivientes, tiempo_despeje

# Corre múltiples iteraciones de un algoritmo en un mapa y calcula las metricas
def benchmark(mapa_elegido, nombre_mapa, funcion_algoritmo, nombre_algoritmo, iteraciones,
              cantidad_agentes=80, semilla_base=1000, k=2, sensibilidad=3.5, capacidad=3,
              pausar=True):
    print(f"\nIniciando Benchmark: {nombre_algoritmo} en {nombre_mapa} ({iteraciones} iteraciones)")

    tiempos_totales = []
    supervivientes_totales = []
    # Bucle para ejecutar todas las iteraciones configuradas
    for i in range(iteraciones):
        semilla = semilla_base + i
        sobrevivientes, tiempo_despeje = ejecutar_iteracion(
            mapa_elegido, funcion_algoritmo, cantidad_agentes, semilla, k, sensibilidad, capacidad
        )

        supervivientes_totales.append(sobrevivientes)
        if tiempo_despeje is not None:
            tiempos_totales.append(tiempo_despeje)

        print(f"Iteracion {i + 1}/{iteraciones} finalizada. Supervivientes: {sobrevivientes} | "
              f"Turno último agente evacuado: {tiempo_despeje}")

    resultados = Metricas.calcular_estadisticas(tiempos_totales, supervivientes_totales, cantidad_agentes)

    print("\nRESULTADOS BENCHMARK")
    print(f"Tasa de Supervivencia Promedio = {resultados['supervivencia_media_pct']:.2f}%")
    print(f"Tiempo de despeje Medio = {resultados['tiempo_media']:.2f} turnos")
    print(f"Desviación Estándar = {resultados['tiempo_std']:.2f} turnos")
    print(f"Tiempo Mínimo = {resultados['tiempo_min']} turnos")
    print(f"Tiempo Máximo = {resultados['tiempo_max']} turnos\n")

    if pausar:
        input("\nPresione Enter para continuar\n")