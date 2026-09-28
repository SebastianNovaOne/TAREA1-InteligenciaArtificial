from src.entorno.entorno import EntornoSimulacion
from src.evaluacion.metricas import Metricas
import numpy as np


def obtener_posiciones_vacias(matriz_mapa, cantidad):
    posiciones_vacias = np.argwhere(matriz_mapa == 0)
    indices_elegidos = np.random.choice(len(posiciones_vacias), cantidad, replace=False)
    posiciones_seleccionadas = posiciones_vacias[indices_elegidos]
    return [tuple(pos) for pos in posiciones_seleccionadas]


def benchmark(mapa_elegido, nombre_mapa, funcion_algoritmo, nombre_algoritmo, iteraciones,
              cantidad_agentes=80):
    print(f"\nIniciando Benchmark: {nombre_algoritmo} en {nombre_mapa} ({iteraciones} iteraciones)")

    tiempos_totales = []
    supervivientes_totales = []

    for i in range(iteraciones):
        entorno = EntornoSimulacion(
            matriz_mapa=mapa_elegido,
            k=2,
            sensibilidad_congestion=3.5,
            fuego_aleatorio=True,
            capacidad_maxima=3
        )

        posiciones_iniciales = obtener_posiciones_vacias(entorno.mapa_actual, cantidad_agentes)
        entorno.agregar_agentes(posiciones_iniciales)

        while not entorno.terminado():
            acciones = {}
            matriz_costos = entorno.matriz_costos()

            for agente in entorno.agentes:
                if agente.estado == "VIVO":
                    acciones[agente.id_agente] = funcion_algoritmo(
                        agente.posicion,
                        entorno.posicion_salida,
                        entorno.mapa_actual,
                        matriz_costos
                    )

            entorno.avanzar_turno(acciones)

        sobrevivientes = sum(1 for a in entorno.agentes if a.estado == "EVACUADO")
        supervivientes_totales.append(sobrevivientes)

        if sobrevivientes > 0:
            tiempos_totales.append(entorno.turno_actual)

        print(f"Iteracion {i + 1}/{iteraciones} finalizada con exito. Supervivientes: {sobrevivientes}")

    resultados = Metricas.calcular_estadisticas(tiempos_totales, supervivientes_totales, cantidad_agentes)

    parametros = {
        "mapa": nombre_mapa,
        "algoritmo": nombre_algoritmo,
        "iteraciones": iteraciones,
        "agentes_iniciales": cantidad_agentes
    }
    print("\nRESULTADOS BENCHMARK")
    print(f"Tasa de Supervivencia Promedio = {resultados['supervivencia_media_pct']:.2f}%")
    print(f"Tiempo Medio = {resultados['tiempo_media']:.2f} turnos")
    print(f"Desviación Estándar = {resultados['tiempo_std']:.2f} turnos")
    print(f"Tiempo Mínimo = {resultados['tiempo_min']} turnos")
    print(f"Tiempo Máximo = {resultados['tiempo_max']} turnos\n")
    input("\nPresione Enter para continuar\n")