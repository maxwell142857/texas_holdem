class Card:
    SUITS = ['♠', '♥', '♦', '♣'] 
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    def __init__(self,suit,rank):
        if suit not in self.SUITS:
            raise ValueError(f'invalid suit{suit}')
        if rank not in self.RANKS:
            raise ValueError(f'invalid rank{rank}')
        
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.suit}{self.rank}'
        
    def __lt__(self,other):
        if not isinstance(other,Card):
            raise NotImplementedError('less than error')
        return self.RANKS.index(self.rank) < self.RANKS.index(other.rank)