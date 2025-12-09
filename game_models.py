import json
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

import config


@dataclass
class Card:
    id: int
    name: str
    attack: int
    defense: int
    level: int
    attribute: str
    type: str

    def __str__(self) -> str:
        return f"{self.name} (ATK {self.attack}, DEF {self.defense})"


@dataclass
class FusionRule:
    ingredients: Tuple[int, int]
    result: int


@dataclass
class PlayerState:
    name: str
    life_points: int = config.STARTING_LP
    deck: List[int] = field(default_factory=list)   # ids de cartas
    hand: List[int] = field(default_factory=list)
    # ANTES se llamaba 'field', eso causaba el conflicto con dataclasses.field
    monster_zone: List[Optional[int]] = field(default_factory=lambda: [None] * config.MAX_MONSTERS)
    graveyard: List[int] = field(default_factory=list)

    def clone(self) -> "PlayerState":
        return PlayerState(
            name=self.name,
            life_points=self.life_points,
            deck=list(self.deck),
            hand=list(self.hand),
            monster_zone=list(self.monster_zone),
            graveyard=list(self.graveyard),
        )


@dataclass
class Move:
    # Tipos de jugada muy simplificados:
    # - "summon": invocar un monstruo desde la mano
    # - "attack": un monstruo ataca a otro o directo
    # - "fusion": fusionar dos cartas de la mano
    kind: str
    params: dict


@dataclass
class GameState:
    cards: Dict[int, Card]
    fusions: Dict[Tuple[int, int], int]
    player: PlayerState
    ai: PlayerState
    current_turn: str = "player"  # "player" o "ai"
    finished: bool = False
    winner: Optional[str] = None  # "player", "ai", "draw" o None

    def clone(self) -> "GameState":
        return GameState(
            cards=self.cards,
            fusions=self.fusions,
            player=self.player.clone(),
            ai=self.ai.clone(),
            current_turn=self.current_turn,
            finished=self.finished,
            winner=self.winner,
        )

    # ---------------------------
    # Utilidades
    # ---------------------------

    def get_active_player(self) -> PlayerState:
        return self.player if self.current_turn == "player" else self.ai

    def get_opponent(self) -> PlayerState:
        return self.ai if self.current_turn == "player" else self.player

    def switch_turn(self) -> None:
        self.current_turn = "ai" if self.current_turn == "player" else "player"

    # ---------------------------
    # Reglas básicas
    # ---------------------------

    def draw_card(self, player: Optional[PlayerState] = None) -> None:
        if player is None:
            player = self.get_active_player()
        if player.deck:
            card_id = player.deck.pop(0)
            player.hand.append(card_id)

    def initial_draw(self) -> None:
        # Roba la mano inicial
        for _ in range(config.HAND_SIZE):
            self.draw_card(self.player)
            self.draw_card(self.ai)

    def check_game_over(self) -> None:
        if self.player.life_points <= 0 and self.ai.life_points <= 0:
            self.finished = True
            self.winner = "draw"
        elif self.player.life_points <= 0:
            self.finished = True
            self.winner = "ai"
        elif self.ai.life_points <= 0:
            self.finished = True
            self.winner = "player"

    # ---------------------------
    # Generación de jugadas
    # ---------------------------

    def valid_moves(self) -> List[Move]:
        """Genera jugadas simples: invocar un monstruo, o atacar con uno que ya esté en campo."""
        if self.finished:
            return []

        moves: List[Move] = []
        current = self.get_active_player()
        opponent = self.get_opponent()

        # Invocar desde la mano a la primera casilla libre
        free_slots = [i for i, c in enumerate(current.monster_zone) if c is None]
        if free_slots:
            for idx, card_id in enumerate(current.hand):
                moves.append(Move(kind="summon", params={"hand_index": idx, "slot_index": free_slots[0]}))

        # Intentar fusiones (dos cartas de la mano)
        if len(current.hand) >= 2:
            for i in range(len(current.hand)):
                for j in range(i + 1, len(current.hand)):
                    c1, c2 = current.hand[i], current.hand[j]
                    key = tuple(sorted((c1, c2)))
                    if key in self.fusions and free_slots:
                        moves.append(Move(kind="fusion", params={
                            "hand_index_1": i,
                            "hand_index_2": j,
                            "slot_index": free_slots[0]
                        }))

        # Atacar con cualquier monstruo que esté en campo
        attacker_slots = [i for i, cid in enumerate(current.monster_zone) if cid is not None]
        opponent_slots = [i for i, cid in enumerate(opponent.monster_zone) if cid is not None]

        for a in attacker_slots:
            if opponent_slots:
                for d in opponent_slots:
                    moves.append(Move(kind="attack", params={"attacker_slot": a, "defender_slot": d}))
            else:
                # Ataque directo
                moves.append(Move(kind="attack", params={"attacker_slot": a, "defender_slot": None}))

        return moves

    # ---------------------------
    # Aplicar jugadas
    # ---------------------------

    def apply_move(self, move: Move) -> None:
        if self.finished:
            return

        current = self.get_active_player()
        opponent = self.get_opponent()

        if move.kind == "summon":
            h_idx = move.params["hand_index"]
            s_idx = move.params["slot_index"]
            if 0 <= h_idx < len(current.hand) and current.monster_zone[s_idx] is None:
                card_id = current.hand.pop(h_idx)
                current.monster_zone[s_idx] = card_id

        elif move.kind == "fusion":
            h1 = move.params["hand_index_1"]
            h2 = move.params["hand_index_2"]
            s_idx = move.params["slot_index"]
            if h1 == h2:
                return

            i1, i2 = sorted((h1, h2))
            if i2 >= len(current.hand):
                return

            c1 = current.hand[i1]
            c2 = current.hand[i2]
            key = tuple(sorted((c1, c2)))
            if key not in self.fusions:
                return

            result_id = self.fusions[key]

            # Quitar las cartas de la mano (cuidado con índices)
            current.graveyard.append(current.hand.pop(i2))
            current.graveyard.append(current.hand.pop(i1))

            if current.monster_zone[s_idx] is None:
                current.monster_zone[s_idx] = result_id

        elif move.kind == "attack":
            a_slot = move.params["attacker_slot"]
            d_slot = move.params.get("defender_slot", None)

            if not (0 <= a_slot < len(current.monster_zone)):
                return

            attacker_id = current.monster_zone[a_slot]
            if attacker_id is None:
                return

            attacker_card = self.cards[attacker_id]

            if d_slot is None:
                # Ataque directo
                opponent.life_points -= attacker_card.attack
                self.check_game_over()
            else:
                if not (0 <= d_slot < len(opponent.monster_zone)):
                    return
                defender_id = opponent.monster_zone[d_slot]
                if defender_id is None:
                    return
                defender_card = self.cards[defender_id]

                if attacker_card.attack > defender_card.attack:
                    damage = attacker_card.attack - defender_card.attack
                    opponent.life_points -= damage
                    opponent.graveyard.append(defender_id)
                    opponent.monster_zone[d_slot] = None
                elif attacker_card.attack < defender_card.attack:
                    damage = defender_card.attack - attacker_card.attack
                    current.life_points -= damage
                    current.graveyard.append(attacker_id)
                    current.monster_zone[a_slot] = None
                else:
                    # se destruyen ambos
                    opponent.graveyard.append(defender_id)
                    current.graveyard.append(attacker_id)
                    opponent.monster_zone[d_slot] = None
                    current.monster_zone[a_slot] = None

                self.check_game_over()

        # Al final del turno, cambia turno
        self.switch_turn()
        # Robar carta al nuevo jugador activo
        self.draw_card(self.get_active_player())
        self.check_game_over()


