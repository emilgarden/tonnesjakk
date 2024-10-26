# src/game/model.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Optional, Tuple, Set
import numpy as np

class PieceType(Enum):
    EMPTY = 0
    BARREL = auto()
    MILK_BUCKET = auto()

@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)
    
    def __sub__(self, other: 'Position') -> 'Position':
        return Position(self.row - other.row, self.col - other.col)

@dataclass
class Piece:
    piece_type: PieceType
    player: int
    position: Position

class GameState:
    def __init__(self, board_size: int = 6):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1
        self.pieces: Dict[int, List[Piece]] = {
            1: [],  # Spiller 1's brikker
            2: []   # Spiller 2's brikker
        }
        self.barrels_remaining = {1: 4, 2: 4}
        self.milk_buckets_remaining = {1: 1, 2: 1}
        self.barrels_passed = {1: 0, 2: 0}
        self.move_history: List[Tuple[Position, Position]] = []
        self.is_jumping = False
        self.current_jump_sequence: List[Position] = []

    def is_valid_position(self, pos: Position) -> bool:
        """Sjekk om en posisjon er innenfor brettet eller gyldig utgangspunkt."""
        # Spesialtilfelle for å gå ut av brettet
        if self.can_exit_board(pos):
            return True
        return 0 <= pos.row < self.board_size and 0 <= pos.col < self.board_size

    def can_exit_board(self, pos: Position) -> bool:
        """Sjekk om en posisjon er gyldig for å gå ut av brettet."""
        piece = self.get_piece_at(Position(pos.row + 1 if pos.row < 0 else pos.row - 1, pos.col))
        if not piece:
            return False
            
        if piece.player == 1:
            return pos.row == -1 and 0 <= pos.col < self.board_size
        else:
            return pos.row == self.board_size and 0 <= pos.col < self.board_size

    def is_forward_move(self, from_pos: Position, to_pos: Position, player: int) -> bool:
        """Sjekk om bevegelsen er fremover for gjeldende spiller."""
        if player == 1:
            return to_pos.row <= from_pos.row
        return to_pos.row >= from_pos.row

    def get_piece_at(self, pos: Position) -> Optional[Piece]:
        """Hent brikke på gitt posisjon hvis den finnes."""
        if not self.is_valid_position(pos):
            return None
        
        for player_pieces in self.pieces.values():
            for piece in player_pieces:
                if piece.position == pos:
                    return piece
        return None

    def place_barrel(self, pos: Position, player: int) -> bool:
        """Plasser en tønne på brettet."""
        if not self.can_place_barrel(pos, player):
            return False

        new_piece = Piece(
            piece_type=PieceType.BARREL,
            player=player,
            position=pos
        )
        
        if self.add_piece(new_piece):
            self.barrels_remaining[player] -= 1
            self._end_turn()  # Avslutt turen etter plassering
            return True
        return False

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        """Utfør et trekk."""
        piece = self.get_piece_at(from_pos)
        if piece is None or to_pos not in self.get_valid_moves(from_pos):
            return False

        # Håndter utgang fra brettet
        if self.can_exit_board(to_pos):
            self.remove_piece(from_pos)
            self.barrels_passed[piece.player] += 1
            self._end_turn()
            return True

        # Utfør normal flytting
        for p in self.pieces[piece.player]:
            if p.position == from_pos:
                p.position = to_pos
                break

        self.move_history.append((from_pos, to_pos))
        self._update_board()

        # Sjekk om dette var et hopp
        if abs(to_pos.row - from_pos.row) == 2 or abs(to_pos.col - from_pos.col) == 2:
            self.is_jumping = True
            self.current_jump_sequence.append(to_pos)
            # Ikke avslutt turen hvis det finnes flere hopp
            if not any(abs(next_pos.row - to_pos.row) == 2 or abs(next_pos.col - to_pos.col) == 2
                      for next_pos in self.get_valid_moves(to_pos)):
                self._end_turn()
        else:
            self._end_turn()

        return True

    def _end_turn(self):
        """Avslutt gjeldende tur."""
        self.is_jumping = False
        self.current_jump_sequence = []
        self.current_player = 3 - self.current_player

    def get_valid_moves(self, pos: Position) -> Set[Position]:
        """Hent alle gyldige trekk for en brikke på gitt posisjon."""
        piece = self.get_piece_at(pos)
        if piece is None or piece.piece_type != PieceType.BARREL:
            return set()

        valid_moves = set()
        
        # Sjekk om brikken kan gå ut av brettet
        if ((piece.player == 1 and pos.row == 0) or 
            (piece.player == 2 and pos.row == self.board_size - 1)):
            exit_pos = Position(-1 if piece.player == 1 else self.board_size, pos.col)
            valid_moves.add(exit_pos)

        directions = [
            Position(-1, -1), Position(-1, 0), Position(-1, 1),
            Position(0, -1),                   Position(0, 1),
            Position(1, -1),  Position(1, 0),  Position(1, 1)
        ]

        # Normal bevegelse (hvis ikke midt i en hoppserie)
        if not self.is_jumping:
            for direction in directions:
                new_pos = Position(pos.row + direction.row, pos.col + direction.col)
                if (self.is_valid_position(new_pos) and 
                    self.get_piece_at(new_pos) is None and
                    self.is_forward_move(pos, new_pos, piece.player)):
                    valid_moves.add(new_pos)

        # Hopp
        for direction in directions:
            middle_pos = Position(pos.row + direction.row, pos.col + direction.col)
            jump_pos = Position(pos.row + 2*direction.row, pos.col + 2*direction.col)
            
            if self.is_valid_position(jump_pos) and self.get_piece_at(jump_pos) is None:
                middle_piece = self.get_piece_at(middle_pos)
                if middle_piece is not None:
                    if (middle_piece.piece_type == PieceType.BARREL or 
                        (middle_piece.piece_type == PieceType.MILK_BUCKET and 
                         middle_piece.player == piece.player)):
                        if self.is_forward_move(pos, jump_pos, piece.player):
                            valid_moves.add(jump_pos)

        return valid_moves

    def is_game_over(self) -> bool:
        """Sjekk om spillet er over."""
        return any(passed == 4 for passed in self.barrels_passed.values())

    def get_winner(self) -> Optional[int]:
        """Returner vinneren hvis spillet er over."""
        if not self.is_game_over():
            return None
        return next(player for player, passed in self.barrels_passed.items() 
                   if passed == 4)
