# src/game/main.py
from .controller import GameController
from .view import ConsoleView

def main():
    controller = GameController()
    view = ConsoleView(controller)
    
    print("Velkommen til Tønnesjakk!")
    
    while True:
        view.display_board()
        view.display_game_status()
        
        status = controller.get_game_status()
        if status["is_game_over"]:
            winner = status["winner"]
            print(f"\nSpillet er over! Spiller {winner} har vunnet!")
            break
            
        action = view.get_action()
        if action is None:
            if input("\nVil du avslutte spillet? (j/n): ").lower() == 'j':
                break
            continue
            
        result = controller.handle_action(
            action.action_type, 
            action.player, 
            action.positions
        )
        
        if not result.success:
            view.display_message(result.message)

if __name__ == "__main__":
    main()