# ====================================================
# Funciones para cargar cartas / fusiones y crear un estado inicial
# ====================================================

def load_cards(path: str) -> Dict[int, Card]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cards: Dict[int, Card] = {}
    for c in data["cards"]:
        cards[c["id"]] = Card(**c)
    return cards


def load_fusions(path: str) -> Dict[Tuple[int, int], int]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    fus: Dict[Tuple[int, int], int] = {}
    for rule in data["fusions"]:
        ing = tuple(sorted((rule["ingredients"][0], rule["ingredients"][1])))
        fus[ing] = rule["result"]
    return fus


def build_random_deck(card_ids: List[int], size: int) -> List[int]:
    """
    Construye un mazo aleatorio.

    - Si size <= número de cartas distintas: usa cartas SIN repetir (más variedad).
    - Si size > número de cartas distintas: permite repeticiones para rellenar.
    """
    if size <= len(card_ids):
        # sin repetición
        return random.sample(card_ids, size)
    else:
        deck: List[int] = []
        while len(deck) < size:
            faltan = size - len(deck)
            bloque = random.sample(card_ids, min(len(card_ids), faltan))
            deck.extend(bloque)
        return deck



def create_initial_game_state() -> GameState:
    cards = load_cards(config.CARDS_FILE)
    fusions = load_fusions(config.FUSIONS_FILE)
    all_ids = list(cards.keys())

    player_deck = build_random_deck(all_ids, config.DECK_SIZE)
    ai_deck = build_random_deck(all_ids, config.DECK_SIZE)

    random.shuffle(player_deck)
    random.shuffle(ai_deck)

    player = PlayerState(name="Jugador", deck=player_deck)
    ai = PlayerState(name="IA", deck=ai_deck)

    state = GameState(cards=cards, fusions=fusions, player=player, ai=ai)
    state.initial_draw()
    return state
