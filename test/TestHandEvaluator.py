import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.hand_evaluator import HandEvaluator
from core.card import Card

class TestHandEvaluator(unittest.TestCase):

    def setUp(self):
        self.C = lambda s, r: Card(s, r)

    def test_high_card(self):
        hand = [self.C("♠", "A"), self.C("♥", "9")]
        board = [self.C("♣", "2"), self.C("♦", "5"), self.C("♣", "7"), self.C("♣", "J"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["High Card"])

    def test_one_pair(self):
        hand = [self.C("♠", "A"), self.C("♥", "A")]
        board = [self.C("♣", "2"), self.C("♦", "5"), self.C("♣", "7"), self.C("♣", "J"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["One Pair"])

    def test_two_pair(self):
        hand = [self.C("♠", "A"), self.C("♥", "5")]
        board = [self.C("♣", "A"), self.C("♦", "5"), self.C("♣", "7"), self.C("♣", "J"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Two Pair"])

    def test_three_of_a_kind(self):
        hand = [self.C("♠", "A"), self.C("♥", "A")]
        board = [self.C("♣", "A"), self.C("♦", "5"), self.C("♣", "7"), self.C("♣", "J"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Three of a Kind"])

    def test_straight(self):
        hand = [self.C("♠", "6"), self.C("♥", "7")]
        board = [self.C("♣", "8"), self.C("♦", "9"), self.C("♣", "10"), self.C("♣", "2"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Straight"])

    def test_straight_low_ace(self):
        hand = [self.C("♠", "A"), self.C("♥", "2")]
        board = [self.C("♣", "3"), self.C("♦", "4"), self.C("♣", "5"), self.C("♣", "10"), self.C("♦", "J")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Straight"])

    def test_flush(self):
        hand = [self.C("♣", "2"), self.C("♣", "6")]
        board = [self.C("♣", "9"), self.C("♣", "10"), self.C("♣", "3"), self.C("♣", "Q"), self.C("♦", "7")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Flush"])

    def test_full_house(self):
        hand = [self.C("♠", "K"), self.C("♥", "K")]
        board = [self.C("♣", "K"), self.C("♦", "3"), self.C("♣", "3"), self.C("♣", "7"), self.C("♦", "9")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Full House"])

    def test_four_of_a_kind(self):
        hand = [self.C("♠", "9"), self.C("♥", "9")]
        board = [self.C("♣", "9"), self.C("♦", "9"), self.C("♣", "3"), self.C("♣", "7"), self.C("♦", "J")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Four of a Kind"])

    def test_straight_flush(self):
        hand = [self.C("♣", "8"), self.C("♣", "9")]
        board = [self.C("♣", "10"), self.C("♣", "J"), self.C("♣", "Q"), self.C("♣", "2"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Straight Flush"])

    def test_royal_flush(self):
        hand = [self.C("♠", "A"), self.C("♠", "K")]
        board = [self.C("♠", "Q"), self.C("♠", "J"), self.C("♠", "10"), self.C("♣", "2"), self.C("♦", "3")]
        result = HandEvaluator.evaluate_hand(hand, board)
        self.assertEqual(result, HandEvaluator.HAND_RANKS["Royal Flush"])

    def test_not_a_straight_due_to_missing_6(self):
        # 玩家手牌：9♠, 7♠
        hand = [self.C("♠", "9"), self.C("♠", "7")]

        # 公共牌：8♦, 5♣, 5♥, 2♦, K♣
        board = [self.C("♦", "8"), self.C("♣", "5"), self.C("♥", "5"),
                self.C("♦", "2"), self.C("♣", "K")]

        result = HandEvaluator.evaluate_hand(hand, board)

        # 预期是 "One Pair"，因为有两张 5
        self.assertEqual(result, HandEvaluator.HAND_RANKS["One Pair"])


    def test_valid_straight_9_to_5(self):
        # 手牌：♠9, ♣7
        hand = [self.C("♠", "9"), self.C("♣", "7")]

        # 公共牌：♥8, ♦6, ♠5, ♦2, ♠Q
        board = [self.C("♥", "8"), self.C("♦", "6"), self.C("♠", "5"),
                self.C("♦", "2"), self.C("♠", "Q")]

        result = HandEvaluator.evaluate_hand(hand, board)

        self.assertEqual(result, HandEvaluator.HAND_RANKS["Straight"])


if __name__ == "__main__":
    unittest.main()
