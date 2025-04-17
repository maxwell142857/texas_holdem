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
        # Alice = RuleBased(name='Alice', chips=2000)
        Alice = MonteCarlo(name='Alice', chips=2000)
        # Bob = MonteCarlo(name='Bob', chips=1000)
        Bob = MCTSPlayer(name='Bob', chips=2000)
        name2cnt[fight_to_the_last_chip([Alice,Bob])] += 1
        # name2cnt[oneRound([Alice,Bob])] += 1
        # name2cnt[oneRound([Bob,Alice])] += 1
        print("round: "+round);
    return name2cnt


def fight_with_timeout(players, max_rounds=2000):
    game = PokerGame(players)
    for round_num in range(max_rounds):
        game.start_game()

        while game.game_state.current_betting_round < 4:
            game.play_round()
            if game.game_state.current_betting_round < 4:
                game.next_phase() 
    
        game.determine_winner()

        if players[0].chips < 0:
            return players[1].name
        elif players[1].chips < 0:
            return players[0].name

    # 如果超过 max_rounds 仍无人输光
    print(f"Timeout reached after {max_rounds} rounds.")
    print(f"{players[0].name}: {players[0].chips} chips")
    print(f"{players[1].name}: {players[1].chips} chips")
    return players[0].name if players[0].chips > players[1].chips else players[1].name

def new_evaluate(round):
    name2cnt = defaultdict(int)
    for _ in range(round):
        Alice = MonteCarlo(name='Alice', chips=2000)
        Bob = MCTSPlayer(name='Bob', chips=2000)
        name2cnt[fight_with_timeout([Alice, Bob], max_rounds=2000)] += 1
    return name2cnt


def simulate_battles(rounds=10000):
    win_count = defaultdict(int)
    
    for _ in range(rounds):
        Alice = MonteCarlo(name='Alice', chips=2000)
        Bob = MCTSPlayer(name='Bob', chips=2000)
        winner = fight_with_timeout([Alice, Bob], max_rounds=2000)
        win_count[winner] += 1

    total = sum(win_count.values())
    print(f"Total rounds: {total}")
    for player in ['Alice', 'Bob']:
        wins = win_count[player]
        win_rate = wins / total * 100
        print(f"{player} wins: {wins} ({win_rate:.2f}%)")


if __name__ == "__main__":
    simulate_battles(rounds=10000)

    # print(new_evaluate(100))
    
