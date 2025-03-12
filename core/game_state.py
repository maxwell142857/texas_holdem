from core.deck import Deck

class GameState:
    ROUNDS = ["Preflop", "Flop", "Turn", "River"]
    
    def __init__(self, players):
        self.players = players  
        self.community_cards = []  
        self.pot = 0  
        self.current_betting_round = 0  # 0=Preflop, 1=Flop(3), 2=Turn(4), 3=River(5)
        self.dealer_position = 0  
    
    def add_to_pot(self, amount):
        self.pot += amount
    
    def deal_community_cards(self, deck, num_cards):
        self.community_cards.extend(deck.draw(num_cards))
    
    def next_round(self):
        if self.current_betting_round < 4:
            self.current_betting_round += 1
        else:
            raise ValueError("Game has already reached the final round")
    
    def reset_game_state(self):
        self.community_cards = []
        self.pot = 0
        self.current_betting_round = 0
        self.dealer_position = (self.dealer_position + 1) % len(self.players)  