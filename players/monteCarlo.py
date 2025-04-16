import random
from core.hand_evaluator import HandEvaluator
from core.player import Player
from core.card import Card

class MonteCarlo(Player):
    def make_decision(self, game_state, simulations=500):
        if game_state.current_betting_round <= 1:
            return "call"
        
        deck = self._get_remaining_deck(game_state)
        wins = 0
        ties = 0
        losses = 0

        for _ in range(simulations):
            deck_copy = deck.copy()
            random.shuffle(deck_copy)

            needed_community = 5 - len(game_state.community_cards)
            simulated_community = game_state.community_cards + [deck_copy.pop() for _ in range(needed_community)]

            # 模拟一个对手手牌
            simulated_opponent_hand = [deck_copy.pop(), deck_copy.pop()]

            my_score = HandEvaluator.evaluate_hand(self.hand, simulated_community)
            opponent_score = HandEvaluator.evaluate_hand(simulated_opponent_hand, simulated_community)

            if my_score > opponent_score:
                wins += 1
            elif my_score == opponent_score:
                ties += 1
            else:
                losses += 1

        win_rate = (wins + ties * 0.5) / simulations

        if win_rate > 0.8:
            return "raise"
        elif win_rate > 0.2:
            return "call"
        else:
            return "fold"

    def _get_remaining_deck(self, game_state):
        used_cards = self.hand + game_state.community_cards
        full_deck = [Card(suit, rank) for rank in Card.RANKS for suit in Card.SUITS]
        return [card for card in full_deck if card not in used_cards]

