from collections import Counter
from core.card import Card

class HandEvaluator:
    HAND_RANKS = {
        "High Card": 1,
        "One Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10
    }
    
    @staticmethod
    def evaluate_hand(player_hand, community_cards):
        all_cards = player_hand + community_cards
        ranks = [card.rank for card in all_cards]
        suits = [card.suit for card in all_cards]
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        is_flush = any(count >= 5 for count in suit_counts.values())
        sorted_ranks = sorted([Card.RANKS.index(rank) for rank in ranks], reverse=True)
        is_straight = HandEvaluator.is_straight(sorted_ranks)
        
        if is_flush and is_straight and max(sorted_ranks) == Card.RANKS.index("A"):
            return HandEvaluator.HAND_RANKS["Royal Flush"]
        if is_flush and is_straight:
            return HandEvaluator.HAND_RANKS["Straight Flush"]
        if 4 in rank_counts.values():
            return HandEvaluator.HAND_RANKS["Four of a Kind"]
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            return HandEvaluator.HAND_RANKS["Full House"]
        if is_flush:
            return HandEvaluator.HAND_RANKS["Flush"]
        if is_straight:
            return HandEvaluator.HAND_RANKS["Straight"]
        if 3 in rank_counts.values():
            return HandEvaluator.HAND_RANKS["Three of a Kind"]
        if list(rank_counts.values()).count(2) == 2:
            return HandEvaluator.HAND_RANKS["Two Pair"]
        if 2 in rank_counts.values():
            return HandEvaluator.HAND_RANKS["One Pair"]
        
        return HandEvaluator.HAND_RANKS["High Card"]
    
    # @staticmethod
    # def is_straight(sorted_ranks):
    #     for i in range(len(sorted_ranks) - 4):
    #         if sorted_ranks[i] - sorted_ranks[i + 4] == 4:
    #             return True
    #     return False


    @staticmethod
    def is_straight(sorted_ranks):
        # 去重，防止重复牌误判为顺子
        unique_ranks = sorted(set(sorted_ranks), reverse=True)

        # 检查所有长度为 5 的连续窗口
        for i in range(len(unique_ranks) - 4):
            window = unique_ranks[i:i+5]
            if window[0] - window[4] == 4 and len(window) == 5:
                return True

        # 特殊情况：A-2-3-4-5（A=12, 2=0, 3=1, 4=2, 5=3）
        if set([12, 0, 1, 2, 3]).issubset(set(sorted_ranks)):
            return True

        return False
