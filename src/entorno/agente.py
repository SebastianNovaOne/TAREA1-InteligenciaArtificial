# Representa un agente individual en la simulacion
class Agente:
    def __init__(self, id_agente, posicion_inicial):
        self.id_agente = id_agente
        self.posicion = posicion_inicial
        self.estado = "VIVO"
        self.pasos_dados = 0

    def mover(self, nueva_posicion):
        if self.estado == "VIVO":
            self.posicion = nueva_posicion
            self.pasos_dados += 1

    def evacuar(self):
        self.estado = "EVACUADO"

    def morir(self):
        self.estado = "MUERTO"