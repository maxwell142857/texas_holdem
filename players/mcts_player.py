import random
from core.player import Player
from core.hand_evaluator import HandEvaluator
from core.card import Card

class MCTSPlayer(Player):
    def __init__(self, name, chips, num_simulations=500):
        super().__init__(name, chips)
        self.num_simulations = num_simulations

    def make_decision(self, game_state):
        if not self.is_active:
            return "fold"

        # 前两轮信息不足，直接 call 保守过渡
        if game_state.current_betting_round <= 1:
            return "call"

        # 模拟胜率评估
        win_rate = self._estimate_win_rate(game_state)

        # 基于胜率选择动作
        if win_rate > 0.8:
            return "raise"
        elif win_rate > 0.3:
            return "call"
        else:
            return "fold"

    def _estimate_win_rate(self, game_state):
        wins, ties, losses = 0, 0, 0
        deck = self._get_remaining_deck(game_state)

        for _ in range(self.num_simulations):
            deck_copy = deck.copy()
            random.shuffle(deck_copy)

            # 填满公共牌
            needed_community = 5 - len(game_state.community_cards)
            simulated_community = game_state.community_cards + [deck_copy.pop() for _ in range(needed_community)]

            # 模拟对手手牌
            opponent_hand = [deck_copy.pop(), deck_copy.pop()]

            my_score = HandEvaluator.evaluate_hand(self.hand, simulated_community)
            opp_score = HandEvaluator.evaluate_hand(opponent_hand, simulated_community)

            if my_score > opp_score:
                wins += 1
            elif my_score == opp_score:
                ties += 1
            else:
                losses += 1

        return (wins + 0.5 * ties) / self.num_simulations

    def _get_remaining_deck(self, game_state):
        used = set(self.hand + game_state.community_cards)
        full_deck = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        return [card for card in full_deck if card not in used]
