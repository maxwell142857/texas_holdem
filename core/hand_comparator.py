from core.hand_evaluator import HandEvaluator

class HandComparator:
    """
    用于比较两个玩家手牌 + 公共牌，返回胜者（或平局）
    """

    @staticmethod
    def rank_value(rank):
        rank_order = {
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return rank_order[rank]

    @staticmethod
    def compare(player1, player2, community_cards, prefer_first_if_tie=False, verbose=False):
        """
        比较两个玩家牌力，返回胜者的 player 对象。
        """
        rank1 = HandEvaluator.evaluate_hand(player1.hand, community_cards)
        rank2 = HandEvaluator.evaluate_hand(player2.hand, community_cards)

        if verbose:
            print("\n=== SHOWDOWN ===")
            print(f"Board: {[str(c) for c in community_cards]}")
            print(f"{player1.name}: {[str(c) for c in player1.hand]} => {rank1}")
            print(f"{player2.name}: {[str(c) for c in player2.hand]} => {rank2}")

        if rank1 > rank2:
            return player1
        elif rank2 > rank1:
            return player2

        # 平局时用 kicker 比较
        cards1 = sorted(player1.hand + community_cards, key=lambda c: HandComparator.rank_value(c.rank), reverse=True)
        cards2 = sorted(player2.hand + community_cards, key=lambda c: HandComparator.rank_value(c.rank), reverse=True)

        for c1, c2 in zip(cards1[:5], cards2[:5]):
            val1 = HandComparator.rank_value(c1.rank)
            val2 = HandComparator.rank_value(c2.rank)
            if val1 > val2:
                return player1
            elif val2 > val1:
                return player2

        return player1 if prefer_first_if_tie else None
