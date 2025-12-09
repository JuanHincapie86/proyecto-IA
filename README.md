# Proyecto 2 - IA: Yu-Gi-Oh! Forbidden Memories con Minimax

Implementación en Python de una versión simplificada de Yu-Gi-Oh! Forbidden Memories
con IA usando algoritmo Minimax y una interfaz gráfica con Pygame.

## 📋 Características Implementadas

### ✅ Requisitos Cumplidos

1. **80 Cartas Disponibles** - El juego incluye 80 cartas únicas con diferentes atributos, niveles y tipos
2. **30 Fusiones Definidas** - Más de 30 combinaciones de fusión implementadas (supera el mínimo de 15)
3. **Interfaz Gráfica Completa** - GUI con Pygame que muestra:
   - Campos de batalla de ambos jugadores
   - Manos de cartas
   - Life Points (LP)
   - Mazos boca abajo
   - **Panel de mazos visibles** (característica clave)
   
4. **Visibilidad Total de Mazos** - A diferencia del juego original:
   - Se pueden ver TODAS las cartas de ambos mazos
   - El orden de las cartas es conocido desde el inicio
   - No hay sorpresas en las cartas que se van sacando
   - Panel lateral muestra las próximas cartas de cada mazo

5. **IA con Minimax** - Algoritmo minimax implementado con profundidad configurable
6. **Regla de 1 Acción por Turno** - Después de invocar, fusionar o atacar, el turno pasa automáticamente a la IA
7. **Mazo Configurable** - Tamaño del mazo ajustable en `config.py` (máximo 40 cartas)
8. **El Jugador Siempre Inicia** - El humano tiene el primer turno
9. **Sin Cartas Mágicas ni Trampa** - Solo batallas de monstruos

## 🎮 Cómo Jugar

### Acciones Disponibles:
1. **Invocar**: Selecciona 1 carta de tu mano → botón "Invocar"
2. **Fusionar**: Selecciona 2 cartas de tu mano → botón "Fusionar"
3. **Atacar**: 
   - Clic en tu monstruo (se marca en amarillo)
   - Clic en un monstruo enemigo, o
   - Botón "Atacar directo" (solo si la IA no tiene monstruos)
4. **Pasar Turno**: Botón "Fin de turno" (sin realizar acción)

### Reglas Importantes:
- **Solo 1 acción por turno**: Invocar, fusionar o atacar
- Tras cualquier acción, el turno pasa automáticamente a la IA
- Máximo 5 monstruos en el campo
- El juego termina cuando un jugador llega a 0 LP o se queda sin cartas

## 🔧 Configuración

Edita `config.py` para ajustar:
```python
DECK_SIZE = 20          # Tamaño del mazo (máx 40)
MINIMAX_DEPTH = 2       # Profundidad del algoritmo (mayor = IA más fuerte)
STARTING_LP = 8000      # Life Points iniciales
HAND_SIZE = 5           # Cartas en la mano inicial
```

## 📦 Instalación y Ejecución

```bash
pip install -r requirements.txt
python main.py
```

## 📁 Estructura del Proyecto

```
├── main.py              # Punto de entrada
├── gui.py               # Interfaz gráfica (Pygame)
├── game_models.py       # Lógica del juego
├── ai_minimax.py        # IA con algoritmo Minimax
├── config.py            # Configuración
├── requirements.txt     # Dependencias
└── data/
    ├── cards.json       # 80 cartas definidas
    └── fusions.json     # 30+ fusiones
```

## 🎯 Diferencias con el Juego Original

### Característica Clave: **Información Completa**
En el juego original de Yu-Gi-Oh! Forbidden Memories, las cartas del mazo son desconocidas hasta que se roban. En esta versión:

- ✅ Ambos jugadores pueden ver **todas las cartas** de ambos mazos
- ✅ El **orden exacto** en que aparecerán las cartas es conocido
- ✅ La IA puede planificar con **información perfecta**
- ✅ Panel lateral derecho muestra las próximas 8 cartas de cada mazo

Esto convierte el juego en un problema de **estrategia determinista** ideal para algoritmos de búsqueda como Minimax.

## 🧠 Implementación de la IA

- **Algoritmo**: Minimax sin poda alfa-beta
- **Función de evaluación**: LP + ATK total en campo
- **Profundidad configurable**: Por defecto 2 (ajustable en `config.py`)
- **Tipos de jugadas**: Invocar, fusionar, atacar

## 👥 Notas de Desarrollo

- Desarrollado en Python 3 con Pygame
- Orientado a objetos con dataclasses
- Sin dependencias externas complejas
- Código documentado y modular

---
**Proyecto de Inteligencia Artificial - Minimax en Juegos de Cartas**
