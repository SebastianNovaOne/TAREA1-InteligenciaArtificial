import time
from src.entorno.entorno import EntornoSimulacion
from colores_visualizacion import limpiar_pantalla, imprimir_mapa_consola
from benchmark import obtener_posiciones_vacias

def ejecutar_simulacion_visual(mapa_elegido, funcion_algoritmo, nombre_algoritmo):
    entorno = EntornoSimulacion(
        matriz_mapa=mapa_elegido,
        k=3,
        sensibilidad_congestion=1.0,
        fuego_aleatorio=True,
        capacidad_maxima=3
    )

    posiciones_iniciales = obtener_posiciones_vacias(entorno.mapa_actual, cantidad=20)
    entorno.agregar_agentes(posiciones_iniciales)

    while not entorno.terminado():
        limpiar_pantalla()
        print(f"Turno: {entorno.turno_actual} | Algoritmo: {nombre_algoritmo}")

        posiciones_agentes_vivos = [agente.posicion for agente in entorno.agentes if agente.estado == "VIVO"]
        imprimir_mapa_consola(entorno.mapa_actual, posiciones_agentes_vivos)

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
        time.sleep(0.3)

    print("Simulacion completada.")
    input("Presione Enter para volver al menu.")
