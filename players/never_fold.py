import random
from core.player import Player

class NeverFold(Player):
    def make_decision(self, game_state):
        return random.choice(["call", "raise"])