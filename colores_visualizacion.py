import os

RESET = "\033[0m"
ROJO = "\033[91m"
VERDE = "\033[92m"
GRIS = "\033[90m"
AZUL = "\033[94m"
BLANCO = "\033[97m"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_mapa_consola(matriz_mapa, posiciones_agentes):
    mapa_visual = matriz_mapa.astype(str)

    for pos in posiciones_agentes:
        mapa_visual[pos] = "A"

    for fila in mapa_visual:
        linea_formateada = ""
        for valor in fila:
            if valor == "1":
                linea_formateada += f"{GRIS}██{RESET}"
            elif valor == "2":
                linea_formateada += f"{ROJO}FF{RESET}"
            elif valor == "3":
                linea_formateada += f"{VERDE}SS{RESET}"
            elif valor == "A":
                linea_formateada += f"{AZUL}AA{RESET}"
            else:
                linea_formateada += f"{BLANCO}  {RESET}"
        print(linea_formateada)