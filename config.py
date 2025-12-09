"""
Configuración centralizada para Yu-Gi-Oh! Forbidden Memories
"""

# ============================================================================
# 1. CONFIGURACIÓN DE VENTANA Y RENDIMIENTO
# ============================================================================
WINDOW_WIDTH = 1400          # Ancho de la ventana
WINDOW_HEIGHT = 720          # Alto de la ventana
FPS = 30                     # Cuadros por segundo

# ============================================================================
# 2. CONFIGURACIÓN DEL JUEGO
# ============================================================================
# Sistema de vida y turnos
STARTING_LP = 8000           # Puntos de vida iniciales
MAX_LP = 9999                # Límite máximo de LP

# Tamaños de mazos y manos (configurables según enunciado)
DECK_SIZE = 20               # Tamaño del mazo (15, 20, 30, 40 - máximo 40)
HAND_SIZE = 5                # Cartas en mano inicial
MAX_HAND_SIZE = 7            # Límite máximo de cartas en mano
MAX_MONSTERS = 5             # Monstruos máximos en campo por jugador

# ============================================================================
# 3. CONFIGURACIÓN DE IA (MINIMAX)
# ============================================================================
MINIMAX_DEPTH = 2            # Profundidad del árbol de búsqueda

# ============================================================================
# 4. RUTAS DE ARCHIVOS
# ============================================================================
CARDS_FILE = "data/cards.json"
FUSIONS_FILE = "data/fusions.json"

# ============================================================================
# 5. CONSTANTES DE DISEÑO (para UI)
# ============================================================================
# Colores base
COLORS = {
    # Fondos
    'bg_dark': (10, 30, 50),
    'bg_medium': (20, 50, 80),
    'bg_light': (40, 80, 120),
    
    # Jugadores
    'player_primary': (100, 255, 100),
    'player_secondary': (50, 200, 50),
    'player_dark': (20, 80, 20),
    
    'ai_primary': (255, 100, 100),
    'ai_secondary': (200, 50, 50),
    'ai_dark': (80, 20, 20),
    
    # Elementos UI
    'border_gold': (255, 215, 0),
    'border_silver': (200, 200, 220),
    'text_white': (255, 255, 255),
    'text_gold': (255, 215, 0),
    'text_gray': (150, 150, 150),
    'text_dark': (50, 50, 50),
}

# Tamaños de fuentes
FONT_SIZES = {
    'tiny': 12,
    'small': 16,
    'normal': 20,
    'large': 24,
    'title': 32,
    'huge': 40,
}