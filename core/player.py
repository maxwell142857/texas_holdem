import random
class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.is_active = True

    def receive_cards(self, cards):
        self.hand = cards

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("chip is not enough")
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.is_active = False

    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.is_active = True
        
    def make_decision(self, game_state):
        return random.choice(["call", "raise", "fold"])