from core.poker_game import PokerGame
from core.player import Player
from collections import defaultdict

from players.never_fold import NeverFold
from players.rule_based import RuleBased
from players.monteCarlo import MonteCarlo
from players.mcts_player import MCTSPlayer

def fight_to_the_last_chip(players):
    game = PokerGame(players)
    total = 0
    hand_win_counter = defaultdict(int)  # 新增：记录每人赢了几局

    while True:
        total += 1
        game.start_game()

        while game.game_state.current_betting_round < 4:
            game.play_round()
            if game.game_state.current_betting_round < 4:
                game.next_phase() 
    
        winner = game.determine_winner()
        hand_win_counter[winner] += 1
        print(f"{players[0].name}:{players[0].chips}    {players[1].name}:{players[1].chips}   pot: {game.game_state.pot} ")

        if players[0].chips < 0:
            print(f'total round is {total}')
            print(f"Final Hand Wins: {hand_win_counter}")
            return players[1].name
        elif players[1].chips < 0:
            print(f'total round is {total}')
            print(f"Final Hand Wins: {hand_win_counter}")
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
    for i in range(round):
        Alice = MonteCarlo(name='Alice', chips=2000)
        # NeverFold RuleBased MonteCarlo MCTSPlayer

        Bob =MCTSPlayer(name='Bob', chips=2000)
        name2cnt[fight_to_the_last_chip([Alice,Bob])] += 1
        # name2cnt[oneRound([Alice,Bob])] += 1
        # name2cnt[oneRound([Bob,Alice])] += 1
        print("round: "+str(i+1))
        
    return name2cnt

def evaluate1(rounds):
    name2cnt = defaultdict(int)
    for i in range(rounds):
        Alice = RuleBased(name='Alice', chips=1000)
        Bob = MCTSPlayer(name='Bob', chips=1000)
        winner = fight_to_the_last_chip([Alice, Bob])
        # winner = oneRound([Alice,Bob])
        # name2cnt[winner] += 1
        # winner = oneRound([Bob,Alice])
        name2cnt[winner] += 1
        print(f"Round {i+1} winner: {winner}")
    return name2cnt

if __name__ == "__main__":

    print(evaluate1(1))
    