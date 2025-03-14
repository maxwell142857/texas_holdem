import random
from core.hand_evaluator import HandEvaluator
from core.player import Player

class RuleBased(Player):
    def make_decision(self, game_state):
        if game_state.current_betting_round == 3:
            val = HandEvaluator.evaluate_hand(self.hand,game_state.community_cards)
            if val == 1:
                return 'fold'
            elif val <= 3:
                return 'call'
            else:
                return 'raise'
        else:
            return 'call'