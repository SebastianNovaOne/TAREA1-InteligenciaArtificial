import time
from src.entorno.entorno import EntornoSimulacion
from colores_visualizacion import limpiar_pantalla, imprimir_mapa_consola
from benchmark import obtener_posiciones_vacias

# Muestra en consola paso a paso el desarrollo de la simulacion
def ejecutar_simulacion_visual(mapa_elegido, funcion_algoritmo, nombre_algoritmo, cantidad_agentes=20):
    entorno = EntornoSimulacion(
        matriz_mapa=mapa_elegido,
        k=2,
        sensibilidad_congestion=3.5,
        fuego_aleatorio=True,
        capacidad_maxima=3
    )

    posiciones_iniciales = obtener_posiciones_vacias(entorno.mapa_actual, cantidad=cantidad_agentes)
    entorno.agregar_agentes(posiciones_iniciales)

    turno_evacuacion = {}
    # Loop visual turno a turno hasta terminar la evacuacion
    while not entorno.terminado():
        limpiar_pantalla()
        print(f"Turno: {entorno.turno_actual} | Algoritmo: {nombre_algoritmo}")
        print(f"Cantidad de agentes restantes: {sum(1 for agente in entorno.agentes if agente.estado == 'VIVO')}")
        posiciones_agentes_vivos = [agente.posicion for agente in entorno.agentes if agente.estado == "VIVO"]
        imprimir_mapa_consola(entorno.mapa_actual, posiciones_agentes_vivos)

        acciones = {}
        matriz_costos = entorno.matriz_costos()

        # Consulta el movimiento de cada agente vivo
        for agente in entorno.agentes:
            if agente.estado == "VIVO":
                acciones[agente.id_agente] = funcion_algoritmo(
                    agente.posicion,
                    entorno.posicion_salida,
                    entorno.mapa_actual,
                    matriz_costos
                )

        entorno.avanzar_turno(acciones)
        # Guarda el turno de llegada de los agentes evacuados
        for agente in entorno.agentes:
            if agente.estado == "EVACUADO" and agente.id_agente not in turno_evacuacion:
                turno_evacuacion[agente.id_agente] = entorno.turno_actual

        time.sleep(0.3)

    print("Simulacion completada.")
    if turno_evacuacion:
        print(f"Supervivientes: {len(turno_evacuacion)} | Turno último agente evacuado: {max(turno_evacuacion.values())}")
    else:
        print("Supervivientes: 0 | Nadie logro evacuar")
    input("Presione Enter para volver al menu.")