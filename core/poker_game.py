from core.deck import Deck
from core.game_state import GameState
from core.hand_evaluator import HandEvaluator

class PokerGame:
    def __init__(self, players):
        self.players = players  
        self.deck = Deck()  
        self.game_state = GameState(players)  
        self.deck.shuffle()  
    
    def start_game(self):
        self.game_state.reset_game_state()
        self.deck = Deck()  
        self.deck.shuffle()

        for player in self.players:
            player.receive_cards(self.deck.draw(2))
        
        self.game_state.next_round()
    
    def play_round(self):
        for player in self.players:
            if player.is_active:
                decision = player.make_decision(self.game_state)
                print(f'player{player.name} choose to {decision}')
                if decision == "fold":
                    player.fold()
                elif decision == "call":
                    self.game_state.add_to_pot(player.current_bet)
                elif decision == "raise":
                    raise_amount = player.current_bet * 2 
                    self.game_state.add_to_pot(raise_amount)
    
    def next_phase(self):
        if self.game_state.current_betting_round == 0:
            self.game_state.deal_community_cards(self.deck, 3)  # Flop
        elif self.game_state.current_betting_round in [1, 2]:
            self.game_state.deal_community_cards(self.deck, 1)  # Turn or River
        self.game_state.next_round()
    
    def determine_winner(self):
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
