import numpy as np


class Metricas:
    @staticmethod
    def calcular_estadisticas(tiempos, supervivientes, total_agentes_por_prueba):
        tasa_supervivencia_media = (np.mean(supervivientes) / total_agentes_por_prueba) * 100

        if len(tiempos) > 0:
            media_tiempo = np.mean(tiempos)
            desviacion_tiempo = np.std(tiempos)
            min_tiempo = np.min(tiempos)
            max_tiempo = np.max(tiempos)
        else:
            media_tiempo = 0
            desviacion_tiempo = 0
            min_tiempo = 0
            max_tiempo = 0

        return {
            "supervivencia_media_pct": round(tasa_supervivencia_media, 2),
            "tiempo_media": round(media_tiempo, 2),
            "tiempo_std": round(desviacion_tiempo, 2),
            "tiempo_min": min_tiempo,
            "tiempo_max": max_tiempo
        }

