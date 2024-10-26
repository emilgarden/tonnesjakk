"""
Unit tests for the basic game model functionality.
Testing core functionality like:
- Game state initialization
- Basic piece placement
- Board management
- Simple moves
"""

import unittest
from src.game.model import GameState, Position, PieceType, Piece

class TestGameState(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = GameState()

    def test_initial_state(self):
        """Test that the game initializes with correct values."""
        self.assertEqual(self.game.board_size, 6)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.barrels_remaining[1], 4)
        self.assertEqual(self.game.barrels_remaining[2], 4)
        self.assertEqual(self.game.milk_buckets_remaining[1], 1)
        self.assertEqual(self.game.milk_buckets_remaining[2], 1)

    def test_position_validity(self):
        """Test position validation."""
        valid_pos = Position(0, 0)
        invalid_pos = Position(6, 6)
        
        self.assertTrue(self.game.is_valid_position(valid_pos))
        self.assertFalse(self.game.is_valid_position(invalid_pos))

    def test_piece_placement(self):
        """Test placing pieces on the board."""
        pos = Position(5, 0)
        piece = Piece(PieceType.BARREL, 1, pos)
        
        # Test placing a piece
        self.assertTrue(self.game.add_piece(piece))
        
        # Test getting piece at position
        retrieved_piece = self.game.get_piece_at(pos)
        self.assertIsNotNone(retrieved_piece)
        self.assertEqual(retrieved_piece.piece_type, PieceType.BARREL)
        self.assertEqual(retrieved_piece.player, 1)

    def test_barrel_placement_rules(self):
        """Test rules for placing barrels."""
        # Test valid placement for player 1 (bottom row)
        valid_pos = Position(5, 0)
        self.assertTrue(self.game.can_place_barrel(valid_pos, 1))
        
        # Test invalid placement for player 1 (wrong row)
        invalid_pos = Position(4, 0)
        self.assertFalse(self.game.can_place_barrel(invalid_pos, 1))
        
        # Test valid placement for player 2 (top row)
        valid_pos_p2 = Position(0, 0)
        self.assertTrue(self.game.can_place_barrel(valid_pos_p2, 2))

    def test_milk_bucket_placement(self):
        """Test placing milk buckets."""
        pos = Position(3, 3)
        
        # Test initial placement
        self.assertTrue(self.game.can_place_milk_bucket(pos, 1))
        self.assertTrue(self.game.place_milk_bucket(pos, 1))
        
        # Test placing in occupied position
        self.assertFalse(self.game.can_place_milk_bucket(pos, 2))
        
        # Test placing when no milk buckets remaining
        new_pos = Position(3, 4)
        self.assertFalse(self.game.can_place_milk_bucket(new_pos, 1))

    def test_valid_moves(self):
        """Test valid move calculation."""
        # Place a test piece
        start_pos = Position(5, 0)
        self.game.place_barrel(start_pos, 1)
        
        # Get valid moves
        valid_moves = self.game.get_valid_moves(start_pos)
        
        # Should be able to move one step forward/diagonal
        expected_moves = {Position(4, 0), Position(4, 1)}
        self.assertTrue(expected_moves.issubset(valid_moves))

    def test_movement_execution(self):
        """Test executing moves."""
        # Place a test piece
        from_pos = Position(5, 0)
        to_pos = Position(4, 0)
        
        self.game.place_barrel(from_pos, 1)
        self.assertTrue(self.game.make_move(from_pos, to_pos))
        
        # Verify piece moved
        self.assertIsNone(self.game.get_piece_at(from_pos))
        self.assertIsNotNone(self.game.get_piece_at(to_pos))

if __name__ == '__main__':
    unittest.main()