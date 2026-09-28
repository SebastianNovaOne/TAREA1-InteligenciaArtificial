from src.entorno.mapas import mapa_alta_densidad, mapa_media_densidad, mapa_baja_densidad
from src.algoritmos.busqueda_no_informada import BusquedaNoInformada
from src.algoritmos.busqueda_informada import BusquedaInformada
from src.algoritmos.algoritmo_genetico import AlgoritmoGenetico

from visualizacion import ejecutar_simulacion_visual

def ejecutar_bfs(pos, salida, mapa, costos):
    return BusquedaNoInformada.BreadthFirstSearch(pos, salida, mapa)

def ejecutar_ucs(pos, salida, mapa, costos):
    return BusquedaNoInformada.UniformCostSearch(pos, salida, mapa, costos)

def ejecutar_greedy(pos, salida, mapa, costos):
    return BusquedaInformada.GreedyBestFirstSearch(pos, salida, mapa)

def ejecutar_a_star(pos, salida, mapa, costos):
    return BusquedaInformada.AStar(pos, salida, mapa, costos)

def ejecutar_genetico(pos, salida, mapa, costos):
    return AlgoritmoGenetico.genetico(pos, salida, mapa, costos)


diccionario_algoritmos = {
    "1": ("BFS", ejecutar_bfs),
    "2": ("UCS", ejecutar_ucs),
    "3": ("Greedy", ejecutar_greedy),
    "4": ("A*", ejecutar_a_star),
    "5": ("Genetico", ejecutar_genetico)
}

diccionario_mapas = {
    "1": ("Alta Densidad", mapa_alta_densidad),
    "2": ("Media Densidad", mapa_media_densidad),
    "3": ("Baja Densidad", mapa_baja_densidad)
}

def menu_principal():
    while True:
        print("Simulador de evacuacion de incendios basado en algoritmos")
        print("1. Modo Visualizacion [1 Iteracion, con actualizaciones visuales en terminal]")
        print("2. Cancelar")

        modo = input("Selecciona una opcion (1-2): ")

        if modo == "2":
            break
        if modo != "1":
            continue

        print("\nSELECCION DE MAPA")
        print("1. Alta Densidad")
        print("2. Media Densidad")
        print("3. Baja Densidad")
        opcion_mapa = input("Selecciona un mapa (1-3): ")

        if opcion_mapa not in diccionario_mapas:
            continue

        nombre_mapa, funcion_mapa = diccionario_mapas[opcion_mapa]
        mapa_seleccionado = funcion_mapa()

        print("\nSELECCION DE ALGORITMO")
        print("1. Breadth First Search")
        print("2. Uniform Cost Search")
        print("3. Greedy Best First Search")
        print("4. A*")
        print("5. Algoritmo Genetico")
        opcion_algoritmo = input("Selecciona un algoritmo (1-5): ")

        if opcion_algoritmo not in diccionario_algoritmos:
            continue

        nombre_algoritmo, funcion_algoritmo = diccionario_algoritmos[opcion_algoritmo]

        ejecutar_simulacion_visual(mapa_seleccionado, funcion_algoritmo, nombre_algoritmo)

if __name__ == "__main__":
    menu_principal()