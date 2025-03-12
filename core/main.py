from core.poker_game import PokerGame
from core.player import Player

def main():
    players = [Player(name=1, chips=1000), Player(name=2, chips=1000)]
    
    game = PokerGame(players)
    game.start_game()
    
    while game.game_state.current_betting_round < 3:
        print(f"=== current state: {game.game_state.ROUNDS[game.game_state.current_betting_round]} ===")
        
        game.play_round()
        if game.game_state.current_betting_round < 3:
            game.next_phase()
    
    game.determine_winner()

    print(f"winner is Player {max(players, key=lambda p: p.chips).name}，筹码数：{max(players, key=lambda p: p.chips).chips}")

if __name__ == "__main__":
    main()
