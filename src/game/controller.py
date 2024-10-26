# src/game/controller.py
from typing import Optional, List
from .model import GameState, Position, PieceType
from dataclasses import dataclass

@dataclass
class GameAction:
    action_type: str  # 'place_barrel', 'place_milk_bucket', 'move'
    player: int
    positions: List[Position]
    success: bool
    message: str

class GameController:
    def __init__(self):
        self.game_state = GameState()
        self.current_move_sequence: List[Position] = []
        self.is_jumping = False

    def handle_action(self, action_type: str, player: int, 
                     positions: List[Position]) -> GameAction:
        """Håndter en spillehandling."""
        if player != self.game_state.current_player:
            return GameAction(action_type, player, positions, False, 
                            "Ikke din tur")

        if action_type == "place_barrel":
            success = self.game_state.place_barrel(positions[0], player)
            message = "Tønne plassert" if success else "Ugyldig plassering"
            
        elif action_type == "place_milk_bucket":
            success = self.game_state.place_milk_bucket(positions[0], player)
            message = "Melkespann plassert" if success else "Ugyldig plassering"
            
        elif action_type == "move":
            success = self._handle_move(positions[0], positions[1])
            message = "Trekk utført" if success else "Ugyldig trekk"
            
        else:
            return GameAction(action_type, player, positions, False, 
                            "Ugyldig handling")

        if success and not self.is_jumping:
            self._end_turn()

        return GameAction(action_type, player, positions, success, message)

    def _handle_move(self, from_pos: Position, to_pos: Position) -> bool:
        """Håndter et trekk."""
        # Hvis vi er midt i en hoppserie
        if self.is_jumping and from_pos != self.current_move_sequence[-1]:
            return False

        # Sjekk om trekket er gyldig
        if not self.game_state.make_move(from_pos, to_pos):
            return False

        # Oppdater movesekvensen
        if not self.current_move_sequence:
            self.current_move_sequence = [from_pos, to_pos]
        else:
            self.current_move_sequence.append(to_pos)

        # Sjekk om dette var et hopp
        if abs(to_pos.row - from_pos.row) == 2 or abs(to_pos.col - from_pos.col) == 2:
            next_jumps = self._get_valid_jumps(to_pos)
            if next_jumps:
                self.is_jumping = True
                return True

        self.is_jumping = False
        return True

    def _get_valid_jumps(self, pos: Position) -> List[Position]:
        """Hent gyldige hopp fra en posisjon."""
        valid_moves = self.game_state.get_valid_moves(pos)
        return [move for move in valid_moves 
                if abs(move.row - pos.row) == 2 or abs(move.col - pos.col) == 2]

    def _end_turn(self):
        """Avslutt gjeldende tur."""
        self.current_move_sequence = []
        self.is_jumping = False
        self.game_state.current_player = 3 - self.game_state.current_player

    def get_valid_moves(self, pos: Position) -> List[Position]:
        """Hent gyldige trekk for en posisjon."""
        if self.is_jumping:
            return self._get_valid_jumps(pos)
        return list(self.game_state.get_valid_moves(pos))

    def get_game_status(self) -> dict:
        """Hent spillets nåværende status."""
        return {
            "current_player": self.game_state.current_player,
            "barrels_remaining": self.game_state.barrels_remaining.copy(),
            "milk_buckets_remaining": self.game_state.milk_buckets_remaining.copy(),
            "barrels_passed": self.game_state.barrels_passed.copy(),
            "is_jumping": self.is_jumping,
            "current_sequence": self.current_move_sequence.copy(),
            "is_game_over": self.game_state.is_game_over(),
            "winner": self.game_state.get_winner()
        }