import random
from core.card import Card

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit,rank))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self, n=1):
        if n > len(self.cards):
            n = len(self.cards)
        drawn_cards = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn_cards
    
    def is_empty(self):
        return len(self.cards) == 0
    
    def reset(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()
    
    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
