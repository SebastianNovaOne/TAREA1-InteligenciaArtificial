from src.entorno.mapas import mapa_alta_densidad, mapa_media_densidad, mapa_baja_densidad
from src.algoritmos.busqueda_no_informada import BusquedaNoInformada
from src.algoritmos.busqueda_informada import BusquedaInformada
from src.algoritmos.algoritmo_genetico import AlgoritmoGenetico

from visualizacion import ejecutar_simulacion_visual
from benchmark import benchmark

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

def pedir_entero(texto, minimo, maximo):
    while True:
        valor = input(texto).strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return int(valor)
        print(f"Valor no valido. Ingrese un numero entero entre {minimo} y {maximo}.")

def menu_principal():
    while True:
        print("\nSimulador de evacuacion de incendios basado en algoritmos")
        print("1. Modo Visualizacion [1 Iteracion, con actualizaciones visuales en terminal]")
        print("2. Modo Benchmarking [Multiples Iteraciones, sin visualizacion, Solo rendimiento]")
        print("3. Cancelar")

        modo = input("Selecciona una opcion [numero entre 1 y 3]: ")

        if modo == "3":
            break
        if modo not in ["1", "2"]:
            continue

        print("\nSELECCION DE MAPA")
        print("1. Alta Densidad")
        print("2. Media Densidad")
        print("3. Baja Densidad")
        opcion_mapa = input("Selecciona un mapa [numero entre 1 y 3]: ")

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
        opcion_algoritmo = input("Selecciona un algoritmo [numero entre 1 y 5]: ")

        if opcion_algoritmo not in diccionario_algoritmos:
            continue

        nombre_algoritmo, funcion_algoritmo = diccionario_algoritmos[opcion_algoritmo]

        if modo == "1":
            agentes = pedir_entero("\nIngrese cantidad de agentes [MINIMO 20 - MAXIMO 300]: ", 20, 300)
            ejecutar_simulacion_visual(mapa_seleccionado, funcion_algoritmo, nombre_algoritmo, agentes)
        elif modo == "2":
            iteraciones = pedir_entero("\nIngrese cantidad de iteraciones [MINIMO 80 - MAXIMO 200]: ", 80, 200)
            agentes = pedir_entero("Ingrese cantidad de agentes por cada iteracion [MINIMO 80 - MAXIMO 300]: ", 80, 300)
            benchmark(mapa_seleccionado, nombre_mapa, funcion_algoritmo, nombre_algoritmo, iteraciones, agentes)

if __name__ == "__main__":
    menu_principal()