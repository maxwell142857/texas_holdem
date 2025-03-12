from core.poker_game import PokerGame
from core.player import Player

def main():
    players = [Player(name=1, chips=1000), Player(name=2, chips=1000)]
    
    game = PokerGame(players)
    game.start_game()

    while game.game_state.current_betting_round < 4:
        print(f"=== current state: {game.game_state.ROUNDS[game.game_state.current_betting_round]} ===")

        for player in players:
            hand_str = ", ".join(str(card) for card in player.hand)
            print(f"Player {player.name} card: {hand_str} (Chipsc {player.chips})")
        community_cards_str = ", ".join(str(card) for card in game.game_state.community_cards)
        print(f"Community Cards: {community_cards_str if community_cards_str else 'None'}")

        game.play_round()

        if game.game_state.current_betting_round < 4:
            game.next_phase()
    
    game.determine_winner()

    # print(f"winner is Player {max(players, key=lambda p: p.chips).name}，chips：{max(players, key=lambda p: p.chips).chips}")

    # winner = max(players, key=lambda p: p.chips)
    # loser = min(players, key=lambda p: p.chips)

    for player in players:
        print(f"Player {player.name}，chips：{player.chips}")


    # print(f"Winner is Player {winner.name}，chips：{winner.chips}")
    # print(f"Loser is Player {loser.name}，chip：{loser.chips}")


if __name__ == "__main__":
    main()
