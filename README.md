# TAREA1-InteligenciaArtificial
# Sebastián Nova Sánchez

# Simulador de evacuación de incendios

Simula un incendio en 3 mapas de 30x30 y compara 5 algoritmos que controlan a los agentes:
BFS, UCS, Greedy, A* y un algoritmo genético.

## Requisitos
- Python
- NumPy: `pip install numpy`
- Una terminal moderna (usa colores). Para el modo visual conviene agrandarla como mencionado en el informe.

## Estructura
```
main.py                 # menú principal (se ejecuta este)
benchmark.py            # modo benchmarking
visualizacion.py        # modo visualización
colores_visualizacion.py
src/
  entorno/              # agente.py, entorno.py, mapas.py
  algoritmos/           # busqueda_no_informada.py, busqueda_informada.py, algoritmo_genetico.py
  evaluacion/           # metricas.py
```

## Cómo ejecutarlo
Desde la carpeta del proyecto ejecutar lo siguiente en la terminal:
```
python main.py




```
El menú pide, en orden: el modo, el mapa (Alta, Media o Baja densidad) y el algoritmo.

**Modo 1 - Visualización:** una sola iteración en la terminal.
Pide la cantidad de agentes (20 a 300). Azul `AA` = agente, rojo `FF` = fuego, verde `SS` = salida.
Al terminar muestra los supervivientes y el turno del último evacuado.

**Modo 2 - Benchmarking:** varias iteraciones sin visualización.
Pide la cantidad de iteraciones (80 a 200) y de agentes (80 a 300).
Al terminar muestra la tasa de supervivencia y la media, desviación estándar, mínimo y máximo del
tiempo de despeje (turno en que sale el último sobreviviente). Presiona Enter para volver al menú.

Si escribes un valor fuera de rango o que no sea un número entero, el programa vuelve a preguntar.

## Parámetros modificables
- `benchmark.py`: `semilla_base` (1000), `k` (2, el fuego se propaga cada k turnos),
  `sensibilidad` (3.5, costo de congestión) y `capacidad` (3, agentes por celda).
- `visualizacion.py`: los mismos parámetros dentro de `EntornoSimulacion(...)`.
- `src/entorno/mapas.py`: las matrices de los mapas (1 = pared, 0 = libre, 2 = fuego inicial, 3 = salida).

## Notas
- A veces el primer menú aparece dos veces si quedó un Enter pendiente en la terminal. No afecta, el programa funciona bien igualmente.
