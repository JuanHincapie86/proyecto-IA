from typing import Tuple, Optional

import config
from game_models import GameState, Move


def evaluate_state(state: GameState) -> int:
    """Función de evaluación muy simple:
    Ventaja en LP + suma de ATK en el campo.
    Positivo favorece a la IA, negativo favorece al jugador.
    """
    ai = state.ai
    pl = state.player

    # OJO: ahora usamos monster_zone en lugar de field
    ai_field_attack = sum(state.cards[cid].attack for cid in ai.monster_zone if cid is not None)
    pl_field_attack = sum(state.cards[cid].attack for cid in pl.monster_zone if cid is not None)

    score = (ai.life_points - pl.life_points) + (ai_field_attack - pl_field_attack)
    return score


def minimax(state: GameState, depth: int, maximizing_for: str) -> Tuple[int, Optional[Move]]:
    """Minimax sin poda alfa-beta para simplificar.
    maximizing_for: "ai" o "player" (quién queremos que gane).
    """
    if depth == 0 or state.finished:
        score = evaluate_state(state)
        # Si estamos maximizando para la IA, score tal cual.
        # Si maximizamos para el jugador, invertimos el signo.
        return (score if maximizing_for == "ai" else -score), None

    moves = state.valid_moves()
    if not moves:
        score = evaluate_state(state)
        return (score if maximizing_for == "ai" else -score), None

    # Nodo MAX si es turno del que maximizamos; MIN si es del otro
    if ((state.current_turn == "ai" and maximizing_for == "ai") or
            (state.current_turn == "player" and maximizing_for == "player")):
        # MAX
        best_value = float("-inf")
        best_move: Optional[Move] = None
        for m in moves:
            next_state = state.clone()
            next_state.apply_move(m)
            value, _ = minimax(next_state, depth - 1, maximizing_for)
            if value > best_value:
                best_value = value
                best_move = m
        return best_value, best_move
    else:
        # MIN
        best_value = float("inf")
        best_move: Optional[Move] = None
        for m in moves:
            next_state = state.clone()
            next_state.apply_move(m)
            value, _ = minimax(next_state, depth - 1, maximizing_for)
            if value < best_value:
                best_value = value
                best_move = m
        return best_value, best_move


def choose_ai_move(state: GameState) -> Optional[Move]:
    """Elige la mejor jugada para la IA usando Minimax."""
    _, move = minimax(state, config.MINIMAX_DEPTH, maximizing_for="ai")
    return move
