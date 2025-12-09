"""
GUI mejorada para Yu-Gi-Oh! Forbidden Memories
Interfaz gráfica más clara y organizada
"""
import pygame
import sys
from typing import List, Optional, Tuple, Dict
import math

import config
from game_models import GameState, create_initial_game_state, Move, Card
from ai_minimax import choose_ai_move


class UIStyles:
    """Clase para almacenar todos los estilos de la UI"""
    
    # Colores principales
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
        
        # Botones
        'btn_summon': (50, 180, 80),
        'btn_fusion': (180, 50, 180),
        'btn_attack': (220, 60, 60),
        'btn_end': (60, 100, 220),
        'btn_hover': (80, 160, 240),
        
        # Cartas por atributo
        'attr_light': (255, 255, 180),
        'attr_dark': (140, 100, 180),
        'attr_fire': (240, 120, 80),
        'attr_water': (80, 180, 240),
        'attr_earth': (180, 140, 100),
        'attr_wind': (170, 240, 200),
        'attr_default': (160, 160, 160),
    }
    
    # Atributos con colores
    ATTRIBUTE_COLORS = {
        "Luz": COLORS['attr_light'],
        "Oscuridad": COLORS['attr_dark'],
        "Fuego": COLORS['attr_fire'],
        "Agua": COLORS['attr_water'],
        "Tierra": COLORS['attr_earth'],
        "Viento": COLORS['attr_wind'],
    }
    
    # Símbolos de atributos
    ATTRIBUTE_SYMBOLS = {
        "Luz": "☀️",
        "Oscuridad": "🌙",
        "Fuego": "🔥",
        "Agua": "💧",
        "Tierra": "🌍",
        "Viento": "💨",
    }
    
    # Tamaños de fuentes - optimizados para mejor espaciado
    FONT_SIZES = {
        'tiny': 10,
        'small': 13,
        'normal': 16,
        'large': 20,
        'title': 28,
        'huge': 36,
    }


class UIConstants:
    """Constantes de diseño para la UI"""
    
    # Dimensiones de elementos - optimizadas
    CARD_WIDTH = 95
    CARD_HEIGHT = 120
    CARD_SPACING = 10
    BUTTON_WIDTH = 140
    BUTTON_HEIGHT = 36
    PANEL_WIDTH = 260
    
    # Posiciones y áreas
    AREAS = {
        'top_bar': (0, 0, config.WINDOW_WIDTH, 70),
        'ai_field': (0, 70, config.WINDOW_WIDTH, 160),
        'divider': (0, 230, config.WINDOW_WIDTH, 10),
        'player_field': (0, 240, config.WINDOW_WIDTH, 160),
        'hand_area': (0, 400, config.WINDOW_WIDTH, 150),
        'buttons_area': (0, 550, config.WINDOW_WIDTH, 70),
        'message_area': (0, 620, config.WINDOW_WIDTH, 50),
        'info_panel': (config.WINDOW_WIDTH - 300, 70, 280, 200),
        'deck_panel': (config.WINDOW_WIDTH - 300, 280, 280, 200),
        'history_panel': (20, 70, 260, 200),
    }
    
    # Margenes
    MARGIN_SMALL = 10
    MARGIN_MEDIUM = 20
    MARGIN_LARGE = 30


class UIComponent:
    """Clase base para componentes de la UI"""
    
    def __init__(self, app):
        self.app = app
        self.styles = UIStyles()
        self.constants = UIConstants()
    
    def draw_rounded_rect(self, surface, rect, color, radius=10, border=0, border_color=None):
        """Dibuja un rectángulo con bordes redondeados"""
        if border > 0 and border_color:
            # Borde exterior
            pygame.draw.rect(surface, border_color, rect, border_radius=radius)
        
        # Rectángulo interior
        inner_rect = rect.inflate(-border*2, -border*2) if border > 0 else rect
        pygame.draw.rect(surface, color, inner_rect, border_radius=radius)
    
    def draw_text_with_shadow(self, text, font, x, y, color, shadow_color=(0, 0, 0), shadow_offset=2):
        """Dibuja texto con sombra para mejor legibilidad"""
        shadow = font.render(text, True, shadow_color)
        text_surface = font.render(text, True, color)
        
        self.app.screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
        self.app.screen.blit(text_surface, (x, y))
        
        return text_surface


