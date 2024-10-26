# src/game/view.py
from typing import List, Optional
from .model import Position, PieceType, GameState
from .controller import GameController, GameAction

class ConsoleView:
    def __init__(self, controller: GameController):
        self.controller = controller

    def display_board(self):
        """Vis spillbrettet."""
        board = self.controller.game_state.board
        print("\n   0 1 2 3 4 5")  # Kolonneindekser
        print("  " + "-" * 13)
        for row in range(len(board)):
            print(f"{row}|", end=" ")
            for val in board[row]:
                if val == 0:
                    print("·", end=" ")
                elif val == 1:
                    print("T₁", end=" ")
                elif val == 2:
                    print("M₁", end=" ")
                elif val == 3:
                    print("T₂", end=" ")
                elif val == 4:
                    print("M₂", end=" ")
            print("|")
        print("  " + "-" * 13)

    def display_game_status(self):
        """Vis spillstatus."""
        status = self.controller.get_game_status()
        player = status["current_player"]
        print(f"\nSpiller {player} sin tur")
        print(f"Gjenværende tønner: P1: {status['barrels_remaining'][1]}, "
              f"P2: {status['barrels_remaining'][2]}")
        print(f"Gjenværende melkespann: P1: {status['milk_buckets_remaining'][1]}, "
              f"P2: {status['milk_buckets_remaining'][2]}")
        
        if status["is_jumping"]:
            print("\nMidt i en hoppserie! Må fullføre eller avslutte trekket.")
            
    def display_message(self, message: str):
        """Vis en melding til spilleren."""
        print(f"\n>>> {message}")

    def get_action(self) -> Optional[GameAction]:
        """Hent spillerens neste handling."""
        status = self.controller.get_game_status()
        player = status["current_player"]
        
        if status["is_jumping"]:
            return self._handle_jumping_move(player)
            
        while True:
            print("\nVelg handling:")
            print("1. Plasser tønne")
            print("2. Plasser melkespann")
            print("3. Flytt brikke")
            print("4. Vis brett")
            print("5. Avslutt")
            
            choice = input("Valg (1-5): ").strip()
            
            if choice == "1":
                return self._handle_barrel_placement(player)
            elif choice == "2":
                return self._handle_milk_bucket_placement(player)
            elif choice == "3":
                return self._handle_move(player)
            elif choice == "4":
                self.display_board()
                self.display_game_status()
            elif choice == "5":
                return None
            else:
                print("Ugyldig valg, prøv igjen.")

    def _get_position(self, prompt: str) -> Optional[Position]:
        """Hjelper for å få en posisjon fra bruker."""
        try:
            row, col = map(int, input(f"{prompt} (rad,kolonne): ").split(","))
            return Position(row, col)
        except (ValueError, IndexError):
            print("Ugyldig posisjon format. Bruk: rad,kolonne (f.eks. 0,1)")
            return None

    def _handle_barrel_placement(self, player: int) -> Optional[GameAction]:
        """Håndter plassering av tønne."""
        pos = self._get_position("Hvor vil du plassere tønnen?")
        if pos is None:
            return None
        return GameAction("place_barrel", player, [pos], True, "")

    def _handle_milk_bucket_placement(self, player: int) -> Optional[GameAction]:
        """Håndter plassering av melkespann."""
        pos = self._get_position("Hvor vil du plassere melkespannet?")
        if pos is None:
            return None
        return GameAction("place_milk_bucket", player, [pos], True, "")

    def _handle_move(self, player: int) -> Optional[GameAction]:
        """Håndter flytting av brikke."""
        from_pos = self._get_position("Fra posisjon")
        if from_pos is None:
            return None
            
        to_pos = self._get_position("Til posisjon")
        if to_pos is None:
            return None
            
        return GameAction("move", player, [from_pos, to_pos], True, "")

    def _handle_jumping_move(self, player: int) -> Optional[GameAction]:
        """Håndter hopp når man er midt i en hoppserie."""
        print("\nDu er midt i en hoppserie!")
        print("1. Fortsett å hoppe")
        print("2. Avslutt trekket")
        
        choice = input("Valg (1-2): ").strip()
        
        if choice == "1":
            to_pos = self._get_position("Til posisjon")
            if to_pos is None:
                return None
            current_pos = self.controller.current_move_sequence[-1]
            return GameAction("move", player, [current_pos, to_pos], True, "")
        elif choice == "2":
            self.controller.is_jumping = False
            self.controller._end_turn()
            return None
        
        return None