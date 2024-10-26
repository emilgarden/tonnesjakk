"""
Unit tests for game rules and mechanics.
Testing specific game rules like:
- Complex jumping sequences
- Milk bucket interaction rules
- Directional movement restrictions
- Win conditions
- Board exit rules
- Turn sequencing
"""
import unittest
from src.game.model import GameState, Position, PieceType, Piece

class TestTonnesjakkRules(unittest.TestCase):
    def setUp(self):
        self.game = GameState()

    def test_jumping_sequence(self):
        """Test at flere hopp er tillatt i ett trekk."""
        # Sett opp en situasjon med mulighet for flere hopp
        self.game.place_barrel(Position(5, 0), 1)  # Startbrikke
        self.game.place_barrel(Position(4, 1), 2)  # Brikke å hoppe over
        self.game.place_barrel(Position(2, 1), 2)  # Enda en brikke å hoppe over

        # Utfør første hopp
        self.assertTrue(self.game.make_move(Position(5, 0), Position(3, 2)))
        # Skulle kunne hoppe igjen fra ny posisjon
        valid_moves = self.game.get_valid_moves(Position(3, 2))
        self.assertIn(Position(1, 0), valid_moves)

    def test_cannot_jump_opponent_milk_bucket(self):
        """Test at man ikke kan hoppe over motstanderens melkespann."""
        # Plasser testbrikker
        self.game.place_barrel(Position(5, 0), 1)
        self.game.place_milk_bucket(Position(4, 1), 2)  # Motstanders melkespann

        valid_moves = self.game.get_valid_moves(Position(5, 0))
        self.assertNotIn(Position(3, 2), valid_moves)  # Skal ikke kunne hoppe over

    def test_can_jump_own_milk_bucket(self):
        """Test at man kan hoppe over eget melkespann."""
        self.game.place_barrel(Position(5, 0), 1)
        self.game.place_milk_bucket(Position(4, 1), 1)  # Eget melkespann

        valid_moves = self.game.get_valid_moves(Position(5, 0))
        self.assertIn(Position(3, 2), valid_moves)  # Skal kunne hoppe over

    def test_directional_movement(self):
        """Test at brikker kun kan bevege seg framover eller sidelengs."""
        self.game.place_barrel(Position(3, 3), 1)
        valid_moves = self.game.get_valid_moves(Position(3, 3))
        
        # For spiller 1 (beveger seg oppover)
        forward_moves = {pos for pos in valid_moves if pos.row < 3}  # Oppover
        backward_moves = {pos for pos in valid_moves if pos.row > 3}  # Nedover
        
        self.assertTrue(len(forward_moves) > 0)  # Skal ha gyldige trekk framover
        self.assertEqual(len(backward_moves), 0)  # Skal ikke kunne gå bakover

    def test_win_condition(self):
        """Test vinnermekanikk."""
        # Simuler at alle brikker er flyttet ut
        self.game.barrels_passed[1] = 4
        
        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winner(), 1)

    def test_exit_board(self):
        """Test at brikker kan forlate brettet på motsatt side."""
        # For spiller 1 (starter nederst)
        self.game.place_barrel(Position(0, 0), 1)  # Brikke på øverste rad
        valid_moves = self.game.get_valid_moves(Position(0, 0))
        self.assertIn(Position(-1, 0), valid_moves)  # Skal kunne gå ut av brettet

        # For spiller 2 (starter øverst)
        self.game.current_player = 2
        self.game.place_barrel(Position(5, 0), 2)  # Brikke på nederste rad
        valid_moves = self.game.get_valid_moves(Position(5, 0))
        self.assertIn(Position(6, 0), valid_moves)  # Skal kunne gå ut av brettet

    def test_turn_sequence(self):
        """Test at spiller-turer alternerer korrekt."""
        initial_player = self.game.current_player
        
        # Utfør et trekk
        self.game.place_barrel(Position(5, 0), initial_player)
        self.assertEqual(self.game.current_player, 3 - initial_player)  # Skal bytte til andre spiller

        # Utfør neste trekk
        self.game.place_barrel(Position(0, 0), self.game.current_player)
        self.assertEqual(self.game.current_player, initial_player)  # Tilbake til første spiller

if __name__ == '__main__':
    unittest.main()