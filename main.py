from core.poker_game import PokerGame
from core.player import Player
from collections import defaultdict

from players.never_fold import NeverFold
from players.rule_based import RuleBased
from players.monteCarlo import MonteCarlo

def fight_to_the_last_chip(players):
    game = PokerGame(players)
    total = 0
    while True:
        total += 1
        game.start_game()

        while game.game_state.current_betting_round < 4:
            game.play_round()
            if game.game_state.current_betting_round < 4:
                game.next_phase() 
    
        game.determine_winner()
        print(f"{players[0].name}:{players[0].chips}    {players[1].name}:{players[1].chips}")

        if players[0].chips < 0:
            print(f'total round is {total}')
            return players[1].name
        elif players[1].chips < 0:
            print(f'total round is {total}')
            return players[0].name
        
def oneRound(players):
    game = PokerGame(players)
    game.start_game()
    while game.game_state.current_betting_round < 4:
        game.play_round()
        if game.game_state.current_betting_round < 4:
            game.next_phase() 
    
    return game.determine_winner()
    
def evaluate(round):
    name2cnt = defaultdict(int)
    for _ in range(round):
        Alice = RuleBased(name='Alice', chips=5000)
        Bob = MonteCarlo(name='Bob', chips=5000)
        name2cnt[fight_to_the_last_chip([Alice,Bob])] += 1
        # name2cnt[oneRound([Alice,Bob])] += 1
        # name2cnt[oneRound([Bob,Alice])] += 1
    return name2cnt

if __name__ == "__main__":
    
    print(evaluate(100))
    
