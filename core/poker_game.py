from core.deck import Deck
from core.game_state import GameState
from core.hand_evaluator import HandEvaluator

class PokerGame:
    SMALL_BLIND = 5
    BIG_BLIND = 10

    def __init__(self, players):
        self.players = players  
        self.deck = Deck()  
        self.game_state = GameState(players)  
        self.deck.shuffle()
        #新增
        self.dealer = players[0]  # 默认第一个玩家是庄家
        self.dealer.is_dealer = True  # 标记庄家

    def start_game(self):
        self.game_state.reset_game_state()
        self.deck = Deck()
        self.deck.shuffle()
        
        self.players[0].reset_hand()
        self.players[1].reset_hand()

        #新增 轮流交换庄家
        self.dealer = self.players[0] if self.players[1].is_dealer else self.players[1]
        self.players[0].is_dealer = self.dealer == self.players[0]
        self.players[1].is_dealer = self.dealer == self.players[1]

        # 设置小盲（SB）和大盲（BB）和下注操作
        sb = self.players[0] if self.players[0].is_dealer else self.players[1]
        bb = self.players[1] if sb == self.players[0] else self.players[0]
        sb.bet(self.BIG_BLIND)
        bb.bet(self.SMALL_BLIND)
        self.game_state.add_to_pot(self.SMALL_BLIND + self.BIG_BLIND)

        print(f'{bb.name}: {bb.chips} ')
        print(f'{sb.name}: {sb.chips} ')
        print(f'-------pot:{self.game_state.pot}-------')

        for player in self.players:
            player.receive_cards(self.deck.draw(2))

        # self.game_state.next_round()
    
    def play_round(self):
        for player in self.players:
            if player.is_active:
                decision = player.make_decision(self.game_state)
                print(f'player{player.name} choose to {decision}')
                if decision == "fold":
                    player.fold()
                    break
                elif decision == "call":
                    print(f'------- before current_bet :{player.current_bet} and chip {player.chips}-------')

                    self.game_state.add_to_pot(player.current_bet)
                    player.bet(player.current_bet)
                    print(f'-------current_bet :{player.current_bet} and chip {player.chips}-------')
                    print(f'-------pot:{self.game_state.pot}-------')
                elif decision == "raise":
                    print(f'-------before current_bet :{player.current_bet} and chip {player.chips}-------')

                    raise_amount = player.current_bet * 2
                    player.bet(raise_amount)
                    self.game_state.add_to_pot(raise_amount)
                    print(f'-------current_bet :{player.current_bet} and chip {player.chips}-------')
                    print(f'-------pot:{self.game_state.pot}-------')


    def next_phase(self):
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) == 1:
            print(f"Player{active_players[0].name} win, all other player fold!")
            self.game_state.current_betting_round = 4
            next_phase_name = "SHOWDOWN"
            return
    
        if self.game_state.current_betting_round == 0:
            self.game_state.deal_community_cards(self.deck, 3)  # Flop
        elif self.game_state.current_betting_round in [1, 2]:
            self.game_state.deal_community_cards(self.deck, 1)  # Turn or River

        if self.game_state.current_betting_round < 3:
            next_phase_name = self.game_state.ROUNDS[self.game_state.current_betting_round + 1]
        else:
            next_phase_name = "SHOWDOWN"
        print(f"Moving to next phase: {next_phase_name}")        

        self.game_state.next_round()
    
    def determine_winner(self):
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) == 1:
            print(f"player {active_players[0].name}:chips {active_players[0].chips}")        
            active_players[0].chips += self.game_state.pot
            return
    
        best_player = None
        best_hand_value = -1

        for player in self.players:
            if player.is_active:
                hand_value = HandEvaluator.evaluate_hand(player.hand, self.game_state.community_cards)
                if hand_value > best_hand_value:
                    best_hand_value = hand_value
                    best_player = player
        
        if best_player:
            best_player.chips += self.game_state.pot  
    
    def reset_game(self):
        self.start_game()