class GameApp:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("⚡ Yu-Gi-Oh! Forbidden Memories - Minimax AI ⚡")
        self.clock = pygame.time.Clock()
        
        # Componentes de UI
        self.ui = UIComponent(self)
        
        # Inicializar fuentes
        self.init_fonts()
        
        # Estado del juego
        self.state: GameState = create_initial_game_state()
        
        # Interacción
        self.selected_hand_indices: List[int] = []
        self.selected_attacker_slot: Optional[int] = None
        self.hovered_element = None
        self.hovered_card_index = None
        
        # Mensajes
        self.message: str = (
            "¡Bienvenido! Tu turno. Selecciona 1 carta para INVOCAR o 2 para FUSIONAR. "
            "O selecciona un monstruo tuyo para ATACAR. Solo 1 acción por turno."
        )
        
        # Crear áreas rectangulares
        self.areas = {name: pygame.Rect(*coords) for name, coords in UIConstants.AREAS.items()}
        
        # Crear botones
        self.create_buttons()
        
        # Historial
        self.action_history = []
        
        # Efectos
        self.effect_timer = 0
        self.active_effect = None

    def init_fonts(self):
        """Inicializa todas las fuentes necesarias"""
        self.fonts = {
            'tiny': pygame.font.SysFont("Arial", UIStyles.FONT_SIZES['tiny']),
            'small': pygame.font.SysFont("Arial", UIStyles.FONT_SIZES['small']),
            'normal': pygame.font.SysFont("Arial", UIStyles.FONT_SIZES['normal']),
            'large': pygame.font.SysFont("Arial", UIStyles.FONT_SIZES['large'], bold=True),
            'title': pygame.font.SysFont("Arial", UIStyles.FONT_SIZES['title'], bold=True),
            'huge': pygame.font.SysFont("Arial", UIStyles.FONT_SIZES['huge'], bold=True),
        }

    def create_buttons(self):
        """Crea todos los botones de la interfaz"""
        area = self.areas['buttons_area']
        button_y = area.y + 15
        spacing = 20
        total_width = 4 * UIConstants.BUTTON_WIDTH + 3 * spacing
        start_x = (config.WINDOW_WIDTH - total_width) // 2
        
        self.buttons = {
            'summon': pygame.Rect(start_x, button_y, UIConstants.BUTTON_WIDTH, UIConstants.BUTTON_HEIGHT),
            'fusion': pygame.Rect(start_x + UIConstants.BUTTON_WIDTH + spacing, button_y, 
                                 UIConstants.BUTTON_WIDTH, UIConstants.BUTTON_HEIGHT),
            'attack': pygame.Rect(start_x + 2*(UIConstants.BUTTON_WIDTH + spacing), button_y, 
                                 UIConstants.BUTTON_WIDTH, UIConstants.BUTTON_HEIGHT),
            'end_turn': pygame.Rect(start_x + 3*(UIConstants.BUTTON_WIDTH + spacing), button_y, 
                                   UIConstants.BUTTON_WIDTH, UIConstants.BUTTON_HEIGHT),
        }
        
        # Botón de reinicio
        self.button_restart = pygame.Rect(
            config.WINDOW_WIDTH // 2 - 100, 300, 200, 50
        )

    # -------------------------------------------------
    # Control del juego
    # -------------------------------------------------
    def reset_game(self) -> None:
        """Reinicia el juego a su estado inicial"""
        self.state = create_initial_game_state()
        self.selected_hand_indices = []
        self.selected_attacker_slot = None
        self.hovered_element = None
        self.hovered_card_index = None
        self.message = "¡Nueva partida! Comienza el jugador. ¡Buena suerte!"
        self.action_history = []
        self.active_effect = None

    def run(self) -> None:
        """Bucle principal del juego"""
        while True:
            self.clock.tick(config.FPS)
            self.handle_events()
            
            if not self.state.finished:
                self.update()
            
            self.render()

    # -------------------------------------------------
    # Manejo de eventos
    # -------------------------------------------------
    def handle_events(self) -> None:
        """Maneja todos los eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state.finished:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.button_restart.collidepoint(mx, my):
                        self.reset_game()
                continue
            
            if self.state.current_turn != "player":
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                self.handle_mouse_click(mx, my)
            
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                self.handle_mouse_hover(mx, my)

    def handle_mouse_click(self, mx: int, my: int) -> None:
        """Maneja clics del mouse"""
        # 1. Cartas en mano
        hand_rects = self.get_hand_rects()
        for idx, rect in enumerate(hand_rects):
            if rect.collidepoint(mx, my) and idx < len(self.state.player.hand):
                self.handle_hand_click(idx)
                return
        
        # 2. Monstruos del jugador
        player_field_rects = self.get_field_rects(self.areas['player_field'].y + 30)
        for idx, rect in enumerate(player_field_rects):
            if rect.collidepoint(mx, my) and self.state.player.monster_zone[idx] is not None:
                self.handle_select_attacker(idx)
                return
        
        # 3. Monstruos de la IA
        ai_field_rects = self.get_field_rects(self.areas['ai_field'].y + 30)
        for idx, rect in enumerate(ai_field_rects):
            if rect.collidepoint(mx, my) and self.state.ai.monster_zone[idx] is not None:
                self.handle_attack_target(idx)
                return
        
        # 4. Botones
        button_actions = {
            'summon': self.do_player_summon,
            'fusion': self.do_player_fusion,
            'attack': self.do_player_direct_attack,
            'end_turn': self.end_player_turn,
        }
        
        for btn_name, action in button_actions.items():
            if self.buttons[btn_name].collidepoint(mx, my):
                action()
                return

    def handle_mouse_hover(self, mx: int, my: int) -> None:
        """Maneja el hover del mouse para tooltips"""
        self.hovered_element = None
        self.hovered_card_index = None
        
        # Cartas en mano
        hand_rects = self.get_hand_rects()
        for idx, rect in enumerate(hand_rects):
            if rect.collidepoint(mx, my) and idx < len(self.state.player.hand):
                self.hovered_card_index = idx
                return
        
        # Botones
        for btn_name, rect in self.buttons.items():
            if rect.collidepoint(mx, my):
                self.hovered_element = ('button', btn_name)
                return

    # -------------------------------------------------
    # Lógica del jugador
    # -------------------------------------------------
    def handle_hand_click(self, idx: int) -> None:
        """Maneja clic en una carta de la mano"""
        self.selected_attacker_slot = None
        
        if idx in self.selected_hand_indices:
            self.selected_hand_indices.remove(idx)
        else:
            if len(self.selected_hand_indices) < 2:
                self.selected_hand_indices.append(idx)
        
        # Actualizar mensaje
        self.update_selection_message()

    def update_selection_message(self):
        """Actualiza el mensaje según la selección actual"""
        if len(self.selected_hand_indices) == 0:
            self.message = "Selecciona cartas de tu mano para jugar."
        
        elif len(self.selected_hand_indices) == 1:
            card_id = self.state.player.hand[self.selected_hand_indices[0]]
            card = self.state.cards[card_id]
            self.message = f"Seleccionada: {card.name} (ATK: {card.attack}). Selecciona otra para FUSIONAR o presiona INVOCAR."
        
        else:
            idx1, idx2 = sorted(self.selected_hand_indices)
            card1_id = self.state.player.hand[idx1]
            card2_id = self.state.player.hand[idx2]
            card1 = self.state.cards[card1_id]
            card2 = self.state.cards[card2_id]
            
            fusion_key = tuple(sorted((card1_id, card2_id)))
            if fusion_key in self.state.fusions:
                result_id = self.state.fusions[fusion_key]
                result_card = self.state.cards[result_id]
                self.message = f"¡FUSIÓN DISPONIBLE! {card1.name} + {card2.name} = {result_card.name} (ATK: {result_card.attack})"
            else:
                self.message = f"NO HAY FUSIÓN: {card1.name} + {card2.name}. Selecciona otra combinación."

    def handle_select_attacker(self, slot_index: int) -> None:
        """Selecciona un monstruo del campo como atacante"""
        self.selected_hand_indices.clear()
        self.selected_attacker_slot = slot_index
        
        card_id = self.state.player.monster_zone[slot_index]
        card = self.state.cards[card_id]
        self.message = f"Atacante seleccionado: {card.name}. Ahora selecciona un monstruo enemigo o usa 'Atacar' para ataque directo."

    def handle_attack_target(self, target_slot: int) -> None:
        """Ataca a un monstruo enemigo"""
        if self.selected_attacker_slot is None:
            self.message = "Primero selecciona un monstruo tuyo para atacar."
            return
        
        move = Move(kind="attack", params={
            "attacker_slot": self.selected_attacker_slot,
            "defender_slot": target_slot
        })
        
        # Registrar acción
        attacker_card = self.state.cards[self.state.player.monster_zone[self.selected_attacker_slot]]
        defender_card = self.state.cards[self.state.ai.monster_zone[target_slot]]
        self.action_history.append(f"Jugador ataca: {attacker_card.name} → {defender_card.name}")
        
        self.state.apply_move(move)
        self.selected_attacker_slot = None
        self.message = "¡Ataque realizado! Turno de la IA..."

    def do_player_direct_attack(self) -> None:
        """Realiza un ataque directo"""
        if self.selected_attacker_slot is None:
            self.message = "Selecciona primero un monstruo tuyo para atacar."
            return
        
        if any(cid is not None for cid in self.state.ai.monster_zone):
            self.message = "No puedes atacar directo: la IA tiene monstruos en su campo."
            return
        
        move = Move(kind="attack", params={
            "attacker_slot": self.selected_attacker_slot,
            "defender_slot": None
        })
        
        # Registrar acción
        attacker_card = self.state.cards[self.state.player.monster_zone[self.selected_attacker_slot]]
        self.action_history.append(f"Jugador ataque directo: {attacker_card.name} → LP IA")
        
        self.state.apply_move(move)
        self.selected_attacker_slot = None
        self.message = "¡Ataque directo realizado! Turno de la IA..."

    def do_player_summon(self) -> None:
        """Realiza una invocación normal"""
        if len(self.selected_hand_indices) != 1:
            self.message = "Para invocar, selecciona EXACTAMENTE 1 carta en tu mano."
            return
        
        player = self.state.player
        free_slots = [i for i, c in enumerate(player.monster_zone) if c is None]
        
        if not free_slots:
            self.message = "No tienes espacio libre en el campo para invocar (máximo 5 monstruos)."
            return
        
        hand_index = self.selected_hand_indices[0]
        card_id = player.hand[hand_index]
        card = self.state.cards[card_id]
        
        move = Move(kind="summon", params={
            "hand_index": hand_index,
            "slot_index": free_slots[0]
        })
        
        # Registrar acción
        self.action_history.append(f"Jugador invoca: {card.name}")
        
        self.state.apply_move(move)
        self.selected_hand_indices.clear()
        self.message = f"¡Has invocado a {card.name}! Turno de la IA..."

    def do_player_fusion(self) -> None:
        """Realiza una fusión"""
        if len(self.selected_hand_indices) != 2:
            self.message = "Para fusionar, selecciona EXACTAMENTE 2 cartas en tu mano."
            return
        
        player = self.state.player
        free_slots = [i for i, c in enumerate(player.monster_zone) if c is None]
        
        if not free_slots:
            self.message = "No tienes espacio libre en el campo para la carta fusionada."
            return
        
        idx1, idx2 = sorted(self.selected_hand_indices)
        card1_id = player.hand[idx1]
        card2_id = player.hand[idx2]
        
        fusion_key = tuple(sorted((card1_id, card2_id)))
        
        if fusion_key not in self.state.fusions:
            self.message = "Esas cartas no se pueden fusionar. Selecciona otra combinación."
            return
        
        result_id = self.state.fusions[fusion_key]
        result_card = self.state.cards[result_id]
        card1 = self.state.cards[card1_id]
        card2 = self.state.cards[card2_id]
        
        move = Move(kind="fusion", params={
            "hand_index_1": idx1,
            "hand_index_2": idx2,
            "slot_index": free_slots[0]
        })
        
        # Registrar acción y activar efecto
        self.action_history.append(f"Jugador fusiona: {card1.name} + {card2.name} = {result_card.name}")
        self.trigger_fusion_effect(free_slots[0], False)
        
        self.state.apply_move(move)
        self.selected_hand_indices.clear()
        self.message = f"¡FUSIÓN EXITOSA! Has invocado a {result_card.name}! Turno de la IA..."

    def end_player_turn(self) -> None:
        """Termina el turno del jugador sin realizar acción"""
        self.selected_hand_indices.clear()
        self.selected_attacker_slot = None
        
        # Registrar acción
        self.action_history.append("Jugador pasa turno")
        
        self.state.switch_turn()
        self.state.draw_card(self.state.get_active_player())
        self.state.check_game_over()
        
        self.message = "Has terminado tu turno. Ahora juega la IA."

    def trigger_fusion_effect(self, slot_index: int, is_ai: bool) -> None:
        """Activa efecto visual de fusión"""
        self.active_effect = {
            'type': 'fusion',
            'timer': 30,
            'slot': slot_index,
            'is_ai': is_ai
        }

    # -------------------------------------------------
    # Lógica de la IA
    # -------------------------------------------------
    def update(self) -> None:
        """Actualiza el estado del juego (turno de la IA)"""
        if self.state.finished:
            return
        
        # Actualizar efectos
        if self.active_effect:
            self.active_effect['timer'] -= 1
            if self.active_effect['timer'] <= 0:
                self.active_effect = None
        
        # Turno de la IA
        if self.state.current_turn == "ai":
            move = choose_ai_move(self.state)
            
            if move is not None:
                self.log_ai_move(move)
                self.state.apply_move(move)
                self.message = "La IA ha realizado su jugada. Tu turno."
            else:
                self.action_history.append("IA pasa turno")
                self.state.switch_turn()
                self.state.draw_card(self.state.get_active_player())
                self.state.check_game_over()
                self.message = "La IA pasa. Tu turno."

    def log_ai_move(self, move: Move) -> None:
        """Registra la acción de la IA en el historial"""
        if move.kind == "summon":
            card_id = self.state.ai.hand[move.params["hand_index"]]
            card = self.state.cards[card_id]
            self.action_history.append(f"IA invoca: {card.name}")
        
        elif move.kind == "fusion":
            idx1 = move.params["hand_index_1"]
            idx2 = move.params["hand_index_2"]
            card1_id = self.state.ai.hand[idx1]
            card2_id = self.state.ai.hand[idx2]
            card1 = self.state.cards[card1_id]
            card2 = self.state.cards[card2_id]
            
            fusion_key = tuple(sorted((card1_id, card2_id)))
            if fusion_key in self.state.fusions:
                result_id = self.state.fusions[fusion_key]
                result_card = self.state.cards[result_id]
                self.action_history.append(f"IA fusiona: {card1.name} + {card2.name} = {result_card.name}")
                self.trigger_fusion_effect(move.params["slot_index"], True)
        
        elif move.kind == "attack":
            attacker_slot = move.params["attacker_slot"]
            defender_slot = move.params.get("defender_slot")
            
            if defender_slot is None:
                attacker_card = self.state.cards[self.state.ai.monster_zone[attacker_slot]]
                self.action_history.append(f"IA ataque directo: {attacker_card.name} → LP Jugador")
            else:
                attacker_card = self.state.cards[self.state.ai.monster_zone[attacker_slot]]
                defender_card = self.state.cards[self.state.player.monster_zone[defender_slot]]
                self.action_history.append(f"IA ataca: {attacker_card.name} → {defender_card.name}")

    # -------------------------------------------------
    # Renderizado - Métodos principales
    # -------------------------------------------------
    def render(self) -> None:
        """Renderiza toda la interfaz"""
        # 1. Fondo
        self.draw_background()
        
        # 2. Áreas principales
        self.draw_game_areas()
        
        # 3. Elementos del juego
        self.draw_life_bars_and_turn()
        self.draw_monster_fields()
        self.draw_player_hand()
        self.draw_deck_piles()
        self.draw_action_buttons()
        
        # 4. Paneles de información
        self.draw_info_panel()
        self.draw_deck_panel()
        self.draw_history_panel()
        
        # 5. Mensajes y efectos
        self.draw_messages()
        self.draw_tooltips()
        self.draw_effects()
        
        # 6. Pantalla de fin de juego
        if self.state.finished:
            self.draw_game_over_screen()
        
        pygame.display.flip()

    def draw_background(self) -> None:
        """Dibuja el fondo con gradiente"""
        # Gradiente azul oscuro
        for y in range(config.WINDOW_HEIGHT):
            r = int(15 + (y / config.WINDOW_HEIGHT) * 25)
            g = int(40 + (y / config.WINDOW_HEIGHT) * 35)
            b = int(70 + (y / config.WINDOW_HEIGHT) * 30)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (config.WINDOW_WIDTH, y))
        
        # Línea divisoria central
        center_y = self.areas['divider'].centery
        pygame.draw.line(self.screen, UIStyles.COLORS['border_gold'], 
                        (0, center_y), (config.WINDOW_WIDTH, center_y), 3)
        
        # Patrón de tablero sutil
        self.draw_board_pattern()

    def draw_board_pattern(self) -> None:
        """Dibuja un patrón sutil de tablero"""
        # Líneas verticales tenues
        for x in range(0, config.WINDOW_WIDTH, 60):
            alpha_surface = pygame.Surface((1, config.WINDOW_HEIGHT), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, 10))
            self.screen.blit(alpha_surface, (x, 0))
        
        # Líneas horizontales en campos
        for area_name in ['ai_field', 'player_field']:
            area = self.areas[area_name]
            for y in range(area.top + 20, area.bottom, 40):
                alpha_surface = pygame.Surface((area.width, 1), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, 15))
                self.screen.blit(alpha_surface, (area.left, y))

    def draw_game_areas(self) -> None:
        """Dibuja las áreas definidas de la interfaz"""
        # Campos con bordes
        for area_name in ['ai_field', 'player_field']:
            area = self.areas[area_name]
            color = UIStyles.COLORS['ai_dark'] if 'ai' in area_name else UIStyles.COLORS['player_dark']
            
            # Fondo semi-transparente
            alpha_surface = pygame.Surface((area.width, area.height), pygame.SRCALPHA)
            alpha_surface.fill((*color, 150))
            self.screen.blit(alpha_surface, area)
            
            # Borde
            pygame.draw.rect(self.screen, UIStyles.COLORS['border_gold'], area, 3, border_radius=5)
        
        # Área de mano
        hand_area = self.areas['hand_area']
        alpha_surface = pygame.Surface((hand_area.width, hand_area.height), pygame.SRCALPHA)
        alpha_surface.fill((30, 50, 80, 180))
        self.screen.blit(alpha_surface, hand_area)
        
        # Borde del área de mano
        pygame.draw.rect(self.screen, UIStyles.COLORS['border_silver'], hand_area, 2, border_radius=5)

    def draw_life_bars_and_turn(self) -> None:
        """Dibuja las barras de vida y el indicador de turno"""
        # Barras de vida
        self.draw_life_bar(self.state.player.life_points, True)
        self.draw_life_bar(self.state.ai.life_points, False)
        
        # Indicador de turno
        self.draw_turn_indicator()

    def draw_life_bar(self, life_points: int, is_player: bool) -> None:
        """Dibuja una barra de vida"""
        bar_width = 300
        bar_height = 28
        margin = 20
        top_margin = 15
        
        # Calcular porcentaje
        percent = max(0, life_points) / config.STARTING_LP
        
        # Posición
        if is_player:
            x = margin
            color = UIStyles.COLORS['player_primary']
        else:
            x = config.WINDOW_WIDTH - bar_width - margin
            color = UIStyles.COLORS['ai_primary']
        
        y = top_margin
        fill_width = int(bar_width * percent)
        
        # Fondo de la barra
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        self.ui.draw_rounded_rect(self.screen, bg_rect, (40, 40, 40), radius=5)
        
        # Relleno
        if fill_width > 0:
            fill_rect = pygame.Rect(x, y, fill_width, bar_height)
            self.ui.draw_rounded_rect(self.screen, fill_rect, color, radius=5)
        
        # Borde
        self.ui.draw_rounded_rect(self.screen, bg_rect, UIStyles.COLORS['border_silver'], 
                                 radius=5, border=2, border_color=UIStyles.COLORS['border_gold'])
        
        # Texto
        lp_text = f"{life_points} LP"
        text_color = UIStyles.COLORS['text_white'] if percent > 0.3 else (255, 100, 100)
        text_surface = self.fonts['large'].render(lp_text, True, text_color)
        
        # Sombra del texto
        shadow = self.fonts['large'].render(lp_text, True, (0, 0, 0))
        self.screen.blit(shadow, (x + bar_width//2 - text_surface.get_width()//2 + 2, y + 5))
        self.screen.blit(text_surface, (x + bar_width//2 - text_surface.get_width()//2, y + 3))

    def draw_turn_indicator(self) -> None:
        """Dibuja el indicador de turno"""
        if self.state.current_turn == 'player':
            text = "🎮 TU TURNO 🎮"
            color = (120, 255, 150)
            bg_start = (30, 100, 50)
            bg_end = (10, 60, 30)
        else:
            text = "🤖 TURNO IA 🤖"
            color = (255, 120, 120)
            bg_start = (100, 30, 30)
            bg_end = (60, 10, 10)
        
        # Efecto de pulsación
        pulse = int(8 * abs(pygame.time.get_ticks() % 1200 - 600) / 600)
        
        # Fondo del indicador
        indicator_rect = pygame.Rect(
            config.WINDOW_WIDTH // 2 - 190,
            8,
            380,
            50
        )
        
        # Sombra
        shadow_rect = indicator_rect.move(3, 3)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 150), shadow_surf.get_rect(), border_radius=12)
        self.screen.blit(shadow_surf, shadow_rect.topleft)
        
        # Gradiente de fondo
        for i in range(indicator_rect.height):
            ratio = i / indicator_rect.height
            bg_color = tuple(int(bg_start[j] * (1 - ratio) + bg_end[j] * ratio + pulse // 2) for j in range(3))
            pygame.draw.line(self.screen, bg_color, 
                           (indicator_rect.x, indicator_rect.y + i), 
                           (indicator_rect.x + indicator_rect.width, indicator_rect.y + i))
        
        # Brillo superior
        shine_rect = pygame.Rect(indicator_rect.x + 10, indicator_rect.y + 5, indicator_rect.width - 20, 12)
        shine_surf = pygame.Surface((shine_rect.width, shine_rect.height), pygame.SRCALPHA)
        for i in range(shine_rect.height):
            alpha = int(70 * (1 - i / shine_rect.height))
            pygame.draw.line(shine_surf, (255, 255, 255, alpha), (0, i), (shine_rect.width, i))
        self.screen.blit(shine_surf, shine_rect.topleft)
        
        # Bordes con animación
        pygame.draw.rect(self.screen, (0, 0, 0), indicator_rect, 1, border_radius=12)
        border_color = tuple(min(255, c + pulse) for c in color)
        pygame.draw.rect(self.screen, border_color, indicator_rect, 4 + pulse // 3, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255), indicator_rect.inflate(-6, -6), 1, border_radius=11)
        
        # Texto con sombra
        turn_text = self.fonts['title'].render(text, True, color)
        text_x = config.WINDOW_WIDTH // 2 - turn_text.get_width() // 2
        self.ui.draw_text_with_shadow(text, self.fonts['title'], text_x, 13, color, shadow_offset=3)

    def draw_monster_fields(self) -> None:
        """Dibuja los campos de monstruos de ambos jugadores"""
        # Campo de la IA
        self.draw_field_label("🔴 CAMPO ENEMIGO", self.areas['ai_field'].y, False)
        self.draw_monster_row(self.state.ai.monster_zone, self.areas['ai_field'].y + 30, True)
        
        # Campo del jugador
        self.draw_field_label("🟢 TU CAMPO", self.areas['player_field'].y, True)
        self.draw_monster_row(self.state.player.monster_zone, self.areas['player_field'].y + 30, False)
        
        # Contadores de monstruos
        self.draw_monster_counts()

    def draw_field_label(self, text: str, y: int, is_player: bool) -> None:
        """Dibuja la etiqueta de un campo"""
        label = self.fonts['large'].render(text, True, 
                                          UIStyles.COLORS['player_primary'] if is_player 
                                          else UIStyles.COLORS['ai_primary'])
        
        # Fondo para la etiqueta
        label_bg = pygame.Rect(
            config.WINDOW_WIDTH // 2 - label.get_width() // 2 - 15,
            y + 5,
            label.get_width() + 30,
            35
        )
        
        bg_color = UIStyles.COLORS['player_dark'] if is_player else UIStyles.COLORS['ai_dark']
        self.ui.draw_rounded_rect(self.screen, label_bg, bg_color, radius=8)
        pygame.draw.rect(self.screen, UIStyles.COLORS['border_gold'], label_bg, 2, border_radius=8)
        
        # Texto
        self.screen.blit(label, (config.WINDOW_WIDTH // 2 - label.get_width() // 2, y + 10))

    def draw_monster_row(self, zone: List[Optional[int]], y: int, is_ai: bool) -> None:
        """Dibuja una fila de monstruos"""
        total_width = 5 * UIConstants.CARD_WIDTH + 4 * UIConstants.CARD_SPACING
        start_x = (config.WINDOW_WIDTH - total_width) // 2
        
        for i in range(5):
            x = start_x + i * (UIConstants.CARD_WIDTH + UIConstants.CARD_SPACING)
            rect = pygame.Rect(x, y, UIConstants.CARD_WIDTH, UIConstants.CARD_HEIGHT)
            
            cid = zone[i]
            if cid is not None:
                card = self.state.cards[cid]
                self.draw_monster_card(rect, card, is_ai, i)
            else:
                self.draw_empty_slot(rect, is_ai)

    def draw_monster_card(self, rect: pygame.Rect, card: Card, is_ai: bool, slot_index: int) -> None:
        """Dibuja una carta de monstruo en el campo"""
        # Color según atributo
        bg_color = UIStyles.ATTRIBUTE_COLORS.get(card.attribute, UIStyles.COLORS['attr_default'])
        
        # Fondo de la carta
        self.ui.draw_rounded_rect(self.screen, rect, bg_color, radius=8)
        
        # Borde según estado
        border_color = UIStyles.COLORS['border_silver']
        border_width = 2
        
        # Resaltar si es atacante seleccionado
        if not is_ai and self.selected_attacker_slot == slot_index:
            border_color = (255, 255, 0)
            border_width = 4
        
        pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=8)
        
        # Cabecera con nombre
        header_rect = pygame.Rect(rect.x, rect.y, rect.width, 30)
        pygame.draw.rect(self.screen, (40, 40, 40), header_rect, border_radius=8)
        
        # Nombre truncado
        display_name = card.name[:12] + "..." if len(card.name) > 12 else card.name
        name_text = self.fonts['small'].render(display_name, True, UIStyles.COLORS['text_white'])
        self.screen.blit(name_text, (rect.x + 5, rect.y + 8))
        
        # Atributo
        attr_symbol = UIStyles.ATTRIBUTE_SYMBOLS.get(card.attribute, "❓")
        attr_text = self.fonts['small'].render(attr_symbol, True, UIStyles.COLORS['text_gold'])
        self.screen.blit(attr_text, (rect.x + rect.width - 25, rect.y + 8))
        
        # Estadísticas
        self.draw_card_stats(rect, card.attack, card.defense)

    def draw_card_stats(self, rect: pygame.Rect, attack: int, defense: int) -> None:
        """Dibuja las estadísticas de una carta"""
        # Fondo para estadísticas
        stats_bg = pygame.Rect(rect.x + 5, rect.y + rect.height - 50, rect.width - 10, 45)
        self.ui.draw_rounded_rect(self.screen, stats_bg, (20, 20, 20, 200), radius=5)
        
        # ATK
        atk_text = self.fonts['normal'].render(f"⚔️ {attack}", True, (255, 100, 100))
        self.screen.blit(atk_text, (rect.x + 10, rect.y + rect.height - 45))
        
        # DEF
        def_text = self.fonts['small'].render(f"🛡️ {defense}", True, (100, 150, 255))
        self.screen.blit(def_text, (rect.x + 10, rect.y + rect.height - 25))

    def draw_empty_slot(self, rect: pygame.Rect, is_ai: bool) -> None:
        """Dibuja un espacio vacío en el campo"""
        color = UIStyles.COLORS['ai_dark'] if is_ai else UIStyles.COLORS['player_dark']
        self.ui.draw_rounded_rect(self.screen, rect, color, radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 2, border_radius=8)
        
        # Texto "Vacío"
        empty_text = self.fonts['small'].render("VACÍO", True, (150, 150, 150))
        self.screen.blit(empty_text, (rect.x + 30, rect.y + 60))

    def draw_monster_counts(self) -> None:
        """Dibuja los contadores de monstruos"""
        ai_count = sum(1 for c in self.state.ai.monster_zone if c is not None)
        player_count = sum(1 for c in self.state.player.monster_zone if c is not None)
        
        # IA
        ai_text = self.fonts['normal'].render(f"👹 Monstruos: {ai_count}/5", 
                                            True, UIStyles.COLORS['ai_primary'])
        self.screen.blit(ai_text, (config.WINDOW_WIDTH - 220, self.areas['ai_field'].y + 5))
        
        # Jugador
        player_text = self.fonts['normal'].render(f"🛡️ Monstruos: {player_count}/5", 
                                                True, UIStyles.COLORS['player_primary'])
        self.screen.blit(player_text, (config.WINDOW_WIDTH - 220, self.areas['player_field'].y + 5))

    def draw_player_hand(self) -> None:
        """Dibuja la mano del jugador"""
        # Título
        title = self.fonts['large'].render("🎴 TU MANO", True, UIStyles.COLORS['text_gold'])
        self.ui.draw_text_with_shadow("🎴 TU MANO", self.fonts['large'],
                                     config.WINDOW_WIDTH // 2 - title.get_width() // 2,
                                     self.areas['hand_area'].y + 10,
                                     UIStyles.COLORS['text_gold'])
        
        # Cartas
        hand_rects = self.get_hand_rects()
        for idx, rect in enumerate(hand_rects):
            if idx < len(self.state.player.hand):
                card_id = self.state.player.hand[idx]
                card = self.state.cards[card_id]
                self.draw_hand_card(rect, card, idx)
            else:
                self.draw_empty_hand_slot(rect)

    def draw_hand_card(self, rect: pygame.Rect, card: Card, hand_index: int) -> None:
        """Dibuja una carta en la mano del jugador"""
        # Efecto de elevación si está seleccionada
        draw_rect = rect.copy()
        is_selected = hand_index in self.selected_hand_indices
        
        if is_selected:
            draw_rect.y -= 20
            # Efecto de brillo pulsante
            pulse = int(8 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            glow_rect = draw_rect.inflate(8 + pulse, 8 + pulse)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 215, 0, 150), glow_surf.get_rect(), border_radius=12)
            self.screen.blit(glow_surf, glow_rect.topleft)
        
        # Sombra de la carta
        shadow_rect = draw_rect.move(2, 3)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 100), shadow_surf.get_rect(), border_radius=8)
        self.screen.blit(shadow_surf, shadow_rect.topleft)
        
        # Color según atributo
        bg_color = UIStyles.ATTRIBUTE_COLORS.get(card.attribute, UIStyles.COLORS['attr_default'])
        
        # Fondo de la carta con gradiente sutil
        for i in range(draw_rect.height):
            ratio = i / draw_rect.height
            color = tuple(min(255, int(bg_color[j] * (0.95 + ratio * 0.1))) for j in range(3))
            pygame.draw.line(self.screen, color, (draw_rect.x, draw_rect.y + i), (draw_rect.x + draw_rect.width, draw_rect.y + i))
        
        # Borde según selección
        pygame.draw.rect(self.screen, (0, 0, 0), draw_rect, 1, border_radius=8)
        border_color = (255, 255, 0) if is_selected else UIStyles.COLORS['border_silver']
        border_width = 5 if is_selected else 2
        pygame.draw.rect(self.screen, border_color, draw_rect, border_width, border_radius=8)
        
        if is_selected:
            pygame.draw.rect(self.screen, (255, 215, 0), draw_rect.inflate(-4, -4), 1, border_radius=7)
        
        # Cabecera
        header_rect = pygame.Rect(draw_rect.x, draw_rect.y, draw_rect.width, 25)
        pygame.draw.rect(self.screen, (40, 40, 40), header_rect, border_radius=8)
        
        # Nombre
        display_name = card.name[:14] + "..." if len(card.name) > 14 else card.name
        name_text = self.fonts['small'].render(display_name, True, UIStyles.COLORS['text_white'])
        self.screen.blit(name_text, (draw_rect.x + 5, draw_rect.y + 5))
        
        # Número de carta
        index_text = self.fonts['tiny'].render(f"#{hand_index + 1}", True, (200, 200, 200))
        self.screen.blit(index_text, (draw_rect.x + draw_rect.width - 25, draw_rect.y + 5))
        
        # Estadísticas
        self.draw_card_stats(draw_rect, card.attack, card.defense)
        
        # Resaltar si está siendo hovered
        if self.hovered_card_index == hand_index:
            highlight = draw_rect.inflate(6, 6)
            pygame.draw.rect(self.screen, (255, 255, 255, 100), highlight, 2, border_radius=10)

    def draw_empty_hand_slot(self, rect: pygame.Rect) -> None:
        """Dibuja un espacio vacío en la mano"""
        self.ui.draw_rounded_rect(self.screen, rect, (40, 50, 60), radius=8)
        pygame.draw.rect(self.screen, (80, 90, 100), rect, 2, border_radius=8)
        
        # Signo más para indicar que se puede robar carta
        plus_text = self.fonts['large'].render("+", True, (100, 100, 100))
        self.screen.blit(plus_text, (rect.x + 45, rect.y + 55))

    def get_hand_rects(self) -> List[pygame.Rect]:
        """Calcula los rectángulos para las cartas en mano"""
        max_cards = max(5, len(self.state.player.hand))
        total_width = max_cards * UIConstants.CARD_WIDTH + (max_cards - 1) * UIConstants.CARD_SPACING
        start_x = (config.WINDOW_WIDTH - total_width) // 2
        y = self.areas['hand_area'].y + 45
        
        rects = []
        for i in range(max_cards):
            x = start_x + i * (UIConstants.CARD_WIDTH + UIConstants.CARD_SPACING)
            rects.append(pygame.Rect(x, y, UIConstants.CARD_WIDTH, UIConstants.CARD_HEIGHT))
        
        return rects

    def get_field_rects(self, y: int) -> List[pygame.Rect]:
        """Calcula los rectángulos para los monstruos en campo"""
        total_width = 5 * UIConstants.CARD_WIDTH + 4 * UIConstants.CARD_SPACING
        start_x = (config.WINDOW_WIDTH - total_width) // 2
        
        rects = []
        for i in range(5):
            x = start_x + i * (UIConstants.CARD_WIDTH + UIConstants.CARD_SPACING)
            rects.append(pygame.Rect(x, y, UIConstants.CARD_WIDTH, UIConstants.CARD_HEIGHT))
        
        return rects

    def draw_deck_piles(self) -> None:
        """Dibuja los mazos boca abajo"""
        # Mazo de la IA
        ai_deck_rect = pygame.Rect(50, self.areas['ai_field'].centery - 50, 70, 100)
        self.draw_deck_pile(ai_deck_rect, "Mazo IA", len(self.state.ai.deck), False)
        
        # Mazo del jugador
        player_deck_rect = pygame.Rect(50, self.areas['player_field'].centery - 50, 70, 100)
        self.draw_deck_pile(player_deck_rect, "Tu Mazo", len(self.state.player.deck), True)

    def draw_deck_pile(self, rect: pygame.Rect, name: str, count: int, is_player: bool) -> None:
        """Dibuja un mazo de cartas boca abajo"""
        # Color del mazo
        deck_color = UIStyles.COLORS['ai_dark'] if not is_player else UIStyles.COLORS['player_dark']
        
        # Efecto de apilamiento
        for i in range(3):
            offset_rect = pygame.Rect(rect.x + i * 2, rect.y + i * 2, rect.width, rect.height)
            color_factor = 20 * i
            card_color = (
                min(255, deck_color[0] + color_factor),
                min(255, deck_color[1] + color_factor),
                min(255, deck_color[2] + color_factor)
            )
            
            self.ui.draw_rounded_rect(self.screen, offset_rect, card_color, radius=5)
            pygame.draw.rect(self.screen, (200, 200, 200), offset_rect, 1, border_radius=5)
        
        # Etiqueta
        label = self.fonts['small'].render(name, True, UIStyles.COLORS['text_white'])
        self.screen.blit(label, (rect.x - 5, rect.y - 25))
        
        # Contador
        count_text = self.fonts['normal'].render(str(count), True, UIStyles.COLORS['text_gold'])
        self.screen.blit(count_text, (rect.centerx - 10, rect.centery - 10))

    def draw_action_buttons(self) -> None:
        """Dibuja los botones de acción"""
        button_configs = [
            ('summon', "🟢 INVOCAR", UIStyles.COLORS['btn_summon'], 
             "Invocar 1 carta seleccionada"),
            ('fusion', "🔮 FUSIONAR", UIStyles.COLORS['btn_fusion'],
             "Fusionar 2 cartas seleccionadas"),
            ('attack', "⚔️ ATACAR", UIStyles.COLORS['btn_attack'],
             "Atacar con monstruo seleccionado"),
            ('end_turn', "⏭️ FIN TURNO", UIStyles.COLORS['btn_end'],
             "Terminar turno sin acción"),
        ]
        
        for btn_name, text, color, tooltip in button_configs:
            self.draw_button(self.buttons[btn_name], text, color, tooltip)

    def draw_button(self, rect: pygame.Rect, text: str, base_color: Tuple[int, int, int], 
                    tooltip: str = "") -> None:
        """Dibuja un botón con efectos de hover"""
        # Verificar hover
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        
        # Animación de pulsación
        pulse = 0
        if is_hovered:
            pulse = int(5 * abs(pygame.time.get_ticks() % 800 - 400) / 400)
        
        # Color según hover con brillo
        if is_hovered:
            color = tuple(min(255, c + 60 + pulse) for c in base_color)
            shadow_offset = 2
            text_offset = -1
        else:
            color = base_color
            shadow_offset = 4
            text_offset = 0
        
        # Sombra más pronunciada
        shadow_rect = rect.move(shadow_offset, shadow_offset)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 140), shadow_surf.get_rect(), border_radius=10)
        self.screen.blit(shadow_surf, shadow_rect.topleft)
        
        # Gradiente del botón
        for i in range(rect.height):
            ratio = i / rect.height
            gradient_color = tuple(max(0, min(255, int(color[j] * (1.1 - ratio * 0.3)))) for j in range(3))
            pygame.draw.line(self.screen, gradient_color, (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))
        
        # Brillo superior
        shine_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width - 10, rect.height // 3)
        shine_surf = pygame.Surface((shine_rect.width, shine_rect.height), pygame.SRCALPHA)
        for i in range(shine_rect.height):
            alpha = int(50 * (1 - i / shine_rect.height))
            pygame.draw.line(shine_surf, (255, 255, 255, alpha), (0, i), (shine_rect.width, i))
        self.screen.blit(shine_surf, shine_rect.topleft)
        
        # Borde triple para profundidad
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1, border_radius=10)
        border_color = UIStyles.COLORS['border_gold'] if is_hovered else UIStyles.COLORS['border_silver']
        border_width = 4 if is_hovered else 3
        pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=10)
        
        if is_hovered:
            pygame.draw.rect(self.screen, (255, 255, 255), rect.inflate(-6, -6), 1, border_radius=9)
        
        # Texto del botón con sombra
        button_text = self.fonts['normal'].render(text, True, UIStyles.COLORS['text_white'])
        text_x = rect.x + (rect.width - button_text.get_width()) // 2
        text_y = rect.y + (rect.height - button_text.get_height()) // 2
        
        # Sombra del texto
        shadow_text = self.fonts['normal'].render(text, True, (0, 0, 0))
        self.screen.blit(shadow_text, (text_x + 1, text_y + 1))
        
        # Texto principal
        self.screen.blit(button_text, (text_x, text_y))
        
        # Tooltip si hay hover
        if is_hovered and tooltip:
            self.draw_tooltip_text(rect.centerx, rect.top - 10, tooltip)

    def draw_info_panel(self) -> None:
        """Dibuja el panel de instrucciones"""
        panel = self.areas['info_panel']
        
        # Fondo del panel
        self.draw_panel_background(panel, "📋 INSTRUCCIONES")
        
        # Contenido
        y = panel.y + 45
        instructions = [
            ("1️⃣ SELECCIONAR", UIStyles.COLORS['text_gold']),
            ("• 1 carta → Invocar", UIStyles.COLORS['player_primary']),
            ("• 2 cartas → Fusionar", UIStyles.COLORS['btn_fusion']),
            ("• Monstruo → Atacar", UIStyles.COLORS['ai_primary']),
            ("", (0, 0, 0)),
            ("2️⃣ ACCIÓN", UIStyles.COLORS['text_gold']),
            ("• Presionar botón", UIStyles.COLORS['text_white']),
            ("correspondiente", UIStyles.COLORS['text_white']),
            ("", (0, 0, 0)),
            ("3️⃣ TURNO", UIStyles.COLORS['text_gold']),
            ("• 1 acción por turno", UIStyles.COLORS['text_white']),
            ("• Turno alterna", UIStyles.COLORS['text_white']),
        ]
        
        for text, color in instructions:
            if text:
                txt = self.fonts['small'].render(text, True, color)
                self.screen.blit(txt, (panel.x + 20, y))
            y += 20

    def draw_deck_panel(self) -> None:
        """Dibuja el panel de información de mazos"""
        panel = self.areas['deck_panel']
        
        # Fondo del panel
        self.draw_panel_background(panel, "🎴 MAZOS VISIBLES")
        
        # Contenido
        y = panel.y + 45
        
        # Mazo del jugador
        player_text = self.fonts['normal'].render(f"Tu Mazo: {len(self.state.player.deck)}", 
                                                True, UIStyles.COLORS['player_primary'])
        self.screen.blit(player_text, (panel.x + 20, y))
        y += 25
        
        # Cartas del mazo del jugador
        for i, card_id in enumerate(self.state.player.deck[:4]):
            card = self.state.cards[card_id]
            card_text = self.fonts['small'].render(f"{i+1}. {card.name[:18]}", 
                                                 True, (200, 255, 200))
            self.screen.blit(card_text, (panel.x + 30, y))
            y += 18
        
        y += 10
        
        # Mazo de la IA
        ai_text = self.fonts['normal'].render(f"Mazo IA: {len(self.state.ai.deck)}", 
                                            True, UIStyles.COLORS['ai_primary'])
        self.screen.blit(ai_text, (panel.x + 20, y))
        y += 25
        
        # Cartas del mazo de la IA
        for i, card_id in enumerate(self.state.ai.deck[:4]):
            card = self.state.cards[card_id]
            card_text = self.fonts['small'].render(f"{i+1}. {card.name[:18]}", 
                                                 True, (255, 200, 200))
            self.screen.blit(card_text, (panel.x + 30, y))
            y += 18

    def draw_history_panel(self) -> None:
        """Dibuja el panel de historial de acciones"""
        panel = self.areas['history_panel']
        
        # Fondo del panel
        self.draw_panel_background(panel, "📜 HISTORIAL")
        
        # Contenido
        y = panel.y + 45
        recent_history = self.action_history[-6:]  # Mostrar últimas 6 acciones
        
        for action in recent_history:
            # Color según jugador
            if action.startswith("Jugador"):
                color = UIStyles.COLORS['player_primary']
            elif action.startswith("IA"):
                color = UIStyles.COLORS['ai_primary']
            else:
                color = UIStyles.COLORS['text_gray']
            
            action_text = self.fonts['small'].render(action[:24], True, color)
            self.screen.blit(action_text, (panel.x + 15, y))
            y += 22
        
        # Si no hay historial
        if not recent_history:
            empty_text = self.fonts['small'].render("No hay acciones aún", 
                                                  True, UIStyles.COLORS['text_gray'])
            self.screen.blit(empty_text, (panel.x + 50, panel.y + 80))

    def draw_panel_background(self, panel: pygame.Rect, title: str) -> None:
        """Dibuja el fondo de un panel con título"""
        # Fondo semi-transparente
        alpha_surface = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        alpha_surface.fill((0, 0, 0, 180))
        self.screen.blit(alpha_surface, panel)
        
        # Borde
        pygame.draw.rect(self.screen, UIStyles.COLORS['border_gold'], panel, 3, border_radius=10)
        
        # Título
        title_text = self.fonts['large'].render(title, True, UIStyles.COLORS['text_gold'])
        self.ui.draw_text_with_shadow(title, self.fonts['large'],
                                     panel.x + (panel.width - title_text.get_width()) // 2,
                                     panel.y + 10,
                                     UIStyles.COLORS['text_gold'])

    def draw_messages(self) -> None:
        """Dibuja los mensajes del juego"""
        area = self.areas['message_area']
        
        # Determinar tipo de mensaje y color
        msg_lower = self.message.lower()
        if "✅" in self.message or "fusion" in msg_lower and "disponible" in msg_lower:
            bg_start = (50, 100, 50)
            bg_end = (30, 70, 30)
            border_color = (100, 255, 100)
            icon = "✅"
        elif "❌" in self.message or "imposible" in msg_lower or "no se pueden" in msg_lower:
            bg_start = (100, 40, 40)
            bg_end = (70, 20, 20)
            border_color = (255, 100, 100)
            icon = "❌"
        elif "invoca" in msg_lower:
            bg_start = (40, 80, 120)
            bg_end = (20, 50, 80)
            border_color = (100, 200, 255)
            icon = "🎴"
        elif "ataque" in msg_lower or "atacar" in msg_lower:
            bg_start = (120, 60, 40)
            bg_end = (80, 30, 20)
            border_color = (255, 150, 80)
            icon = "⚔️"
        else:
            bg_start = (40, 50, 70)
            bg_end = (20, 30, 50)
            border_color = (150, 170, 200)
            icon = "💬"
        
        # Área de mensaje expandida
        msg_rect = pygame.Rect(area.x + 10, area.y + 5, area.width - 320, area.height - 10)
        
        # Gradiente de fondo
        for i in range(msg_rect.height):
            ratio = i / msg_rect.height
            color = tuple(int(bg_start[j] * (1 - ratio) + bg_end[j] * ratio) for j in range(3))
            pygame.draw.line(self.screen, color, (msg_rect.x, msg_rect.y + i), (msg_rect.x + msg_rect.width, msg_rect.y + i))
        
        # Brillo en la parte superior
        shine_rect = pygame.Rect(msg_rect.x + 5, msg_rect.y + 3, msg_rect.width - 10, 10)
        shine_surf = pygame.Surface((shine_rect.width, shine_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shine_surf, (255, 255, 255, 40), shine_surf.get_rect(), border_radius=5)
        self.screen.blit(shine_surf, shine_rect.topleft)
        
        # Borde triple
        pygame.draw.rect(self.screen, (0, 0, 0), msg_rect, 1, border_radius=10)
        pygame.draw.rect(self.screen, border_color, msg_rect, 3, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), msg_rect.inflate(-4, -4), 1, border_radius=9)
        
        # Icono con brillo
        icon_text = self.fonts['large'].render(icon, True, border_color)
        icon_shadow = self.fonts['large'].render(icon, True, (0, 0, 0))
        self.screen.blit(icon_shadow, (msg_rect.x + 12, msg_rect.y + 13))
        self.screen.blit(icon_text, (msg_rect.x + 10, msg_rect.y + 11))
        
        # Texto del mensaje con sombra
        msg_display = self.message[:85] + "..." if len(self.message) > 85 else self.message
        self.ui.draw_text_with_shadow(msg_display, self.fonts['normal'], 
                                      msg_rect.x + 45, msg_rect.y + 15, 
                                      (255, 255, 255), shadow_offset=2)
        
        # Feedback de selección actual
        self.draw_selection_feedback()

    def draw_selection_feedback(self) -> None:
        """Dibuja feedback sobre la selección actual"""
        feedback = ""
        color = UIStyles.COLORS['text_gray']
        
        if len(self.selected_hand_indices) == 1:
            card_id = self.state.player.hand[self.selected_hand_indices[0]]
            card = self.state.cards[card_id]
            feedback = f"✅ 1 carta seleccionada: {card.name} - Lista para INVOCAR"
            color = UIStyles.COLORS['player_primary']
        
        elif len(self.selected_hand_indices) == 2:
            idx1, idx2 = sorted(self.selected_hand_indices)
            card1_id = self.state.player.hand[idx1]
            card2_id = self.state.player.hand[idx2]
            card1 = self.state.cards[card1_id]
            card2 = self.state.cards[card2_id]
            
            fusion_key = tuple(sorted((card1_id, card2_id)))
            if fusion_key in self.state.fusions:
                result_id = self.state.fusions[fusion_key]
                result_card = self.state.cards[result_id]
                feedback = f"✨ FUSIÓN DISPONIBLE: {result_card.name} (ATK: {result_card.attack})"
                color = UIStyles.COLORS['btn_fusion']
            else:
                feedback = f"❌ No hay fusión para {card1.name} + {card2.name}"
                color = UIStyles.COLORS['ai_primary']
        
        elif self.selected_attacker_slot is not None:
            card_id = self.state.player.monster_zone[self.selected_attacker_slot]
            card = self.state.cards[card_id]
            feedback = f"🎯 Atacante seleccionado: {card.name} - Elige objetivo o 'Atacar' para ataque directo"
            color = UIStyles.COLORS['text_gold']
        
        if feedback:
            # Dibujar feedback encima del área de mensajes
            fb_area = pygame.Rect(20, self.areas['message_area'].y - 40, 
                                 config.WINDOW_WIDTH - 40, 30)
            
            # Fondo semi-transparente
            alpha_surface = pygame.Surface((fb_area.width, fb_area.height), pygame.SRCALPHA)
            alpha_surface.fill((0, 0, 0, 180))
            self.screen.blit(alpha_surface, fb_area)
            
            # Borde
            pygame.draw.rect(self.screen, color, fb_area, 2, border_radius=6)
            
            # Texto de feedback
            fb_text = self.fonts['small'].render(feedback[:85], True, color)
            self.screen.blit(fb_text, (25, fb_area.y + 8))

    def draw_tooltips(self) -> None:
        """Dibuja tooltips para elementos hover"""
        if self.hovered_card_index is not None:
            self.draw_card_tooltip(self.hovered_card_index)
        
        elif self.hovered_element and self.hovered_element[0] == 'button':
            self.draw_button_tooltip(self.hovered_element[1])

    def draw_card_tooltip(self, card_index: int) -> None:
        """Dibuja tooltip para una carta en mano"""
        card_id = self.state.player.hand[card_index]
        card = self.state.cards[card_id]
        
        # Posición del tooltip (junto al cursor)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tooltip_x = min(mouse_x + 20, config.WINDOW_WIDTH - 250)
        tooltip_y = mouse_y - 20
        
        # Contenido del tooltip
        lines = [
            f"📖 {card.name}",
            f"⚔️ ATK: {card.attack}",
            f"🛡️ DEF: {card.defense}",
            f"✨ Atributo: {card.attribute}",
            f"# En mano: {card_index + 1}"
        ]
        
        self.draw_multi_line_tooltip(tooltip_x, tooltip_y, lines)

    def draw_button_tooltip(self, button_name: str) -> None:
        """Dibuja tooltip para un botón"""
        tooltips = {
            'summon': "Invocar 1 carta seleccionada al campo",
            'fusion': "Fusionar 2 cartas seleccionadas",
            'attack': "Atacar con monstruo seleccionado",
            'end_turn': "Terminar turno sin acción",
        }
        
        if button_name in tooltips:
            rect = self.buttons[button_name]
            self.draw_tooltip_text(rect.centerx, rect.top - 10, tooltips[button_name])

    def draw_tooltip_text(self, x: int, y: int, text: str) -> None:
        """Dibuja un tooltip simple de una línea"""
        text_surface = self.fonts['small'].render(text, True, UIStyles.COLORS['text_white'])
        
        # Dimensiones del tooltip
        padding = 8
        tooltip_width = text_surface.get_width() + 2 * padding
        tooltip_height = text_surface.get_height() + 2 * padding
        
        # Ajustar posición
        tooltip_x = x - tooltip_width // 2
        tooltip_y = y - tooltip_height
        
        # Asegurarse de que no salga de la pantalla
        tooltip_x = max(10, min(tooltip_x, config.WINDOW_WIDTH - tooltip_width - 10))
        
        # Fondo del tooltip
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        self.ui.draw_rounded_rect(self.screen, tooltip_rect, (0, 0, 0, 220), radius=5)
        pygame.draw.rect(self.screen, UIStyles.COLORS['border_gold'], tooltip_rect, 2, border_radius=5)
        
        # Texto
        self.screen.blit(text_surface, (tooltip_x + padding, tooltip_y + padding))

    def draw_multi_line_tooltip(self, x: int, y: int, lines: List[str]) -> None:
        """Dibuja un tooltip con múltiples líneas"""
        if not lines:
            return
        
        # Calcular dimensiones
        line_height = 20
        padding = 10
        max_width = 0
        
        # Calcular ancho máximo
        for line in lines:
            text_surface = self.fonts['small'].render(line, True, (255, 255, 255))
            max_width = max(max_width, text_surface.get_width())
        
        # Dimensiones del tooltip
        tooltip_width = max_width + 2 * padding
        tooltip_height = len(lines) * line_height + 2 * padding
        
        # Ajustar posición para que no salga de la pantalla
        if x + tooltip_width > config.WINDOW_WIDTH:
            x = config.WINDOW_WIDTH - tooltip_width - 10
        if y + tooltip_height > config.WINDOW_HEIGHT:
            y = config.WINDOW_HEIGHT - tooltip_height - 10
        if y < 10:
            y = 10
        
        # Dibujar fondo del tooltip
        tooltip_rect = pygame.Rect(x, y, tooltip_width, tooltip_height)
        self.ui.draw_rounded_rect(self.screen, tooltip_rect, (0, 0, 0, 220), radius=8)
        pygame.draw.rect(self.screen, UIStyles.COLORS['border_gold'], tooltip_rect, 2, border_radius=8)
        
        # Dibujar líneas de texto
        current_y = y + padding
        for line in lines:
            text_surface = self.fonts['small'].render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (x + padding, current_y))
            current_y += line_height

    def draw_effects(self) -> None:
        """Dibuja efectos visuales"""
        if self.active_effect and self.active_effect['type'] == 'fusion':
            self.draw_fusion_effect()

    def draw_fusion_effect(self) -> None:
        """Dibuja un efecto visual para la fusión"""
        effect = self.active_effect
        timer = effect['timer']
        
        # Obtener posición del slot
        field_rects = self.get_field_rects(
            self.areas['ai_field'].y + 30 if effect['is_ai'] else self.areas['player_field'].y + 30
        )
        
        if effect['slot'] < len(field_rects):
            rect = field_rects[effect['slot']]
            center_x, center_y = rect.center
            
            # Círculo brillante que se expande y desvanece
            radius = 60 - timer * 2  # Se contrae con el tiempo
            alpha = 255 * timer // 30  # Se desvanece con el tiempo
            
            if radius > 0 and alpha > 0:
                # Crear superficie para el efecto con alpha
                effect_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                
                # Dibujar círculo brillante
                color = (255, 100, 255, alpha)  # Color magenta brillante
                pygame.draw.circle(effect_surface, color, (radius, radius), radius)
                
                # Dibujar círculo exterior
                pygame.draw.circle(effect_surface, (255, 255, 255, alpha), 
                                 (radius, radius), radius, 3)
                
                # Dibujar en la pantalla principal
                self.screen.blit(effect_surface, (center_x - radius, center_y - radius))

    def draw_game_over_screen(self) -> None:
        """Dibuja la pantalla de fin de juego"""
        # Superficie semi-transparente sobre toda la pantalla
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Determinar mensaje según ganador
        if self.state.winner == "player":
            title = "¡VICTORIA! 🏆"
            color = UIStyles.COLORS['player_primary']
        elif self.state.winner == "ai":
            title = "DERROTA 💀"
            color = UIStyles.COLORS['ai_primary']
        else:
            title = "EMPATE 🤝"
            color = UIStyles.COLORS['text_gold']
        
        # Título principal
        title_text = self.fonts['huge'].render(title, True, color)
        self.ui.draw_text_with_shadow(title, self.fonts['huge'],
                                     config.WINDOW_WIDTH // 2 - title_text.get_width() // 2,
                                     150, color)
        
        # Estadísticas finales
        stats_y = 220
        stats = [
            f"Turnos jugados: {self.state.turn_count}",
            f"LP Jugador: {self.state.player.life_points}",
            f"LP IA: {self.state.ai.life_points}",
            f"Cartas en mazo Jugador: {len(self.state.player.deck)}",
            f"Cartas en mazo IA: {len(self.state.ai.deck)}",
        ]
        
        for stat in stats:
            stat_text = self.fonts['normal'].render(stat, True, UIStyles.COLORS['text_white'])
            self.screen.blit(stat_text, 
                            (config.WINDOW_WIDTH // 2 - stat_text.get_width() // 2, stats_y))
            stats_y += 35
        
        # Botón para reiniciar
        self.draw_button(self.button_restart, "🔄 JUGAR DE NUEVO", UIStyles.COLORS['btn_hover'])
        
        # Instrucción
        inst_text = self.fonts['small'].render("Presiona el botón para comenzar una nueva partida", 
                                              True, UIStyles.COLORS['text_gray'])
        self.screen.blit(inst_text, 
                        (config.WINDOW_WIDTH // 2 - inst_text.get_width() // 2, 380))